%define name	pax
%define version	3.0
%define release	8avx

Summary:	POSIX File System Archiver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving/Backup
URL:		ftp://ftp.suse.com/pub/people/kukuk/pax/
Source:		ftp://ftp.suse.com/pub/people/kukuk/pax/%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root

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
* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 3.0-8avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.org> 3.0-7avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.0-6sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 3.0-5sls
- OpenSLS build
- tidy spec

* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.0-4mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT in the beginning of %%install

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
