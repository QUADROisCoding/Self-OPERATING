{pkgs}: {
  deps = [
    pkgs.libGLU
    pkgs.libGL
    pkgs.xvfb-run
    pkgs.scrot
    pkgs.tesseract
    pkgs.zlib
    pkgs.tk
    pkgs.tcl
    pkgs.openjpeg
    pkgs.libxcrypt
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.freetype
    pkgs.postgresql
    pkgs.openssl
  ];
}
