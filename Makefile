lint:
	pycodestyle generate.py jobs/*.py

fix_style:
	autopep8 --in-place --aggressive --aggressive generate.py jobs/*.py

build:
	docker build -t sld --rm .
	./copy_build.sh

fix_permissions:
	sudo chown -R $(shell id -u):$(shell id -g) build

clean:
	docker rmi -f sld $(shell docker images -f 'dangling=true' -q)
	rm -Rf build noises

.PHONY: lint fix_style build fix_permissions clean
