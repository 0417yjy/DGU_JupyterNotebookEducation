#include <stdio.h>

int main(void) {
    int mult, n, i;
    
    for (;;) {
        printf("Insert any number from 1 to 20 (0 to exit): ");
        scanf("%d", &n);
        if(n<=0)
            break;
        for(i=1, mult = 1;i<=n;i++)
            mult *= i;
        printf("n! is: %d\n", mult);
    }
    puts("Exit..");
    
    return 0;
        
}