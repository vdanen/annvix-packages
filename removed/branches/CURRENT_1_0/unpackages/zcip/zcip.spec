%define srcver 4

Summary: Ad-hoc link-local IP autoconfiguration
Name: zcip
Version: 4
Release: 3mdk
Source0: %{name}-%{srcver}.tar.bz2
Patch0: zcip-4-alias.patch.bz2
Patch1: zcip-4-gcc3.patch.bz2
License: MIT
Group: System/Configuration/Networking
URL: http://zeroconf.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: net-devel = 1.0.2a, libpcap-devel, glibc-static-devel
Prefix: %{_prefix}

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
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/sbin %{buildroot}%{_mandir}/man8
install zcip %{buildroot}/sbin
install -m 644 zcip.8 %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_localstatedir}/zcip

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README draft-ietf-zeroconf-ipv4-linklocal-07.txt Changelog Copyright TODO
/sbin/*
%{_mandir}/man8/*
%{_localstatedir}/zcip

%changelog
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
