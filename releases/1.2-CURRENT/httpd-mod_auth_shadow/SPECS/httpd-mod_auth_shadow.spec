#
# spec file for package httpd-mod_auth_shadow
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		httpd-%{mod_name}
%define version 	%{apache_version}_%{mod_version}
%define release 	2avx

# Module-Specific definitions
%define apache_version	2.0.54
%define mod_version	2.0
%define mod_name	mod_auth_shadow
%define mod_conf	83_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	Shadow password authentication for the Apache web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://mod-auth-shadow.sourceforge.net/
Source0:	%{sourcename}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		%{sourcename}-register.patch.bz2
Patch1:		%{sourcename}-makefile.patch.bz2
Patch2:		mod_auth_shadow-2.0-CAN-2005-2963.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}

Prereq:		httpd >= %{apache_version}, httpd-conf
Provides:	apache2-mod_auth_shadow
Obsoletes:	apache2-mod_auth_shadow

%description
%{mod_name} is an Apache module which authenticates against
the /etc/shadow file. You may use this module with a mode 400 
root:root /etc/shadow file, while your web daemons are running
under a non-privileged user.


%prep
%setup -q -n %{sourcename}
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .can-2005-2963

%build
export PATH="$PATH:/usr/sbin"
%make CFLAGS="%{optflags}" -f makefile


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/httpd-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_sbindir}
install -m 4755 validate %{buildroot}%{_sbindir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc CHANGES INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}
%attr(4755,root,root) %{_sbindir}/validate


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Oct 28 2005 Vincent Danen <vdanen@annvix.org> 2.0.54_2.0-2avx
- P2: fix for CAN-2005-2963

* Wed Sep 07 2005 Vincent Danen <vdanen@annvix.org> 2.0.54_2.0-1avx
- apache 2.0.54
- s/conf.d/modules.d/
- s/apache2/httpd/

* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_2.0-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_2.0-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_2.0-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52_2.0-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_2.0-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_2.0-1sls
- apache 2.0.49

* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_2.0-3sls
- small cleanup

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_2.0-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_2.0-1mdk
- built for apache 2.0.48

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_2.0-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_2.0-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_2.0-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_2.0-3mdk
- cosmetic rebuild for apache v2.0.45

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_2.0-3mdk
- fix another typo in config file (damn templates ;-)

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_2.0-2mdk
- fix typo in config file

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_2.0-1mdk
- initial cooker contrib
