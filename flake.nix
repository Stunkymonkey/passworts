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

      perSystem =
        { pkgs
        , self'
        , ...
        }: {
          packages = {

            default = pkgs.stdenvNoCC.mkDerivation {
              pname = "stunkymonkey-passworts";
              version = builtins.substring 0 8 self.lastModifiedDate;
              src = self;
              nativeBuildInputs =
                let
                  python-with-my-packages = pkgs.python3.withPackages (ps: with ps; [
                    flask
                    flask_wtf

                    # move to shell
                    black
                    pylint
                    isort
                  ]);
                in
                [
                  python-with-my-packages
                ];
              buildPhase = ''
                # generate stuff
                runHook preBuild
                mkdir -p $out
                hugo --minify --destination $out
                runHook postBuild
              '';
              dontInstall = true;
              meta = with pkgs.lib; {
                description = "My awesome homepage";
                license = licenses.mit;
                platforms = platforms.all;
              };
            };

          };

          devShells.default = pkgs.mkShellNoCC {
            packages = with pkgs; [
              black
            ];
            name = "home";
            inputsFrom = [
              self'.packages.default
            ];
          };
        };
    };
}
