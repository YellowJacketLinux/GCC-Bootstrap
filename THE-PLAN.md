The Plan
========

This is an attempt to create a new GNU/Linux distribution. The why is in the
file `THE_WHY.md` but TLDR, because I can. Well, because I think I can. Maybe,
and even if not, I will still learn a lot...

The new distribution will be called ‘Yellow-Jacket GNU/Linux’ (abbreviated as
‘YJL’) and will be heavily based upon ‘Linux From Scratch’ (LFS) but will have
many influences from my years with Red Hat Linux, including use of RPM as the
package manager.


Phase One: LFS Bootstrap
------------------------

Create the needed shell scripts to build the current SystemD LFS (12.2 as I
type) on a USB thumb drive that can then boot an `x86_64` system and rebuild
itself to the hard drive of that system. Long term goal is a generic image that
can be copied onto any thumb drive via `dd`, boot a generic `x86_64` system, and
build LFS on it. Short term goal is specific to my system.

For the git related to Phase One, see
https://github.com/YellowJacketLinux/lfs-buildscripts/tree/main


Phase Two: GCC Bootstrap
------------------------

This phase is what the git is about.

The GCC built by LFS does not support building the Ada or D compilers. Both of
those compilers are useful on a GNU/Linux system.

Once I have a hard-disk install booting, the very first order of business is to
rebuild GCC for full compiler support.

To compile GCC with Ada and D support, a working Ada and D compiler is needed.

My LFS 11.3 system has those. What I did back then, on CentOS 7.9 (my build host
for LFS 11.3) I built GCC 7.5.0 with Ada (`gnat`) support, with an install
prefix of `/opt/gcc750`. GCC 7.5.0 was the newest GCC I could get to build in
CentOS 7.9 with Ada.

I had to copy a few shared libraries from the CentOS 7 system into
`/opt/gcc750/lib` but once I did that, I was able to use that GCC in LFS 11.3 to
then build an Ada and D capable GCC 10.4.0 within `/opt/gcc1040`, GCC 7.5.0
would not succesfully build an Ada and D capable GCC 12.2.0.

However I was then able to use GCC 10.4.0 to build the Ada and D capable GCC
12.2.0 which is the GCC version in LFS 11.3.

For the LFS 12.2 GCC bootstrap, I *suspect* I can use the Ada and D capable GCC
GCC 12.2.0 in LFS 11.3 to build an Ada and D capable GCC 14.2.0 installed in
`/opt/gcc1420` that I can then use in LFS 12.2 to bootstrap the system GCC, of
course running the full test suite before installing.

I tried adding Ada and D support to the GCC building of LFS 12.2 Chapter 5 and
it caused a build failure, so it is *possible* I will need another intemediary.

Anyway, boostrapping an Ada and D capable GCC within LFS 12.2 will be my first
priority once it is booting.


Phase Three: Building RPM
--------------------------

The needed libraries to build RPM will need to be built and installed, and then
RPM will be built and installed.


Phase Four: RPM Bootstrap
-------------------------

Once RPM is built and installed comes the long and tedious task of writing the
needed RPM spec files to rebuild every package on the system in RPM. Much of
that work has already been done from my LFS 11.3 system but the spec files need
to be updated and some still needed to be written when the water pipe broke.


Phase Five: Mock Build Environment
----------------------------------

After the system is RPM bootstrapped, I have to build and configure a Mock build
environment for packages, see https://rpm-software-management.github.io/mock/

A Mock build build environment is essential for clean, untainted packages. I
have used Mock build environments in the past but creating one from scratch for
a new distribution is something I have not done.


Phase Six: XFCE
---------------

Once the system is RPM bootstrapped, I can start building the software needed
for the XFCE desktop environment.

My *personal* preferred desktop environment is actually MATE but XFCE is what I
am building as the default desktop environment for YJL.


Phase Seven: Installer
----------------------

With XFCE running, a bootable USB thumb drive that can install the system from
RPM packages will have the be created. That will be when YJL becomes a reality
and not just a concept I am working towards.


