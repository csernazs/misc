all: server database
CFLAGS=-g -Wall

server: server.c database.c
	gcc $(CFLAGS) -DDBLIB server.c database.c -o server

database: database.c
	gcc $(CFLAGS) database.c -o database

clean:
	rm -f server database
