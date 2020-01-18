#include <stdio.h>

int main(void) {
 
    int input;
    
    printf("Insert a number: ");
    scanf("%d", &input);
    printf("Inserted value: %d\n", input);
    printf("Address: %u(decimal), %p(hexadecimal)\n", &input, &input);
    printf("Address: %d(decimal), %#p(hexadecimal)\n", &input, &input);
    printf("Size of address value: %d\n", sizeof(&input));
    
    return 0;
}