#
# spec file for package apache-conf
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		apache-conf
%define version		2.0.53
%define release		7avx

%define compat_dir	/etc/httpd
%define compat_conf	/etc/httpd/conf


Summary:	Configuration files for Apache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org
Source1:	httpd2.conf
Source2:	httpd2-perl.conf
Source3:	mime.types
Source4:	apache-2.0.40-testscript.pl
Source5:	magic.default
Source6:	commonhttpd.conf
Source10:	Vhosts.conf
Source11:	DynamicVhosts.conf
Source12:	VirtualHomePages.conf
Source14:	favicon.ico.bz2
Source20:	index.shtml
Source21:	annvix.html
Source22:	optim.html
Source23:	logo.gif
Source24:	apacheicon.gif
Source25:	medbutton.png
Source26:	stamp.gif
Source29:	annvix-icons.tar.bz2
Source30:	advxaddmod
Source31:	advxdelmod
Source32:	advxfixconf
Source33:	advxlogserverstatus
Source34:	advxsplitlogfile
Source35:	advxsplitlogfile.c
Source40:	advx-checkifmigrate
Source41:	mod_ssl-migrate-20
Source42:	advx-migrate-httpd.conf
Source43:	advx-migrate-httpd-perl.conf
Source44:	advx-migrate-commonhttpd.conf
Source45:	advx-migrate-vhosts.conf
Source46:	advx-cleanremove
Source51:	httpd.conf
Source52:	httpd-perl.conf
Source53:	ap13chkconfig
Source98:	robots.txt
Source99:	README.apache-conf
Source100:	httpd2.run
Source101:	httpd2-log.run
Source102:	03_apache2.afterboot
Source103:	fileprotector.conf

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.20-1mdk

Requires:	lynx >= 2.8.5
Provides:	apache2-conf
#JMD: We have to do this here, since files have moved
Obsoletes:	apache-common
PreReq:		rpm-helper, afterboot

%description
This package contains configuration files for apache and apache-mod_perl.
It is necessary for operation of the apache webserver.

Having those files into a separate modules provides better customization for
OEMs and ISPs, who can modify the look and feel of the %{name} webserver
without having to re-compile the whole suite to change a logo or config
file.


%prep
%setup -q -c -T -n %{name}-%{version}
cp %{SOURCE35} .


%build
diet gcc -Os -s -static -nostdinc -o advxsplitlogfile-DIET advxsplitlogfile.c
gcc %{optflags} -o advxsplitlogfile advxsplitlogfile.c


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}/var/www/html
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}/var/log/httpd
mkdir -p %{buildroot}/var/www
mkdir -p %{buildroot}/var/www/cgi-bin
mkdir -p %{buildroot}/var/www/perl
mkdir -p %{buildroot}/var/www/html/addon-modules
mkdir -p %{buildroot}/var/cache/httpd
mkdir -p %{buildroot}/var/apache-mm
mkdir -p %{buildroot}%{_datadir}/ADVX
mkdir -p %{buildroot}%{_libdir}/ADVX/contribs
mkdir -p %{buildroot}%{_libdir}/ADVX/contribs

install -m 0755 advxsplitlogfile-DIET %{buildroot}%{_libdir}/ADVX/contribs/
install -m 0755 advxsplitlogfile %{buildroot}%{_libdir}/ADVX/contribs/

install -m 0755 %{SOURCE40} %{buildroot}%{_datadir}/ADVX
install -m 0755 %{SOURCE41} %{buildroot}%{_datadir}/ADVX
install -m 0755 %{SOURCE42} %{buildroot}%{_datadir}/ADVX
install -m 0755 %{SOURCE43} %{buildroot}%{_datadir}/ADVX
install -m 0755 %{SOURCE44} %{buildroot}%{_datadir}/ADVX
install -m 0755 %{SOURCE45} %{buildroot}%{_datadir}/ADVX
install -m 0755 %{SOURCE46} %{buildroot}%{_datadir}/ADVX

ln -sf ../../var/log/httpd %{buildroot}%{compat_dir}/logs

