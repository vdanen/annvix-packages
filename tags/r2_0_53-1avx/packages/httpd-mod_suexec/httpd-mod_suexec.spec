%define name	apache2-%{mod_name}
%define version %{apache_version}
%define release 1avx

# Module-Specific definitions
%define apache_version	2.0.53
%define mod_name	mod_suexec
%define mod_conf	69_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{apache_version}

Summary:	Allows CGI scripts to run as a specified user and Group
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org/docs/suexec.html
Source1:	%{mod_conf}.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  apache2-devel >= %{apache_version}, apache2-source >= %{apache_version}

Prereq:		rpm-helper
Prereq:		apache2 >= %{apache_version}, apache2-conf

%description
This module, in combination with the suexec support program
allows CGI scripts to run as a specified user and Group.

Normally, when a CGI or SSI program executes, it runs as the
same user who is running the web server.

%prep
%setup -c -T -n %{name}

cp %{_includedir}/apache2/* .
cp `apr-config --includedir`/* .
cp `apu-config --includedir`/* .

echo "#define AP_GID_MIN 100"  >> ap_config_auto.h
echo "#define AP_UID_MIN 100"  >> ap_config_auto.h
echo "#define AP_DOC_ROOT \"/var/www\"" >> ap_config_auto.h
echo "#define AP_HTTPD_USER \"apache\""  >> ap_config_auto.h
echo "#define AP_LOG_EXEC \"/var/log/httpd/suexec_log\""  >> ap_config_auto.h
echo "#define AP_SAFE_PATH \"/usr/local/bin:/usr/bin:/bin\""  >> ap_config_auto.h
echo "#define AP_SUEXEC_UMASK 0077"  >> ap_config_auto.h
echo "#define AP_USERDIR_SUFFIX \"public_html\""  >> ap_config_auto.h

cp %{_prefix}/src/apache2-%{version}/docs/man/suexec.8 .
cp %{_prefix}/src/apache2-%{version}/docs/manual/mod/mod_suexec.html.en mod_suexec.html
cp %{_prefix}/src/apache2-%{version}/docs/manual/programs/suexec.html.en programs-suexec.html
cp %{_prefix}/src/apache2-%{version}/docs/manual/suexec.html.en suexec.html
cp %{_prefix}/src/apache2-%{version}/modules/generators/mod_suexec.c .
cp %{_prefix}/src/apache2-%{version}/modules/generators/mod_suexec.h .
cp %{_prefix}/src/apache2-%{version}/support/suexec.c .
cp %{_prefix}/src/apache2-%{version}/support/suexec.h .

%build

gcc `%{_sbindir}/apxs2 -q CFLAGS -Wall` -I. -o suexec suexec.c

%{_sbindir}/apxs2 -I. -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d

install -m 0755 suexec %{buildroot}%{_sbindir}/apache2-suexec
install suexec.8 %{buildroot}%{_mandir}/man8/apache2-suexec.8

mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/apache2-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}

mkdir -p %{buildroot}/var/www/html/addon-modules
ln -s ../../../../%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc mod_suexec.html suexec.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_so}
%attr(4710,root,apache) %{_sbindir}/apache2-suexec
%{_mandir}/man8/*
/var/www/html/addon-modules*

%changelog
* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-1avx
- apache 2.0.52
- use ap*-config --includedir to get headers (oden)

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49-2avx
- Annvix build

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
