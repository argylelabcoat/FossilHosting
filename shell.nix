{ pkgs ? import <nixpkgs> {} }:
  with pkgs; mkShell {
    buildInputs = [ fossil ] ++ (with python38Packages;[
click
flask
requests
    ]);
}
