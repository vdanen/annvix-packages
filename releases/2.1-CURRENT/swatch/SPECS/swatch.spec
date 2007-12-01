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
BuildRequires:	perl-devel
BuildRequires:	perl(File::Tail)
BuildRequires:	perl(Date::Calc)
BuildRequires:	perl(Time::HiRes)
BuildRequires:	perl-TimeDate

Requires:	perl(File::Tail)
Requires:	perl(Date::Calc)
Requires:	perl(Time::HiRes)
Requires:	perl-TimeDate

%description
The Swatch utility monitors system log files, filters out unwanted data
and takes specified actions (i.e., sending email, executing a script,
etc.) based upon what it finds in the log files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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

cat %{SOURCE2} >> %{_builddir}/%{name}-%{version}/README-Annvix

rm -rf %{buildroot}%{perl_vendorlib}/auto


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/swatch
%{_bindir}/swatch_oldrc2newrc
%{_mandir}/man?/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/swatchrc
%dir %{perl_vendorlib}/Swatch
%{perl_vendorlib}/Swatch/*

%files doc
%defattr(-,root,root)
%doc CHANGES INSTALL COPYRIGHT KNOWN_BUGS README* examples tools


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1
- rebuild

* Sat Jan 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1
- fix requires

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1-1avx
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
