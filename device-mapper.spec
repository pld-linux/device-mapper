Summary:	Userspace support for the device-mapper
Name:		device-mapper
Version:	0.96.08
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.sistina.com/pub/LVM2/device-mapper/%{name}.%{version}.tgz
Patch0:		%{name}-install.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The goal of this driver is to support volume management.
The driver enables the definition of new block devices composed of
ranges of sectors of existing devices.  This can be used to define
disk partitions - or logical volumes.  This light-weight kernel
component can support user-space tools for logical volume management.

%package devel
Summary:	Header files and development documentation for %{name}
Summary(pl):	Pliki nag³ówkowe i dokumentacja do %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for %{name}.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja do %{name}.

%prep
%setup -q -n %{name}.%{version}
%patch0 -p1

%build
%{__aclocal}                                                                    
%{__autoconf}                                                                   
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib

%{__make} install DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.* $RPM_BUILD_ROOT/lib/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INTRO INSTALL README
%attr(755, root, root) %{_sbindir}/*
%attr(755, root, root) /lib/lib*.so.*.*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%attr(755, root, root) %{_libdir}/lib*.so
%{_includedir}/*.h
