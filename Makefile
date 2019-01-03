## ----- Variables -----
ENV = 1 # 0 for production, 1 for development
DB_VOL_NAME = postgres.data
STACK_NAME = $(shell basename $$PWD)
APP_NAME =  cicsa_ranking

## Use git-secret.
SECRETS = true


## ----- Commands (targets) -----
.PHONY: default setup

## Default target when no arguments are given to make (run the program).
default: run

## Sets up this project on a new device.
setup: setup-hooks install
	@if [ "$(SECRETS)" == true ]; then $(REVEAL_SECRETS_CMD); fi


## [Git setup / configuration commands]
.PHONY: setup-hooks hide-secrets reveal-secrets

## Configure Git to use .githooks (for shared githooks).
setup-hooks:
	@echo "Configuring githooks..."
	@git config core.hooksPath .githooks && echo "done"

## Initialize git-secret
init-secrets:
	@git secret init

## Hide modified secret files using git-secret.
hide-secrets:
	@echo "Hiding modified secret files..."
	@git secret hide -m

## Reveal files hidden by git-secret.
REVEAL_SECRETS_CMD = git secret reveal
reveal-secrets:
	@echo "Revealing secret files..."
	@$(REVEAL_SECRETS_CMD)


## [Python commands]
.PHONY: install dev-run prod-run

install:
	@echo "Installing dependencies using 'pipenv'..."
	@pipenv install --dev

dev-run:
	@echo "Starting Django server (Development LOCAL) ..."
	@python3 manage.py runserver

dev-run-server:
	@echo "Starting Django server (Development SERVER) ..."
	@python3 manage.py runserver --insecure 0.0.0.0:$$PORT

prod-run:
	@echo "Starting Django server (Production) ..."
	@./scripts/prod_execute.sh ${APP_NAME}

