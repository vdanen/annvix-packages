%define name	apache
%define version	1.3.29
%define release	2sls

#New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}

%{expand:%%define mm_major %(mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\1/')}
%{expand:%%define mm_minor %(mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\2/')}
%define mm_version %{mm_major}.%{mm_minor}

%define apache_version		%{version}
%define apache_release		%{release}
%define EAPI_version		2.8.16
%define modssl_apache_version	%{apache_version}

Summary:	The most widely used Web server on the Internet.
Name:		%{name}
Version:	%{apache_version}
Release:	%{apache_release}
License:	Apache License
Group:		System/Servers
URL:		http://www.advx.org
Source0:	apache_%{version}.tar.gz
Source1:	apache_%{version}.tar.gz.asc
Source2:	http://www.modssl.org/source/mod_ssl-%{EAPI_version}-%{modssl_apache_version}.tar.gz
Source3:	http://www.modssl.org/source/mod_ssl-%{EAPI_version}-%{modssl_apache_version}.tar.gz.asc
Source4:	README.ADVX
Patch1:		apache_1.3.11-apxs.patch.bz2
Patch2:		apache_1.3.26-srvroot.patch.bz2
#Patch3:	apache_1.3.20-nondbm.patch.bz2
Patch3:		apache-1.3.23-dbm.patch.bz2
Patch4:		Configuration.diff.bz2
Patch5:		apache-1.3.29-baseversion.patch.bz2
Patch6:		apache-1.3.14-mkstemp.patch.bz2
Patch8:		apache-1.3.20.manpage.patch.bz2
Patch9:		apache-1.3.22-man.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildConflicts:	BerkeleyDB-devel
BuildRequires:	ADVX-build >= 1.2
BuildRequires:	libmm-devel = %{mm_major}.%{mm_minor}
BuildRequires:	perl >= 0:5.601
BuildRequires:	libgdbm-devel
BuildRequires:	db3-devel
BuildRequires:	db1-devel
BuildRequires:	glibc-devel
BuildRequires:	openssl-devel

Prereq:		apache-modules >= %{apache_version}-%{apache_release}
Prereq:		apache-conf >= %{apache_version}
Prereq:		apache-common >= %{apache_version}-%{apache_release}
Prereq:		rpm-helper
Prereq:		mm = %{mm_major}.%{mm_minor}
Provides:	webserver 
Provides:	ADVXpackage
Provides:	AP13package

%description
Apache is a powerful, full-featured, efficient and freely-available
Web server. Apache is also the most popular Web server on the
Internet.

This version of Apache includes many optimizations, Extended
Application Programming Interface (EAPI), Shared memory module, hooks for
SSL modules, and several patches/cosmetic improvements.

It is also fully modular, and many modules are available in pre-compiled 
format, like PHP4, the Hotwired XSSI module and Apache-ASP. Also included are
special patches to enable FrontPage 2000 support (see mod_frontpage package).

%package modules
Summary:	Standard modules for Apache
Group:		System/Servers
Prereq:		apache-common >= %{apache_version}-%{apache_release}
Prereq:		mm = %{mm_major}.%{mm_minor}
Provides:	ADVXpackage
Provides:	AP13package

%description modules
This package contains standard modules for Apache 1.3. 
It is required for normal operation of the web server. 
The reason we split these into a separate package is they can be used 
also with the apache-mod_perl package.


%package devel
Summary:	Module development tools for Apache 1.3.
Group:		Development/C
Provides:	secureweb-devel
Obsoletes:	secureweb-devel
Prereq:		mm = %{mm_major}.%{mm_minor}
Prereq:		mm-devel = %{mm_major}.%{mm_minor}
Prereq:		perl >= 0:5.601
Requires:	libgdbm-devel
Requires:	db1-devel
#Do not require libdb3.3-devel anymore, since there is a conflict
#between libdb3.3 and libdb4.0 devel packages. This messes the upgrade
#Requires libdb3.3-devel
Requires:	glibc-devel
Provides:	ADVXpackage
Provides:	AP13package

%description devel
The apache-devel package contains the header files and libraries 
for Apache 1.3 and the APXS binary you'll need to build Dynamic
Shared Objects (DSOs) for Apache.

If you are installing the Apache 1.3 server and
you want to be able to compile or develop additional modules
for it, you'll need to install this package.

%package source
Summary:	Apache Source
Group:		System/Servers
Prereq:		mm = %{mm_major}.%{mm_minor}
Prereq:		mm-devel = %{mm_major}.%{mm_minor}
#No use to install it if you don't have libgdbm.so and libpthread.so!
Requires:	db1-devel
Requires:	libgdbm-devel
Requires:	glibc-devel
#Do not require libdb3.3-devel anymore, since there is a conflict
#between libdb3.3 and libdb4.0 devel packages. This messes the upgrade
#Requires libdb3.3-devel
Provides:	ADVXpackage
Provides:	AP13package

%description source
The Apache 1.3 Source, including Mandrake patches and EAPI. 
Use this package to build apache-mod_perl, or your own custom version.

%prep
#unpack apache.
%setup -q -n apache_%{apache_version}
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 
%patch4 -p1
%patch5 -p0
%patch6 -p1 -b .mkstemp
%patch8 -p0
%patch9 -p0

#Correct layout 
perl -pi -e 's|" PLATFORM "|%{distribution}/%{apache_release}|;' \
	src/main/http_main.c
perl -pi -e 's|/home/httpd|%{ap_datadir}|; \
			 s|\$prefix/man|%{_mandir}|;' \
		config.layout

#Correct perl paths
find -type f|xargs perl -pi -e " s|/usr/local/bin/perl|%{_bindir}/perl|g; \
	s|/usr/local/bin/perl5|%{_bindir}/perl|g; \
	s|/path/to/bin/perl|%{_bindir}/perl|g; \
	" 

cp %{SOURCE4} .

#Fix manual (move *.html.html to *.html)
find htdocs/manual|grep "~"| xargs rm -f
pushd htdocs/manual
for i in `ls *.html.html`
do
    good=`basename $i .html`
    mv -v $good.html $good
done
for i in *
do
    if [ -d $i ]
    then
        cd $i
	for j in `ls *.html.html`
	do
	    good=`basename $j .html`
	    mv $good.html $good
	done
	cd ..
    fi
done
popd


#### EAPI
%setup -q -n apache_%{apache_version} -T -D -b 2

ssl="../mod_ssl-%{EAPI_version}-%{modssl_apache_version}"
mv $ssl/pkg.eapi/*.c src/ap/
mv $ssl/pkg.eapi/*.h src/include/ 
mv $ssl/pkg.addon/*.c src/modules/extra
cp src/modules/extra/mod_define.c src/modules/standard
perl -p -i -e "s/^--- /--- .\//g; s/^\+\+\+ /\+\+\+ .\//g" \
	$ssl/pkg.addon/addon.patch $ssl/pkg.eapi/eapi.patch
patch -p1 < $ssl/pkg.addon/addon.patch
patch -p1 < $ssl/pkg.eapi/eapi.patch
#Correct MM_CORE_PATH so apache works as a non-root user
perl -pi -e 's|logs/mm|/var/apache-mm/mm|;' \
	src/include/httpd.h

cp $ssl/pkg.addon/mod_define.html \
	htdocs/manual/mod/mod_define.html

####
#Copy pre-patched Apache source so we can package an apache-source rpm and
#use it to build mod_perl
FILZ=`ls`
mkdir -p usr/src/apache_%{apache_version}
cp -dpR $FILZ usr/src/apache_%{apache_version}

# make mr. lint happy and do some house cleaning...
pushd usr/src/apache_%{apache_version}
    for f in `find . -type f -name ".orig"` \
	`find . -type f -name ".deps"` \
	`find . -type f -name ".indent.pro"` \
	`find . -type f -name ".gdbinit"`; do
	rm -f $f
    done
popd

%build

%serverbuild

#Add a useless --libdir option to the configure script
#to fool rpmlint in giving one less error ;-)
perl -pi -e "s|--mandir=\*\)|--libdir=\*\)\n\t\t;;\n\t--mandir=\*\)|;" configure

echo "### define configure flags"
APVARS="--prefix=%{_prefix} \
	--libexecdir=%{_libdir}/apache \
	--with-layout=ADVX \
	--disable-rule=WANTHSREGEX \
        --with-perl=%{_bindir}/perl \
	--enable-module=all \
	--enable-module=auth_digest \
	--disable-rule=expat \
	--enable-shared=max \
	--manualdir=%{ap_htdocsdir}/manual \
	--enable-rule=SHARED_CORE \
	"

# Why was dbm disabled?
#	--disable-module=auth_dbm \

#Copy configure flags to a file in the apache-source rpm.
echo $APVARS > usr/src/apache_%{apache_version}/APVARS

echo "### Build Apache"
#JMD: Zero out the CFLAGS that the damn serverbuild macro exported,
#     Apache needs to use OPTIM, otherwise apxs will not work 
export CFLAGS=""
#JMD: -fno-strict-aliasing is used by mod_perl
OPTIM="$RPM_OPT_FLAGS -fno-strict-aliasing" \
	CFLAGS="-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" \
	EAPI_MM=SYSTEM \
	LIBS="-lgdbm -lpthread" \
./configure --enable-rule=EAPI --libdir=%{_libdir} \
	$APVARS

if [ x"$SMP" != x"" ]; then
	make MAKE="make -j $SMP -k"
else
	make
fi

%install
rm -rf %{buildroot}
mkdir %{buildroot}

# install source
cp -a usr %{buildroot}

#Install Apache
make root=%{buildroot} install

rm -f %{buildroot}%{_mandir}/man8/suexec.8
rm -f %{buildroot}%{_mandir}/man8/httpd.8

find -type f|grep "\.a$"|xargs -iFL cp -f FL %{buildroot}%{_libdir}/apache

mkdir -p %{buildroot}/var/apache-mm
mkdir -p %{buildroot}%{ap_webdoc}

rm -fr %{buildroot}/var/
rm -fr %{buildroot}%{_bindir}
rm -f %{buildroot}%{_sbindir}/ab
rm -f %{buildroot}%{_sbindir}/logresolve
rm -f %{buildroot}%{_sbindir}/rotatelogs
rm -f %{buildroot}%{ap_base}/conf/*
rm -f %{buildroot}%{_sbindir}/apachectl
rm -f %{buildroot}%{_mandir}/man1/*
rm -f %{buildroot}%{_mandir}/man8/ab*
rm -f %{buildroot}%{_mandir}/man8/apachectl*
rm -f %{buildroot}%{_mandir}/man8/logresolve*
rm -f %{buildroot}%{_mandir}/man8/rotatelogs*
rm -f %{buildroot}%{_mandir}/man8/apxs*

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

[ "../mod_ssl-%{EAPI_version}-%{modssl_apache_version}" != "/" ] && rm -rf ../mod_ssl-%{EAPI_version}-%{modssl_apache_version}

%pre
#Check config file sanity
%AP13pre

%post
#JMD: do *not* use _post_service here, it is used in apache-conf, since we
#can have both apache and apache-mod_perl
%ADVXpost

%postun
#JMD: do *not* use _post_service here, otherwise it will uninstall
#apache-mod_perl as well!!
%ADVXpost

%files 
%defattr(-,root,root)
%{_sbindir}/httpd
#%{_mandir}/man8/httpd.*
%doc README.ADVX

%files modules
%defattr(-,root,root)
%{_libdir}/apache/*.exp
%{_libdir}/apache/*.ep
%{_libdir}/apache/*.so
%doc README.ADVX

%files devel
%defattr(-,root,root)
%{_includedir}/apache
%{_libdir}/apache/*.a
%{_sbindir}/apxs
#%{_mandir}/man8/apxs.*
%doc README.ADVX

%files source
%defattr(-,root,root)
/usr/src/apache_%{apache_version}
%doc README.ADVX

%changelog
* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.3.29-2sls
- OpenSLS build
- tidy spec

* Sat Nov 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.29-1mdk
- apache v1.3.29
- EAPI v2.8.16
- misc spec file fixes
- rediffed P5
- drop P10, it's included
- really cleanup in %%clean

* Wed Sep 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.28-4mdk
- BuildRequires: libmm-devel, not libmm1-devel

* Mon Sep 08 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.28-3mdk
- fix ASF bug #21737 (cgi zombie processes)

* Thu Sep 04 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.28-2mdk
- remove conflicting man page (is in apache-common now)

* Mon Aug 25 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.28-1mdk
- apache v1.3.28
- EAPI v2.8.15
- misc spec file fixes
- rediffed P5

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.27-11mdk
- BuildRequires: db3-devel, libgdbm-devel

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 1.3.27-10mdk
- Rebuild to fix bad signature

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.27-9mdk
- rebuilt against new mm
- misc spec file fixes

* Fri Feb 28 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-8mdk
- Do not require libdb3.3-devel anymore, since there is a conflict
  between libdb3.3 and libdb4.0 devel packages. This messes the upgrade

* Thu Feb 20 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-7mdk
- pickup libap.a, libmain.a, libos.a and libstandard.a, and put them in
  apache-devel
- removed apache-common and apache-manual, they will be split into their
  own packages so we can put apache-modules into cooker main.

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-6mdk
- add AP13pre macro to make sure about the sanity of the conf files
- remove the warning messages from apxs, they are not necessery and confuse
  the user and some scripts
- re-add mod_auth_dbm

* Tue Jan 07 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-5mdk
- Use ADVX-build to generate macros
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 
- Likewise, add Provides: AP13package and AP20package in the same
  manner

* Thu Jan 02 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-4mdk
- rebuilt for new mm version
- enable SHARED_CORE for Kylix compatibility

* Fri Nov 15 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.27-3mdk
- Make it lib64 aware

* Fri Nov  8 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-2mdk
- Rebuild for Cooker

* Mon Oct 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-1mdk
- Security update
- New version

* Fri Jul 12 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.26-6mdk
- don't use apache for document root (possible minor security bug) and icons
- require rpm-helper

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.26-5mdk
- add apache user

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.3.26-4mdk
- change the requires on perl (precise the Epoch)

* Mon Jul  8 2002 Pixel <pixel@mandrakesoft.com> 1.3.26-3mdk
- build with "-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" since mod_perl uses this
  (since using uselargefiles in perl)
  => apache_mod-perl will now work again :)

* Tue Jun 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.26-1mdk
- new version 1.3.26.

* Thu May 16 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.24-2mdk
- Rebuild with gcc 3.1.
- New openssl.

* Mon Apr 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.24-1mdk
- Updated perl version.
- 1.3.24 (security and bug fixes).
- EAPI&mod_ssl 2.8.8.
- Re-generate Patch5.

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.23-4mdk
- added --disable-rule=expat to stop segfaults in mod_perl. The only reason
  expat is needed is for mod_dav, and then it's possible to link it with the
  real expat shared library. Links:
  http://lists.xml.org/archives/xml-dev/200008/msg00229.html
  http://axkit.org/faq.xml

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.23-3mdk
- Re-build since there was a mod_ssl security update and a few things have
  been fixed in the EAPI as well (and that's in Apache).
- Fix manual path
- Fix configuration files to be more secure, and also to be easier to parse
  by Frontpage and other addons.
- The old advx.com is broken, the new site is www.advx.org
- Misc. fixes to index.shtml (yes, I removed my name from the index.shtml, 
  some people did not like it)
- Removed suexec, will be in a separate package instead. The problem was the
  docroot was hardcoded in it, and people with non-standard html directories
  had to re-compile everything to get it working for their configuration.

* Thu Feb 28 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.23-2mdk
- Fix apache-manual files (*.html.html ->  *.html)

* Mon Jan 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.23-1mdk
- Apache 1.3.23
- mod_ssl 2.8.6

* Mon Dec 17 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.22-3mdk
- Fix apache-manual problems.
- Fix man page (s/inetd/xinetd).

* Tue Nov 06 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.22-2mdk
- fix owner in apache-manual.
- fix source permissions (rpmlint).

* Tue Oct 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.22-1mdk
- apache 1.3.22.
- EAPI 2.8.5.
- remake patches.

* Mon Oct 15 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.20-7mdk
- Put html manual in /var/www/html/apache-manual.

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.20-6mdk
- Build against new db3.

* Tue Oct  9 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.20-5mdk
- Make rpmlint happier.

* Tue Oct  9 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.20-4mdk
- Correct the manpage to show the right conf and log files.
- Provides the Obsoletes for compatibility.

* Fri Aug 24 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.20-3mdk
- added BuildConflicts:  BerkeleyDB-devel

* Fri Aug 24 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.20-2mdk
- fixed requires apache-conf

* Thu Jul 05 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.20-1mdk
- update

* Fri Apr 13 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19-3mdk
- fixed requires

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19-2mdk
- added serverbuild flag
- EAPI 2.8.2 (cleanup and bugfixes)

* Sun Mar 25 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19-1mdk
- Completely remade the spec file so it's easier to grok
- Updated to 1.3.19
- Removed SGI optimizations, they are now unsupported by SGI =(
  Bad thing and good thing, since the patches had a bunch of casts and
  other constructs that ASF try to keep out of the code because it leads
  to very subtle bugs... If I have time, I will create an Apache-SGI package
  for contribs with the 1.3.14 version that will work in proxy mode.
- Replaced the Microsoft Frontpage patches by the Improved Frontpage
  module, which is better, and a lot more secure. This module will we in a
  separate package.
- Re-put mod_perl into its own SRPM. We'll use the new apache-source 
  package to build the static mod_perl
- Split modules into their own package so they can be used with mod_perl
  as well
- Put mod_include_xssi in a different package so it can USE_PERL_SSI
- Replaced the ln and rm commands in the post scripts by a relative symbolic 
  link created in the build process.
- Get the EAPI directly from mod_ssl so we don't have to untar it, extract
  the two directories we need and re-tar them for Apache
- Add small advertising on index.shtml for Thawte SSL certificates for
  people to secure their web servers
- Added Prereqs almost everywhere to install in the right order
- Changed MM_CORE_PATH to /var/apache-mm/mm instead of /var/run/mm 
  because only root can write to /var/run and we have to be able to run 
  Apache as a non-root user! Also, we change httpd.h directly since 
  adding the define under the shell removes the quote, and it breaks 
  future use with apxs
- Added -fno-strict-aliasing since it's used by mod_perl
- Removed russian package descriptions
- Removed all configuration files, they will be put into apache-conf module,
  so they can be easily tailored by an ISP or an OEM
- Added rotatelogs utility

* Thu Feb 01 2001 Francis Galiegue <fg@mandrakesoft.com> 1.3.14-4mdk
- Do not run make test on ia64 :(

* Wed Jan 17 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.3.14-3mdk
- fix for insecure tempfile creation in htpasswd and htdigest

* Tue Oct 24 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.14-2mdk
- put Requires: apache-common in HTML-Embperl package

* Sat Oct 21 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.14-1mdk
- update to 1.3.14 bugfix+security release
- mod_rewrite patch thanks to Vincent Danen <vdanen@mandrakesoft.com>
- update to EAPI 2.7.1 (bugfixes + update for 1.3.14) thanks to RSE
- update to HTML-Embperl-1.3b6 (update for 1.3.14)
- one week of diff-of-a-diff-of-a-diff-of-a-diff tweaking
- modified httpd.conf so /doc points to /usr/share/doc (thanks to Guillaume
  Rousse <Guillaume.Rousse@univ-reunion.fr>
- added new init script from Mikhail Zabaluev <mookid@sigent.ru> of the
  Russian Apache Project
- Fixed a bug in httpd-perl.conf thanks to Florin Grad
 <florin@mandrakesoft.com>
- Added KOffice mimetypes

* Wed Sep 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-30mdk
- Fixed the [PASSED] in the init script
- Added index.php in DirectoryIndex for PHPNuke 
- fixed post-install script
- fixed BuildRequires
- fixed library name mismatch in mm
- There are still 129 errors with rpmlint, but that's only because all files
  are owned by apache.apache and flepied didn't rebuilt rpmlint.

* Fri Sep 8 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-27mdk
- Created an hyper-robust init script
- apachectl is now a symlink to the init script
- Fixed problems with segfaulting when logtorating (some modules don't like
  kill -USR1, and you have to stop and restart Apache so it restarts
  cleanly)
- Removed BUFFERED_LOGS from the main Makefile. Instead, create a copy of
  mod_log_config with the #define and leave the choice to the user by
  tweaking httpd.conf
- Added support for ApacheJServ, and hopefully Tomcat/Jakarta
- link with -lpthread to fix php-mysql issues
  (Thanks a lot to taki@enternet.hu!)
- rebuilt with patched mm
- new user apache (compatibility with RedHat)
- changed /var/www ownership to apache.apache
- changed log dir ownership to apache.apache
- fixed possible security bug submitted by richardjbrain@hotmail.com where
  the /perl/ directory is browseable

* Thu Aug 24 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-26mdk
- new Mandrake logo from http://mandrake.com/en/poweredby.php3
- EAPI 2.6.6
- fix HTML::Embperl config file
- do not run make test on alpha
- added some documentation in httpd.conf about the buffered logs

* Mon Aug 21 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-25mdk
- fixed init script

* Wed Aug  9 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-24mdk
- fixed a bad link in HTML-Embperl documentation

* Tue Aug  8 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-23mdk
- Apache now works perfectly with mod_perl, HTML::Embperl and Apache::ASP
- Rebuilt with new perl for more security
- Tested *every* file, except for 1 DBI file
- The build process now makes 300 different tests before it writes the
  package
- Cleaned the spec file

* Fri Aug  4 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-22mdk
- added .htaccess for Embperl so the examples work online

* Thu Aug  3 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-21mdk
- fixed provides for mod_perl
- fixed post scripts

* Thu Aug  3 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-20mdk
- fixed manual path
- removed the part on the webpage about the SGI optimizations for the
  mod_perl package

* Thu Aug  3 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-19mdk
- at post-install, s|/home/httpd|/var/www| in httpd-perl.conf also
- put manual in separate package
- put PARSE_FORM and RANDOM_SSI defines for the xssi module

* Thu Aug  3 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-18mdk
- Fixed the configure script (seems we need to define additional modules
  at the beginning of the configure options.. weird...)

* Thu Aug  3 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-17mdk
- if /home/httpd exists, link /var/www to it so upgrades do not break the
  system
- at post-install, s|/home/httpd|/var/www| in httpd.conf 

* Wed Aug  2 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-16mdk
- added standalone and cgi Embperl, plus a battery of tests to make sure
  everything compiles and works correctly
- moved document root to %{apacheroot}

* Mon Jul 31 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-15mdk
- added HTML-Embperl in the main package since if won't compile when httpd
  is stripped (needs symbols)
- Long period of experimenting to determine the correct build sequence and
  understand the code well enough to create patches
- HTML-Embperl is needed for many interesting applications, such as Tallyman
  (E-commerce application)  

* Fri Jul 14 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-14mdk
- Bonnne Fete la France! 14 juillet et 14mdk =)
- completely remade package. Now has mod_perl inside, to build separate
  packages: apache-common, apache-mod_perl and apache. The apache-mod_perl
  package is statically linked and *stable*, while the combination of apache
  + mod_perl (DSO) was causing segfaults all the time, specially with ASP.
  Took me a long time to figure out how to get rid of that problem, and
  thanks to Mikhail Zabaluev for his help!
- It's possible to use both apache and apache-mod_perl. The plain apache
  will proxy the requests to apache-mod_perl. Very efficient.
- prepare for FHS/LSB. Now a macro defines apacheroot, apachecontent and
  apachebase. Macro-ized everything
- added -D_FILE_OFFSET_BITS=64 definitions
- EAPI 2.6.5

* Mon May 08 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-11mdk
- EAPI 2.6.4 (bugfixes again!)
- Workaround for big bug in msec. Now apache chmods 0755 /home/httpd
- More russian descriptions from from Mikhail Zabaluev <mookid@sigent.ru>
- USE_STAT_CACHE

* Mon Apr 17 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-10mdk
- Use the contribs mm instead of bundling it into apache (we'll move mm to
  the main distro, otherwise it'll conflict)
- EAPI 2.6.3 (bugfixes)
- Replaced the vhost sample lines by sample files for DynamicVhosts and
  VirtualHomePages
- Added the new SGI 12-1 and 12-2 patches (bugfixes)
- Split mod_include_xssi.c from mod_include.c (conflict)
- put documentation in /usr/doc where it belongs and made a symlink
  in /home/httpd/html/manual
- added russian descriptions from Mikhail Zabaluev <mookid@sigent.ru>
- changed logrotate so it sends SIGUSR1 because httpdloses buffered log
  entries when restarted by a SIGHUP.

* Fri Apr 14 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-9mdk
- append .c to AddModule mod_vhost_alias
- suggestions from Eric Snyder <Eric@Credible.net>:
- add #VirtualDocumentRoot sample line
- add #VirtualScriptAlias sample line
- add #NameVirtualHost sample line
- put LMDK200Rw.gif logo

* Wed Apr  5 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-8mdk
- cleaned spec

* Mon Apr  3 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-7mdk
- EAPI 2.6.2 (no changes, just want to keep current with Ralph EngelSchall)
- Changed Pentium optimizations to Processor-specific optimizations on web
  page
- Changed layout of webpage so the package is labeled as Mandrake and people
  see it as Apache+addons instead of a non-standard Apache.
- Tested all combinations of patches for mod_perl and mod_ssl, mod_perl was
  the culprit.

* Mon Apr  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.3.12-6mdk
- don't compile QSC on arch other than Intel.

* Tue Feb 29 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-5mdk
- updated EAPI to 2.6.1

* Sun Feb 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-3mdk
- fixed link for addon modules

* Sun Feb 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-3mdk
- removed the patch for mod_log_config.c, was causing a segfault under
  certain conditions with the CustomLog of mod_ssl

* Sun Feb 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-2mdk
- hacked the SGI patches to they work with the EAPI. There is only one
  .rej file that I don't know how to handle yet (buff.c). Maybe we will
  not get every full bit of the 10x performance increase, but we should
  get almost all of it, and Apache will still work with mod_ssl.
- Changed signature for Apache-AdvancedExtranetServer

* Sat Feb 26 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.12-1mdk
- updated to 1.3.12
- updated to EAPI 2.6.0

* Sun Jan 23 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 1.3.11
- updated to EAPI 2.5.0

* Tue Jan 18 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to EAPI 2.4.10
- Put the nice Advanced Extranet and SGI optimized logos.

* Wed Jan  5 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- moved suexec to another package so it doesn't get installed by default
- added index.php3 as valid index.

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- rebuilt for Mandrake 7.0
- fixed httpd.pid

* Sat Dec 12 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to mm 1.0.12 and EAPI 2.4.9 
- modified index.shtml to link to www.advancedextranet.com

* Tue Nov 23 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- strip (plz)

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- SMP check/build

* Mon Oct  4 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- build for cooker.


* Mon Sep 06 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- re-build for EAPI 2.4.2 and mm 1.0.11

* Sun Sep 05 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- added tables in index.s html and removed the part about the docs in
  /extranet, because they're not completed yet.

* Fri Sep 03 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- fixed package description

* Fri Sep 03 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated EAPI to 2.4.1
- updated mm to 1.0.10
- added "Listen 80" in httpd.conf

* Wed Aug 18 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated EAPI to 2.4.0

* Mon Aug 16 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 1.3.9

* Sun Aug 15 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- Solaris fixes again

* Sat Aug 14 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- changed install for cp -aR so ldconfig does not complain on shared mem
  libs

* Fri Aug 13 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 1.3.8
- cleaned the SPEC file

* Tue Aug 10 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- got new patches from rse@engelschall.com
- fixed some bugs in Solaris RPM
- re-added apachectl, don't know why RH removed it...

* Tue Aug 3 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- re-made the SPEC to port to Solaris rpm
- re-designed the web page to be able to include platform and to
  separate Apache from all the addon packages
- got new patches from rse@engelschall.com

* Sun Aug 1 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- created modules and vhosts directory to clean up a bit

* Sat Jul 31 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated EAPI from mod_ssl 2.3.10
- complete re-write of index.html
- created *LOTS* of new modules for this version
- removed mod_auth bandwidth
- added Hotwired mod_include
- created /protected-cgi-bin to fix security concerns with a cgi in the
  Squid package that was accessible to anyone

* Wed Jul 21 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to mm-1.0.9
- updated EAPI from Jul 15 version of rse@engelschall.com
- cosmetic changes on html manual structure, updated links for
  crypto stuff now that it's on Mandrake site
- removed mod_auth_radius and mod_put, will be in separate packages.
- cleaned sources to have less files

* Sun Jun 06 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to mm-1.0.6
- removed php3 from main apache package, will be in a separate rpm

* Sat Jun 05 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to mm-1.0.5
- added mod_define and addon patch from <rse@engelschall.com>
- added FrontPage 2000 patch
- added fr locale
- added mod_auth_radius
- added mod_put (Netscape Publish)
- changed index.html to add more documentation, links and icons
- re-made httpd.conf, erased srm.conf and access.conf

* Sat May 29 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- Updated to mm-1.0.4
- Updated EAPI from mod_ssl-2.3.1-1.3.6 <rse@engelschall.com>

* Tue May 25 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- Hacked apxs so the package finally compiles in one shot
- Tweaked config files to add a bit more performance
- Added shared_time in scoreboard

* Mon May 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Should correctly deside if it should restart apache

* Sun May 23 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to php3.0.8

* Sat May 22 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- added support for RPM_OPT_CFLAGS

* Thu May 20 1999 Jean-Michel Dault <jmdault@netrevolution.com>

- added index.htm and Default.htm in srm.conf
- removed msql support (no rpm, no binary, commercial license)
- added mm-1.0.3 from rse@engelschall.com
- added EAPI from rse@engelschall.com
- added suexec code 

* Tue May 18 1999 Gaël Duval <gael@linux-mandrake.com>

- removed sed stuff (there is no sed at install time)
- added a correct srm.conf

* Fri May 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix dependences.

* Wed May 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fixing typo.
- Compressing man-pages.

* Mon May 03 1999 Gaël Duval <gael@linux-mandrake.com>
- merged apache and php3, added post and postun config scripts
- moved all archives from tar.gz to tar.bz2
- Mandrake apdaption
- php3 doc linked from the local index.html

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- allow indexes in /doc

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Mon Apr 05 1999 Preston Brown <pbrown@redhat.com>
- prerequire /bin/rm, added /doc path pointing to /usr/doc for localhost

* Fri Mar 26 1999 Preston Brown <pbrown@redhat.com>
- updated log rotating scripts to not complain if logs aren't present.

* Thu Mar 25 1999 Preston Brown <pbrown@redhat.com>
- fixed up path to perl

* Wed Mar 24 1999 Preston Brown <pbrown@redhat.com>
- updated init script to conform to new standards
- upgraded to 1.3.6, fixed apxs patch

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- clean up logfiles on deinstallation

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Mar 12 1999 Cristian Gafton <gafton@redhat.com>
- added mod_bandwidth
- updated to 1.3.4
- prereq mailcap

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- added patch to disable building support for ndbm
- build against glibc 2.1

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.3.3 to catch up with bug fixes
- added the /usr/bin/* binaries to the spec file list

* Fri Sep 25 1998 Cristian Gafton <gafton@redhat.com>
- change ownership of cache dir to nobody
- added "Red Hat" to the server string
- updated to version 1.3.2
- fixed all references to httpsd in config files

* Fri Sep 04 1998 Cristian Gafton <gafton@redhat.com>
- small fixes to the spec file
- patch to handle correctly the -d <newroot> option
- leave out the .usr.src.apache_%{version} for now

* Thu Sep 03 1998 Preston Brown <pbrown@redhat.com>
- patched apxs not to bomb out if it can't find httpd

* Wed Sep 02 1998 Preston Brown <pbrown@redhat.com>
- upgraded to apache 1.3.1.
- Heavy rewrite.
- changed providing a_web_server to just webserver.  Humor is not an option.

* Mon Aug 10 1998 Erik Troan <ewt@redhat.com>
- updated to build as non-root user
- added patch to defeat header dos attack

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- fixed the default config files to be more paranoid about security

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- fixed init script
- added index.htm to the list of acceptable indexes

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.2.6
- added post script to install htm extension for text/html into
  /etc/mime.types

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced sysv init script

* Tue Jan 06 1998 Erik Troan <ewt@redhat.com>
- updated to 1.2.5, which includes many security fixes

* Wed Dec 31 1997 Otto Hammersmith <otto@redhat.com>
- fixed overkill on http.init stop

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- added patch for backslash DOS attach

* Thu Nov 06 1997 Donnie Barnes <djb@redhat.com>
- added htdigest binary to file list

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- made the default index.html be config(noreplace) so we no longer
  blow away other folks' index.html

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added chkconfig support
- added restart|status options to initscript
- renamed httpd.init to httpd

* Tue Oct 07 1997 Elliot Lee <sopwith@redhat.com>
- Redid spec file, patches, etc. from scratch.

