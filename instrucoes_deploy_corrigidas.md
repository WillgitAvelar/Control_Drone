# Instruções Corrigidas para Deploy no Render

## PROBLEMA IDENTIFICADO NO NOVO LOG

O erro agora é diferente:
```
gunicorn: error: unrecognized arguments: --host=0.0.0.0 --port=10000
```

**Causa**: O gunicorn não aceita `--host` e `--port` separados. Ele usa `--bind` para especificar host e porta juntos.

## SOLUÇÃO CORRIGIDA

### Opção 1: Configuração Manual no Painel do Render
1. Acesse **Settings** > **Build & Deploy**
2. Configure o **Start Command** como:
   ```
   gunicorn main:app --bind 0.0.0.0:$PORT
   ```

### Opção 2: Usar render.yaml Corrigido
Use o arquivo `render.yaml` corrigido que está nesta pasta:
```yaml
services:
  - type: web
    name: control-drone
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app --bind 0.0.0.0:$PORT
    healthCheckPath: /healthz
```

## COMANDOS CORRETOS PARA GUNICORN

❌ **INCORRETO** (causa o erro):
```
gunicorn main:app --host=0.0.0.0 --port=$PORT
```

✅ **CORRETO**:
```
gunicorn main:app --bind 0.0.0.0:$PORT
```

## PROGRESSO ATUAL

✅ Build funcionando (dependências instaladas corretamente)
✅ Flask-CORS adicionado
✅ Estrutura de arquivos corrigida
❌ Start command com sintaxe incorreta do gunicorn

## PRÓXIMOS PASSOS

1. Atualize o **Start Command** no painel do Render para:
   ```
   gunicorn main:app --bind 0.0.0.0:$PORT
   ```

2. OU substitua o `render.yaml` pelo arquivo corrigido

3. Faça um novo deploy

O deploy deve funcionar agora!

