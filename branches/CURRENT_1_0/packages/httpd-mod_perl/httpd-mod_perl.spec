%define name	apache2-%{mod_name}
%define version %{apache_version}_%{mod_version}
%define release 0.RC4.1avx

# Module-Specific definitions
%define apache_version	2.0.53
%define mod_version	2.0.0
%define mod_name	mod_perl
%define mod_conf	75_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}-RC4
%{expand:%%define perl_version %(rpm -q --qf '%%{epoch}:%%{version}' perl)}

%define _requires_exceptions perl(Data::Flow)\\|perl(Carp::Heavy)\\|perl(Apache::FunctionTable)\\|perl(Apache::StructureTable)\\|perl(Apache::TestConfigParse)\\|perl(Apache::TestConfigPerl)\\|perl(Module::Build)

Summary:	An embedded Perl interpreter for the apache2 Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://perl.apache.org/
Source0:	%{sourcename}.tar.gz
Source1:	%{sourcename}.tar.gz.asc
Source2:	%{mod_conf}.bz2
Source3:	%{name}-startup.pl
Source61:       apache2-mod_perl-testscript.pl

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	perl-devel >= 5.8.6, apache2-devel >= %{apache_version}, db4-devel
BuildRequires:	perl-HTML-Parser, perl-Tie-IxHash, perl-URI, perl-libwww-perl, perl-CGI
BuildRequires:	apache2-mod_cache, apache2-mod_dav, apache2-mod_deflate, apache2-mod_disk_cache
BuildRequires:	apache2-mod_file_cache, apache2-mod_ldap, apache2-mod_mem_cache, apache2-mod_proxy,
BuildRequires:	apache2-mod_ssl, apache2-mod_suexec

BuildConflicts:	perl-Apache-Test

Prereq:		perl
Requires:	apache2-mod_proxy, perl = %{perl_version}
Requires:	perl-Apache-Test >= 1.20
Prereq:		apache2 >= %{apache_version}, apache2-conf
Provides:	apache-mod_perl = %{version}

%description
%{name} incorporates a Perl interpreter into the apache2 web server,
so that the Apache2 web server can directly execute Perl code.
Mod_perl links the Perl runtime library into the apache2 web server and
provides an object-oriented Perl interface for apache2's C language
API.  The end result is a quicker CGI script turnaround process, since
no external Perl interpreter has to be started.

Install %{name} if you're installing the apache2 web server and you'd
like for it to directly incorporate a Perl interpreter.

%package devel
Summary:	Files needed for building XS modules that use mod_perl
Group:		Development/C
Requires:	%{name} = %{version}
Requires:	apache2-devel >= %{apache_version}

%description devel 
The mod_perl-devel package contains the files needed for building XS
modules that use mod_perl.

%prep
%setup -q -n %{sourcename}

%build

# Compile the module.
%{__perl} Makefile.PL \
    MP_CCOPTS="$(%{_sbindir}/apxs2 -q CFLAGS) -fPIC" \
    MP_INST_APACHE2=1 \
    MP_APXS=%{_sbindir}/apxs2 \
    MP_APR_CONFIG=%{_bindir}/apr-config \
    INSTALLDIRS=vendor </dev/null 

ln -s Apache-mod_perl_guide-1.29/bin bin

%make

# XXX mod_include/SSI does not include files when they are not named .shtml
mv t/htdocs/includes-registry/test.pl t/htdocs/includes-registry/test.shtml
mv t/htdocs/includes-registry/cgipm.pl t/htdocs/includes-registry/cgipm.shtml
sed 's/\.pl/.shtml/' t/htdocs/includes/test.shtml > tmpfile && mv tmpfile t/htdocs/includes/test.shtml

# Run the test suite.
#  Need to make t/htdocs/perlio because it isn't expecting to be run as
#  root and will fail tests that try and write files because the server
#  will have changed it's uid.
mkdir -p t/htdocs/perlio
chmod 777 t/htdocs/perlio

#
# fix for bad_scripts.t in 1.99_12
# [Tue Mar 02 17:28:26 2004] [error] file permissions deny server execution/usr/src/packages/BUILD/modperl-2.0/ModPerl-Registry/t/cgi-bin/r_inherited.pl
if test -e ModPerl-Registry/t/cgi-bin/r_inherited.pl; then chmod +x ModPerl-Registry/t/cgi-bin/r_inherited.pl; fi
#
# 1.99_12_20040302 fix for t/hooks/cleanup.t and t/hooks/cleanup2.t
# [Tue Mar 02 18:38:41 2004] [error] [client 127.0.0.1] can't open /usr/src/packages/BUILD/modperl-2.0/t/htdocs/hooks/cleanup2: Permission denied at /usr/src/packages/BUILD/modperl-2.0/Apache-Test/lib/Apache/TestUtil.pm line 82.
mkdir -p t/htdocs/hooks
chmod 2770 t/htdocs/hooks
#
# run test suite:
#
#make TEST_VERBOSE=1 APACHE_TEST_PORT=select APACHE_TEST_STARTUP_TIMEOUT=360 test  || {
#       ps aufx | grep "/usr/sbin/httpd2-prefork -d /usr/src/packages/BUILD/modperl-2.0" \
#               | grep -v grep | awk '{print $2}' | xargs -r kill
#       exit 1
#}

