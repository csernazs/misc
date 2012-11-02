
all: prime p012 libprime.so

clean:
	rm -f prime p012 libprime.so

prime: prime.c Makefile
	gcc -g -O3  prime.c -o prime

libprime.so: prime.c Makefile
	gcc -g -O3 -DSHARED prime.c -shared -o libprime.so	
	
p012: p012.c
	gcc -Wall -g -O3  p012.c -lm -o p012
	
	
	