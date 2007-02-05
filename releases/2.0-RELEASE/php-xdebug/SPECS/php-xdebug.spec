#
# spec file for package php-xdebug
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-%{modname}
%define version		2.0.0
%define release		%_revrel
%define epoch		1

%define phpversion	5.2.0
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		xdebug
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		29_%{modname}.ini

Summary:	Extension for providing function traces and profiling for PHP5
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	PHP License
Group:		Development/PHP
URL:		http://xdebug.org/
Source0:	http://xdebug.org/files/%{modname}-%{version}RC2.tgz
Source1:	xdebug.ini
Source2:	xdebug-docs.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  php-devel >= %{phpversion}

Conflicts:	php-apc

%description
The Xdebug extension helps you debugging your script by providing a lot of
valuable debug information.  The debug information that Xdebug can provide
includes the following:

* stack and function traces in error messages with:
  o full parameter display for user defined functions
  o function name, file name and line indications
  o support for member functions
* memory allocation
* protection for infinite recursions

Xdebug also provides:

* profiling information for PHP scripts
* script execution analysis
* capabilities to debug your scripts interactively with a debug client


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{modname}-%{version}RC2 -a 2


%build
phpize
%configure2_5x \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

# make the debugclient
pushd debugclient
    touch config.h
    gcc %{optflags} -o debugclient main.c usefulstuff.c -lnsl
popd


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_bindir}

install -m 0644 %{_sourcedir}/xdebug.ini %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m 0755 %{soname} %{buildroot}%{phpdir}/extensions/
install -m 0755 debugclient/debugclient %{buildroot}%{_bindir}/

perl -pi -e 's|/usr/lib|%{_libdir}|g' %{buildroot}%{_sysconfdir}/php.d/%{inifile}


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%attr(0755,root,root) %{phpdir}/extensions/%{soname}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%{_bindir}/debugclient

%files doc
%defattr(-,root,root)
%doc CREDITS Changelog LICENSE NEWS README xdebug-docs/*


%changelog
* Fri Jan 05 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.0RC2
- 2.0.0RC2
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
