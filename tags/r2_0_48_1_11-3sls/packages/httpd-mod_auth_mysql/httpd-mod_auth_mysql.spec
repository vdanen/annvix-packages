%define name	%{ap_name}-%{mod_name}
%define version %{ap_version}_%{mod_version}
%define release 3sls

# Module-Specific definitions
%define mod_version	1.11
%define mod_name	mod_auth_mysql
%define mod_conf	12_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

Summary:	Basic authentication for the %{ap_name} web server using a MySQL database.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		ftp://ftp.kciLink.com/pub/
Source0:	ftp://ftp.kciLink.com/pub/%{mod_name}.c.bz2
Source1:	ftp://ftp.kciLink.com/pub/mysql-group-auth.txt.bz2
Source2:	%{mod_conf}.bz2
Patch0:		%{mod_name}-1.11-ap2.patch.bz2
Patch1:		%{mod_name}-1.11-register.patch.bz2
Patch2:		%{mod_name}-newapi.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildPrereq:	MySQL-devel
# Standard ADVX requires
BuildRequires:  ADVX-build >= 9.2
BuildRequires:  %{ap_name}-devel >= 2.0.44-5mdk

# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf
Provides: 	ADVXpackage
Provides:	AP20package

%description
mod_auth_mysql can be used to limit access to documents served by
a web server by checking data in a MySQL database.

%prep

%setup -q -c -T
bzcat %{SOURCE0} > mod_auth_mysql.c
bzcat %{SOURCE1} > mysql-group-auth.txt
cat mod_auth_mysql.c | tail +84 | head -101 | cut -c 4- > mod_auth_mysql.txt
%patch0 -p0 -b .ap2
%patch1
%patch2

%build

%{apxs} -c mod_auth_mysql.c -I%{_includedir}/mysql -Wl,-lmysqlclient

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%ADVXinstlib
%ADVXinstconf %{SOURCE2} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%ADVXpost

%postun
%ADVXpost

%files
%defattr(-,root,root)
%doc *.txt
%{ap_extralibs}/%{mod_so}
%config(noreplace) %{ap_confd}/%{mod_conf}
%{ap_webdoc}/*

%changelog
* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.11-3sls
- little cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_1.11-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.11-1mdk
- built for apache 2.0.48

* Fri Sep 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.47_1.11-4mdk
- nuke implicit requires

* Thu Sep 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.11-3mdk
- fix buildrequires

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_1.11-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.11-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.11-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_1.11-1mdk
- cosmetic rebuild for apache v2.0.45

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_1.11-2mdk
- link with libmysql12

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_1.11-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-7mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-6mdk
- rebuilt against rebuilt buildrequires

* Tue Jan 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-5mdk
- build against latest BuildRequires

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-4mdk
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-3mdk
- rebuilt for/against apache2 where dependencies has changed in apr

* Tue Oct 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-2mdk
- extra modules needs to be loaded _before_ mod_ssl, mod_php and mod_perl
  in order to show up in the server string...

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.11-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)
- sanitize rpm package versioning

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_1.11-6mdk
- rebuilt against new apache v2.0.42

* Wed Sep  3 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_1.11-5mdk
- Comply with ADVX policy at http://advx.org/devel/policy.php
- link with dynamic libmysqlclient.so instead of the static .a (really
  important when used with PHP)

* Sat Aug 31 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-4mdk
- use examples in S2 from RH Rawhide

* Sun Aug 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-3mdk
- revert macro changes in %%post and %%preun (what was I thinking...)

* Sat Aug 17 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-2mdk
- use macros in %%post and %%preun
- fix requires

* Tue Aug 13 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.11-1mdk
- initial cooker contrib, ripped from RH, adapted for ML

