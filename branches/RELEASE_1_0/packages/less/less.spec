%define name	less
%define version	382
%define release	1avx

Summary:	A text file browser similar to more, but better.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		http://www.greenwoodsoftware.com/less
Source:		ftp://ftp.gnu.org/pub/gnu/less/%name-%version.tar.bz2
Source1:	faq_less.html
Source2:	lesspipe.sh
Patch0:		less-374-manpages.patch.bz2

Buildroot:	%_tmppath/%name-root
BuildRequires:	ncurses-devel

# lesspipe.sh requires file
Requires:	file

%description
The less utility is a text file browser that resembles more, but has
more capabilities.  Less allows you to move backwards in the file as
well as forwards.  Since less doesn't have to read the entire input file
before it starts, less starts up more quickly than text editors (for
example, vi). 

%prep
%setup -q
%patch0 -p1

%build
CFLAGS=$(echo "%{optflags} -DHAVE_LOCALE" | sed -e s/-fomit-frame-pointer//)
%configure
%make 

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
# faq
install -m 644 %SOURCE1 .
install -m 755 %SOURCE2 %{buildroot}/%{_bindir}/

mv %{buildroot}%{_bindir}/{less,less.bin}
cat << EOF > %{buildroot}%{_bindir}/less
#!/bin/sh

#export LESSCHARSET="\${LESSCHARSET:-utf-8}"
export LESSCHARSET="\${LESSCHARSET:-koi8-r}"
exec less.bin "\$@"
EOF

install -m 644 less{echo,pipe}.1 %{buildroot}%{_mandir}/man1

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc faq_less.html
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Sep 22 2004 Vincent Danen <vdanen@annvix.org> 382-1avx
- 382
- spec cleanups

* Wed Jun 23 2004 Vincent Danen <vdanen@annvix.org> 381-5avx
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
