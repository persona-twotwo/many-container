#include <stdio.h>
#include <unistd.h>   // fork(), getpid(), getppid() 등을 사용하기 위한 헤더 파일
#include <sys/types.h>
#include <sys/wait.h> // wait() 시스템 콜을 사용하기 위한 헤더 파일
#include <stdlib.h>   // exit() 함수 사용을 위한 헤더 파일
#include <time.h>     // 시간 측정을 위한 헤더 파일

int main() {
    
    pid_t pid;
    unsigned long long count = 0;
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start); // 시작 시간 측정

    while (1) {
	    count++;

        pid = fork();
        if (pid < 0) {
            perror("fork 실패");
            return 1;
        }
        else if (pid == 0) {
            exit(0);
        }
        else {
            int status;
            wait(&status);

            if (WIFEXITED(status)) {
                if(count%10000 == 0){
                    clock_gettime(CLOCK_MONOTONIC, &end); // 종료 시간 측정
                    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
                    clock_gettime(CLOCK_MONOTONIC, &start); // 시작 시간 측정
                    printf("%llu %f\n", count, elapsed);
                    fflush(stdout);
                }       
            }
        }
        
    }

    return 0;
}
