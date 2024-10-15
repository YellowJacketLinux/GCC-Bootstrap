#!/bin/bash

# This is to be run in Ada/D Capable LFS 11.3

MYPREFIX="/opt/gcc-prebootstrap"

[ -d gcc-14.2.0 ] && rm -rf gcc-14.2.0
tar -Jxf gcc-14.2.0.tar.xz

cd gcc-14.2.0

sed -i.orig '/m64=/s/lib64/lib/' gcc/config/i386/t-linux64

mkdir build && cd build

../configure \
  --prefix=${MYPREFIX}  \
  --datadir=${MYPREFIX}/share \
  --mandir=${MYPREFIX}/share/man \
  --infodir=${MYPREFIX}/info \
  --disable-multilib \
  --with-system-zlib \
  --disable-libssp \
  --disable-libquadmath \
  --disable-libgomp \
  --disable-libvtv \
  --disable-libsanitizer \
  --enable-libada \
  --enable-linker-build-id \
  --enable-languages=c,c++,ada,d
make -j4

if [ $? -ne 0 ]; then
  echo "Failed building gcc"
  exit 1
fi

echo
echo "build complete. As root, run make install (inside build directory)."

# note - tests are not run at this point, way too time consuming.
