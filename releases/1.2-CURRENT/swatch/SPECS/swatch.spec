#
# spec file for package swatch
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		swatch
%define version		3.1.1
%define release 	%_revrel

Summary:	A utility for monitoring system logs files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://swatch.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	swatchrc
Source2:	README-mandrake

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel perl-File-Tail perl-Date-Calc perl-Time-HiRes perl-TimeDate

Requires:	perl perl-File-Tail perl-Date-Calc perl-Time-HiRes perl-TimeDate

%description
The Swatch utility monitors system log files, filters out unwanted data
and takes specified actions (i.e., sending email, executing a script,
etc.) based upon what it finds in the log files.


%prep
%setup -q


%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor
%make

%check
%make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

eval `perl '-V:installarchlib'`
mkdir -p %{buildroot}/$installarchlib
perl -pi -e "s|^(INSTALLMAN1DIR\s=\s/usr/share/man/man1)|INSTALLMAN1DIR = \\$\(PREFIX\)/share/man/man1|" %{_builddir}/%{name}-%{version}/Makefile

%makeinstall_std
install tools/swatch_oldrc2newrc -D %{buildroot}%{_bindir}/swatch_oldrc2newrc

mkdir -p %{buildroot}%{_sysconfdir}
cat %{SOURCE1} >> %{buildroot}%{_sysconfdir}/swatchrc

cat %{SOURCE2} >> %{_builddir}/%{name}-%{version}/README-Mandrake

rm -rf %{buildroot}%{perl_vendorlib}/auto


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%doc CHANGES INSTALL COPYRIGHT KNOWN_BUGS README* examples tools
%{_bindir}/swatch
%{_bindir}/swatch_oldrc2newrc
%{_mandir}/man?/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/swatchrc
%dir %{perl_vendorlib}/Swatch
%{perl_vendorlib}/Swatch/*


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1-1avx
- first Annvix build

* Thu Dec 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.1.1-1mdk
- 3.1.1

* Mon May 31 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 3.1-1mdk
- 3.1
- use %%makeinstall_std macro
- update %%files
- update url

* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.0.4-3mdk
- rm -rf %{buildroot} at the beginning of %%install
- rebuild
- remove unpackaged files

* Fri Oct 11 2002 Amaury Amblard-Ladurantie <amaury@mandrakesoft.com> 3.0.4-2mdk
- modified default swatchrc

* Mon Jul 22 2002 Jonathan Gotti <jgotti@mandrakesoft.com> 3.0.4-1mdk
- new release

* Wed Jul 11 2001 Stefan van der Eijk <stefan@eijk.nu> 3.0.2-3mdk
- BuildRequires:	perl-devel

* Wed May 23 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0.2-2mdk
- s/Copyright/License/;

* Fri Feb 23 2001 Gregory Letoquart <gletoquart@mandrakesoft.com> 3.0.2-1mdk
- Up to version 3.0.2

* Fri Feb 23 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.0.1-2mdk
- include manpages
- include default config file
- new README-Mandrake in docs details some ways to customize and run swatch
  under Linux-Mandrake

* Mon Aug  7 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.1-1mdk
- Release 3.0.1 (merge from Redhat)

* Fri Jul 28 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 2.2-11mdk
- BM + macroszification (update patch file for man dir)
- rename specfile to remove version of filename

* Sat Mar 25 2000 Daouda Lo <daouda@mandrakesoft.com> 2.2-10mdk
- relocate to new mandrake group structure 

* Fri Nov 5 1999 Damien Krotkine <damien@mandrakesoft.com>
- Mandrakes release

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Tue Mar 16 1999 Preston Brown <pbrown@redhat.com>
- patched to use /var/log/messages as default, not /var/log/syslog (duh)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Wed Apr 29 1998 Cristian Gafton <gafton@redhat.com>
- fixed paths

* Thu Oct 23 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Fri Aug 22 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
