%define name	hwdata
%define version	0.145
%define release	1avx

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

# remove hotplug file, we don't use hotplug or support pcmcia
rm -rf %{buildroot}%{_sysconfdir}/{hotplug,pcmcia}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE COPYING
%dir /usr/share/hwdata
%config /usr/share/hwdata/*
# This file is screaming to be moved into /usr/share/hwdata sometime <g>
/usr/X11R6/lib/X11/Cards

%changelog
* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 0.145-1avx
- 0.145
- remove config files for pcmcia and hotplug

* Thu Jun 24 2004 Vincent Danen <vdanen@annvix.org> 0.111-2avx
- Annvix build

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> 0.111-1sls
- first OpenSLS build; from Fedora
