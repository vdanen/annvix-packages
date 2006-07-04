#
# spec file for package pam
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# pam-0.99.3.0-6mdk
#
# $Id$

%define revision	$Rev$
%define name		pam
%define version		0.99.3.0
%define release		%_revrel

%define pam_redhat_version 0.99.2-1

%define rhrelease	5
%define libname		%mklibname %{name} 0

Summary:	A security tool which provides authentication for applications
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or BSD
Group:		System/Libraries
URL:		http://www.us.kernel.org/pub/linux/libs/pam/index.html
Source0:	ftp://ftp.us.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%{version}.tar.bz2
Source1:	pam-redhat-%{pam_redhat_version}.tar.bz2
Source2:	other.pamd
Source3:	system-auth.pamd
Source4:	pam-0.99.3.0-README.update
Source5:	pam-annvix.perms

# RedHat patches (0-100)
Patch0:		pam-0.99.2.1-redhat-modules.patch
Patch1:		pam-0.78-unix-hpux-aging.patch
Patch2:		pam-0.75-sgml2latex.patch
Patch3:		pam-0.99.2.1-dbpam.patch

# Mandriva patches (101-200)
Patch100:	Linux-PAM-0.99.3.0-mdvperms.patch
# (fl) fix infinite loop
Patch101:	pam-0.74-loop.patch
# (fl/blino) reset to id 0 if user/group isn't found instead of stopping processing
Patch102:	Linux-PAM-0.99.3.0-console-reset.patch
# (fc) 0.75-29mdk don't complain when / is owned by root.adm
Patch103:	Linux-PAM-0.99.3.0-pamtimestampadm.patch
Patch104:	Linux-PAM-0.99.3.0-verbose-limits.patch
# (fl) pam_xauth: set extra groups because in high security levels
#      access to /usr/X11R6/bin dir is controlled by a group
Patch105:	Linux-PAM-0.99.3.0-xauth-groups.patch
# (tv/blino) add defaults for nice/rtprio in /etc/security/limits.conf
Patch106:	Linux-PAM-0.99.3.0-enable_rt.patch
# (fl) fix uninitialized variable user (aka fix crash on C3)
Patch107:	pam-0.77-use_uid.patch
# (blino) fix parallel build (in doc/specs and pam_console)
Patch108:	Linux-PAM-0.99.3.0-pbuild.patch
Patch109:	Linux-PAM-0.99.3.0-pbuild-rh.patch
# (blino) ensure that sgml2txt worked
Patch110:	Linux-PAM-0.99.3.0-sgml2txt.patch
# (blino) allow to disable pwdb
Patch111:	Linux-PAM-0.99.3.0-pwdb.patch

# Annvix patches (200+)
Patch200:	pam-0.99.3.0-annvix-perms.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison, flex, glib2-devel
BuildRequires:	db4-devel, automake1.8, openssl-devel

Requires:	glibc-crypt_blowfish-devel
# pam_unix is now provided by pam_tcb
Requires:	pam_tcb, pam_passwdqc
Requires(pre):	rpm-helper
Requires(pre):	setup >= 2.5-5735avx
Obsoletes:	pamconfig
Provides:	pamconfig

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.


%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{name} < 0.77-11sls

%description -n %{libname}
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the libraries for %{name}


%package -n %{libname}-devel
Summary:	Development headers and libraries for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel <= 0.77-10sls

%description -n %{libname}-devel
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the development libraries for %{name}


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n Linux-PAM-%{version} -a 1
# (RH)
%patch0 -p0 -b .redhat-modules
%patch1 -p1 -b .unix-hpux-aging
%patch2 -p1 -b .doc
%patch3 -p1 -b .dbpam

# (Mandriva)
%patch100 -p1 -b .mdvperms
%patch101 -p1 -b .loop
%patch102 -p1 -b .console-reset
%patch103 -p1 -b .pamtimestampadm
%patch104 -p1 -b .verbose-limits
%patch105 -p1 -b .xauth-groups
%patch106 -p1 -b .enable_rt
%patch107 -p1 -b .use_uid
%patch108 -p1 -b .pbuild
%patch109 -p1 -b .pbuild-rh
%patch110 -p1 -b .sgml2txt
%patch111 -p1 -b .pwdb

%patch200 -p1 -b .avxperms

