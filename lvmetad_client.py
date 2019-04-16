#!/usr/bin/env python3

import sys
import os
import socket
import pdb
from pprint import pprint


r"""
[pid   276] select(1024, [3], NULL, NULL, NULL <unfinished ...>
[pid 17354] set_robust_list(0x7ff559cdd9e0, 24) = 0
[pid 17354] read(5, "request = \"hello\"\n\n##\n", 32) = 22
[pid 17354] write(5, "response = \"OK\"\nprotocol = \"lvmetad\"\nversion = 1\n", 49) = 49
[pid 17354] write(5, "\n##\n", 4)       = 4
[pid 17354] read(5, "request = \"get_global_info\"\ntoke", 32) = 32
[pid 17354] read(5, "n = \"skip\"\npid = 17353\ncmd = \"pvs\"\n\n##\n", 1024) = 39
[pid 17354] getpid()                    = 276
[pid 17354] write(5, "response = \"OK\"\nglobal_invalid = 0\nglobal_disable = 0\ndisable_reason = \"none\"\ndaemon_pid = 276\ntoken = \"filter:3239235440\"\nupdate_cmd = \"\"\nupdate_pid = 0\nupdate_begin = 0\nupdate_timeout = 0\n", 190) = 190
[pid 17354] write(5, "\n##\n", 4)       = 4
[pid 17354] read(5, "request = \"get_global_info\"\ntoke", 32) = 32
[pid 17354] read(5, "n = \"skip\"\npid = 17353\ncmd = \"pvs\"\n\n##\n", 1024) = 39
[pid 17354] getpid()                    = 276
[pid 17354] write(5, "response = \"OK\"\nglobal_invalid = 0\nglobal_disable = 0\ndisable_reason = \"none\"\ndaemon_pid = 276\ntoken = \"filter:3239235440\"\nupdate_cmd = \"\"\nupdate_pid = 0\nupdate_begin = 0\nupdate_timeout = 0\n", 190) = 190
[pid 17354] write(5, "\n##\n", 4)       = 4
[pid 17354] read(5, "request=\"vg_list\"\ntoken =\"filter", 32) = 32
[pid 17354] read(5, ":3239235440\"\nupdate_timeout =10\npid =17353\ncmd =\"pvs\"\n\n##\n", 1024) = 58
[pid 17354] write(5, "response=\"OK\"\nvolume_groups {\n}\n\n\n", 34) = 34
[pid 17354] write(5, "\n##\n", 4)       = 4
[pid 17354] read(5, "request=\"pv_list\"\ntoken =\"filter", 32) = 32
[pid 17354] read(5, ":3239235440\"\nupdate_timeout =10\npid =17353\ncmd =\"pvs\"\n\n##\n", 1024) = 58
[pid 17354] write(5, "response=\"OK\"\nphysical_volumes {\n}\n\n\n", 37) = 37
[pid 17354] write(5, "\n##\n", 4)       = 4
[pid 17354] read(5, "", 32)             = 0
[pid 17354] close(5)                    = 0
[pid 17354] madvise(0x7ff5594dd000, 8368128, MADV_DONTNEED) = 0
[pid 17354] exit(0)                     = ?
[pid 17354] +++ exited with 0 +++
"""


def iter_lines(sock):
    buff = b""
    while True:
        buff += sock.recv(4096)
        if buff == b"":
            return

        while True:
            idx = buff.find(b"\n")
            while idx > -1:
                line = buff[:idx]
                buff = buff[idx + 1 :]
                yield line.decode("utf-8")
                idx = buff.find(b"\n")


class ClientError(Exception):
    pass


class Message(dict):
    @classmethod
    def load(cls, lines):
        key_base = []
        retval = {}
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#") or not stripped:
                continue

            if line.endswith("{"):
                key_base.append(line.strip("\t {"))
                continue

            if stripped == "}":
                key_base.pop()
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            else:
                value = int(value)

            if key_base:
                key = "{}.{}".format(".".join(key_base), key)
            retval[key] = value

        return cls(retval)

    def dump(self):
        lines = []
        for key, value in self.items():
            if isinstance(value, str):
                msg_value = '"{}"'.format(value)
            elif isinstance(value, int):
                msg_value = str(value)
            else:
                raise TypeError("Unsupported type: {!r}".format(value))

            lines.append("{} = {}".format(key, msg_value))

        lines.append("##")

        return "\n".join(lines) + "\n"


class Client:
    def __init__(self, path="/run/lvm/lvmetad.socket", debug=True):
        self.path = path
        self.sock = None
        self.version = None
        self.token = None
        self.debug = debug

        self.connect()
        self.hello()

    def _log_debug(self, msg):
        if self.debug:
            print(msg)

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self.path)
        self.sock = sock

    def close(self):
        self.sock.close()

    def recv_message(self):
        lines = []
        for line in iter_lines(self.sock):
            self._log_debug("<<< {}".format(line))

            if line == "##":
                break

            lines.append(line)

        return Message.load(lines)

    def send_dict(self, dict):
        msg = Message(dict)
        self.send_message(msg)

    def send_message(self, msg: Message):
        serialized = msg.dump()
        for line in serialized.split("\n"):
            self._log_debug(">>> {}".format(line))
        self.sock.sendall(serialized.encode("utf-8"))

    def hello(self):
        self.send_dict({"request": "hello"})
        resp = self.recv_message()
        if resp["version"] != 1:
            raise ClientError("Unsupported version: {}".format(resp["version"]))

        self.version = resp["version"]

    def get_token(self, cmd: str):
        self.send_dict(dict(request="get_global_info", token="skip", pid=os.getpid(), cmd=cmd))
        resp = self.recv_message()
        self.token = resp["token"]

    def ensure_token(self, cmd: str):
        if self.token:
            return
        self.get_token(cmd)

    def pv_list(self):
        cmd = "pvs"
        self.ensure_token(cmd)
        self.send_dict(dict(request="pv_list", token=self.token, update_timeout=10, pid=os.getpid(), cmd=cmd))
        resp = self.recv_message()

        pvs = {}
        for key, value in resp.items():
            if key.startswith("physical_volumes."):
                fields = key.split(".")
                pv_id = fields[1]
                pv_key = ".".join(fields[2:])
                if pv_id not in pvs:
                    pvs[pv_id] = {}
                pvs[pv_id][pv_key] = value

        pprint(pvs)

    def vg_list(self):
        cmd = "vgs"
        self.ensure_token(cmd)
        self.send_dict(dict(request="vg_list", token=self.token, update_timeout=10, pid=os.getpid(), cmd=cmd))
        self.recv_message()


def main():
    client = Client()
    client.pv_list()
    client.vg_list()
    client.close()


if __name__ == "__main__":
    sys.exit(main())
