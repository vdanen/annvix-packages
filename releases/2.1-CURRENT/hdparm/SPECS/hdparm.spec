#
# spec file for package hdparm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		hdparm
%define version 	6.6
%define release 	%_revrel

Summary:	A utility for displaying and/or setting hard disk parameters
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Kernel and hardware
URL:		http://sourceforge.net/projects/hdparm/
Source:		ftp://sunsite.unc.edu/pub/Linux/system/hardware/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Hdparm is a useful system utility for setting (E)IDE hard drive
parameters.  For example, hdparm can be used to tweak hard drive
performance and to spin down hard drives for power conservation.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
perl -pi -e "s/-O2/%{optflags}/" Makefile
make clean
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/sbin
install -D -m 0755 hdparm %{buildroot}/sbin/hdparm
install -D -m 0644 hdparm.8 %{buildroot}%{_mandir}/man8/hdparm.8
mkdir -p %{buildroot}/etc/sysconfig/env/hdparm


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/hdparm
%{_mandir}/man8/hdparm.8*
%dir /etc/sysconfig/env/hdparm

%files doc
%defattr(-,root,root)
%doc hdparm.lsm Changelog contrib/README README.acoustic


%changelog
* Fri Feb 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.6
- add /etc/sysconfig/env/hdparm and remove the sysconfig file

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.6
- 6.6
- use the real source
- use %%_sourcdir/file instead of %%{SOURCEx}
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.1
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1-2avx
- put back our hdparm-sysconfig file; accidentally replaced it
  with the less-complete Mandriva one

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1-1avx
- 6.1
- update url

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.6-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.6-2avx
- rebuild

* Wed Aug 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.6-1avx
- 5.6
- update /etc/sysconfig/harddisks with more info

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.4-6avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 5.4-5sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 5.4-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