# Remove unwanted modules.
for d in pam_{cracklib,debug,postgresok,rps,selinux,unix}; do
    rm -r modules/$d
    sed -i "s,modules/$d/Makefile,," configure.in
    sed -i "s/ $d / /" modules/Makefile.am
done
find modules -type f -name Makefile -delete -print


for readme in modules/pam_*/README ; do
    cp -f ${readme} doc/txts/README.`dirname ${readme} | sed -e 's|^modules/||'`
done
rm -f doc/txts/README


%build
aclocal -I m4
libtoolize -f
autoconf
autoheader
automake -a
export ac_cv_lib_ndbm_dbm_store=no \
    ac_cv_lib_db_dbm_store=no \
    ac_cv_lib_selinux_getfilecon=no \
    ac_cv_search_FascistCheck='none required'

CFLAGS="%{optflags} -fPIC" \
%configure \
    --sbindir=/sbin \
    --libdir=/%{_lib} \
    --disable-pwdb \
    --includedir=%{_includedir}/security

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}/security
mkdir -p %{buildroot}/%{_lib}/security
make install DESTDIR=%{buildroot} LDCONFIG=:

mkdir -p %{buildroot}/etc/pam.d
install -m 0644 %{SOURCE2} %{buildroot}/etc/pam.d/other
install -m 0644 %{SOURCE3} %{buildroot}/etc/pam.d/system-auth
chmod 0644 %{buildroot}/etc/pam.d/{other,system-auth}

