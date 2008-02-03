#
# spec file for package nss_ldap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		nss_ldap
%define version 	259
%define release 	%_revrel

Summary:	NSS library for LDAP
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	LGPL
Group:		System/Libraries
URL: 		http://www.padl.com/
Source0:	http://www.padl.com/download/%{name}-%{version}.tar.gz
Patch0:		nss_ldap-makefile.patch
Patch1:		nss_ldap-250-bind_policy_default_soft.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
#BuildRequires:	db4-devel >= 4.1.25
BuildRequires:	openldap-devel >= 2.0.7-7.1mdk
BuildRequires:	automake1.4
BuildRequires:	krb5-devel

Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description
This package includes two LDAP access clients: nss_ldap and pam_ldap.
Nss_ldap is a set of C library extensions which allows X.500 and LDAP
directory servers to be used as a primary source of aliases, ethers,
groups, hosts, networks, protocol, users, RPCs, services and shadow
passwords (instead of or in addition to using flat files or NIS).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .makefile
%patch1 -p1 -b .bind_policy_soft
# first line not commented upstream for some reason
perl -pi -e 's/^ /#/' ldap.conf


%build
%serverbuild

rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake

%configure \
    --enable-schema-mapping \
    --with-ldap-lib=openldap \
    --enable-debug \
    --enable-rfc2307bis \
    --enable-ids-uid \
    --libdir=/%{_lib}
%__make INST_UID=`id -u` INST_GID=`id -g`


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}/%{_lib}

# Install the nsswitch module.
%make install DESTDIR="%{buildroot}" INST_UID=`id -u` INST_GID=`id -g` \
    libdir=/%{_lib}
echo "secret" > %{buildroot}%{_sysconfdir}/ldap.secret

# Remove unpackaged file
rm -rf %{buildroot}%{_sysconfdir}/nsswitch.ldap
rm -rf %{buildroot}%{_libdir}/libnss_ldap.so.2


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
/sbin/ldconfig
%_post_srv nscd

%postun
/sbin/ldconfig
%_preun_srv nscd


%files
%defattr(-,root,root)
%attr (600,root,root) %config(noreplace) %{_sysconfdir}/ldap.secret
%attr (644,root,root) %config(noreplace) %{_sysconfdir}/ldap.conf
/%{_lib}/*so*
%{_mandir}/man5/nss_ldap.5*

%files doc
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS ChangeLog COPYING NEWS README doc INSTALL
%doc nsswitch.ldap certutil ldap.conf


%changelog
* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 259
- rebuild against new krb5

* Thu Dec 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 259
- 259

* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 257
- 257
- rebuild against new openldap

* Sat Dec 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 253
- fix buildrequires and rebuild against new krb5

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 253
- 253
- rebuild against new openldap

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 250
- rebuild against new openldap 
- spec cleanups

* Sat Jun 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 250
- 250
- P1: default bind_policy is set to "soft" to keep previous default
  behavious of not retrying binds to servers that are not available
- first line of ldap.conf isn't commented; fix it
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 243
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 243
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Oct 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 243-1avx
- 243

* Wed Sep 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 242-1avx
- 242

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 239-1avx
- 239
- break out the pam_ldap package into it's own package
- libtoolize
- BuildRequires openldap-devel, not libldap-devel

* Tue Aug 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 220-5avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 220-4avx
- rebuild

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 220-3avx
- rebuild against latest openssl

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 220-2avx
- pam_ldap 170

* Wed Jun 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 220-1avx
- pam_ldap 169
- nss_ldap 220
- remove P1 (obsolete)
- rediff P5 and rename to P1
- always have pam_ldap require this packaged version of nss_ldap

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 207-7avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 207-6sls
- minor spec cleanups
- use _srv macros to restart nscd

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 207-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
