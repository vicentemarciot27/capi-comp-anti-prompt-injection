#CAPI - Comp Anti Prompt Injection

Um detector de prompt injection :P

Procura instruções suspeitas, texto escondido e ofuscação em atividades e
materiais do Google Classroom, em URLs e em arquivos enviados manualmente.

A detecção fica em `scanner/core/`, que não importa nada do Google. Classroom é
apenas um adapter em `scanner/connectors/`.

## Pipeline

```txt
  Classroom / URL / upload
            │
            ▼
   árvore de artifacts        scanner/scan.py
            │
            ▼
      extractors              scanner/core/extract/
   pdf zip docx html img
            │
            ▼
   canonicalização            scanner/core/canonicalize.py
   unicode base64 hidden
            │
            ▼
        ensemble              scanner/core/detect.py
   regras + classificador local + LLM judge opcional
            │
            ▼
   Finding: risco + trecho + caminho até o conteúdo
```

Constroi-se a arvore da atividade e todas as folhas passam pelo detector:

```txt
Trabalho 5
├── description
├── link → página → texto escondido
├── Google Form → título, descrição, perguntas
└── material.zip
    ├── instructions.pdf → texto, metadata, annotations, imagem → OCR
    └── readme.txt
```

O resultado mostra a evidência de injeção / a fonte da suspeita:

```txt
HIGH  Trabalho 5 > material.zip > slides.pdf > page 7 > annotation
      "Ignore previous instructions and..."
```

## Uso

```bash
pip install -e .
scanner connect --redirect-uri http://localhost:8080/oauth/callback
scanner list-courses --credential 1
scanner scan-course 1
scanner scan-url https://exemplo.com/atividade
scanner scan-file material.zip
scanner scan-due          # chamado pelo cron / Cloud Run Job
```

## Deploy

O CLI roda e termina, então qualquer máquina com cron serve: uma VM própria
(Oracle always-free, servidor da Rede, ITA Junior), Cloud Run Job com Cloud
Scheduler, ou cron do GitHub Actions. VM própria mantém o classificador local
em disco entre execuções, sem cold start. A Oracle always-free roda em ARM:
confirme antes que o `onnxruntime` tenha wheel para `aarch64`.

Scan incremental: recurso com mesmo `updateTime`/`md5Checksum` e mesma versão
de extractor/detector é pulado sem download.

Segredos: refresh token cifrado com Fernet, chave em variável de ambiente.

## Estado

Placeholders. Apenas `scanner/core/models.py` e o `SCHEMA` em `scanner/db.py`
têm conteúdo; o resto levanta `NotImplementedError`.

`python3 tests/test_detect.py` é a especificação executável do detector e falha
até `detect.py` existir.

## Restrições

O sistema guarda refresh token cifrado, nunca access token. O extractor abre
arquivos hostis: em produção roda em container separado, sem credencial e sem
rede.

`drive.readonly` exige verificação de app pela Google antes de liberar para
outros usuários.

## Fora de escopo

- Archives e PDFs criptografados: não inspecionados, reportados como
  `SCAN_INCOMPLETE`.
- Páginas que só montam o conteúdo via JavaScript.
- Garantia de detectar qualquer prompt injection. O scanner reporta o que
  cobriu e o que não conseguiu abrir.
