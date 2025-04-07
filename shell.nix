{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.setuptools
    pkgs.python3Packages.wheel
    pkgs.python3Packages.pytest
    pkgs.python3Packages.black
    pkgs.python3Packages.jsonschema
    pkgs.vscode
    pkgs.git
  ];

  vscodeExtensions = with pkgs.vscode-extensions; [
    ms-python.python
    ms-python.vscode-pylance
    ms-toolsai.jupyter
  ];

  shellHook = ''
    echo "Development environment for Prj is set up."
  '';
}

