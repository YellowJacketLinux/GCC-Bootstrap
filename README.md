Boostrapping Ada and D support within LFS 11.3
==============================================

In the LFS book, GCC is only built with C and C++ support.

Additional languages can then be added by rebuilding GCC in BLFS (see
[BLFS GCC-12.2.0](https://www.linuxfromscratch.org/blfs/view/stable/general/gcc.html))
but there is a gotcha.

For Ada support (GCC `gnat`) and D support (GCC `gdc`), GCC 12.2.0
requires that you have are building from a GCC that already has
`gnat` and `gdc` support.

GCC has always been that way with respect to `gnat` which I believe was
originally a separate package merged into GCC, but I believe needing
`gdc` to build D support is new as of the GCC 12 series.

Anyway, I am not sure that I will ever *personally* need D support but
Ada is named after Lovelace who is credited with having written the
first computer program (for an analog mechanical computing device).
Just for the nostalgia of that name, I do sometimes play with Ada.

So...to get Ada and D into my LFS 11.3/YJL Environment:


Step One: Build Ada enabled GCC 7.5.0 in CentOS 7.9
---------------------------------------------------

CentOS 7.9 (my host for building 11.3) has an ancient GCC 4.8.5 but
it does have Ada support.

Using that GCC, I built a vanilla (unpatched) GCC 7.5.0 with Ada
support, using a install prefix of `/opt/gcc750`.

The GCC 7.5.0 I build in CentOS 7.9 has all the optional libraries
disabled, they are not needed when only using it to build another
GCC.

The build process can be seen in
[gcc750-centos7.spec](SPECS/gcc750-centos7.spec).

Note that while I did use an RPM spec file build it, I did not actually
create an RPM file. RPM was just a convenient way to do the build
process, but in the `%install` section I just make a tarball from the
installed result and then exit RPM via `/bin/false`.

Note that (other than glibc) GCC only has three library dependencies
outside of GCC itself:

* MPFR
* GMP
* MPC

The MPFR and MPC in CentOS 7.9 are not ABI compatible with the newer
versions of those shared libraries in LFS 11.3 so I did have to copy
the older CentOS 7 versions of those shared libraries into the directory
with the GCC 7.5.0 shared libraries.

A more elegant solution would have been to build the newer versions
of those libraries to link GCC 7.5.0 against but I did not do that.

After copying the tarball out of the BUILDROOT I booted into LFS 11.3,
created a `/etc/ld.so.conf.d/bootstrap.conf` file containing
`/opt/gcc750/lib`, unpacked the tarball in `/opt`, and then ran
`/sbin/ldconfig` so that the GCC 7.5.0 build could load all the
libraries it needed.

To test that it working, I added `/opt/gcc750/bin` to patch and
compiled the [hello.adb](hello.adb) program:

    gnatmake hello.adb

When the program compiled without a segfault and ran without a segfault
I knew I was probably good to continue.
