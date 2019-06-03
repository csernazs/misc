#include <arpa/inet.h>
#include <errno.h>
#include <netinet/ip.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#include "database.h"

#define BIND_HOST "127.0.0.1"
#define BIND_PORT 5000

#define OP_GET 0
#define OP_PUT 1
#define OP_RESULT 2

struct message {
    char op;
    char key[512];
    char value[512];
};

int start(void)
{
    int sockfd;
    uint16_t socket_port = ntohs(BIND_PORT);
    struct in_addr bind_address;
    struct sockaddr_in socket_address;

    if (inet_aton(BIND_HOST, &bind_address) == 0) {
        printf("Invalid address: %s\n", BIND_HOST);
        return -1;
    }

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        printf("Error at socket(): %s\n", strerror(errno));
        return -1;
    }

    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int)) == -1) {
        printf("Error at setsockopt(): %s\n", strerror(errno));
        return -1;
    }

    socket_address.sin_family = AF_INET;
    socket_address.sin_addr = bind_address;
    socket_address.sin_port = socket_port;

    if (bind(sockfd, (struct sockaddr*)&socket_address, sizeof(socket_address)) == -1) {
        printf("Error at bind(): %s\n", strerror(errno));
        return -1;
    }

    return sockfd;
}

void print_message(struct message* msg)
{
    if (msg->op == OP_GET) {
        printf("GET key=%s\n", msg->key);
    }
    else if (msg->op == OP_PUT) {
        printf("PUT key='%s' value='%s'\n", msg->key, msg->value);
    }
    else if (msg->op == OP_RESULT) {
        printf("RESULT key='%s' value='%s'\n", msg->key, msg->value);
    }

}

int main(void)
{
    int sockfd;
    ssize_t received;
    struct sockaddr client_address;
    socklen_t client_address_length = sizeof(client_address);
    struct message message_in;
    struct message message_out;
    char* value;

    db_put("foo", "bar");

    sockfd = start();
    if (sockfd == -1) {
        return 1;
    }
    while (1) {
        received = recvfrom(sockfd, &message_in, sizeof(message_in), 0, &client_address, &client_address_length);
        printf("Received %ld bytes\n", received);
        printf("< ");
        print_message(&message_in);
        message_out.op = OP_GET;
        if (message_in.op == OP_GET) {
            message_out.op = OP_RESULT;

            value = db_get(message_in.key);
            if (value == NULL) {
                printf("key '%s' not found\n", message_in.key);
                memset(message_out.key, '\0', sizeof(message_out.key));
                memset(message_out.value, '\0', sizeof(message_out.value));
            } else {
                printf("key '%s' found: '%s'\n", message_in.key, value);
                strcpy(message_out.key, message_in.key);
                strcpy(message_out.value, value);
            }
        }

        if (message_in.op == OP_PUT) {
            db_put(message_in.key, message_in.value);
            message_out = message_in;
        }
        printf("> ");
        print_message(&message_out);

        sendto(sockfd, &message_out, received, 0, &client_address, client_address_length);
    }
    close(sockfd);
    return 0;
}
