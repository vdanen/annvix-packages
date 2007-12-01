#
# spec file for package pam_passwdqc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		pam_passwdqc
%define version 	1.0.4
%define release 	%_revrel

Summary:	PAM module for password quality control
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	BSD-compatible
Group:		System/Libraries
URL: 		http://www.openwall.com/passwdqc/
Source0:	ftp://ftp.openwall.com/pub/projects/pam/modules/%{name}/%{name}-%{version}.tar.gz

BuildRoot: 	%{_buildroot}/%{name}-%{version}

%description
pam_passwdqc is a simple password strength checking module for
PAM-aware password changing programs, such as passwd(1).  In addition
to checking regular passwords, it offers support for passphrases and
can provide randomly generated ones.  All features are optional and
can be (re-)configured without rebuilding.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
make CFLAGS="-Wall -fPIC -DHAVE_SHADOW -DLINUX_PAM %{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%make install DESTDIR="%{buildroot}" mandir=%{_mandir} SECUREDIR=/%{_lib}/security


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/%{_lib}/security/pam_passwdqc.so
%{_mandir}/man8/pam_passwdqc.8*

%files doc
%defattr(-,root,root)
%doc LICENSE README


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.0.4
- 1.0.4

* Mon Jul 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- lib64 fixes

* Sat Jul 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2
- first Annvix build; to replace pam_cracklib

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
