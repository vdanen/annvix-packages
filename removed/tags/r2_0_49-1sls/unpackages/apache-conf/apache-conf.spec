%define name	apache-conf
%define version	2.0.49
%define release	1sls

# OE: conditional switches
#(ie. use with rpm --rebuild):
#	--with diet	Compile advxsplitlogfile against dietlibc
# regarding "--with diet", check: http://d-srv.com/Cooker/apache2-conf-2_0_40ADVX-14mdk.html

%define build_diet 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}

%define compat_dir	/etc/httpd
%define compat_conf	/etc/httpd/conf


Summary:	Configuration files for Apache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://www.advx.org
Source0:	httpd.init.mandrake
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
Source21:	opensls.html
Source22:	optim.html
Source23:	logo.gif
Source24:	apacheicon.gif
Source25:	medbutton.png
Source26:	stamp.gif
Source29:	ADVX-icons.tar.bz2
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
Source54:	advxrun1.3
Source55:	advxrun2.0
Source99:	README.apache-conf

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildPreReq:	ADVX-build >= 9.2
%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.20-1mdk
%endif

Requires:	lynx >= 2.8.5
Provides:	apache2-conf
Provides:	apache-conf = 1.3.28
Provides:	ADVXpackage
Provides:	AP20package
#JMD: We have to do this here, since files have moved
Obsoletes:	apache-common
PreReq:		rpm-helper

%description
This package contains configuration files for apache and 
apache-mod_perl. 
It is necessary for operation of the apache webserver.

Having those files into a separate modules provides better customization for
OEMs and ISPs, who can modify the look and feel of the %{name} webserver
without having to re-compile the whole suite to change a logo or config
file.

%prep

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
cp %{SOURCE35} .

%if %{build_diet}
    # OE: use the power of dietlibc
    diet gcc %{optflags} -s -static -nostdinc -o advxsplitlogfile-DIET advxsplitlogfile.c
%else
    gcc %{optflags} -o advxsplitlogfile advxsplitlogfile.c
%endif

%install

mkdir -p %{buildroot}%{compat_conf}
mkdir -p %{buildroot}%{ap_confd}
mkdir -p %{buildroot}%{ap_htdocsdir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{ap_logfiledir}
mkdir -p %{buildroot}%{ap_datadir}
mkdir -p %{buildroot}%{ap_datadir}/cgi-bin
mkdir -p %{buildroot}%{ap_datadir}/perl
mkdir -p %{buildroot}%{ap_webdoc}
mkdir -p %{buildroot}%{ap_proxycachedir}
mkdir -p %{buildroot}/var/apache-mm
mkdir -p %{buildroot}%{ADVXdir}
mkdir -p %{buildroot}%{_libdir}/ADVX/contribs
mkdir -p %{buildroot}%{_libdir}/ADVX/contribs

%if %{build_diet}
    install -m755 advxsplitlogfile-DIET %{buildroot}%{_libdir}/ADVX/contribs/
%else
    install -m755 advxsplitlogfile %{buildroot}%{_libdir}/ADVX/contribs/
%endif

install -m755 %{SOURCE40} %{buildroot}%{ADVXdir}
install -m755 %{SOURCE41} %{buildroot}%{ADVXdir}
install -m755 %{SOURCE42} %{buildroot}%{ADVXdir}
install -m755 %{SOURCE43} %{buildroot}%{ADVXdir}
install -m755 %{SOURCE44} %{buildroot}%{ADVXdir}
install -m755 %{SOURCE45} %{buildroot}%{ADVXdir}
install -m755 %{SOURCE46} %{buildroot}%{ADVXdir}

ln -sf ../..%{ap_logfiledir} %{buildroot}%{compat_dir}/logs

install -D -m755 %{SOURCE4} %{buildroot}%{ap_datadir}/cgi-bin/test.cgi
install -D -m755 %{SOURCE4} %{buildroot}%{ap_datadir}/perl/test.pl

install -D -m644 %{SOURCE1} %{buildroot}%{compat_conf}/httpd2.conf
install -D -m644 %{SOURCE51} %{buildroot}%{compat_conf}/httpd.conf
install -D -m644 %{SOURCE6} %{buildroot}%{compat_conf}/commonhttpd.conf
install -D -m644 %{SOURCE2} %{buildroot}%{compat_conf}/httpd2-perl.conf
install -D -m644 %{SOURCE52} %{buildroot}%{compat_conf}/httpd-perl.conf

#For compatibility if someone installs Apache 2.0, then changes their
#mind and installs 1.3 instead, they will need the config files!
mkdir -p %{buildroot}%{ADVXdir}/compat
install -D -m644 %{SOURCE51} %{buildroot}%{ADVXdir}/compat/httpd.conf
install -D -m644 %{SOURCE52} %{buildroot}%{ADVXdir}/compat/httpd-perl.conf

cd %{buildroot}%{compat_conf}/
install -d -m755 %{buildroot}%{ap_addonconf}
install -D -m644 %{SOURCE3} %{buildroot}%{compat_conf}/apache-mime.types
install -D -m644 %{SOURCE5} %{buildroot}%{compat_conf}/magic.default
cp -p magic.default magic
install -d -m755 vhosts
install -D -m644 %{SOURCE10} %{buildroot}%{compat_conf}/vhosts/Vhosts.conf
install -D -m644 %{SOURCE11} %{buildroot}%{compat_conf}/vhosts/DynamicVhosts.conf
install -D -m644 %{SOURCE12} %{buildroot}%{compat_conf}/vhosts/VirtualHomePages.conf

# install our icon
# JMD: We need an ADVX icon ;-)
bzcat %{SOURCE14} > %{buildroot}%{ap_htdocsdir}/favicon.ico

#install misc documentation and logos
install -D -m644 %{SOURCE20} %{buildroot}/%{ap_htdocsdir}/index.shtml
install -D -m644 %{SOURCE22} %{buildroot}/%{ap_htdocsdir}/optim.html
install -D -m644 %{SOURCE21} %{buildroot}/%{ap_htdocsdir}/platform.html
install -d -m755 %{buildroot}/%{ap_datadir}/icons/
install -D -m644 %{SOURCE23} %{buildroot}/%{ap_datadir}/icons/logo.gif
install -D -m644 %{SOURCE24} %{buildroot}/%{ap_datadir}/icons/apacheicon.gif
install -D -m644 %{SOURCE26} %{buildroot}/%{ap_datadir}/icons/stamp.gif
install -D -m644 %{SOURCE25} %{buildroot}/%{ap_datadir}/icons/medbutton.png
pushd %{buildroot}/%{ap_datadir}/icons/
tar xjf %{SOURCE29}
popd

install -d -m755 %{buildroot}%{ap_webdoc}/
echo "Get all the latest modules at <a href=http://www.advx.org>www.advx.org</a>" \
	>> %{buildroot}%{ap_webdoc}/HOWTO_get_modules.html
cat << EOF > %{buildroot}%{ap_webdoc}/.htaccess
Order deny,allow
Deny from all
Allow from 127.0.0.1
ErrorDocument 403 "This directory can only be viewed from localhost. If you don't care about this security feature, remove /var/www/html/addon-modules/.htaccess.
EOF

# install log rotation stuff
install -d -m755 %{buildroot}%{_sysconfdir}/logrotate.d

cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} << EOF
%{ap_logfiledir}/access_log %{ap_logfiledir}/error_log %{ap_logfiledir}/agent_log %{ap_logfiledir}/referer_log %{ap_logfiledir}/apache_runtime_status
%{ap_logfiledir}/ssl_mutex %{ap_logfiledir}/ssl_access_log %{ap_logfiledir}/ssl_error_log %{ap_logfiledir}/ssl_agent_log %{ap_logfiledir}/ssl_request_log 
%{ap_logfiledir}/suexec_log 
{
    rotate 5
    monthly
    missingok
    nocompress
    prerotate
	svc -h /service/apache; svc -h /service/apache2
    endscript
    postrotate
	svc -h /service/apache; svc -h /service/apache2
    endscript
}
EOF

