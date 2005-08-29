#
# spec file for package runit
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define	name		runit
%define	version		1.3.1
%define	release		1avx

%define aver		0.1

Summary:	A UN*X init scheme with service supervision
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Base
URL:		http://smarden.org/runit/
Source0:	%{name}-%{version}.tar.gz
# available from http://annvix.org/cg-bin/viewcvs.cgi/tools/runit/
Source1:	annvix-runit-%{aver}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.28

Requires:	SysVinit >= 2.85-7avx, initscripts, srv, mingetty, execline
Conflicts:	SysVinit <= 2.85-6avx

%description
runit is a daemontools-like replacement for SysV-init and other
init schemes.  It currently runs on GNU/Linux, OpenBSD, FreeBSD,
and can easily be adapted to other Unix operating systems.  runit
implements a simple three-stage concept.  Stage 1 performs the
system's one-time initialization tasks.  Stage 2 starts the
system's uptime services (via the runsvdir program).  Stage 3
handles the tasks necessary to shutdown and halt or reboot. 


%prep
%setup -q -n admin -a 1


%build
pushd %{name}-%{version}/src
    echo "diet gcc -Os -pipe" > conf-cc
    echo "diet gcc -Os -static -s" > conf-ld
    make
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{/service,/sbin,%{_mandir}/man8,%{_sysconfdir}/runit,%{_srvdir}/mingetty-tty{1,2,3,4,5,6}}
install -d %{buildroot}/sbin/
install -d %{buildroot}%{_mandir}/man8

pushd %{name}-%{version}
    for i in `cat package/commands`; do
	install -m 0755 src/$i %{buildroot}/sbin/
    done
    mv %{buildroot}/sbin/runit-init %{buildroot}/sbin/init
popd

