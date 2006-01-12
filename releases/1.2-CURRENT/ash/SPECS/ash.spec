#
# spec file for package ash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ash
%define version		0.3.8
%define release		%_revrel

Summary:	The Almquist shell
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Shells

Source:		%{name}-%{version}.tar.gz
Patch0:		ash-0.3.8-gcc.patch
Patch1:		ash-0.3.8-defpath.patch
Patch2:		ash-0.3.8-dietlibc.patch
Patch3:		ash-0.3.8-stat.patch
Patch4:		ash-0.3.8-fixyaccparser.patch
Patch5:		ash-0.3.8-getcwd.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	binutils, flex, gcc, make, byacc
BuildRequires:	dietlibc-devel

Provides:	ash-static

%description
The Almquist shell is a clone of Berkeley's Bourne shell. Ash
supports all of the standard sh shell commands and is considerably
smaller than bash. The ash shell lacks some features (for example,
command-line history), but needs a lot less memory.

This package contains a small, statically linked version of ash 
that can be handy for system recovery or as a fail-safe interactive
shell for the superuser.


%prep
%setup -q
%patch0 -p1 -b .gcc
%patch1 -p1 -b .defpath
%patch2 -p1 -b .dietlibc
%ifarch s390 alpha
%patch3 -p1 -b .stat
%endif
%patch4 -p1 -b .fixyaccparser
%patch5 -p1 -b .getcwd


%build
make STATIC=-static


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -D -m 0755 sh %{buildroot}/sbin/bsh
install -D -m 0644 sh.1 %{buildroot}%{_mandir}/man1/ash.1
mkdir %{buildroot}/bin
ln -s /sbin/bsh %{buildroot}/bin/ash
ln -s /sbin/bsh %{buildroot}/bin/bsh
ln -s ash.1 %{buildroot}%{_mandir}/man1/bsh.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /bin/ash
# Add /etc/shells entry without using external commands
SHELLS=%{_sysconfdir}/shells
for sh in /bin/ash /bin/bsh; do
    while read i; do [ "$i" = "$sh" ] && break; done < $SHELLS
    [ "$i" = "$sh" ] || echo $sh >> $SHELLS
done

%preun -p /bin/ash
# Remove /etc/shells entry without using external commands
if [ "$1" = "0" ]; then
    SHELLS=%{_sysconfdir}/shells
    TEMP=${SHELLS}-
    for sh in /bin/ash /bin/bsh; do
        while read i; do echo $i; done < $SHELLS > $TEMP
        while read i; do
            [ "$i" = "$sh" ] || echo $i
        done < $TEMP > $SHELLS
    done
fi


%files
%defattr(-,root,root)
/sbin/bsh
/bin/ash
/bin/bsh
%{_mandir}/man1/ash.1*
%{_mandir}/man1/bsh.1*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8-3avx
- rebuild against new dietlibc

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8-2avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8-1avx
- first Annvix build
- make it always build with dietlibc

* Wed May 25 2005 Claudio Matsuoka <claudio@mandriva.com> 0.3.8-8mdk
- fixed changelog

* Fri May 13 2005 Claudio Matsuoka <claudio@mandriva.com> 0.3.8-7mdk
- created Mandriva package of the Conectiva Linux static ash
- lifted restrictions on dietlibc for s390, alpha and sparc
- better post/postun scriptlets

* Thu Apr 15 2004 Wanderlei Antonio Cavassin <cavassin@conectiva.com.br>
+ 2004-04-15 10:13:41 (56995)
- Defined __DIETLIBC__ and forced use of internal getcwd function
  instead of /bin/pwd. Fixes that annoyance bug in mi's shell.

* Thu Mar 11 2004 Ricardo Erbano <erbano@conectiva.com>
+ 2004-03-11 10:17:52 (52166)
- Added patch file fixyaccparser to fix build error

* Tue Dec 30 2003 Arnaldo Carvalho de Melo <acme@conectiva.com.br>
+ 2003-12-30 19:04:19 (42615)
- Added some more BuildRequires

* Mon Aug 25 2003 Ricardo Erbano <erbano@conectiva.com>
+ 2003-08-25 15:16:26 (34605)
- Disabled dietlibc in sparc, closes: #7329

* Tue Sep 03 2002 Gustavo Niemeyer <niemeyer@conectiva.com>
+ 2002-09-03 14:15:09 (11123)
- Imported package from snapshot.

* Thu Aug 29 2002 Gustavo Niemeyer <niemeyer@conectiva.com>
+ 2002-08-29 17:19:26 (7317)
- Imported package from 8.0.

* Tue Aug 27 2002 Gustavo Niemeyer <niemeyer@conectiva.com>
+ 2002-08-27 18:40:24 (139)
- Imported package from 6.0.

* Tue Apr 30 2002 Flavio Bruno Leitner <flavio@conectiva.com>
+ ash-0.3.8-7cl
- Closes: #5409 (ash build fails on alpha)

* Sun Apr 28 2002 Claudio Matsuoka <claudio@conectiva.com>
+ ash-0.3.8-6cl
- building with glibc for alpha

* Fri Feb 22 2002 Claudio Matsuoka <claudio@conectiva.com>
+ ash-0.3.8-5cl
- building with glibc for S/390

* Tue Nov 13 2001 Claudio Matsuoka <claudio@conectiva.com>
+ ash-0.3.8-4cl
- installing as /sbin/bsh to prevent crap with bash scripts using !#/bin/sh
  when /sbin is before /bin in PATH

* Thu Nov 01 2001 Claudio Matsuoka <claudio@conectiva.com>
+ ash-0.3.8-3cl
- installing shell as /sbin/sh, symlinking from /bin/{a,b}sh

* Tue Oct 30 2001 Claudio Matsuoka <claudio@conectiva.com>
+ ash-0.3.8-2cl
- right, using /bin/ash as the shell for the rpm scriptlets ;)

* Mon Oct 29 2001 Claudio Matsuoka <claudio@conectiva.com>
+ ash-0.3.8-1cl
- new upstream release
- building with dietlibc

* Mon Apr 17 2000 Guilherme Wunsch Manika <gwm@conectiva.com>
- Misc. fixes
- Deal with compressed man pages

* Tue Jan 25 2000 Paulo Andrade <pcpa@conectiva.com>
- add patch to make ash behaviour identical to tcsh on background processes that receive SIGHUP

* Thu Sep 23 1999 Wanderlei Antonio Cavassin <cavassin@conectiva.com>
- fixed bug in mkinit
- fixed bug in test builtin command (patch from Carlos Santos)
