build:
	docker build -t elmo --rm .
	./copy_build.sh

fix_permissions:
	sudo chown -R $(shell id -u):$(shell id -g) ./build

clean:
	docker rmi elmo $(shell docker images -f 'dangling=true' -q)

.PHONY: build
