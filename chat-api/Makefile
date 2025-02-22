.PHONY: install run format lint

install:
	poetry install

run:
	poetry run uvicorn event_advert:app --reload

format:
	poetry run black .

lint:
	poetry run flake8 .