install -m755 %{SOURCE30} %{buildroot}%{_sbindir}
install -m755 %{SOURCE31} %{buildroot}%{_sbindir}
install -m755 %{SOURCE32} %{buildroot}%{_sbindir}
install -m755 %{SOURCE33} %{buildroot}%{_sbindir}
install -m755 %{SOURCE34} %{buildroot}%{_sbindir}
install -m755 %{SOURCE53} %{buildroot}%{_sbindir}
install -m755 %{SOURCE54} %{buildroot}%{_sbindir}
install -m755 %{SOURCE55} %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_docdir}/apache2-conf-%{version}
install -m644 %{SOURCE99} %{buildroot}%{_docdir}/apache2-conf-%{version}

#Apache 1.3 compatibility
mkdir -p %{buildroot}%{_libdir}/apache-extramodules
mkdir -p %{buildroot}%{ap_base}/apache-extramodules
#link modules dir
ln -sf ../..%{_libdir}/apache-extramodules \
        %{buildroot}%{ap_base}/extramodules

%pre
%_pre_useradd apache /var/www /bin/sh 74

%post
if [ $1 = "1" ]; then
  %{ADVXdir}/advx-checkifmigrate
fi
%_post_srv apache
%_post_srv apache2
%ADVXpost

%preun
%_preun_srv apache
%_preun_srv apache2
%ADVXpost

%postun
%_postun_userdel apache

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#Clean up some
[ "advxsplitlogfile" != "/" ] && rm -f advxsplitlogfile*

%files 
%defattr(-,root,root)
%dir %{compat_dir}
%dir %{compat_dir}/logs
%dir %{ap_confd}
%dir %{ap_logfiledir}
%dir %{compat_conf}
%{ADVXdir}/*
%config %ghost %{compat_conf}/httpd.conf
%config %ghost %{compat_conf}/httpd-perl.conf
%config(noreplace) %{compat_conf}/httpd2.conf
%config(noreplace) %{compat_conf}/commonhttpd.conf
%config(noreplace) %{compat_conf}/httpd2-perl.conf
%config(noreplace) %{compat_conf}/magic
%config(noreplace) %{compat_conf}/apache-mime.types
%config(noreplace) %{compat_conf}/magic.default
%config(noreplace) %{compat_conf}/vhosts
%dir %{ap_addonconf}
%dir %{ap_webdoc}
%{ap_webdoc}/*
%config(noreplace) %{ap_webdoc}/.htaccess
%dir %{ap_datadir}
%dir %{ap_datadir}/cgi-bin
%{ap_datadir}/cgi-bin/*
%dir %{ap_datadir}/perl
%{ap_datadir}/perl/*
%dir %{ap_datadir}/icons
%{ap_datadir}/icons/*
%dir %{ap_htdocsdir}
%{ap_htdocsdir}/platform.html
%{ap_htdocsdir}/optim.html
%config(noreplace) %{ap_htdocsdir}/favicon.ico
%config(noreplace) %{ap_htdocsdir}/index.shtml
%attr(-,apache,apache) %dir %{ap_proxycachedir}
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_docdir}/apache2-conf-%{version}/README.apache-conf
%{_libdir}/ADVX/*
%{ap_base}/extramodules
#JMD: For compatibility with Apache 1.3
#JMD: *never remove this!* 1333 is the *right* permission.
%attr(1333,apache,apache) %dir /var/apache-mm

%changelog
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
