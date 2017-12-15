.PHONY: init rebuild tag release deploy git_init check_docker_login setup test deploy

SHELL:=bash
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=12 --verify HEAD)

init:
	docker pull agbiome/base-datascience
	docker pull agbiome/base
	docker build --rm -f Dockerfile -t agbiome/crawler .
	docker build --rm -f Dockerfile.jupyter -t agbiome/crawler_jupyter .
	docker build --rm -f Dockerfile.notebook -t agbiome/crawler_notebook .
	docker build --rm -f Dockerfile.kernel_gateway -t agbiome/crawler_kernel_gateway .

rebuild:
	docker build --rm --no-cache -f Dockerfile -t agbiome/crawler .
	docker build --rm --no-cache -f Dockerfile.jupyter -t agbiome/crawler_jupyter .
	docker build --rm --no-cache -f Dockerfile.notebook -t agbiome/crawler_notebook .
	docker build --rm --no-cache -f Dockerfile.kernel_gateway -t agbiome/crawler_kernel_gateway .

tag:
	docker tag agbiome/crawler:latest agbiome/crawler:$(GIT_MASTER_HEAD_SHA)
	docker tag agbiome/crawler_jupyter:latest agbiome/crawler_jupyter:$(GIT_MASTER_HEAD_SHA)
	docker tag agbiome/crawler_notebook:latest agbiome/crawler_notebook:$(GIT_MASTER_HEAD_SHA)
	docker tag agbiome/crawler_kernel_gateway:latest agbiome/crawler_kernel_gateway:$(GIT_MASTER_HEAD_SHA)

release:
	docker push agbiome/crawler
	docker push agbiome/crawler_jupyter
	docker push agbiome/crawler_notebook
	docker push agbiome/crawler_kernel_gateway

deploy: 
	./deploy.sh

TEST=$(shell docker info | grep "Username")
check_docker_login:
	@if [ "$(TEST)" ]; then echo "Logged in to dockerhub."; else echo "Please log in to dockerhub."; exit 1; fi

git_init:
	@curl --user ${GITHUB_TOKEN}:x-oauth-basic --request POST \
		--data '{"name":"crawler","private":true,"gitignore_template":"Python"}' \
		https://api.github.com/orgs/agbiome/repos && \
	git init && \
	git remote add origin git@github.com:AgBiome/crawler.git && \
	git remote -v && \
	git pull origin master && \
	git add . && \
	git commit -m "start project" && \
	git push -u origin master

test:
	./test.sh

setup: check_docker_login init git_init

deploy: check_docker_login rebuild tag release
