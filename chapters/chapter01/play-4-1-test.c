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

    pid_t parent = getpid();
    pid_t child = fork();

    signal(SIGINT, sig_handler);

    if (child == -1) {  // Error!
        fprintf(stderr, "Failed to fork!\n");
        return 1;
    } else if (child == 0) { // Child    
        execl(argv[1], argv[1], NULL); // Add command line options here
        kill(parent, SIGINT);
        return 1;
    }

    int status = 0;
    waitpid(child, &status, 0);
    

    buffer[1023] = '\0'; // Prevent issues with this

    // Time to analyze results

    printf("Here is the contents of the error.txt\n");
    system("cat errors.txt");

    return 0;
}