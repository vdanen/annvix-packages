#
# spec file for package ethtool
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ethtool
%define version		3
%define release		%_revrel

Summary:	Ethernet settings tool for network cards
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://sourceforge.net/projects/gkernel/
Source:		http://prdownloads.sourceforge.net/gkernel/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
This utility allows querying and changing of ethernet card settings, such
as speed, port, and autonegotiation.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{_sbindir}/ethtool

%files doc
%defattr(-,root,root)
%doc AUTHORS NEWS


%changelog
* Tue Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3
- first Annvix package (needed by new initscripts)

* Sun May 14 2006 Stefan van der Eijk <stefan@eijk.nu> 3-3mdk
- rebuild for sparc

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 3-2mdk
- Rebuild

* Sun Jun 12 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 3-1mdk
- new release
- %%mkrel
- don't ship COPYING (it's GPL, copyright notice is shipped with common-licenses)

* Mon Dec 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8-1mdk
- new release
- add some doc

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.6-2mdk
- rebuild
- drop redundant requires

* Mon Mar  4 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 1.6-1mdk
- new version
- rebuild with new gcc

* Mon Mar  4 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 1.5-1mdk
- new version
- use %%configure2_5x
- use %%makeinstall_std

* Tue Nov 20 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.4-1mdk
- new version

* Wed Nov  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3-2mdk
- add URL for source tarball
- use 'make DESTDIR='

* Wed Nov  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.3-1mdk
- new version

* Thu May 24 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.2-1mdk
- Version 1.2.  Adds support for getting ethernet driver info.

* Wed Mar 21 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.0-3mdk
- Oops, update the description too, to remove Sparc reference.

* Wed Mar 21 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.0-2mdk
- Build for all architectures.
- Clean spec.
- Fix ethtool for kernel 2.4.
- autoconf/automake support for ethtool.

* Wed Jan 19 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0-1mdk
- first mandrake version.

* Wed Apr 14 1999 Bill Nottingham <notting@redhat.com>
- run through with new s/d

* Tue Apr 13 1999 Jakub Jelinek <jj@ultra.linux.cz>
- initial package.
