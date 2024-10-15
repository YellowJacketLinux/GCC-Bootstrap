#!/bin/bash

# This is to be run in LFS 12.2

MYPREFIX="/opt/gcc-bootstrap"

[ -d gcc-14.2.0 ] && rm -rf gcc-14.2.0
tar -Jxf gcc-14.2.0.tar.xz

export PATH=/opt/gcc-prebootstrap/bin:${PATH}
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

# tests take a LONG time

sed -e '/cpython/d'               -i ../gcc/testsuite/gcc.dg/plugin/plugin.exp
sed -e 's/no-pic /&-no-pie /'     -i ../gcc/testsuite/gcc.target/i386/pr113689-1.c
sed -e 's/300000/(1|300000)/'     -i ../libgomp/testsuite/libgomp.c-c++-common/pr109062.c
sed -e 's/{ target nonpic } //' \
    -e '/GOTPCREL/d'              -i ../gcc/testsuite/gcc.target/i386/fentryname3.c

CWD="`pwd`"
echo
echo "Running tests. This will take a VERY long time. Watch the tests in"
echo "another console via:"
echo
echo "  tail -f ${CWD}/gcc.check.log"
echo

make -k check > gcc.check.log

echo
echo "To see a test summary:"
echo
echo "  cd ${CWD}"
echo "  ../contrib/test_summary"
echo
echo "If all looks good, as root run"
echo
echo "  make install"
