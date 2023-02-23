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

reformat: black isort flake
check: check_black check_isort flake