.PHONY: init init_nb rebuild rebuild_nb tag tag_nb release check_docker_login test setup setup_nb setup_all deploy

SHELL:=bash
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=12 --verify HEAD)

init:
	time docker build --rm -f Dockerfile -t crisprlab/crisprdisco .

init_nb:
	time docker build --rm -f Dockerfile.jupyter -t crisprlab/crisprdisco_notebook .

rebuild:
	time docker build --rm --no-cache -f Dockerfile -t crisprlab/crisprdisco .

rebuild_nb:
	time docker build --rm --no-cache -f Dockerfile.jupyter -t crisprlab/crisprdisco_notebook .

tag:
	docker tag crisprlab/crisprdisco:latest crisprlab/crisprdisco:$(GIT_MASTER_HEAD_SHA)

tag_nb:
	docker tag crisprlab/crisprdisco_notebook:latest crisprlab/crisprdisco_notebook:$(GIT_MASTER_HEAD_SHA)

release:
	docker push crisprlab/crisprdisco:latest 
	docker push crisprlab/crisprdisco:$(GIT_MASTER_HEAD_SHA)
	docker push crisprlab/crisprdisco_notebook:latest
	docker push crisprlab/crisprdisco_notebook:$(GIT_MASTER_HEAD_SHA)

TEST=$(shell docker info | grep "Username")
check_docker_login:
	@if [ "$(TEST)" ]; then echo "Logged in to dockerhub."; else echo "Please log in to dockerhub with 'docker login'."; exit 1; fi

test:
	./test.sh

setup: check_docker_login init

setup_nb: check_docker_login init_nb

setup_all:  check_docker_login init init_nb

deploy: check_docker_login rebuild rebuild_nb tag tag_nb release
