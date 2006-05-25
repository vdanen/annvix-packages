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
%define version		2.2.2
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
Source2:	httpd.sysconf
Source3:	httpd.conf
Source4:	fileprotector.conf
Source5:	magic
Source6:	mime.types
Source7:	index.html
Source8:	httpd-conf-README.urpmi
Source10:	robots.txt
Source11:	00_default_vhosts.conf
Source12:	mod_ssl-gentestcrt.sh

Source100:	httpd.run
Source101:	httpd-log.run
Source102:	03_apache2.afterboot

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.20-1mdk

Requires:	lynx >= 2.8.5, httpd >= %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper, afterboot
Requires(pre):	rpm-helper, afterboot
Requires(preun): rpm-helper
Provides:	apache2-conf apache-conf
Obsoletes:	apache2-conf apache-conf
#JMD: We have to do this here, since files have moved
Obsoletes:	apache-common

%description
This package contains configuration files for apache. It is
necessary for operation of the apache webserver. Having those
files into a separate modules provides better customization for
OEMs and ISPs, who can modify the look and feel of the apache
webserver without having to re-compile the whole suite to change
a logo or config file.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .
cp %{SOURCE6} .
cp %{SOURCE7} .
cp %{SOURCE8} README.urpmi
cp %{SOURCE10} .
cp %{SOURCE11} .
cp %{SOURCE12} .


%build
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif

$COMP -Os -s -static -nostdinc -o advxsplitlogfile-DIET advxsplitlogfile.c


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf/vhosts.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf/addon-modules
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

mkdir -p %{buildroot}/var/cache/httpd
mkdir -p %{buildroot}/var/log/httpd
mkdir -p %{buildroot}/var/www/cgi-bin
mkdir -p %{buildroot}/var/www/icons
mkdir -p %{buildroot}/var/www/perl
mkdir -p %{buildroot}/var/www/html
mkdir -p %{buildroot}%{_datadir}/ADVX


install -m 0755 advxsplitlogfile-DIET %{buildroot}%{_sbindir}/
install -m 0644 advxsplitlogfile %{buildroot}%{_sbindir}/
install -m 0755 apache-2.0.40-testscript.pl %{buildroot}/var/www/cgi-bin/test.cgi
install -m 0755 apache-2.0.40-testscript.pl %{buildroot}/var/www/perl/test.pl
install -m 0755 mod_ssl-gentestcrt.sh %{buildroot}%{_sbindir}/mod_ssl-gentestcrt

# make some softlinks
pushd %{buildroot}%{_sysconfdir}/httpd
    ln -s ../..%{_libdir} %{_lib}
    ln -s ../../var/log/httpd logs
    ln -s ../..%{_libdir}/httpd modules
    ln -s ../..%{_libdir}/httpd-extramodules extramodules
popd

# config files
install -m 0644 httpd.conf %{buildroot}%{_sysconfdir}/httpd/conf/httpd.conf
install -m 0644 fileprotector.conf %{buildroot}%{_sysconfdir}/httpd/conf/fileprotector.conf
install -m 0644 mime.types %{buildroot}%{_sysconfdir}/httpd/conf/mime.types
install -m 0644 magic %{buildroot}%{_sysconfdir}/httpd/conf/magic
install -m 0644 httpd.sysconf %{buildroot}%{_sysconfdir}/sysconfig/httpd
install -m 0644 00_default_vhosts.conf %{buildroot}%{_sysconfdir}/httpd/conf/vhosts.d/00_default_vhosts.conf

# install misc documentation and logos
install -m 0644 index.shtml %{buildroot}/var/www/html/
install -m 0644 optim.html %{buildroot}/var/www/html/
install -m 0644 annvix.html %{buildroot}/var/www/html/
install -m 0644 favicon.ico %{buildroot}/var/www/html/
install -m 0644 robots.txt %{buildroot}/var/www/html/
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
install -m 0644 mod_ssl-gentestcrt.sh %{buildroot}%{_datadir}/ADVX/

