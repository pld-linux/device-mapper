# TODO
# - add fix to drop BuildConflicts:	device-mapper-initrd-devel
#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
%bcond_without	initrd		# don't build initrd version
#
Summary:	Userspace support for the device-mapper
Summary(pl):	Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika
Name:		device-mapper
Version:	1.02.08
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}.tgz
# Source0-md5:	e1821d2367b4e26f7b364bdae2385153
# http://www.redhat.com/archives/dm-devel/2005-March/msg00022.html
Patch0:		%{name}-disable_dynamic_link.patch
Patch1:		%{name}-klibc.patch
Patch2:		%{name}-getopt.patch
Patch3:		%{name}-ac.patch
URL:		http://sources.redhat.com/dm/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_initrd:BuildRequires:	klibc-static}
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.10}
%{?with_initrd:BuildRequires:	uClibc-static >= 0.9.26}
# /usr/include/klibc/libdevmapper.h is included first before currently built version with klcc
BuildConflicts:	device-mapper-initrd-devel < 1.02.07
%{?with_selinux:Requires:	libselinux >= 1.10}
Conflicts:	dev < 2.9.0-8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	configure_cache
%define		_sbindir	/sbin

%description
The goal of this driver is to support volume management. The driver
enables the definition of new block devices composed of ranges of
sectors of existing devices. This can be used to define disk
partitions - or logical volumes. This light-weight kernel component
can support user-space tools for logical volume management.

%description -l pl
Celem tego sterownika jest obs³uga zarz±dzania wolumenami. Sterownik
w³±cza definiowanie nowych urz±dzeñ blokowych z³o¿onych z przedzia³ów
sektorów na istniej±cych urz±dzeniach. Mo¿e to byæ wykorzystane do
definiowania partycji na dysku lub logicznych wolumenów. Ten lekki
sk³adnik j±dra mo¿e wspieraæ dzia³aj±ce w przestrzeni u¿ytkownika
narzêdzia do zarz±dzania logicznymi wolumenami.

%package initrd
Summary:	Userspace support for the device-mapper - static dmsetup for initrd
Summary(pl):	Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika - statyczne dmsetup dla initrd
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description initrd
Userspace support for the device-mapper - static dmsetup binary for
initrd.

%description initrd -l pl
Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika - statyczna
wersja dmsetup dla initrd.

%package devel
Summary:	Header files and development documentation for %{name}
Summary(pl):	Pliki nag³ówkowe i dokumentacja do %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and development documentation for %{name}.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja do %{name}.

%package static
Summary:	Static devmapper library
Summary(pl):	Statyczna biblioteka devmapper
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static devmapper library.

%description static -l pl
Statyczna biblioteka devmapper.

%package initrd-devel
Summary:	Static devmapper library and header files for initrd applications
Summary(pl):	Statyczna biblioteka devmapper i jej pliki nag³ówkowe dla aplikacji initrd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	klibc

%description initrd-devel
Static devmapper library and its header files for initrd applications
linked with klibc.

%description initrd-devel -l pl
Statyczna, zlinkowana z klibc biblioteka devmapper oraz jej pliki
nag³ówkowe dla aplikacji u¿ywanych w initrd.

%package scripts
Summary:	Additional scripts
Summary(pl):	Dodatkowe skrypty
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	util-linux

%description scripts
Additional scripts.

%description scripts -l pl
Dodatkowe skrypty.

%prep
%setup -q -n %{name}.%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# klcc puts its own -I before any options, so klibc's <linux/*>
# overrides include/linux/*, requiring very fresh kernel headers
sed -i -e 's,<linux/dm-ioctl.h>,"../../kernel/ioctl/dm-ioctl.h",' lib/ioctl/libdm-iface.c

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}

%if %{with initrd}
# kcc
%configure \
	CC="klcc -static" \
	CLDFLAGS="%{rpmldflags}" \
	--disable-selinux \
	--disable-dynamic_link \
	--enable-static_link \
	--with-optimisation="%{rpmcflags}" \
	--with-user=%(id -u) \
	--with-group=%(id -g) \
	--with-interface=ioctl \
	--disable-nls
