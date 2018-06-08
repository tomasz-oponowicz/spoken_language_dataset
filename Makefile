lint:
	pycodestyle generate.py jobs

fix_style:
	pycodestyle generate.py jobs

build:
	docker build -t sld --rm .
	./copy_build.sh

fix_permissions:
	sudo chown -R $(shell id -u):$(shell id -g) build

clean:
	docker rmi sld $(shell docker images -f 'dangling=true' -q)
	rm -Rf build noises

.PHONY: lint fix_style build fix_permissions clean
