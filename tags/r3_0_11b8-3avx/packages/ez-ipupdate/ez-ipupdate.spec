%define name	ez-ipupdate
%define version 3.0.11b8
%define release 3avx

Summary:	Client for Dynamic DNS Services
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Networking/Other
License:	GPL
URL:		http://www.gusnet.cx:8080/proj/ez-ipupdate/
Source:		%{name}-%{version}.tar.bz2
Source1:	ez-ipupdate.init

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

PreReq:		rpm-helper

%description
ez-ipupdate is a small utility for updating your host name for any of the
dynamic DNS service offered at: 

    * http://www.ez-ip.net
    * http://www.justlinux.com
    * http://www.dhs.org
    * http://www.dyndns.org
    * http://www.ods.org
    * http://gnudip.cheapnet.net (GNUDip)
    * http://www.dyn.ca (GNUDip)
    * http://www.tzo.com
    * http://www.easydns.com
    * http://www.dyns.cx
    * http://www.hn.org
    * http://www.zoneedit.com

it is pure C and works on Linux, *BSD and Solaris.  

Don't forget to create your own config file ( in /etc/ez-ipupdate.conf )
You can find some example in /usr/share/doc/%{name}-%{version}

%prep
%setup -q

%build
%configure

%make 

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

perl -pi -e "s|\/usr\/local\/bin|\/usr\/bin|" *.conf
perl -pi -e 's|/tmp/ez-ipupdate.cache|/var/cache/ez-ipupdate|g;' *.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/rc.d/init.d/
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ez-ipupdate

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc COPYING INSTALL README
%doc *.conf
%{_bindir}/*
%config(noreplace) %{_initrddir}/ez-ipupdate

%post
%_post_service ez-ipupdate

%preun
%_preun_service ez-ipupdate


%changelog
* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 3.0.11b8-3avx
- rebuild

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 3.0.11b8-2avx
- Annvix build

* Fri Mar  5 2004 Thomas Backlund <tmb@mandrake.org> 3.0.11b8-1sls
- first OpenSLS build

* Mon Nov 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.0.11b8-2mdk
- use /var/cache for the cache file rather than /tmp in example configs

* Sun May 11 2003 Laurent Culioli <laurent@pschit.net> 3.0.11b8-1mdk
- 3.0.11b8
- drop patch0 ( merged upstream )

* Fri Feb 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0.11b7-3mdk
- Patch0: don't assume errno to be a global variable.

* Tue Aug 13 2002 Laurent Culioli <laurent@pschit.net> 3.0.11b7-2mdk
- update init

* Tue Jun 18 2002 Laurent Culioli <laurent@mandrakesoft.com> 3.0.11b7-1mdk
- 3.0.11b7

* Tue Feb 26 2002 Laurent Culioli <laurent@mandrakesoft.com> 3.0.11b6-2mdk
- fix init

* Mon Feb 25 2002 Laurent Culioli <laurent@mandrakesoft.com> 3.0.11b6-1mdk
- add init-script
- 3.0.11b6

* Fri Jan 11 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 3.0.11b5-2mdk
- Clean specfile
- Fix config files

* Mon Aug 27 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.11b5-1mdk
- updated to 3.0.11b5

* Fri Jul 06 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.11b-2mdk
- fix description, thx to Mordy Ovits

* Fri Jul 06 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.11b-1mdk
- updated to 3.011b

* Tue Jan 09 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.0.4-1mdk
- updated to 3.0.4

* Tue Dec 12 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.0.1-1mdk
- updated to 3.0.1
- updated list of supported services

* Sun Nov 12 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.9.5-1mdk
- updated to 2.9.5
- provide all configuration example files

* Wed Aug 30 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.8.1-1mdk
- v2.8.1
- BM

* Tue Jul 04 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.4.2-2mdk
- rebuild

* Wed Jun 21 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.4.2-1mdk
- new in contribs
