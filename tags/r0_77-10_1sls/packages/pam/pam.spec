%define name	pam
%define version	0.77
%define release	10.1sls

%define rhrelease	1
%define db_version	4.1.25

Summary:	A security tool which provides authentication for applications.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or BSD
Group:		System/Libraries
URL:		http://www.us.kernel.org/pub/linux/libs/pam/index.html
Source:		ftp.us.kernel.org:/pub/linux/libs/pam/pre/library/Linux-PAM-%{version}.tar.bz2
Source1:	pam-redhat-%{version}-%{rhrelease}.tar.bz2
Source2:	other.pamd
Source3:	system-auth.pamd
Source4:	install-sh
# From SUSE
Source10:	ftp://ftp.suse.com/pub/people/kukuk/pam/pam_unix2/pam_unix2-1.18.tar.bz2
Source11:	ftp://ftp.suse.com/pub/people/kukuk/pam/pam_pwcheck/pam_pwcheck-2.4.tar.bz2
Source12:	pam_homecheck-1.3.tar.bz2
Source14:	pam_make-0.1.tar.bz2
Source15:	http://www.openwall.com/pam/modules/pam_passwdqc/pam_passwdqc-0.7.3.tar.bz2
Source16:	http://www.openwall.com/pam/modules/pam_userpass/pam_userpass-0.5.1.tar.bz2
Source17:	http://www.openwall.com/pam/modules/pam_mktemp/pam_mktemp-0.2.4.tar.bz2
Source20:	README.blowfish
Source21:	README.cracklib
Source22:	README.md5
Source24:	unix2_chkpwd.c
Source25:	unix_chkpwd.8
Source26:	unix2_chkpwd.8
Patch0:		pam-0.77-modutil-thread.patch.bz2
Patch1:		pam-0.77-include_path.patch.bz2
Patch2:		pam-0.77-build.patch.bz2
Patch3:		pam-0.75-linkage.patch.bz2
Patch4:		pam-0.75-prompt.patch.bz2
Patch5:		pam-0.75-return.patch.bz2
Patch6:		pam-0.75-security.patch.bz2
Patch7:		pam-0.77-string.patch.bz2
Patch8:		pam-0.77-userdb.patch.bz2
Patch9:		pam-0.75-group-reinit.patch.bz2
Patch10:	pam-0.77-lastlog-utmp.patch.bz2
Patch11:	pam-0.77-securetty-fail.patch.bz2
Patch12:	pam-0.75-time.patch.bz2
Patch13:	pam-0.77-issue.patch.bz2
Patch14:	pam-0.77-doc-rhl.patch.bz2
Patch15:	pam-0.77-bigcrypt-main.patch.bz2
Patch16:	pam-0.77-cracklib-init.patch.bz2
Patch17:	pam-0.77-filter-comments.patch.bz2
Patch18:	pam-0.75-unix-loop.patch.bz2
Patch19:	pam-0.77-unix-preserve.patch.bz2
Patch20:	pam-0.77-unix-brokenshadow.patch.bz2
Patch21:	pam-0.77-unix-hpux-aging.patch.bz2
Patch22:	pam-0.77-unix-nis.patch.bz2
Patch23:	pam-0.77-unix-nullok.patch.bz2
Patch24:	pam-0.77-issue-heap.patch.bz2
Patch25:	pam-0.75-listfile-tty.patch.bz2
Patch26:	pam-0.77-misc-err.patch.bz2
Patch27:	pam-0.77-unix-aixhash.patch.bz2
Patch28:	pam-0.75-sgml2latex.patch.bz2
Patch29:	pam-0.77-multicrack.patch.bz2
Patch30:	pam-0.75-isa.patch.bz2
Patch31:	pam-0.77-utmp-dev.patch.bz2
Patch32:	pam-0.77-pwdb-static.patch.bz2
Patch33:	pam-0.77-nss-reentrant.patch.bz2
Patch34:	pam-0.77-dbpam.patch.bz2

Patch500:	pam-0.77-mdkconf.patch.bz2
Patch501:	pam-0.74-loop.patch.bz2
Patch502:	pam-0.75-console-dead-x.patch.bz2
Patch503:	pam-0.77-devfsd.patch.bz2
Patch504:	pam-0.77-console-reset.patch.bz2
Patch506:	pam-0.77-lib64.patch.bz2
patch507:	pam-0.75-time-tty.patch.bz2
# (fc) 0.75-29mdk don't complain when / is owned by root.adm
Patch508:	Linux-PAM-0.75-pamtimestampadm.patch.bz2
Patch509:	pam-0.75-biarch-utmp.patch.bz2
Patch510:	pam-0.77-sigchld.patch.bz2
Patch511:	pam-0.77-verbose-limits.patch.bz2
Patch512:	pam-0.77-xauth-groups.patch.bz2

