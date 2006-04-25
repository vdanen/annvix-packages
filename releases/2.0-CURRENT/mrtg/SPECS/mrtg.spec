#
# spec file for package mrtg
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define	name		mrtg
%define version		2.13.2
%define release		%_revrel

%define _provides_exceptions perl(MRTG_lib)\\|perl(locales_mrtg)\\|perl(stat.pl)\\|perl(find.pl)\\|perl(MRP::BaseClass)\\|%{_bindir}/ksh\\|%{_bindir}/expect
%define _requires_exceptions perl(MRTG_lib)\\|perl(locales_mrtg)\\|perl(stat.pl)\\|perl(find.pl)\\|perl(MRP::BaseClass)\\|%{_bindir}/ksh\\|%{_bindir}/expect\\|pear(.*.inc.php)\\|perl(Net::SNMP)

Summary:	Multi Router Traffic Grapher
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.mrtg.org/
Source0:	http://people.ee.ethz.ch/~oetiker/webtools/mrtg/pub/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gd-devel, zlib-devel, png-devel
BuildPreReq:	chrpath

Requires:	perl, net-snmp

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the
traffic load on network-links. MRTG generates HTML pages containing
PNG images which provide a LIVE visual representation of this traffic.


%package contribs
Summary:	Multi Router Traffic Grapher contribs
Group:		Networking/Other
Requires:	%{name} = %{version}
Requires(pre):	expect
Requires(pre):	pdksh

%description contribs
Contributed softwares for The Multi Router Traffic Grapher (MRTG)


%prep
%setup -q

# cleanups
perl -pi -e "s|^sleep .*||g" configure*

# fix perl path
find -type f | xargs perl -pi -e "s|/store/bin/perl|%{_bindir}/perl|g; \
    s|/usr/local/bin/perl|%{_bindir}/perl|g; \
    s|/usr/sepp/bin/perl|%{_bindir}/perl|g; \
    s|/usr/tardis/local/gnu/bin/perl5|%{_bindir}/perl|g; \
    s|/usr/local/gnu/bin/perl5|%{_bindir}/perl|g; \
    s|/usr/drwho/local/bin/perl|%{_bindir}/perl|g; \
    s|c\:\\\perl\\\bin|%{_bindir}/perl|g; \
    s|/opt/gnu/bin/perl|%{_bindir}/perl|g; \
    s|/pkg/gnu/bin/perl|%{_bindir}/perl|g"


%build
export LIBS="$LIBS -L%{_prefix}/X11R6/%{_lib} -lXpm -lX11"

%configure \
    --with-gd=%{_prefix} \
    --with-gd-lib=%{_libdir} \
    --with-gd-inc=%{_includedir} \
    --with-z=%{_prefix} \
    --with-z-lib=%{_libdir} \
    --with-z-inc=%{_includedir} \
    --with-png=%{_prefix} \
    --with-png-lib=%{_libdir} \
    --with-png-inc=%{_includedir}

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_datadir}
mkdir -p %{buildroot}/var/www/html/mrtg
mkdir -p %{buildroot}%{perl_vendorarch}

find contrib | cpio -dpm %{buildroot}%{_datadir}/mrtg2

