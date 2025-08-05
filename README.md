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
- [Como executar o Projeto](#como-executar-o-projeto)
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

### Overview

O repositório possui build e testes automatizados com Pytest e CI de Jenkins + Github Actions.

Para construção da API foi utilizado, principalmente, Flask. Para implantação são utilizados Docker, NGINX e Gunicorn.

Além disso, a persistência se dá com um PostgreSQL, cache com Redis e agendamento de tarefas com Celery Beat, todas essas já disponiveis no `docker-compose.yml`. A administração do Banco de Dados é feita em código com Flask-migrations e Object Relation Mapper (ORM) do SQLAlchemy.

### Docker Compose

O Docker Compose (`docker-compose.yml`) principal desse repositório sobe todos os serviços necessários para disponibilizar os recursos dessa API.

Entre os serviços temos os seguintes:

* `redis`: Serviço Redis para utilização de cache no Flask.
* `db`: Serviço respons ável por subir o PostgreSQL usado para persistência de dados.
* `api`: Serviço que sobe a API Flask, por meio do gunicorn. A api escuta a porta 5000 internamente, ou seja, a porta só escuta dentro do container.
* `celery worker`: Serviço responsável pelo envio do resumo semanal por e-mail (Dispara a função).
* `celery beat`: Serviço que agenda e dispara tarefas periódicas.
* `nginx`: Serviço de reverse proxy que recebe as requisições externas e as encaminha para a API Flask (porta 5000).

Neste repositório, ainda há um Docker Compose que pode ser usado para subir uma instância de Jenkins em `http://localhost:8080`. Ele está na pasta `jenkins/docker-compose.yml`.

### Nginx

O `nginx.conf` é o arquivo de configuração do NGINX para proxy reverso da API.

Esse serviço escuta a porta 443 e envia as requisições para localhost:5000 (Flask com Gunicorn). Além disso, ele está preparado para servir a API com certificado SSL, para mais informações verifique a seção: [Como executar o Projeto](#como-executar-o-projeto).

### Jenkins

Neste repositório, além do arquivo `Jenkinsfile` que aciona os testes via Github Actions, também há um `docker-compose.yml` na pasta `jenkins/` para subir uma instância de Jenkins em `http://localhost:8080/`. Mais a frente haverão instruções para sua configuração.

### PostgreSQL

O gerenciamento do banco em si acontence por meio do Docker, porém no diretório `db/` há o script para criação do Schema utilizado pela Flask. Esse script só é executado apenas na primeira vez que o build do serviço é feito e o volume de persistencia dos dado não existe ou está vazio.

### Flask

Aqui é onde está o código da API Flask, nela existem os seguintes modulos:
* `app/`: Módulo principal (raiz) do projeto, onde todos os outros módulos e arquivos estão presentes.
    * `app/main.py`: Arquivo principal da API Flask, onde o app flask é instanciados e os objetos de configuração são importados e definidos para o app.
    * `app/extensions.py`: Arquivo para instanciar extensões para o flask, como, `JWTManager()`, `Cache()`, `Mail()`, etc.
    * `app/config.py`: Arquivo para carregar e centralizar as variáveis de ambiente disponíveis no arquivo `.env`.
    * `app/tasks.py`: Arquivo para 'agendar' a execução de tarefas por meio do Celery. Onde o resumo semanal está implementado.
    * `app/evals.py`: Arquivo para implementar lógica com `scikit-learn` para calcular métricas do classificador de comentários.
    * `app/api/`: Módulo para agrupar arquivos referentes a roteamente e lógicas de endpoints do Flask.
        * `app/api/routes.py`: Arquivo para realizar o roteamento de endpoints. Difinição de rotas.
        * `app/api/resources/`: Módulo para agrupar lógicas de endpoints.
            * `app/api/resources/auth.py`: Arquivo para implementação de endpoints para autenticaçao JWT.
            * `app/api/resources/comentarios_export.py`: Arquivo para implementação de endpoint de exportação de comentários classificados em CSV.
            * `app/api/resources/comentarios.py`: Arquivo para implementação de endpoints de listagem e criação de comentários classificados.
            * `app/api/resources/insights.py`: Arquivo para implementação de endpoint para criação de resposta, via LLM, para pergunta feita via requisição, usando resumos semanais anteriores como contexto.
            * `app/api/resources/relatorios.py`: Arquivo para implementação de endpoint de geração de relatórios (JSON de gráficos).
    * `app/models/`: Módulo para definiição de models do Flask (esses models refletem as tabelas no PostgreSQL).
        * `app/models/comentario.py`: Arquivo para definir classe e atribuitos do model de comentários classificados.
        * `app/models/resumo.py`: Arquivo para definir classe e atribuitos do model de resumo semanal.
        * `app/models/user.py`: Arquivo para definir classe e atribuitos do model de users. Gerenciamento com JWT.
    * `app/services/`: Módulo para implementação de lógicas de serviços ('regras de negócio').
        * `app/services/classifier.py`: Implementação de métodos para classificação de comentário (texto) por meio de modelo de LLM.
        * `app/services/insights.py`:  Implementação de método para responder pergunta feita em linguagem natural, pelo usuário via requisição, por meio de modelo de LLM, com contexto dos últimos resumos semanais enviados.
        * `app/services/summary.py`: Implementação de método para gerar resumo semanal com base em comentários classficados através de modelo de LLM.
    * `app/templates/`: Módulo para implementação de telas simples em HTML para exibição de comentários classificados.
        * `app/templates/dashboard.html`: Tela para exibição e filtrar comentários filtrados.
        * `app/templates/login.html`: Tela de login para parte privada (exibição de comentários classificados).
    * `app/views/`: Módulo para roteamento de views (tela de login e dashboard).
        * `app/views/dashboard.py`: Arquivo para instânciamento de blueprint que faz o roteamento dos caminhos para HTMLs.
* `data/`: Pasta para salvar datasets (CSV) usados para gerar métricas do modelo de classificação de comentários.
* `migrations/`: Pasta para armazenar migrations gerados automaticamente pelo Flask-migrate, que aplicam os models no banco de dados configurado.

### Pytest

Nesta pasta, estão todos os testes automaticos do Flask. Nele serão definidos testes para garantir o bom funcionamente da API e cálculo de métricas de EVALs mínimas. Além disso uma pasta dedicada para testes unitários.

> De maneira geral, utilizei Mock para todos os momentos que a API da `openai` é chamada. A única excessão são os testes de EVALs do prompt de classificação de comnetários, que devem atender um valor mínimo de recall, precision e f1-score do modelo.

## Como executar o Projeto

## Testes e Métricas (EVALs)

## CI/CD

## Painel e Relátorios

## Resumo por E-mail

## Extra: Insights
