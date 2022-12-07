#!/usr/bin/env python3

import sys
from dataclasses import dataclass, field
from typing import Iterable, Optional

import pytest


@dataclass
class File:
    name: str
    size: int

    @classmethod
    def from_string(cls, string: str):
        size_s, name = string.split()
        size = int(size_s)
        return cls(name, size)


@dataclass
class Directory:
    name: str
    files: dict[str, File] = field(default_factory=dict)
    dirs: dict[str, "Directory"] = field(default_factory=dict)
    parent: Optional["Directory"] = None

    def add_dir(self, directory: "Directory") -> "Directory":
        self.dirs[directory.name] = directory
        directory.parent = self
        return directory

    def add_file(self, file: File) -> File:
        self.files[file.name] = file
        return file

    def get_dir(self, path: list[str]) -> "Directory":
        if path == []:
            return self
        subdir = self.dirs[path[0]]
        return subdir.get_dir(path[1:])

    def ensure_dir(self, path: list[str]) -> "Directory":
        if path == []:
            return self

        if path[0] not in self.dirs:
            subdir = self.add_dir(Directory(path[0]))
        else:
            subdir = self.dirs[path[0]]

        return subdir.ensure_dir(path[1:])

    def iter_files(self) -> Iterable[File]:
        for file in self.files.values():
            yield file

        for dir in self.dirs.values():
            yield from dir.iter_files()

    def iter_dirs(self) -> Iterable["Directory"]:
        for dir in self.dirs.values():
            yield dir

        for dir in self.dirs.values():
            yield from dir.iter_dirs()

    def get_total_size(self) -> int:
        retval = 0
        for file in self.iter_files():
            retval += file.size
        return retval

    def format(self):
        retval = []
        retval.append(f"==> current dir: {self.name}")
        for dir in self.dirs.values():
            retval.append(f"dir: {dir.name}")
        for file in self.files.values():
            retval.append(f"file: {file}")

        for dir in self.dirs.values():
            retval.extend(dir.format())

        return retval

    def print(self):
        print("\n".join(self.format()))


def parse(lines: list[str]):
    current_path: list[str] = []
    S_CMD = 0
    S_LS = 1
    state: int = S_CMD

    current_dir = Directory("/")
    root_dir = current_dir

    for line in lines:
        if line.startswith("$ cd "):
            state = S_CMD
            change_dir = line.split()[-1]
            if change_dir == "/":
                current_dir = root_dir
                current_path = []
            elif change_dir.startswith("/"):
                current_path = change_dir.split("/")[1:]
                current_dir = root_dir.ensure_dir(current_path)
            elif change_dir == "..":
                current_path.pop()
                assert current_dir.parent is not None
                current_dir = current_dir.parent
            else:
                current_path.append(change_dir)
                current_dir = current_dir.ensure_dir([change_dir])

        elif line == "$ ls":
            state = S_LS
        elif state == S_LS:
            if line.startswith("dir "):
                name = line.split()[-1]
                current_dir.ensure_dir([name])
            elif line.startswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
                current_dir.add_file(File.from_string(line))

    return root_dir


def part01(root_dir: Directory) -> int:
    retval = 0
    for subdir in root_dir.iter_dirs():
        subdir_size = subdir.get_total_size()
        if subdir_size < 100000:
            retval += subdir_size
    return retval


def part02(root_dir: Directory) -> int:
    fs_size = 70000000
    required_space = 30000000

    taken = root_dir.get_total_size()
    free_space = fs_size - taken
    to_delete = required_space - free_space
    assert to_delete > 0

    retval: Optional[int] = None

    for subdir in root_dir.iter_dirs():
        dir_size = subdir.get_total_size()
        if dir_size >= to_delete:
            if retval is None or dir_size < retval:
                retval = dir_size

    assert retval is not None
    return retval


def main():
    with open("aoc_07.txt") as infile:
        lines = [x.strip() for x in infile]

    root_dir = parse(lines)
    print(part01(root_dir))
    print(part02(root_dir))


@pytest.fixture
def root_dir() -> Directory:
    root_dir = Directory("/")
    root_dir.add_file(File("b.txt", 14848514))
    root_dir.add_file(File("c.dat", 8504156))
    dir_a = root_dir.ensure_dir(["a"])
    dir_d = root_dir.ensure_dir(["d"])

    dir_e = dir_a.ensure_dir(["e"])
    dir_a.add_file(File("f", 29116))
    dir_a.add_file(File("g", 2557))
    dir_a.add_file(File("h.lst", 62596))

    dir_e.add_file(File("i", 584))

    dir_d.add_file(File("j", 4060174))
    dir_d.add_file(File("d.log", 8033020))
    dir_d.add_file(File("d.ext", 5626152))
    dir_d.add_file(File("k", 7214296))
    return root_dir


def test_parse(root_dir: Directory):
    lines = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]

    parsed = parse(lines)
    assert parsed.format() == root_dir.format()


def test_part01(root_dir: Directory):
    assert part01(root_dir) == 95437


def test_part02(root_dir: Directory):
    assert part02(root_dir) == 24933642


def test_get_dir():
    root = Directory("")
    foo = Directory("foo")
    bar = foo.add_dir(Directory("bar"))
    root.add_dir(foo)
    tmp = root.add_dir(Directory("tmp"))

    root.get_dir(["foo", "bar"]) is bar
    root.get_dir(["foo"]) is foo
    root.get_dir(["tmp"]) is tmp
    root.get_dir([]) is root


def test_ensure_dir():
    root = Directory("")
    baz = root.ensure_dir(["foo", "bar", "baz"])

    root.get_dir(["foo", "bar", "baz"]) is baz

    root.get_dir(["foo", "bar"]) is baz.parent
    root.get_dir(["foo"]) is baz.parent.parent


def test_iter_files_empty():
    root = Directory("")
    root.ensure_dir(["foo", "bar", "baz"])
    root.ensure_dir(["tmp"])

    assert list(root.iter_files()) == []


def test_iter_files():
    root = Directory("")
    baz = root.ensure_dir(["foo", "bar", "baz"])
    tmp = root.ensure_dir(["tmp"])
    baz.add_file(File("foo.txt", 1234))
    baz.add_file(File("bar.txt", 5555))
    tmp.add_file(File("tmp.txt", 999))
    tmp.add_file(File("tmp2.txt", 1111))
    root.add_file(File("root.txt", 1234))

    assert list(root.iter_files()) == [
        File("root.txt", 1234),
        File("foo.txt", 1234),
        File("bar.txt", 5555),
        File("tmp.txt", 999),
        File("tmp2.txt", 1111),
    ]


def test_iter_dirs():
    root = Directory("")
    foo = root.ensure_dir(["foo"])
    bar = foo.ensure_dir(["bar"])
    baz = bar.ensure_dir(["baz"])
    tmp = root.ensure_dir(["tmp"])

    assert list(root.iter_dirs()) == [foo, tmp, bar, baz]


def test_total_size():
    root = Directory("")
    baz = root.ensure_dir(["foo", "bar", "baz"])
    tmp = root.ensure_dir(["tmp"])
    baz.add_file(File("foo.txt", 1234))
    baz.add_file(File("bar.txt", 5555))
    tmp.add_file(File("tmp.txt", 999))
    tmp.add_file(File("tmp2.txt", 1111))
    root.add_file(File("root.txt", 1234))

    root.get_total_size() == 1234 + 5555 + 999 + 1111 + 1234
    tmp.get_total_size() == 999 + 1111


if __name__ == "__main__":
    sys.exit(main())
