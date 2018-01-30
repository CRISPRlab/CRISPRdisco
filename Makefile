.PHONY: init rebuild tag release deploy git_init check_docker_login setup test deploy

SHELL:=bash
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=12 --verify HEAD)

init:
	docker build --rm -f Dockerfile -t crisprlab/crisprdisco .
	docker build --rm -f Dockerfile.jupyter -t crisprlab/crisprdisco_notebook .

rebuild:
	docker build --rm --no-cache -f Dockerfile -t crisprlab/crisprdisco .
	docker build --rm --no-cache -f Dockerfile.jupyter -t crisprlab/crisprdisco_notebook .

tag:
	docker tag crisprlab/crisprdisco:latest crisprlab/crisprdisco:$(GIT_MASTER_HEAD_SHA)
	docker tag crisprlab/crisprdisco_notebook:latest crisprlab/crisprdisco_notebook:$(GIT_MASTER_HEAD_SHA)

release:
	docker push crisprlab/crisprdisco:latest 
	docker push crisprlab/crisprdisco:$(GIT_MASTER_HEAD_SHA)
	docker push crisprlab/crisprdisco_notebook:latest
	docker push crisprlab/crisprdisco_notebook:$(GIT_MASTER_HEAD_SHA)

TEST=$(shell docker info | grep "Username")
check_docker_login:
	@if [ "$(TEST)" ]; then echo "Logged in to dockerhub."; else echo "Please log in to dockerhub."; exit 1; fi

test:
	./test.sh

setup: check_docker_login init

deploy: check_docker_login rebuild tag release