#perl t/TEST -start-httpd -port select -startup_timeout 360 -verbose -httpd_conf /etc/httpd/conf/httpd2.conf
#perl t/TEST -run-tests || {
#perl t/TEST -stop-httpd
#    exit 1
#}
#perl t/TEST -stop-httpd
# in case of failures, see http://perl.apache.org/docs/2.0/user/help/help.html#_C_make_test___Failures
# then, debug like this:
# t/TEST -start-httpd
# tail -F t/logs/*&
# t/TEST -run-tests -verbose $failed_test
# t/TEST -stop-httpd


# (oe) Sat Jan 22 2005
# currently these tests fails:

#Failed Test                      Stat Wstat Total Fail  Failed  List of Failed
#-------------------------------------------------------------------------------
#t/apache/content_length_header.t  255 65280    27   54 200.00%  1-27
#t/api/aplog.t                                  36   13  36.11%  24-36
#t/apr-ext/finfo.t                  29  7424    ??   ??       %  ??
#t/apr-ext/util.t                   29  7424    ??   ??       %  ??
#t/apr/finfo.t                     255 65280    ??   ??       %  ??
#t/apr/util.t                      255 65280    ??   ??       %  ??
#3 tests skipped.
#Failed 6/222 test scripts, 97.30% okay. 40/2257 subtests failed, 98.23% okay.

#make \
#    APACHE_TEST_PORT=select \
#    APACHE_TEST_STARTUP_TIMEOUT=30 \
#    APACHE_TEST_COLOR=1 \
#    TEST_VERBOSE=1 \
#    APACHE_TEST_HTTPD=%{_sbindir}/httpd2 \
#    APACHE_TEST_APXS=%{_sbindir}/apxs2 \
#    test

# kill any stale processes
#kill -9 `/sbin/pidof %{_sbindir}/httpd2`


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf/addon-modules
mkdir -p %{buildroot}/var/www/perl

%makeinstall \
    MODPERL_AP_LIBEXECDIR=%{buildroot}%{_libdir}/apache2-extramodules \
    MODPERL_AP_INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir}/apache2 \
    MP_INST_APACHE2=1 \
    INSTALLDIRS=vendor

bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}

mkdir -p %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

# Remove empty file
rm -f docs/api/mod_perl-2.0/pm_to_blib

# Add startup file...
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf/addon-modules/

install -d %{buildroot}//var/www/perl
install -m 755 %{SOURCE61} %{buildroot}/var/www/perl

# install missing required files
install -m644 xs/tables/current/Apache/StructureTable.pm \
    %{buildroot}%{perl_vendorarch}/Apache2/Apache/
install -m644 xs/tables/current/Apache/FunctionTable.pm \
    %{buildroot}%{perl_vendorarch}/Apache2/Apache/

# cleanup
find %{buildroot}%{perl_archlib} -name perllocal.pod | xargs rm -f

# don't pack the Apache-Test stuff
rm -rf %{buildroot}%{perl_vendorlib}/Apache
rm -f %{buildroot}%{perl_vendorlib}/Bundle/ApacheTest.pm
rm -f %{buildroot}%{_mandir}/man3/Apache::Test*
rm -f %{buildroot}%{_mandir}/man3/Bundle::ApacheTest.3pm


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_post_srv httpd2

%postun
%_post_srv httpd2

