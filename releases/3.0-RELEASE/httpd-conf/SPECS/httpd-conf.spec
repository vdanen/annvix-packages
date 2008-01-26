#
# spec file for package httpd-conf
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-conf
%define version		2.2.8
%define release		%_revrel

%define compat_dir	/etc/httpd
%define compat_conf	/etc/httpd/conf


Summary:	Configuration files for Apache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org
Source0:	%{name}-%{version}.tar.bz2
Source3:	httpd.conf
Source4:	fileprotector.conf
Source5:	magic
Source6:	mime.types
Source7:	index.html
Source10:	robots.txt
Source11:	00_default_vhosts.conf
Source12:	mod_ssl-gentestcrt.sh
Source13:	httpd.run
Source14:	httpd-log.run
Source15:	03_apache2.afterboot
Source16:	httpd.logrotate

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	lynx >= 2.8.5
Requires:	httpd >= %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires(postun): afterboot
Requires(pre):	rpm-helper
Requires(pre):	afterboot
Requires(preun): rpm-helper

%description
This package contains configuration files for apache. It is necessary for
operation of the apache webserver. Having those files into a separate
modules provides better customization for OEMs and ISPs, who can modify the
look and feel of the apache webserver without having to re-compile the
whole suite to change a logo or config file.


%prep
%setup -q -n %{name}-%{version}


%build
%serverbuild

gcc %{optflags} -o advxsplitlogfile.bin advxsplitlogfile.c


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf/vhosts.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf/addon-modules
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

mkdir -p %{buildroot}/var/log/httpd
mkdir -p %{buildroot}/var/www/cgi-bin
mkdir -p %{buildroot}/var/www/icons
mkdir -p %{buildroot}/var/www/perl
mkdir -p %{buildroot}/var/www/html
mkdir -p %{buildroot}%{_datadir}/ADVX


install -m 0755 advxsplitlogfile.bin %{buildroot}%{_sbindir}/advxsplitlogfile
install -m 0755 advxsplitlogfile %{buildroot}%{_sbindir}/advxsplitlogfile.pl
install -m 0755 apache-2.0.40-testscript.pl %{buildroot}/var/www/cgi-bin/test.cgi
install -m 0755 apache-2.0.40-testscript.pl %{buildroot}/var/www/perl/test.pl
install -m 0755 mod_ssl-gentestcrt.sh %{buildroot}%{_sbindir}/mod_ssl-gentestcrt

# make some softlinks
pushd %{buildroot}%{_sysconfdir}/httpd
    ln -s ../../var/log/httpd logs
    ln -s ../..%{_libdir}/httpd modules
    ln -s ../..%{_libdir}/httpd-extramodules extramodules
popd

# config files
install -m 0644 %{_sourcedir}/httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf/httpd.conf
install -m 0644 %{_sourcedir}/fileprotector.conf %{buildroot}%{_sysconfdir}/httpd/conf/fileprotector.conf
install -m 0644 %{_sourcedir}/mime.types %{buildroot}%{_sysconfdir}/httpd/conf/mime.types
install -m 0644 %{_sourcedir}/magic %{buildroot}%{_sysconfdir}/httpd/conf/magic
install -m 0644 %{_sourcedir}/00_default_vhosts.conf %{buildroot}%{_sysconfdir}/httpd/conf/vhosts.d/00_default_vhosts.conf

# install misc documentation and logos
install -m 0644 index.shtml %{buildroot}/var/www/html/
install -m 0644 optim.html %{buildroot}/var/www/html/
install -m 0644 annvix.html %{buildroot}/var/www/html/
install -m 0644 favicon.ico %{buildroot}/var/www/html/
install -m 0644 %{_sourcedir}/robots.txt %{buildroot}/var/www/html/
install -m 0644 *.gif %{buildroot}/var/www/icons/
install -m 0644 *.png %{buildroot}/var/www/icons/
rm -f %{buildroot}/var/www/icons/mandrake.png
rm -f %{buildroot}/var/www/icons/medbutton.png

