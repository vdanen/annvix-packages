#
# spec file for package cvs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cvs
%define version		1.12.13
%define release		%_revrel

%define _requires_exceptions tcsh

Summary:	A version control system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.cvshome.org/
Source: 	ftp://ftp.cvshome.org/pub/cvs-%{version}/cvs-%{version}.tar.bz2
Source1: 	cvspserver
Source2: 	cvs.conf
Source3: 	ftp://ftp.cvshome.org/pub/cvs-%{version}/cvs-%{version}.tar.bz2.sig
Source4:	cvs.run
Source5:	cvs-log.run
Source6:	06_cvspserver.afterboot
Patch0:		cvs-1.11.19-mdk-varargs.patch
Patch1: 	cvs-1.12.13-errno.patch
Patch2:		cvs-1.11.1-newline.patch
Patch3:		cvs-1.11.4-first-login.patch
Patch4:		cvs-zlib-read.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	texinfo
BuildRequires:	zlib-devel
BuildRequires:	krb5-devel

Requires:	ipsvd
Requires(post):	info-install
Requires(post):	afterboot
Requires(post):	rpm-helper
Requires(post):	ipsvd
Requires(preun): info-install
Requires(preun): rpm-helper
Requires(postun): afterboot

%description
CVS means Concurrent Version System; it is a version control
system which can record the history of your files (usually,
but not always, source code). CVS only stores the differences
between versions, instead of every version of every file
you've ever created. CVS also keeps a log of who, when and
why changes occurred, among other aspects.

CVS is very helpful for managing releases and controlling
the concurrent editing of source files among multiple
authors. Instead of providing version control for a
collection of files in a single directory, CVS provides
version control for a hierarchical collection of
directories consisting of revision controlled files.

These directories and files can then be combined together
to form a software release.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .varargs
%patch1 -p1 -b .errno
%patch2 -p1 -b .newline
%patch3 -p1 -b .first-login
%patch4 -p0 -b .zlib-read


%build
export SENDMAIL="%{_sbindir}/sendmail"

%serverbuild
export CFLAGS="%(echo %optflags | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')"
export CXXFLAGS="${CFLAGS}"
export CCFLAGS="${CFLAGS}"

%configure2_5x --with-tmpdir=/tmp

%make

make -C doc info


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/cvs
install -m 0755 %{_sourcedir}/cvspserver %{buildroot}%{_sbindir}
install -m 0644 %{_sourcedir}/cvs.conf %{buildroot}%{_sysconfdir}/cvs

# get rid of "no -f" so we don't have a Dep on this nonexistant interpretter
perl -pi -e 's/no -f/\/bin\/sh/g' %{buildroot}%{_datadir}/cvs/contrib/sccs2rcs

mkdir -p %{buildroot}%{_srvdir}/cvspserver/{log,peers,env}
install -m 0740 %{_sourcedir}/cvs.run %{buildroot}%{_srvdir}/cvspserver/run
install -m 0740 %{_sourcedir}/cvs-log.run %{buildroot}%{_srvdir}/cvspserver/log/run
touch %{buildroot}%{_srvdir}/cvspserver/peers/0
chmod 0640 %{buildroot}%{_srvdir}/cvspserver/peers/0

echo "2401" >%{buildroot}%{_srvdir}/cvspserver/env/PORT

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/06_cvspserver.afterboot %{buildroot}%{_datadir}/afterboot/06_cvspserver


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv cvspserver
%_install_info %{name}.info
%_install_info cvsclient.info
%_mkafterboot
pushd %{_srvdir}/cvspserver >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd >/dev/null 2>&1


%preun
%_preun_srv cvspserver
%_remove_install_info %{name}.info
%_remove_install_info cvsclient.info


%postun
%_mkafterboot


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/cvs
%config(noreplace) %{_sysconfdir}/cvs/cvs.conf
%{_bindir}/cvs
%{_bindir}/cvsbug
%{_bindir}/rcs2log
%{_sbindir}/cvspserver
%{_mandir}/man1/cvs.1*
%{_mandir}/man5/cvs.5*
%{_mandir}/man8/cvsbug.8*
%{_infodir}/cvs*
%{_datadir}/cvs
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver/log
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver/peers
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver/env
%attr(0740,root,admin) %{_srvdir}/cvspserver/run
%attr(0740,root,admin) %{_srvdir}/cvspserver/log/run
%attr(0640,root,admin) %{_srvdir}/cvspserver/peers/0
%attr(0640,root,admin) %{_srvdir}/cvspserver/env/PORT
%{_datadir}/afterboot/06_cvspserver

%files doc
%defattr(-,root,root)
%doc BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README


%changelog
* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.12.13
- 1.12.13
- renumber patches
- P4: fix hang when using zlib (nanardon)
- spec cleanups

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.11.20 
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.11.20
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.11.20
- Obfuscate email addresses and new tagging
- Uncompress patches

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.20-3avx
- grab defaults from the tcpsvd environment

* Sun Sep 25 2005 Sean P. Thomas <spt-at-build.annvix.org> 1.11.20-2avx
- use execlineb for run script, and created an envdir.
- fix requires (vdanen)
- supplied default env files (vdanen)
- pre-compile a peers.cdb in %%post (vdanen)

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.20-1avx
- 1.11.20
- use execlineb for run scripts
- move logdir to /var/log/service/cvspserver
- run scripts are now considered config files and are not replaceable
- P0: varags fixes for x86_64 (potential, but harmless here) (gbeauchesne)
- drop P13; merged upstream

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-6avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-5avx
- bootstrap build (new gcc, new glibc)
- remove postscript docs

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-4avx
- rebuild

* Thu May 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-3avx
- P13: security fix for CAN-2005-0753

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-2avx
- no need to lose our cvs.conf; put it back

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-1avx
- 1.11.19
- use logger for logging
- remove broken P14 (mdk bug #13118) (flepied)

* Tue Jan 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-5avx
- update the run script; exec tcpsvd so that it will actually stop
  when we want it to
- service name is cvspserver, not cvs

* Tue Oct 05 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-4avx
- switch from tcpserver to tcpsvd
- Requires: ipsvd
- add the /service/cvspserver/peers directory to, by default, allow
  all connections
- add afterboot snippet

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-3avx
- updated run scripts

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-2avx
- Annvix build
- require packages not files

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 1.11.17-1sls
- 1.11.17 (security fixes for CAN-2004-0414, CAN-2004-0146, CAN-2004-0417,
  CAN-2004-0418, CAN-2004-0396)
- update P6, P14
- personalize cvs.conf

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 1.11.11-1sls
- 1.11.11
- remove %%build_opensls macro
- supervise macros
- minor spec cleanups
- use %%_post_srv and %%_preun_srv
- merge with 1.11.11-1mdk:
  - DIRM: /etc/cvs (flepied)
  - add localid patch to be able to access xfree86 cvs repository cleanly
    (flepied)

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.11.10-2sls
- put supervise run scripts in if %%build_opensls; remove xinetd support

* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 1.11.10-1sls
- OpenSLS build
- tidy spec
- pass tmpdir to configure
- fix a sccs2rcs script in contrib scripts which was making a Req on "no"
