#
# spec file for package rsync
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rsync
%define version		2.6.9
%define release		%_revrel

Summary:	A program for synchronizing files over a network
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/File Transfer
URL:		http://rsync.samba.org/
Source:		http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz
Source1:	rsync.html
Source2:	rsyncd.conf.html
Source4:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz.asc
Source5:	rsync.run
Source6:	rsync-log.run
Source7:	07_rsync.afterboot

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	popt-devel
BuildRequires:	acl
BuildRequires:	libacl-devel

Requires:	ipsvd
Requires(post):	afterboot
Requires(post):	rpm-helper
Requires(post):	ipsvd
Requires(postun): afterboot
Requires(preun): afterboot
Requires(preun): rpm-helper

%description
Rsync uses a quick and reliable algorithm to very quickly bring
remote and host files into sync.  Rsync is fast because it just
sends the differences in the files over the network (instead of
sending the complete files). Rsync is often used as a very powerful
mirroring process or just as a more capable replacement for the
rcp command.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%serverbuild
rm -f config.h
%configure2_5x \
    --with-acl-support \
    --enable-acl-support

# hack around bug in rsync configure.in
#echo '#define HAVE_INET_NTOP 1' >> config.h
#echo '#define HAVE_INET_PTON 1' >> config.h

%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/{man1,man5}}

%makeinstall
install -m 0644 %{_sourcedir}/rsync.html %{_sourcedir}/rsyncd.conf.html .
mkdir -p %{buildroot}%{_srvdir}/rsync/{log,peers,env}
install -m 0740 %{_sourcedir}/rsync.run %{buildroot}%{_srvdir}/rsync/run
install -m 0740 %{_sourcedir}/rsync-log.run %{buildroot}%{_srvdir}/rsync/log/run
touch %{buildroot}%{_srvdir}/rsync/peers/0
chmod 0640 %{buildroot}%{_srvdir}/rsync/peers/0

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/07_rsync.afterboot %{buildroot}%{_datadir}/afterboot/07_rsync

echo "873" >%{buildroot}%{_srvdir}/rsync/env/PORT


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv rsync
%_mkafterboot
pushd %{_srvdir}/rsync >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd


%preun
%_preun_srv rsync

%postun
%_mkafterboot


%files
%defattr(-,root,root)
%{_bindir}/rsync
%dir %attr(0750,root,admin) %{_srvdir}/rsync
%dir %attr(0750,root,admin) %{_srvdir}/rsync/log
%dir %attr(0750,root,admin) %{_srvdir}/rsync/peers
%dir %attr(0750,root,admin) %{_srvdir}/rsync/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rsync/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rsync/log/run
%config(noreplace) %attr(0640,root,admin)%{_srvdir}/rsync/peers/0
%config(noreplace) %attr(0640,root,admin)%{_srvdir}/rsync/env/PORT
%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*
%{_datadir}/afterboot/07_rsync

%files doc
%defattr(-,root,root)
%doc tech_report.tex README COPYING *html


%changelog
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.9
- 2.6.9
- enable ACL support

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.8
- 2.6.8
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6-3avx
- execline for runscript
- env dirs
- compile peers.cdb in %%post

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6-2avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6-1avx
- 2.6.6
- drop all patches; P1 not needed anymore, P0 was for draksync which
  we obviously don't ship
- use execlineb for run scripts
- move logdir to /var/log/service/rsync
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-4avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-2avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-1avx
- 2.6.3
- use logger for logging
- drop P2; no longer needed

* Fri Oct 08 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-6avx
- switch from tcpserver to tcpsvd
- Requires: ipsvd
- add the /service/rsync/peers directory to, by default, allow all
  connections
- add afterboot snippet

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-5avx
- update run scripts

* Fri Sep 03 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-4avx
- P2: security fix for CAN-2004-0792

* Wed Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-3avx
- remove xinetd support

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-2avx
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 2.6.2-1sls
- 2.6.2 (security update for CAN-2004-0426)
- rediff P1

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-3sls
- minor spec cleanups
- remove %%build_opensls macro
- srv macros

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-3sls
- put supervise scripts in here if %%build_opensls

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
