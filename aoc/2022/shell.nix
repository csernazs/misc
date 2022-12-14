{ pkgs ? import <nixpkgs> {} }:

let
  unstable = import <nixos-unstable> { config = { allowUnfree = true; }; };
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python3Packages.pytest
    python3Packages.icecream
    python3Packages.mypy
    python3Packages.numpy
    python3Packages.pillow
    bashInteractive
  ];
}
