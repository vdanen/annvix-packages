#
# spec file for package tmpwatch
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		tmpwatch
%define version		2.9.10
%define release		%_revrel

# CVSROOT=':ext:user@devserv.devel.redhat.com:/home/devel/CVS'
Summary:	A utility for removing files based on when they were last accessed
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		ftp://ftp.redhat.com/pub/redhat/linux/rawhide/SRPMS/SRPMS/
Source0:	%{name}-%{version}.tar.gz
Source1:	tmpwatch.cron

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	psmisc

%description
The tmpwatch utility recursively searches through specified
directories and removes files which have not been accessed in a
specified period of time.  Tmpwatch is normally used to clean up
directories which are used for temporarily holding files (for example,
/tmp).  Tmpwatch ignores symlinks, won't switch filesystems and only
removes empty directories and regular files.


%prep
%setup -q


%build
make RPM_OPT_FLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall ROOT=%{buildroot} MANDIR=%{_mandir} SBINDIR=%{_sbindir}

mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
install -m 0755 %{_sourcedir}/tmpwatch.cron %{buildroot}%{_sysconfdir}/cron.daily/tmpwatch


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/tmpwatch
%{_mandir}/man8/tmpwatch.8*
%attr(755,root,root) %{_sysconfdir}/cron.daily/tmpwatch


%changelog
* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.9.7
- update the cron script; make sure it only checks directories that exist

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9.7
- 2.9.7
- cron script isn't a config file

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9.6
- 2.9.6
- S1: make the cron script a source instead of echo'd in the spec
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0-6avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0-5avx
- bootstrap build

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.9.0-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.9.0-3sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.9.0-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
