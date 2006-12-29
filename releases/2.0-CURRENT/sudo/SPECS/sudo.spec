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
Patch0:		sudo-1.6.8p8-default_whitelist.patch

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
%patch0 -p0 -b .default_whitelist


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
* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.8p12
- rebuild against new pam

* Thu Aug 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.8p12
- P0: make sudo use env_reset by default so instead of blacklisting certain
  variables, we whitelist a few and the admin needs to use env_keep to pass
  any other variables he/she wants (ref: MDKSA-2006:159)

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6.8p12
- rebuild against new pam
- update S3 to use the include directive rather than pam_stack

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
