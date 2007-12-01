#
# spec file for package smbldap-tools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		smbldap-tools
%define version 	0.9.4
%define release 	%_revrel

Summary:	User & Group administration tools for Samba-OpenLDAP
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Group: 		System/Servers
License: 	GPL
URL:		https://gna.org/projects/smbldap-tools/
Source0: 	http://download.gna.org/smbldap-tools/packages/%{name}-%{version}.tgz
Source1: 	mkntpwd.tar.bz2
Patch0:		smbldap-tools-0.9.4-mdv-mdvconfig.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-perldoc

Requires:	perl-IO-Socket-SSL

%description
Smbldap-tools is a set of perl scripts written by Idealx. Those scripts are
designed to help managing users and groups in a ldap directory server and
can be used both by users and administrators of Linux systems:

- users can change their password in a way similar to the standard
  "passwd" command,
- administrators can perform users and groups management

Scripts are described in the Smbldap-tools User Manual
(http://samba.idealx.org/smbldap-tools.en.html) which also give command
line examples.
You can download the latest version on Idealx web site
(http://samba.idealx.org/dist/).
Comments and/or questions can be sent to the smbldap-tools mailing list
(http://lists.idealx.org/lists/samba).


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a1
%patch0 -p1 -b .mdvconf

# nuke that IDEALX stuff from the code
for i in `find -type f`; do
    perl -pi -e "s|/etc/opt/IDEALX/smbldap-tools/|%{_sysconfdir}/smbldap-tools/|g; \
    s|/opt/IDEALX/bin:||g; \
    s|/opt/IDEALX/sbin|%{_sbindir}|g" $i
done


%build
pushd mkntpwd
    %make CFLAGS="%{optflags}"
popd

# make some manpages
for i in smbldap-groupadd smbldap-groupdel smbldap-groupmod smbldap-groupshow smbldap-passwd \
    smbldap-populate smbldap-useradd smbldap-userdel smbldap-userinfo smbldap-usermod smbldap-usershow; do
    perldoc $i > $i.1
done


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sysconfdir}/smbldap-tools,%{_sbindir},%{perl_vendorlib},%{_mandir}/man1}

install -m 0644 smbldap.conf %{buildroot}%{_sysconfdir}/smbldap-tools/
install -m 0644 smbldap_bind.conf %{buildroot}%{_sysconfdir}/smbldap-tools/
install -m 0644 smbldap_tools.pm %{buildroot}%{perl_vendorlib}/

install -m 0755 smbldap-groupadd %{buildroot}%{_sbindir}/
install -m 0755 smbldap-groupdel %{buildroot}%{_sbindir}/
install -m 0755 smbldap-groupmod %{buildroot}%{_sbindir}/
install -m 0755 smbldap-groupshow %{buildroot}%{_sbindir}/
install -m 0755 smbldap-passwd %{buildroot}%{_sbindir}/
install -m 0755 smbldap-populate %{buildroot}%{_sbindir}/
install -m 0755 smbldap-useradd %{buildroot}%{_sbindir}/
install -m 0755 smbldap-userdel %{buildroot}%{_sbindir}/
install -m 0755 smbldap-userinfo %{buildroot}%{_sbindir}/
install -m 0755 smbldap-usermod %{buildroot}%{_sbindir}/
install -m 0755 smbldap-usershow %{buildroot}%{_sbindir}/
install -m 0755 mkntpwd/mkntpwd %{buildroot}%{_sbindir}/
install -m 0755 mkntpwd/mkntpwd %{buildroot}%{_sbindir}/
install -m 0644 smbldap-*.1 %{buildroot}%{_mandir}/man1/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%{_sbindir}/mkntpwd
%{_sbindir}/smbldap-groupadd
%{_sbindir}/smbldap-groupdel
%{_sbindir}/smbldap-groupmod
%{_sbindir}/smbldap-groupshow
%{_sbindir}/smbldap-passwd
%{_sbindir}/smbldap-populate
%{_sbindir}/smbldap-useradd
%{_sbindir}/smbldap-userdel
%{_sbindir}/smbldap-usermod
%{_sbindir}/smbldap-userinfo
%{_sbindir}/smbldap-usershow
%{_mandir}/man1/*.1*
%{perl_vendorlib}/smbldap_tools.pm

%files doc
%defattr(-,root,root)
%doc CONTRIBUTORS COPYING ChangeLog INFRA INSTALL README TODO doc
%doc smbldap.conf smbldap_bind.conf configure.pl


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.4
- 0.9.4
- update url
- build the man pages, so require perl-perldoc
- drop P1; merged upstream
- updated P0 from Mandriva

* Sun Dec 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.2
- 0.9.2
- fix requires
- P1: use "account" instead of "inetOrgPerson" for the structural
  ObjectClass for computer accounts (mdv bug #23921 -- andreas)

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1-2avx
- P0: reapply changes as when shipped with samba to match the default
  smb.conf, LDAP layout, OpenLDAP ACLs, and default nss_ldap behaviour
  (bgmilne)

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1-1avx
- 0.9.1
- drop redundant P0

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.7-7avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.7-6avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.7-5avx
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
