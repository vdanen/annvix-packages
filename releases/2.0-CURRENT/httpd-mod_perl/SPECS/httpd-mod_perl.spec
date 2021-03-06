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
%define apache_version	2.2.4
%define mod_version	2.0.3
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
Patch0:		mod_perl-2.0.3-mdv-external_perl-apache-test.patch
Patch1:		mod_perl-2.0.2-DESTDIR.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel >= 5.8.6
BuildRequires:	httpd-devel >= %{apache_version}
BuildRequires:	perl(Apache::Test) >= 1.29

Requires:	httpd-mod_proxy
Requires:	perl = %{perl_version}
Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-conf
Requires(pre):	perl
Requires(pre):	rpm-helper
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


%package devel
Summary:	Files needed for building XS modules that use mod_perl
Group:		Development/C
Requires:	%{name} = %{version}
Requires:	httpd-devel >= %{apache_version}

%description devel 
The mod_perl-devel package contains the files needed for building XS
modules that use mod_perl.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{sourcename}
%patch0 -p1
%patch1 -p0
rm -rf Apache-Test


%build
# Compile the module.
perl Makefile.PL \
    MP_CCOPTS="$(%{_sbindir}/apxs -q CFLAGS) -fPIC" \
    MP_APXS=%{_sbindir}/apxs \
    MP_APR_CONFIG=%{_bindir}/apr-1-config \
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

%makeinstall_std \
    MODPERL_AP_LIBEXECDIR=%{_libdir}/httpd-extramodules \
    MODPERL_AP_INCLUDEDIR=%{_includedir}/httpd \
    INSTALLDIRS=vendor DESTDIR=%{buildroot}

cat %{_sourcedir}/%{mod_conf} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

# Remove empty file
rm -f docs/api/mod_perl-2.0/pm_to_blib

install -d %{buildroot}/var/www/perl
install -m 0755 %{_sourcedir}/apache2-mod_perl-testscript.pl %{buildroot}/var/www/perl

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


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}
%attr(0755,root,root) /var/www/perl/*.pl
%{perl_vendorlib}
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/httpd/*

%files doc
%defattr(-,root,root)
%doc Changes INSTALL LICENSE README docs todo


%changelog
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_2.0.3
- apache 2.2.4

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_2.0.3
- 2.0.3
- updated P0 from Mandriva

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_2.0.2
- apache 2.2.3
- spec cleanups

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_2.0.2
- rebuild against new db4

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_2.0.2
- apache 2.2.2
- mod_perl 2.0.2
- P1: allow us to use %%makeinstall_std (oden)
- updated config
- rebuild with gcc4

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.0.1
- rebuild against perl 5.8.8
- perl policy on buildreq
- use requires(pre) instead of prereq

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.0.1
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_2.0.1
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_2.0.1
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