# From SUSE:
Patch600:	pam_unix2.dif
Patch602:	pam_make-0.1.dif
Patch603:	pam_passwdqc-0.7.3.dif
Patch604:	pam_userpass-0.5.1.dif
Patch605:	pam_mktemp-0.2.4.dif

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	bison cracklib-devel flex db4-devel libxcrypt-devel

Requires:	cracklib-dicts, initscripts >= 3.94
PreReq:		rpm-helper
Obsoletes:	pamconfig
Provides:	pamconfig

%description
PAM (Pluggable Authentication Modules) is a system security tool
which allows system administrators to set authentication policy
without having to recompile programs which do authentication.

%package devel
Summary:	Development headers and libraries for %{name}
Group:		Development/Other
PreReq:		%{name} = %version-%release

%description devel
PAM (Pluggable Authentication Modules) is a system security tool
which allows system administrators to set authentication policy
without having to recompile programs which do authentication.

This is the devlopement librairies for %{name}

%prep
%setup -q -n Linux-PAM-%{version} -a 1 -a 10 -a 11 -a 12 -a 14 -a 15 -a 16 -a 17
cp %{SOURCE4} .

%patch0  -p1 -b .modutil-thread
%patch1  -p1 -b .include_path
%patch2  -p1 -b .build
%patch3  -p1 -b .linkage
%patch4  -p1 -b .prompt
%patch5  -p1 -b .return
%patch6  -p1 -b .security
%patch7  -p1 -b .string
%patch8  -p1 -b .userdb
%patch9  -p1 -b .group-reinit
%patch10 -p1 -b .lastlog-utmp
%patch11 -p1 -b .securetty-fail
%patch12 -p1 -b .time
%patch13 -p1 -b .issue
%patch14 -p1 -b .doc-rhl
%patch15 -p1 -b .bigcrypt-main
%patch16 -p1 -b .cracklib-init
%patch17 -p1 -b .filter-comments
%patch18 -p1 -b .unix-loop
%patch19 -p1 -b .unix-preserve
%patch20 -p1 -b .unix-brokenshadow
%patch21 -p1 -b .unix-hpux-aging
%patch22 -p1 -b .unix-nis
%patch23 -p1 -b .unix-nullok
%patch24 -p1 -b .issue-heap
%patch25 -p1 -b .listfile-tty
%patch26 -p1 -b .misc-err
%patch27 -p1 -b .unix-aixhash
%patch28 -p1 -b .doc
%patch29 -p1 -b .multicrack
%patch30 -p1 -b .isa
%patch31 -p1 -b .utmp-dev
#%patch32 -p1 -b .pwdb-static
%patch33 -p1 -b .nss-reentrant
%patch34 -p1 -b .dbpam

%patch500 -p1 -b .mdkconf
%patch501 -p1 -b .loop
%patch502 -p1 -b .dead-x
%patch503 -p1 -b .devfsd
%patch504 -p1 -b .console-reset
%patch506 -p1 -b .lib64
%patch507 -p1 -b .time-tty
%patch508 -p1 -b .pamtimestampadm
%patch509 -p1 -b .biarch-utmp
%patch510 -p1 -b .kernel25x
%patch511 -p1 -b .verbose-limits
%patch512 -p1 -b .xauth-groups

pushd pam_unix2-*
%patch600 -p0 -b .pam_unix2
popd
pushd pam_make-*
%patch602 -p0 -b .pam_make
popd
pushd pam_passwdqc-*
%patch603 -p0 -b .pam_passwdqc
popd
pushd pam_userpass-*
%patch604 -p0 -b .pam_userpass
popd
pushd pam_mktemp-*
%patch605 -p0 -b .pam_mktemp
popd

for readme in modules/pam_*/README ; do
	cp -fv ${readme} doc/txts/README.`dirname ${readme} | sed -e 's|^modules/||'`
done
autoconf

%build
# get rid of modules we don't want from here
rm -rf modules/pam_{console,pwdb,radius}

CFLAGS="$RPM_OPT_FLAGS -fPIC" \
./configure \
	--prefix=/ \
	--libdir=/%{_lib} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--enable-static-libpam \
	--enable-securedir=/%{_lib}/security \
	--enable-fakeroot=$RPM_BUILD_ROOT
# %%make doesn't work
make

