#include <stdio.h>
#include <string.h>

void reverse_string(char *str) {
    if (!str) return;
    int len = strlen(str)
    char *start = str;
    char *end = str + len - 1;
    char temp;

    while (start < end) {
        temp = *start;
        *start = *end;
        *end = temp;
        start++;
        end--;
    }
}

int main(void) {
    char word[] = "holberton";
    reverse_string(word);
    printf("Reversed: %s\n", word);
    return 0;
}
