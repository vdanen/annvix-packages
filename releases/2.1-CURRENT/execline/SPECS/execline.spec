#
# spec file for package execline
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		execline
%define version		1.07
%define release		%_revrel

%define _bindir		/bin

Summary:	A light non-interactive scripting language
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Shells
URL:		http://www.skarnet.org/software/execline/
Source0:	http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  dietlibc-devel >= 0.28
BuildRequires:  skalibs-devel >= 0.40

%description
execline is a very light, non-interactive scripting language, which is 
similar to a shell. Simple shell scripts can be easily rewritten in the 
execline language, improving performance and memory usage. execline was 
designed for use in embedded systems, but works on most Unix flavors.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n admin


%build
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif

pushd %{name}-%{version}
    echo "$COMP -O2 -W -Wall -fomit-frame-pointer -pipe" > conf-compile/conf-cc
    echo "$COMP -Os -static -s" > conf-compile/conf-ld
    echo "strip" >conf-compile/conf-stripbins

    echo "linux-:%{_target_cpu}-:" > src/sys/systype

    echo "%{_includedir}/skalibs" > conf-compile/import
    echo "%{_libdir}/skalibs" >> conf-compile/import

    package/compile
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/bin

pushd %{name}-%{version}
    for i in `cat package/command.exported` ;  do
        install -m 0755 command/$i %{buildroot}/bin/
    done
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/bin/*

%files doc
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html


%changelog
* Mon Nov 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- 1.07
- explicitly set 'strip' as conf-compile/conf-stripbins

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.06
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.06
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.06
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Tue Aug 23 2005 Sean P. Thomas <spt-at-build.annvix.org> 1.06-1avx
- initial Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