install -m 0644 images/*.png %{buildroot}/var/www/html/mrtg
install -m 0644 -c lib/mrtg2/{Pod/*pm,*pm} %{buildroot}%{perl_vendorarch}/

# clean up
rm -rf %{buildroot}/%{_libdir}/mrtg2/{*gif,*png,Pod/*pm,*pm}
rm -rf %{buildroot}/%{_libdir}/mrtg2/contrib/mrtgmk/src/

pushd %{buildroot}/%{_datadir}/mrtg2
    for i in `find -name "*.h"` `find -name "*.c"`; do
	rm -f $i
    done
popd

rm -f %{buildroot}/var/www/html/mrtg/*-nt*
rm -f %{buildroot}%{_mandir}/man1/*-nt*

rm -rf %{buildroot}/usr/doc/mrtg2
rm -rf %{buildroot}/usr/share/mrtg2/icons

# fix the stupid rpatch stuff...
chrpath -d %{buildroot}%{_bindir}/rateup

# clean up
mv %{buildroot}%{_datadir}/doc/mrtg2 .


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ANNOUNCE CHANGES MANIFEST README THANKS
%doc doc/cfgmaker.txt
%doc doc/mrtg-faq.txt
%doc doc/mrtg-forum.txt
%doc doc/index.txt
%doc doc/indexmaker.txt
%doc doc/mrtg-logfile.txt
%doc doc/mrtg-mibhelp.txt
%doc doc/mrtg-rrd.txt
%doc doc/mrtg.txt
%doc doc/mrtglib.txt
%doc doc/mrtg-reference.txt
%doc doc/mrtg-squid.txt
%doc doc/mrtg-unix-guide.txt
%doc doc/mrtg-webserver.txt
%attr(755,root,root) %dir /var/www/html/mrtg
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{perl_vendorarch}/*
%{_mandir}/man1/cfgmaker.1*
%{_mandir}/man1/mrtg-faq.1*
%{_mandir}/man1/mrtg-forum.1*
%{_mandir}/man1/indexmaker.1*
%{_mandir}/man1/mrtg-logfile.1*
%{_mandir}/man1/mrtg-mibhelp.1*
%{_mandir}/man1/mrtg-rrd.1*
%{_mandir}/man1/mrtg.1*
%{_mandir}/man1/mrtglib.1*
%{_mandir}/man1/mrtg-reference.1*
%{_mandir}/man1/mrtg-squid.1*
%{_mandir}/man1/mrtg-unix-guide.1*
%{_mandir}/man1/mrtg-webserver.1*
%{_mandir}/man1/mrtg-ipv6.1*
%{_mandir}/man1/mrtg-nw-guide.1*
%attr(644,root,root) /var/www/html/mrtg/*

%files contribs
%defattr(-,root,root)
%doc doc/mrtg-contrib.txt
%{_mandir}/man1/mrtg-contrib.1*
%{_datadir}/mrtg2/contrib/*


%changelog
* Tue Apr 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13.2
- exclude requires on Net::SNMP until we can bundle it and the dozen or so
  modules it requires (only really required for SNMP v3 support)

* Fri Apr 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13.2
- first Annvix build

* Tue Jan 31 2006 Oden Eriksson <oeriksson@mandriva.com> 2.13.1-1mdk
- 2.13.1 (Major feature enhancements)

* Fri Sep 16 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.12.2-2mdk
- explicit exceptions for wrong pear dependencies

* Wed Aug 17 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.12.2-1mdk
- New release 2.12.2

* Wed May 18 2005 Oden Eriksson <oeriksson@mandriva.com> 2.12.1-1mdk
- 2.12.1 (Major bugfixes)
- strip away annoying ^M

* Sun Apr 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.11.1-2mdk
- make it compile on 10.0 too

* Fri Jan 07 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.11.1-1mdk
- 2.11.1

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 2.10.15-3mdk
- Rebuild for new perl

* Fri Oct 10 2004 Robert Vojta <robert.vojta@mandrake.org> 2.10.15-2mdk
- use /etc/cron.d/mrtg instead of /etc/crontab (#6279)

* Sun Aug 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.10.15-1mdk
- 2.10.15

* Fri Jun 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.10.14-2mdk
- rebuilt against new gd

* Wed Jun 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.10.14-1mdk
- 2.10.14
- use simpler spec magic

* Mon Feb 09 2004 Pascal Terjan <pterjan@mandrake.org> 2.10.13-1mdk
- Few improvements over Loïc changes so that the spec is also fine for
  cooker.
- From Loïc Vaillant <loic.vaillant@edge-it.fr>
 - 2.10.13
 - mdk release control for png library

* Mon Jan 05 2004 Lenny Cartier <lenny@mandrakesoft.com> 2.10.12-1mdk
- 2.10.12
- change doc names in the filelist reflecting changes in this release

* Sun Nov 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.10.6-1mdk
- 2.10.6

* Sun Oct 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.10.5-3mdk
- exclude some more stuff from the autorequires "magic"

* Wed Oct 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.10.5-2mdk
- use the %%define _provides_exceptions macro
- use the %%define _requires_exceptions macro
- fix perl path

* Wed Oct 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.10.5-1mdk
- 2.10.5

* Tue Apr 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.29-2mdk
- fix buildrequires, thanks to Stefan van der Eijks robot

* Tue Apr 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.29-1mdk
- 2.9.29

* Mon Feb 24 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.27-1mdk
- 2.9.27
- require net-snmp for cfgmaker & indexmaker

* Thu Feb 13 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.9.25-5mdk
- rebuild

* Tue Jan 28 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.9.25-4mdk
- rebuild

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.25-3mdk
- rebuilt against gd2

* Mon Nov 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.25-2mdk
- misc spec file fixes (argh!!!)

* Mon Nov 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.25-1mdk
- new version
- fix no doc or icons install, handled by rpm instead
- fix rpatch stuff in %{_bindir}/rateup to make rpmlint happier
- move contribs to %{_datadir}/mrtg2 into a subpackage, and also make 
  rpmlint happier
- misc spec file fixes

* Fri Oct 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.22-1mdk
- new version
- remove P0, it's fixed in the source

* Sun Aug 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.21-3mdk
- rebuilt against new multi threaded perl

* Tue Jul 23 2002 Pixel <pixel@mandrakesoft.com> 2.9.21-2mdk
- fix $VERSION in @ISA (stupid?!)

* Mon Jul 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.21-1mdk
- new version
- misc spec file fixes and clean ups

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.18-1mdk
- new version

* Mon May 20 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.17-5mdk
- rebuilt with gcc3.1

* Sun Dec 2 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.9.17-4mdk
- spec file cleanup
- removed obsolete patches
- provide only *.png files, otherwise you could get sued by unisys...

* Sun Dec  2 2001 Stefan van der Eijk <stefan@eijk.nu> 2.9.17-3mdk
- fix %%files section

* Mon Oct 15 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.9.17-2mdk
- rebuild against new libpng

* Mon Sep 17 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.9.17-1mdk
- 2.9.17

* Sun Sep  2 2001 Daouda LO <daouda@mandrakesoft.com> 2.9.7-2mdk
- rebuilt against gd.

* Mon Jan 22 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.9.7-1mdk
- updated 2.9.7

* Thu Dec 14 2000 Florin Grad <florin@mandrakesoft.com> 2.9.6-1mdk
- 2.9.6
- update the patch
- remove the mv command in postun (it's cp now :) rpmlint-wise

* Fri Oct 27 2000 Vincent Saugey <vince@mandrakesoft.com> 2.9.4-2mdk
- Adding man page in package !!!

* Fri Oct 26 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.9.4-1mdk
- updated to 2.9.4
- remove backup files

* Mon Oct 02 2000 Florin Grad <florin@mandrakesoft.com> 2.9.0pre24-1mdk
- lot of spec restructuring
- new beta version

* Mon Sep 11 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.8.12-1mdk
- BM
- macros
- v2.8.12

* Tue May 02 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.8.9-3mdk
- fix group
- clean spec

* Tue Dec 21 1999 Philippe Libat <philippe@mandrakesoft.com>
- [2.8.9]
  Install locales_mrtg.pm in %{siteperldir}

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Reprefixing to /usr (RTFHS).

* Wed Jul 14 1999 Oden Eriksson <oden.eriksson@kvikkjokk.net>
  [2.7.5]
  Moved over to /usr/local/
  Removed the stupid GIF89a feature.
  
* Tue Mar  2 1999 Henri Gomez <gomez@slib.fr>
  [2.6.6]
  
* Wed Feb 17 1999 Henri Gomez <gomez@slib.fr>
  [2.6.4]
- removed mrtg-squid (specific OIDS)
- cfgmaker and indexmaker now /usr/bin
- libgd must be >= 1.3

* Fri Jan 29 1999 Henri Gomez <gomez@slib.fr>
  [2.5.4c-3]
- Added mrtg-squid to monitor squid (specific OIDS)

* Fri Jan 28 1999 Henri Gomez <gomez@slib.fr>
  [2.5.4c-2]
- applied squid snmp patch

* Wed Jan 27 1999 Henri Gomez <gomez@slib.fr>
  [2.5.4c-1] 
- upgraded to 2.5.4c.
- added require libgd-devel

* Mon Nov 30 1998 Arne Coucheron <arneco@online.no>
  [2.5.4a-1]

* Thu Jun 18 1998 Arne Coucheron <arneco@online.no>
  [2.5.3-1]
- using %%{name} and %%{version} macros
- using %defattr macro in filelist
- using install -d in various places instead of cp
- added -q parameter to %setup
- removed older changelogs
