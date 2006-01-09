#
# spec file for package pam_ldap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		pam_ldap
%define version 	180
%define release 	%_revrel

Summary:	PAM module for LDAP
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	LGPL
Group:		System/Libraries
URL: 		http://www.padl.com/
Source0:	http://www.padl.com/download/%{name}-%{version}.tar.bz2
Patch0:		pam_ldap-156-makefile.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	openldap-devel >= 2.0.7-7.1mdk, pam-devel, automake1.4

Requires:	nss_ldap >= 217

%description
Pam_ldap is a module for Linux-PAM that supports password changes, V2
clients, Netscapes SSL, ypldapd, Netscape Directory Server password
policies, access authorization, crypted hashes, etc.


%prep
%setup -q
%patch0 -p1 -b .makefile


%build
%serverbuild

rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake

export CFLAGS="$CFLAGS -fno-strict-aliasing"
%configure \
    --with-ldap-lib=openldap \
    --libdir=/%{_lib}
%__make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}/%{_lib}/security

%make install DESTDIR="%{buildroot}" libdir=/%{_lib}

# Remove unpackaged file
rm -rf %{buildroot}%{_sysconfdir}/ldap.conf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING COPYING.LIB README pam.d chsh chfn ldap.conf
/%{_lib}/security/*so*
%{_mandir}/man5/pam_ldap.5*


%changelog
* Mon Jan 09 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 180-1avx
- first Annvix package; split from nss_ldap
