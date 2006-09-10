#
# spec file for package less
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		less
%define version		394
%define release		%_revrel

%define lessp_ver	1.53

Summary:	A text file browser similar to more, but better
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://www.greenwoodsoftware.com/less
Source:		ftp://ftp.gnu.org/pub/gnu/less/%{name}-%{version}.tar.bz2
Source1:	faq_less.html
Source2:	http://www-zeuthen.desy.de/~friebel/unix/less/lesspipe-%{lessp_ver}.tar.bz2
Patch0:		less-374-mdv-manpages.patch
Patch1:		lesspipe.lynx_for_html-mdv.patch
Patch2:		lesspipe-1.53-mdv-posix.patch
Patch3:		less-382-fdr-fixline.patch
Patch4:		less-392-fdr-Foption.patch
Patch5:		lesspipe-1.53-mdv-no-o3read.patch

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel

# lesspipe.sh requires file
Requires:	file

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi). 


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 2
%patch0 -p1
pushd lesspipe-%{lessp_ver}
%patch1 -p1
%patch2 -p1
%patch5 -p1
chmod a+r *
popd

%patch3 -p1 -b .fixline
%patch4 -p1 -b .Foption


%build
CFLAGS=$(echo "%{optflags} -DHAVE_LOCALE" | sed -e s/-fomit-frame-pointer//)
%configure2_5x
%make 

pushd lesspipe-%{lessp_ver}
    ./configure --yes
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
# faq
install -m 0644 %SOURCE1 .

pushd lesspipe-%{lessp_ver}
    %makeinstall PREFIX=%{buildroot}%{_prefix}
popd

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
cat << EOF > %{buildroot}%{_sysconfdir}/profile.d/less.sh
#!/bin/sh
CHARSET=\$(locale charmap 2> /dev/null) 
case "\$CHARSET" in 
       UTF-8) 
               export LESSCHARSET="\${LESSCHARSET:-utf-8}" 
       ;; 
       * ) 
               export LESSCHARSET="\${LESSCHARSET:-koi8-r}" 
       ;; 
esac
# Make a filter for less
export LESSOPEN="|/usr/bin/lesspipe.sh %s"
EOF

cat << EOF > %{buildroot}%{_sysconfdir}/profile.d/less.csh
#!/bin/csh
if ! ( \$?LESSCHARSET ) then
	set CHARSET=\ocale charmap\
+	if ( "\$CHARSET" == "UTF-8" ) then
		setenv LESSCHARSET utf-8
	else
		setenv LESSCHARSET koi8-r
	endif
endif
# Make a filter for less
setenv LESSOPEN "|/usr/bin/lesspipe.sh %s"
EOF

cat << EOF > README.avx
This version of less includes lesspipe.sh from Wolfgang Friebel
( http://www-zeuthen.desy.de/~friebel//unix/less/ ).

This enables you to view gz, zip, rpm and html files
among others with less. It works by setting the LESSOPEN 
environment variable, see the man pages for details.

If you want to disable this behavior, either use 'unset LESSOPEN' or
use an alias ( alias less='less -l' ).

less will open html files with lynx, then html2text, then cat if
none of the previous were found.
EOF


install -m 0644 lessecho.1 %{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%attr(755,root,root)%_sysconfdir/profile.d/*

%files doc
%defattr(-,root,root)
%doc faq_less.html lesspipe-%{lessp_ver}/{BUGS,COPYING,ChangeLog,README,english.txt}
%doc README.avx


%changelog
* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 394
- 394
- lesspipe 1.53
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcedir/file instead of %%{SOURCEx}
- rediffed P2 from Mandriva
- P3: fix display of bogus newline for growing files (fedora)
- P4: fix the -F option (fedora)
- P5: improved less config (mdv)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 382
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 382
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-4avx
- lesspipe 1.52
- use lesspipe's included manpage
- move LESSOPEN variable to the profile.d scripts and remove less wrapper
  (waschk)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 382-2avx
- bootstrap build

* Wed Sep 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 382-1avx
- 382
- spec cleanups

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 381-5avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 381-4sls
- minor spec cleanups

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 381-3sls
- OpenSLS build
- tidy spec

* Sun Jun 15 2003 Stefan van der Eijk <stefan@eijk.nu> 381-2mdk
- BuildRequires

* Tue Feb 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 381-1mdk
- new release

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 378-2mdk
- build release

* Thu Oct 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 378-1mdk
- new release

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 376-3mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Tue Jul 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 376-2mdk
- requires file for lord gnome

* Tue Jul 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 376-1mdk
- new release
- update lesspipe.sh from 1.33 to 1.34
- requires less for lord gnome
- drop patch1

* Thu Apr 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 374-4mdk
- use koi8-r as default charset since this is the closest charset to an
  raw charset

* Wed Apr 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 374-3mdk
- really use utf-8 only by default, so that we don't overwrite
  $LESSCHARSET (escape $)
- "exec less.bin" instead of "less.bin; return $?"

* Mon Apr 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 374-2mdk
- less:
  $LESSCHARSET
- to screen.c: properly sets raw mode if stderr is redirected
  to /dev/null [Patch1]

* Mon Apr 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 374-1mdk
- new release
- utf8 overstriking fix has been merged upstream, dropping patch0
- upgrade to lesspipe.sh-1.33
- add Url
- add less{echo,pipe}(1) man pages

* Fri Jul 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 358-14mdk
- Don't hardcode /usr/bin in the less wrapper script (pixel).

* Sat Jun 23 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 358-13mdk
- Put double quotes around the definition of the LESSCHARSET variable
  in the hope that we can the tcltk build.
  
* Thu May 03 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 358-12mdk
- improved the utf8 patch so it also works for underscores

* Thu May 03 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 358-11mdk
- improved the utf8 patch so it also works for underscores

* Fri Apr 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 358-10mdk
- Fix the script (oh silly me).

* Fri Apr 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 358-9mdk
- Wrapper script to define LESSCHARSET=utf-8 before running less.

* Sun Apr 08 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 358-8mdk
- Make it build without -fomit-frame-pointer to get -DHAVE_LOCALE support, or
  else we get a segfault.

* Sun Apr  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 358-7mdk
- By default don't render .html file in lesspipe.

* Fri Jan 12 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 358-6mdk
- Rebuild against last ncurses

* Thu Jan  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 358-5mdk
- Improve lesspipe.sh and don't make depend of file rpm.

* Sat Aug 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 358-4mdk
- Add lesspipe.sh here.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 358-3mdk
- automatically added BuildRequires

* Thu Jul 27 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 358-2mdk
- rebuild for BM

* Wed Jul 12 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 358-1mdk
- new release
- use more macros

* Thu Jun 29 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 346-2mdk
- added UTF-8 patch from Alastair.McKinstry@compaq.com
- modularized path names

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 346-1mdk
- new release

* Fri Mar 31 2000 Jerome Dumonteil <jd@mandrakesoft.com>
- use of _tmppath _prefix
- change copyright

*Mon Nov 01 1999 Vincent Saugey <vincent@mandrakesoft.com>
- add faq page to /usr/doc

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 340.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Update to 337
- Fix up URL
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- relocatable

* Tue Mar 16 1999 Preston Brown <pbrown@redhat.com>
- removed ifarch axp stuff for /bin/more, more now works on alpha properly.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Thu May 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 332 and built for Manhattan
- added buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
