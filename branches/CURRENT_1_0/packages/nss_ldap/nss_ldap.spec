%define name 	nss_ldap
%define version 207
%define release 2mdk
%define pam_ldap_version 164

Summary:	NSS library and PAM module for LDAP.
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	LGPL
Group:		System/Libraries
URL: 		http://www.padl.com/
BuildRequires:	db4-devel >= 4.1.25
BuildRequires:	gdbm-devel
BuildRequires:	libldap2-devel-static >= 2.0.7-7.1mdk
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	pam-devel
Source0:	%{name}-%{version}.tar.bz2
Source1: 	pam_ldap-%{pam_ldap_version}.tar.bz2
Source2:	ldap-mdk.conf
Patch0:		nss_ldap-makefile.patch.bz2
Patch1:		nss_ldap-150-db3.patch.bz2
Patch2:		pam_ldap-156-makefile.patch.bz2
Patch3: 	pam_ldap-107-dnsconfig.patch.bz2
Patch4:		pam_ldap-164-fix-duplicate-definition.patch.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot

%description
This package includes two LDAP access clients: nss_ldap and pam_ldap.
Nss_ldap is a set of C library extensions which allows X.500 and LDAP
directory servers to be used as a primary source of aliases, ethers,
groups, hosts, networks, protocol, users, RPCs, services and shadow
passwords (instead of or in addition to using flat files or NIS).

%package -n pam_ldap
Summary:	NSS library and PAM module for LDAP.
Version: 	%{pam_ldap_version}
Release: 	%{release}
License:	LGPL
Group:		System/Libraries
URL: 		http://www.padl.com/
Requires:	nss_ldap >= 207

%description -n pam_ldap
Pam_ldap is a module for Linux-PAM that supports password changes, V2
clients, Netscapes SSL, ypldapd, Netscape Directory Server password
policies, access authorization, crypted hashes, etc.

Install nss_ldap if you need LDAP access clients.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -a 1
%patch0 -p1 -b .makefile
%patch1 -p1 -b .db3
pushd pam_ldap-%{pam_ldap_version}
%patch2 -p1 -b .pam_makefile
%patch3 -p1 -b .dnsconfig
%patch4 -p1 -b .duplicate-definition
cp ../resolve.c .
cp ../resolve.h .

popd

%build
rm -rf $RPM_BUILD_ROOT
%serverbuild
# Build nss_ldap.
aclocal && automake && autoheader && autoconf
%configure --enable-schema-mapping --with-ldap-lib=openldap --enable-debug \
--enable-rfc2307bis --enable-ids-uid --libdir=/lib
%__make INST_UID=`id -u` INST_GID=`id -g`

# Build pam_ldap.
pushd pam_ldap-%{pam_ldap_version}
touch NEWS
aclocal && automake && autoheader && autoconf
export CFLAGS="$CFLAGS -fno-strict-aliasing"
%configure --with-ldap-lib=openldap --libdir=/lib
%__make
popd

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT/lib/security

# Install the nsswitch module.
%make install DESTDIR="${RPM_BUILD_ROOT}" INST_UID=`id -u` INST_GID=`id -g` \
	libdir=/lib


# Install the module for PAM.
pushd pam_ldap-%{pam_ldap_version}
%make install DESTDIR="$RPM_BUILD_ROOT" libdir=/lib
popd
echo "secret" > $RPM_BUILD_ROOT/%{_sysconfdir}/ldap.secret

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/ldap.conf

# Remove unpackaged file
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/nsswitch.ldap

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ -f /etc/init.d/nscd ]; then
	/sbin/service nscd restart >/dev/null 2>/dev/null || :
fi

%postun
/sbin/ldconfig
if [ -f /etc/init.d/nscd ]; then
	/sbin/service nscd restart >/dev/null 2>/dev/null || :
fi

%files
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS ChangeLog COPYING NEWS README doc INSTALL
%doc nsswitch.ldap certutil ldap.conf
%attr (600,root,root) %config(noreplace) %{_sysconfdir}/ldap.secret
%attr (644,root,root) %config(noreplace) %{_sysconfdir}/ldap.conf
/lib/*so*

%files -n pam_ldap 
%defattr(-,root,root)
%doc pam_ldap-%{pam_ldap_version}/{AUTHORS,NEWS,COPYING,COPYING.LIB,README,ChangeLog,pam.d,chsh,chfn,ldap.conf}
/lib/security/*so*

%changelog
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
- remove re-define of %%_libdir (was mapping it to /lib which caused
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

