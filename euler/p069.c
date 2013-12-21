#include <stdio.h>

int gcd(int a, int b) {
    while (a!=b) {
        if (a>b) {
            a = a - b;
        } else {
            b = b - a;
        }
    }
    return a;
}

int phi(int n) {
    int cnt = 1;
    int i;
    for (i=2;i<=n;i++) {
        if (gcd(n, i) == 1) {
            cnt += 1;
        }
    }

    return cnt;
}

int main(void) {
    int i;
    for (i=2; i<=1000000; i++) {
        printf("%d\n", i);
        phi(i);
//        printf("%d\n", phi(i));
    }
    return 0;
}
