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

In LFS 11.3, I used the Ada and D capable GCC 12.2.0 to compile an Ada and D
capable GCC 14.2.0. This was done using the script
[`build-pre-bootstrap.sh`](build-pre-bootstrap.sh) (in this git) within my LFS
11.3 system.

The GCC 12.2.0 the script built in LFS 11.3 has an install target of
`/opt/gcc-prebootstrap` and was only built with support for `c`,`c++`,`d`, and
`ada`.

Once built, the directory `/opt/gcc-preboostrap` was packed into a tarball to be
unpacked in the same location in the LFS 12.2 environment.

Note that (other than glibc) GCC only has three library dependencies outside of
GCC itself:

* MPFR (libmpfr.so.6 in LFS 12.2)
* GMP (libgmp.so.10, libgmpxx.so.4 in LFS 12.2)
* MPC (libmpc.so.3 in LFS 12.2)

Since those are the same ABI versions in LFS 11.3, I did not need to worry about
copying the the LFS 11.3 versions into `/opt/gcc-preboostrap/lib`.

The tarball was unpacked into LFS 12.2 for Step Two. The file
`/etc/ld.so.conf.d/gcc-prebootstrap.conf` was created containing:

    /opt/gcc-preboostrap/lib

I then ran `ldconfig` as root so the linker knew where the libraries are.

To test that it working in LFS 12.2, I added `/opt/gcc-prebootstrap/bin` to my
`$PATH` and compiled the [hello.adb](hello.adb) program:

    gnatmake hello.adb

The program compiled without a segfault and ran without a segfault so I knew I
was probably good to go.


Step Two: Build Ada and D enabled GCC 14.2.0 in LFS 12.2
--------------------------------------------------------

Theoretically this step could be skipped but I would rather be safe.

Using the `/opt/gcc-preboostrap` build of GCC 14.2.0, I will rebuild it in LFS
12.2 with the same configure options except using an install target of
`/opt/gcc-bootstrap`.

In this case, I will not to attempt to compile the `hello.adb` program after
the build because the test suite will have tested that it works in the LFS 12.2
host it is built in.

Once built and installed, the `/opt/gcc-prebootstrap` directory can be deleted.
The `/etc/ld.so.conf.d/gcc-prebootstrap.conf` file gets renamed to
`/etc/ld.so.conf.d/gcc-bootstrap.conf` and the path inside changed to
`/opt/gcc-preboostrap/lib` re-running `ldconfig` to update the library linker.


Step Three: Build Ada and D enabled GCC 14.2.0 with `/usr` prefix
-----------------------------------------------------------------

Using the `/opt/gcc-bootstrap` build of GCC 14.2.0, it will be built once again
except using `/usr` as the install prefix, *replacing* the GCC 14.2.0 built
during the build of LFS 12.2.

This build will use the same build options as the LFS Chapter 8 build of GCC
except with the following:

    --enable-libada \
    --enable-linker-build-id \
    --enable-languages=c,c++,ada,d

Of course, to build it, it will use the freshly built GCC from
`/opt/gcc-bootstrap`

Phase Two of `THE-PLAN.md` will be complete. `/opt/gcc-bootstrap` can be deleted
and the `/etc/ld.so.conf.d/gcc-bootstrap.conf` file can be deleted.


Future GCC
----------

During ‘Phase Four’ of `THE-PLAN.md` (RPM Bootstrap), GCC will be rebuilt as RPM
packages. During that rebuild, support for all the other languages GCC supports
will be built.
