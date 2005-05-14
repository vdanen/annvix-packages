%define	name	php-%{modname}
%define version	%{phpversion}
%define release	1avx

%define phpversion	4.3.11
%define phpsource       %{_prefix}/src/php-devel
%define phpdir		%{_libdir}/php

%define realname	GD
%define modname		gd
%define dirname		%{modname}
%define soname		%{modname}.so
%define inifile		23_%{modname}.ini


Summary:	The %{realname} module for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:  php4-devel
BuildRequires:  freetype2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel 
BuildRequires:  libxpm-devel
BuildRequires:  XFree86-devel
BuildRequires:  chrpath >= 0.10-4mdk

Requires:	php4
Requires:       libpng >= 1.2.0
Provides:       mod_php-gd
Provides:       mod_php3-gd
Obsoletes:      mod_php-gd
Obsoletes:      mod_php3-gd


%description
The %{name} package is a dynamic shared object (DSO) that adds
%{realname} support to PHP. PHP is an HTML-embedded scripting language. 
If you need %{realname} support for PHP applications, you will need to 
install this package in addition to the php package.


%prep
%setup -c -T
cp -dpR %{_usrsrc}/php-devel/extensions/%{dirname}/* .

%build

#%{phpsource}/buildext %{extname} "gd.c gdttf.c gdcache.c gdt1.c" \
#        "-ljpeg -lpng -lgd -lttf -lt1 -lc" "-DCOMPILE_DL_GD \
#        -DHAVE_LIBGD -DHAVE_LIBGD13 -DHAVE_LIBGD15 \
#        -DHAVE_COLORCLOSESTHWB -DHAVE_GDIMAGECOLORRESOLVE \
#        -DHAVE_GD_PNG -DHAVE_LIGPNG \
#        -DHAVE_GD_JPG -DHAVE_LIBJPEG \
#        -DHAVE_GD_WBMP -DHAVE_WMBP -DHAVE_GD_XPM -DHAVE_GD_XBM \
#        -DHAVE_LIBT1 -DHAVE_LIBFREETYPE -DHAVE_LIBT1_OUTLINE \
#        -DENABLE_GD_TTF -DUSE_GD_IMGSTRTTF \
#        -DHAVE_GD_STRINGTTF -DHAVE_GD_STRINGFT \
#        -I/usr/include/freetype2 -I/usr/include/freetype2/freetype"

phpize
export LIBS="$LIBS -lm"
%configure2_5x \
    --with-jpeg-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-zlib-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix}/X11R6 \
    --with-ttf=%{_prefix} \
    --with-freetype-dir=%{_prefix} \
    --enable-gd-native-ttf 

%make
mv modules/*.so .
chrpath -d %{soname}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{phpdir}/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{phpdir}/extensions/

cat > README.%{modname} <<EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README*
%config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%{phpdir}/extensions/%{soname}

%changelog
* Sat May 14 2005 Vincent Danen <vdanen@annvix.org> 4.3.11-1avx
- php 4.3.11

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 4.3.10-2avx
- spec cleanups

* Fri Dec 17 2004 Vincent Danen <vdanen@annvix.org> 4.3.10-1avx
- php 4.3.10

* Wed Sep 29 2004 Vincent Danen <vdanen@annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- use the %%configure2_5x macro (oden)
- remove the perl hack, the fix is included (oden)
- move scandir to /etc/php.d

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- minor spec cleanups

* Fri Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-4mdk
- built for 4.3.3
- buildrequires chrpath >= 0.10-4mdk
- t1lib is not required anymore
- misc spec file fixes

* Wed Aug 20 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3.2-3mdk
- Nuke implicit Requires

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Tue May 06 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild (thanks to Pascal Terjan for the help!)

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuild

* Sun Jan  5 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New 4.3.0 release
- Totally macroize based on suggestions from Alexander Skwar
- New method of installing extensions thanks to Oden Eriksson
- Use phpize instead of buildext since GD is now bundled with PHP, 
  and there are *tons* of new defines...
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Sat Sep  7 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3 maintenance release
- Do not reload apache

* Thu Aug 22 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.2.2-1mdk
- Rebuild for 4.2.2
- Macroize a bit more, make version depend on "php -v"

* Tue Aug  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.2.1-3mdk
- rebuild for libintl.so.2

* Sun May 26 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-2mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.1-1mdk
- updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>
	- misc spec file fixes
	- PHP 4.2.1

* Mon Apr 29 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.2.0-1mdk
- Updated by Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	- misc spec file fixes
	- PHP 4.2.0

* Mon Mar 04 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.1.2-1mdk
- PHP 4.1.2

* Wed Jan 09 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-2mdk
- Add -DHAVE_GD_STRINGTTF -DHAVE_GD_STRINGFT -DHAVE_GD_STRINGFTEX

* Mon Jan 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.1-1mdk
- PHP 4.1.1.

* Tue Dec 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.1.0-1mdk
- Update Requires and BuildRequires.
- PHP 4.1.0.

* Fri Nov 16 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-4mdk
- Fix no-url-tag and invalid-packager warnings in rpmlint.

* Wed Oct 10 2001 Stefan van der Eijk <stefan@eijk.nu> 4.0.6-3mdk
- BuildRequires: libjpeg-devel
- Adjust Requires: libpng2 --> libpng3

* Mon Sep 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 4.0.6-2mdk
- Provides the Obsoletes for compatibility.

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 4.0.6-1mdk
- 4.0.6
- BuildRequires: freetype-devel
- remove -D_HAVE_CONFIG from buildext command

* Thu Apr 19 2001 David BAUDENS <baudens@mandrakesoft.com> 4.0.4pl1-7mdk
- Fix BuildRequires on libgd*-devel to allow build

* Fri Apr 13 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-6mdk
- fix requires
- made it working with gd 1.8.4 to have working jpeg support at last

* Mon Apr  9 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-5mdk
- fix post scripts for good 

* Mon Apr  2 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.0.4pl1-4mdk
- Split gd package from php package so that when a new gd 
  package comes out, we don't have to recompile php, only this module
