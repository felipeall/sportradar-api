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

gh-docs:
	cp README.md docs/index.md
	pip install mkdocs mkdocs-material mkdocstrings[python] mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin mkdocs-git-authors-plugin
	git config user.name 'github-actions[bot]' && git config user.email 'github-actions[bot]@users.noreply.github.com'
	mkdocs gh-deploy --force

reformat: black isort flake
check: check_black check_isort flake