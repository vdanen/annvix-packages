%define name	apache2-%{mod_name}
%define version	%{apache_version}_%{mod_version}
%define release 1avx

# Module-Specific definitions
%define apache_version	2.0.53
%define mod_version	4.0.1a
%define mod_name	mod_layout
%define mod_conf	15_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	Add custom header and/or footers for apache2
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-style
Group:		System/Servers
URL:		http://software.tangent.org/
Source0:	%{sourcename}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		%{mod_name}-%{mod_version}-register.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  apache2-devel >= %{apache_version}

Prereq:		rpm-helper
Prereq:		apache2 >= %{apache_version}, apache2-conf

%description
Mod_Layout creates a framework for doing design. Whether you need
a simple copyright or ad banner attached to every page, or need to
have something more challenging such a custom look and feel for a
site that employs an array of technologies (Java Servlets,
mod_perl, PHP, CGI's, static HTML, etc...), Mod_Layout creates a
framework for such an environment. By allowing you to cache static
components and build sites in pieces, it gives you the tools for
creating large custom portal sites. 

%prep

%setup -q -n %{sourcename}
%patch0 -p0

%build

%{_sbindir}/apxs2 -c mod_layout.c utility.c layout.c

cat > index.html <<EOF

<p>No documentation exists yet for this module, go to 
<a href="http://software.tangent.org/">tangent.org</a> 
for more information</p>

<p>Meanwhile take a look at the %{_sysconfdir}/httpd/conf.d/%{mod_conf} file</p>

<-- replace_me -->

EOF

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/apache2-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}

mkdir -p %{buildroot}/var/www/html/addon-modules
ln -s ../../../../%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

# make the example work... (ugly, but it works...)

NEW_URL=/addon-modules/%{name}-%{version}/index.html
perl -pi -e "s|_REPLACE_ME_|$NEW_URL|g" %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog INSTALL README index.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_so}
/var/www/html/addon-modules/*

%changelog
* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_4.0.1a-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52_4.0.1a-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_4.0.1a-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_4.0.1a-1sls
- apache 2.0.49

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_4.0.1a-3sls
- fix the index.html

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_4.0.1a-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_4.0.1a-1mdk
- built for apache 2.0.48

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_4.0.1a-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_4.0.1a-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_4.0.1a-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_4.0.1a-1mdk
- cosmetic rebuild for apache v2.0.45

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_4.0.1a-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.0.1a-5mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.0.1a-4mdk
- rebuilt against rebuilt buildrequires

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.0.1a-3mdk
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.0.1a-2mdk
- rebuilt for/against apache2 where dependencies has changed in apr

* Tue Oct 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_4.0.1a-1mdk
- extra modules needs to be loaded _before_ mod_ssl, mod_php and mod_perl
  in order to show up in the server string...
- initial cooker contrib
