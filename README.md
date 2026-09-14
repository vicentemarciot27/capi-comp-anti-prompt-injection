# Prompt Injection Scanner

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

Uma atividade vira uma árvore, e cada nó passa pelo mesmo detector:

```txt
Trabalho 5
├── description
├── link → página → texto escondido
├── Google Form → título, descrição, perguntas
└── material.zip
    ├── instructions.pdf → texto, metadata, annotations, imagem → OCR
    └── readme.txt
```

O resultado carrega a proveniência completa, não só o rótulo:

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

Um comando, um processo, termina no fim. Não existe daemon com todos os tokens
em memória.

## Deploy

O CLI é um processo que roda e termina, então qualquer máquina com cron serve.
Em ordem de preferência:

### VM própria (Oracle always-free, servidor da Rede, ITA Junior)

```cron
*/30 * * * * cd /opt/scanner && ./venv/bin/scanner scan-due >> scan.log 2>&1
```

É a opção mais simples e a melhor para o classificador local: o Prompt Guard
2 22M fica em disco e carregado em RAM entre execuções, sem cold start e sem
baixar o modelo a cada run. A VM always-free da Oracle é ARM.

Deploy self hosted tem a vantagem de poder rodar um LLM local mais reliably.

### Cloud Run Job + Cloud Scheduler

Um Scheduler dispara um endpoint que lê `scan-due` e cria um Job por curso
vencido. Um Scheduler serve todos os cursos; não é um por curso.

```txt
Cloud Scheduler (1 job, a cada 30-60 min)
        │
        ▼
    dispatcher  →  scanner scan-due
        │
        ├── Cloud Run Job (course A)
        ├── Cloud Run Job (course B)
        └── Cloud Run Job (course C)
```

Vale quando o isolamento por curso e a gestão de segredos compensarem o custo
de operar. Cloud Scheduler inclui 3 jobs sem custo por billing account, e Cloud
Run tem franquia mensal de CPU e memória, mas exige billing configurado e não é
garantia de custo zero.

### GitHub Actions cron

Terceira opção, para não manter máquina nenhuma. Runners padrão são gratuitos
em repositório público; privado tem franquia de minutos conforme o plano. Com
dados de Classroom, prefira VM ou Cloud Run.

### Comum a todos

O scan é incremental: recurso com mesmo `updateTime`/`md5Checksum` e mesmas
versões de extractor e detector é pulado sem download. Subir só
`DETECTOR_VERSION` reprocessa o texto já extraído, sem baixar o PDF de novo.

Segredos: refresh token cifrado com Fernet no SQLite, chave em variável de
ambiente. Funciona igual em VM e em Cloud Run. Secret Manager inclui 6 versões
ativas sem custo por billing account, o que serve para 2 ou 3 usuários; um
secret por refresh token não escala para centenas de alunos.

## Estado

Placeholders. Apenas `scanner/core/models.py` e o `SCHEMA` em `scanner/db.py`
têm conteúdo; o resto levanta `NotImplementedError`.

`python3 tests/test_detect.py` é a especificação executável do detector e falha
até `detect.py` existir.

## Restrições

Persistimos refresh token cifrado, nunca access token. O extractor abre
arquivos hostis: em produção roda em container separado, sem credencial e sem
rede.

`drive.readonly` é um scope restricted na Google e exige verificação do app.

## Fora de escopo

- Archives e PDFs criptografados: não inspecionados, reportados como
  `SCAN_INCOMPLETE`.
- Páginas que só montam o conteúdo via JavaScript.
- Garantia de detectar qualquer prompt injection. O scanner reporta o que
  cobriu e o que não conseguiu abrir.
