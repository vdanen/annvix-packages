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
%define version 	243
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

BuildRoot: 	%{_buildroot}/%{name}-%{version}
#BuildRequires:	db4-devel >= 4.1.25
BuildRequires:	openldap-devel >= 2.0.7-7.1mdk, automake1.4
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description
This package includes two LDAP access clients: nss_ldap and pam_ldap.
Nss_ldap is a set of C library extensions which allows X.500 and LDAP
directory servers to be used as a primary source of aliases, ethers,
groups, hosts, networks, protocol, users, RPCs, services and shadow
passwords (instead of or in addition to using flat files or NIS).


%prep
%setup -q
%patch0 -p1 -b .makefile


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
%doc ANNOUNCE AUTHORS ChangeLog COPYING NEWS README doc INSTALL
%doc nsswitch.ldap certutil ldap.conf
%attr (600,root,root) %config(noreplace) %{_sysconfdir}/ldap.secret
%attr (644,root,root) %config(noreplace) %{_sysconfdir}/ldap.conf
/%{_lib}/*so*
%{_mandir}/man5/nss_ldap.5*


%changelog
* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Mon Nov 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 207-4.1.92mdk
- fixes from Luca Berra <bluca@vodka.it>
  - fix looking for db4 libraries
  - remove buildrequire for gdbm, static ldap libs
  - buildrequires: ldap-devel

* Fri Oct 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 207-4mdk
- use /%%{_lib} not /lib so libs are installed in the right place for amd64

* Fri Sep 26 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 207-3mdk
- fix deps

* Thu Sep 18 2003 Florin <florin@mandrakesoft.com> 207-2mdk
- rebuild

* Tue Aug 05 2003 Buchan Milne <bgmilne@linux-mandrake.com> 207-1mdk
- 207 and pam_ldap 164
- rebuild for kerberos-1.3
- Remove redundant buildrequires, tighten libdb requires to ensure db4.1
- patch (4) pam_ldap to not redefine _rebind_proc, use -fno-strict-aliasing

* Mon May  5 2003 Vincent Danen <vdanen@mandrakesoft.com> 204-2mdk
- change defaults in our ldap.conf to make it more suitable for
  authentication purposes

* Sat Apr 12 2003 Stefan van der Eijk <stefan@eijk.nu> 204-1mdk
- pam_ldap 161
- nss_ldap 204
- remove unpackaged file
- Removed duplicate BuildRequires

* Wed Oct 30 2002 Vincent Danen <vdanen@mandrakesoft.com> 202-1mdk
- pam_ldap 202
- nss_ldap 156 (security fixes)
- rediff P2

* Thu Aug 01 2002 Vincent Danen <vdanen@mandrakesoft.com> 194-3mdk
- update /etc/ldap.conf so paths to certs match 9.0 specs
  (/etc/ssl/openldap)

* Mon Jul 22 2002 Vincent Danen <vdanen@mandrakesoft.com> 194-2mdk
- remove re-define of %%{_libdir} (was mapping it to /lib which caused
  problems with brp-mandrake); re: David Walser
- don't call nscd initscript with condrestart; re: David Walser

* Tue Jun 11 2002 Vincent Danen <vdanen@mandrakesoft.com> 194-1mdk
- pam_ldap 148
- nss_ldap 194

* Thu Mar 28 2002 Vincent Danen <vdanen@mandrakesoft.com> 173-2mdk
- re-enable --with-rfc2307bis and --enable-ids-uid

* Thu Nov 22 2001 Philippe Libat <philippe@mandrakesoft.com> 173-1mdk
- pam_ldap version: 134
- nss_ldap version: 173

* Thu Oct 18 2001 Philippe Libat <philippe@mandrakesoft.com> 172-4mdk
- new db3

* Sat Oct 13 2001 Stefan van der Eijk <stefan@eijk.nu> 172-3mdk
- BuildRequires: db3-devel

* Fri Sep 21 2001 Vincent Saugey <vince@mandrakesoft.com> 172-2mdk
- Change default and conf file
- Set to tls by default

* Tue Aug 21 2001 Vincent Saugey <vince@mandrakesoft.com> 168-1mdk
- update pam_ldap & nss_ldap

* Fri Jul 13 2001 Philippe Libat <philippe@mandrakesoft.com> 163-1mdk
- update pam_ldap & nss_ldap

* Mon Jul 02 2001 Philippe Libat <philippe@mandrakesoft.com> 159-1mdk
- update pam_ldap & nss_ldap version

* Sun Jun 17 2001 Stefan van der Eijk <stefan@eijk.nu> 153-3mdk
- BuildRequires: pam-devel
- bzipped patches

* Tue Jun 05 2001 Philippe Libat <philippe@mandrakesoft.com> 153-2mdk
- added patch: specify per-service attributes from Matthew Geddes <mgeddes@xavier.sa.edu.au>

* Thu May 17 2001 Philippe Libat <philippe@mandrakesoft.com> 153-1mdk
- new pam_ldap and nss_ldap

* Thu May 17 2001 Philippe Libat <philippe@mandrakesoft.com> 150-7mdk
- split in 2 RPMs

* Wed May 16 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 150-6mdk
- added creation of ldap.secret
- changed ldap.conf defaults

* Wed May 16 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 150-5mdk
- dinamically linked libraries in nss_ldap

* Mon May 07 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 150-4mdk
- re-enabled pam_ldap-107-dnsconfig.patch
- added BuildRequires:	libldap2-devel-static >= 2.0.7-8mdk

* Sun Apr 29 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 150-3mdk
- pam_ldap-108
- disabled pam_ldap-105-dnsconfig.patch
- new db3 patch

* Mon Apr 16 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 150-2mdk
- pam_ldap-107

* Fri Apr 13 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 150-1mdk
- nss_ldap-150
- removed no more needed nss_ldap-149-fail.patch
- removed no more needed pam_ldap-46-pam_console.patch

* Thu Apr 12 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 149-2mdk
- removed unneeded files
- added post and postun
- added nscd reset
- patched non-root nss_ldap compilation
- added db3 support
- fixed configure
- merged with pam_ldap  
- added BuildRequires openssl-devel, libsasl7-devel, libldap2-devel
- added Requires openssl, libsasl7, libldap2
- changed make macro

* Tue Mar 06 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 149-1mdk
- new release 
- clean up in spec
- splitted from pam_ldap

* Wed Aug 30 2000 Etienne Faure <etienne@mandrakesoft.com> 107-2mdk
- rebuilt with new %doc macro

* Fri Mar 31 2000 Jerome Dumonteil <jd@mandrakesoft.com>
- merge with Nalin Dahyabhai'RH patchs
- update to nss_ldap 107
- update to pam_ldap 46
- change group

* Tue Nov 30 1999 Jerome Dumonteil <jd@mandrakesoft.com>
- use of _tmppatch in Buildroot.
- changes in the description text.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First mandrake release.
- Fix building as user.

* Fri Oct 22 1999 Bill Nottingham <notting@redhat.com>
- statically link ldap libraries (they're in /usr/lib)

* Tue Aug 10 1999 Cristian Gafton <gafton@redhat.com>
- use the ldap.conf file as an external source
- don't forcibly build the support for version 3
- imported the default spec file from the tarball and fixed it up for RH 6.1

