ifeq ($(container),)
	# Se a variavel container não foi setada
	# use 'app' como padrão
	container=app
endif
$(info Make: VAR container="$(container)".)

# Por padrão make sem nada vai rodar 'help'
.DEFAULT_GOAL := help

# PHONY especifica que 'help' é um comando, não uma target que precisa ser
# compilada.
.PHONY: help

# Roubado de: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# grep -E faz o matchig: [COMANDO]:[espaço]<COMENTÁRIO>[espaço].
#      Nota: Em makefiles $ tem que ser trocado por $$
#
# sort: ordena os resultados alfabeticamente.
#
# awk: formata o retorno do sort em "[COMANDO]<30 espaços>[COMENTÁRIO]
#      usando ":.?##" como field separator (FS).
help:
	@echo "$$(tput bold)Comandos:$$(tput sgr0)";echo;
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s%s\n", $$1, $$2}'

up: ## Sobe os containers no modo detached (-d)
	docker-compose up -d

up-debug: ## Sobe os containers em modo de debug (sem -d)
	docker-compose up

clean: ## Remove volumes associados ao container
	docker-compose rm -vsf
	docker-compose down -v --remove-orphans

build: ## Rebuilda os containers
	$(MAKE) clean
	docker-compose build
	$(MAKE) up

create-db:
	docker-compose run app flask db migrate && flask db upgrade

down: ## Para e remove os containers
	docker-compose down

test: ## Sobe o container e executa os testes
	docker-compose run $(container) pytest -rpf

test-file: ## Sobe o container da aplicação e executa um arquivo de teste
	docker-compose run $(container) pytest -rpf ./tests/$(FILE)

tail-logs: ## Sobe o container da aplicação e acompanha os logs
	docker-compose logs -f $(container)

coverage:
	coverage run -m pytest && coverage report

coverage-html:
	coverage html

prettier: ## Formata o codigo para torna-lo mais bonito
	black -l 79 ./app

lint: ## Verifica qualidade da escrita de codigo
	flake8 ./app