sed -i -e 's#rpl_malloc#malloc#g' include/configure.h
%{__make}

cp -a dmsetup/dmsetup.static initrd-dmsetup
cp -a lib/ioctl/libdevmapper.a initrd-libdevmapper-klibc.a
%{__make} clean

# uclibc (for lvm2)
%configure \
	CC="%{_target_cpu}-uclibc-gcc" \
	CLDFLAGS="%{rpmldflags}" \
	--disable-selinux \
	--disable-dynamic_link \
	--with-optimisation="-Os" \
	--with-interface=ioctl \
	--disable-nls
sed -i -e 's#rpl_malloc#malloc#g' include/configure.h
%{__make}

cp -a lib/ioctl/libdevmapper.a initrd-libdevmapper-uclibc.a
%{__make} clean
%endif

%configure \
	CLDFLAGS="%{rpmldflags}" \
	--%{?with_selinux:en}%{!?with_selinux:dis}able-selinux \
	--with-optimisation="%{rpmcflags}" \
	--with-user=%(id -u) \
	--with-group=%(id -g) \
	--with-interface=ioctl \
	--enable-dmeventd \
	--disable-klibc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_lib},%{_libdir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

SONAME=$(cd $RPM_BUILD_ROOT%{_libdir}; echo libdevmapper.so.*.*)
ln -sf /%{_lib}/${SONAME} $RPM_BUILD_ROOT%{_libdir}/libdevmapper.so
SONAME=$(cd $RPM_BUILD_ROOT%{_libdir}; echo libdevmapper-event.so.*.*)
ln -sf /%{_lib}/${SONAME} $RPM_BUILD_ROOT%{_libdir}/libdevmapper-event.so
mv -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.* $RPM_BUILD_ROOT/%{_lib}
install scripts/* $RPM_BUILD_ROOT%{_libdir}/%{name}

install lib/ioctl/libdevmapper.a $RPM_BUILD_ROOT%{_libdir}
install dmeventd/libdevmapper-event.a $RPM_BUILD_ROOT%{_libdir}

%if %{with initrd}
install -d $RPM_BUILD_ROOT/usr/{{%{_lib},include}/klibc,%{_target_cpu}-linux-uclibc/usr/{lib,include}}
install initrd-dmsetup $RPM_BUILD_ROOT%{_sbindir}
install initrd-libdevmapper-klibc.a $RPM_BUILD_ROOT/usr/%{_lib}/klibc/libdevmapper.a
install initrd-libdevmapper-uclibc.a $RPM_BUILD_ROOT/usr/%{_target_cpu}-linux-uclibc/usr/lib/libdevmapper.a
install include/libdevmapper.h $RPM_BUILD_ROOT/usr/include/klibc
install include/libdevmapper.h $RPM_BUILD_ROOT/usr/%{_target_cpu}-linux-uclibc/usr/include
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INTRO INSTALL README scripts/*
%attr(755,root,root) %{_sbindir}/dmsetup
%attr(755,root,root) /%{_lib}/libdevmapper.so.*.*
%attr(755,root,root) /%{_lib}/libdevmapper-event.so.*.*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdevmapper.so
%attr(755,root,root) %{_libdir}/libdevmapper-event.so
%{_includedir}/libdevmapper*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libdevmapper.a
%{_libdir}/libdevmapper-event.a

%files scripts
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-dmsetup

%files initrd-devel
%defattr(644,root,root,755)
%{_prefix}/%{_lib}/klibc/libdevmapper.a
%{_prefix}/%{_target_cpu}-linux-uclibc/usr/lib/libdevmapper.a
%{_includedir}/klibc/libdevmapper.h
%{_prefix}/%{_target_cpu}-linux-uclibc/usr/include/libdevmapper.h
%endif
