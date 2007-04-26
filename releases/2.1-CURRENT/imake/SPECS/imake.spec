#
# spec file for package imake
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		imake
%define version 	1.0.2
%define release 	%_revrel

Summary:	C preprocessor interface to the make utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Text Tools
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/util/%{name}-%{version}.tar.bz2
Patch0:		imake-1.0.2-mdv-cleanlinks.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	x11-util-macros >= 1.0.1
BuildRequires:	x11-proto-devel

Requires:	x11-util-cf-files >= 1.0.2

%description
Imake is used to generate Makefiles from a template, a set of cpp macro
functions,  and  a  per-directory input file called an Imakefile.  This allows
machine dependencies (such as compiler options,  alternate com- mand  names,
and  special  make  rules)  to  be kept separate from the descriptions of
the various items to be built.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .cleanlinks_fix


%build
%configure2_5x \
    --with-config-dir=%{_datadir}/X11/config \
    --x-includes=%{_includedir} \
    --x-libraries=%{_libdir}

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
