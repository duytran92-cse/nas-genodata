REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t genopedia/genodata/admin-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t genopedia/genodata/admin-web/test .
	sudo docker tag genopedia/genodata/admin-web/test $(REGISTRY)/genopedia/genodata/admin-web/test
	sudo docker push $(REGISTRY)/genopedia/genodata/admin-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t genopedia/genodata/admin-web/prod .
	sudo docker tag genopedia/genodata/admin-web/prod $(REGISTRY)/genopedia/genodata/admin-web/prod
	sudo docker push $(REGISTRY)/genopedia/genodata/admin-web/prod
