{ pkgs, self, python3 }:
pkgs.python3Packages.buildPythonPackage {
  pname = "stunkymonkey-passworts";
  version = builtins.substring 0 8 self.lastModifiedDate;

  src = self;
  format = "other";

  propagatedBuildInputs = with python3.pkgs; [
    flask
    flask_wtf
    gevent
    gunicorn
  ];

  buildPhase = ''
    runHook preBuild

    for f in ./dict/*.txt;
      # skip the words calculations, because they do not make much sense
      do [[ "$f" != *"words"* ]] && ${python3.pythonOnBuildForHost.interpreter} calc.py -f "$f";
    done

    mkdir -p $out/
    cp -r ./* $out/

    runHook postBuild
  '';

  dontInstall = true;

  passthru = {
    inherit python3;
  };

  meta = with pkgs.lib; {
    description = "Passworts to create rememberable passwords";
    license = licenses.mit;
    platforms = platforms.all;
  };
}
