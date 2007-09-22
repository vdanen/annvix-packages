#
# spec file for package pam
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# pam-0.99.6.3-1mdv
#
# $Id$

%define revision	$Rev$
%define name		pam
%define version		0.99.8.1
%define release		%_revrel

%define pam_redhat_version 0.99.8-1 

%define libname		%mklibname %{name} 0
%define devname		%mklibname %{name} -d

Summary:	A security tool which provides authentication for applications
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or BSD
Group:		System/Libraries
URL:		http://www.us.kernel.org/pub/linux/libs/pam/index.html
Source0:	ftp://ftp.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%{version}.tar.bz2
Source1:	ftp://ftp.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%{version}.tar.bz2.sign
Source2:	pam-redhat-%{pam_redhat_version}.tar.bz2
Source3:	other.pamd
Source4:	system-auth.pamd
Source5:	pam-annvix.perms
Source6:	config-util.pamd
Source7:	dlopen.sh

Patch0:		pam-0.99.7.0-redhat-modules.patch
Patch1:		pam-0.99.7.1-rh-unix-hpux-aging.patch
Patch2:		pam-0.99.8.1-rh-unix-update-helper.patch
Patch3:		pam-0.99.3.0-rh-tally-fail-close.patch
Patch4:		pam-0.99.7.1-rh-namespace-temp-logon.patch
Patch5:		pam-0.99.8.1-fdr-audit-no-log.patch
Patch6:		pam-0.99.8.1-fdr-namespace-init.patch
Patch7:		pam-0.99.7.1-rh-namespace-homedir.patch
Patch8:		Linux-PAM-0.99.8.1-mdvclasses.patch
Patch9:		Linux-PAM-0.99.8.1-mdvgroups.patch
Patch10:	pam-0.74-mdv-loop.patch
Patch11:	Linux-PAM-0.99.3.0-mdv-pamtimestampadm.patch
Patch12:	Linux-PAM-0.99.3.0-mdv-verbose-limits.patch
Patch13:	Linux-PAM-0.99.3.0-mdv-xauth-groups.patch
Patch14:	Linux-PAM-0.99.6.3-mdv-enable_rt.patch
Patch15:	Linux-PAM-0.99.3.0-mdv-pbuild-rh.patch
Patch16:	pam-0.99.8.1-avx-annvix-perms.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	db4-devel
BuildRequires:	automake1.8
BuildRequires:	openssl-devel
BuildRequires:	glibc-crypt_blowfish-devel
BuildRequires:	audit-devel

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
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the libraries for %{name}


