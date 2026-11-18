"""Extract time-coded production evidence from an authorized media file."""

import base64
from functools import lru_cache
from fractions import Fraction
import json
import math
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import wave


MAX_DURATION_SECONDS = 7_200
MAX_FILE_BYTES = 1_000_000_000
MAX_OCR_FRAMES = 32
MAX_VISUAL_FRAMES = 12
SUPPORTED_FORMATS = {"mov", "matroska", "avi", "flv", "mpeg", "mpegts", "ogg"}


def _run(args: list[str], timeout: int, input_data: bytes | None = None) -> bytes:
    try:
        result = subprocess.run(
            args, input=input_data, capture_output=True, timeout=timeout, check=True
        )
    except FileNotFoundError as error:
        raise RuntimeError(f"Executable unavailable: {args[0]}") from error
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"{args[0]} exceeded {timeout} seconds") from error
    except subprocess.CalledProcessError as error:
        diagnostic = error.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"{args[0]}: {diagnostic[:400]}") from error
    return result.stdout


def _fps(value: str) -> float | None:
    try:
        fps = float(Fraction(value))
    except (ValueError, ZeroDivisionError):
        return None
    return round(fps, 3) if fps > 0 else None


def _duration(*values: str | None) -> float:
    for value in values:
        try:
            duration = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(duration) and duration > 0:
            return duration
    raise ValueError("The video duration could not be read")


def _probe(path: Path) -> tuple[dict, int]:
    data = json.loads(_run(
        [
            "ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe",
            "-show_format", "-show_streams", "-of", "json", str(path),
        ],
        timeout=30,
    ))
    format_info = data.get("format", {})
    formats = set(format_info.get("format_name", "").split(","))
    if not formats.intersection(SUPPORTED_FORMATS):
        raise ValueError("Provide a self-contained MP4, MOV, MKV, WebM or AVI video file")

    streams = data.get("streams", [])
    video = next(
        (
            stream for stream in streams
            if stream.get("codec_type") == "video"
            and not stream.get("disposition", {}).get("attached_pic")
        ),
        None,
    )
    if video is None:
        raise ValueError("The file does not contain a playable video stream")

    duration = _duration(format_info.get("duration"), video.get("duration"))
    if duration > MAX_DURATION_SECONDS:
        raise ValueError("Video exceeds the two-hour analysis limit")

    width, height = video.get("width"), video.get("height")
    display_rotation = next(
        (
            item["rotation"] for item in video.get("side_data_list", [])
            if "rotation" in item
        ),
        0,
    )
    if abs(display_rotation) % 180 == 90:
        width, height = height, width
    return {
        "duration_seconds": round(duration, 3),
        "width": width,
        "height": height,
        "fps": _fps(video.get("avg_frame_rate", "0/0")),
        "audio_present": any(stream.get("codec_type") == "audio" for stream in streams),
    }, video["index"]


@lru_cache(maxsize=1)
def _transcription_model(model_name: str):
    from faster_whisper import WhisperModel

    return WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=2)


def _transcribe(path: Path, model_name: str, duration: float) -> list[dict]:
    import numpy as np

    # Normalize the first audio stream so the ASR model works with one local WAV.
    with TemporaryDirectory(prefix="ad-audio-") as directory:
        audio = Path(directory) / "audio.wav"
        _run(
            [
                "ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
                "-i", str(path), "-map", "0:a:0", "-vn", "-t", str(duration),
                "-af", "aresample=async=1:first_pts=0", "-ac", "1", "-ar", "16000",
                "-c:a", "pcm_s16le", str(audio),
            ],
            timeout=240,
        )
        # FFmpeg already produced 16 kHz mono PCM. Pass the samples directly to Whisper.
        with wave.open(str(audio), "rb") as wav:
            samples = np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
        if not samples.size:
            return []
        segments, _info = _transcription_model(model_name).transcribe(samples, beam_size=3, vad_filter=True)
        return [
            {
                "start_seconds": round(segment.start, 3),
                "end_seconds": round(segment.end, 3),
                "text": segment.text.strip(),
            }
            for segment in segments
            if segment.text.strip()
        ]


