{ pkgs ? import <nixpkgs> {} }:

let
  unstable = import <nixos-unstable> { config = { allowUnfree = true; }; };
in pkgs.mkShell {
  buildInputs = [
    pkgs.python3Packages.icecream
    # pkgs.python3Packages.pylint
    # pkgs.python3Packages.black
    # pkgs.python3Packages.autopep8
    # pkgs.python3Packages.rope
    # pkgs.python3Packages.lxml
    # pkgs.python3Packages.setuptools
    # pkgs.python3Packages.tox
    # pkgs.python3Packages.pyglet
    # pkgs.python3Packages.future
    # pkgs.python3Packages.pytest
    # pkgs.python3Packages.pip
    pkgs.python3Packages.numpy
    pkgs.python3Packages.termcolor
    # pkgs.python3Packages.bitarray

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
