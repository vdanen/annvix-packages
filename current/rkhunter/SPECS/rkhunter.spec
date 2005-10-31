#
# spec file for package rkhunter
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		rkhunter
%define version		1.2.7
%define release		1avx

Summary:	Rootkit scans for rootkits, backdoors and local exploits
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Other
URL:		http://www.rootkit.nl/projects/rootkit_hunter.html
Source0:	http://downloads.rootkit.nl/%{name}-%{version}.tar.gz
Patch0:		rkhunter-1.2.7-avx-annvix_curl.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	webfetch e2fsprogs binutils

%description
Rootkit scanner is scanning tool to ensure you for about 99.9%% you're
clean of nasty tools. This tool scans for rootkits, backdoors and local
exploits by running tests like:
	- MD5 hash compare
	- Look for default files used by rootkits
	- Wrong file permissions for binaries
	- Look for suspected strings in LKM and KLD modules
	- Look for hidden files
	- Optional scan within plaintext and binary files


%prep
%setup -q -n %{name}
%patch0 -p0 -b .avx

chmod a+r files/{README,WISHLIST,CHANGELOG}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

./installer.sh --installdir %{buildroot}

rm -rf %{buildroot}%{_datadir}/%{name}/doc
mkdir -p %{buildroot}%{_sbindir} %{buildroot}/var/lib/%{name}/db %{buildroot}/var/lib/%{name}/tmp
install -m 0750 files/rkhunter %{buildroot}%{_sbindir}/
install -m 0640 files/rkhunter.conf %{buildroot}%{_sysconfdir}
echo "INSTALLDIR=/" >> %{buildroot}%{_sysconfdir}/rkhunter.conf
cp -p files/*.dat %{buildroot}/var/lib/%{name}/db

chmod -R o-rx %{buildroot}{/var/lib/%{name},/lib/%{name}}

# remove unwanted files
rm -rf %{buildroot}/lib/%{name}/docs


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc files/CHANGELOG files/README files/WISHLIST
%config(noreplace) %{_sysconfdir}/rkhunter.conf
%{_sbindir}/*
%dir /lib/%{name}
%dir /lib/%{name}/db
%dir /lib/%{name}/scripts
%dir /lib/%{name}/tmp
/lib/%{name}/db/*
/lib/%{name}/scripts/*
%dir /var/lib/%{name}
%dir /var/lib/%{name}/db
%dir %attr(0700,root,root) /var/lib/%{name}/tmp
/var/lib/%{name}/db/*


%changelog
* Thu Sep 25 2005 Vincent Danen <vdanen@annvix.org> 1.2.7-1avx
- build for Annvix to replace chkrootkit
- P0: add support for curl and Annvix

* Sat Aug  6 2005 Gaetan Lehmann <glehmann@n4.mandriva.com> 1.2.7-1mdk
- complete URL
- use mkrel
- fix config file (reported on expert mailing list)

* Wed May 25 2005 Lenny Cartier <lenny@mandriva.com> 1.2.7-1mdk
- 1.2.7

* Wed May 11 2005 Lenny Cartier <lenny@mandriva.com> 1.2.6-1mdk
- 1.2.6

* Fri Feb 11 2005 Mandrakelinux Team <http://www.mandrakeexpert.com> 1.2.0-1mdk
- New release 1.2.0

* Tue Feb 08 2005 Mandrakelinux Team <http://www.mandrakeexpert.com> 1.1.9-1mdk
- New release 1.1.9

* Mon Aug 23 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.6-2mdk
- fixed update script path (Mario R. Pizzolanti)

* Wed Aug 18 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.6-1mdk
- added missing requires
- New release 1.1.6

* Wed Jun 23 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.1.1-1mdk
- New release 1.1.1

* Fri May 28 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.0.9-1mdk
- initial package

# end of file
