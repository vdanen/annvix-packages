#
# spec file for package httpd-mod_layout
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-%{mod_name}
%define version		%{apache_version}_%{mod_version}
%define release 	%_revrel

# Module-Specific definitions
%define apache_version	2.2.3
%define mod_version	4.0.1a
%define mod_name	mod_layout
%define mod_conf	15_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	Add custom header and/or footers for Apache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-style
Group:		System/Servers
URL:		http://software.tangent.org/
Source0:	%{mod_name}-%{mod_version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_layout-4.0.1a-register.patch
Patch1:		mod_layout-4.0.1a-cvs_fixes.patch
Patch2:		mod_layout-4.0.1a-apache220.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}

Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-conf >= 2.2.2
Provides:	apache2-mod_layout
Obsoletes:	apache2-mod_layout

%description
Mod_Layout creates a framework for doing design. Whether you need
a simple copyright or ad banner attached to every page, or need to
have something more challenging such a custom look and feel for a
site that employs an array of technologies (Java Servlets,
mod_perl, PHP, CGI's, static HTML, etc...), Mod_Layout creates a
framework for such an environment. By allowing you to cache static
components and build sites in pieces, it gives you the tools for
creating large custom portal sites. 


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{mod_name}-%{mod_version}
%patch0 -p0
%patch1 -p1
%patch2 -p1


%build
%{_sbindir}/apxs -c mod_layout.c utility.c layout.c


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/httpd-extramodules/
cat %{_sourcedir}/%{mod_conf} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}

%files doc
%defattr(-,root,root)
%doc ChangeLog INSTALL README


%changelog
* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_4.0.1a
- apache 2.2.3
- spec cleanups

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_4.0.1a
- apache 2.2.2
- P1: fixes from CVS
- P2: make it work with apache2.2
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_4.0.1a
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_4.0.1a
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.0.1a
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.0.1a
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.0.1a
- Clean rebuild

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.0.1a-1avx
- apache 2.0.54
- s/conf.d/modules.d/
- s/apache2/httpd/

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_4.0.1a-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_4.0.1a-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_4.0.1a-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_4.0.1a-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_4.0.1a-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_4.0.1a-1sls
- apache 2.0.49

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_4.0.1a-3sls
- fix the index.html

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_4.0.1a-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
