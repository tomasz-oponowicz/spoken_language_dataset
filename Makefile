build:
	docker build -t elmo --rm .
	./copy_build.sh

clean:
	docker rmi elmo $(shell docker images -f 'dangling=true' -q)

.PHONY: build
