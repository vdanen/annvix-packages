%define name	apache-mod_perl
%define version	%{apache_version}_%{mod_perl_version}
%define release	4sls

#New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}

%{expand:%%define apache_version %(rpm -q apache-devel|sed 's/apache-devel-\([0-9].*\)-.*$/\1/')}
%{expand:%%define apache_release %(rpm -q apache-devel|sed 's/apache-devel-[0-9].*-\(.*\)$/\1/')}

%{expand:%%define mm_major %(mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\1/')}
%{expand:%%define mm_minor %(mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\2/')}
%define mm_version %{mm_major}.%{mm_minor}

%define perl_version		%(rpm -q --qf '%%{epoch}:%%{version}' perl)
%define mod_perl_version	1.29
%define embperl_version		1.3.6

#we use this so apache and apache-mod_perl can use the same modules
%define apflags %(echo "`%{_sbindir}/apxs -q CFLAGS 2>/dev/null|sed s/-DSHARED_CORE//g`")

Summary:	Apache Web server with a built-in Perl interpreter
Name:		%{name}
Version:	%{apache_version}_%{mod_perl_version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://perl.apache.org
Source0:	mod_perl-%{mod_perl_version}.tar.gz
Source1:	mod_perl-%{mod_perl_version}.tar.gz.asc
Source2:	README.ADVX
Source6:	mod_include_xssi.c
Source16:	proxied_handlers.pl
Source22:	mod_include_xssi.html
Source60:	mod_perl.html
Source61:	mod_perl-testscript.pl
Source70:	ftp://ftp.dev.ecos.de/pub/perl/embperl/HTML-Embperl-%{embperl_version}.tar.bz2
Source71:	embperl-apache.diff.bz2
Source72:	HTML-Embperl.html
Patch1:		HTML-Embperl-1.3.4-disable-some-tests.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	ADVX-build >= 1.2
# needed for /var/apache-mm
BuildRequires:	apache-conf
BuildRequires:	apache-source = %{apache_version}
BuildRequires:	apache-devel = %{apache_version}
BuildRequires:	mm-devel = %{mm_major}.%{mm_minor}
BuildRequires:	perl-libwww-perl
BuildRequires:	perl-HTML-Parser
BuildRequires:	perl-URI
BuildRequires:	perl-MIME-Base64
BuildRequires:	perl-libnet
BuildRequires:	perl-Digest-MD5
BuildRequires:	perl-Apache-Session
BuildRequires:	glibc-devel
BuildRequires:	perl-CGI
BuildRequires:	libgdbm-devel
BuildRequires:	db1-devel
BuildRequires:	db3-devel
BuildRequires:	perl-devel
BuildConflicts:	BerkeleyDB-devel

Obsoletes:	mod_perl
Requires:	perl = %{perl_version}
Prereq:		apache-conf >= %{apache_version}
Prereq:		apache-common >= %{apache_version} 
Prereq:		apache-modules = %{apache_version}
Prereq:		mm = %{mm_major}.%{mm_minor}
Prereq:		mod_perl-common = %{apache_version}_%{mod_perl_version}
Provides:	webserver mod_perl 
Provides:	apache = %{apache_version}
Provides:	mod_perl = %{mod_perl_version}
Provides:	ADVXpackage
Provides:	AP13package

%description 
Apache is a powerful, full-featured, efficient and freely-available
Web server. 

mod_perl incorporates a Perl interpreter into the Apache web
server, so that the Apache web server can directly execute Perl
code.  Mod_perl links the Perl runtime library into the Apache
web server and provides an object-oriented Perl interface for
Apache's C language API.  The end result is a quicker CGI script
turnaround process, since no external Perl interpreter has to
be started.

This package contains Apache with mod_perl linked statically. It also
contains a statically linked HTML::Embperl module, but you need the separate
HTML-Embperl package to activate it.

%package -n mod_perl-devel
Summary:	Apache-Mod_Perl Development Files
Version:	%{apache_version}_%{mod_perl_version}
Group:		System/Servers
URL:		http://perl.apache.org
#Icon: mod_perl.gif
Prereq:		apache-conf >= %{apache_version}
Prereq:		apache-common >= %{apache_version}
Prereq:		apache-mod_perl = %{apache_version}_%{mod_perl_version}
Prereq:		mm = %{mm_major}.%{mm_minor}
Prereq:		mod_perl-common = %{apache_version}_%{mod_perl_version}
Provides:	apache-mod_perl-devel
Obsoletes:	apache-mod_perl-devel
Requires:	perl = %{perl_version}
Prereq:		perl-devel
Provides:	ADVXpackage
Provides:	AP13package

%description -n mod_perl-devel
The apache-mod_perl include files for developing mod_perl modules

%package -n HTML-Embperl
Summary:	HTML::Embperl module
Version:	%{apache_version}_%{embperl_version}
Group:		System/Servers
URL:		http://perl.apache.org/embperl/
Requires:	perl = %{perl_version}
Prereq:		apache-mod_perl = %{apache_version}_%{mod_perl_version}
Prereq:		mod_perl-common = %{apache_version}_%{mod_perl_version}
Prereq:		apache-modules = %{apache_version}
Prereq:		apache-conf >= %{apache_version}
Prereq:		apache-common >= %{apache_version}
Prereq:		mm = %{mm_major}.%{mm_minor}
Provides:	ADVXpackage
Provides:	AP13package

%description -n HTML-Embperl
Embeded perl allows perl to be embeded with HTML pages that are served out
to clients.

This module contains support for apache-mod_perl, support for standalone
mode, or cgi under any webserver.

%package -n mod_perl-common
Summary:	The mod_perl and apache-mod_perl common files
Version:	%{apache_version}_%{mod_perl_version}
Group:		System/Servers
URL:		http://perl.apache.org
Requires:	perl = %{perl_version}
Requires:	perl-Devel-Symdump
Requires:	perl-BSD-Resource
Provides:	ADVXpackage
Provides:	AP13package

%description -n mod_perl-common
The mod_perl and apache-mod_perl common files

%prep

# unpack HTML-Embperl
%setup -q -n HTML-Embperl-%{embperl_version} -T -b 70

%patch1 -p1

#unpack mod_perl
%setup -q -n mod_perl-%{mod_perl_version} 

rm -rf $RPM_BUILD_DIR/apache-mod_perl_%{apache_version}
cp -dpR /usr/src/apache_%{apache_version} \
	$RPM_BUILD_DIR/apache-mod_perl_%{apache_version}

%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

#JMD: do not use the serverbuild macro here, we pick the flags from apxs.

echo "### define configure flags"
#APVARS=`cat $RPM_BUILD_DIR/apache-mod_perl_%{apache_version}/APVARS`
APVARS=`sed s/--enable-rule=SHARED_CORE//g $RPM_BUILD_DIR/apache-mod_perl_%{apache_version}/APVARS`

echo "### configure and pre-compile mod_perl and apache for embperl"
cd $RPM_BUILD_DIR/mod_perl-%{mod_perl_version}
perl -pi -e "s|PRODUCT|BASEPRODUCT|;" Makefile.PL
%{__perl} Makefile.PL INSTALLDIRS=vendor \
     APACHE_SRC=../apache-mod_perl_%{apache_version}/src \
     DO_HTTPD=1 \
     USE_APACI=1 \
     EVERYTHING=1 \
     APACI_ARGS="$APVARS --enable-rule=EAPI --disable-rule=expat --disable-shared=perl"

# echo
#    APACHE_SRC=../apache-mod_perl_%{apache_version}/src \
#    DO_HTTPD=1
#	 USE_APXS=1 \
#	 WITH_APXS=/usr/sbin/apxs \

#     APACI_ARGS="$APVARS --enable-rule=EAPI --disable-rule=expat --disable-shared=include --disable-shared=perl"

#JMD: *Very Important!*
#get the optflags from apxs, so we're 100% module-compatible with apache
%define LIBDB -ldb-3.3
perl -pi -ple 's|^OPTIM=|OPTIM=%{apflags}|; \
     s|EXTRA_LIBS=|EXTRA_LIBS=%{LIBDB} -lgdbm -lpthread -lmm|;' \
    `find ../apache-mod_perl_%{apache_version}/src -name Makefile -print`


# (cb) 02.02.04 structure DBM is not in db1/db.h, but in db1/ndbm.h
cd $RPM_BUILD_DIR/apache-mod_perl_%{apache_version}/src/modules/standard
perl -pi -ple 's|<db.h>|<db1/ndbm.h>|;' mod_rewrite.h
cd -

#JMD: why does -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 cause segfaults?!?!

# OE: why is this needed?
cd $RPM_BUILD_DIR/apache-mod_perl_%{apache_version}/src/modules/standard
perl -pi -ple 's|<db.h>|<db1/ndbm.h>|;' mod_auth_dbm.c
cd -

make

echo "### patch Apache to enable linking mod_perl with embperl"
cd $RPM_BUILD_DIR/apache-mod_perl_%{apache_version} 
perl -pi -e \
	"s|EXTRA_INCLUDES=|EPDIR=../../../../HTML-Embperl-%{embperl_version}\nEXTRA_INCLUDES= -I\\\$\(EPDIR\) |" \
	src/modules/perl/Makefile
bzcat %{SOURCE71}|patch -p0 

echo "### build embperl"
cd $RPM_BUILD_DIR/HTML-Embperl-%{embperl_version} 
(echo y;echo y)| \
    perl -I$RPM_BUILD_DIR/mod_perl-%{mod_perl_version}/blib/lib Makefile.PL INSTALLDIRS=vendor
perl -pi -e \
    "s|{ . |{ . $RPM_BUILD_DIR/mod_perl-%{mod_perl_version}/blib/lib |;" \
    test/conf/startup.pl
make

echo "### build Apache with mod_perl+embperl linked statically, also build Perl-side"
# files
cd $RPM_BUILD_DIR/mod_perl-%{mod_perl_version} 
make
cd faq
make
cd ..
##Make the test work even if the hostname is invalid!
perl -pi -e "s/autoindex/autoindex\|unique/g;" ./apaci/load_modules.pl

%ifnarch ia64
make test
%endif

echo "### test embperl to make sure everything was linked successfully"
cd $RPM_BUILD_DIR/HTML-Embperl-%{embperl_version} 
%ifnarch alpha ia64
#make test
%endif

#-----------------------------------

%install

# install mod_perl files
cd $RPM_BUILD_DIR/mod_perl-%{mod_perl_version}
make PREFIX=%{buildroot}/usr install_vendor

mkdir -p %{buildroot}%{_docdir}/apache-mod_perl-%{apache_version}_%{mod_perl_version}
mkdir -p %{buildroot}%{ap_webdoc}
pushd %{buildroot}%{ap_webdoc}
rm -f mod_perl-%{apache_version}_%{mod_perl_version}
ln -s  ../../../..%{_docdir}/mod_perl-common-%{apache_version}_%{mod_perl_version} \
	mod_perl-%{apache_version}_%{mod_perl_version}
popd

# install HTML-Embperl
cd $RPM_BUILD_DIR/HTML-Embperl-%{embperl_version} 
make install PREFIX=%{buildroot}/tmp/usr
rm -f %{buildroot}/tmp/%{perl_vendorarch}/auto/HTML/Embperl/.packlist
rm -f %{buildroot}/tmp/%{perl_vendorarch}/auto/HTML/Embperl/Embperl.bs
rm -rf %{buildroot}/tmp/usr
make install PREFIX=%{buildroot}/usr
rm -f %{buildroot}/%{perl_vendorarch}/auto/HTML/Embperl/.packlist
rm -f %{buildroot}/%{perl_vendorarch}/auto/HTML/Embperl/Embperl.bs
rm -rf HTML-Embperl
mkdir -p %{buildroot}%{ap_datadir}/perl/HTML-Embperl-%{embperl_version}
pushd %{buildroot}%{ap_datadir}/perl/HTML-Embperl-%{embperl_version}
cp -dpR $RPM_BUILD_DIR/HTML-Embperl-%{embperl_version}/eg .
cat << EOF > .htaccess
<Files ~ (\.htm)>
SetHandler perl-script
PerlHandler HTML::Embperl
</Files>
Options +Indexes
EOF
popd


# install apache-mod_perl 
cd $RPM_BUILD_DIR/apache-mod_perl_%{apache_version}
mkdir -p %{buildroot}%{_sbindir}
install -m755 src/httpd %{buildroot}%{_sbindir}/httpd-perl
install -d -m755 %{buildroot}%{_libdir}/perl-apache/
#install -m755 src/modules/*/*.so %{buildroot}%{_libdir}/perl-apache/

# install Embperl documentation
install -m644 %{SOURCE72} \
        %{buildroot}/%{ap_webdoc}/HTML-Embperl.html
export EMBDOC=mod_perl-%{mod_perl_version}/embdoc
mkdir -p $RPM_BUILD_DIR/$EMBDOC
install -m 644 $RPM_BUILD_DIR/HTML-Embperl-%{embperl_version}/{README,TODO} \
	$RPM_BUILD_DIR/$EMBDOC
install -m 644 $RPM_BUILD_DIR/HTML-Embperl-%{embperl_version}/*.pod \
	$RPM_BUILD_DIR/$EMBDOC

# install mod_perl files
cd $RPM_BUILD_DIR/mod_perl-%{mod_perl_version}
make pure_install PREFIX=%{buildroot}/usr
rm -f %{buildroot}%{perl_vendorarch}/auto/Apache/Symbol/Symbol.bs
rm -f %{buildroot}%{perl_vendorarch}/auto/Apache/Leak/Leak.bs

#install mod_perl documentation
export PERLDOC=mod_perl-%{mod_perl_version}/perldocs
mkdir -p $RPM_BUILD_DIR/$PERLDOC
install -m 644 htdocs/manual/mod/mod_perl.html \
	$RPM_BUILD_DIR/$PERLDOC
perl -pi -e "s|../../../|/manual/images/|g;" \
	$RPM_BUILD_DIR/$PERLDOC/mod_perl.html
install -m 644 %{SOURCE60} \
	$RPM_BUILD_DIR/$PERLDOC
install -m 644 README \
	$RPM_BUILD_DIR/$PERLDOC/README.txt
install -m 644 SUPPORT Changes \
	$RPM_BUILD_DIR/$PERLDOC
install -m 644 faq/*.html faq/*.txt \
	$RPM_BUILD_DIR/$PERLDOC
install -m 644 apache-modlist.html mod_perl.gif \
	$RPM_BUILD_DIR/$PERLDOC

mkdir -p %{buildroot}/%{ap_addonconf}
install -m 644 %{SOURCE16} \
	%{buildroot}/%{ap_addonconf}/proxied_handlers.pl
install -d -m755 %{buildroot}/%{ap_datadir}/perl
install -m 755 %{SOURCE61} %{buildroot}/%{ap_datadir}/perl

perl -pi -e "s,^/usr.*\n,,;" \
         -e "s,^%{buildroot},,;" \
    %{buildroot}/%{perl_vendorarch}/auto/mod_perl/.packlist

ln -sf ../..%{_libdir}/perl-apache %{buildroot}%{ap_base}/perl-modules

# where's this file?
#cp %{_includedir}/apache/README.ADVX \
#	$RPM_BUILD_DIR/mod_perl-%{mod_perl_version}/
cp %{SOURCE2} .

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# do some house cleaning..
[ -e ../HTML-Embperl-%{embperl_version} ] && rm -fr ../HTML-Embperl-%{embperl_version}
[ -e ../apache-mod_perl_%{apache_version} ] && rm -fr ../apache-mod_perl_%{apache_version}

%files 
%defattr(-,root,root)
%config(noreplace) %{ap_addonconf}/proxied_handlers.pl
%{_sbindir}/httpd-perl
%{ap_base}/perl-modules

%files -n mod_perl-common
%defattr(-,root,root)
%doc perldocs/*
%doc README.ADVX
%{perl_vendorarch}/Apache.pm
%dir %{perl_vendorarch}/Apache
%{perl_vendorarch}/Apache/*
%dir %{perl_vendorarch}/Bundle
%{perl_vendorarch}/Bundle/*
%{perl_vendorarch}/auto/Apache/Leak/*
%{perl_vendorarch}/auto/Apache/Symbol/*
%{perl_vendorarch}/auto/Apache/mod_perl.exp
%{perl_vendorarch}/auto/Apache/typemap
%{perl_vendorarch}/cgi_to_mod_perl.pod
%{perl_vendorarch}/mod_perl*
%{_mandir}/man3/Apache*
%{_mandir}/man3/Bundle::Apache*
%{_mandir}/man3/cgi_to_mod_perl*
%{_mandir}/man3/mod_perl*
%{ap_datadir}/perl/*.pl
%{ap_webdoc}/mod_perl-*

%files -n mod_perl-devel
%defattr(-,root,root)
%{perl_vendorarch}/auto/Apache/include/*

%files -n HTML-Embperl 
%defattr(-,root,root)
%doc embdoc/*
%{ap_webdoc}/HTML-Embperl.html
%{ap_datadir}/perl/HTML-Embperl-%{embperl_version}
%{_bindir}/embpexec.pl
%{perl_vendorarch}/HTML/*
%{perl_vendorarch}/auto/HTML/*
%{_mandir}/man3/HTML*
%{_mandir}/man1/*

%pre
#Check config file sanity
%AP13pre

%post
#JMD: do *not* use _post_service here, it is used in apache-conf, since we
#can have both apache and apache-mod_perl
%ADVXpost

%postun
#JMD: do *not* use _post_service here, otherwise it will uninstall
#apache as well!!
%ADVXpost

%changelog
* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 1.3.29_1.29-4sls
- rebuild for perl 5.8.3
- README.ADVX in one package only
- some spec cleanups
- add unpackaged file /etc/httpd/perl-modules

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.3.29_1.29-3sls
- OpenSLS build
- tidy spec

* Wed Nov 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.29_1.29-2mdk
- rebuilt against perl-5.8.2

* Sat Nov 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.29_1.29-1mdk
- 1.29
- HTML-Embperl-1.3.6
- add the pgp sig file

* Thu Sep 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.28_1.28-2mdk
- Fix deps

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.28_1.28-1mdk
- rebuild for apache security release

* Sun Aug  3 2003 Pixel <pixel@mandrakesoft.com> 1.3.27_1.28-12mdk
- new release
- revive "make test" on mod_perl
- drop mod_perl-1.27-URI.patch.bz2

* Sun Aug  3 2003 Pixel <pixel@mandrakesoft.com> 1.3.27_1.27-12mdk
- rebuild for new perl

* Wed Jul 30 2003 Pixel <pixel@mandrakesoft.com> 1.3.27_1.27-11mdk
- when requiring the perl-base used for building, include the epoch
- fix build (regarding vendor_perl)

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 1.3.27_1.27-10mdk
- Rebuild to fix bad signature

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.27_1.27-9mdk
- fix requires

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.27_1.27-8mdk
- rebuilt to let rpm v4.2 know about some perl stuff
- added S1
- misc spec file fixes

* Wed Feb 19 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-1.27-7mdk
- fix requires (mod_perl-common does not require apache)
- remove old macros and replace them by ADVX macros

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27_1.27-6mdk
- add AP13pre macro to make sure about the sanity of the conf files

* Wed Jan 08 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27_1.27-5mdk
- Clean spec file a bit, some files were installed but not packaged.

* Tue Jan 07 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27_1.27-4mdk
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 
- Likewise, add Provides: AP13package and AP20package in the same
  manner

* Thu Jan 02 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27_1.27-3mdk
- rebuilt for new mm version

* Fri Nov  8 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27_1.27-2mdk
- Rebuild for Cooker

* Mon Oct 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27_1.27-1mdk
- New version

* Fri Sep 06 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.26_1.27-7mdk
- Don't use apache.apache for the documentation
- Bzip patches

* Fri Sep 06 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.26_1.27-6mdk
- Fix file conflict, fix link to documentation and re-add test script.

* Wed Aug 06 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.26_1.27-5mdk
- rebuild with new perl

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 1.3.26_1.27-4mdk
- get rid of a few more "Requires: perl = 5.6.1"

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.3.26_1.27-3mdk
- have "Requires: perl = %%{perl_version}" instead of hard-coding it

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.3.26_1.27-2mdk
- rebuild for perl 5.8.0
- disable some test for HTML-Embperl :-(
  (will report to perl and Embperl projects)

* Thu Jun 27 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.26_1.27-1mdk
- apache 1.3.26.
- mod_perl 1.27
- regenerate Source80.

* Thu May 16 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.24_1.26-2mdk
- Rebuild

* Mon Apr 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.24_1.26-1mdk
- Apache 1.3.24.

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.23_1.26-5mdk
- Disable expat to prevent segfault with axkit
- Put back make test
- Fix broken link in doc

* Mon Feb 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.23_1.26-4mdk
- Rollback to Embperl 1.3.4.
- Rebuild against latest apache.
- Build mod_rewrite part against ndbm.h instead of db.h.
- mod_perl test still not working (it doesn't find URI perl module).

* Sun Oct 28 2001 Stefan van der Eijk <stefan@eijk.nu> 1.3.22_1.26-3mdk
- EXTRA_LIBS=-ldb-3.2 --> EXTRA_LIBS=-ldb-3.3

* Thu Oct 25 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.22_1.26-2mdk
- Provides the Obsoletes for compatibilty.

* Thu Oct 25 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.22_1.26-1mdk
- mod_perl 1.26.
- Embperl 2.0b3 (make test not working...).
- Build against new apache.
- Build against new db3.
- make rpmlint happier.

* Wed Aug 29 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.20_1.25_01-3mdk
- build against libgdbm2

* Thu Jul 12 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.20_1.25_01-2mdk
- fix HTML-Embed version

* Tue Jul 10 2001 Philippe Libat <philippe@mandrakesoft.com> 1.3.20_1.25_01-1mdk
- upgrade
- new apache version
- fix db3 lib

* Wed Jun 13 2001 Pixel <pixel@mandrakesoft.com> 1.3.19_1.25-4mdk
- rebuild for perl 5.6.1
- new HTML-Embed 1.3.3 (needed for perl 5.6.1)

* Fri Apr 13 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19_1.25-3mdk
- fix requires
- fix documentation links

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19_1.25-2mdk
- fix httpd-perl segfault when installing apache-conf
- BuildRequires perl-CGI now that the package has been split

* Sun Mar 25 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.19_1.25-1mdk
- Completely remade spec file
- Re-split mod_perl in its own package again
- Get Apache source from package apache-source so we share the same code
  and it's easier to maintain
- Get optflags from apxs so that apache and apache-mod_perl have the same
  flags and we can use the same modules
- Get apache-mod_perl and apache share same modules so we can have a static
  apache+mod_perl and still have mod_dav, etc...
- Put httpd-perl.conf in apache-conf package to enable better configuration
  for OEMs and ISPs

