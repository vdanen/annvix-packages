#
# spec file for package slocate
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		slocate
%define version		3.1
%define release		%_revrel

Summary:	Finds files on a system via a central database
Name:		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		File tools
URL:		http://slocate.trakker.ca/
Source:		http://slocate.trakker.ca/files/%{name}-%{version}.tar.gz
Source1:	slocate.cron
Source3:	updatedb.conf
Source4:	updatedb.sh

Buildroot:	%{_buildroot}/%{name}-%{version}

Requires(pre):	rpm-helper
Requires(postun): rpm-helper


%description
Slocate is a security-enhanced version of locate. Just like locate,
slocate searches through a central database (updated regularly)
for files which match a given pattern. Slocate allows you to quickly
find files anywhere on your system.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
chmod 0644 Changelog notes README


%build
pushd src
    %make CFLAGS="%{optflags}"
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
mkdir -p %{buildroot}/var/lib/slocate

install src/slocate %{buildroot}%{_bindir}/
ln -s slocate %{buildroot}%{_bindir}/locate
install doc/slocate.1 %{buildroot}%{_mandir}/man1/
install doc/updatedb.1 %{buildroot}%{_mandir}/man1/
ln -s slocate.1.bz2 %{buildroot}%{_mandir}/man1/locate.1.bz2

install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.weekly/

install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/updatedb


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_groupadd slocate 17


%post
if [ "$1" = "0" ]; then
    [ -f /var/lib/slocate/slocate.db ] && rm -f /var/lib/slocate/slocate.db
    touch /var/lib/slocate/slocate.db
fi

%preun
if [ "$1" = "0" ]; then 
    [ -f /var/lib/slocate/slocate.db ] && rm -f /var/lib/slocate/slocate.db || true
fi

%postun
%_postun_groupdel slocate


%files
%defattr(-,root,root,755)
%attr(2755,root,slocate) %{_bindir}/*locate
%attr(-,root,slocate) %{_bindir}/updatedb
%{_mandir}/man1/*
%dir %attr(750,root,slocate) /var/lib/slocate
%config(noreplace) %{_sysconfdir}/cron.weekly/slocate.cron
%config(noreplace) %{_sysconfdir}/updatedb.conf

%files doc
%defattr(-,root,root,755)
%doc README Changelog notes


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.1
- rebuild

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1
- 3.1
- fix url/source locations
- drop all patches; fixed upstream
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.7
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.7
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-8avx
- correct the buildroot

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-7avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-6avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.7-5avx
- Annvix build

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.7-4sls
- minor spec cleanups
- assign slocate a static gid of 17 (%%_post_groupadd/%%_preun_groupdel)

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.7-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
