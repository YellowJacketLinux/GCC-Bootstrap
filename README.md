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

In LFS 11.3, I used the Ada and D capable GCC 12.3.0 to compile an Ada and D
capable GCC 14.2.0. This was done using the script
[`build-pre-bootstrap.sh`](build-pre-bootstrap.sh) (in this git) within my LFS
11.3 system.

The GCC 14.2.0 the script built in LFS 11.3 has an install target of
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

Theoretically this step could be skipped and I could have built the system GCC
without this step but I would rather be safe.

Using the `/opt/gcc-preboostrap` build of GCC 14.2.0 as the compiler, I did an
identical build within LFS 12.2 but using `/opt/gcc-bootstrap` as the install
prefix. This was done with the script
[`build-bootstrap.sh`](build-bootstrap.sh) (in this git) within my LFS 12.2
system.

In this case, since I was building the compiler that would then build the system
compiler, I did run the test suite after it finished (and it takes a long time).

There were a few unexpected errors but when building GCC there *always* are. The
tests that had unexpected errors are shown below:

                    === libphobos Summary ===
    
    # of expected passes            412
    # of unexpected failures        3
    
    ...
    
                    === libphobos Summary ===
    
    # of expected passes            389
    # of unexpected failures        1
    
    ...
    
                    === gcc Summary ===
    
    # of expected passes            88026
    # of unexpected failures        2
    # of expected failures          776
    # of unsupported tests          1611
    
    ...
    
                    === g++ Summary ===
    
    # of expected passes            15870
    # of unexpected failures        2
    # of expected failures          32
    # of unsupported tests          209

Summaries from the log file *without* unexpected failures are not shown. I was
very happy with the test results. 
 
Once built and installed, I did make a tarball of `/opt/gcc-bootstrap` just in
case I screw the system up and need to re-install LFS 12.2, I can then use that
tarball to go straight to Step Three.

The `/opt/gcc-prebootstrap` directory was then deleted and the
`/etc/ld.so.conf.d/gcc-prebootstrap.conf` file was renamed to
`/etc/ld.so.conf.d/gcc-bootstrap.conf` with the path in it updated to point to
`/opt/gcc-preboostrap/lib`, of course re-running `ldconfig` afterwards.

The system is now ready to build the Ada and D capable GCC as the system GCC
with an install prefix of `/usr`.


Step Three: Build Ada and D enabled GCC 14.2.0 with `/usr` prefix
-----------------------------------------------------------------

Step three replaced the original LFS build of GCC with a build that supports Ada
and D, using the GCC built in Step Two. This was done using the script
[`CH08.27-gcc-modified.sh`](CH08.27-gcc-modified.sh) (in this git) within my LFS
12.2 system.

The build used the same build options as the LFS Chapter 8 build of GCC except
with the following configure options removed:

    --enable-languages=c,c++ \
    --disable-bootstrap      \
    --enable-host-pie        \

and the following configure options added:

    --enable-linker-build-id \
    --enable-languages=c,c++,ada,d

The `--disable-bootstrap` option was removed because despite bootstrap builds
taking a *much* longer time, it is generally recommended. BLFS also removes that
configure option so GCC does an internal bootstrap.

The `--enable-host-pie` option was removed because it causes a build failure
when compiling many of the languages beyong `c` and `c++`, including Ada. BLFS
also does not use that configure option.

The `--enable-linker-build-id` option was added because RPM will need it to make
debug packages.

As with Step Two, there were very few errors in the `make -k check` log and the
errors that were there were the same. The build is a good build.


Phase Two of `THE-PLAN.md` is complete. `/opt/gcc-bootstrap` was deleted and the
`/etc/ld.so.conf.d/gcc-bootstrap.conf` file was removed.


Future GCC Build
----------------

During ‘Phase Four’ of `THE-PLAN.md` (RPM Bootstrap), GCC will be rebuilt as RPM
packages. During that rebuild, support for all the other languages GCC supports
will also be built.
