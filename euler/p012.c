#include <math.h>
#include <stdio.h>

int divisors(int n) {
    int i;
    int retval = 2;
    int n_max;
    
    n_max = (int) sqrt(n);
    
    for (i=2; i<n_max+1; i++) {
        if (n%i == 0) {
            retval = retval + 2;
        }
    }
    if (n == n_max*n_max) {
        retval--;
    }
    return retval;
}

int main(void) {
    int add = 1;
    int curr = 1;
    int divs;
    
    while (1) {
        divs = divisors(curr);
        if (divs>500) {
            printf("%d\t%d\n", curr, divs);
            break;
        }
        
        add++;
        curr += add;
    
    }

    return (0);
    

}


