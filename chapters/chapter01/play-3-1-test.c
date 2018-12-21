#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<fcntl.h>
#include<sys/types.h>
#include<sys/wait.h>
#include<sys/stat.h>

const char sing[] = "hello!";
const char singnl[] = "hello!\n";
const char doub[] = "hello!hello!";
const char doubnl[] = "hello!hello!\n";

void sig_handler (int signo) {
    fprintf(stderr, "Failed to exec!\n");
    exit(1);
}

int main (int argc, char **argv) {

    // Setting up child process
    // Fork - Exec - Wait

    signal(SIGINT, sig_handler);

    pid_t parent = getpid();
    pid_t child = fork();

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

    child = fork();

    if (child == -1) {  // Error!
        fprintf(stderr, "Failed to fork!\n");
        return 1;
    } else if (child == 0) { // Child      
        execl(argv[1], argv[1], NULL); // Add command line options here
        kill(parent, SIGINT);
        return 1;
    }

    waitpid(child, &status, 0);

    // Time to analyze results

    struct stat statbuf;
    if (stat("./message.txt", &statbuf)) {
        printf("Error analyzing message.txt\n");
        return 1;
    }

    if ((statbuf.st_mode & S_IRGRP) || (statbuf.st_mode & S_IROTH)) {
        printf("Other people can read your file!\n");
    } else {
        printf("Only you can read your file. Nice!\n");
    }

    char buffer[1024];
    memset(buffer, 0, 1024);

    int fd = open("./message.txt", O_RDONLY);
    read(fd, buffer, 1024);

    buffer[1023] = '\0';

    printf("After two runs, message.txt looks like: \n\n%s\n", buffer);

    if (strcmp(buffer, sing) == 0 || strcmp(buffer, singnl) == 0) {
        printf("Looks good!\n");
    } else if (strcmp(buffer, doub) == 0 || strcmp(buffer, doubnl) == 0) {
        printf("Looks like you are appending to the file instead of truncating it. Check your flags!\n");
    } else {
        printf("Something looks off, try checking your flags and your write statement\n");
    }

    return 0;
}