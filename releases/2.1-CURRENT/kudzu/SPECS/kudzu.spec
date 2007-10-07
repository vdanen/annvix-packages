#
# spec file for package kudzu
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		kudzu
%define version		1.2.71
%define release		%_revrel

Summary:	The Red Hat Linux hardware probing tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Applications/System
URL:		http://fedora.redhat.com/projects/additional-projects/kudzu/
Source0:	kudzu-%{version}.tar.gz
Source1:	kudzu-avx.init
Patch0:		kudzu-1.1.95-avx-python2.patch
Patch1:		kudzu-1.2.60-avx-force_mv.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	pciutils-devel >= 2.2.3
BuildRequires:	python-devel
BuildRequires:	python
BuildRequires:	newt-devel

Requires(post):	runit
Requires(post):	rpm-helper
Requires(preun): runit
Requires(preun): rpm-helper
Requires:	pam >= 0.74-17
Requires:	hwdata
Requires:	python-base >= %{py_ver}
Requires:	module-init-tools
Requires:	libnewt

%description
Kudzu is a hardware probing tool run at system boot time to determine
what hardware has been added or removed from the system.


%package devel
Summary:	Development files needed for hardware probing using kudzu
Group:		Development/Libraries
Requires:	pciutils-devel

%description devel
The kudzu-devel package contains the libkudzu library, which is used
for hardware probing and configuration.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .python2
%patch1 -p1 -b .force_mv

%build
ln -s `pwd` kudzu

make RPM_OPT_FLAGS="%{optflags} -I." all kudzu


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install install-program DESTDIR=%{buildroot} libdir=%{buildroot}%{_libdir}
install -m 0755 fix-mouse-psaux %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_initrddir}
install -m 0750 %{_sourcedir}/kudzu-avx.init %{buildroot}%{_initrddir}/kudzu
rm -rf %{buildroot}%{_sysconfdir}/rc.d/init.d

rm -f %{buildroot}%{_sysconfdir}/sysconfig/kudzu
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/env/kudzu
echo "no" >%{buildroot}%{_sysconfdir}/sysconfig/env/kudzu/SAFE

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_service kudzu


%preun
%_preun_service kudzu


%files -f %{name}.lang
%defattr(-,root,root)
/sbin/kudzu
%{_sbindir}/kudzu
%{_sbindir}/fix-mouse-psaux
%{_mandir}/man8/*
%dir %{_sysconfdir}/sysconfig/env/kudzu
%config(noreplace) %attr(0640,root,admin) %dir %{_sysconfdir}/sysconfig/env/kudzu/SAFE
%attr(0750,root,admin) %{_initrddir}/kudzu
%{_libdir}/python*/site-packages/*

%Files devel
%defattr(-,root,root)
%{_libdir}/libkudzu.a
%{_libdir}/libkudzu_loader.a
%{_includedir}/kudzu

%files doc
%defattr(-,root,root)
%doc README hwconf-description


%changelog
* Sun Oct 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.71
- requires module-init-tools, not modutils

* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.71
- 1.2.71
- rebuild against new newt
- fix requires

* Fri May 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.60
- rebuild againt new python

* Sun Nov 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.60
- kudzu no longer has a -z option so fix initscript

* Sat Nov 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.60
- 1.2.60
- use "kudzu -q" in initscript
- P1: force the use of "mv -f"
- include the envdir file kudzu/SAFE

* Thu Nov 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.34.3
- use getenvopt() in the initscript

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.34.3
- add the order keyword to the initscript
- requires runit

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.34.3
- S1: our own custom initscript
- remove dependenicies on initscripts and chkconfig
- permissions on the initscript are now 0750 and owned root:admin

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.34.3
- remove locales

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.34.3
- fix python-base requires (use >= rather than = since %%py_ver in this
  case resolves to "2.4")

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.34.3
- 1.2.34.3
- add -doc subpackage
- rebuild with gcc4
- the initscript is not a config file
- remove invalid LC_MESSAGES directories
- set an explicit versioned requires on python-base

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.95
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1.95
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.95-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1.95-2avx
- rebuild

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> - 1.1.95-1avx
- 1.1.111
- don't build with dietlibc anymore

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> - 1.1.95-1avx
- 1.1.95
- update url
- P1: we don't rename python to python2 so fix Makefile

* Wed Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> - 1.1.51-4avx
- require packages not files
- Annvix build

* Thu Mar 18 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-3sls
- fix deps for amd64

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-2sls
- Requires: s/newt/libnewt0.51/

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-1sls
- first OpenSLS build; from Fedora

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
