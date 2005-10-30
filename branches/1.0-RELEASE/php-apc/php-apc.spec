%define name	php-%{modname}
%define version	%{phpversion}_%{rver}
%define rver	2.0.4
%define release	1avx

%define phpversion	4.3.11
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define modname		apc
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		99_%{modname}.ini

Summary:		The apc (Alternative PHP Cache) module for PHP
Name:			%{name}
Version:		%{version}
Release:		%{release}
License:		PHP License
Group:			System/Servers
URL:			http://pecl.php.net/package/APC
Source0:		APC-%{rver}.tar.bz2
Source1:		apc.ini.bz2

BuildRoot:		%{_tmppath}/%{name}-root
BuildRequires:  	php4-devel

Requires:		php4
Conflicts:		php-afterburner php-mmcache

%description
APC was conceived of to provide a way of boosting the performance
of PHP on heavily loaded sites by providing a way for scripts to
be cached in a compiled state, so that the overhead of parsing and
compiling can be almost completely eliminated. There are
commercial products which provide this functionality, but they are
neither open-source nor free. Our goal was to level the playing
field by providing an implementation that allows greater
flexibility and is universally accessible. 

We also wanted the cache to provide visibility into it's own
workings and those of PHP, so time was invested in providing
internal diagnostic tools which allow for cache diagnostics and
maintenance. 

Thus arrived APC. Since we were committed to developing a product
which can easily grow with new version of PHP, we implemented it
as a zend extension, allowing it to either be compiled into PHP or
added post facto as a drop in module. As with PHP, it is available
completely free for commercial and non-commercial use, under the
same terms as PHP itself. 

APC has been tested under PHP 4.0.3, 4.0.3pl1 and 4.0.4. It
currently compiles under Linux and FreeBSD. Patches for ports to
other OSs/ PHP versions are welcome. 

NOTE!: %{name} has to be loaded last, very important!

%prep
%setup -q -n APC-%{rver}

%build

phpize
%configure2_5x \
    --enable-%{modname}=shared,%{_prefix}
#    --enable-mmap \
#    --disable-sem

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 

NOTE!: %{name} has to be loaded last, very important!

There's also a apc-gui v1.0.3, but it does not work 100% and
it seems unmaintained. But anyway check here if you want to
hack it to work: http://apc.neuropeans.com/

EOF

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m755 %{soname} %{buildroot}%{phpdir}/extensions/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc CHANGELOG INSTALL NOTICE README*
%{phpdir}/extensions/%{soname}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}

%changelog
* Sat May 14 2005 Vincent Danen <vdanen@annvix.org> 4.3.11_2.0.4-1avx
- php 4.3.11

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 4.3.10_2.0.4-2avx
- rebuild and cleanups

* Thu Dec 16 2004 Vincent Danen <vdanen@annvix.org> 4.3.10_2.0.4-1avx
- php 4.3.10

* Thu Sep 30 2004 Vincent Danen <vdanen@annvix.org> 4.3.9_2.0.4-1avx
- first Annvix build

* Sun Aug 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_2.0.4-2mdk
- make it work again...

* Sat Jul 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_2.0.4-1mdk
- 2.0.4

* Wed Jul 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_2.0.3-1mdk
- rebuilt for php-4.3.8

* Mon Jul 12 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_2.0.3-2mdk
- remove redundant provides

* Mon Jun 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_2.0.3-1mdk
- rebuilt for php-4.3.7

* Sun May 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_2.0.3-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php.d

* Wed May 05 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_2.0.3-1mdk
- 2.0.3
- fix url
- built for php 4.3.6

* Sun Nov 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4_2.0-2mdk
- rebuilt for re-upload

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4_2.0-1mdk
- built for php 4.3.4

* Fri Sep 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3_2.0-3mdk
- rebuilt

* Fri Sep 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3_2.0-2mdk
- use correct url

* Wed Aug 27 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3_2.0-1mdk
- built for php 4.3.3
- oops, it's either mmap or sem ;)
- misc spec file fixes

* Fri Aug 22 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2_2.0-1mdk
- 2.0
- misc spec file fixes

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2_2.0-0.20030603.1mdk
- update from CVS
- built for 4.3.2

* Tue Feb 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1_2.0-0.20030218.1mdk
- update from CVS
- fix the php versioning

* Mon Feb 17 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20030217.1mdk
- update from CVS
- updated S1
- run the brute force tests and save the results in docs dir

* Sat Feb 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0-0.20030214.1mdk
- brand new spanking version!
- new license
- updated S1
- conflicts with php-mmcache
- misc spec file fixes

* Wed Feb 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-0.20020722.7mdk
- fix a silly bug in the tmpwatch invocation

* Sun Jan 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-0.20020722.6mdk
- really rebuilt against rebuilt buildrequires

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-0.20020722.5mdk
- rebuilt against rebuilt buildrequires

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-0.20020722.4mdk
- added a tmpwatch command so that the cache gets cleared if needed on 
  a daily basis, otherwise bad things might happen if not enough space 
  availible in /var/cache/apc ;)

* Sun Jan 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-0.20020722.3mdk
- fix S1
- install apcinfo.php into webspace (go to http://localhost/apcinfo.php)

* Fri Jan 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-0.20020722.2mdk
- built against php-4.3.0
- follow the spec file design as in main

* Tue Nov 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-0.20020722.1mdk
- fix version (duh!)
- fix description
- fix the README file
- fix dir perms on /var/cache/apc

* Sat Sep 21 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.3-0.20020722.2mdk
- added the %{_sysconfdir}/apc.ini file which has to be appended to 
  the %{_sysconfdir}/php.d.ini file
- can't use %%post or %%preun (yet)
- Conflicts:	php-afterburner
- added the cache dir

* Fri Sep 20 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.3-0.20020722.1mdk
- initial cooker contrib
