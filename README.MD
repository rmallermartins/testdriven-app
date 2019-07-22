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


## Local

Atualizar os containers (novas dependencias, alteração nas imagens, etc...)

```shell
$ sc up -d --build
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
