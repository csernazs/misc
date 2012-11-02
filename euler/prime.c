#include <stdio.h>
#include <stdlib.h>


int* get_primes(int n) {
    char* numbers;
    int i;
    int n_max;
    int t;
    int* ip;
    int* retval;
    int length = 0;
    

        
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

    retval = calloc(length+1, sizeof(int));
    ip = retval;
    for (i=2; i<n; i++) {
        if (numbers[i] == 0) {
            *ip = i;
            ip++;
        }
    }

    return retval;
    
}

#ifndef SHARED
int main(void) {
    int* primes;
    int p;
    primes = get_primes(1000000);
    while (p = *primes) {
        printf("%d\n", p);
        primes++;
    }
    return 0;
}
#endif

