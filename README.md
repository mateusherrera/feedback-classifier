# AluMusic Feedback Classifier

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)](https://www.python.org/)


Este projeto é uma API RESTful desenvolvida com Flask e integrada à API da OpenAI, com o objetivo de classificar automaticamente feedbacks textuais deixados por usuários da plataforma AluMusic. Ele permite a ingestão segura de comentários, classificação inteligente via LLM, análise de tendências e geração de relatórios semanais.

O sistema foi construído com foco em paralelismo, autenticação via JWT, interface moderna para curadoria e painel público para insights em tempo real. Tudo isso orquestrado com Docker, Gunicorn, NGINX e CI/CD com Jenkins + GitHub Actions.

## Sumário

- [Ferramentas Utilizadas](#ferramentas-utilizadas)
- [Descrição do Projeto](#descrição-do-projeto)
- [Documentações](#documentações)
- [Como Rodar o Projeto](#como-rodar-o-projeto)
- [Testes e Métricas](#testes-e-métricas)
- [CI/CD](#cicd)
- [Painel e Relatórios](#painel-e-relatórios)
- [Resumo por E-mail](#resumo-por-e-mail)
- [Extra: Q&A Insights](#extra-qa-insights)


## Ferramentas Utilizadas

| Categoria      | Ferramenta                                                                               |
|----------------|------------------------------------------------------------------------------------------|
| Linguagem      | [Python 3.10+](https://www.python.org/)                                                  |
| Framework Web  | [Flask RESTful](https://flask-restful.readthedocs.io/en/latest/)                         |
| Banco de Dados | [PostgreSQL](https://www.postgresql.org/)                                                |
| ORM            | [SQLAlchemy](https://www.sqlalchemy.org/)                                                |
| Migrations     | [Flask-Migrate / Alembic](https://flask-migrate.readthedocs.io/)                         |
| Auth           | [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)                         |
| LLM API        | [OpenAI](https://platform.openai.com/docs)                                               |
| Servidor WSGI  | [Gunicorn](https://gunicorn.org/)                                                        |
| Reverse Proxy  | [NGINX](https://nginx.org/en/docs/)                                                      |
| Containers     | [Docker Compose](https://docs.docker.com/compose/)                                       |
| CI/CD          | [Jenkins](https://www.jenkins.io/) + [GitHub Actions](https://docs.github.com/actions)   |
| Testes         | [PyTest](https://docs.pytest.org/en/latest/)                                             |
