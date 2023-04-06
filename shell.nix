{ pkgs ? import <nixpkgs> {} }:

let
  pythonEnv = pkgs.python37;
in
  pkgs.mkShell {
    buildInputs = [
      pythonEnv
      pythonEnv.pkgs.pip
    ];
  }