# Install man pages.
mkdir -p %{buildroot}%{_mandir}/man[358]
install -m 0644 doc/man/*.3 %{buildroot}%{_mandir}/man3/
install -m 0644 doc/man/*.8 %{buildroot}%{_mandir}/man8/

# Make sure every module built.
for dir in modules/pam_* ; do
if [ -d ${dir} ] && [ ${dir} != "modules/pam_selinux" ] && [ ${dir} != "modules/pam_pwdb" ]; then
    if ! ls -1 %{buildroot}/%{_lib}/security/`basename ${dir}`*.so ; then
        echo ERROR `basename ${dir}` did not build a module.
        exit 1
    fi
fi
done

install -m 644 %{SOURCE5} %{buildroot}/etc/security/console.perms.d/50-annvix.perms

#remove unpackaged files
rm -rf %{buildroot}/%{_lib}/*.la \
    %{buildroot}/%{_lib}/security/*.la \
    %{buildroot}%{_prefix}/doc/Linux-PAM \
    %{buildroot}%{_datadir}/doc/pam

touch %{buildroot}%{_sysconfdir}/environment

%find_lang Linux-PAM


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig


%files -f Linux-PAM.lang
%defattr(-,root,root)
%dir /etc/pam.d
%config(noreplace) %{_sysconfdir}/environment
%config(noreplace) /etc/pam.d/other
%config(noreplace) /etc/pam.d/system-auth
%config(noreplace) /etc/security/access.conf
%config(noreplace) /etc/security/chroot.conf
%config(noreplace) /etc/security/time.conf
%config(noreplace) /etc/security/group.conf
%config(noreplace) /etc/security/limits.conf
%config(noreplace) /etc/security/pam_env.conf
%config(noreplace) /etc/security/console.perms
%config(noreplace) /etc/security/console.handlers
%dir %{_sysconfdir}/security/console.perms.d
%config(noreplace) /etc/security/console.perms.d/50-default.perms
%config(noreplace) /etc/security/console.perms.d/50-annvix.perms
/sbin/pam_console_apply
/sbin/pam_tally
%dir /etc/security/console.apps
%attr(4755,root,root) /sbin/pam_timestamp_check
#%attr(4755,root,root) /sbin/unix_chkpwd
%dir /etc/security/console.apps
%dir /var/run/console
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%dir /%{_lib}/security
/%{_lib}/libpam.so.*
/%{_lib}/libpamc.so.*
/%{_lib}/libpam_misc.so.*
/%{_lib}/security/*.so
/%{_lib}/security/pam_filter

%files -n %{libname}-devel
%defattr(-,root,root)
/%{_lib}/libpam.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpamc.so
%{_includedir}/security/*.h
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc CHANGELOG Copyright doc/txts/*


%changelog
* Sat Jul 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.3.0
- don't build pam_{cracklib,debug,postgresok,rps,selinux,unix} modules
- requires pam_tcb (which provides the pam_unix replacement)
- buildrequies: glibc-crypt_blowfish-devel
- no longer require cracklib or pwdb/pwdb-devel
- update the other.pamd and system-auth.pamd to use pam_tcb and pam_passwdqc
- requires: pam_userpass
- requires setup-2.5-5735avx

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.3.0
- rebuild against new db4

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.3.0
- 0.99.3.0
- merge changes from Mandriva, which in turn synced with RH:
  - don't package pwdb_chkpwd
  - package security/chroot.conf
  - package libpamc
  - package language files
  - package new security/console.handlers and security/console.perms.d/
  - drop lots of patches and integrate/update new ones
  - buildrequires: openssl, automake1.8
  - disable pam_pwdb
  - make unix_chkpwd setuid root again
- renumber patches
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.77
- Clean rebuild

* Mon Jan 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.77
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.77-22avx
- P515 (flepied)

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.77-21avx
- sync with mandrake 0.77-30mdk:
  - don't apply the P38 (fix mdk bug #16961, su segfault on x86_64)
    (couriousous)
  - fix requires (flepied)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.77-20avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.77-19avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.77-18avx
- bootstrap build

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.77-17avx
- revert the pam.d/{other,system-auth} changes that crept in from mdk
  packages

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.77-16avx
- include some documentation on the various modules
- rebuild against new glib

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.77-15avx
- sync with Mandrake 0.77-25mdk:
  - console.perms: /proc/usb -> /proc/bus/usb (Marcel Pol)
    [bug #8285] (flepied)
  - updated P16 to give console perms to rfcomm devices (fcrozat)
  - manage dri file perms [bug #10876] (flepied)
  - manage perms of /dev/raw1394 [bug #9240] (flepied)
  - console.perms more group friendly [bug #3033] (flepied)
  - merged with rh 0.77-54 (flepied) - without SELINUX support
  - put back <serial> group in console.perms (flepied)
  - added /dev/rfcomm* /dev/ircomm* to serial group (Fred Crozat)
    (flepied)
  - fixed lookup when a group or a user doesn't exist [bug #11256]
    (flepied)
  - add sr* to cdrom group (fcrozat)
  - implement pam_console_setowner for udev (flepied)    
  - fixed debug code in pam_console_apply_devfsd (flepied)
  - added a way to debug pam_console_setowner by setting PAM_DEBUG
    env variable (flepied)
  - build pam_console_apply_devfs aainst glib-1.2 (gbeauchesne)
  - pam_env: don't abort if /etc/environment isn't present (Oded Arbel)
    (flepied)
  - create an empty /etc/environment (flepied)
- remove selinux-related bits from P40 and likewise drop the
  pam-0.77-closefd.patch which patches against the (unapplied) selinux patch

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.77-14avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.77-13sls
- minor spec cleanups

* Fri Feb 06 2004 Vincent Danen <vdanen@opensls.org> 0.77-12sls
- remove %%build_opensls macro
- fix pam_console config for our removed groups (P600)
- don't add group video here

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.77-11sls
- sync with 10mdk (flepied): libification

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 0.77-10sls
- OpenSLS build
- tidy spec
- don't build doc for %%build_opensls
- put BuildReq on linuxdoc-tools for the doc package

* Mon Sep  1 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.77-9mdk
- added a prereq on rpm-helper

* Wed Aug 27 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.77-8mdk
- added video group in %%pre

* Mon Aug 25 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.77-7mdk
- fixed patch512 to use the right way to initialize the supplementary groups

* Mon Aug 25 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.77-6mdk
- make pam_xauth works in high security levels (patch512)
- added rtc to console.perms in v4l group
- make pam_limits more verbose (patch511)

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.77-5mdk
- BuildRequires: db4-devel >= 4.0.14

* Fri Jul 18 2003 Warly <warly@mandrakesoft.com> 0.77-4mdk
- remove cracklib requires (should autoreq libcrack)

* Thu Jul 17 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.77-3mdk
- patch 510: support kernel*2.5.x

* Sat Jul 12 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.77-2mdk
- fixed pam_console_apply_devfsd.so link

* Thu Jul 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.77-1mdk
- merged 0.77

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 0.75-34mdk
- Rebuild

* Fri May 23 2003 Götz Waschk <waschk@linux-mandrake.com> 0.75-33mdk
- rebuild for devel provides

* Tue Apr  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.75-32mdk
- Patch509: Handle biarch struct utmp

* Tue Apr  8 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.75-31mdk
- rebuild for libdb4.0

* Fri Feb 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.75-30mdk
- updated patch0 for scanner support

* Thu Dec 12 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.75-29mdk
- Patch509: don't complain when / is owned by root.adm

* Thu Nov 14 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.75-28mdk
- Add missing pam_timestamp_check 

* Fri Oct 25 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-27mdk
- correct pam_time to work with non tty services like ftp.

* Mon Sep 30 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.75-26mdk
- Patch506: Make it lib64-aware when looking for cracklib dictionaries

* Thu Sep  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-25mdk
- correct pam_xauth to work with ssh X forwarding too

* Tue Sep  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-24mdk
- corrected path for ttyUSB*

* Wed Aug 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-23mdk
- pam_console_apply: corrected buggy error reporting
- pam_console: reset to id 0 if user/group isn't found instead of
stopping processing.

* Mon Aug 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-22mdk
- merge with rh 0.75-40

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.75-21mdk
- rpmlint fixes: configure-without-libdir-spec, hardcoded-library-path

* Sun Mar  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-20mdk
- really apply patch to reduce number of access to /etc/{passwd,group}
(Andrej).

* Tue Feb 26 2002 Pixel <pixel@mandrakesoft.com> 0.75-19mdk
- add /dev/rdvd in group cdrom (modified patch pam-0.75-mdkconf.patch.bz2)
  (rdvd is meant to be a symlink to a raw/raw<n>)

* Thu Feb 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.75-18mdk
- Fix leak in devfsd patch (Andrej).

* Mon Feb 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-17mdk
- updated patch503 to try to supermount triggering as much as possible and
/var/lock -> /var/run. (Andrej)
- console.perms: /dev/sequencer* (Andrej)

* Sat Feb  2 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-16mdk
- updated devfsd patch and BuildRequires (Andrej)

* Fri Feb  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.75-15mdk
- resync with rh 0.75-21

* Sat Jan 19 2002 David BAUDENS <baudens@mandrakesoft.com> 0.75-14mdk
- Fix Group: for devel package

* Wed Jan 16 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.75-13mdk
- Player play again compile pam_console_apply_devfsd statically.

* Wed Jan 16 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.75-12mdk
- Revert my morning crack.

* Wed Jan 16 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.75-11mdk
- Don't compile pam_console_apply_devfsd with libglib (it's /usr based).

* Wed Jan 16 2002 David BAUDENS <baudens@mandrakesoft.com> 0.75-10mdk
- Clean after build
- Fix Requires:

* Thu Nov 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.75-9mdk
- apply patch from Andrej Borsenkow to build a pam_console_apply_devfsd.so

* Fri Oct 05 2001 Stefan van der Eijk <stefan@eijk.nu> 0.75-8mdk
- BuildRequires: db2-devel db3-devel

* Mon Sep 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.75-7mdk
- fix pam_console when the X server disapear before the session is closed.

* Fri Jul 20 2001 Pixel <pixel@mandrakesoft.com> 0.75-6mdk
- rebuild with new glibc that works

* Thu Jul 19 2001  Daouda Lo <daouda@mandrakesoft.com> 0.75-5mdk
- workaround -> symlink soname a la mano until glibc/ldconfig fix 

* Wed Jul 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.75-4mdk
- Resync with redhat pam 0.75-5 : remove patch 3 (merged)

* Tue Jul  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.75-3mdk
- recompiled for db3.2

* Tue Jun 26 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.75-2mdk
- Patch 3 : fix pam_console

* Wed Jun 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.75-1mdk
- 0.75
- added devel man pages to devel package

* Wed May 16 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.74-7mdk
- changed ttyS* group owner from uucp to tty (thanks to ygingras@eclipsys.qc.ca)

* Thu Apr 12 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.74-6mdk
- Add usb to console permission file

* Thu Apr  5 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.74-5mdk
- applied patch from Debian on pam_mkhomedir module 
  (thanks to Christian Zoffoli)

* Thu Mar 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.74-4mdk
- fix infinite loop

* Wed Mar 14 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 0.74-3mdk
- removed "account required /lib/security/pam_access.so" entry
  in system-auth to get imap-2000 working.
- added pam_tally and pam_console_apply in /sbin.

* Mon Mar 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.74-2mdk
- 0.74-17 from rh.

* Mon Feb 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.74-1mdk
- 0.74.

* Sat Dec 16 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.72-14mdk
- security fix for localuser module

* Mon Dec 11 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 0.72-13mdk
- fix build with db1
- fix some rpmlint warnings

* Mon Oct  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.72-12mdk
- added glib-devel bison flex BuildRequires.

* Mon Sep 25 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.72-11mdk
- include system-auth (chmou sucks).

* Sun Sep 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.72-10mdk
- Sync with last rh pam :
		- add a broken_shadow option to pam_unix
		- fix pam_stack debug and losing-track-of-the-result bug
		- rework pam_console's usage of syslog to actually be sane (#14646)
		- take the LOG_ERR flag off of some of pam_console's 

* Tue Sep 19 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.72-9mdk
- noreplace.
- resync console.perms with the dev package.

* Mon Sep  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.72-8mdk
- Add cdburner permission.
- Set all sound stuff to audio group.

* Sat Jul 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.72-7mdk
- Merge with latest RH changes (security fixes).

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.72-6mdk
- Merge with last RH changes.
- BM.

* Thu May 18 2000 Pixel <pixel@mandrakesoft.com> 0.72-5mdk
- fix add .so.0

* Thu May 18 2000 Pixel <pixel@mandrakesoft.com> 0.72-4mdk
- add .so.0
- create -devel
- move more doc to -doc

* Thu Apr 27 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.72-3mdk
- added a BuildRequires on pwdb-devel and cracklib-devel

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 0.72-2mdk
- new group
- only keep html doc in main package. ps & txt moved to -doc

* Sun Feb 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.72-1mdk
- 0.72. 
- Clean up %files section.

* Fri Jan 28 2000 Francis Galiegue <francis@mandrakesoft.com> 0.68-4mdk

- Fixed wrong user id for /sbin/pwdb_chkpwd

* Tue Jan 11 2000 Pixel <pixel@mandrakesoft.com>
- fix build as non-root

* Tue Jan  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.68-2mdk
- don't allow '/'/ on service_name (rh).

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.68.

* Wed Jul  7 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- return audio devices to pam control

* Thu Jun 01 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Local user audio "hack" we no longer modify audio device permissions

* Sun May  2 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Fix compilation on systems that don't have pam headers installed already
- Fix a bug (chmod 0755 $FAKEROOT/etc/security/console.apps, not
  /etc/security/console.apps !!!)

* Tue Apr 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adatations.

* Sat Apr 17 1999 Michael K. Johnson <johnsonm@redhat.com>
- added video4linux devices to /etc/security/console.perms

* Fri Apr 16 1999 Michael K. Johnson <johnsonm@redhat.com>
- added joystick lines to /etc/security/console.perms

* Thu Apr 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed a couple segfaults in pam_xauth uncovered by yesterday's fix...

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- use gcc -shared to link the shared libs

* Wed Apr 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- many bug fixes in pam_xauth
- pam_console can now handle broken applications that do not set
  the PAM_TTY item.

* Tue Apr 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed glob/regexp confusion in pam_console, added kbd and fixed fb devices
- added pam_xauth module

* Sat Apr 10 1999 Cristian Gafton <gafton@redhat.com>
- pam_lastlog does wtmp handling now

* Thu Apr 08 1999 Michael K. Johnson <johnsonm@redhat.com>
- added option parsing to pam_console
- added framebuffer devices to default console.perms settings

* Wed Apr 07 1999 Cristian Gafton <gafton@redhat.com>
- fixed empty passwd handling in pam_pwdb

* Mon Mar 29 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed /dev/cdrom default user permissions back to 0600 in console.perms
  because some cdrom players open O_RDWR.

* Fri Mar 26 1999 Michael K. Johnson <johnsonm@redhat.com>
- added /dev/jaz and /dev/zip to console.perms

* Thu Mar 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed the default user permissions for /dev/cdrom to 0400 in console.perms

* Fri Mar 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed a few bugs in pam_console

* Thu Mar 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_console authentication working
- added /etc/security/console.apps directory

* Mon Mar 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- added pam_console files to filelist

* Fri Feb 12 1999 Cristian Gafton <gafton@redhat.com>
- upgraded to 0.66, some source cleanups

* Mon Dec 28 1998 Cristian Gafton <gafton@redhat.com>
- add patch from Savochkin Andrey Vladimirovich <saw@msu.ru> for umask
  security risk

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- upgrade to ver 0.65
- build the package out of internal CVS server

