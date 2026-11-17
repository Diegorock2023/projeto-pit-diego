# Sistema de Cadastro de Pessoas — PIT

Aplicação web de demonstração acadêmica com operações CRUD (criar, listar, editar e excluir), validação de dados e banco SQLite.

## Arquitetura MVC
- **Model:** tabela SQLite `pessoas` e operações SQL em `app.py`.
- **View:** templates Jinja2 em `templates/` e CSS em `static/`.
- **Controller:** rotas Flask em `app.py`.

Para um projeto didático pequeno, Model e Controller estão no mesmo arquivo, mas as responsabilidades são identificáveis.

## Executar
1. Instale Python 3.10 ou superior.
2. Abra um terminal nesta pasta.
3. Execute `python -m pip install -r requirements.txt`.
4. Execute `python app.py`.
5. Acesse `http://127.0.0.1:5000` no navegador.

## Testes automatizados
Execute `python -m unittest -v test_app.py`.

## Publicação e privacidade
O sistema funciona **localmente**. Não há hospedagem pública configurada. Para publicar, configure uma hospedagem Python/Flask, uma chave secreta segura, proteção CSRF, autenticação e controles de privacidade. Não insira dados pessoais reais durante demonstrações públicas.

## Entregas acadêmicas ainda necessárias
Publicar o repositório GitHub, realizar testes com cinco colegas, registrar evidências reais, gravar vídeo narrado inicial (mínimo 5 minutos) e vídeo de correções (até 5 minutos), preencher os links no template.
