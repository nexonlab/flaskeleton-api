## Flaskeleton API
> Uma aplicação minimalista e completamente funcional contemplando todas as características de uma API
> completa utilizando *Flask*, *SQLAlchemy*, *Flask-Migrate*, *Marshmallow* e *APIBlueprint*.

#### Setup inicial
Recomendamos utilizar um ambiente virtual `python` para execução
do projeto. Problemas com o *SQLAlchemy* e conflitos entre
pacotes ocorrem facilmente quando utilizado num único ambiente
com outros projeto `python`.

Portanto, indicamos a utilização do [*VirtualEnvWrapper*](https://virtualenvwrapper.readthedocs.io/en/latest/)
para isolar a instalação dos pacotes em `requirements.txt`.

Caso não esteja interessado em utilizar um ambiente virtual python,
também tem a opção de rodar num *container docker*. Recomendamos
a instalação do [*docker-compose*](https://docs.docker.com/compose/), o qual já está integrado
com este projeto.

Com o *docker-compose* já instalado, execute
```shell script
docker-compose up -d
``` 
para subir o *container* e iniciar a aplicação e
```shell script
docker-compose down
```  
para matar o *container* e encerrar a aplicação.

Para auxiliar no processo de deploy, debug e testes, o arquivo `Makefile`
contém alguns comandos úteis que podem ser acessados através de 
```shell script
make help
```

#### Estrutura do projeto
A aplicação consiste em um pacote principal `app` que contém toda a aplicação.
Dentro do pacote principal são encontrados pacotes das camadas de controle,
modelo, visualização (*endpoints*) e acesso aos dados.

    |-- app
    |   | -- controllers
    |   | -- dao
    |   | -- errors
    |   | -- models
    |   | -- resources
    |   | ...

Além dos pacotes principais, pacotes como `docs` e `templates` são
auxiliares e utilizados pela *API Blueprint*, além do pacote `migrations`
utilizado pela extensão *Flask-Migrate*.

#### Flask-Migrate
A aplicação é completamente funcional e autocontida, ou seja, funciona
sem dependências externas. Para auxiliar nesse processo foi utilizado
juntamente com o ORM *SQLAlchemy* a extensão [*Flask-Migrate*](https://flask-migrate.readthedocs.io/en/latest/). É
ela a responsável por construir a base de dados, migrar alterações
e manter a consistência dos dados. Para tanto, é necessário efetuar,
antes de iniciar a aplicação, a construção da base de dados.

A base de dados, nessa aplicação, é mantida utilizando o [*SQLite3*](https://www.sqlite.org/index.html). Portanto,
antes de executar a aplicação, certifique-se de que está rodando corretamente
em sua máquina. O *SQLite3* é uma excelente escolha para uma aplicação pequena,
como essa, que serve de exemplo para uso do ORM e principais funcionalidades
do framework *Flask*.

Ao executar pela primeira vez, rode o comando 
```shell script
flask db migrate
```
para garantir a criação de tabelas e gerar um `script` de revisão
que levará quaisquer mudanças nos seus `models` para suas tabelas.

Em seguida, execute
```shell script
flask db upgrade
```
para de fato atualizar as tabelas da base de dados.

Ao concluir com sucesso pela primeira vez os comandos acima,
note a criação de um arquivo chamado `flaskeleton.db`. Esse
é o banco de dados *SQLite3* da aplicação.
