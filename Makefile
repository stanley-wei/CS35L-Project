# Targets
migrate:
	python3 manage.py migrate 

makemigrations:
	python3 manage.py makemigrations 

showmigrations:
	python3 manage.py showmigrations

shell:
	python3 manage.py shell

runserver:
	python3 manage.py runserver

test:
	python3 manage.py test 

# Phony targets
.PHONY: migrate makemigrations showmigrations shell runserver test