pushd annvix-runit-%{aver}
    for i in 1 2 3 ctrlaltdel
    do 
        install -m 0700 $i %{buildroot}%{_sysconfdir}/runit/$i
    done
    for i in 1 2 3 4 5 6
    do 
        install -m 0740 mingetty-tty$i/* %{buildroot}%{_srvdir}/mingetty-tty$i/
    done
popd

install -m 0644 %{name}-%{version}/man/*.8 %{buildroot}%{_mandir}/man8/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ $1 == "1" ]; then
    # this is a new install, we need to setup the gettys
    for i in 2 3 4 5 6
    do
	echo "Setting up the mingetty service for tty$i..."
        srv add mingetty-tty$i
        # even though this may cause some grief for existing non-runit systems, we need
        # to remove the down file because on a new install, the user would reboot into a
        # system with no gettys
        rm -f /service/mingetty-tty$i/down
    done
fi


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/package/THANKS
%doc %{name}-%{version}/doc/*.html
%doc %{name}-%{version}/etc/2
%doc %{name}-%{version}/etc/debian
%dir /service
%attr(0700,root,root) /sbin/runit
%attr(0700,root,root) /sbin/init
%attr(0755,root,root) /sbin/runsv
%attr(0755,root,root) /sbin/runsvdir
%attr(0755,root,root) /sbin/runsvchdir
%attr(0755,root,root) /sbin/svwaitdown
%attr(0755,root,root) /sbin/sv
%attr(0755,root,root) /sbin/runsvctrl
%attr(0755,root,root) /sbin/runsvstat
%attr(0755,root,root) /sbin/svwaitup
%attr(0755,root,root) /sbin/svlogd
%attr(0755,root,root) /sbin/chpst
%attr(0755,root,root) /sbin/utmpset
%attr(0644,root,root) %{_mandir}/man8/chpst.8*
%attr(0644,root,root) %{_mandir}/man8/runit-init.8*
%attr(0644,root,root) %{_mandir}/man8/runit.8*
%attr(0644,root,root) %{_mandir}/man8/runsv.8*
%attr(0644,root,root) %{_mandir}/man8/runsvchdir.8*
%attr(0644,root,root) %{_mandir}/man8/runsvctrl.8*
%attr(0644,root,root) %{_mandir}/man8/runsvdir.8*
%attr(0644,root,root) %{_mandir}/man8/runsvstat.8*
%attr(0644,root,root) %{_mandir}/man8/svlogd.8*
%attr(0644,root,root) %{_mandir}/man8/svwaitdown.8*
%attr(0644,root,root) %{_mandir}/man8/svwaitup.8*
%attr(0644,root,root) %{_mandir}/man8/sv.8*
%attr(0644,root,root) %{_mandir}/man8/utmpset.8*
%attr(0700,root,root) %dir %{_sysconfdir}/runit
%attr(0700,root,root) %{_sysconfdir}/runit/1
%attr(0700,root,root) %{_sysconfdir}/runit/2
%attr(0700,root,root) %{_sysconfdir}/runit/3
%attr(0700,root,root) %{_sysconfdir}/runit/ctrlaltdel
%dir %attr(0750,root,admin) %{_srvdir}/mingetty-tty1
%attr(0740,root,admin) %{_srvdir}/mingetty-tty1/run
%attr(0740,root,admin) %{_srvdir}/mingetty-tty1/finish
%dir %attr(0750,root,admin) %{_srvdir}/mingetty-tty2
%attr(0740,root,admin) %{_srvdir}/mingetty-tty2/run
%attr(0740,root,admin) %{_srvdir}/mingetty-tty2/finish
%dir %attr(0750,root,admin) %{_srvdir}/mingetty-tty3
%attr(0740,root,admin) %{_srvdir}/mingetty-tty3/run
%attr(0740,root,admin) %{_srvdir}/mingetty-tty3/finish
%dir %attr(0750,root,admin) %{_srvdir}/mingetty-tty4
%attr(0740,root,admin) %{_srvdir}/mingetty-tty4/run
%attr(0740,root,admin) %{_srvdir}/mingetty-tty4/finish
%dir %attr(0750,root,admin) %{_srvdir}/mingetty-tty5
%attr(0740,root,admin) %{_srvdir}/mingetty-tty5/run
%attr(0740,root,admin) %{_srvdir}/mingetty-tty5/finish
%dir %attr(0750,root,admin) %{_srvdir}/mingetty-tty6
%attr(0740,root,admin) %{_srvdir}/mingetty-tty6/run
%attr(0740,root,admin) %{_srvdir}/mingetty-tty6/finish


%changelog
* Mon Aug 29 2005 Vincent Danen <vdanen@annvix.org> 1.3.1-1avx
- 1.3.1

* Fri Aug 26 2005 Vincent Danen <vdanen@annvix.org> 1.3.0-2avx
- fix perms on run scripts

* Wed Aug 24 2005 Vincent Danen <vdanen@annvix.org> 1.3.0-1avx
- 1.3.0
- Requires: execline
- new tarball from cvs (tools/runit) for runit scripts
- change run script ownership to root:admin and mode 0740
- make runit and init mode 0700

* Wed Aug 10 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-8avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-7avx
- note the time we're waiting for service shutdowns (re: Sean Thomas)
- fix changelog entries

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-6avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-5avx
- instead of waiting 350secs for all services to stop, we wait
  180secs; this is because logged in ssh users will cause this
  timeout as sshd will not die with any children running.  3
  minutes is more than reasonable

* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-4avx
- build against new dietlibc

* Tue Jan 25 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-3avx
- build without dietlibc
- remove BuildRequires: dietlibc; add BuildRequires: glibc-static-devel

* Thu Jan 20 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-2avx
- rebuild against fixed dietlibc

* Thu Jan 20 2005 Vincent Danen <vdanen@annvix.org> 1.2.1-1avx
- 1.2.1
- don't set -march=pentium anymore

* Wed Oct 13 2004 Vincent Danen <vdanen@annvix.org> 1.0.5-1avx
- 1.0.5

* Fri Sep 17 2004 Vincent Danen <vdanen@annvix.org> 1.0.4-6avx
- own /service since daemontools will soon be removed

* Tue Sep 14 2004 Vincent Danen <vdanen@annvix.org> 1.0.4-5avx
- don't ever restart the gettys
- Requires: mingetty

* Sat Sep 10 2004 Vincent Danen <vdanen@annvix.org> 1.0.4-4avx
- dammit... works good if you install from remote, but kicks you off your vc
  if you're local, so don't automatically add tty1; the installer will take
  care of this for new installs

* Sat Sep 10 2004 Vincent Danen <vdanen@annvix.org> 1.0.4-3avx
- somewhat ugly means of getting the getty's up and running for the
  reboot, but necessary as %%_post_srv only checks to restart a service
  and doesn't set one up or make it ready to start

* Sat Sep 10 2004 Vincent Danen <vdanen@annvix.org> 1.0.4-2avx
- Conflicts: SysVinit <= 2.85-6avx (7avx moves init to init.srv)
- Requires SysVinit >= 2.86-7avx, initscripts, srv

* Sat Sep 10 2004 Vincent Danen <vdanen@annvix.org> 1.0.4-1avx
- first Annvix build
- S1: runit scripts

* Tue Aug 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.4-1mdk
- 1.0.4

* Thu Nov 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.12.1-1mdk
- 0.12.1

* Thu Sep 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.11.1-1mdk
- 0.11.1

* Fri Aug 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.11.0-1mdk
- initial cooker contrib
