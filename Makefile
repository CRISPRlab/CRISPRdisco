.PHONY: init rebuild tag release deploy git_init check_docker_login setup test deploy

SHELL:=bash
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=12 --verify HEAD)

init:
	docker pull continuumio/miniconda
	docker build --rm -f Dockerfile -t crisprlab/crisprdisco .
	docker build --rm -f Dockerfile.jupyter -t crisprlab/crisprdisco_jupyter .
	docker build --rm -f Dockerfile.notebook -t crisprlab/crisprdisco_notebook .
	docker build --rm -f Dockerfile.kernel_gateway -t crisprlab/crisprdisco_kernel_gateway .

rebuild:
	docker build --rm --no-cache -f Dockerfile -t crisprlab/crisprdisco .
	docker build --rm --no-cache -f Dockerfile.jupyter -t crisprlab/crisprdisco_jupyter .
	docker build --rm --no-cache -f Dockerfile.notebook -t crisprlab/crisprdisco_notebook .
	docker build --rm --no-cache -f Dockerfile.kernel_gateway -t crisprlab/crisprdisco_kernel_gateway .

tag:
	docker tag crisprlab/crisprdisco:latest crisprlab/crisprdisco:$(GIT_MASTER_HEAD_SHA)
	docker tag crisprlab/crisprdisco_jupyter:latest crisprlab/crisprdisco_jupyter:$(GIT_MASTER_HEAD_SHA)
	docker tag crisprlab/crisprdisco_notebook:latest crisprlab/crisprdisco_notebook:$(GIT_MASTER_HEAD_SHA)
	docker tag crisprlab/crisprdisco_kernel_gateway:latest crisprlab/crisprdisco_kernel_gateway:$(GIT_MASTER_HEAD_SHA)

release:
	docker push crisprlab/crisprdisco
	docker push crisprlab/crisprdisco_jupyter
	docker push crisprlab/crisprdisco_notebook
	docker push crisprlab/crisprdisco_kernel_gateway

deploy: 
	./deploy.sh

TEST=$(shell docker info | grep "Username")
check_docker_login:
	@if [ "$(TEST)" ]; then echo "Logged in to dockerhub."; else echo "Please log in to dockerhub."; exit 1; fi

git_init:
	@curl --user ${GITHUB_TOKEN}:x-oauth-basic --request POST \
		--data '{"name":"crisprdisco","private":true,"gitignore_template":"Python"}' \
		https://api.github.com/orgs/crisprlab/repos && \
	git init && \
	git remote add origin git@github.com:crisprlab/crisprdisco.git && \
	git remote -v && \
	git pull origin master && \
	git add . && \
	git commit -m "start project" && \
	git push -u origin master

test:
	./test.sh

setup: check_docker_login init git_init

deploy: check_docker_login rebuild tag release
