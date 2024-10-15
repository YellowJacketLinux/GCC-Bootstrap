Boostrapping Ada and D support within LFS 12.2
==============================================

In the LFS book, GCC is only built with C and C++ support.

There are many additional languages that can be built. Two of them, Ada (GCC
`gnat`) and D (GCC `gdc`), require the GCC compiler used to build them *already*
have Ada and D support.

The host distribution I used to build LFS 12.2 (LFS 11.3) has them, added by me
previously, but the stripped down GCC used to build the LFS `tools` that then
builds LFS is not built with Ada and D support, so GCC with Ada and D support
has to be bootstrapped *after* building LFS 12.2.

So...to get Ada and D into my LFS 12.2/YJL Environment:


Step One: Build Ada enabled GCC 12.2 in LFS 11.3
------------------------------------------------

In LFS 11.3, use the Ada and D capable GCC 12.2.0 to compile an Ada and D
capable GCC 14.2.0.

The GCC 12.2.0 built in LFS 11.2 will have an install target of
`/opt/gcc-prebootstrap` and will only be built for support for `c`,`c++`,`d`,
and `ada`.

Once built, the directory `/opt/gcc-preboostrap` will be packed into a tarball.

Note that (other than glibc) GCC only has three library dependencies outside of
GCC itself:

* MPFR
* GMP
* MPC

If any of those libraries have an ABI compatibility issue between LFS 11.3 and
LFS 12.2 (I have not checked yet), then the LFS 11.3 versions of those libraries
will be copies into the `/opt/gcc-prebootstrap/lib` directory before making the
tarball and a file called `/etc/ld.so.conf.d/prebootstrap.conf` in LFS 12.2
containing `/opt/gcc-preboostrap/lib` will tell the dynamic library linker where
to find them.

The tarball will be unpacked into LFS 12.2.

To test that it working, I'll add `/opt/gcc-prebootstrap/bin` to my `$PATH` and
compiled the [hello.adb](hello.adb) program:

    gnatmake hello.adb

If the program compiles without a segfault and runs without a segfault I will
know I am probably good to go.


Step Two: Build Ada and D enabled GCC 14.2.0 in LFS 12.2
--------------------------------------------------------

Using the `/opt/gcc-preboostrap` build of GCC 14.2.0, I will rebuild it in LFS
12.2 with the same configure options except using an install target of
`/opt/gcc-bootstrap`.

In this case, I will not to attempt to compile the `hello.adb` program after
the build because the test suite will test that it works in the LFS 12.2 host it
is built in.

Once built and installed, the `/opt/gcc-prebootstrap` directory can be deleted.

Step Three: Build Ada and D enabled GCC 14.2.0 with `/usr` prefix
-----------------------------------------------------------------

Using the `/opt/gcc-bootstrap` build of GCC 14.2.0, it will be built once again
except using `/usr` as the install prefix, *replacing* the GCC 14.2.0 built
during the build of LFS 12.2.

Phase Two of `THE-PLAN.md` will be complete.


Future GCC
----------

During ‘Phase Four’ of `THE-PLAN.md` (RPM Bootstrap), GCC will be rebuilt as RPM
packages. During that rebuild, support for all the other languages GCC supports
will be built.
