#
# spec file for package pax
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		pax
%define version		3.4
%define release		%_revrel

Summary:	POSIX File System Archiver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		ftp://ftp.suse.com/pub/people/kukuk/pax/
Source:		ftp://ftp.suse.com/pub/people/kukuk/pax/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	common-licenses

%description
'pax' is the POSIX standard archive tool.  It supports the two most
common forms of standard Unix archive (backup) files - CPIO and TAR.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS NEWS README THANKS
%{_bindir}/pax
%{_mandir}/man1/*


%changelog
* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.4-1avx
- 3.4

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-9avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-8avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0-7avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.0-6sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 3.0-5sls
- OpenSLS build
- tidy spec

* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.0-4mdk
- rebuild
- rm -rf %{buildroot} in the beginning of %%install

* Fri Dec 27 2002 Stew Benedict <sbenedict@mandrakesoft.com> 3.0-3mdk
- rebuild for new glibc/rpm

* Mon Jul 22 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 3.0-2mdk
- use %%configure2_5x and %%makeinstall_std
- fix License: s/BSD/GPL/
- Requires: common-licenses
- add %%doc documentation (AUTHORS, NEWS, README, THANKS)

* Wed Apr 10 2002 Stew Benedict <sbenedict@mandrakesoft.com> 3.0-1mdk
- new "unbroken" version, courtesy of Thorsten Kukuk <kukuk@suse.de>

* Tue Feb 19 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.5-3mdk
- rebuild to fix the "expected size" not matching the "actual size"

* Wed Aug 22 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.5-2mdk
- bzip2 sources & patches

* Sun Aug  5 2001 Stew Benedict <sbenedict@mandrakesoft.com> 1.5-1mdk
- borrowed RedHat SRPM - used by lsb-testsuite
