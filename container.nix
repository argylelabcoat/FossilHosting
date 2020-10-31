{ pkgs ? import <nixpkgs> {} }:

pkgs.dockerTools.buildImage {
  name = "hello-docker";
  contents = with pkgs;[ python38 fossil ];
  config = {
    Cmd = [ "${pkgs.hello}/bin/hello" ];
  };
}