def _detect_scenes(path: Path, duration: float) -> list[dict]:
    from scenedetect import ContentDetector, SceneManager, open_video
    from scenedetect.video_stream import VideoOpenFailure

    try:
        video = open_video(str(path), backend="opencv")
    except VideoOpenFailure as error:
        raise RuntimeError(str(error)) from error
    manager = SceneManager()
    manager.add_detector(ContentDetector())
    frame_skip = 2 if duration > 600 else 0
    try:
        manager.detect_scenes(video, duration=duration, frame_skip=frame_skip)
    finally:
        video.capture.release()
    cuts = [
        (start.get_seconds(), min(duration, end.get_seconds()))
        for start, end in manager.get_scene_list(start_in_scene=True)
    ]
    return [
        {"start_seconds": round(start, 3), "end_seconds": round(end, 3)}
        for start, end in cuts if end > start
    ]


def _sample_times(duration: float, scenes: list[dict]) -> list[float]:
    # Favor the hook, then sample the full video and the first few scene changes.
    latest = max(0, duration - 0.15)
    times = [0.25, 0.85, 1.5, 2.5, 3.5, 5, 7, 10, 15]
    times.extend(duration * index / 16 for index in range(1, 16))
    times.extend(scene["start_seconds"] + 0.2 for scene in scenes[1:9])
    return sorted({
        round(min(time, latest), 3) for time in times[:MAX_OCR_FRAMES] if time < duration
    } | {round(min(0.25, latest), 3)})


def _jpeg_at(path: Path, stream_index: int, timestamp: float) -> bytes:
    return _run(
        [
            "ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
            "-ss", str(timestamp), "-i", str(path), "-map", f"0:{stream_index}",
            "-frames:v", "1", "-vf", "scale=960:960:force_original_aspect_ratio=decrease",
            "-c:v", "mjpeg", "-q:v", "5", "-f", "image2pipe", "pipe:1",
        ],
        timeout=20,
    )


def _screen_text(image: bytes) -> str:
    result = _run(
        ["tesseract", "stdin", "stdout", "-l", "eng", "--psm", "11"],
        timeout=15,
        input_data=image,
    )
    return "\n".join(line.strip() for line in result.decode("utf-8").splitlines() if line.strip())


def analyze_media(path: Path, model_name: str, include_frames: bool = False) -> dict:
    """Return speech, scene boundaries and sample-based on-screen text for one video."""
    path = path.resolve(strict=True)
    if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("Provide a single video file up to 1 GB")

    report, stream_index = _probe(path)
    duration = report["duration_seconds"]
    warnings = []
    try:
        transcript = _transcribe(path, model_name, duration) if report["audio_present"] else []
    except (ImportError, OSError, RuntimeError, ValueError) as error:
        transcript = []
        warnings.append(f"Speech transcription unavailable: {error}")
    try:
        scenes = _detect_scenes(path, duration)
    except (ImportError, OSError, RuntimeError, ValueError) as error:
        scenes = []
        warnings.append(f"Scene detection unavailable: {error}")

    times = _sample_times(duration, scenes)
    frame_indices = {
        round(index * (len(times) - 1) / (MAX_VISUAL_FRAMES - 1))
        for index in range(MAX_VISUAL_FRAMES)
    }
    frames = []
    text_samples = []
    sample_failure = None
    for index, timestamp in enumerate(times):
        try:
            image = _jpeg_at(path, stream_index, timestamp)
            if not image:
                continue
            if include_frames and index in frame_indices:
                data = base64.b64encode(image).decode("ascii")
                frames.append({
                    "timestamp_seconds": timestamp,
                    "data_url": f"data:image/jpeg;base64,{data}",
                })
            text = _screen_text(image)
            if text and (not text_samples or text != text_samples[-1]["text"]):
                text_samples.append({"timestamp_seconds": timestamp, "text": text})
        except (RuntimeError, UnicodeError) as error:
            sample_failure = str(error)
    if sample_failure:
        warnings.append(f"Some visual samples were unavailable: {sample_failure}")

    return {
        **report,
        "transcript": transcript,
        "scenes": scenes,
        "screen_text": text_samples,
        "frames": frames,
        "warnings": warnings,
    }
