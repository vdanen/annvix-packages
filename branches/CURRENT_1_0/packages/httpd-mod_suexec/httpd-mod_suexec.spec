%define name	%{ap_name}-%{mod_name}
%define version %{ap_version}
%define release 1sls

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

# Module-Specific definitions
%define mod_name	mod_suexec
%define mod_conf	69_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{ap_version}

Summary:	Allows CGI scripts to run as a specified user and Group
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org/docs/suexec.html
Source1:	%{mod_conf}.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
# Standard ADVX requires
BuildRequires:  ADVX-build >= 9.2
BuildRequires:  %{ap_name}-devel >= 2.0.44-5mdk
BuildRequires:  %{ap_name}-source >= 2.0.44-5mdk

Prereq:		rpm-helper
# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		apache-conf
Provides: 	ADVXpackage
Provides:	AP20package

%description
This module, in combination with the suexec support program
allows CGI scripts to run as a specified user and Group.

Normally, when a CGI or SSI program executes, it runs as the
same user who is running the web server.

%prep
%setup -c -T -n %{name}

cp %{ap_includedir}/* .

echo "#define AP_GID_MIN 100"  >> ap_config_auto.h
echo "#define AP_UID_MIN 100"  >> ap_config_auto.h
echo "#define AP_DOC_ROOT \"%{ap_datadir}\"" >> ap_config_auto.h
echo "#define AP_HTTPD_USER \"apache\""  >> ap_config_auto.h
echo "#define AP_LOG_EXEC \"%{ap_logfiledir}/suexec_log\""  >> ap_config_auto.h
echo "#define AP_SAFE_PATH \"/usr/local/bin:/usr/bin:/bin\""  >> ap_config_auto.h
echo "#define AP_SUEXEC_UMASK 0077"  >> ap_config_auto.h
echo "#define AP_USERDIR_SUFFIX \"public_html\""  >> ap_config_auto.h

cp %{ap_abs_srcdir}/docs/man/suexec.8 .
cp %{ap_abs_srcdir}/docs/manual/mod/mod_suexec.html.en mod_suexec.html
cp %{ap_abs_srcdir}/docs/manual/programs/suexec.html.en programs-suexec.html
cp %{ap_abs_srcdir}/docs/manual/suexec.html.en suexec.html
cp %{ap_abs_srcdir}/modules/generators/mod_suexec.c .
cp %{ap_abs_srcdir}/modules/generators/mod_suexec.h .
cp %{ap_abs_srcdir}/support/suexec.c .
cp %{ap_abs_srcdir}/support/suexec.h .

%build

gcc `%{apxs} -q CFLAGS -Wall` -I. -o suexec suexec.c

%{apxs} -I. -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8

install -m4711 suexec %{buildroot}%{_sbindir}/%{ap_name}-suexec
install suexec.8 %{buildroot}%{_mandir}/man8/%{ap_name}-suexec.8

%ADVXinstlib
%ADVXinstconf %{SOURCE1} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%ADVXpost

%postun
%ADVXpost

%files
%defattr(-,root,root)
%doc mod_suexec.html suexec.html
%config(noreplace) %{ap_confd}/%{mod_conf}
%{ap_extralibs}/%{mod_so}
%{ap_webdoc}/*
%attr(4710,root,apache) %{_sbindir}/%{ap_name}-suexec
%{_mandir}/man8/*

%changelog
* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49-1sls
- apache 2.0.49

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.0.48-3sls
- rebuild

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48-1mdk
- built for apache 2.0.48

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2
- misc spec file fixes

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45-1mdk
- cosmetic rebuild for apache v2.0.45
- fix one missing(?) ">" in buildrequires

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44-2mdk
- fix versioning
- macroize a bit more
- test package

* Fri Feb 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44-1mdk
- 2.0.44
- also build the module

* Thu Aug 1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.40-0.20020731.1mdk
- first attempt at this based on ideas from the apache1 suexec spec file...
