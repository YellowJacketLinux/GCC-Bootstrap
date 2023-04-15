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


Step Two: Build Ada and D enabled GCC 10.4.0 in LFS 11.3
--------------------------------------------------------

GCC 10.4.0 does require a working `gnat` to build Ada support, which
I had via the CentOS 7 compiled GCC 7.5.0, but that version of GCC
still allows building D support without needing an existing `gdc`
compiler.

So using the Ada capable GCC 7.5.0, I built an Ada and D capable
GCC 10.4.0.

This build was built with `/opt/gcc1040` as the install prefix and also
was done without building the optional additional libraries and it also
was built within RPM but this time I did create an actual RPM package.

For the compile options, see [gcc1040.spec](SPECS/gcc1040.spec).

Once it was build, I deleted the /opt/gcc750 directory and updated the
`/etc/ld.so.conf.d/bootstrap.conf` file to load libraries from
`/opt/gcc1040/lib` and installed the package.

Again I compiled the `hello.adb` program just to make the Ada part of
the GCC 10.4.0 build was working.


Step Three: Build Limited Ada and D enabled GCC 12.2.0 in LFS 11.3
------------------------------------------------------------------

This step probably could have been skipped.

Using the GCC 10.4.0 build, I built an Ada and D enabled build of
GCC 12.2.0 but again with the additional optional libraries disabled
from the GCC built. The install prefix was `/opt/gcc1220` and again
RPM was used, see [gcc1220.spec](SPECS/gcc1220.spec).

Once the RPM was built, I again updated the `/etc/ld.so.conf.d/bootstrap.conf`
file to load libraries from `/opt/gcc1040/lib` and then I removed the
`gcc1040` package and installed the `gcc1220` package.

Again I compiled the `hello.adb` program just to make the Ada part of
the GCC 10.4.0 build was working.


Step Four: Build Ada and D Enabled GCC as System GCC
----------------------------------------------------

I then updated my system [gcc.spec](https://github.com/YellowJacketLinux/LFS/blob/main/SPECS/gcc.spec)
to build GCC with a prefix of `/usr` and all the optional libraries.

I added the ability to build it using the GCC in `/opt/gcc1220` by
simply defining the `%{gccbootstrap}` macro when building it.

One built, I deleted the `/etc/ld.so.conf.d/bootstrap.conf` file
and removed the `gcc1220` package, and upgraded my system GCC packages.

I tested it by again compiling the `hello.adb` program and also by
building the newly released `linux-2.6.24` kerne.


Step Five: Run Tests
--------------------

Finally I enabled running of the test suites and did one more build
of the system GCC 12.2.0 package with the tests, which takes over seven
hours on my hardware (I do not do parallel tests).

The tests results were as good as I could hope.


Future LFS
----------

When I build a future version of LFS, I will deviate from the instructions
in the book and build GCC with Ada and D support from the start.

Note that doing so would not have worked from CentOS 7 without first
building another GCC in CentOS 7 because the GCC in CentOS 7 is too old
to have D support, and while it does have Ada support, GCC 12.2.0 requires
a newer GCC with Ada support than 4.8.5.

Well, I could have by building an Ada and D capable GCC 10.4.0 in
CentOS 7.9 but...

Anyway, now that I have modern GCC with Ada and D, I should be able to
avoid needing to do a bootstrap process again by just always building
LFS with Ada and D support from the start.