%files -n %{name}
%defattr(-,root,root)
%doc Changes INSTALL LICENSE README docs todo
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/addon-modules/*
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_so}
%attr(0755,root,root) /var/www/perl/*.pl
%{perl_vendorlib}
%{_mandir}/*/*
/var/www/html/addon-modules/*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/apache2/*

%changelog
* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_2.0.0-0.RC4.1avx
- 2.0.0-RC4
- apache 2.0.53
- fix license
- rule out a number of perl requires (ala Mandrake and Fedora)
- nuke fake Apache::Status as this is included and now works
- don't include bundled Apache-Test
- make "make test" work using stuff from Fedora and SUSE (oden)
  - this only kinda works here; craps out on a SetEnv directive; not sure
    why so disable for now
- remove ADVX stuff

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 2.0.52_1.99_11-2avx
- rebuild against new perl

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52_1.99_11-1avx
- apache 2.0.52

* Sat Sep 11 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_1.99_11-3avx
- rebuild against new perl
- remove req's on mod_perl-common... apache 1.x is gone
- BuildRequires: db4-devel

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_1.99_11-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_1.99_11-1sls
- apache 2.0.49

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.99_11-5sls
- rebuild for perl 5.8.4
- require exact version of perl, including epoch
- fix standard-dir-owned-by-package /usr/share/man/man3 (pixel)

* Fri Feb 20 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.99_11-4sls
- tiny cleanups

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.99_11-3sls
- put back the mod_perl-common req's as we are shipping apache 1.x

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_1.99_11-2sls
- OpenSLS build
- tidy spec
- don't require mod_perl-common for anything because we don't ship apache 1.x

* Fri Nov 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.99_11-1mdk
- 1.99_11

* Wed Nov 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.99_10-2mdk
- rebuilt against perl-5.8.2

* Sun Nov 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.99_10-1mdk
- built for apache 2.0.48
- 1.99_10
- drop useless P0
- drop P1, it's included

* Wed Aug 13 2003 François Pons <fpons@mandrakesoft.com> 2.0.47_1.99_09-3mdk
- rebuild against with latest perl.
- add patch from mod_perl cvs to handle perl 5.8.1 and above for hash
  ramdomization.
- added require to apache2-mod_proxy needed by configuration files.

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_1.99_09-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.99_09-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.99_09-4mdk
- force provide on "perl(Apache::TestConfigParse)" and "perl(Apache::TestConfigPerl)"

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.99_09-3mdk
- install missing required files

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.99_09-2mdk
- fix requires and provides (duh!)

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.99_09-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2
- added the pgp sig file
- added P0 and some spec file stuff from rh rawhide
- added the devel sub package

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_1.99_08-1mdk
- cosmetic rebuild for apache v2.0.45

* Mon Feb 17 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_1.99_08-3mdk
- add fake Apache::Status with a message that it's not implemented yet,
  asking to install mod_perl-common if the user requires this function.

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_1.99_08-2mdk
- rebuild

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_1.99_08-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.99_08-3mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.99_08-2mdk
- rebuilt against rebuilt buildrequires

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.99_08-3mdk
- 1.99_08
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.99_07-2mdk
- rebuilt for/against apache2 where dependencies has changed in apr

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.99_07-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)

* Mon Sep 30 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_1.99_07-1mdk
- new version
- rebuilt against new apache v2.0.42

* Wed Sep  4 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_1.99_05-2mdk
- Fix Requires

* Wed Aug 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_1.99_05-1mdk
- Rebuild with ADVX policy (http://advx.org/devel/policy.php)
- Provide a working, tested, configuration file and startup script
- Move config script to order 75 (always best to put after mod_php)

* Wed Aug 21 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.99_05-1mdk
- Official 1.99_05 version

* Wed Aug 21 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0-0.20020803.4mdk
- Add the MP_TRACE option since this is a CVS module and still has bugs
- Remade specfile so it works with the new ADVX Apache 2.

* Tue Aug  6 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020803.3mdk
- rebuilt against new multi threading perl
- really use the 0803 snapshot this time, not 0802

* Fri Aug  2 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020803.2mdk
- fix so mod_perl-1.27 can coexist, well at least when building (thanks to Stas Bekman)

* Fri Aug  2 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020803.1mdk
- new CVS version (it compiles!)
- built against new apache2 and perl
- misc spec file fixes

* Wed Jul 10 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020710.1mdk
- new CVS version

* Mon Jul  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020701.1mdk
- new CVS version

* Sat Jun 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020629.1mdk
- new CVS version
- ship the correct perl.conf file...

* Tue Jun 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020618.1mdk
- new CVS version

* Mon Jun 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020617.1mdk
- new CVS version

* Sun Jun 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020616.1mdk
- new CVS version

* Sat Jun 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020615.2mdk
- restart apache2 in %%post and %%preun (duh!)

* Sat Jun 15 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020615.1mdk
- new CVS version

* Fri Jun 14 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020614.1mdk
- new CVS version
- misc spec file fixes

* Fri Jun 14 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020613.2mdk
- hmmm..., it seems crucial that mod_perl is built against the exact CVS
  version of apache2
- added similar disclamier as in the apache2 %%description

* Thu Jun 13 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020613.1mdk
- new CVS version
- renamed ServerRoot/conf.d/perl.conf to ServerRoot/conf.d/45_mod_perl.conf

* Thu Jun 12 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20020612.1mdk
- boldy stolen spec file from RH Rawhide :-)
- 1.99_02 did not compile, but the one from CVS did...
