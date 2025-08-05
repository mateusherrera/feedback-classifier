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
- [Endpoints](#endpoints)
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

Nessa seção será listado o passo-a-passo para executar o projeto utilizando Docker.

### Requisitos:

* Python 3.10+
* Git
* Linux ou WSL2 (Para instalar WSL2 no Windows, caso seja o caso você [pode seguir esse tutorial](https://medium.com/@habbema/desvendando-o-wsl-2-no-windows-11-c7649545026d))
* Docker Desktop no Windows integrado com WSL2, caso necessário[utilize o tutorial oficial](https://docs.docker.com/desktop/features/wsl/)

### Clone o repositório

Clone o repositório e entre na pasta:

```sh
git clone https://github.com/mateusherrera/feedback-classifier.git
cd feedback-classifier
```

### Variáveis de ambiente

O primeiro passo é definir as variáveis de ambiente.
Na pasta raiz do repostório há o template, para preencher com seus valores faça:

```sh
cp .env.template .env
```

Em seguida preenchar os valores adequados. Para isso, pode fazer pelo deu editor preferido, ou pelo terminal com `nano .env`.

Abaixo seguem as descrições da cada variáveis que deve ser fornecida para o projeto:

> Os itens marcados com '**' precisam ser preenchidos. Ou seja, não podem ser usados com valor default

* Variáveis para o Flask:
    * ``FLASK_APP``: Caminho para o módulo para app flask, caso não tenha alteração na estrutura do projeto, pode ser deixada como valor default: `app.main:app`.
    * ``FLASK_ENV``: Indica se o flask será rodado em `production`, `development` ou `testing`. Em execução local pode ser deixado como `development`.
    * ** ``SECRET_KEY``: Chave aleatória gerada para utilização do Flask App, para gera pode seguir [esses passos](#para-gerar-as-chaves-aleatórias)
* ** ``OPENAI_API_KEY``: Chave válida para utilização da API da OpenAI. Pode ser gera na [plataforma oficial da OpenAi](https://platform.openai.com)
* ** ``JWT_SECRET_KEY``: Chave aleatória para utilização nos métodos do JWT. Pode ser gerada seguindo o mesmo método da SECRET_KEY do Flask, [aqui](#para-gerar-as-chaves-aleatórias).
* Variáveis de Banco de Dados:
    * ``SQLALCHEMY_DATABASE_URI``: Conn string para conexão com o banco a ser utilizado pelo Flask. Exemplo: `postgresql://usuario:senha@host:5432/nome_do_banco`. PS.: para utilizar o banco gerado pelo Docker, host será o mesmo nome do container, no caso `db`.
        > Importante: A connstring será usada para conexão. As variáveis abaixo são apenas para criação do banco com o docker compose.
        > Então caso queira conectar a um banco proprio, pode preencher apenas a connstring com as suas configurações, e as debaixo podem ser ignoradas. Para esse último caso, não suba o serviço db, quando fazer o build dos containers.
    * ``POSTGRES_DB``: Nome do Banco de Dados que será gerado pelo docker ao fazer o build do PostgreSQL.
    * ``POSTGRES_HOST``: Host do Banco de Dados que será gerado pelo docker ao fazer o build do PostgreSQL. De acordo com a estrutura do `docker-compose.yml` o valor deve ser o nome do service, no caso `db`.
    * ``POSTGRES_PORT``: Número da porta para conexão com o Banco de Dados.
    * ``POSTGRES_USER``: Usuário admin que será gerado no build do container.
    * ``POSTGRES_PASSWORD``: Senha para o usuário admin.
    * ``PGDATA_PATH``: Caminho local para armazenamento dos dados do banco de dados. Pode ser o default: `/var/lib/postgresql/data`. Tenha em mente que ela precisa existir e a permissão deve ser concedida para o docker: `sudo mkdir /var/lib/postgresql/data` e `sudo chown -R 999:999 /var/lib/postgresql/data/`.
* Variáveis para configuração do Redis (Cache):
    * ``CACHE_TYPE``: Tipo de cache a ser utilizado para o cache. Pode ser deixado o valor default: `RedisCache`, para utilização do Redis.
    * ``CACHE_REDIS_HOST``: Host para o redis, segue a lógica do postgres, usando o Docker, deixe o nome do service: `redis`.
    * ``CACHE_REDIS_PORT``: Número da porta para conexão com o redis.
    * ``CACHE_REDIS_DB``: Indice do Banco de Dados, pode ser deixado em default: `0`.
    * ``CACHE_DEFAULT_TIMEOUT``: Timeout padrão para o redis, pode ser deixado também com valor default: `60`.
* Variávies para configuração de envio de e-mail automáticos:
    > Se usar Gmail, MAIL_SERVER e MAIL_PORT podem ser deixados default.
    * ** ``MAIL_SERVER``: Servidor de STMP do e-mail que será utilizado para envio automático de resumo semanal.
    * ** ``MAIL_PORT``: Porta para o servidor STMP do e-mail que será utilizado para envio automático de resumo semanal.
    * ** ``MAIL_USERNAME``: Usuário de e-mail que será utilizado para envio automático de resumo semanal.
    * ** ``MAIL_PASSWORD``: Senha de app do e-mail que será utilizado para envio automático de resumo semanal. No caso do GMail, pode ser [esse documento](https://support.google.com/accounts/answer/185833?hl=pt-BR) para gerar a senha de app.
    * ** ``MAIL_DEFAULT_SENDER``: E-mail remetente da mensagem, pode ser o mesmo que o USERNAME.
    * ** ``STAKEHOLDERS_EMAILS``: E-mail que receberão o resumo semanal separados por `,` (vírgula), por exemplo: `example1@mail.com,example1@mail.com`
    * ``CELERY_BROKER_URL``: Connstring para redis, por exemplo `redis://host_redis:porta_redis/numero_db_redis`. Lembrando que assim como no postges, o host é o nome do serviço no Docker, no caso `redis`.
.* Nomes dos container, esse valores são os nomes dos containers de cada serviço, pode ser deixado o valor default:
    * ``REDIS_CONTAINER_NAME``: Nome do container de Redis (`feedback-classifier_redis`).
    * ``DB_CONTAINER_NAME``: Nome do container do PostgreSQl (`feedback-classifier_db`).
    * ``API_CONTAINER_NAME``: Nome do container do Flask (`feedback-classifier_api`).
    * ``NGINX_CONTAINER_NAME``: Nome do container do NGINX (`feedback-classifier_nginx`).

#### Para gerar as chaves aleatórias

Para gerar as chaves aleatórias use o interpretador do python com `python3` e rode:

```python
import secrets
print(secrets.token_urlsafe(32))
```

> Importante: Usar chaves destintas para SECRET_KEY e JWT_SECRET_KEY

### Docker Compose

Com o `.env` devidamente criado e preenchido basta fazer o build do Docker, rodando:

```sh
docker compose up -d
```

Para verificar se tudo ocorreu bem rode:

```sh
docker ps
```

E a saida deve ser algo como:

```sh
CONTAINER ID   IMAGE                               COMMAND                  CREATED        STATUS             PORTS                                         NAMES
252a2ca89c1e   feedback-classifier-nginx           "/docker-entrypoint.…"   46 hours ago   Up About an hour   0.0.0.0:443->443/tcp, [::]:443->443/tcp       feedback-classifier_nginx
0c254b54dcf5   feedback-classifier-celery_worker   "celery -A app.tasks…"   46 hours ago   Up About an hour                                                 celery_worker
a4cef3afbb0e   feedback-classifier-celery_beat     "celery -A app.tasks…"   46 hours ago   Up About an hour                                                 celery_beat
f99f6fbe771e   feedback-classifier-api             "gunicorn -w 4 -b 0.…"   46 hours ago   Up About an hour   0/tcp                                         feedback-classifier_api
a1ba3bd2e5ad   postgres:16                         "docker-entrypoint.s…"   2 days ago     Up About an hour   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   feedback-classifier_db
9d76af791392   redis:7                             "docker-entrypoint.s…"   2 days ago     Up About an hour   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   feedback-classifier_redis
```

### Jenkins

Caso queira, é possível é subir um Jenkins com o `docker-compose.yml` disponível em `jenkins/docker-compose.yml`. Basta rodar:

```sh
cd jenkins
docker compose up -d
```

Se você optou por subir o jenkins do repositório, faça o seu primeiro acesso com a senha disponível com o comando abaixo, e crie o seu usuário de administrador.

```sh
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Feito isso, ou usando um Jekins proprio. Logado, faça as seguinte configurações para rodar os testes automáticos com Github Actions:

1. Adicione seu Github Personal Access Token:

    > Para esse caso, crie o token com repo e admin:repo_hook.

    1. Acesse Manage Jenkins → Manage Credentials → selecione o store global.
    2. Clique em Add Credentials e preencha:
        * Kind: Secret text
        * Secret: cole o seu GitHub Personal Access Token
        * ID: github-token
        * Description: “Token para acionar GitHub Actions”
    3. Salve.

2. Adicione suas credencias do Github:
    1. Vá em Manage Jenkins → Manage Credentials → selecione o escopo (global).
    2. Clique em Add Credentials e preencha:
        * Kind: Username with password
        * Username: seu usuário GitHub (ex.: mateusherrera)
        * Password: seu GitHub Personal Access Token (o mesmo criado no passo 1)
        * ID: github-credentials
        * Description: “Credenciais GitHub (usuário + token)”
    3. Salve.

3. Crie o pipeline para o repositório
    1. No dashboard do Jenkins, clique em “New Item” (ou “Novo Item”) no menu lateral.
    2. Dê um nome ao job, por exemplo feedback-classifier-ci, selecione “Pipeline” e clique em OK.
    3. Na tela de configuração do job:
        1. Em Pipeline faça:
            * Definition: selecione “Pipeline script from SCM”.
            * SCM: escolha “Git”.
            * Repository URL: https://github.com/mateusherrera/feedback-classifier.git ou repo de fork caso tenha feito.
            * Credentials: selecione github-credentials.
            * Branches to build: */main.
            * Script Path: Jenkinsfile.
    4. Clique em Save.

## Testes e Métricas (EVALs)

Para realizar testes locais rode o comando:

```sh
PYTHONPATH=flask OPENAI_API_KEY=<token-openai> LLM_MODEL=gpt-3.5-turbo pytest -v
```

Para realizar testes de EVALs rode o comando abaixo, para cálcular métricas de recall, precision e f1 de todas as categorias classificadas:

```sh
PYTHONPATH=flask dotenv run -- python -m app.evals --all
```

### Flags Disponíveis

| Flag                            | Descrição                                                                 |
|---------------------------------|---------------------------------------------------------------------------|
| `-d, --data-csv PATH`           | Caminho para o CSV (default: `flask/data/test_comments.csv`)              |
| `--all`                         | Avalia todas as categorias                                               |
| `--<slug>`                      | Avalia somente a categoria cujo slug é `<slug>` (ex.: `--elogio`)         |
| `--<slug>-min-recall FLOAT`     | Recall mínimo aceito em `<slug>`                                          |
| `--<slug>-max-recall FLOAT`     | Recall máximo aceito em `<slug>`                                          |
| `--<slug>-min-precision FLOAT`  | Precisão mínima aceita em `<slug>`                                        |
| `--<slug>-max-precision FLOAT`  | Precisão máxima aceita em `<slug>`                                        |
| `--<slug>-min-f1 FLOAT`         | F1 mínima aceita em `<slug>`                                              |
| `--<slug>-max-f1 FLOAT`         | F1 máxima aceita em `<slug>`                                              |


### Testes automatizados de EVALs

Sobre as métricas mínimas definidas no Github Actions, o CI não passara caso os valores sejam:

TODO: Adicionar tabela de valores

## Endpoints

Em `docs/postman-collection/` há o arquivo `Flask - LLM API.postman_collection.json` que pode ser importado no, idalmente, no Postman ou no Insomnia, para carregar os endpoits no seu cliet de preferência.


### Lista de Endpoints:

> host: https://localhost/

> Para testar os endpoints passe o access token em Authorization com Berear.

> Exemplos de request e response, podem ser visto no collection do Postman.

* Auth:
    * POST `api/auth/register`: Endpoint para criar usuários.
    * POST `api/auth/login`: Endpoint para fazer login, 
    * POST `api/auth/refresh`: Endpoint para regerar um access token (vale por um minuto, em dev um dia), com refresh token (vale por um dia) válido.
* Classificação de comentários:
    * POST `api/comentarios`: Endpoint para classificar comentário com modelo LLM.
    * GET `api/comentarios`: Listar todos os comentários classificados.
    * GET `api/comentarios/export`: Exportar dados de comentários classificados em CSV.
* Relatório Semanal:
    * GET `api/relatorio/semana`: Retorna os dados (em JSON) cálculados para os dashboards.
* Insights:
    * POST `api/insights/perguntar`: Responde pergunta em linguagem natural com base nos últimos 8 relatórios semanais.

## Painel e Relátorios

## Resumo por E-mail

## Extra: Insights
