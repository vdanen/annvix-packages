#
# spec file for package autoconf2.1
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		autoconf2.1
%define version		2.13
%define release 	%_revrel
%define epoch		1

# Factorize uses of autoconf libdir home and handle only one exception in rpmlint
%define scriptdir	%{_datadir}/autotools

# we need to patch out the 3 F77 tests before we can re-enable this
%define docheck		0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically configuring source code
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/autoconf/
Source:		ftp://ftp.gnu.org/pub/gnu/autoconf/autoconf-%{version}.tar.bz2
Source3:	autoconf_special_readme2.1
Patch0:		autoconf-2.12-race.patch
Patch1:		autoconf-2.13-mawk.patch
Patch2:		autoconf-2.13-notmp.patch
Patch3:		autoconf-fix-for-gcc2.96-patch
Patch4:		autoconf-2.13-versioned-info.patch
Patch5:		autoconf-2.13-automake14.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	texinfo
BuildRequires:	m4

Requires(post):	info-install
Requires(preun): info-install
Requires:	gawk
Requires:	m4
Requires:	mktemp
Requires:	%{scriptdir}/ac-wrapper.pl
Conflicts:	autoconf2.5 <= 1:2.59-2avx
Obsoletes:	autoconf <= 1:2.13-22avx
Provides:	autoconf = %{epoch}:%{version}-%{release}
# for tests
%if %{docheck}
BuildRequires:	bison
BuildRequires:	flex
%endif


%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script; 
Autoconf is only required for the generation of the scripts, not
their use.

%{expand:%(cat %{_sourcedir}/autoconf_special_readme2.1)}


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n autoconf-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1 -b .parallel
%patch5 -p1 -b .automake14
install -m 0644 %{_sourcedir}/autoconf_special_readme2.1 IMPORTANT.README.Annvix


%build
%configure --program-suffix=-%{version}
%make


%check
%if %{docheck}
make check     # VERBOSE=1
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mv %{buildroot}%{_infodir}/autoconf.info %{buildroot}%{_infodir}/autoconf-%{version}.info

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f %{buildroot}%{_infodir}/standards*
cp install-sh %{buildroot}%{_datadir}/autoconf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info autoconf-%{version}.info


%preun
%_remove_install_info autoconf-%{version}.info


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/autoconf
%{_infodir}/*

%files doc
%defattr(-,root,root)
%doc README IMPORTANT.README.Annvix


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13
- add -doc subpackage
- fix pre-req

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13
- Clean rebuild

* Fri Dec 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13-25avx
- bootstrap build (new gcc, new glibc)
- disable the tests for now until we can patch out for F77/fortran
  tests since they always fail since we don't ship a fortran compiler

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13-24avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13-23avx
- now known as autoconf2.1
- wrapper script is in autoconf2.5
- add --with-check option to enable make check
- P5: invoke automake-1.4 and aclocal-1.4 instead of random (abel)
- version of automake/aclocal in autoreconf (abel)
- do make check

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.13-22avx
- Annvix build
- require packages not files

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.13-21sls
- more spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.13-20sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