# put the advx stuff here
install -m 0644 advxaddmod %{buildroot}%{_datadir}/ADVX/
install -m 0644 advxdelmod %{buildroot}%{_datadir}/ADVX/
install -m 0644 advxfixconf %{buildroot}%{_datadir}/ADVX/
install -m 0644 advxlogserverstatus %{buildroot}%{_datadir}/ADVX/
install -m 0644 advx-checkifmigrate %{buildroot}%{_datadir}/ADVX/
install -m 0644 advx-cleanremove %{buildroot}%{_datadir}/ADVX/
install -m 0644 advx-migrate-commonhttpd.conf %{buildroot}%{_datadir}/ADVX/
install -m 0644 advx-migrate-httpd-perl.conf %{buildroot}%{_datadir}/ADVX/
install -m 0644 advx-migrate-httpd.conf %{buildroot}%{_datadir}/ADVX/
install -m 0644 advx-migrate-vhosts.conf %{buildroot}%{_datadir}/ADVX/
install -m 0644 mod_ssl-migrate-20 %{buildroot}%{_datadir}/ADVX/
install -m 0644 %{_sourcedir}/mod_ssl-gentestcrt.sh %{buildroot}%{_datadir}/ADVX/
install -m 0644 %{_sourcedir}/httpd.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/httpd

mkdir -p %{buildroot}%{_srvdir}/httpd/log
install -m 0740 %{_sourcedir}/httpd.run %{buildroot}%{_srvdir}/httpd/run
install -m 0740 %{_sourcedir}/httpd-log.run %{buildroot}%{_srvdir}/httpd/log/run

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/03_apache2.afterboot %{buildroot}%{_datadir}/afterboot/03_apache

# get rid of the ADVX stuff (I don't think we need any of it but this is a quick back if we do)
rm -rf %{buildroot}%{_datadir}/ADVX


%pre
%_pre_useradd apache /var/www /bin/true 74
%_mkafterboot


%post
%_post_srv httpd


%preun
%_preun_srv httpd


%postun
%_postun_userdel apache
%_mkafterboot


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/httpd

%dir %{_sysconfdir}/httpd
%dir %{_sysconfdir}/httpd/conf
%dir %{_sysconfdir}/httpd/conf/addon-modules
%dir %{_sysconfdir}/httpd/conf/vhosts.d
%dir %{_sysconfdir}/httpd/conf.d
%dir %{_sysconfdir}/httpd/modules.d

%dir %{_sysconfdir}/httpd/logs
%dir %{_sysconfdir}/httpd/modules
%dir %{_sysconfdir}/httpd/extramodules

%attr(0755,apache,apache) %dir /var/www
%attr(0755,root,root) %dir /var/www/html

%dir /var/log/httpd
%dir /var/www/cgi-bin
%dir /var/www/icons
%dir /var/www/perl

%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/fileprotector.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/mime.types
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/magic
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/vhosts.d/00_default_vhosts.conf

