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
BuildRequires:	perl-devel
BuildRequires:	perl(URPM)
BuildRequires:	perl(BerkeleyDB)

%description
Some tools to check the integrity of rpms from a repository.
It works from rpms or hdlist, and reports missing or wrong
dependencies, conflicts, and other errors.
It can be used to check rpms from a specific project or the
entire distribution.

Currently only one script is included: distlint.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
perl Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix}
make PREFIX=%{_prefix}


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/distlint
%{_bindir}/distlintbatch
%{_bindir}/chkupload
%{_bindir}/chk_inst_files
%{perl_vendorlib}/*.pm
%dir %{perl_vendorlib}/urpmchecker
%{perl_vendorlib}/urpmchecker/*.pm
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc batch_exemple index.html chkupload.main ChangeLog
%doc conf_exemple


%changelog
* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org>  0.1.2
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2-2avx
- rebuild

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.1.2-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
