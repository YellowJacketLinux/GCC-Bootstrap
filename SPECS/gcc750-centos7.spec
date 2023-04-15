%global debug_package %{nil}
%global __strip /bin/true

%global tarname gcc

Name:           gcc750
Version:        7.5.0
Release:        1
Summary:        GCC 7.5.0 with gnat

Group:          Bootstrapping
License:        GPL/LGPL
URL:            https://gcc.gnu.org/
Source0:        %{tarname}-%{version}.tar.xz

BuildRequires:  libgnat-devel gcc-gnat
BuildRequires:  gmp-devel mpfr-devel libmpc-devel

%description
This builds GCC 7.5.0 with ADA (GNAT) in CentOS 7 for the purpose of
bootstraping ADA support into LFS 11.3.

It does not actually build an RPM but it built with -bi so that a
tarball can be made to unpack in an LFS 11.3 /opt

%prep
%setup -n %{tarname}-%{version}
#sed -i.orig '/m64=/s/lib64/lib/' gcc/config/i386/t-linux64


%build
mkdir build && cd build
../configure \
  --prefix=/opt/gcc750 \
  --datadir=%{_datadir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir} \
  --disable-multilib  \
  --with-system-zlib  \
  --disable-libssp \
  --disable-libquadmath \
  --disable-libgomp \
  --disable-libvtv \
  --disable-libsanitizer \
  --enable-libada \
  --enable-linker-build-id \
  --enable-languages=c,c++,ada
make -j4

%install
cd build
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}
pushd %{buildroot}/opt/gcc750
rm -f lib64/*.la
mv lib64/* lib/ && rmdir lib64

cp -p /usr/lib64/libmpfr.so.4.1.1 %{buildroot}/opt/gcc750/lib/
ln -s libmpfr.so.4.1.1 %{buildroot}/opt/gcc750/lib/libmpfr.so.4
cp -p /usr/lib64/libgmp.so.10.2.0 %{buildroot}/opt/gcc750/lib/
ln -s libgmp.so.10.2.0 %{buildroot}/opt/gcc750/lib/libgmp.so.10

cd ..

tar -cf gcc750-centos7-built.tar gcc750
popd

/bin/false

%files
%doc



%changelog

