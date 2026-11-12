#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *format_user_tag(const char *username, int id) {
    if (!username) {
        return NULL;
    }
    char id_str[12];
    snprintf(id_str, sizeof(id_str), "#%04d", id);
    
    size_t total_len = strlen(username) + strlen(id_str);
    char *buffer = (char *)malloc(total_len + 1);
    if (!buffer) {
        return NULL;
    }
    
    strcpy(buffer, username);
    strcat(buffer, id_str);
    return buffer;
}

int main(void) {
    char *t1 = format_user_tag("developer", 42);
    printf("Test 1 (Standard Tag): %s\n", (t1 && strcmp(t1, "developer#0042") == 0) ? "PASS" : "FAIL");
    free(t1);

    char *t2 = format_user_tag("", 1);
    printf("Test 2 (Empty Username): %s\n", (t2 && strcmp(t2, "#0001") == 0) ? "PASS" : "FAIL");
    free(t2);

    char *t3 = format_user_tag("admin", 9999);
    printf("Test 3 (Large ID): %s\n", (t3 && strcmp(t3, "admin#9999") == 0) ? "PASS" : "FAIL");
    free(t3);

    return 0;
}
