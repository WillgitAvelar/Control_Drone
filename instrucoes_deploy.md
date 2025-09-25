# Instruções para Deploy no Render

## Passos para Corrigir o Deploy

### 1. Atualizar o Repositório GitHub
Substitua os arquivos do seu repositório pelos arquivos corrigidos desta pasta.

### 2. Configurar o Render (Escolha uma opção)

#### Opção A: Configuração Manual no Painel
1. Acesse o painel do Render
2. Vá em **Settings** > **Build & Deploy**
3. **REMOVA** o Procfile do seu repositório
4. Configure:
   - **Start Command**: `gunicorn main:app --host=0.0.0.0 --port=$PORT`
   - **Health Check Path**: `/healthz`

#### Opção B: Usar render.yaml (Mais Simples)
1. Adicione o arquivo `render.yaml` na raiz do projeto
2. Faça commit e push
3. O Render detectará automaticamente

### 3. Verificar Configurações Atuais
No seu painel do Render, certifique-se que:
- **Build Command**: `pip install -r requirements.txt` ✓
- **Start Command**: `gunicorn main:app --host=0.0.0.0 --port=$PORT`
- **Health Check Path**: `/healthz`

### 4. Fazer o Deploy
1. Faça commit das alterações
2. Push para o branch main
3. O Render fará o deploy automaticamente

## O que foi Corrigido

### Problema Principal
- **Antes**: Procfile com `web: gunicorn main:app` causava erro bash
- **Depois**: Start command direto no Render ou via render.yaml

### Estrutura de Arquivos
- **Antes**: Import `from routes.drone_control` falhava
- **Depois**: Pasta `routes/` criada com `__init__.py`

### Arquivos Estáticos
- **Antes**: `index.html` na raiz, Flask procurava em `static/`
- **Depois**: `index.html` movido para `static/`

### CORS e Health Check
- **Adicionado**: Flask-CORS para requisições cross-origin
- **Adicionado**: Rota `/healthz` para monitoramento do Render

## Teste Local
```bash
cd projeto_corrigido
pip install -r requirements.txt
python main.py
```

Acesse: http://localhost:5000

