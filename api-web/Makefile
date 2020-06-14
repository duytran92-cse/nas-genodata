REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t genopedia/genodata/api-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t genopedia/genodata/api-web/test .
	sudo docker tag genopedia/genodata/api-web/test $(REGISTRY)/genopedia/genodata/api-web/test
	sudo docker push $(REGISTRY)/genopedia/genodata/api-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t genopedia/genodata/api-web/test .
	sudo docker tag genopedia/genodata/api-web/prod $(REGISTRY)/genopedia/genodata/api-web/prod
	sudo docker push $(REGISTRY)/genopedia/genodata/api-web/prod
