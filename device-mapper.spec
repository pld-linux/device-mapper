#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel headers
#
Summary:	Userspace support for the device-mapper
Summary(pl):	Wsparcie dla mapowania urz±dzeñ w przestrzeni u¿ytkownika
Name:		device-mapper
Version:	1.00.07
Release:	0.1@%{_kernel_ver_str}
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.sistina.com/pub/LVM2/device-mapper/%{name}.%{version}.tgz
# Source0-md5:	44920cd973a6abc79109af9bff9d8af6
Patch0:		%{name}-install.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-errno.patch
BuildRequires:	autoconf
BuildRequires:	automake
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
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.sub autoconf
%{__aclocal}
%{__autoconf}
%configure \
	--with-interface=ioctl \
	--with-kernel-dir=%{_kernelsrcdir} \
	--with-kernel-version=%{_kernel_ver}
%{__make}

ar cru libdevmapper.a lib/ioctl/*.o lib/*.o
ranlib libdevmapper.a

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.* $RPM_BUILD_ROOT/lib

install libdevmapper.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INTRO INSTALL README
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /lib/lib*.so.*.*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
