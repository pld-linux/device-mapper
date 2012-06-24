#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
%bcond_without	initrd		# don't build initrd version
#
Summary:	Userspace support for the device-mapper
Summary(pl):	Wsparcie dla mapowania urz�dze� w przestrzeni u�ytkownika
Name:		device-mapper
Version:	1.01.03
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}.tgz
# Source0-md5:	10469034e2f1f1483fd3d80fb3883af2
Patch0:		%{name}-stack.patch
# http://www.redhat.com/archives/dm-devel/2005-March/msg00022.html
Patch1:		%{name}-disable_dynamic_link.patch
Patch2:		%{name}-klibc.patch
URL:		http://sources.redhat.com/dm/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.10}
%{?with_selinux:Requires:	libselinux >= 1.10}
%{?with_initrd:BuildRequires:	klibc}
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
Celem tego sterownika jest obs�uga zarz�dzania wolumenami.
Sterownik w��cza definiowanie nowych urz�dze� blokowych z�o�onych z
przedzia��w sektor�w na istniej�cych urz�dzeniach. Mo�e to by�
wykorzystane do definiowania partycji na dysku lub logicznych
wolumen�w. Ten lekki sk�adnik j�dra mo�e wspiera� dzia�aj�ce w
przestrzeni u�ytkownika narz�dzia do zarz�dzania logicznymi
wolumenami.

%package initrd
Summary:	Userspace support for the device-mapper - static dmsetup for initrd
Summary(pl):	Wsparcie dla mapowania urz�dze� w przestrzeni u�ytkownika - statyczne dmsetup dla initrd
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description initrd
Userspace support for the device-mapper - static dmsetup binary for initrd.

%description initrd -l pl
Wsparcie dla mapowania urz�dze� w przestrzeni u�ytkownika - statyczna wersja
dmsetup dla initrd.

%package devel
Summary:	Header files and development documentation for %{name}
Summary(pl):	Pliki nag��wkowe i dokumentacja do %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and development documentation for %{name}.

%description devel -l pl
Pliki nag��wkowe i dokumentacja do %{name}.

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
Summary(pl):	Statyczna biblioteka devmapper i jej pliki nag��wkowe dla aplikacji initrd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	klibc

%description initrd-devel
Static devmapper library and its header files for initrd applications linked
with klibc.

%description initrd-devel -l pl
Statyczna biblioteka devmapper oraz jej pliki nag��wkowe dla aplikacji
u�ywanych w initrd, zlinkowana z klibc.

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
	--disable-dynamic_link \
	--enable-klibc \
	CC="klcc"
%{__make}

cp -a dmsetup/dmsetup.static initrd-dmsetup
cp -a lib/ioctl/libdevmapper.a initrd-libdevmapper.a
%{__make} clean
%endif

%configure \
	--%{?with_selinux:en}%{!?with_selinux:dis}able-selinux \
	--with-optimisation="%{rpmcflags}" \
	--with-user=%(id -u) \
	--with-group=%(id -g) \
	--with-interface=ioctl \
	--disable-klibc
%{__make}

ar cru libdevmapper.a lib/ioctl/*.o lib/*.o
ranlib libdevmapper.a

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_lib},%{_libdir}/%{name},/usr/{%{_lib},include}/klibc}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

SONAME=$(basename $(ls -1 $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*))
ln -sf /%{_lib}/${SONAME} $RPM_BUILD_ROOT%{_libdir}/libdevmapper.so
mv -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.* $RPM_BUILD_ROOT/%{_lib}
install scripts/* $RPM_BUILD_ROOT/%{_libdir}/%{name}

install libdevmapper.a $RPM_BUILD_ROOT%{_libdir}
%{?with_initrd:install initrd-dmsetup $RPM_BUILD_ROOT%{_sbindir}}
%{?with_initrd:install initrd-libdevmapper.a $RPM_BUILD_ROOT/usr/%{_lib}/klibc/libdevmapper.a}
%{?with_initrd:install include/libdevmapper.h $RPM_BUILD_ROOT/usr/include/klibc}

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

%files initrd-devel
%defattr(644,root,root,755)
/usr/%{_lib}/klibc/libdevmapper.a
/usr/include/klibc/libdevmapper.h
