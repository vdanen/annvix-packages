%define ver 4

Summary:	A program which manages RPC connections
Name:		portmap
Version:	%{ver}.0
Release:	21mdk
Group:		System/Servers
License:	BSD

Source0:	ftp://coast.cs.purdue.edu:/pub/tools/unix/netutils/portmap/portmap_%{ver}.tar.bz2
Source1:	portmap.init
Source2:	pmap_set.8.bz2
Source3:	pmap_dump.8.bz2
Source4:	portmap.8.bz2
Patch0:		portmap-4.0-linux.patch.bz2
Patch1:		portmap-malloc.patch.bz2
Patch2:		portmap-4.0-cleanup.patch.bz2
Patch3:		portmap-4.0-rpc_user.patch.bz2
Patch4:		portmap-4.0-sigpipe.patch.bz2
Patch5:		portmap-4.0-errno.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Prereq:		/sbin/chkconfig, rpm-helper
BuildRequires:	tcp_wrappers-devel
Requires: setup >= 2.1.9-38mdk

%description
The portmapper program is a security tool which prevents theft of NIS
(YP), NFS and other sensitive information via the portmapper.  A
portmapper manages RPC connections, which are used by protocols like
NFS and NIS.

The portmap package should be installed on any machine which acts as
a server for protocols using RPC.

%prep 
%setup -q -n portmap_%{ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%serverbuild
make FACILITY=LOG_AUTH ZOMBIES='-DIGNORE_SIGCHLD -Dlint' LIBS="-lnsl" RPM_OPT_FLAGS="$RPM_OPT_FLAGS" \
	WRAP_DIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d

install -m 755 -s portmap $RPM_BUILD_ROOT/sbin
install -m 755 -s pmap_set $RPM_BUILD_ROOT/usr/sbin
install -m 755 -s pmap_dump $RPM_BUILD_ROOT/usr/sbin
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/portmap

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd rpc / /bin/false

%post
%_post_service portmap

%triggerpostun -- portmap <= portmap-4.0-9
/sbin/chkconfig --add portmap

%preun
%_preun_service portmap

%postun
%_postun_userdel rpc

%files
%defattr(-,root,root)
%doc README CHANGES BLURB

/sbin/portmap
/usr/sbin/pmap_dump
/usr/sbin/pmap_set
%{_mandir}/*/*

%config(noreplace) %{_initrddir}/portmap

%changelog
* Mon Apr 28 2003 Warly <warly@mandrakesoft.com> 4.0-21mdk
- fix rebuild

* Wed Jul 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0-20mdk
- lib64 fixes

* Thu Jul 18 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0-19mdk
- add rpc user

* Wed Feb 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0-18mdk
- applied patch from rh to not die on sigpipe

* Fri Mar 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-17mdk
- use new server macros

* Mon Mar 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-16mdk
- initscript installed as no replace.
- depends on setup-2.1.9-38mdk for user rpc.

* Wed Mar 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-15mdk
- We have a rpc user we can apply the rpc user patch.
- Requires last setup.

* Mon Feb 26 2001 Francis Galiegue <fg@mandrakesoft.com> 4.0-14mdk
- Don't apply patch3, unless we decide one day to have a rpc user...

* Sat Feb 24 2001 Francis Galiegue <fg@mandrakesoft.com> 4.0-13mdk
- Patch merge from RH

* Fri Nov 10 2000 David BAUDENS <baudens@mandrakesoft.com> 4.0-12mdk
- BuildRequires: tcp_wrappers-devel

* Thu Aug 31 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 4.0-11mdk
- slight specfile cleanup
- use %{_initrddir}
- don't link portmap init script in runlevel dir, chkconfig do it for us

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>  4.0-10mdk
- BM, macros

* Wed Mar 22 2000 Pixel <pixel@mandrakesoft.com> 4.0-9mdk
- fix version (is 4.0, not 4)

* Tue Mar 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 4-9mdk
- Fix group tag.
- Use version tag.

* Fri Nov  5 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- checkconfig --del in %preun.

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- added man pages.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul  7 1998 Jeff Johnson <jbj@redhat.com>
- start/stop portmap at levels 11/89

* Mon May 04 1998 Cristian Gafton <gafton@redhat.com>
- fixed the trigger script

* Fri May 01 1998 Jeff Johnson <jbj@redhat.com>
- added triggerpostun

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- added %trigger to fix a previously broken package

* Thu Apr 23 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscripts

* Thu Jan 08 1998 Erik Troan <ewt@redhat.com>
- rebuilt against glibc 2.0.6

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>
- fixed service name in stop section of init script

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- fixed chkconfig support

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- added restart, status commands to init script
- added chkconfig support
- uses a buildroot and %attr tags

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
