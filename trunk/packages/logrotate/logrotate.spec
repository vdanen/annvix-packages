Summary: Rotates, compresses, and mails system logs
Name: logrotate
Version: 3.6.6
Release: 2mdk
License: GPL
Group: File tools
BuildRequires: popt-devel
Source0: ftp://ftp.redhat.com/pub/redhat/code/logrotate/logrotate-%{PACKAGE_VERSION}.tar.bz2
Source1: logrotate.conf.mdk.bz2
BuildRoot: %{_tmppath}/logrotate.root
URL: ftp://ftp.redhat.com/pub/redhat/linux/rawhide/SRPMS/SRPMS/

%description
Logrotate is designed to ease administration of systems that generate
large numbers of log files. It allows automatic rotation, compression,
removal, and mailing of log files. Each log file may be handled daily,
weekly, monthly, or when it grows too large.

%prep
%setup -q

%build
%make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
make PREFIX=$RPM_BUILD_ROOT install MANDIR=%{_mandir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily

bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

install -m 755 examples/%{name}.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGES
%attr(0755, root, root) %{_sbindir}/%{name}
%attr(0644, root, root) %{_mandir}/man8/%{name}.8*
%config(noreplace) %attr(0755, root, root) %{_sysconfdir}/cron.daily/%{name}
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0755, root, root) %dir %{_sysconfdir}/%{name}.d

%changelog
* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.6.6-2mdk
- rebuild
- macroize
- use %%make macro

* Fri Dec 27 2002 Warly <warly@mandrakesoft.com> 3.6.6-1mdk
- new version

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.6.5-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Sat Aug 10 2002 Warly <warly@mandrakesoft.com> 3.6.5-1mdk
- new version

* Fri Mar 29 2002 Warly <warly@mandrakesoft.com> 3.6.3-1mdk
- new version

* Mon Dec 31 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.6-1mdk
- 3.6.
- Remove the errors line.

* Fri Nov  2 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 3.5.9-1mdk
- new version
- add URL tag

* Thu Apr 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.5.4-1mdk
- Add doc.
- 3.5.4:
     - patch /tmp file race condition problem, use mkstemp;	
	  Thanks go to Solar Designer <solar@openwall.com>

* Mon Dec 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.5.2-1mdk
- new and shiny source.

* Thu Sep 14 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 3.3-9mdk
- removed patch (taboo extensions are used only for config files in /etc)
- solution : 
	+ don't use * in logrotate.d/syslog (easy but a bit boring)
		That's what I do in package sysklogd
	+ OR patch readConfigFile function in config.c 
	     which creates the log set to rotate and calls rotateLogSet
		 on line 693 : glob result should be freed from compressed archives

* Mon Sep 04 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 3.3-8mdk
- Added one line patch for logrotate to avoid rotating .bz2 file if '*' 
  is specified.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.3-7mdk
- automatically added BuildRequires

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3-6mdk
- macros, BM, _spechelper_
- make it nice with rpmlint :-)

* Thu May 04 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 3.3-5mdk
- logrotate syslog config now installed by syslog...
  reverted the previous change.

* Tue May 02 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 3.3-4mdk
- We shouldn't ship the default logrotate config file.
  install the logrotate.conf.mdk file.
- Adjusted to feet the actual syslog.conf

* Tue Apr 18 2000 Jerome Dumonteil <jd@mandrakesoft.com> 3.3-3mdk
- add version
* Fri Mar 31 2000 Jerome Dumonteil <jd@mandrakesoft.com>
- change group
- use _tmppath

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 3.3.

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- update to 2.1.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
