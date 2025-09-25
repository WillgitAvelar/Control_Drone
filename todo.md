## Tarefas para identificar problemas e erros

- [x] Verificar a estrutura de pastas esperada para arquivos estáticos.
- [x] Analisar a lógica de conexão do drone em `drone_control.py`.
- [x] Avaliar a segurança da comunicação com o drone (UDP sem autenticação/criptografia).
- [x] Verificar a consistência entre o frontend (`index.html`) e o backend (`drone_control.py`).
- [x] Padronizado o método de inicialização da aplicação (Gunicorn via `procfile.py`, `run.py` removido).
- [x] Identificar a ausência de um diretório `static`.
- [x] Removida a importação de `flask_sqlalchemy` sem uso aparente.


