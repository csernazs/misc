#!/usr/bin/env python3


import socket
import sys
import struct

GET = 0
PUT = 1
RESULT = 2


class Message:
    def __init__(self, op, key, value):
        self.op = op
        self.key = key
        self.value = value

    def dump(self) -> bytes:
        if isinstance(self.key, str):
            key = self.key.encode("utf8")
        else:
            key = self.key

        if isinstance(self.value, str):
            value = self.value.encode("utf8")
        else:
            value = self.value

        return struct.pack("b512s512s", self.op, key, value)

    @classmethod
    def load(cls, payload: bytes):
        op, key, value = struct.unpack("b512s512s", payload)
        key = key.decode("utf-8")
        value = value.decode("utf-8")
        return cls(op, key, value)

    def __str__(self):
        return "<{} key={} value={}>".format(self.op, self.key, self.value)


class Client:
    BUFSIZE = 65535

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None
        self.connect()

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.host, self.port))
        self.sock = sock

    def put(self, key, value):
        self.sock.send(Message(PUT, key, value).dump())
        self.sock.recv(self.BUFSIZE)

    def get(self, key):
        self.sock.send(Message(GET, key, "").dump())
        data = self.sock.recv(self.BUFSIZE)
        msg = Message.load(data)
        if msg.key.rstrip("\0") == "":
            return None
        else:
            return msg.value.rstrip("\0")

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def __getitem__(self, key: str):
        retval = self.get(key)
        if retval is None:
            raise KeyError(key)
        else:
            return retval

    def __setitem__(self, key: str, value: str):
        self.put(key, value)


def main():
    host, port = sys.argv[1], int(sys.argv[2])
    client = Client(host, port)
    client["zzz"] = "Bar"
    print(repr(client["zzz"]))

    print(repr(client.get("ooo")))
    client.close()


if __name__ == "__main__":
    sys.exit(main())
