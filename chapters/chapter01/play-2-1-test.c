#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<sys/types.h>
#include<sys/wait.h>

const char answer[] = "I think\nI thin\nI thi\nI th\nI t\nI \nI\n";

void sig_handler (int signo) {
    fprintf(stderr, "Failed to exec!\n");
    exit(1);
}

int main (int argc, char **argv) {

    // Setting up child process
    // Fork - Exec - Wait

    int pipefd[2];

    if (pipe(pipefd)) {
        fprintf(stderr, "Failed to setup pipe!\n");
        return 1;
    }

    pid_t parent = getpid();
    pid_t child = fork();

    signal(SIGINT, sig_handler);

    if (child == -1) {  // Error!
        fprintf(stderr, "Failed to fork!\n");
        return 1;
    } else if (child == 0) { // Child
        close(pipefd[0]);
        dup2(pipefd[1], STDOUT_FILENO);
        close(pipefd[1]);        
        execl(argv[1], argv[1], NULL); // Add command line options here
        kill(parent, SIGINT);
        return 1;
    }

    close(pipefd[1]);

    int status = 0;
    char buffer[1024];
    memset(buffer, 0, 1024);

    read(pipefd[0], buffer, 1024);
    waitpid(child, &status, 0);
    
    int retval = WEXITSTATUS(status);

    buffer[1023] = '\0'; // Prevent issues with this

    // Time to analyze results

    printf("Program returned: %d\n", retval);
    if (retval == 7) {
        printf("Nice! Now try returning 1023\n");
    } else if (retval == 255) {
        printf("Interesting :)\n");
    } else {
        printf("Try returning 7 or 1023\n");
    }

    if (buffer[0] == '\0') {
        printf("You didn't write anything to stdout! Check your write statement.\n");
    } else {
        printf("You printed out:\n\n%s\n", buffer);
        if (strcmp(buffer, answer) == 0) {
            printf("Nice work!\n");
        } else {
            printf("Looks like something isn't quite right with your write statements\n");
        }
    }

    return 0;
}