#
# spec file for package rkhunter
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rkhunter
%define version		1.2.7
%define release		%_revrel

Summary:	Rootkit scans for rootkits, backdoors and local exploits
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://www.rootkit.nl/projects/rootkit_hunter.html
Source0:	http://downloads.rootkit.nl/%{name}-%{version}.tar.gz
Patch0:		rkhunter-1.2.7-avx-conf.patch
Patch1:		rkhunter-1.2.7-avx-annvix_curl.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	webfetch
Requires:	e2fsprogs
Requires:	binutils

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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}
%patch0 -p0 -b .avx-conf
%patch1 -p0 -b .curl

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

%files doc
%defattr(-,root,root)
%doc files/CHANGELOG files/README files/WISHLIST


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7 
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- fix group

* Wed Feb 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- re-order patches and break out the config stuff vs. the curl stuff
  and update the config to support 1.2-RELEASE

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7-2avx
- update P0 to make 1.1-RELEASE supported rather than 1.1-CURRENT

* Thu Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7-1avx
- build for Annvix to replace chkrootkit
- P0: add support for curl and Annvix

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