%package -n %{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{devname}
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
%setup -q -n Linux-PAM-%{version} -a 2
# (RH)
%patch0 -p1 -b .redhat-modules
%patch5 -p1 -b .no-log
%patch2 -p1 -b .update-helper
%patch1 -p1 -b .unix-hpux-aging
%patch3 -p1 -b .fail-close
%patch4 -p1 -b .temp-logon
%patch6 -p1 -b .ns-init
%patch7 -p1 -b .ns-homedir 
%patch8 -p1 -b .mdvclasses
%patch9 -p1 -b .mdvgroups
# (blino) make sure devices are accessible by their group if specified
perl -pi.660 -e 's/0600/0660/g if m|\broot\.| && !m|\B/dev/console\b|' modules/pam_console/50-default.perms
%patch10 -p1 -b .loop
%patch11 -p1 -b .pamtimestampadm
%patch12 -p1 -b .verbose-limits
%patch13 -p1 -b .xauth-groups
%patch14 -p1 -b .enable_rt
%patch15 -p1 -b .pbuild-rh
%patch16 -p1 -b .avxperms

# Remove unwanted modules.
for d in pam_{cracklib,debug,postgresok,rps,selinux,unix}; do
    rm -r modules/$d
    sed -i "s,modules/$d/Makefile,," configure.in
    sed -i "s/ $d / /" modules/Makefile.am
done
find modules -type f -name Makefile -delete -print

mkdir -p doc/txts
for readme in modules/pam_*/README ; do
    cp -f ${readme} doc/txts/README.`dirname ${readme} | sed -e 's|^modules/||'`
done
rm -f doc/txts/README

autoreconf


%build
CFLAGS="%{optflags} -fPIC -I%{_includedir}/db4" \
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

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{_sourcedir}/other.pamd %{buildroot}%{_sysconfdir}/pam.d/other
install -m 0644 %{_sourcedir}/system-auth.pamd %{buildroot}%{_sysconfdir}/pam.d/system-auth
install -m 0644 %{_sourcedir}/config-util.pamd %{buildroot}%{_sysconfdir}/pam.d/config-util
install -m 0600 /dev/null %{buildroot}%{_sysconfdir}/security/opasswd

# Install man pages.
mkdir -p %{buildroot}%{_mandir}/man[358]
install -m 0644 doc/man/*.3 %{buildroot}%{_mandir}/man3/
install -m 0644 doc/man/*.8 %{buildroot}%{_mandir}/man8/

install -m 0644 %{_sourcedir}/pam-annvix.perms %{buildroot}%{_sysconfdir}/security/console.perms.d/50-annvix.perms

mkdir -p %{buildroot}/var/log
install -m 0600 /dev/null %{buildroot}/var/log/faillog
install -m 0600 /dev/null %{buildroot}/var/log/tallylog

#remove unpackaged files
rm -rf %{buildroot}/%{_lib}/*.la \
    %{buildroot}/%{_lib}/security/*.la \
    %{buildroot}%{_datadir}/doc/Linux-PAM \
    %{buildroot}%{_datadir}/doc/pam


%kill_lang Linux-PAM
%find_lang Linux-PAM


%check
# Make sure every module built.
for dir in modules/pam_* ; do
if [ -d ${dir} ] && [ ${dir} != "modules/pam_selinux" ] && [ ${dir} != "modules/pam_pwdb" ]; then
    if ! ls -1 %{buildroot}/%{_lib}/security/`basename ${dir}`*.so ; then
        echo ERROR `basename ${dir}` did not build a module.
        exit 1
    fi
fi
done

# Check for module problems.  Specifically, check that every module we just
# installed can actually be loaded by a minimal PAM-aware application.
/sbin/ldconfig -n %{buildroot}/%{_lib}
for module in %{buildroot}/%{_lib}/security/pam*.so ; do
    if ! env LD_LIBRARY_PATH=%{buildroot}/%{_lib} %{_sourcedir}/dlopen.sh -ldl -lpam -L%{buildroot}/%{_lib} ${module} ; then
        echo ERROR module: ${module} cannot be loaded.
        exit 1
    fi
    # And for good measure, make sure that none of the modules pull in threading
    # libraries, which if loaded in a non-threaded application, can cause Very
    # Bad Things to happen.
    if env LD_LIBRARY_PATH=%{buildroot}/%{_lib} LD_PRELOAD=%{buildroot}/%{_lib}/libpam.so ldd -r ${module} | fgrep -q libpthread ; then
        echo ERROR module: ${module} pulls threading libraries.
        exit 1
    fi
done



%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post
if [ ! -a /var/log/faillog ]; then
    install -m 0600 /dev/null /var/log/faillog
fi
if [ ! -a /var/log/tallylog ]; then
    install -m 0600 /dev/null /var/log/tallylog
fi


%files -f Linux-PAM.lang
%defattr(-,root,root)
%dir %{_sysconfdir}/pam.d
%config(noreplace) %{_sysconfdir}/environment
%config(noreplace) %{_sysconfdir}/pam.d/config-util
%config(noreplace) %{_sysconfdir}/pam.d/other
%config(noreplace) %{_sysconfdir}/pam.d/system-auth
%config(noreplace) %{_sysconfdir}/security/access.conf
%config(noreplace) %{_sysconfdir}/security/chroot.conf
%config(noreplace) %{_sysconfdir}/security/group.conf
%config(noreplace) %{_sysconfdir}/security/limits.conf
%config(noreplace) %{_sysconfdir}/security/namespace.conf
%config(noreplace) %{_sysconfdir}/security/opasswd
%config(noreplace) %{_sysconfdir}/security/time.conf
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/security/namespace.init
%config(noreplace) %{_sysconfdir}/security/pam_env.conf
%config(noreplace) %{_sysconfdir}/security/console.perms
%config(noreplace) %{_sysconfdir}/security/console.handlers
%dir %{_sysconfdir}/security/console.perms.d
%config(noreplace) %{_sysconfdir}/security/console.perms.d/50-default.perms
%config(noreplace) %{_sysconfdir}/security/console.perms.d/50-annvix.perms
/sbin/pam_console_apply
/sbin/pam_tally
/sbin/pam_tally2
%attr(4755,root,root) /sbin/pam_timestamp_check
%dir %{_sysconfdir}/security/console.apps
%dir /var/run/console
%ghost %verify(not md5 size mtime) /var/log/faillog
%ghost %verify(not md5 size mtime) /var/log/tallylog
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

%files -n %{devname}
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
* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.99.8.1
- 0.99.8.1
- pam-redhat 0.99.8-1
- updated P0, P1
- new P2, P3, P4 from redhat
- P5: don't log an audit error when uid !=0 (from Fedora)
- P6: add user and new instance parameter to namespace init (from Fedora)
- P7: fix homedir init with namespace module (RH)
- new P8, P9 from Mandriva (split old P100 into two patches)
- updated P16 (old P200)
- add config-util pam config
- add gpg signature
- add buildreq on audit-devel
- include /var/log/{faillog,tallylog} as ghosts and create them in post script
- put the checks in %%check and add more module checks from Fedora (using new S8)
- add the /etc/security/opasswd file
- drop the upgrading README
- renumber patches and rename patches
- build the namespace module

* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.99.6.3
- implement library provides policy

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.99.6.3
- update P106 to remove the @audio group
- remove unnecessary conflicts
- implement devel naming policy
- fix buildreq on glibc-crypt_blowfish-devel

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.6.3
- 0.99.6.3
- rediff P200
- don't include pam_namespace right now; for some reason it's not even trying
  to compile
- sync with Mandriva 0.99.6.3-1mdv
  - P0: updated from upstream
  - P100: updated from Mandriva
  - drop P2, P102, P107, P108, P110, P111, P112

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