cat > %{buildroot}%{_sysconfdir}/logrotate.d/httpd << EOF
/var/log/httpd/*log
{
    size=2000M
    rotate 5
    monthly
    missingok
    nocompress
    notifempty
    postrotate
	[[ -d /service/httpd ]] && runsvctrl h /service/httpd >/dev/null 2>&1
    endscript
}
EOF

mkdir -p %{buildroot}%{_srvdir}/httpd/log
install -m 0740 %{SOURCE100} %{buildroot}%{_srvdir}/httpd/run
install -m 0740 %{SOURCE101} %{buildroot}%{_srvdir}/httpd/log/run

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE102} %{buildroot}%{_datadir}/afterboot/03_apache


%pre
%_pre_useradd apache /var/www /bin/true 74
%_mkafterboot

%post
if [ -d /var/log/supervise/httpd -a ! -d /var/log/service/httpd ]; then
    mv /var/log/supervise/httpd /var/log/service/
fi
if [ -d /var/log/supervise/httpd2 -a ! -d /var/log/service/httpd ]; then
    mv /var/log/supervise/httpd2 /var/log/service/httpd
fi

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
%doc README.urpmi
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/httpd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/httpd

%dir %{_sysconfdir}/httpd
%dir %{_sysconfdir}/httpd/conf
%dir %{_sysconfdir}/httpd/conf/addon-modules
%dir %{_sysconfdir}/httpd/conf/vhosts.d
%dir %{_sysconfdir}/httpd/conf.d
%dir %{_sysconfdir}/httpd/modules.d

%dir %{_sysconfdir}/httpd/%{_lib}
%dir %{_sysconfdir}/httpd/logs
%dir %{_sysconfdir}/httpd/modules
%dir %{_sysconfdir}/httpd/extramodules

%attr(0755,apache,apache) %dir /var/www
%attr(0755,root,root) %dir /var/www/html
%attr(0755,apache,apache) %dir /var/cache/httpd

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
%{_datadir}/ADVX

%dir %attr(0750,root,admin) %{_srvdir}/httpd
%dir %attr(0750,root,admin) %{_srvdir}/httpd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/httpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/httpd/log/run
%{_datadir}/afterboot/03_apache


%changelog
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

* Wed Oct 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48-1mdk
- 2.0.48
- drop 8x support
- activate mod_logio

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.47-8mdk
- Remove ScriptLog, nice try, but that wasn't the right solution to the
  cgi problem. The Apache bug 22030 was fixed in apache2-2.0.47-6mdk

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.47-7mdk
- Fix ScriptLog

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.47-6mdk
- AddLanguage eo .eo (esperanto)
- AddDefaultCharset Off (it was overriding META tags which is bad for
  international sites) [BUG 5398]
- Make Apache start after Mysql [BUG 5532]
- Add ScriptLog directive to httpd2.conf to flush stderr

* Thu Sep 04 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.47-5mdk
- add mime types for .jar and .jad on request by Andre Nathan
- Remove the #config directive in the initscript since it confuses
  linuxconf 
- fix ownership of cache directory [BUG 3904]

* Thu Sep 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47-4mdk
- fix ASF bug #21685 on request by Grégoire Colbert

* Tue Sep 02 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47-3mdk
- close #4364

* Fri Jul 11 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.47-2mdk
- Fix advxsplitlogfile for good
- Do not rotate ssl_cache, otherwise some race conditions can happen.

* Wed Jul 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47-1mdk
- 2.0.47
- added new (commented) directories to S6

* Wed Jun 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-2mdk
- fix S0 (duh!)

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-1mdk
- 2.0.46
- manually merged entries from old S3 into new S3 from 2.0.46 (phuh!)
- updated S1, S2, S5, S6
- kill zombie advxsplitlogfile processes when shut down (S0)
- split configs into separate files (mod_proxy, etc.)

* Sat Apr 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.45-4mdk
- Fix reload, make it libdir independent. For further changes, please
  make sure to use detect/detectlib before any use of $LIB variable

* Fri Apr 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.45-3mdk
- Make it lib64 aware

* Mon Apr 07 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.45-2mdk
- Rebuild for 9.1 security update

* Tue Apr 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45-1mdk
- 2.0.45
- updated S6

* Tue Mar  4 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-11mdk
- Add link for both versions of modules (1.3 and 2.0).

* Tue Mar  4 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-10mdk
- Remove the text about removing the .htaccess, since it's now included as
  an ErrorDocument message.

* Tue Mar  4 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-9mdk
- fix ErrorDocument for manuals
- change index.shtml to reflect the fact that we can install both versions
  of Apache, that we can switch from one version to the other, and that we
  have both manual versions as well.
- put config(noreplace) for favicon.ico to not overwrite a web site's icon.
  (submitted by David Walser <luigiwalser@yahoo.com>

* Sun Mar  2 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-8mdk
- Fix mime type for svg+xml (requested by liam@w3.org)
- add index.xml to the list of indexes
- fix public_html stuff in commonhttpd.conf

* Sun Mar  2 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-7mdk
- Add a new set of "Powered-by" icons with a similar look-and-feel as the
  ubiquitous Apache icon.
- Redesign the index page a bit
- Add an ErrorDocument directives to the .htaccess file in addon-modules so
  people know what to do if they want to enable access to that directory.
- Change favicon.ico by a new ADVX icon.

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-6mdk
- Modify commonhttpd.conf so that /perl-status works when mod_perl 2.0 is
  really final
- advxsplitlogfile: fixes for "use stric" and perl_checker fixes

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-5mdk
- JMD: PLEASE REMOVE apache2-conf FROM MAIN!
- Obsoletes: apache2-conf

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-4mdk
- Update mime types... before: 270, after: 441!
- Improve migration scripts, we can update from as far as MDK 7.1!

* Sat Feb 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-3mdk
- use %%ghost for old config files

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-2mdk
- renamed apache2-conf SRPM and RPM to apache-conf, since both versions of
  Apache can use the same config files.
- misc. fixes to the init script
- add ap13chkconfig, advxrun1.3 and advxrun2.0 scripts for easy migration
  and switching from 1.3 to 2.0.

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44-1mdk
- 2.0.44
- updated S6

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-5mdk
- fix buildrequires ADVX-build >= 1.1
- clean up after build

* Mon Jan 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43-4mdk
- Up version number to synchronize Cooker: the apache-conf rpm is now
  generated by the apache2-conf SRPM, and the upload scripts don't know
  how to manage that. 

* Tue Jan 07 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43-3mdk
- Put README.apache-conf in the right place.
- Fix initscript to use the pid files to know what to stop, instead
  of relying the presence of binaries, this makes it possible to switch
  versions (1.3/2.0/1.3-perl) on the fly.

* Mon Jan 06 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.43-2mdk
- Use the apache2-conf SRPM to generate apache-conf. It was a PITA to 
  manage two versions, and since the source files are the same, it's a
  logical thing to do.
- Created a new apache-compat package that will help 2.0 users who
  need to roll back to 1.3 temporarily (and back to 2.0 again when
  they're ready)
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 
- Likewise, add Provides: AP13package and AP20package in the same
  manner

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)

* Wed Sep 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-3mdk
- added the new mod_logio module entries to commonhttpd.conf and
  httpd2.conf, check: http://localhost/manual/mod/mod_logio.html

* Wed Sep 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-2mdk
- argh!, corrected a small glitch in commonhttpd.conf

* Wed Sep 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42-1mdk
- remove the ADVX rpm package naming scheme
- merge config changes from 2.0.42, also add missing stuff

* Mon Sep 23 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40ADVX-14mdk
- use spec file magic from the nagios package to enable builds on ML8.x, and/or
  optionally compile advxsplitlogfile.c against dietlibc

* Sat Sep 07 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-13mdk
- add ADVXpost 

* Sat Sep 07 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-12mdk
- Add more sanity checking into init script
- Really fix description this time 

* Fri Sep 06 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-11mdk
- Correct description
- Fix init script in case someone upgrades to apache2-conf without upgrading
  to apache2
- Add back /var/apache-mm for the same reason
- Don't require apache2-devel, since it's not really needed.

* Thu Sep 05 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-10mdk
- Correct migration scripts bugs, and split the functions into different
  files.

* Wed Sep 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-9mdk
- Complete mod_ssl-migrate
- Complete advx-checkifmigrate

* Wed Sep 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-8mdk
- Macroize according to ADVX policy on www.advx.org/devel/policy.php
- added C version of advxsplitlogfile by Anders Melchiorsen <anders@kalibalik.dk>

* Tue Sep 03 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX-7mdk
- Add favicon

* Wed Aug 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40-6mdk
- *Lots* of changes for Apache 2.0.40
- completely macroized specfile
- renamed package apache2-conf

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.26-2mdk
- add apache user

* Tue Jun 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.26-1mdk
- apache 1.3.26.
- EAPI 2.8.10.

* Mon Apr 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.24-1mdk
- apache 1.3.24.
- EAPI 2.8.8.

* Wed Mar 13 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.23-4mdk
- IMPORTANT FIX: add Document root in httpd-perl.conf
- Fixed URL in Spec file

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.23-3mdk
- Removed the restrictive settings on the /addon-modules directory, and 
  replaced it by a .htaccess so people can read the documentation on the
  modules remotely, by removing the .htaccess.
- s/advx.com/advx.org/ in HOWTO-GET-MODULES file

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.23-2mdk
- Fix manual path
- Fix configuration files to be more secure, and also to be easier to parse
  by Frontpage and other addons.
- The old advx.com is broken, the new site is www.advx.org
- Misc. fixes to index.shtml (yes, I removed my name from the index.shtml, 
  some people did not like it)

* Mon Feb 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.23-1mdk
- Apache 1.3.23.
- EAPI 2.8.6.

* Thu Jan 10 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.22-3mdk
- advxsplitlogfile splits using hours, not minutes.
- Require on lynx (used in httpd.init)

* Wed Oct 17 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.3.22-2mdk
- use a more secure commonhttpd.conf; disable Indexes pretty much everywhere

* Tue Oct 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.22-1mdk
- apache 1.3.22.

* Tue Oct 09 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.20-4mdk
- Remove use of RPM_SOURCE_DIR (AKA specfile cleaning).
- make rpmlint happier.

* Wed Sep 12 2001 David BAUDENS <baudens@mandrakesoft.com> 1.3.20-3mdk
- Change default Mandrake Linux image

* Fri Aug 24 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.20-2mdk
- fix init script bug

* Tue Jul 10 2001 Philippe Libat <philippe@mandrakesoft.com>  1.3.20-1mdk
- new apache version

* Fri Apr 13 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19-3mdk
- fix prereqs

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19-2mdk
- fixed bug with mod_perl upgrade
- use _post_service and _preun_service macros
- unset some unneeded (and potentially insecure) environment variables

* Sun Mar 25 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19-1mdk
- Created this new package for configuration files
  see description for more info
- Extensive rewrite of the configuration files
- New mod_perl configuration
- New virtualhost logging and dynamic log rotation
- New utilities for adding/removing modules and upgrades
- Apache and apache_mod-perl now use the same set of modules
- Added some SuSE compatibility
