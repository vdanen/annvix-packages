%define name gif2png
%define version 2.4.7
%define release 1mdk

Name: %{name}
Summary: Tools for converting websites from using GIFs to using PNGs
Summary(fr): Outils de conversion de sites: convertit les GIFs en PNGs.
Summary(es): Herramienta para convertir sitios y imagenes de GIFs hacia PNGs.
Version: %{version}
Release: %{release}
Source: http://www.catb.org/~esr/gif2png/%{name}-%{version}.tar.bz2
Group: Graphics
BuildRequires: libpng-devel zlib-devel
URL: http://www.catb.org/~esr/gif2png/
BuildRoot: %{_tmppath}/%{name}-buildroot
License: MIT style
Requires: python

%description 
Tools for converting GIFs to PNGs.  The program gif2png converts GIF files 
to PNG files.  The Python script web2png converts an entire web tree, 
also patching HTML pages to keep IMG SRC references correct.

%description -l fr
Outil de conversion du format GIF au format PNG. Le programme gif2png
convertit les fichiers GIF au format PNG. Le script Python scanne une
arborescence web complete et modifie aussi les pages HTML afin de référencer
à nouveau les fichiers images <IMG SRC ...>.

%description -l es
Herramienta de conversion GIF hacia PNG. El programa gif2png convierte los
archivos GIF al formato PNG. El script Python convierte un arbol web completo
y modifica incluso las paginas html para poner al dia las referencias a
imagenes <IMG SRC ...>.

%prep
%setup -q

%build
%configure
%make
 
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc README NEWS COPYING AUTHORS
%{_mandir}/*/*
%{_bindir}/*
			 
%changelog
* Thu Jul 31 2003 Daouda LO <daouda@mandrakesoft.com> 2.4.7-1mdk
- release 2.4.7
- change url

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.4.6-2mdk
- rebuild
- use %%make macro
- rm -rf $RPM_BUILD_ROOT in %%install, not %%prep
- drop Prefix tag

* Fri Dec 27 2002 Daouda LO <daouda@mandrakesoft.com> 2.4.6-1mdk
- release 2.4.6
	o Document masters converted to DocBook
	o Work around an apparent automake bug that produced bad SRPMs
	o Man page typo fix

* Tue Jun 18 2002 Daouda LO <daouda@mandrakesoft.com> 2.4.4-1mdk
- 2.4.4 release

* Thu Oct 18 2001 Daouda LO <daouda@mandrakesoft.com> 2.4.2-2mdk
- s/Copyright/License 
- fix permissions on files

* Mon Jul 30 2001 Daouda LO <daouda@mandrakesoft.com> 2.4.2-1mdk
- release 2.4.2

* Fri Jan 05 2001 Geoff <snailtalk@mandrakesoft.com> 2.4.0-1mdk
- new and shiny source.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.3.2-3mdk
- automatically added BuildRequires

* Sun Jul 23 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.2-2mdk
- macroszifications
- full url for src
- rebuilt for BM

* Thu Apr 06 2000 Christopher Molnar <molnarc@mandrakesoft.com> 2.3.2-1mdk
- Updated Version 
- Fixed Group for Mandrake

* Tue Feb 15 2000 Geoffrey Lee <snailtalk@linux-mandrake.com>
- Updated to 2.3.1

* Mon Jan 03 2000 Lenny Cartier <lenny@mandrakesoft.com>
-v2.2.5

* Mon Nov 08 1999 Camille Begnis <camille@mandrakesoft.com>
 
- Upgraded to 2.1.1
               
* Mon Nov 02 1999 Camille Begnis <camille@mandrakesoft.com>

- Upgraded to 2.0.1
					 
* Mon Oct 25 1999 Camille Begnis <camille@mandrakesoft.com>

- Specfile adaptions for Mandrake,
- Add python requirement,
- gz to bz2 compression,	 
