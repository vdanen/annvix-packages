# use fakeroot -ba sudo.spec to build!
%define pre p5

%define build_71 0
%if %build_71
%define _sysconfdir /etc
%endif

Summary:	Allows command execution as root for specified users.
Name:		sudo
Version:	1.6.7
Release:	0.p5.1mdk
Epoch:		1
License:	GPL
Group:		System/Base
URL:		http://www.courtesan.com/sudo
%if %pre
Source:		ftp://ftp.courtesan.com:/pub/sudo/%name-%version%pre.tar.gz
Source1:	ftp://ftp.courtesan.com:/pub/sudo/%name-%version%pre.tar.gz.sig
%else
Source:		ftp://ftp.courtesan.com:/pub/sudo/%name-%version.tar.gz
Source1:	ftp://ftp.courtesan.com:/pub/sudo/%name-%version.tar.gz.sig
%endif
BuildRoot:	%_tmppath/%name-%version
BuildRequires:  pam-devel
Requires:	/etc/pam.d/system-auth

%description
Sudo is a program designed to allow a sysadmin to give limited root
privileges to users and log root activity. The basic philosophy is
to give as few privileges as possible but still allow people to get
their work done.

%prep
%setup -q -n %name-%version%pre

%build
CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" \
%configure --prefix=%_prefix --with-logging=both --with-logpath=/var/log/sudo.log \
	   --with-editor=/bin/vi --enable-log-host --disable-log-wrap --with-pam --with-env-editor
%make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT/usr

%if %build_71
make prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc \
 install_uid=$UID install_gid=$(id -g) sudoers=uid=$UID sudoers_gid=$(id -g) \
 install
make prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc \
 install_uid=$UID install_gid=$(id -g) sudoers=uid=$UID sudoers_gid=$(id -g) \
 install-sudoers
%else
%makeinstall \
install_uid=$UID install_gid=$(id -g) sudoers=uid=$UID sudoers_gid=$(id -g)
%endif

mkdir -p $RPM_BUILD_ROOT/var/run/sudo
chmod 700 $RPM_BUILD_ROOT/var/run/sudo

# Installing sample pam file
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
cat > $RPM_BUILD_ROOT/etc/pam.d/sudo << EOF
#%PAM-1.0
auth       required	/%{_lib}/security/pam_stack.so service=system-auth
account    required	/%{_lib}/security/pam_stack.so service=system-auth
password   required	/%{_lib}/security/pam_stack.so service=system-auth
session    required	/%{_lib}/security/pam_stack.so service=system-auth
EOF

# Installing logrotated file
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
cat <<END >$RPM_BUILD_ROOT/etc/logrotate.d/sudo
/var/log/sudo.log {
    missingok
    monthly
    compress
}
END
chmod 755 $RPM_BUILD_ROOT/usr/bin/sudo
chmod 755 $RPM_BUILD_ROOT/usr/sbin/visudo

%clean
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi

%files
%defattr(-,root,root)
%doc BUGS CHANGES HISTORY INSTALL PORTING README RUNSON TODO
%doc TROUBLESHOOTING UPGRADE sample.sudoers
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers
%config(noreplace) %{_sysconfdir}/logrotate.d/sudo
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%attr(4111,root,root) %{_bindir}/sudo
%attr(0111,root,root) %{_sbindir}/visudo
%{_mandir}/*/*
/var/run/sudo

%changelog
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
