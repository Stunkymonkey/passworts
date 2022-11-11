{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, nixpkgs, flake-parts }:
    flake-parts.lib.mkFlake { inherit self; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      flake = {
        #nixosModules.passworts = import ./module.nix;

        overlay = final: prev: {
          passworts = self.packages.${prev.stdenv.hostPlatform.system}.passworts;
        };
        nixosModules.passworts = { pkgs, lib, config, ... }: {
          imports = [ ./module.nix ];
          nixpkgs.overlays = [ self.overlay ];
        };
      };

      perSystem =
        { pkgs
        , self'
        , ...
        }: {
          packages = rec {
            default = passworts;
            passworts = pkgs.callPackage ./package.nix { inherit self; };
          };

          devShells.default = pkgs.mkShellNoCC {
            name = "home";
            inputsFrom = [
              self'.packages.default
            ];
            # development dependencies
            packages = with pkgs; [
              black
              pylint
              isort
            ];
          };
        };
    };
}
