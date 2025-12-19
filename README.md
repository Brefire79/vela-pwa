# Vela PWA - Calculadora Offline (Flask)

Uma PWA simples construída com Flask que oferece uma calculadora que funciona offline via Service Worker.

## Como rodar

1. Crie um virtualenv (opcional, mas recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. Inicie o servidor Flask:

```powershell
python app.py
```

Acesse em http://localhost:5000.

## Estrutura

- `app.py`: servidor Flask e rotas
- `templates/index.html`: página principal com UI da calculadora
- `static/js/calculator.js`: lógica da calculadora
- `static/css/styles.css`: estilos básicos
- `service-worker.js`: cache e funcionamento offline
- `manifest.json`: metadados PWA

## Deploy

Este repositório não está amarrado a um provedor específico. Para deploy estático, sirva `app.py` com um servidor Python (gunicorn/uwsgi) atrás de um proxy. Para plataformas como Render/railway, configure o comando de start para `python app.py`.
