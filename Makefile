.PHONY: venv all tests static unit integraion install publish clean

all: venv
	@./venv/bin/python3 -m build

venv:
	@python3 -m venv venv
	@./venv/bin/pip install -r ./requirements_dev.txt

tests: static unit integration

static: venv
	@echo "Running static tests..."
	@./venv/bin/flake8 ./src --statistics
	@cd ./src && ../venv/bin/pylint . --recursive=y
	@./venv/bin/black --check ./src
	@./venv/bin/isort --check ./src

unit: venv
	@echo "Running unit tests..."
	@./venv/bin/pytest ./src/tests/unit

integration: venv
	@cd ./src
	@echo "Running integration tests..."
	@./venv/bin/pytest ./src/tests/integration

clean:
	@rm -rf ./venv
	@rm -rf ./dist
	@rm -rf ./call_center_tools.egg-info
