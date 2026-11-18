"""End-to-end media check using a synthetic video created by the cloud runner."""
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from ad_research.media import analyze_media


with TemporaryDirectory() as temp:
    root = Path(temp)
    audio = root / "speech.wav"
    video = root / "demo.mp4"
    subprocess.run(["espeak-ng", "-v", "en-us", "-s", "135", "-w", str(audio),
                    "This notebook keeps your weekly meal plan simple."], check=True)
    subprocess.run([
        "ffmpeg", "-nostdin", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=480x640:d=2:r=24",
        "-f", "lavfi", "-i", "color=c=navy:s=480x640:d=4:r=24", "-i", str(audio),
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,drawtext=text='MEAL PLANNER':"
        "fontcolor=white:fontsize=48:x=(w-tw)/2:y=(h-th)/2[v]",
        "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(video),
    ], check=True)
    evidence = analyze_media(video, "base.en", include_frames=True)
    assert not evidence["warnings"], evidence["warnings"]
    assert evidence["audio_present"] and evidence["transcript"], evidence
    assert len(evidence["scenes"]) >= 2, evidence["scenes"]
    assert any("MEAL PLANNER" in item["text"].upper() for item in evidence["screen_text"]), evidence["screen_text"]
    assert evidence["frames"] and evidence["frames"][0]["data_url"].startswith("data:image/jpeg;base64,")
    print("Mídia sintética validada: transcrição, dois planos, OCR e amostras JPEG.")
