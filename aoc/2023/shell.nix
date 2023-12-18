{ pkgs ? import <nixpkgs> {} }:

let
  unstable = import <nixos-unstable> { config = { allowUnfree = true; }; };
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python311Packages.pytest
    python311Packages.icecream
    python311Packages.mypy
    python311Packages.numpy
    python311Packages.pillow
    bashInteractive
  ];
}
