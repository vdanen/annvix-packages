%define name	%{ap_name}-%{mod_name}
%define version %{ap_version}_%{mod_version}
%define release 2sls

# Module-Specific definitions
%define mod_version	1.99_11
%define mod_name	mod_perl
%define mod_conf	75_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}
%{expand:%%define perl_version %(rpm -q perl|sed 's/perl-\([0-9].*\)-.*$/\1/')}

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

Summary:	An embedded Perl interpreter for the %{ap_name} Web server.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://perl.apache.org/
Source0:	%{sourcename}.tar.gz
Source1:	%{sourcename}.tar.gz.asc
Source2:	%{mod_conf}.bz2
Source3:	%{name}-startup.pl
Source4:	%{name}-status.tar.bz2
Source61:       apache2-mod_perl-testscript.pl

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	perl-devel
# Standard ADVX requires
BuildRequires:	ADVX-build >= 9.2
BuildRequires:	%{ap_name}-devel >= 2.0.43-5mdk

Prereq:		perl
Requires:	perl apache2-mod_proxy
# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf
Provides: 	ADVXpackage
Provides:	AP20package
Provides:	apache-mod_perl = %{version}
# rpm v4.2 should pick this up?
Provides:	perl(Apache2)
Provides:	perl(Apache::TestConfigParse)
Provides:	perl(Apache::TestConfigPerl)

%description
%{name} incorporates a Perl interpreter into the %{ap_name} web server,
so that the Apache2 web server can directly execute Perl code.
Mod_perl links the Perl runtime library into the %{ap_name} web server and
provides an object-oriented Perl interface for %{ap_name}'s C language
API.  The end result is a quicker CGI script turnaround process, since
no external Perl interpreter has to be started.

Install %{name} if you're installing the %{ap_name} web server and you'd
like for it to directly incorporate a Perl interpreter.

%package devel
Summary:	Files needed for building XS modules that use mod_perl
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{ap_name}-devel = %{ap_version}

%description devel 
The mod_perl-devel package contains the files needed for building XS
modules that use mod_perl.

%prep
%setup -q -n %{sourcename}

%build

# Compile the module.
%{__perl} Makefile.PL \
    PREFIX=%{buildroot}%{_prefix} \
    MP_TRACE=1 \
    MP_DEBUG=1 \
    MP_AP_PREFIX=%{_prefix} \
    MP_USE_DSO=1 \
    MP_INST_APACHE2=1 \
    MP_APXS=%{apxs}  \
    MP_APR_CONFIG=%{_bindir}/apr-config \
    CCFLAGS="%{optflags} -fPIC" \
    INSTALLDIRS=vendor </dev/null 

# Don't use this option with 1.99_05!
#    MP_CCOPTS="%{optflags} -Werror" \

# we *NEED* these symbols for HTML::Embperl and Apache-ASP!
export DONT_STRIP=1

%make

# Run the test suite.
#  Need to make t/htdocs/perlio because it isn't expecting to be run as
#  root and will fail tests that try and write files because the server
#  will have changed it's uid.
# mkdir t/htdocs/perlio
chmod 777 t/htdocs/perlio
%if 0
make test
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{ap_extralibs}

%makeinstall \
    MODPERL_AP_LIBEXECDIR=%{buildroot}%{ap_extralibs}/ \
    MODPERL_AP_INCLUDEDIR=$RPM_BUILD_ROOT%{ap_includedir} \
    MP_INST_APACHE2=1 \
    INSTALLDIRS=vendor

#make -C faq
#rm faq/pod2htm*
#install -m644 faq/*.html %{buildroot}%{_docdir}/%{name}-%{version}

%ADVXinstconf %{SOURCE2} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

#Remove empty file
rm -f docs/api/mod_perl-2.0/pm_to_blib

#Add startup file...
install -d %{buildroot}%{ap_addonconf}
install -m 755 %{SOURCE3} %{buildroot}%{ap_addonconf}/

install -d %{buildroot}/%{ap_datadir}/perl
install -m 755 %{SOURCE61} %{buildroot}/%{ap_datadir}/perl
#Fake Apache::Status
tar xjf %{SOURCE4} -C %{buildroot}/%{ap_datadir}/perl

# install missing required files
install -m644 xs/tables/current/Apache/StructureTable.pm \
    %{buildroot}%{perl_vendorarch}/Apache2/Apache/
install -m644 xs/tables/current/Apache/FunctionTable.pm \
    %{buildroot}%{perl_vendorarch}/Apache2/Apache/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%ADVXpost

%postun
%ADVXpost

%files -n %{name}
%defattr(-,root,root)
%config(noreplace) %{ap_confd}/%{mod_conf}
%{ap_extralibs}/%{mod_so}
%{ap_webdoc}/*
%config(noreplace) %{ap_addonconf}/*
%doc Changes INSTALL LICENSE README docs todo
%{perl_vendorlib}
%{_mandir}/*
#Fake Apache::Status
%{ap_datadir}/perl/.modperl2
%{ap_datadir}/perl/*.pl

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{ap_includedir}/*

%changelog
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
