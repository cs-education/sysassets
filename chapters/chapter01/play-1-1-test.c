#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<sys/types.h>
#include<sys/wait.h>

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

    waitpid(child, &status, 0);
    read(pipefd[0], buffer, 1024);
    
    int retval = WEXITSTATUS(status);

    buffer[1023] = '\0'; // Prevent issues with this

    // Time to analyze results

    printf("Program returned: %d\n", retval);
    if (retval != 0) {
        printf("Use a return value of 0 to indicate that your program completed successfully\n");
    }

    if (buffer[0] == '\0') {
        printf("You didn't write anything to stdout! Check your write statement.\n");
    } else {
        printf("You printed out:\n\n%s\nVery Cool!\n", buffer);
    }

    return 0;
}