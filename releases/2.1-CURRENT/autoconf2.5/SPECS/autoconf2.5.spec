#
# spec file for package autoconf
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		autoconf
%define version		2.61
%define release 	%_revrel
%define epoch		1

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
Source:		ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.bz2
Patch1:		autoconf-2.61-avx-dont_use_help2man.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	texinfo
BuildRequires:	m4

Requires(post):	info-install
Requires(preun): info-install
Requires:	gawk
Requires:	m4
Requires:	mktemp
Requires:	perl
Requires:	perl(MDK::Common)
Obsoletes:	autoconf2.5
Provides:	autoconf2.5 = %{epoch}:%{version}-%{release}
Conflicts:	autoconf 2.1 < 1:2.13-7756avx

# for tests
%if %{docheck}
BuildRequires:	flex
BuildRequires:	bison
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n autoconf-%{version}
%patch1 -p1 -b .dont_use_help2man


%build
%configure2_5x
make


%check
%if %{docheck}
make check	# VERBOSE=1
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f %{buildroot}%{_infodir}/standards*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info autoconf.info


%preun
%_remove_install_info autoconf.info


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/autoconf
%{_infodir}/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README AUTHORS BUGS COPYING INSTALL NEWS THANKS TODO


%changelog
* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.61
- 2.61
- drop P0; no longer required
- rediff P1
- add more docs
- drop the wrapper support and rename to autoconf

* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.60
- add requires on perl(MDK::Common)

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.60
- 2.60
- disable make check, it dies saying it can't allocate memory
- P1: disable the need for help2man

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.59
- add -doc subpackage
- s/OpenSLS/Annvix/g

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.59
- Clean rebuild

* Fri Dec 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.59
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.59-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.59-4avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.59-3avx
- requires autconf2.1 for wrapper
- call this package's autoconf when no configure.in or configure.ac
  detected
- so starts the mdk "BIG MOVE" (almost a year later =))

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.59-2avx
- Annvix build
- require packages not files

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.59-1sls
- 2.59

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.57-7sls
- remove %%build_opensls macro
- remove emacs files
- more spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.57-6sls
- OpenSLS build
- tidy spec
- use %%build_opensls to remove emacs files

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
