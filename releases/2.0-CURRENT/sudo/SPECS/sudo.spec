#
# spec file for package sudo
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sudo
%define version		1.6.8p12
%define release		%_revrel
%define epoch		1

Summary:	Allows command execution as root for specified users
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Base
URL:		http://www.courtesan.com/sudo
Source:		ftp://ftp.courtesan.com:/pub/sudo/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.courtesan.com:/pub/sudo/%{name}-%{version}.tar.gz.sig
Source2:	sudoers.annvix
Source3:	sudo.pam
Source4:	sudo.logrotate
Source4:	sudo.logrotate

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  pam-devel

Requires:	pam

%description
Sudo is a program designed to allow a sysadmin to give limited root
privileges to users and log root activity. The basic philosophy is
to give as few privileges as possible but still allow people to get
their work done.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

%build
CFLAGS="%{optflags} -D_GNU_SOURCE" \
%configure --prefix=%{_prefix} \
    --with-logging=both \
    --with-logpath=/var/log/sudo.log \
    --with-editor=/bin/vi \
    --enable-log-host \
    --disable-log-wrap \
    --with-pam \
    --with-env-editor \
    --with-noexec=no \
    --with-secure-path="/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/sbin:/usr/local/bin"
%make CFLAGS="%{optflags} -D_GNU_SOURCE"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}

%makeinstall \
install_uid=$UID install_gid=$(id -g) sudoers=uid=$UID sudoers_gid=$(id -g)

mkdir -p %{buildroot}/var/run/sudo
chmod 0700 %{buildroot}/var/run/sudo

# Install sample pam file
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/sudo

# Install logrotate file
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/sudo

chmod 0755 %{buildroot}%{_bindir}/sudo
chmod 0755 %{buildroot}%{_sbindir}/visudo

# install our sudoers file
install -m 0440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers
%config(noreplace) %{_sysconfdir}/logrotate.d/sudo
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%attr(4111,root,root) %{_bindir}/sudo
%attr(4111,root,root) %{_bindir}/sudoedit
%attr(0111,root,root) %{_sbindir}/visudo
%{_mandir}/*/*
/var/run/sudo

%files doc
%defattr(-,root,root)
%doc BUGS CHANGES HISTORY INSTALL PORTING README RUNSON TODO
%doc TROUBLESHOOTING UPGRADE sample.sudoers


%changelog
* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.8p12
- add the APT group in sudoers, but don't assign it to anyone by default
  (apt can provide too much information for some, unlike rurpmi)
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.8p12
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.8p12
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Dec 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p12-1avx
- 1.6.8p12 (fixes CVE-2005-4158)
- drop P0; merged upstream

* Wed Oct 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p9-5avx
- P0: to fix CAN-2005-2959

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p9-4avx
- update default /etc/sudoers to provide access to restricted urpmi,
  network tools (ping, traceroute), and user management tools (ie.
  chage, chsh, newgrp, etc.) as we are stripping the suid bit from
  these tools

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p9-3avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p9-2avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p9-1avx
- 1.6.8p9 (fixes CAN-2005-1993)
- move embedded "source" files into real source files (S3, S4)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p2-2avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.8p2-1avx
- 1.6.8p2; fixes a security flaw regarding bash scripts
- fix naming convention
- minor spec cleanups
- set env_reset as a default in /etc/sudoers to enforce clean environments
- set the secure-path by default
- include sudoedit
- turn of noexec support

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1:1.6.7-0.p5.4avx
- require pam, not the system-auth file
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1:1.6.7-0.p5.3sls
- fix pam file
- macros and spec cleanups
- S2: our own sudoers file; by default give group admin access to /bin/su

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1:1.6.7-0.p5.2sls
- OpenSLS build
- tidy spec
- remove %%build_71 macro

* Fri Jul 18 2003 Warly <warly@mandrakesoft.com> 1:1.6.7-0.p5.1mdk
- keed gz format and and site signature
- new version

* Thu Jun  6 2002 Warly <warly@mandrakesoft.com> 1.6.6-2mdk
- fix hardcoded libraries path

* Thu May 16 2002 Warly <warly@mandrakesoft.com> 1.6.6-1mdk
- new version

* Tue Apr 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.6.5-0.1p2mdk
- 1.6.5p2
- clean spec file

* Fri Mar  8 2002 Warly <warly@mandrakesoft.com> 1.6.4-2mdk
- add missingok for logrotate (thanks Andrej Borsenkow)

* Mon Jan 14 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.6.4-1mdk
- 1.6.4
- conditional macro; enable %%build_71 for 7.1/Corporate Server 1.0.1

* Wed Jul 18 2001 Warly <warly@mandrakesoft.com> 1.6.3p7-2mdk
- change editor to /bin/vi and use EDITOR env var

* Fri May  4 2001 Warly <warly@mandrakesoft.com> 1.6.3p7-1mdk
- new version

* Mon Feb 26 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.6.3p6-1mdk
- 1.6.3p6
- security fixes for buffer overflow problem

* Tue Oct  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.6.3p4-3mdk
- pam_stack.

* Thu Aug 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.6.3p4-2mdk
- BM
- use noreplace for config files.

* Fri Jun 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.6.3p4-1mdk
- 1.6.3p4.

* Thu Jun 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.6.2p2-4mdk
- Correct build as users.

* Fri Apr 07 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.6.2p2-3mdk
- Set /etc/sudoers as 0440.

* Fri Apr 7 2000 Denis Havlik <denis@mandrakesoft.com> 1.6.2p2-2mdk
- Group: System/Base
- fixed config files

* Mon Feb 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.6.2p2-1mdk
- 1.62p2.

* Wed Feb  9 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.6.2p1-1mdk
- 1.6.2p1.
- specs teak.

* Thu Jul 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.

* Fri Jun  4 1999 Ryan Weaver <ryanw@infohwy.com>
  [sudo-1.5.9p3-1]
- Updated to version 1.5.9p3
- Changed RPM name from cu-sudo tp sudo.

* Fri Jun  4 1999 Ryan Weaver <ryanw@infohwy.com>
  [cu-sudo-1.5.9p2-1]
- Added dir /var/run/sudo to file list.
- Added --enable-log-host --disable-log-wrap to configure.
- Added --with-logging=file to configure.
- Added logrotate.d file to rotate /var/log/sudo.log monthly.

* Fri Jun  4 1999 Ryan Weaver <ryanw@infohwy.com>
  [cu-sudo-1.5.9p2-1]
- Initial RPM build.
- Installing sample pam file.
