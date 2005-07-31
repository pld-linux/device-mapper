#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
%bcond_without	initrd		# don't build initrd version
%bcond_with	glibc		# build glibc-based initrd version
#
%ifnarch %{ix86}
%define with_glibc 1
%endif
Summary:	Userspace support for the device-mapper
Summary(pl):	Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika
Name:		device-mapper
Version:	1.01.03
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}.tgz
# Source0-md5:	10469034e2f1f1483fd3d80fb3883af2
Patch0:		%{name}-stack.patch
URL:		http://sources.redhat.com/dm/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.10}
%{?with_selinux:Requires:	libselinux >= 1.10}
%if %{with initrd}
%{?with_glibc:BuildRequires:	glibc-static}
%{?!with_glibc:BuildRequires:	uClibc-static}
%endif
Conflicts:	dev < 2.9.0-8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The goal of this driver is to support volume management.
The driver enables the definition of new block devices composed of
ranges of sectors of existing devices. This can be used to define
disk partitions - or logical volumes. This light-weight kernel
component can support user-space tools for logical volume management.

%description -l pl
Celem tego sterownika jest obs³uga zarz±dzania wolumenami.
Sterownik w³±cza definiowanie nowych urz±dzeñ blokowych z³o¿onych z
przedzia³ów sektorów na istniej±cych urz±dzeniach. Mo¿e to byæ
wykorzystane do definiowania partycji na dysku lub logicznych
wolumenów. Ten lekki sk³adnik j±dra mo¿e wspieraæ dzia³aj±ce w
przestrzeni u¿ytkownika narzêdzia do zarz±dzania logicznymi
wolumenami.

%package initrd
Summary:	Userspace support for the device-mapper - static dmsetup for initrd
Summary(pl):	Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika - statyczne dmsetup dla initrd
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description initrd
Userspace support for the device-mapper - static dmsetup binary for initrd.

%description initrd -l pl
Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika - statyczna wersja
dmsetup dla initrd.

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

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}

%if %{with initrd}
%configure \
	--disable-selinux \
	--with-optimisation="%{rpmcflags}" \
	--with-user=%(id -u) \
	--with-group=%(id -g) \
	--with-interface=ioctl \
	--enable-static_link \
	%{?!with_glibc:CC="%{_target_cpu}-uclibc-gcc"}
%{__make}

cp -a dmsetup/dmsetup.static initrd-dmsetup
%{__make} clean
%endif

%configure \
	--%{?with_selinux:en}%{!?with_selinux:dis}able-selinux \
	--with-optimisation="%{rpmcflags}" \
	--with-user=%(id -u) \
	--with-group=%(id -g) \
	--with-interface=ioctl
%{__make}

ar cru libdevmapper.a lib/ioctl/*.o lib/*.o
ranlib libdevmapper.a

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_lib},%{_libdir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

SONAME=$(basename $(ls -1 $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*))
ln -sf /%{_lib}/${SONAME} $RPM_BUILD_ROOT%{_libdir}/libdevmapper.so
mv -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.* $RPM_BUILD_ROOT/%{_lib}
install scripts/* $RPM_BUILD_ROOT/%{_libdir}/%{name}

install libdevmapper.a $RPM_BUILD_ROOT%{_libdir}
%{?with_initrd:install initrd-dmsetup $RPM_BUILD_ROOT%{_sbindir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INTRO INSTALL README scripts/*
%attr(755,root,root) %{_sbindir}/dmsetup
%attr(755,root,root) /%{_lib}/lib*.so.*.*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdevmapper.so
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files scripts
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*

%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-dmsetup
