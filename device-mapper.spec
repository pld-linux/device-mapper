Summary:	Userspace support for the device-mapper
Name:		device-mapper
Version:	0.96.08
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.sistina.com/pub/LVM2/device-mapper/%{name}.%{version}.tgz
Patch0:		%{name}-install.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
The goal of this driver is to support volume management.
The driver enables the definition of new block devices composed of
ranges of sectors of existing devices.  This can be used to define
disk partitions - or logical volumes.  This light-weight kernel
component can support user-space tools for logical volume management.

%prep
%setup -q -n %{name}.%{version}
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INTRO INSTALL README
