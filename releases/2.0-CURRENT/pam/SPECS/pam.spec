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
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	db4-devel
BuildRequires:	automake1.8
BuildRequires:	openssl-devel

Requires:	glibc-crypt_blowfish-devel
# pam_unix is now provided by pam_tcb
Requires:	pam_tcb
Requires:	pam_passwdqc
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
install -m 0644 %{_sourcedir}/other.pamd %{buildroot}/etc/pam.d/other
install -m 0644 %{_sourcedir}/system-auth.pamd %{buildroot}/etc/pam.d/system-auth
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

install -m 0644 %{_sourcedir}/pam-annvix.perms %{buildroot}/etc/security/console.perms.d/50-annvix.perms

#remove unpackaged files
rm -rf %{buildroot}/%{_lib}/*.la \
    %{buildroot}/%{_lib}/security/*.la \
    %{buildroot}%{_prefix}/doc/Linux-PAM \
    %{buildroot}%{_datadir}/doc/pam

touch %{buildroot}%{_sysconfdir}/environment

%kill_lang Linux-PAM
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
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.3.0
- remove locales

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.3.0
- rebuild against new glib2.0

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.3.0
- rebuild against new openssl 
- spec cleanups

* Thu Aug 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.3.0
- make the serial ownership root:admin
- spec cleanups

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
