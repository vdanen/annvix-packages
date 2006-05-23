#
# spec file for package am-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		am-utils
%define version		6.0.9
%define release		%_revrel
%define epoch		3

%define major		2
%define libname		%mklibname amu %{major}

Summary:	Automount utilities including an updated version of Amd
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	BSD
Group:		System/Servers
URL:		http://www.am-utils.org/
Source:		ftp://ftp.am-utils.org/pub/am-utils/%{name}/%{name}-%{version}.tar.bz2
Source1:	am-utils.conf
Source2:	am-utils.net.map
Source3:	amd.run
Source4:	amd-log.run
Source5:	AMDOPTS.env
Source6: 	MOUNTPTS.env
Patch0:		am-utils-6.0.4-nfs3.patch
Patch1:		am-utils-6.0.9-avx-gcc4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison, byacc, flex, gdbm-devel

Requires(pre):	grep
Requires(post):	rpm-helper, info-install
Requires(preun): info-install, rpm-helper
Requires:	portmap, setup >= 2.4-16avx
Obsoletes:	amd
Provides:	amd

%description
Am-utils includes an updated version of Amd, the popular BSD
automounter.  An automounter is a program which maintains a cache of
mounted filesystems.  Filesystems are mounted when they are first
referenced by the user and unmounted after a certain period of inactivity.
Amd supports a variety of filesystems, including NFS, UFS, CD-ROMS and
local drives.  


%package -n %{libname}
Summary:        Shared library files for am-utils
Group:          System/Servers
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Shared library files from the am-utils package.


%package -n %{libname}-devel
Summary:        Development files for am-utils
Group:          Development/C
Requires:       %{libname} = %{epoch}:%{version}
Provides:       libamu-devel

%description -n %{libname}-devel
Development headers, and files for development from the am-utils package.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch -p1
%patch1 -p1 -b .gcc4


%build
%serverbuild
%configure \
    --enable-shared \
    --enable-libs="-lnsl -lresolv" \
    --disable-amq-mount \
    --enable-debug \
    --without-ldap

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sysconfdir}/

install -m 0600 %{SOURCE1} %{buildroot}%{_sysconfdir}/amd.conf
install -m 0640 %{SOURCE2} %{buildroot}%{_sysconfdir}/amd.net

mkdir -p %{buildroot}%{_srvdir}/amd/{log,env,depends} 

install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/amd/run
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/amd/log/run

install -m 0640 %{SOURCE5} %{buildroot}%{_srvdir}/amd/env/AMDOPTS
install -m 0640 %{SOURCE6} %{buildroot}%{_srvdir}/amd/env/MOUNTPTS

%_mkdepends amd portmap

mkdir -p %{buildroot}/.automount

