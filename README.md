# Control Drone - Deploy no Render

## Problemas Corrigidos

### 1. Estrutura de Arquivos
- Criada pasta `routes/` para organizar os blueprints
- Movido `index.html` para pasta `static/`
- Adicionado `__init__.py` na pasta routes

### 2. Configuração do Flask
- Adicionado Flask-CORS para permitir requisições cross-origin
- Adicionada rota `/healthz` para health check do Render
- Configurado para usar a variável de ambiente `PORT`

### 3. Dependências
- Adicionado `flask-cors==5.0.0` no requirements.txt

## Configuração no Render

### Opção 1: Remover Procfile e configurar diretamente
1. **Delete o Procfile** do seu repositório
2. No painel do Render, configure:
   - **Start Command**: `gunicorn main:app --host=0.0.0.0 --port=$PORT`
   - **Health Check Path**: `/healthz`

### Opção 2: Usar render.yaml (Recomendado)
1. Adicione o arquivo `render.yaml` na raiz do projeto
2. O Render detectará automaticamente as configurações

## Estrutura Final do Projeto
```
projeto/
├── main.py
├── requirements.txt
├── render.yaml
├── routes/
│   ├── __init__.py
│   └── drone_control.py
├── static/
│   └── index.html
├── mock_drone.py
├── reverse_engineering_tool.py
└── run_waitress.py
```

## Comandos para Testar Localmente
```bash
pip install -r requirements.txt
python main.py
```

O servidor estará disponível em: http://localhost:5000

