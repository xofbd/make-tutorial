SHELL = /bin/bash
ACTIVATE_VENV = source venv/bin/activate
INPUTS = $(wildcard requirements/*.in)
REQS = $(patsubst requirements/%.in,requirements/%.txt,$(INPUTS))
OUTPUTS = .base .dev

.PHONY: all
all: clean-all color_films_by_year.png

data:
	mkdir $@

data/films.csv: | .base data
	$(ACTIVATE_VENV) && python src/oscar_nominees.py $@

data/film_color_data.csv: data/films.csv
	$(ACTIVATE_VENV) && python src/film_color.py $< $@

color_films_by_year.png: data/film_color_data.csv
	$(ACTIVATE_VENV) && python src/color_films_by_year.py $< $@

# Virtual Environments
venv: requirements/pip-tools.txt
	python3 -m venv $@
	$(ACTIVATE_VENV) && pip install -r $<

.base: requirements/base.txt
	$(ACTIVATE_VENV) && pip-sync $<
	rm -f .dev
	touch .base

.dev: requirements/dev.txt
	$(ACTIVATE_VENV) && pip-sync $(REQS)
	rm -f .base
	touch .dev

# Utility
.PHONY: clean clean-all
clean:
	rm -rf venv
	find . | grep __pycache__ | xargs rm -rf
	rm -f $(OUTPUTS)

clean-all: clean
	rm -rf data
	rm -f color_films_by_year.png

.PHONY: tests test-unit test-lint
tests: test-lint test-unit

test-unit: .dev
	-$(ACTIVATE_VENV) && pytest -s tests

test-lint: .dev
	-$(ACTIVATE_VENV) && flake8 src

# Requirements
.PHONY: requirements
requirements: $(REQS)

requirements/%.txt: requirements/%.in | venv
	$(ACTIVATE_VENV) && pip-compile $<

requirements/dev.txt: requirements/base.txt

requirements/pip-tools.txt:
	: # Avoid circular reference