%attr(0755,root,root) /var/www/cgi-bin/*
%attr(0755,root,root) /var/www/perl/*
%attr(0644,root,root) /var/www/icons/*
%attr(0644,root,root) %config(noreplace) /var/www/html/favicon.ico
%attr(0644,root,root) %config(noreplace) /var/www/html/*.html
%attr(0644,root,root) %config(noreplace) /var/www/html/*.shtml
%attr(0644,root,root) %config(noreplace) /var/www/html/robots.txt
%attr(0755,root,root) %{_sbindir}/*
#%{_datadir}/ADVX

%dir %attr(0750,root,admin) %{_srvdir}/httpd
%dir %attr(0750,root,admin) %{_srvdir}/httpd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/httpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/httpd/log/run
%{_datadir}/afterboot/03_apache


%changelog
* Sat Jan 26 2008 Vincent Danen <vdanen-at-build.annivix.org> 2.2.8
- apache 2.2.8

* Fri Dec 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6
- update the afterboot snippet

* Fri Sep 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.6
- 2.2.6
- add mod_speling clause to the config
- time to get rid of the apache/apache2 obsoletes/provides
- don't own /var/cache/httpd; the httpd-common package already does
- don't build advxsplitlogfile against dietlibc as it can create strange logfiles
- updated mime-types with the vanilla one from 2.2.6

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4
- apache 2.2.4

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- put the logrotate script in it's own file
- make sure httpd is running before sending it the hup

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- don't symlink /usr/lib to /etc/httpd/lib (not sure why that was ever there)

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- drop the sysconfig file, it's not used
- some minor httpd.conf cleanups

* Thu Sep 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- no ADVX files should be needed/used anymore so remove the directory
  completely

* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- change runsvctrl calls to /sbin/sv calls
- index.html is in the tarball, not %%_sourcedir

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3
- 2.2.3

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2
- move the README file from httpd-conf to httpd

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2
- 2.2.2
- moved mod_ssl-gentestcrt here
- added default vhosts config
- drop S9 (who wants old mandriva 10.x config files?)
- merge the 2.2.2 configs from mandriva

* Tue Apr 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- don't let apache have a real shell, use /bin/true instead

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- dietlibc fixes

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Clean rebuild

* Sat Oct 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-5avx
- rebuild so the fixed useradd script works

* Fri Sep 16 2005 Sean P. Thomas <spt-at-build.annvix.org> 2.0.54-4avx
- add relocation of log directories

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-3avx
- remove the conf/webapps.d/*.conf stuff from httpd.conf; this is a
  Mandriva-ism that we do not want (is used by rpm packaged web-apps
  which I strongly disagree with)
- new style PreReqs
- make this package also require httpd

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-2avx
- i had fixed the config of the wrong httpd.conf file; fixed to
  minimize the exposed info

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-1avx
- 2.0.54; merge with mandrake apache-conf-2.0.54-12mdk:
- s/httpd2/httpd/
- NOTE: this one will require some personal massaging of the configs
  as we move from a multi-config system (commonhttpd.conf, httpd2.conf,
  and httpd2-perl.conf) to a single httpd.conf file

* Sat Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-9avx
- s/supervise/service/ in log/run

* Sat Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-8avx
- use execlineb for run scripts
- move logdir to /var/log/service/httpd2
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-7avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-5avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-4avx
= user logger for logging

* Sun Feb 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-3avx
- remove more ADVX-related stuff
- remove the peruser, perchild, and metuxmpm sections from the config
  files
- use fileprotector.conf as fileprotector.conf and don't accidentally
  copy the httpd2-perl.conf file
- rename S29
- remove webapps.d support

* Sun Feb 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-2avx
- put back our index.shtml and optim.html
- merge back changes to commonhttpd.conf

* Fri Feb 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-1avx
- 2.0.53
- get rid of ADVX stuff
- s/apache2/httpd2/ for the %%_srv macros
- handle mod_perl2 access from the apache2-mod_perl config (oden)
- add new dumpio module to the config (oden)
- merge changes from the httpd2-VANILLA.conf file (oden)
- S101: add means to secure sensible data (oden)

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-3avx
- rebuild against new dietlibc

* Fri Dec 03 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-2avx
- make apache own the %%ap_htdocsdir and %%ap_datadir
- fix the logrotate script:
  - go back to specifying *log rather than explicit log names (ie. so we can catch
    vhosts, etc.)
  - rotate logfiles 2GB and larger for sure
  - remove the prerotate script; why restart apache twice for each logfile?
- remove /var/apache-mm since we don't care about apache 1.3 anymore
- likewise for /etc/httpd/extramodules symlink
- add robots.txt file after looking at the suse stuff... (oden)
- always build the diet binary of advxlogsplitlogfile
- update the configs
- drop S54 and S55 (toggle between apache 2 and apache 1.3)
- drop S0 (don't need the initscript anymore)

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-1avx
- 2.0.52
- move runscripts and afterboot snippet here from apache2
- update the default index.shtml and related pages; make it more
  Annvix specific and clean it up (what an awful mess)

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-7avx
- update logrotate script

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-6avx
- by default, set ServerTokens to Prod (from Full) and ServerSignature
  to Off (from On)

* Mon Jun 28 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-5avx
- missed a few references to OpenSLS; fixed

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49-4avx
- Annvix build
- new icons (annvix.png and medbutton.png)

* Sun May 09 2004 Vincent Danen <vdanen@opensls.org> 2.0.49-3sls
- fix logrotate file
- make sure httpd2 uses /var/run/httpd2.pid and httpd2-perl uses
  /var/run/httpd-perl2.pid

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49-2sls
- add extramodules to file list (flepied)
- updated mimetypes from cooker 2.0.48-2mdk:
  - urpmi, urpmi-media, rpm, and OOo (flepied)

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49-1sls
- 2.0.49

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.0.48-3sls
- use static uid for user apache
- get rid of initscript
- supervise macros
- ADVXctl is gone now so don't delete apachectl
- include the /etc/httpd/conf/extramodules symlink
- fix logrotation; should work
- OpenSLS branding

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
