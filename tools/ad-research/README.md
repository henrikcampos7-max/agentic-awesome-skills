# Análise de anúncios e VSLs dos EUA

O GitHub Actions executa a análise no runner Linux, com os modelos e as bibliotecas instalados durante a execução. Este repositório público guarda código, exemplos e referências públicas. Para campanhas próprias, chame o workflow reutilizável de um repositório privado.

## Rodar no GitHub

Em **Actions → Análise de anúncios e VSLs → Run workflow** na branch principal, gere o relatório da [pesquisa inicial](research-us.md), sem chave nem dados privados.

Para campanhas próprias, hospede o ZIP em armazenamento com URL HTTPS assinada. No repositório **privado**, cadastre a URL no secret `AD_RESEARCH_INPUT_URL`. Crie um workflow chamador como o exemplo abaixo, substituindo os dois valores `SHA_COMPLETO` pelo mesmo SHA de 40 caracteres do commit publicado.

```yaml
name: Análise privada de campanhas
on: workflow_dispatch
permissions:
  contents: read
jobs:
  analyze:
    uses: henrikcampos7-max/agentic-awesome-skills/.github/workflows/ad-research.yml@SHA_COMPLETO
    with:
      analyzer_ref: SHA_COMPLETO
      ai: false
    secrets:
      AD_RESEARCH_INPUT_URL: ${{ secrets.AD_RESEARCH_INPUT_URL }}
```

Para usar IA, defina `ai: true` e mapeie também `OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}` no workflow chamador. A API recebe a copy, a transcrição, amostras visuais e os fatos da oferta para gerar o roteiro bilíngue. Essa opção tem custo da API. As compras, o gasto, a receita e a URL assinada ficam fora do pedido à API.

Abra **analise-anuncios-vsls** em **Artifacts** no repositório onde a execução foi iniciada. Leia `relatorio.md` e use `evidencias.json` para consultar os dados e as marcações de tempo. O GitHub guarda os artefatos por 14 dias, com acesso de quem pode ler o repositório.

```text
ads.csv
metrics.csv       opcional
offer.json        opcional
media/
  meu-criativo-01.mp4
  minha-vsl-01.mp4
```

### Catálogo, mídia e dados de venda

- [ads.template.csv](examples/ads.template.csv) é o modelo do catálogo. Use um ID único, um nicho consistente, mercado `US` quando observado, plataforma `Facebook` quando identificada e tipo `ad`, `vsl` ou `offer`. Use datas AAAA-MM-DD, URL da referência, página de destino e fonte verificável. Em `copy`, cole ou descreva o trecho necessário para a análise. Informe `distinct_variants` somente quando conferido. Use `observed` ou `active` para observações documentadas, `reference` para referências com confirmação parcial e `archived_reference` para registros históricos.
- Use o ID do catálogo como nome do vídeo, por exemplo `media/meu-criativo-01.mp4`. A VSL precisa de seu próprio ID. O runner aceita MP4, MOV, MKV e WebM, até oito vídeos por execução e ZIP de até 350 MiB. Para VSLs longas, use lotes menores ou trechos relevantes. A extração marca falas, cortes e texto encontrado em quadros amostrados.
- [metrics.template.csv](examples/metrics.template.csv) recebe os dados autorizados do Ads Manager ou do seu sistema de atribuição. Padronize a exportação com uma linha por ID e janela, moeda, atribuição, mercado e plataforma. Use o mesmo mercado e plataforma que em `ads.csv`. Insira números com ponto decimal, mantenha campos sem medição vazios e use zero quando medido. Compare criativos do mesmo nicho, tipo e janela. Para VSLs, use IDs por versão no tracker para atribuir a compra à versão exibida. Para campanhas Facebook US, exporte métricas com o recorte correspondente.
- [offer.template.json](examples/offer.template.json) informa o produto da nova copy, audiência, benefícios verificáveis, material de prova, idioma, formato e CTA. Use fatos da sua oferta para produzir uma adaptação com a estrutura e o ritmo da referência e com falas, cenas e visuais próprios.

### Como ler a classificação

Compras atribuídas, custo por compra e ROAS vêm de `metrics.csv`. As referências públicas são ordenadas por duração observada e quantidade de variantes documentadas. O relatório mostra mercado, origem e lacunas. Dados de ofertas de afiliados são úteis para selecionar funis a estudar. Identificar o anúncio ou a VSL que gerou a compra exige atribuição por ID.

A coleta de anúncios comerciais dos EUA começa na [Biblioteca da Meta](https://www.facebook.com/ads/library/), pela seleção de referências, ou por uma exportação autorizada que siga o formato do catálogo. A [API pública da Biblioteca](https://www.facebook.com/ads/library/api/) tem cobertura limitada para anúncios comerciais que rodam exclusivamente nos EUA. O workflow automatiza a análise depois que a amostra está na nuvem.

## Bibliotecas e fontes de integração

| Código upstream | Uso |
| --- | --- |
| [OpenAI Whisper](https://github.com/openai/whisper), [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) | ASR com marcação de tempo via implementação Faster Whisper em CPU. MIT. |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Detecção de transições de plano via `scenedetect-headless`. BSD-3-Clause. |
| [Tesseract](https://github.com/tesseract-ocr/tesseract) | OCR de textos em inglês nos frames. Apache 2.0. |
| [FFmpeg e FFprobe](https://ffmpeg.org/) | Leitura, extração de áudio e amostragem de quadros. A licença depende do build instalado. |
| [Meta Business SDK](https://github.com/meta/facebook-python-business-sdk) | Referência para integrar contas autorizadas pela Marketing API. O fluxo atual importa métricas por CSV. |

Os pins das dependências Python estão em [requirements-media.txt](requirements-media.txt). Vídeos e pesos de modelo são processados como arquivos temporários do runner.

## Ferramentas dos seus repositórios

| Fonte | Uso nesta automação |
| --- | --- |
| [Trafego Pack](https://github.com/henrikcampos7-max/trafego-pack/tree/a8140c4c983db809e9def29cde14f7aa37cfbf70) | Pesquisa de concorrentes, hipóteses de ângulo e checklist antes do teste. O relatório liga cada referência à fonte e descreve o que observar. |
| [Arquiteto de Ofertas](https://github.com/henrikcampos7-max/arquiteto-de-ofertas/blob/398e52caaaa04238bb40a31a0a63e203cfd4eebb/arquiteto-de-ofertas.md) | Análise da sequência da VSL, continuidade entre promessa do anúncio e página, mapa de cenas e briefing de copy. |
| [Ad Creative](../../skills/ad-creative/SKILL.md), [Competitor Profiling](../../skills/competitor-profiling/SKILL.md), [A/B Test Setup](../../skills/ab-test-setup/SKILL.md) | Variações de gancho com a mesma oferta, registro da evidência por concorrente e um teste com uma variável por vez. |

Esses guias informam o briefing. O workflow usa código próprio para processar os arquivos e produzir o ranking.
