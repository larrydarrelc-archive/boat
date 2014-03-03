.PHONY: main server clients

main: server

server:
	python main.py

clients:
	python clients_runner.py
