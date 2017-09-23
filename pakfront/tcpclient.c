/* 
 * tcpclient.c - A simple TCP client
 * usage: tcpclient <host> <port>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#define BUFSIZE 58790
#define HOSTNAME "localhost"
#define SIZBYTES 4

/* 
 * error - wrapper for perror
 */
void error(char *msg) {
    perror(msg);
    exit(0);
}
int getfromstdin(char * buf){
	char byteTmp;
	for( int i = 0; i < BUFSIZE; i ++){
		scanf("%c",&byteTmp);
		buf[i] = byteTmp;
	}
	return 0;
}
int getmsgsize(char * buf){
	int num = 0;
	char temp;
	for(int i = 0; i < SIZBYTES/2;i++){
		temp = buf[i];
		buf[i] = buf[SIZBYTES-i];
		buf[SIZBYTES-i]= temp;	
	}
	return *((int*)(buf));
}

int main(int argc, char **argv) {
    int sockfd, portno, n;
    struct sockaddr_in serveraddr;
    struct hostent *server;
    char *hostname;
    char buf[BUFSIZE];
    getfromstdin(buf);
    int msglen = getmsgsize(buf);
    FILE* pOutput = fopen("output.JPG","wb");
    printf("Len Requested: %d\n",msglen);
    
    /* check command line arguments */
    if (argc != 2) {
       fprintf(stderr,"usage: %s <port>\n", argv[0]);
       exit(0);
    }
    hostname = HOSTNAME;
    portno = atoi(argv[1]);

    /* socket: create the socket */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) 
        error("ERROR opening socket");

    /* gethostbyname: get the server's DNS entry */
    server = gethostbyname(hostname);
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host as %s\n", hostname);
        exit(0);
    }

    /* build the server's Internet address */
    bzero((char *) &serveraddr, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
	  (char *)&serveraddr.sin_addr.s_addr, server->h_length);
    serveraddr.sin_port = htons(portno);

    /* connect: create a connection with the server */
    if (connect(sockfd, &serveraddr, sizeof(serveraddr)) < 0) 
      error("ERROR connecting");


    /* send the message line to the server */
    char * msg;
//fwrite(msg, msglen, 1, pOutput);
    for(int i  = 0; i < msglen; i += n){
	    msg = &buf[SIZBYTES+1+i];
	    n = write(sockfd, msg, msglen-i);
	    printf("Bytes sent: %d\n",n);
	    if (n < 0) {
	      n = 0;
	    }
    }
    close(sockfd);
    return 0;
}
