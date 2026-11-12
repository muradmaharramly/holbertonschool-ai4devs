#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *format_user_tag(const char *username, int id) {
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
    char *tag = format_user_tag("developer", 42);
    if (tag) {
        printf("Tag: %s\n", tag);
        free(tag);
    }
    return 0;
}
