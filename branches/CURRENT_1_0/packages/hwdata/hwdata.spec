%define name	hwdata
%define version	0.111
%define release	1sls

Summary:	Hardware identification and configuration data
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL/MIT
Group:		System Environment/Base
Source: 	hwdata-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch

%description
hwdata contains various hardware identification and configuration data,
such as the pci.ids database, the XFree86 Cards and MonitorsDb databases.

%prep
%setup -q

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE COPYING
%dir /usr/share/hwdata
%dir /etc/pcmcia
%config /etc/pcmcia/config
%config /usr/share/hwdata/*
# This file is screaming to be moved into /usr/share/hwdata sometime <g>
/usr/X11R6/lib/X11/Cards

%changelog
* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> 0.111-1sls
- first OpenSLS build; from Fedora
