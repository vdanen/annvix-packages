#
# spec file for package httpd-mod_perl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-%{mod_name}
%define version 	%{apache_version}_%{mod_version}
%define release 	%_revrel

# Module-Specific definitions
%define apache_version	2.0.55
%define mod_version	2.0.1
%define mod_name	mod_perl
%define mod_conf	75_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}
%{expand:%%define perl_version %(rpm -q --qf '%%{epoch}:%%{version}' perl)}

%define _requires_exceptions perl(Data::Flow)\\|perl(Carp::Heavy)\\|perl(Apache::FunctionTable)\\|perl(Apache::StructureTable)\\|perl(Apache::TestConfigParse)\\|perl(Apache::TestConfigPerl)\\|perl(Module::Build)

Summary:	An embedded Perl interpreter for the Apache Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://perl.apache.org/
Source0:	%{sourcename}.tar.gz
Source1:	%{sourcename}.tar.gz.asc
Source2:	%{mod_conf}
Source3:	apache2-mod_perl-testscript.pl
Patch0:		mod_perl-2.0.0-external_perl-apache-test.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel >= 5.8.6, httpd-devel >= %{apache_version}, perl-Apache-Test

Prereq:		perl
Requires:	httpd-mod_proxy, perl = %{perl_version}
Prereq:		httpd >= %{apache_version}, httpd-conf
Provides:	apache-mod_perl = %{version}
Provides:	apache2-mod_perl
Obsoletes:	apache2-mod_perl

%description
%{name} incorporates a Perl interpreter into the Apache web server,
so that the Apache2 web server can directly execute Perl code.
Mod_perl links the Perl runtime library into the Apache web server and
provides an object-oriented Perl interface for Apache's C language
API.  The end result is a quicker CGI script turnaround process, since
no external Perl interpreter has to be started.

Install %{name} if you're installing the Apache web server and you'd
like for it to directly incorporate a Perl interpreter.


%package devel
Summary:	Files needed for building XS modules that use mod_perl
Group:		Development/C
Requires:	%{name} = %{version}
Requires:	httpd-devel >= %{apache_version}

%description devel 
The mod_perl-devel package contains the files needed for building XS
modules that use mod_perl.


%prep
%setup -q -n %{sourcename}
%patch0 -p1
rm -rf Apache-Test


%build
# Compile the module.
%{__perl} Makefile.PL \
    MP_CCOPTS="$(%{_sbindir}/apxs -q CFLAGS) -fPIC" \
    MP_APXS=%{_sbindir}/apxs \
    MP_APR_CONFIG=%{_bindir}/apr-config \
    INSTALLDIRS=vendor </dev/null 

ln -s Apache-mod_perl_guide-1.29/bin bin

%make

# XXX mod_include/SSI does not include files when they are not named .shtml
mv t/htdocs/includes-registry/test.pl t/htdocs/includes-registry/test.shtml
mv t/htdocs/includes-registry/cgipm.pl t/htdocs/includes-registry/cgipm.shtml
sed 's/\.pl/.shtml/' t/htdocs/includes/test.shtml > tmpfile && mv tmpfile t/htdocs/includes/test.shtml


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
mkdir -p %{buildroot}/var/www/perl
mkdir -p %{buildroot}%{_includedir}/httpd

%makeinstall \
    MODPERL_AP_LIBEXECDIR=%{_libdir}/httpd-extramodules \
    MODPERL_AP_INCLUDEDIR=%{_includedir}/httpd \
    INSTALLDIRS=vendor

cat %{SOURCE2} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

# Remove empty file
rm -f docs/api/mod_perl-2.0/pm_to_blib

install -d %{buildroot}/var/www/perl
install -m 0755 %{SOURCE3} %{buildroot}/var/www/perl

# install missing required files
install -d %{buildroot}%{perl_vendorarch}/Apache2/Apache
install -m 0644 xs/tables/current/Apache2/ConstantsTable.pm %{buildroot}%{perl_vendorarch}/Apache2/Apache/
install -m 0644 xs/tables/current/Apache2/FunctionTable.pm %{buildroot}%{perl_vendorarch}/Apache2/Apache/
install -m 0644 xs/tables/current/Apache2/StructureTable.pm %{buildroot}%{perl_vendorarch}/Apache2/Apache/

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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}
%attr(0755,root,root) /var/www/perl/*.pl
%{perl_vendorlib}
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/httpd/*


%changelog
* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org>
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.1-1avx
- rebuild against new perl
- fix changelog

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.1-1avx
- apache 2.0.54
- mod_perl 2.0.1
- s/conf.d/modules.d/
- s/apache2/httpd/
- nuke the bundled Apache-Test and use the "system" one (oden)
- never run the test suite as it requires apache and friends to be installed in
  order to run it

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.0.0-0.RC4.3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.0.0-0.RC4.2avx
- rebuild

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_2.0.0-0.RC4.1avx
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

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_1.99_11-2avx
- rebuild against new perl

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_1.99_11-1avx
- apache 2.0.52

* Sat Sep 11 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_1.99_11-3avx
- rebuild against new perl
- remove req's on mod_perl-common... apache 1.x is gone
- BuildRequires: db4-devel

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_1.99_11-2avx
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
