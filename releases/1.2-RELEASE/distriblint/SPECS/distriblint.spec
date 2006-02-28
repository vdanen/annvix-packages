#
# spec file for package distriblint
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		distriblint
%define version 	0.1.2
%define release 	%_revrel

Summary:	Tools to check integrity of rpms repository
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://youri.zarb.org/
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:      noarch
BuildRequires:	perl-devel, perl-URPM, perl-BerkeleyDB

%description
Some tools to check the integrity of rpms from a repository.
It works from rpms or hdlist, and reports missing or wrong
dependencies, conflicts, and other errors.
It can be used to check rpms from a specific project or the
entire distribution.

Currently only one script is included: distlint.


%prep
%setup -q


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix}
make PREFIX=%{_prefix}
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc batch_exemple index.html chkupload.main ChangeLog
%doc conf_exemple
%{_bindir}/distlint
%{_bindir}/distlintbatch
%{_bindir}/chkupload
%{_bindir}/chk_inst_files
%{perl_vendorlib}/*.pm
%dir %{perl_vendorlib}/urpmchecker
%{perl_vendorlib}/urpmchecker/*.pm
%{_mandir}/*/*

%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2-2avx
- rebuild

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2-1avx
- first Annvix build

* Tue Feb 24 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.1.2-1mdk
- 0.1.2 (fix dependencies checking about epoch promotion)

* Mon Feb 09 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.1.1-1mdk
- 0.1.1

* Thu Aug 28 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.1.0-1mdk
- 0.1.0
 
* Thu Aug 07 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.0.9-2mdk
- rebuild for new perl
- use %%makeinstall_std macro

* Fri Jun 06 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.9-1mdk
- 0.0.9

* Wed May 21 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.8-1mdk
- 0.0.8
- fix titi stuff

* Wed May 14 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.7-1mdk
- 0.0.7
- Thx to titi for perl_checker fix

* Sun May 04 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.6-1mdk
- add --reb flag

* Wed Apr 30 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.5-1mdk
- add --update flag
- add html page (%%doc)
- lot of bug fix (yes, yes)

* Sat Apr 26 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.4-1mdk
- 0.0.4 
- batch script for mail, fix bug...

* Fri Apr 25 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.3-1mdk
- add src vs binary checking
- fix somes bug

* Wed Apr 23 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.2-1mdk
- add arch options (only for binary at time)
- fix obsoletes detection

* Tue Apr 22 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.0.1-1mdk
- initial version.