# extra modules
cd $RPM_BUILD_DIR/Linux-PAM-%{version}
for i in pam_* ; do
  cd $i;
  if [ -x configure ] ; then
    CFLAGS="$RPM_OPT_FLAGS -fPIC" \
      ./configure --prefix=/ --libdir=/%{_lib} --infodir=%{_infodir} \
      --mandir=%{_mandir} --enable-static-libpam --enable-securedir=/%{_lib}/security \
      --enable-fakeroot=$RPM_BUILD_ROOT
    make
  else
     make CFLAGS="$RPM_OPT_FLAGS -fPIC -DHAVE_SHADOW -DLINUX_PAM"
  fi
  cd ..
done

gcc -o $RPM_BUILD_DIR/unix2_chkpwd $RPM_OPT_FLAGS %{SOURCE24} -lpam


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}/security
mkdir -p $RPM_BUILD_ROOT/%{_lib}/security
make install FAKEROOT=$RPM_BUILD_ROOT LDCONFIG=:
install -d -m 755 $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/other
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/system-auth
chmod 644 $RPM_BUILD_ROOT/etc/pam.d/{other,system-auth}

# Install man pages.
install -d -m 755 $RPM_BUILD_ROOT/%{_mandir}/man3
install -d -m 755 $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 doc/man/*.3 $RPM_BUILD_ROOT%{_mandir}/man3/
install -m 644 doc/man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

# Make sure every module built.
for dir in modules/pam_* ; do
if [ -d ${dir} ] ; then
	if ! ls -1 $RPM_BUILD_ROOT/%{_lib}/security/`basename ${dir}`*.so ; then
		echo ERROR `basename ${dir}` module did not build.
		exit 1
	fi
fi
done

# install the extra modules
install -m 0755 $RPM_BUILD_DIR/unix2_chkpwd $RPM_BUILD_ROOT/sbin
for i in pam_* ; do
  cd $i
  make DESTDIR=$RPM_BUILD_ROOT install
  cd ..
done

# remove pam_unix.so and make a hardlink to pam_unix2.so
rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_unix.so
ln -f $RPM_BUILD_ROOT/%{_lib}/security/pam_unix2.so $RPM_BUILD_ROOT/%{_lib}/security/pam_unix.so

# install some README's
mkdir modules-doc
for i in pam_*/README ; do
  cp -fpv ${i} modules-doc/README.`dirname ${i}`
done
cd modules
for i in pam_*/README ; do
  cp -fpv ${i} ../modules-doc/README.`dirname ${i}`
done
cd ..
cp %{SOURCE20} modules-doc
cp %{SOURCE21} modules-doc
cp %{SOURCE22} modules-doc

# the extra manpages
install -m 0644 %{SOURCE25} $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 0644 %{SOURCE26} $RPM_BUILD_ROOT%{_mandir}/man8/

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT/%{_lib}/libpam{.a,c.*} \
  $RPM_BUILD_ROOT/%{_lib}/security/pam_filter/upperLOWER \
  $RPM_BUILD_ROOT%{_sysconfdir}/security/chroot.conf \
  $RPM_BUILD_ROOT%{_prefix}/doc/Linux-PAM \
  $RPM_BUILD_ROOT%{_datadir}/doc/pam \
  $RPM_BUILD_ROOT%{_initrddir}/boot.restore_permissions

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_groupadd video

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc modules-doc/*
%dir /etc/pam.d
%config(noreplace) /etc/pam.d/other
%config(noreplace) /etc/pam.d/system-auth
%config(noreplace) /etc/security/access.conf
%config(noreplace) /etc/security/time.conf
%config(noreplace) /etc/security/group.conf
%config(noreplace) /etc/security/limits.conf
%config(noreplace) /etc/security/pam_env.conf
%config(noreplace) /etc/security/pam_pwcheck.conf
%config(noreplace) /etc/security/pam_unix2.conf
/%{_lib}/libpam.so.*
/%{_lib}/libpam_misc.so.*
#%attr(4755,root,root) /sbin/pwdb_chkpwd
/sbin/unix_chkpwd
/sbin/pam_tally
/sbin/pam_timestamp_check
/sbin/unix2_chkpwd
%dir /%{_lib}/security
/%{_lib}/security/*.so
%{_mandir}/man8/*

%files devel
%defattr(-,root,root)
%doc Copyright
/%{_lib}/libpam.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpam_misc.a
%{_includedir}/security/*.h
%{_mandir}/man3/*

%changelog
* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.77-10.1sls
- remove glib-devel and pwdb/pwdb-devel BuildReq/Req's
- don't apply P32 (pwdb-static.patch)
- remove %%build_opensls macros... this one is OpenSLS-specific
- don't build pam_console
- don't build pam_pwdb
- don't build pam_radius (requires pwdb)
- BuildRequires: libxcrypt-devel
- new modules based on SUSE pam-modules: pam_unix2, pam_pwcheck,
  pam_homecheck, pam_make
- new owl modules: pam_passwdqc, pam_userpass, pam_mktemp

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

