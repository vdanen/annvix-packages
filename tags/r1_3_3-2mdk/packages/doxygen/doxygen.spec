%{expand:%%define buildfor8_2 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 8.2 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor9_0 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 9.0 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor9_1 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 9.1 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor9_2 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 9.2 ]; then echo 1; else echo 0; fi)}

%define name doxygen
%define version 1.3.3
%define release 2mdk

%define builddoc 1
%{?_without_doc: %{expand: %%global builddoc 0}}

Name: %{name}
Summary: Doxygen is THE documentation system for C/C++
Version: %{version}
Release: %{release}
Group: Development/Other
License: GPL
URL: http://www.stack.nl/~dimitri/doxygen/
Source:	ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.bz2
Source1: GPL-LICENSE.bz2
Patch0: doxygen-1.2.12-fix-latex.patch.bz2
Patch1: doxygen-1.2.16-fix-for-qt3.patch.bz2
BuildRequires:	XFree86-devel
BuildRequires:	flex
BuildRequires:	gcc-c++
%if !%buildfor9_2
BuildRequires:	libqt3-devel
%else
BuildRequires:  qt3-devel
%endif

%if %builddoc
BuildRequires:	tetex-latex
BuildRequires:	ghostscript
%endif
Packager: Guillaume Cottenceau <gc@mandrakesoft.com>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Epoch: 1

%description
Doxygen is a documentation system for C, C++ and IDL. It can generate
an on-line class browser (in HTML) and/or an off-line reference manual
(in LaTeX) from a set of documented source files. There is also
support for generating man lpages and for converting the generated
output into Postscript, hyperlinked PDF or compressed HTML. The
documentation is extracted directly from the sources.

Doxygen can also be configured to extract the code-structure from
undocumented source files. This can be very useful to quickly find
your way in large source distributions.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
perl -pi -e "s|^TMAKE_CFLAGS_RELEASE.*|TMAKE_CFLAGS_RELEASE = $RPM_OPT_FLAGS|" tmake/lib/linux-g++/tmake.conf
%ifarch x86_64 sparc64 ppc64 s390x
perl -pi -e "s|(QTDIR/)lib|\1%{_lib}|" configure
perl -pi -e "s|/lib$|/%{_lib}|" tmake/lib/linux-g++/tmake.conf
%endif
find -type d -exec chmod 0755 {} \;

%build
export QTDIR=/usr/lib/qt3
export PATH="$PATH:$QTDIR/bin"
./configure --with-doxywizard
%make
%if %builddoc
make docs
mv doc/float.sty latex
mv doc/fancyhdr.sty latex
make pdf
mkdir pdf
mv latex/doxygen_manual.pdf pdf
%endif
bzcat %{SOURCE1} > LICENSE

%install
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -s bin/doxy* ${RPM_BUILD_ROOT}%{_bindir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, root)
%if %builddoc
%doc html examples pdf
%endif
%doc README LICENSE
%{_bindir}/doxygen
%{_bindir}/doxytag
%{_bindir}/doxysearch
%{_bindir}/doxywizard

%changelog
* Tue Sep 02 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.3.3-2mdk
- fix problem libification

* Wed Aug  6 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3.3-1mdk
- new version

* Thu Jun 19 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3.2-1mdk
- new version

* Sat Jun 14 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.3.1-2mdk
- add --without doc option
- use %%make instead make

* Wed May 28 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3.1-1mdk
- new release

* Fri Apr 25 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3-1mdk
- new version

* Wed Feb 19 2003 Giuseppe Ghibo <ghibo@mandrakesoft.com> 1.2.18-3mdk
- Modified Patch0 to let package build with latest teTeX 2.0.1.

* Mon Nov 11 2002 Stefan van der Eijk <stefan@eijk.nu> 1.2.18-2mdk
- introduce patch2 to cure the fileutils --> coreutils switch

* Wed Oct  9 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.18-1mdk
- new version

* Thu Sep 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.17-3mdk
- Fix build on lib64 platforms

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.17-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Jul 29 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.17-1mdk
- new version

* Fri May 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.16-1mdk
- new version
- patch #1 to be able to use QT3
- manual is no longer available as ps, so feature the pdf version

* Wed Apr  3 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.15-1mdk
- new version

* Thu Feb 21 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.14-2mdk
- fix permissions so that percent-clean is now possible

* Tue Feb 19 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.14-1mdk
- new version

* Sun Feb 10 2002 Stefan van der Eijk <stefan@eijk.nu> 1.2.13.1-2mdk
- BuildRequires: flex

* Fri Jan 11 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.13.1-1mdk
- new version
- we need to add $QTDIR/bin to the PATH in order to get moc..

* Mon Dec 03 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.2.12-2mdk
- added newer float.sty for correctly building the documentation.

* Fri Nov 23 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.12-1mdk
- new version
- at last write a patch in sourcecode so that generation of latex is valid

* Fri Oct 12 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.10-2mdk
- rebuild for libpng3
- fix obsolete-tag Serial

* Fri Sep 28 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.10-1mdk
- version 1.2.10

* Mon Aug  6 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.9.1-1mdk
- new version
- no separate frontend generating xml anymore

* Mon Jul 23 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.8.1-2mdk
- provides doxywizard and doxygen_xml, thanks to Konrad.Bernloehr@mpi-hd.mpg.de

* Fri Jun 15 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.8.1-1mdk
- version 1.2.8.1

* Fri Jun  8 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.8-1mdk
- version 1.2.8

* Fri May  4 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.7-1mdk
- 1.2.7

* Thu Apr 26 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.6-1mdk
- revert Dadou's changes to my specfile - wonder if this shit with Dadou
  changing specfiles to fit his cosmetik desires will end someday
- 1.2.6

* Tue Feb 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.5-1mdk
- new and shiny source.

* Tue Jan  2 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.4-1mdk
- 1.2.4 (happy new year)

* Thu Dec 14 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.2.3-3mdk
- do not exclude Alpha

* Fri Nov  3 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.3-2mdk
- recompile against newest libstdc++

* Tue Oct 31 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.3-1mdk
- 1.2.3

* Thu Oct 12 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.2-1mdk
- 1.2.2

* Wed Aug 23 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.1-2mdk
- automatically added packager tag

* Sun Aug 13 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.2.0-2mdk
- automatically added BuildRequires

* Mon Jul 24 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.2.0-1mdk
- 1.2.0

* Thu Jul 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.0-4mdk
- BM
- macros

* Wed May 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.0-3mdk
- ExcludeArch: alpha (yep lazzyness).

* Sat Apr  1 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.0-1mdk
- first Mandrake release
- patch to fix wrong lookup of Qt include/lib
