#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel headers
#
Summary:	Userspace support for the device-mapper
Summary(pl):	Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika
Name:		device-mapper
Version:	1.00.17
Release:	2@%{_kernel_ver_str}
License:	GPL
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/dm/%{name}.%{version}.tgz
# Source0-md5:	b74bb5fa232c77bf74f87eac2f53e1e4
Patch0:		%{name}-opt.patch
URL:		http://sources.redhat.com/dm/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libselinux-devel >= 1.10
Conflicts:	dev < 2.9.0-8
%{!?with_dist_kernel:BuildRequires:	kernel-headers}
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

%package devel
Summary:	Header files and development documentation for %{name}
Summary(pl):	Pliki nag³ówkowe i dokumentacja do %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for %{name}.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja do %{name}.

%package static
Summary:	Static devmapper library
Summary(pl):	Statyczna biblioteka devmapper
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static devmapper library.

%description static -l pl
Statyczna biblioteka devmapper.

%prep
%setup -q -n %{name}.%{version}
%patch0 -p1

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}
%configure \
	--with-user=$(id -u) \
	--with-group=$(id -g) \
	--with-interface=ioctl \
	--with-kernel-version=%{_kernel_ver}
%{__make}

ar cru libdevmapper.a lib/ioctl/*.o lib/*.o
ranlib libdevmapper.a

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/%{_lib},%{_libdir}/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

SONAME=$(basename $(ls -1 $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*))
ln -sf /%{_lib}/${SONAME} $RPM_BUILD_ROOT%{_libdir}/libdevmapper.so
mv -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.* $RPM_BUILD_ROOT/%{_lib}
cp -f scripts/* $RPM_BUILD_ROOT%{_libdir}/%{name}

install libdevmapper.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INTRO INSTALL README
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /%{_lib}/lib*.so.*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
