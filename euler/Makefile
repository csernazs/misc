
all: prime p012 libprime.so

clean:
	rm -f prime p012 libprime.so

prime: prime.c Makefile
	gcc -g -march=native -O3 prime.c -lm -o prime

libprime.so: prime.c Makefile
	gcc -g -march=native -O3 -fPIC -DSHARED prime.c -lm -shared -o libprime.so
	
p012: p012.c
	gcc -Wall -g -march=native -O3  p012.c -lm -o p012
	
	
	