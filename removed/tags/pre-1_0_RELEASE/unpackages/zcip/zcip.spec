%define name	zcip
%define version	4
%define release	5sls

%define srcver	4

Summary:	Ad-hoc link-local IP autoconfiguration
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Configuration/Networking
URL:		http://zeroconf.sourceforge.net/
Source0:	%{name}-%{srcver}.tar.bz2
Patch0:		zcip-4-alias.patch.bz2
Patch1:		zcip-4-gcc3.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	net-devel = 1.0.2a, libpcap-devel, glibc-static-devel

%description
This is an implementation of the ad-hoc link-local IP autoconfiguration
algorithm described in the IETF Draft "Dynamic Configuration of IPv4
link-local addresses".

%prep
%setup -n %name-%srcver
%patch0 -p1 -b .alias
%patch1 -p1 -b .gcc3

%build
%make CFLAGS="$RPM_OPT_FLAGS -DSTORAGE_DIR=\\\"%{_localstatedir}/zcip\\\""

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/sbin %{buildroot}%{_mandir}/man8
install zcip %{buildroot}/sbin
install -m 644 zcip.8 %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_localstatedir}/zcip

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README draft-ietf-zeroconf-ipv4-linklocal-07.txt Changelog Copyright TODO
/sbin/*
%{_mandir}/man8/*
%{_localstatedir}/zcip

%changelog
* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4-5sls
- minor spec cleanups
- remove %%prefix

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 4-4sls
- OpenSLS build
- tidy spec

* Wed Aug 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 4-3mdk
- rebuild

* Mon Nov 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 4-2mdk
- real version 4

* Tue Oct  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 4-1mdk
- new release

* Sun Oct  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 4-0.rc1.2mdk
- added alias support

* Mon Jul  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 4-0.rc1.1mdk
- 4rc1

* Mon Jul  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 3-1mdk
- Initial Mandrake Linux packaging

# end of file
