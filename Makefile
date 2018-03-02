TEMP=tmp

build:
	rm -Rf ${TEMP} && mkdir ${TEMP}
	docker build -t elmo --rm .
	docker run --rm -v $(shell pwd)/tmp:/tmp elmo sh -c "cp -r /app/noises/* /tmp"

clean:
	docker rmi elmo $(shell docker images -f 'dangling=true' -q)

.PHONY: build
