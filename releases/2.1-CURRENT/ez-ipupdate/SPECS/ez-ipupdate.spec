#
# spec file for package ez-ipupdate
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ez-ipupdate
%define version 	3.0.11b8
%define release 	%_revrel

Summary:	Client for Dynamic DNS Services
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Networking/Other
License:	GPL
URL:		http://ez-ipupdate.com/
Source:		%{name}-%{version}.tar.bz2
Source1:	ez-ipupdate.run
Source2:	ez-ipupdate-log.run
Patch0:		ez-ipupdate-3.0.11b8-mdv-64bit.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(post):	rpm-helper
Requires(preun): rpm-helper

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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .missing_header

%build
%configure

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

perl -pi -e "s|\/usr\/local\/bin|\/usr\/bin|" *.conf
perl -pi -e 's|/tmp/ez-ipupdate.cache|/var/cache/ez-ipupdate|g;' *.conf

mkdir -p %{buildroot}%{_srvdir}/ez-ipupdate/log
install -m 0740 %{_sourcedir}/ez-ipupdate.run %{buildroot}%{_srvdir}/ez-ipupdate/run
install -m 0740 %{_sourcedir}/ez-ipupdate-log.run %{buildroot}%{_srvdir}/ez-ipupdate/log/run


%post
%_post_srv ez-ipupdate

%preun
%_preun_srv ez-ipupdate


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%{_bindir}/*
%dir %attr(0750,root,admin) %{_srvdir}/ez-ipupdate
%dir %attr(0750,root,admin) %{_srvdir}/ez-ipupdate/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ez-ipupdate/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ez-ipupdate/log/run

%files doc
%defattr(-,root,root)
%doc COPYING INSTALL README *.conf


%changelog
* Sat Nov 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8
- P0: add missing header to fix crash on x86_64
- fix the runscript

* Wed Oct 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8
- fix url
- rebuild

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcedir/file instead of %%{SOURCEx}

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8-5avx
- run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8-3avx
- rebuild

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11b8-2avx
- Annvix build

* Fri Mar  5 2004 Thomas Backlund <tmb@mandrake.org> 3.0.11b8-1sls
- first OpenSLS build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
