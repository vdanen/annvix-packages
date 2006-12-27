#
# spec file for package dejagnu
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dejagnu
%define version 	1.4.2
%define release 	%_revrel

Summary:	A front end for testing other programs
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Development/Other
License:	GPL
URL:		http://sourceware.cygnus.com
Source:		%{name}-%{version}.tar.bz2 
Patch2:		dejagnu-1.4.2-mkargs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildArch:	noarch

Requires:	common-licenses
Requires:	tcl >= 8.0
Requires:	expect >= 5.21

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch2 -p1


%build
%configure
%make


%check
# all tests must pass (use runtest that was just built)
(
export PATH=$PWD:$PATH
make check
)


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 contrib/bluegnu2.0.3/doc/dejagnu.1 %{buildroot}%{_mandir}/man1

# Nuke unpackaged files
rm -f %{buildroot}%{_libdir}/config.guess
rm -f %{buildroot}%{_includedir}/dejagnu.h


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_datadir}/dejagnu
%{_datadir}/dejagnu/*
%{_bindir}/runtest
%{_mandir}/man1/dejagnu.1*
%{_mandir}/man1/runtest.1*

%files doc
%defattr(-,root,root)
%doc AUTHORS NEWS README TODO


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
- add -doc subpackage
- rebuild with gcc4
- drop the epoch (which means on upgrade the old one needs to be removed
  first and then this one gets installed... that epoch was retarded)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-11avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-10avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-9avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-8avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.4.2-7sls
- remove %%build_opensls macros
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.4.2-6sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not build any doc stuff

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
