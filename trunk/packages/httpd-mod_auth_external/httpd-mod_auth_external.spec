%define name	%{ap_name}-%{mod_name}
%define version	%{ap_version}_%{mod_version}
%define release	1sls

# Module-Specific definitions
%define mod_version	2.2.7
%define mod_name	mod_auth_external
%define mod_conf	10_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

# New ADVX macros
%define ADVXdir	%{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

Summary:	An %{ap_name} authentication DSO using external programs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://www.unixpapa.com/mod_auth_external.html
Source0:	%{sourcename}.tar.bz2
Source1:	%{mod_conf}.bz2
Source2:	pwauth.pam.bz2
Patch0:		%{mod_name}-2.1.14-pam.patch.bz2
Patch1:		%{mod_name}-2.2.7-conf.patch.bz2
Patch2:		%{mod_name}-2.1.14-server.patch.bz2
Patch4:		%{mod_name}-2.2.7-register.patch.bz2
Patch5:		mod_auth_external-2.2.3-64bit-fixes.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pam-devel, apache2-devel
# Standard ADVX requires
BuildRequires:  ADVX-build >= 9.2
BuildRequires:  %{ap_name}-devel >= 2.0.43-5mdk

Prereq:		rpm-helper
# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf
Provides: 	ADVXpackage
Provides:	AP20package

%description
An %{ap_name} external authentication module - uses PAM.

%prep
%setup -q -n %{sourcename}
%patch0
%patch1
%patch2 -p1
%patch4 
%patch5 -p1 -b .64bit-fixes

%build
%{apxs} -c %{mod_name}.c
cd pwauth
%make CFLAGS="%{optflags}" LIB="-lpam -ldl"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%ADVXinstlib
%ADVXinstconf %{SOURCE1} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

mkdir -p %{buildroot}%{ap_extralibs}
install -m 755 -s pwauth/pwauth %{buildroot}%{ap_extralibs}/
install -m 755 -s pwauth/unixgroup %{buildroot}%{ap_extralibs}/

install -d %{buildroot}%{_sysconfdir}/pam.d
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/pam.d/pwauth
bzcat %{SOURCE2} > %{buildroot}%{_sysconfdir}/pam.d/unixgroup

mv pwauth/README README.pwauth
mv pwauth/FORM_AUTH README.pwauth
mv README mod_auth_external.txt
chmod 644 AUTHENTICATORS CHANGES INSTALL* README* TODO mod_auth_external.txt

%post
%ADVXpost

%postun
%ADVXpost

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHENTICATORS CHANGES INSTALL* README* TODO mod_auth_external.txt
%config(noreplace) %{ap_confd}/%{mod_conf}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/pwauth
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/unixgroup
%{ap_extralibs}/%{mod_so}
%attr(04550,root,apache) %{ap_extralibs}/pwauth
%attr(04550,root,apache) %{ap_extralibs}/unixgroup
%{ap_webdoc}/*

%changelog
* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_2.2.7-1sls
- apache 2.0.49

* Wed Feb 11 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_2.2.7-3sls
- more spec cleanups
- remove paths from pam.d file

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_2.2.7-2sls
- OpenSLS build
- tidy spec

* Fri Nov 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_2.2.7-1mdk
- 2.2.7
- rediffed P1 & P4, drop P3

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_2.2.4-1mdk
- built for apache 2.0.48

* Tue Oct 21 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.0.47_2.2.4-3mdk
- rebuild to rewrite /etc/pam.d files

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_2.2.4-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_2.2.4-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Thu Jun 26 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_2.2.4-1mdk
- 2.2.4
- update P1 & P4

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_2.2.3-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.45_2.2.3-2mdk
- Patch5: 64-bit fixes

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_2.2.3-1mdk
- cosmetic rebuild for apache v2.0.45

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_2.2.3-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.2.3-5mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.2.3-4mdk
- rebuild against rebuilt buildrequires

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.2.3-3mdk
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.2.3-2mdk
- rebuilt for/against apache2 where dependencies has changed in apr

* Tue Oct 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.2.3-1mdk
- new version

* Tue Oct 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.2.1-2mdk
- extra modules needs to be loaded _before_ mod_ssl, mod_php and mod_perl
  in order to show up in the server string...

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_2.2.1-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)
- sanitize rpm package versioning

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_2.2.1-3mdk
- rebuilt against new apache v2.0.42

* Tue Sep  3 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_2.2.1-2mdk
- Comply with ADVX policy at http://advx.org/devel/policy.php
- Add P4 to add ap_version_component

* Mon Aug 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.2.1-1mdk
- initial cooker contrib
- based on the spec file for apache1
- deactivate P3
- misc spec file fixes

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 2.1.15-3mdk
- rebuild (so that it builds with "-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64")
  => fix segfault

* Wed Jun 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.15-2mdk
- rebuild against latest apache.

* Sat May 18 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.15-1mdk
- new version.
- build with gcc 3.1.
- updated Patch3 to show new version.

* Mon Apr 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-10mdk
- Apache 1.3.24.

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.1.14-9mdk
- Patched so we know easily if the module is loaded.

* Thu Feb 28 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-8mdk
- Fix documentation permissions.

* Wed Feb 06 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-7mdk
- Add documentation in %{apachecontent}/addon-modules/

* Wed Feb 06 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-6mdk
- Remake the post and postun sections (now like other apache modules).
- Spec cleanup.
- Correct config file for the new location of the module.

* Mon Feb 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-5mdk
- Rebuild against last apache.

* Wed Jan 30 2002 Philippe Libat <philippe@mandrakesoft.com> 2.1.14-4mdk
- Patch2: fix server_uid
- include unixgroup auth.

* Tue Jan 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-3mdk
- Fix doc permission

* Tue Jan 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-2mdk
- Fix typo in the pam patch.

* Thu Jan 17 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.1.14-1mdk
- Fix %%apachebase var (so fix %%post and %%postun).
- Release 2.1.14
- Update patches

* Fri Jul 13 2001 Philippe Libat <philippe@mandrakesoft.com> 2.1.12-1mdk
- New version

* Thu Jun 28 2001 Philippe Libat <philippe@mandrakesoft.com> 2.1.11-1mdk
- update version

* Thu Aug 31 2000 Philippe Libat <philippe@mandrakesoft.com> 2.1.2-1mdk
- Linux-Mandrake adaptations

* Sat Jun 10 2000 Charlie Brady <charlieb@e-smith.net>
- Make sure that "www" group exists before installing.

* Wed May 31 2000 Charlie Brady <charlieb@e-smith.net>
- Fix permissions/ownership - don't want build time group, want install time.

