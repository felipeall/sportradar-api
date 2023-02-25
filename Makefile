black:
	black .

check_black:
	black . --check

isort:
	isort .

check_isort:
	isort .

flake:
	pflake8 .

mkdocs:
	cp README.md docs/index.md
	cp docs/mkdocs.yml .
	mkdocs serve

reformat: black isort flake
check: check_black check_isort flake