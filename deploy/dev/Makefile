GENODATA_API_VOLDEMORT_HOST_PORT=6666
GENODATA_API_MYSQL_HOST_PORT=3313
GENODATA_API_WEB_HOST_PORT=8013
GENODATA_ADMIN_MYSQL_HOST_PORT=3314
GENODATA_ADMIN_WEB_HOST_PORT=8014
GENODATA_API_RABBITMQ_HOST_PORT=5700
GENODATA_API_RABBITMQ_ADMIN_HOST_PORT=15600
GENOPEDIA_GENODATA_HOME=$(GENOPEDIA_HOME)/genopedia-genodata

create-storage:
	sudo docker run -d --name=genopedia-dev.genodata-api.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true
	sudo docker run -d --name=genopedia-dev.genodata-admin.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true

clear-storage:
	-sudo docker stop genopedia-dev.genodata-api.mysql.storage
	-sudo docker rm genopedia-dev.genodata-api.mysql.storage
	-sudo docker stop genopedia-dev.genodata-admin.mysql.storage
	-sudo docker rm genopedia-dev.genodata-admin.mysql.storage

deploy:
	sudo docker run -d --name=genopedia-dev.genodata-api.rabbitmq \
		-p $(GENODATA_API_RABBITMQ_HOST_PORT):5672 \
		-p $(GENODATA_API_RABBITMQ_ADMIN_HOST_PORT):15672 \
		registry.novogenialab.com/notasquare-zero/images/standard-rabbitmq:0.1
	sudo docker run -d --name=genopedia-dev.genodata-api.voldemort \
		-p $(GENODATA_API_VOLDEMORT_HOST_PORT):6666 \
		registry.novogenialab.com/notasquare-zero/images/standard-voldemort:0.1
	sudo docker run -d --name=genopedia-dev.genodata-api.mysql \
		--volumes-from=genopedia-dev.genodata-api.mysql.storage \
		-p $(GENODATA_API_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=genopedia-dev.genodata-api.web \
		--link genopedia-dev.genodata-api.mysql:mysql \
		--link genopedia-dev.genodata-api.voldemort:voldemort \
		--link genopedia-dev.genodata-api.rabbitmq:rabbitmq \
		-v $(GENOPEDIA_GENODATA_HOME)/api-web/src/www:/opt/www \
		-p $(GENODATA_API_WEB_HOST_PORT):80 \
		genopedia/genodata/api-web/dev

	sudo docker run -d --name=genopedia-dev.genodata-admin.mysql \
		-p $(GENODATA_ADMIN_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=genopedia-dev.genodata-admin.web \
		--link genopedia-dev.genodata-admin.mysql:mysql \
		--link genopedia-dev.genodata-api.web:genodata-api \
		-v $(GENOPEDIA_GENODATA_HOME)/admin-web/src/www:/opt/www \
		-p $(GENODATA_ADMIN_WEB_HOST_PORT):80 \
		genopedia/genodata/admin-web/dev

	sudo cp nginx/genopedia-genodata-api-rabbitmq /etc/nginx/sites-enabled
	sudo cp nginx/genopedia-genodata-api-web /etc/nginx/sites-enabled
	sudo cp nginx/genopedia-genodata-admin-web /etc/nginx/sites-enabled
	sudo service nginx reload

	sleep 10

	-sudo docker exec -it genopedia-dev.genodata-api.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS api_db;"
	-sudo docker exec -it genopedia-dev.genodata-api.web python /opt/www/manage.py migrate

	-sudo docker exec -it genopedia-dev.genodata-admin.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS admin_db;"
	-sudo docker exec -it genopedia-dev.genodata-admin.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.genodata-admin.web python /opt/www/manage.py linkstatic

clean:
	-sudo docker stop genopedia-dev.genodata-admin.mysql
	-sudo docker stop genopedia-dev.genodata-admin.web
	-sudo docker stop genopedia-dev.genodata-api.rabbitmq
	-sudo docker stop genopedia-dev.genodata-api.voldemort
	-sudo docker stop genopedia-dev.genodata-api.mysql
	-sudo docker stop genopedia-dev.genodata-api.web

	-sudo docker rm genopedia-dev.genodata-admin.mysql
	-sudo docker rm genopedia-dev.genodata-admin.web
	-sudo docker rm genopedia-dev.genodata-api.rabbitmq
	-sudo docker rm genopedia-dev.genodata-api.voldemort
	-sudo docker rm genopedia-dev.genodata-api.mysql
	-sudo docker rm genopedia-dev.genodata-api.web

	-sudo rm /etc/nginx/sites-enabled/genopedia-genodata-api-web
	-sudo rm /etc/nginx/sites-enabled/genopedia-genodata-api-rabbitmq
	-sudo rm /etc/nginx/sites-enabled/genopedia-genodata-admin-web


start:
	sudo docker start genopedia-dev.genodata-api.rabbitmq
	sudo docker start genopedia-dev.genodata-api.voldemort
	sudo docker start genopedia-dev.genodata-api.mysql
	sudo docker start genopedia-dev.genodata-api.web
	sudo docker start genopedia-dev.genodata-admin.mysql
	sudo docker start genopedia-dev.genodata-admin.web

stop:
	sudo docker stop genopedia-dev.genodata-api.rabbitmq
	sudo docker stop genopedia-dev.genodata-api.voldemort
	sudo docker stop genopedia-dev.genodata-api.mysql
	sudo docker stop genopedia-dev.genodata-api.web
	sudo docker stop genopedia-dev.genodata-admin.mysql
	sudo docker stop genopedia-dev.genodata-admin.web

migrate:
	-sudo docker exec -it genopedia-dev.genodata-api.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.genodata-admin.web python /opt/www/manage.py migrate

ssh-api-rabbitmq:
	sudo docker exec -it genopedia-dev.genodata-api.rabbitmq bash

ssh-api-voldemort:
	sudo docker exec -it genopedia-dev.genodata-api.voldemort bash

ssh-api-mysql:
	sudo docker exec -it genopedia-dev.genodata-api.mysql bash

ssh-api-web:
	sudo docker exec -it genopedia-dev.genodata-api.web bash

ssh-admin-mysql:
	sudo docker exec -it genopedia-dev.genodata-admin.mysql bash

ssh-admin-web:
	sudo docker exec -it genopedia-dev.genodata-admin.web bash
