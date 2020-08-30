.PHONY: image clean run

image:
	docker build -t cma_notebook .

clean:
	docker rmi cma_notebook

run:
	docker run --rm -it -v "${PWD}/notebooks:/home/jovyan/notebooks" -p 8888:8888 cma_notebook
