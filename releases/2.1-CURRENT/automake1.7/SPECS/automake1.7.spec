#
# spec file for package automake1.7
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		automake%{amversion}
%define version 	1.7.9
%define release 	%_revrel

%define amversion 	1.7

%define docheck		0
%{?_with_check:		%global docheck 1}

%define alternatives_install_cmd update-alternatives --install %{_bindir}/automake automake %{_bindir}/automake-%{amversion} 20 --slave %{_bindir}/aclocal aclocal %{_bindir}/aclocal-%{amversion}

Summary:	A GNU tool for automatically creating Makefiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/automake/
Source:		ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Patch0:		automake-1.7.9-infofiles.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	autoconf2.5
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	gawk
BuildRequires:	perl
BuildRequires:	texinfo
%if %{docheck}
BuildRequires:	tetex-latex
BuildRequires:	python
%endif

Requires(post):	info-install
Requires(post):	update-alternatives
Requires(preun): info-install
Requires(preun): update-alternatives
Requires:	perl
Requires:	autoconf2.5
Obsoletes:	automake1.5

%description
Automake is a tool for automatically generating Makefiles compliant with
the GNU Coding Standards.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n automake-%{version}
%patch0 -p0 -b .parallel


%build
export WANT_AUTOCONF_2_5=1
%configure2_5x
%make


%check
%if %{docheck}
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present.  But automake behaviour changed, now it can handle missing
# libtool file as well, so this test is bogus.
perl -pi -e 's/reqd2.test//g' tests/Makefile
export TEX=tex
make check  # VERBOSE=1
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}%{_bindir}/{automake,aclocal}
rm -f %{buildroot}%{_infodir}/*
install -m 0644 automake*info* %{buildroot}%{_infodir}

pushd %{buildroot}%{_infodir}
    for i in *.info*; do
        mv $i %{name}${i#automake}
    done
popd

mkdir -p %{buildroot}%{_datadir}/aclocal


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info
update-alternatives --remove automake %{_bindir}/automake-%{amversion}


%preun
%_remove_install_info %{name}.info


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9
- add -doc subpackage
- remove alternatives and provides for 'automake'
- update buildrequires for %%docheck

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9
- Clean rebuild

* Sat Dec 31 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-5avx
- set alternatives priority to 20

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-2avx
- bootstrap build

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.7.9-1avx
- 1.7.9
- tune up alternative priority (abel)
- add -with-check option to enable 'make check' (abel)
- adjust P0 to refer to the actual command (*-1.7 rather than *1.7) (abel)
- also owns /usr/share/aclocal (abel)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.7.6-4avx
- Annvix build
- require packages not files

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 1.7.6-3sls
- remove %%{prefix}
- minor spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.7.6-2sls
- OpenSLS build
- tidy spec
- remove conflicts since it breaks new automake naming scheme

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
