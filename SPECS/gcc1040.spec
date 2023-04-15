%global debug_package %{nil}
%global __strip /bin/true

%global triplet x86_64-pc-linux-gnu

%global tarname gcc

Name:     gcc1040
Version:  10.4.0
Release:  0.dev1%{?dist}
Summary:  GCC 10.4.0 with gnat,d

Group:    Bootstrapping
License:  GPL/LGPL
URL:      https://gcc.gnu.org/
Source0:  %{tarname}-%{version}.tar.xz

BuildRequires:	gmp-devel mpfr-devel libmpc-devel

%description
This package builds GCC 10.4.0 in LFS, using an ADA enabled GCC 7.5.0
built in CentOS 7 as the compiler.

It is intended as a temporary build to build a native GCC 12.2.0 in

%prep
%setup -n %{tarname}-%{version}
sed -i.orig '/m64=/s/lib64/lib/' gcc/config/i386/t-linux64


%build
export PATH=/opt/gcc750/bin:${PATH}
mkdir build && cd build
../configure \
  --prefix=/opt/gcc1040 \
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
  --enable-languages=c,c++,ada,d
make -j4


%install
export PATH=/opt/gcc750/bin:${PATH}
cd build
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_infodir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir /opt/gcc1040
/opt/gcc1040/bin
/opt/gcc1040/include
%dir /opt/gcc1040/lib
/opt/gcc1040/lib/*.spec
/opt/gcc1040/lib/*.a
/opt/gcc1040/lib/*.so
/opt/gcc1040/lib/*.py
%attr(0755,root,root) /opt/gcc1040/lib/libatomic.so.1.2.0
/opt/gcc1040/lib/libatomic.so.1
%attr(0755,root,root) /opt/gcc1040/lib/libcc1.so.0.0.0
/opt/gcc1040/lib/libcc1.so.0
%attr(0755,root,root) /opt/gcc1040/lib/libgdruntime.so.1.0.0
/opt/gcc1040/lib/libgdruntime.so.1
%attr(0755,root,root) /opt/gcc1040/lib/libgphobos.so.1.0.0
/opt/gcc1040/lib/libgphobos.so.1
%attr(0755,root,root) /opt/gcc1040/lib/libitm.so.1.0.0
/opt/gcc1040/lib/libitm.so.1
%attr(0755,root,root) /opt/gcc1040/lib/libstdc++.so.6.0.28
/opt/gcc1040/lib/libstdc++.so.6
/opt/gcc1040/lib/libgcc_s.so.1
/opt/gcc1040/lib/gcc
%dir /opt/gcc1040/libexec
%dir /opt/gcc1040/libexec/gcc
%dir /opt/gcc1040/libexec/gcc/%{triplet}
%dir /opt/gcc1040/libexec/gcc/%{triplet}/%{version}
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/cc1
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/cc1plus
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/collect2
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/d21
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/gnat1
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/lto-wrapper
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/lto1
%attr(0755,root,root) /opt/gcc1040/libexec/gcc/%{triplet}/%{version}/liblto_plugin.so.0.0.0
/opt/gcc1040/libexec/gcc/%{triplet}/%{version}/liblto_plugin.so.0
/opt/gcc1040/libexec/gcc/%{triplet}/%{version}/liblto_plugin.so
/opt/gcc1040/libexec/gcc/%{triplet}/%{version}/install-tools
/opt/gcc1040/libexec/gcc/%{triplet}/%{version}/plugin
%{_datadir}/gcc-%{version}


%changelog

