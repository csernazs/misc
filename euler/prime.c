#include <stdio.h>
#include <stdlib.h>
#include <math.h>
       
long* get_primes(long n) {
    char* numbers;
    long i;
    long n_max;
    long t;
    long* ip;
    long* retval;
    long length = 0;
    

        
    n_max = n/2;
    
    
    numbers = calloc(n, sizeof(char));

    for (i=2;i<n_max;i++) {
        if (numbers[i] == 1) {
            continue;
        }
        
        t = i*2;
        while (t<=n) {
            numbers[t] = 1;
            t = t + i;
        }
        
    }

    for (i=2; i<n; i++) {
        if (numbers[i] == 0) {
            length++;
        }
    }

    retval = calloc(length+2, sizeof(long));
    *retval = length;
    
    ip = retval+1;
    for (i=2; i<n; i++) {
        if (numbers[i] == 0) {
            *ip = i;
            ip++;
        }
    }

    return retval;
    
}

int is_prime(long n) {
    int div;
    
    long limit;;
    limit = (long) sqrt((double) n);
    
    for (div=2; div<limit; div++) {
        if (n%div == 0) {
            return 0;
        }
    
    }
    return 1;

}

#ifndef SHARED
int main(void) {
    long* primes;
    long p;
    primes = get_primes(1000000);
    primes++; // 1st item is the length
    while (p = *primes) {
        printf("%ld\n", p);
        primes++;
    }
    return 0;
}
#endif

