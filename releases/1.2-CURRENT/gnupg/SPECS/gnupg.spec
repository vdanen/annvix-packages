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
%define version 	1.4.2
%define release		%_revrel

Summary:	GNU privacy guard - a free PGP replacement
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		http://www.gnupg.org
Source:		ftp://ftp.gnupg.org/pub/gcrypt/gnupg/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/pub/gcrypt/gnupg/%{name}-%{version}.tar.bz2.sig
Source2:	annvix-keys.tar.bz2
Source3:	annvix-keys.tar.bz2.asc

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	exim

%description
GnuPG is GNU's tool for secure communication and data storage.
It can be used to encrypt data and to create digital signatures.
It includes an advanced key management facility and is compliant
with the proposed OpenPGP Internet standard as described in RFC2440.


%prep
%setup -q


%build
%ifnarch sparc sparc64
    mguard="--enable-m-guard"
%endif
%configure2_5x \
    --with-included-gettext \
    --with-static-rnd=linux \
    --disable-ldap \
    --without-ldap \
    $mguard
make
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

sed -e "s#../g10/gpg#gpg#" < tools/lspgpot > %{buildroot}%{_bindir}/lspgpot

chmod 0755 %{buildroot}%{_bindir}/lspgpot
# (fc) 1.0.4-5mdk gpg is setuid
chmod 4755  %{buildroot}%{_bindir}/gpg

perl -pi -e 's|/usr/local|/usr/|' %{buildroot}%{_mandir}/man1/gpg.1

#cp -aRf doc doc.geoff
#rm -f doc.geoff/Makefile*
#rm -f doc.geoff/{gpg,gpgv}.1
#rm -f doc/Makefile*
#rm -f doc/{gpg,gpgv}.1

# installed but not wanted
rm -f %{buildroot}%{_datadir}/gnupg/{FAQ,faq.html}
rm -f %{buildroot}%{_datadir}/locale/locale.alias

mkdir -p %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS
tar xvjf %{SOURCE2} -C %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info gpg.info
%_install_info gpgv.info

%postun
%_remove_install_info gpg.info
%_remove_install_info gpgv.info


%files -f %{name}.lang
%defattr(-,root,root)
%doc README NEWS THANKS TODO ChangeLog doc/DETAILS doc/FAQ doc/HACKING
%doc doc/faq.html doc/OpenPGP doc/samplekeys.asc
%attr(4755,root,root) %{_bindir}/gpg
%{_bindir}/gpgv
%{_bindir}/lspgpot
%{_bindir}/gpgsplit
%dir %{_libdir}/gnupg
%{_libdir}/gnupg/gpgkeys*
%dir %{_datadir}/gnupg
%{_datadir}/gnupg/options.skel
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_infodir}/gpg*.info.bz2
%dir %{_sysconfdir}/RPM-GPG-KEYS
%attr(0644,root,root) %{_sysconfdir}/RPM-GPG-KEYS/*.asc


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Thu Nov 27 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.2.3-3.1.92mdk
- security fix (elgamal vuln)

* Tue Aug 26 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.2.3-3mdk
- remove import of gpg keys for rpm as it apparently corrupts the rpmdb

* Tue Aug 26 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.2.3-2mdk
- rebuild so it shows up

* Sat Aug 23 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.2.3-1mdk
- don't add keys to root's keyring anymore
- new directory /etc/RPM-GPG-KEYS stores the keys we use
- import keys into rpm in %%post
- miscellaneous specfile cleanups

* Mon Aug 11 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.2-4mdk
- Move gpgkeys to gnupg subdir
- Patch1: Fix regression test script

* Sat Aug  2 2003 Pixel <pixel@mandrakesoft.com> 1.2.2-3mdk
- /usr/lib/gpgkeys_mailto disappears when i rebuild, otherwise i would have done:
	  only /usr/lib/gpgkeys_mailto needs perl(Getopt::Std),
	  ignore this require
  but this is not needed since gpgkeys_mailto has disappeared (why??)

* Sat Jun 07 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.2.2-2mdk
- fix bus-error on sparc
- don't include debug files

* Wed May  7 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.2.2-1mdk
- 1.2.2

* Tue Feb 25 2003 François Pons <fpons@mandrakesoft.com> 1.2.1-3mdk
- rebuild to remove libopenssl0 dependencies.

* Mon Dec 30 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.1-2mdk
- rebuild against new glibc, etc.
- include missing manpage, info files, _libdir files, and gpgsplit
- install_info/remove_install_info macros

* Mon Oct 28 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1
- try enabling memory guard features (--enable-m-guard)

* Tue Aug 13 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.0.7-3mdk
- fix permissions of /root/.gnupg to be 600 (this way 644 files in the dir
  don't make gpg complain) - re: Andreas Simon
- clean our build dir
- add www.mandrakesecure.net as the default keyserver in newly-created
  options files

* Mon Aug 12 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-2mdk
- rpmlint fixes: strange-permission
- costlessly make check in %%build stage

* Tue Apr 30 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.0.7-1mdk
- 1.0.7
- remove P0; included upstream

* Wed Mar 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.0.6-5mdk
- updated gpg keys

* Tue Oct 23 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.6-4mdk
- strip sgid bit from gpg (thanks ekj@ekj.vetsdata.no) for security

* Fri Jul 13 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.6-3mdk
- s/Copyright/License/
- minor spec cleaning
- use pristine source (tar.gz) and include signature file for sourc
  (security policy)

* Wed May 30 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.6-2mdk
- fix description, remove reference to patents

* Wed May 30 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.6-1mdk
- 1.0.6

* Tue May  1 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.5-1.1mdk
- security update for 7.2/8.0

* Tue May  1 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.5-1mdk
- 1.0.5

* Tue Apr 10 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.0.4-6mdk
- include new public key signed by mandrake@mandrakesoft.com and
  security@turbolinux.com

* Mon Apr  9 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0.4-5mdk
- ship gnupg as setuid (blessed by maintainer and security team)

* Fri Jan 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.4-4mdk
- remove FAQ and faq.html from /usr/share/gnupg.

* Wed Dec 20 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.0.4-3mdk
- security fix, official patch applied
- add the --allow-secret-key-import patch from CVS
- remove the strlen patch, as it is included in the official security patch
- specfile cleanups

* Tue Nov 22 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.4-2mdk
- Red Hat merge aka shamelessly rip patches.

* Wed Oct 18 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.4-1mdk
- build a new and sane version (aka big big bugz fix).

* Thu Oct 12 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.3-1mdk
- 1.2.3
- puts Url: and full Source: path

* Tue Oct  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.2-4mdk
- touch /root/.gnupg/options in %%post to avoid errors.

* Fri Sep 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.2-3mdk
- create ~/.gnupg in %%post to avoid errors.

* Thu Sep 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.2-2mdk
- added import of mandrake's gpg keys ib %%post

* Wed Sep 13 2000 Vincent Danen <vdanen@mandrakesoft.com> 1.0.2-1mdk
- 1.0.2

* Wed Sep 13 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.1-3mdk
- BM

* Tue Apr 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.1-2mdk
- Upgrade groups.

* Thu Jan  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.1-1mdk
- First spec file for Mandrake distribution, mainly based on debian version.

# end of file
