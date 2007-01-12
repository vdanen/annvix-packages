#
# spec file for package aide
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		aide
%define version		0.13.1
%define release		%_revrel

Summary:	Advanced Intrusion Detection Environment
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://sourceforge.net/projects/aide
Source0:	http://prdownloads.sourceforge.net/aide/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/aide/%{name}-%{version}.tar.gz.asc
Source2:	aide.conf
Source3:	aidecheck
Source4:	aideupdate
Source5:	aideinit
Source6:	98_aide.afterboot

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex
BuildRequires:	glibc-devel
BuildRequires:	glibc-static-devel
BuildRequires:	libmhash-devel
BuildRequires:	zlib-devel
BuildRequires:	bison

Requires:	afterboot
Requires:	gnupg

%description
AIDE (Advanced Intrusion Detection Environment) is a free alternative
to Tripwire.  It is a file system integrity monitoring tool.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure \
    --with-config_file=%{_sysconfdir}/aide.conf \
    --with-zlib \
    --with-mhash \
    --enable-mhash \
    --with-syslog_facility=LOG_LOCAL1

perl -pi -e 's|/etc/aide.db|/var/lib/aide/aide.db|g' config.h

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make prefix=%{buildroot}%{_prefix} \
    bindir=%{buildroot}%{_sbindir} \
    mandir=%{buildroot}%{_mandir} \
    install-strip

mkdir -p %{buildroot}{/var/lib/aide/reports,%{_sysconfdir}/cron.daily}

install -m 0600 %{_sourcedir}/aide.conf %{buildroot}%{_sysconfdir}/aide.conf
install -m 0700 %{_sourcedir}/aidecheck %{buildroot}%{_sbindir}/aidecheck
install -m 0700 %{_sourcedir}/aideupdate %{buildroot}%{_sbindir}/aideupdate
install -m 0700 %{_sourcedir}/aideinit %{buildroot}%{_sbindir}/aideinit
ln -sf ../..%{_sbindir}/aidecheck %{buildroot}%{_sysconfdir}/cron.daily/aide

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/98_aide.afterboot %{buildroot}%{_datadir}/afterboot/98_aide


%post
%_mkafterboot


%postun
%_mkafterboot


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0700,root,root) %{_sbindir}/aide
%attr(0700,root,root) %{_sbindir}/aidecheck
%attr(0700,root,root) %{_sbindir}/aideinit
%attr(0700,root,root) %{_sbindir}/aideupdate
%{_mandir}/man1/aide.1*
%{_mandir}/man5/aide.conf.5*
%dir %attr(0700,root,root) /var/lib/aide
%dir %attr(0700,root,root) /var/lib/aide/reports
%attr(0700,root,root) %{_sysconfdir}/cron.daily/aide
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/aide.conf
%{_datadir}/afterboot/98_aide

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README doc/aide.conf.in


%changelog
* Fri Jan 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.13.1
- update aideinit and aidecheck to work around the gpg issue (bug #45);
  this is a bit of a hack but since gpg is segfaulting on receiving typed
  input we can work around the issue this way while we figure out the
  real problem

* Mon Jan 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.13.1
- 0.13.1

* Fri Dec 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.13
- 0.13

* Tue Nov 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.12
- 0.12

* Tue Jul 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- spec cleanups

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- rebuild against new mhash

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- add -doc subpackage
- rebuild with gcc4
- s|/etc|%%{_sysconfdir}|g

* Sat Feb 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- 0.11
- Requires: gnupg

* Mon Jan 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11-rc3
- 0.11-rc3
- drop P0, P1, P3: all merged upstream
- aideinit, aideupdate: pass '-u aide@[host]' to specify the gpg key to use

* Sat Jan 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11-CVS-20060128
- use CVS snapshot as it contains some minor fixes
- fix perms on /etc/aide.conf (0600, not 0700)
- add afterboot snippet
- change wrappers to enforce the use of gpg
- add aideinit script to generate the database and a gpg key
- store a copy of the report in /var/lib/aide/reports
- add aidecheck and made /etc/cron.daily/aide a symlink to it

* Fri Jan 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11-rc2
- first Annvix package; labelled 0.11 but contains 0.11-rc2
- P0: pretty the report output a little bit
- set syslog facility to LOCAL1
- include an aideupdate script to facilitate the updating of the database
  and a cron script to check it (optionally using gpg for verification)
- P1: make --help look nicer

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