install -D -m 0755 %{SOURCE4} %{buildroot}/var/www/cgi-bin/test.cgi
install -D -m 0755 %{SOURCE4} %{buildroot}/var/www/perl/test.pl

install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf/httpd2.conf
install -D -m 0644 %{SOURCE51} %{buildroot}%{_sysconfdir}/httpd/conf/httpd.conf
install -D -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/httpd/conf/commonhttpd.conf
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf/httpd2-perl.conf
install -D -m 0644 %{SOURCE52} %{buildroot}%{_sysconfdir}/httpd/conf/httpd-perl.conf
install -D -m 0644 %{SOURCE103} %{buildroot}%{_sysconfdir}/httpd/conf/fileprotector.conf

#For compatibility if someone installs Apache 2.0, then changes their
#mind and installs 1.3 instead, they will need the config files!
mkdir -p %{buildroot}%{_datadir}/ADVX/compat
install -D -m 0644 %{SOURCE51} %{buildroot}%{_datadir}/ADVX/compat/httpd.conf
install -D -m 0644 %{SOURCE52} %{buildroot}%{_datadir}/ADVX/compat/httpd-perl.conf

cd %{buildroot}%{_sysconfdir}/httpd/conf/
install -d -m 0755 %{buildroot}%{_sysconfdir}/httpd/conf/addon-modules
install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf/apache-mime.types
install -D -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/httpd/conf/magic.default
cp -p magic.default magic
install -d -m 0755 vhosts
install -D -m 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/httpd/conf/vhosts/Vhosts.conf
install -D -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/httpd/conf/vhosts/DynamicVhosts.conf
install -D -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/httpd/conf/vhosts/VirtualHomePages.conf

# install our icon
# JMD: We need an ADVX icon ;-)
bzcat %{SOURCE14} > %{buildroot}/var/www/html/favicon.ico

#install misc documentation and logos
install -D -m 0644 %{SOURCE20} %{buildroot}/var/www/html/index.shtml
install -D -m 0644 %{SOURCE22} %{buildroot}/var/www/html/optim.html
install -D -m 0644 %{SOURCE21} %{buildroot}/var/www/html/platform.html
install -d -m 0755 %{buildroot}/var/www/icons/
install -D -m 0644 %{SOURCE23} %{buildroot}/var/www/icons/logo.gif
install -D -m 0644 %{SOURCE24} %{buildroot}/var/www/icons/apacheicon.gif
install -D -m 0644 %{SOURCE26} %{buildroot}/var/www/icons/stamp.gif
install -D -m 0644 %{SOURCE25} %{buildroot}/var/www/icons/medbutton.png
pushd %{buildroot}/var/www/icons/
tar xjf %{SOURCE29}
popd

install -d -m 0755 %{buildroot}/var/www/html/addon-modules/
echo "Get all the latest modules at <a href=http://www.advx.org>www.advx.org</a>" \
    >> %{buildroot}/var/www/html/addon-modules/HOWTO_get_modules.html
cat << EOF > %{buildroot}/var/www/html/addon-modules/.htaccess
Order deny,allow
Deny from all
Allow from 127.0.0.1
ErrorDocument 403 "This directory can only be viewed from localhost. If you don't care about this security feature, remove /var/www/html/addon-modules/.htaccess.
EOF

# install log rotation stuff
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d

cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} << EOF
/var/log/httpd/*log
{
    size=2000M
    rotate 5
    monthly
    missingok
    nocompress
    notifempty
    postrotate
	[[ -d /service/httpd2 ]] && runsvctrl h /service/httpd2 >/dev/null 2>&1
    endscript
}
EOF

install -m 0755 %{SOURCE30} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE31} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE32} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE33} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE34} %{buildroot}%{_sbindir}
install -m 0755 %{SOURCE53} %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_docdir}/apache2-conf-%{version}
install -m 0644 %{SOURCE99} %{buildroot}%{_docdir}/apache2-conf-%{version}

mkdir -p %{buildroot}%{_srvdir}/httpd2/log
mkdir -p %{buildroot}%{_srvlogdir}/httpd2
install -m 0740 %{SOURCE100} %{buildroot}%{_srvdir}/httpd2/run
install -m 0740 %{SOURCE101} %{buildroot}%{_srvdir}/httpd2/log/run

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE102} %{buildroot}%{_datadir}/afterboot/03_apache2

install -m 0644 %{SOURCE98} %{buildroot}/var/www/html/robots.txt


%pre
%_pre_useradd apache /var/www /bin/sh 74
%_mkafterboot

%post
if [ $1 = "1" ]; then
  %{_datadir}/ADVX/advx-checkifmigrate
fi
%_post_srv httpd2

%preun
%_preun_srv httpd2

%postun
%_postun_userdel apache
%_mkafterboot


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%dir %{compat_dir}
%dir %{compat_dir}/logs
%dir %{_sysconfdir}/httpd/conf.d
%dir /var/log/httpd
%dir %{_sysconfdir}/httpd/conf
%{_datadir}/ADVX/*
%config %ghost %{_sysconfdir}/httpd/conf/httpd.conf
%config %ghost %{_sysconfdir}/httpd/conf/httpd-perl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd2.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/commonhttpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd2-perl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/fileprotector.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%config(noreplace) %{_sysconfdir}/httpd/conf/apache-mime.types
%config(noreplace) %{_sysconfdir}/httpd/conf/magic.default
%config(noreplace) %{_sysconfdir}/httpd/conf/vhosts
%dir %{_sysconfdir}/httpd/conf/addon-modules
%dir /var/www/html/addon-modules
/var/www/html/addon-modules/*
%config(noreplace) /var/www/html/addon-modules/.htaccess
%attr(0755,apache,apache) %dir /var/www
%dir /var/www/cgi-bin
/var/www/cgi-bin/*
%dir /var/www/perl
/var/www/perl/*
%dir /var/www/icons
/var/www/icons/*
%attr(0755,apache,apache) %dir /var/www/html
/var/www/html/platform.html
/var/www/html/optim.html
%config(noreplace) /var/www/html/favicon.ico
%config(noreplace) /var/www/html/index.shtml
%config(noreplace) /var/www/html/robots.txt
%attr(-,apache,apache) %dir /var/cache/httpd
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_docdir}/apache2-conf-%{version}/README.apache-conf
%{_libdir}/ADVX/*
%dir %attr(0750,root,admin) %{_srvdir}/httpd2
%dir %attr(0750,root,admin) %{_srvdir}/httpd2/log
%attr(0740,root,admin) %{_srvdir}/httpd2/run
%attr(0740,root,admin) %{_srvdir}/httpd2/log/run
%dir %attr(0750,logger,logger) %{_srvlogdir}/httpd2
%{_datadir}/afterboot/03_apache2


%changelog
* Fri Aug 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-7avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-5avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-4avx
= user logger for logging

* Sun Feb 27 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-3avx
- remove more ADVX-related stuff
- remove the peruser, perchild, and metuxmpm sections from the config
  files
- use fileprotector.conf as fileprotector.conf and don't accidentally
  copy the httpd2-perl.conf file
- rename S29
- remove webapps.d support

* Sun Feb 27 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-2avx
- put back our index.shtml and optim.html
- merge back changes to commonhttpd.conf

* Fri Feb 25 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-1avx
- 2.0.53
- get rid of ADVX stuff
- s/apache2/httpd2/ for the %%_srv macros
- handle mod_perl2 access from the apache2-mod_perl config (oden)
- add new dumpio module to the config (oden)
- merge changes from the httpd2-VANILLA.conf file (oden)
- S101: add means to secure sensible data (oden)

* Fri Feb 04 2005 Vincent Danen <vdanen@annvix.org> 2.0.52-3avx
- rebuild against new dietlibc

* Fri Dec 03 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-2avx
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

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-1avx
- 2.0.52
- move runscripts and afterboot snippet here from apache2
- update the default index.shtml and related pages; make it more
  Annvix specific and clean it up (what an awful mess)

* Fri Sep 17 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-7avx
- update logrotate script

* Tue Sep 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-6avx
- by default, set ServerTokens to Prod (from Full) and ServerSignature
  to Off (from On)

* Mon Jun 28 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-5avx
- missed a few references to OpenSLS; fixed

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-4avx
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
