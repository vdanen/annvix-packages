#
# spec file for package psmisc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		psmisc
%define version		22.2
%define release		%_revrel

Summary:	Utilities for managing processes on your system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://psmisc.sourceforge.net
Source:		http://download.sourceforge.net/psmisc/psmisc-%{version}.tar.bz2
Patch1:		psmisc-21.9-libsafe.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs
of processes that are using specified files or filesystems.


%prep
%setup -q 
%patch1 -p1


%build
%configure


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
mkdir %{buildroot}/sbin
mv %{buildroot}%{_bindir}/fuser %{buildroot}/sbin/

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
/sbin/fuser
%{_bindir}/killall
%{_bindir}/pstree*
%{_bindir}/oldfuser
%{_mandir}/man1/fuser.1*
%{_mandir}/man1/killall.1*
%{_mandir}/man1/pstree.1*


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 22.2
- spec cleanups
- remove locales

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 22.2
- 22.2
- removed libtermcap-devel as buildrequires
- updated P1
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 21.3
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 21.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 21.3-7avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 21.3-6avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 21.3-5avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 21.3-4sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 21.3-3sls
- OpenSLS build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
