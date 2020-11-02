{ pkgs ? import <nixpkgs> {} }:
  with pkgs; mkShell {
    buildInputs = [ fossil sassc go ] ++ (with python38Packages;[
click
flask
requests
    ]);
}
