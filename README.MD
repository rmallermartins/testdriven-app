# Testdriven-app

[![Build Status](https://travis-ci.org/rmallermartins/testdriven-app.svg?branch=master)](https://travis-ci.org/rmallermartins/testdriven-app)


## Facilidades

Criar Alias para `docker-compose` e `docker-machine` - `dc` e `dm` editando o *.bashrc* :

```bash
alias dc='docker-compose'
alias dm='docker-machine'
```

Remover imagens Docker:

```shell
$ docker rmi $(docker images -q)
```

Acessar psql no Docker:

```shell
$ dc exec users-db psql -U postgres
```

Abrir relatório de cobertura de código em HTML:

```shell
$ open services/users/htmlcov/index.html
```

Rodar Flake8 (checagem de estilo de código e erros de programação):

```shell
$ dc exec users flake8 project
```


## Dev

Variáveis de ambiente:

```shell
$ export REACT_APP_USERS_SERVICE_URL=http://localhost
```

Atualizar os containers (novas dependencias, alteração nas imagens, etc...)

```shell
$ dc up -d --build
```

## Hom

Variáveis de ambiente:

```shell
$ export REACT_APP_USERS_SERVICE_URL=http://DOCKER_MACHINE_STAGING_IP
```

## Prod

Variáveis de ambiente:

```shell
$ export REACT_APP_USERS_SERVICE_URL=http://DOCKER_MACHINE_PROD_IP
$ export SECRET_KEY=SOMETHING_SUPER_SECRET
```


## Deploy

Criar maquina EC2 (São Paulo) pelo Docker:

```shell
$ dm create --driver amazonec2 --amazonec2-region sa-east-1 testdriven-prod
```

Apontar o client do Docker para EC2:

```shell
$ dm env testdriven-prod
$ eval $(dm env testdriven-prod)
```

Listar maquinas:

```shell
$ dm ls
```

Rodar container, criar banco, adicionar seed de dados e rodar testes:

```shell
$ dc -f docker-compose-prod.yml up -d --build

$ dc -f docker-compose-prod.yml exec users python manage.py recreate_db

$ dc -f docker-compose-prod.yml exec users python manage.py seed_db

$ dc -f docker-compose-prod.yml exec users python manage.py test
```

Ver IP do EC2:

```shell
$ dm ip testdriven-prod
```

Checar variáveis de ambiente:

```shell
$ dc -f docker-compose-prod.yml exec users env
```

Apontar o Docker para o localhost novamente:

```shell
$ eval $(dm env -u)
```


## Testes

Rodar testes backend:

```shell
$ docker-compose exec users python manage.py test
```

Cliente:

```shell
$ docker-compose exec client npm run coverage
```

e2e:

```shell
$ ./node_modules/.bin/cypress open --config baseUrl=http://localhost
```

Usando script:

```shell
$ sh test.sh server
$ sh test.sh client
$ sh test.sh e2e
$ sh test.sh all
```


## Swagger

Atualizar swagger.json:

```shell
$ python services/swagger/update-spec.py http://localhost
```
