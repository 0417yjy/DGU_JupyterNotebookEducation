#include <stdio.h>

#define MAX 50

int main(void) {
    int i = 1, sum = 0;
    
    while(i<=MAX)
        sum += i++;
    
    printf("Sum from 1 to 10 is %d\n", sum);

    return 0;
}