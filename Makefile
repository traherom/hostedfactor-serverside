# Local work
build:
	./bin/build.sh

compose_build: build
	docker-compose build

up: compose_build
	docker-compose up -d
	docker-compose logs -f --tail=1

attach:
	docker attach hostedfactor_web_1

stop:
	docker-compose stop

logs:
	docker-compose logs web

# Deployment
push: build
	git push
	docker tag hostedfactor:build traherom/hostedfactor:release
	docker push traherom/hostedfactor:release

deploy: test push
	ansible-playbook ansible/web.yml

# Testing and cleanup
test: compose_build
	docker-compose run web python -Wall /code/manage.py test

lint: compose_build
	docker-compose run web flake8 .

check: compose_build lint test
	echo "Success"

# Database management
make_migrations: compose_build
	docker-compose run web python manage.py makemigrations

migrate: compose_build
	docker-compose run web python manage.py migrate

loaddata: compose_build
	docker-compose run web python manage.py loaddata exec_envs

pgcli: compose_build
	docker-compose run web pgcli -U postgres -h db

# Low-level management
python: compose_build
	docker-compose run web python manage.py shell

bash: compose_build
	docker-compose run web bash
