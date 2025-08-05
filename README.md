# AluMusic Feedback Classifier
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![OpenAI API](https://img.shields.io/badge/OpenAI-API-brightgreen?logo=openai&logoColor=white)
![Model GPT‐3.5‐turbo](https://img.shields.io/badge/Model-gpt--3.5--turbo-blueviolet)
![License](https://img.shields.io/github/license/mateusherrera/feedback-classifier.svg)

Foi desenvolvida uma API RESTful em Flask, integrada à API da OpenAI, para classificar automaticamente os comentários da plataforma AluMusic. O sistema foi projetado para escalar desde o início, com processamento paralelo em lote e autenticação via JWT, assegurando segurança e performance.

Todo o ambiente está conteinerizado com Docker e servido por Gunicorn e NGINX, além de contar com uma pipeline de CI/CD orquestrada por Jenkins que aciona workflows no GitHub Actions, garantindo builds e testes automatizados.

## Sumário

- [Ferramentas Utilizadas](#ferramentas-utilizadas)
- [Descrição do Projeto](#descrição-do-projeto)
- [Documentação](#documentação)
- [Como Rodar o Projeto](#como-rodar-o-projeto)
- [Testes e Métricas (EVALs)](#testes-e-métricas-evals)
- [CI/CD](#cicd)
- [Painel e Relatórios](#painel-e-relátorios)
- [Resumo por E-mail](#resumo-por-e-mail)
- [Extra: Insights](#extra-insights)

## Ferramentas Utilizadas

| Categoria             | Ferramenta                                                                               |
|-----------------------|------------------------------------------------------------------------------------------|
| Linguagem             | [Python 3.10+](https://www.python.org/)                                                  |
| Web                   | [Flask](https://flask.palletsprojects.com/en/stable/#user-s-guide)                       |
| API                   | [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)                         |
| Migrations            | [Flask-Migrate / Alembic](https://flask-migrate.readthedocs.io/)                         |
| Auth                  | [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)                         |
| Banco de Dados        | [PostgreSQL](https://www.postgresql.org/)                                                |
| ORM                   | [SQLAlchemy](https://www.sqlalchemy.org/)                                                |
| LLM                   | [OpenAI](https://platform.openai.com/docs)                                               |
| Cache / Broker        | [Redis](https://redis.io/)                                                               |
| Tarefas Assíncronas   | [Celery](https://docs.celeryq.dev/en/stable/)                                            |
| Agendamento de Tarefas| [Celery Beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html)          |
| Envio de E-mail       | [Flask-Mail](https://flask-mail.readthedocs.io/en/latest/)                               |
| Servidor WSGI         | [Gunicorn](https://gunicorn.org/)                                                        |
| Reverse Proxy         | [NGINX](https://nginx.org/en/docs/)                                                      |
| Containers            | [Docker Compose](https://docs.docker.com/compose/)                                       |
| CI/CD                 | [Jenkins](https://www.jenkins.io/) + [GitHub Actions](https://docs.github.com/actions)   |
| Métricas & EVALs      | [scikit-learn](https://scikit-learn.org/stable/)                                         |
| Testes                | [PyTest](https://docs.pytest.org/en/latest/)                                             |

## Descrição do Projeto

Esse projeto se trata de um API REST, desenvolvida em Flask + Flask RESTful, com o objetivo de fornecer endpoints para analise e acopanhamento de tendencias nos cometário da AluMusic.

Para foram feitos:
1. Endpoint para classficação (unitário ou em lote) de comentário quanto a sua categoria.
2. Endpoint que fornece JSONs (atualizado a cada 60s) para contrução de 5 gráficos diferentes.
3. Interface simples e privada para consulta dos cometários classificados.
4. Resumo semanal dos  cometários enviado por e-mail aos stakeholders.
5. Método para avaliação dos dados classificados, considerando recall, precision e f1-score.
6. *Extra:* Endpoint para pergunta livre em linguagem natural. A resposta tem como base os últimos 3 relatórios semanais enviados.

## Documentação

## Como rodar o Projeto

## Testes e Métricas (EVALs)

## CI/CD

## Painel e Relátorios

## Resumo por E-mail

## Extra: Insights
