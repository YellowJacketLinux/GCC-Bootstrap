#!/bin/bash

if [ "`whoami`" == "root" ]; then
  echo "Danger, Will Robinson!"
  echo "Do not execute me as r00t"
  exit 1
elif [ ! -f gcc-14.2.0.tar.xz ]; then
  echo "The GCC source tarball gcc-14.2.0.tar.xz"
  echo "must exist in same directory this script"
  echo "is run from."
  exit 1
fi

[ -d gcc-14.2.0 ] && rm -rf gcc-14.2.0

tar -Jxf gcc-14.2.0.tar.xz

export PATH=/opt/gcc-bootstrap/bin:${PATH}
cd gcc-14.2.0

sed -e '/m64=/s/lib64/lib/' \
    -i.orig gcc/config/i386/t-linux64

mkdir build && cd build

../configure --prefix=/usr \
            LD=ld \
            --enable-default-pie     \
            --enable-default-ssp     \
            --disable-multilib       \
            --disable-fixincludes    \
            --with-system-zlib       \
            --enable-linker-build-id \
            --enable-languages=c,c++,ada,d

make -j4
if [ $? -ne 0 ]; then
  echo "Failed building gcc"
  exit 1
fi

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
echo
echo "To review the tests:"
echo
echo "  cd ${CWD}"
echo
echo "View the file \"gcc.check.log\" and search for the term 'Summary'"
echo
echo "If all looks good, as root run:"
echo
echo "  make install"
echo
echo "You probably should delete the .la libtool files installed"
echo "in /usr/lib"
