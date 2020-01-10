#include <stdio.h>

int main(void) {
 char a[100];
 printf("이름을 입력하세요: ");
 scanf("%s", &a);
 printf("환영합니다. %s\n", a);
 return 0;
}