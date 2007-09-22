#
# spec file for package gnupg
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gnupg
%define version 	1.4.7
%define release		%_revrel

Summary:	GNU privacy guard - a free PGP replacement
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://www.gnupg.org
Source0:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/gnupg/%{name}-%{version}.tar.bz2.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	exim
BuildRequires:	curl-devel
BuildRequires:	libtermcap-devel
BuildRequires:	gettext
BuildRequires:	bzip2-devel
BuildRequires:	libusb-devel
BuildRequires:	perl
BuildRequires:	readline-devel

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x \
    --with-included-gettext \
    --enable-static-rnd=linux \
    --disable-ldap \
    --without-ldap \
    --enable-noexecstack \
    --enable-m-guard
%make


%check
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

sed -e "s#../g10/gpg#gpg#" < tools/lspgpot > %{buildroot}%{_bindir}/lspgpot

chmod 0755 %{buildroot}%{_bindir}/lspgpot

perl -pi -e 's|/usr/local|/usr/|' %{buildroot}%{_mandir}/man1/gpg.1

# installed but not wanted
rm -f %{buildroot}%{_datadir}/gnupg/{FAQ,faq.html}
rm -f %{buildroot}%{_datadir}/locale/locale.alias

# remove non-standard lc directories
for i in en@boldquot en@quot ; do rm -rf %{buildroot}%{_datadir}/locale/$i; done

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info gnupg.info

%postun
%_remove_install_info gnupg.info


%files -f %{name}.lang
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/gpg
%{_bindir}/gpgv
%{_bindir}/lspgpot
%{_bindir}/gpgsplit
%{_bindir}/gpg-zip
%dir %{_libdir}/gnupg
%{_libdir}/gnupg/gpgkeys*
%dir %{_datadir}/gnupg
%{_datadir}/gnupg/options.skel
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_infodir}/gnupg*.info*

%files doc
%defattr(-,root,root)
%doc README NEWS THANKS TODO doc/DETAILS doc/FAQ doc/HACKING
%doc doc/faq.html doc/OpenPGP doc/samplekeys.asc


%changelog
* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.4.7
- use parallel build
- remove sparc conditionals
- build against new curl
- drop ChangeLog, we already have NEWS

* Sat Jun 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.4.7
- rebuild against new readline

* Wed Mar 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.4.7
- 1.4.7: fixes CVE-2007-1263

* Wed Jan 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.4.6
- use --enable-static-rnd instead of --with-static-rnd

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.6
- 1.4.6: fixes CVE-2006-6235
- fix the buildrequires
- put the tests in %%check

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.4
- spec cleanups
- remove locales

* Thu Jul 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.4
- 1.4.4
- pass --enable-noexecstack to configure
- don't ship it suid root anymore (yes, we loose some memory protection,
  but that's less of a concern than a vuln in gpg someone could take
  advantage of to elevate to root privs)
- drop P0; fixed upstream

* Tue Jun 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2.2
- P0: security patch for CVE-2006-3082
- don't install the gpg keys; the rpm package does this now
- add -doc subpackage
- rebuild with gcc4

* Thu Mar 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2.2
- 1.4.2.2 (fixes CVE-2006-0049)

* Wed Feb 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2.1
- 1.4.2.1 (fixes CVE-2006-0455)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-1avx
- 1.4.2
- P0 dropped; merged upstream
- don't build against ldap libs

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.6-4avx
- bootstrap build (new gcc, new glibc)
- gnupg builds the gpgkeys_* files based on what's installed, so
  although it seems wierd, we need to require exim

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.6-3avx
- bootstrap build

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.6-2avx
- P0: patch to fix CAN-2005-0366

* Sun Sep 12 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.6-1avx
- 1.2.6
- s/opensls-keys/annvix-keys/
- remove P2; fixed upstream
- remove unapplied P1
- remove P0; the mandrakesecure.net keyserver no longer exists

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3-6avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.2.3-5sls
- minor spec cleanups
- get rid of some docs we don't need
- use OpenSLS key rather than Mandrake keys

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 1.2.3-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