# remove unwanted files
rm -f %{buildroot}%{_sbindir}/ctl-amd
rm -f %{buildroot}/amd.conf
rm -f %{buildroot}/%{_sysconfdir}/*-sample
rm -f %{buildroot}/amd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv amd
%_install_info %{name}.info


%preun
%_preun_srv amd


%postun
%_remove_install_info %{name}.info


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/amd.conf
%config(noreplace) %{_sysconfdir}/amd.net
%dir /.automount
%{_bindir}/pawd
%{_bindir}/expn
%{_sbindir}/*
%{_mandir}/man[58]/*
%{_mandir}/man1/pawd.1*
%{_mandir}/man1/expn.1*
%{_infodir}/*.info*
%dir %attr(0750,root,admin) %{_srvdir}/amd
%dir %attr(0750,root,admin) %{_srvdir}/amd/log
%dir %attr(0750,root,admin) %{_srvdir}/amd/env
%dir %attr(0750,root,admin) %{_srvdir}/amd/depends
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/amd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/amd/log/run
%attr(0640,root,admin) %config(noreplace) %{_srvdir}/amd/env/AMDOPTS
%attr(0640,root,admin) %config(noreplace) %{_srvdir}/amd/env/MOUNTPTS
%attr(0640,root,admin) %{_srvdir}/amd/depends/portmap

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

%files doc
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog NEWS README* scripts/*-sample INSTALL COPYING


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- add -doc subpackage
- rebuild with gcc4
- drop the postscript docs
- remove service log relocation stuff
- P1: fix compilation with gcc4
- fix rpmlint requires-on-release

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-11avx
- quotes in runscript

* Sun Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-10avx
- back down to 6.0.9 due to some very wierd amd behaviour with
  6.1.x
- bump the epoch
- change the logfile from syslog to /dev/stderr in amd.conf

* Sun Sep 25 2005 Sean P. Thomas <vdanen-at-build.annvix.org> 6.1.2.1-1avx
- Converted to env dirs, run script to execlineb, converted 
- dependencies, and upgraded to newest version. 

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1.1-2avx
- s/supervise/service/ in log/run

* Fri Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.1.1-1avx
- 6.1.1
- use execlineb for run scripts
- move logdir to /var/log/service/amd
- run scripts are now considered config giles and are not replaceable


* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-12avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-11avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-10avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.0.9-9avx
- first Annvix build, to replace autofs

* Thu Nov 18 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 6.0.9-8mdk
- clean dep, update for 64bits

* Tue Mar 02 2004 Pascal Terjan <pterjan@mandrake.org> 6.0.9-7mdk
- Fix one more DEP

* Sun Feb 29 2004 Pascal Terjan <pterjan@mandrake.org> 6.0.9-6mdk
- Fix DEP due to Epoch

* Thu Feb 26 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 6.0.9-5mdk
- Fix DEP
- disabling ldap (won't build on klama)

* Fri Aug 08 2003 Buchan Milne <bgmilne@linux-mandrake.com> 6.0.9-4mdk
- Rebuild to lose libsasl7 dependency

* Sun Mar 02 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 6.0.9-3mdk
- jump to -3mdk (seems -2mdk existed in past)

* Sun Mar 02 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 6.0.9-1mdk 
- use %%mklibname
- clean unpackaged files
- reintroduce in contrib (do not understand version mismatch between CVS and this SPEC)
- rpmlint clean up

* Fri Nov  2 2001 Jeff Garzik <flepied@mandrakesoft.com> 6.0.7-1mdk
- New version.
- Add URL.
- Remove manual call to autoconf/aclocal/automake/autoheader, or
  libtool should handle things correctly now.
- Libification: new packages libamu and libamu-devel
- Use make DESTDIR

* Wed Sep 19 2001 Philippe Libat <philippe@mandrakesoft.com> 6.0.6-3mdk
- fix MOUNTPTS in sysconfig/amd

* Thu Sep  6 2001 Vincent Saugey <vince@mandrakesoft.com> 6.0.6-2mdk 
- Rebuild without ldap1 support now use ldap2

* Thu May  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.0.6-1mdk
- 6.0.6.

* Wed Apr  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 6.0.5-4mdk
- use server macros
- noreplace

* Sun Feb 11 2001 Jeff Garzik <flepied@mandrakesoft.com> 6.0.5-3mdk
- spec cleaning

* Mon Feb  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.0.5-2mdk
- Fix initscript for default runlevel.

* Mon Feb  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.0.5-1mdk
- condrestart in %postun.
- Stop the service in %preun.
- Sync the initscripts with the 1.3 from Red Hat.
- Define NFSV3.
- 6.0.5.

* Mon Jan  8 2001  Daouda Lo <daouda@mandrakesoft.com> 6.0.4-5mdk
- reompile against new openldap libs (thanx Luis)

* Sat Nov 11 2000 Jeff Garzik <flepied@mandrakesoft.com> 6.0.4-4mdk
- Rebuild with new gcc/glibc
- Add some more docs to perfect-doc.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 6.0.4-3mdk
- automatically added BuildRequires

* Wed Aug 02 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 6.0.4-2mdk
- BM

* Tue Jul 11 2000 dam's <damien@mandrakesoft.com> 6.0.4-1mdk
- updated.

* Sat Jul 08 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 6.0.3-5mdk
- add makeinstall macro

* Tue Apr 18 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 6.0.3-4mdk
- update group
- compress config files
- include omitted /etc/amd.net

* Sun Feb 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.0.3-3mdk
- --disable-amq-mount by default.
- enhance init script to be more wait4amd2die-like (r).
- make default map type to be file (r).
- get rid of the kludges (r).
- by defaut do rsize=8192,wsize=8192 (jeff).

* Fri Feb 18 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 6.0.3-1mdk
- Various BuildRequires:
- Merge with redhat version.
- 6.0.3
- Clean up specs.
- Prereq: grep.

* Thu Nov 6 1999 Damien Krotkine <damien@mandrakesoft.com>
- Version 6.0.2

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Thu Apr 08 1999 Preston Brown <pbrown@redhat.com>
- kill -HUP on reload, restart does a real restart.

* Fri Mar 26 1999 Bill Nottingham <notting@redhat.com>
- twiddle an echo in initscript

* Tue Mar 23 1999 Cristian Gafton <gafton@redhat.com>
- version 6.0 proper
- Serial:1 because to enforce versioning

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- rebuild for glibc 2.1
- strip all binaries

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- add missing ':' to default 'opts:=nosuid,nodev'
- install info pages

* Mon Jul 13 1998 Cristian Gafton <gafton@redhat.com>
- added the NIS support that the broken configure script failed to detect

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- disabled autofs support on alpha
- run ldconfig in postinstall

* Mon May 04 1998 Cristian Gafton <gafton@redhat.com>
- new package to replace the old and unmaintained amd
