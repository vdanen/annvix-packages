%define name	ocaml
%define version	3.06
%define release	13sls

%{!?build_opensls:%global build_opensls 0}

%define build_ocamlopt	1
%define build_ocamltk	1

Summary:	The Objective Caml compiler and programming environment
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	QPL & LGPL
Group:		Development/Other
URL:		http://www.ocaml.org/
Source0:	ftp://ftp.inria.fr/lang/caml-light/ocaml-3.06/ocaml-%{version}.tar.bz2
Source1:	ftp://ftp.inria.fr/lang/caml-light/ocaml-3.06/ocaml-%{version}-refman.html.tar.bz2
Source4:	%{name}.menu
Patch1:		ocaml-3.06-Tk_PhotoPutBlock-change-tk-8.4.patch.bz2
Patch3:		ocaml-3.00-ocamltags--no-site-start.patch.bz2
Patch6:		ocaml-3.04-do-not-add-rpath-X11R6_lib-when-using-option-L.patch.bz2
Patch7:		ocaml-3.05-no-opt-for-debug-and-profile.patch.bz2
Patch8:		ocaml-3.04-larger-buffer-for-uncaught-exception-messages.patch.bz2
Patch9:		ocaml-3.06-add-warning-for-unused-local-variables.patch.bz2
#(peroyvind) patches from debian
Patch10:	%{name}-3.06-configure-sparc-build.patch.bz2
Patch11:	%{name}-3.06-threads-fixes.patch.bz2
Patch12:	%{name}-3.06-gc-stat-aux-fix.patch.bz2
Patch13:	%{name}-3.06-doc-fixes.patch.bz2
Patch14:	%{name}-3.06-init-fixes.patch.bz2
Patch15:	ocaml-3.06-amd64.patch.bz2
Patch16:	ocaml-3.06-lib64.patch.bz2

BuildRoot:	%{_tmppath}/ocaml-root
BuildRequires: XFree86-devel ncurses-devel tk

Obsoletes:	ocaml-emacs
Provides:	ocaml-emacs

%description
Objective Caml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler and an
optimizing native-code compiler), an interactive toplevel system, Lex&Yacc
tools, a replay debugger, and a comprehensive library.

%if !%{build_opensls}
%package doc
Summary:	Documentation for OCaml
Group:		Books/Computer books
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for OCaml
%endif

%package -n camlp4
Summary:	Preprocessor for OCaml
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description -n camlp4
Preprocessor for OCaml

%package -n ocamltk
Summary:	Tk toolkit binding for OCaml
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description -n ocamltk
Tk toolkit binding for OCaml

%prep
%setup -q -T -b 0
%setup -q -T -D -a 1
%patch1 -p1
%patch3 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p0
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p1 -b .amd64
%patch16 -p1 -b .lib64

#- because of added warning for unused local variables, treating warning as errors is no good
perl -pi -e 's/-warn-error A/-w A/' `find -name "Makefile*"`
rm -rf `find -name .cvsignore`

%build
%ifarch alpha
echo %{optflags} | grep -q mieee || { echo "on alpha you need -mieee to compile ocaml"; exit 1; }
%endif

./configure -bindir %{_bindir} -libdir %{_libdir}/ocaml -mandir %{_mandir}/man1
make BYTECCCOMPOPTS="%{optflags}" NATIVECCCOMPOPTS="%{optflags}" world
%if %{build_ocamlopt}
make BYTECCCOMPOPTS="%{optflags}" NATIVECCCOMPOPTS="%{optflags}" opt opt.opt
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install BINDIR=%{buildroot}%{_bindir} LIBDIR=%{buildroot}%{_libdir}/ocaml MANDIR=%{buildroot}%{_mandir}

# remove stupid camlp4o.opt which can't work
rm -f %{buildroot}%{_bindir}/camlp4*.opt
rm -f %{buildroot}%{_mandir}/man1/camlp4*.opt.*

(cd emacs; make install install-ocamltags BINDIR=%{buildroot}%{_bindir} EMACSDIR=%{buildroot}%{_datadir}/emacs/site-lisp)

# fix
perl -pi -e "s|$RPM_BUILD_ROOT||" $RPM_BUILD_ROOT%{_libdir}/ocaml/ld.conf

%if %{build_ocamlopt}
# only keep the binary versions (which are much faster, and have no drawbacks (?))
for i in $RPM_BUILD_ROOT%{_bindir}/*.opt ; do
  nonopt=`echo $i | sed "s/.opt$//"`
  rm -f $nonopt
  ln -s `basename $i` $nonopt
done
%endif


install -d $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el
(require 'caml-font)
(autoload 'caml-mode "caml" "Caml editing mode" t)
(add-to-list 'auto-mode-alist '("\\\\.mli?$" . caml-mode))
EOF

# menu (kept in case we want to use it again one day)
#install -d $RPM_BUILD_ROOT%{_menudir}
#install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_menudir}/%{name}

# don't package mano man pages since we have the html files
rm -rf $RPM_BUILD_ROOT%{_mandir}/mano

export EXCLUDE_FROM_STRIP="ocamldebug ocamlbrowser"

rm -f %{name}.list
n="labltk|camlp4|ocamlbrowser|tkanim"
(cd $RPM_BUILD_ROOT ; find usr/bin ! -type d -printf "/%%p\n" | egrep -v $n) >> %{name}.list
(cd $RPM_BUILD_ROOT ; find usr/%{_lib}/ocaml ! -type d -printf "/%%p\n" | egrep -v $n) >> %{name}.list
(cd $RPM_BUILD_ROOT ; find usr/%{_lib}/ocaml   -type d -printf "%%%%dir /%%p\n" | egrep -v $n) >> %{name}.list

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.list
%defattr(-,root,root)
%doc Changes LICENSE README
%{_mandir}/man*/*ocaml*
#%{_menudir}/*
%{_datadir}/emacs/site-lisp/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*

%if !%{build_opensls}
%files doc
%defattr(-,root,root)
%doc htmlman/* 
%endif

%if %{build_ocamltk}
%files -n ocamltk
%defattr(-,root,root)
%doc otherlibs/labltk/README otherlibs/labltk/example*
%{_bindir}/*labltk*
%{_bindir}/ocamlbrowser
%{_libdir}/ocaml/*labltk*
%{_libdir}/ocaml/stublibs/dlllabltk.so
%{_libdir}/ocaml/stublibs/dlltkanim.so
%endif

%files -n camlp4
%defattr(-,root,root)
%{_mandir}/man*/*camlp4*
%{_bindir}/*camlp4*
%{_libdir}/ocaml/camlp4

%changelog
* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 3.06-13sls
- OpenSLS build
- tidy spec
- use %%build_opensls to not build -doc

* Thu Jul 24 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.06-12mdk
- Patch15: Integrate AMD64 port from 3.07b1
- Patch16: Enough of lib64 fixery to build ocamltk on amd64

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.06-11mdk
- rebuild

* Mon Jun 16 2003 Stefan van der Eijk <stefan@eijk.nu> 3.06-10mdk
- BuildRequires

* Mon Jun 16 2003 Pixel <pixel@mandrakesoft.com> 3.06-9mdk
- replace lib with %%{_lib} to fix build on boxes using /usr/lib64 

* Fri Jun 13 2003 Pixel <pixel@mandrakesoft.com> 3.06-8mdk
- no native build on x86_64, no ocamltk on x86_64

* Thu May 29 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.06-7mdk
- apply various debian patches
  - fix bus error that happens during compile under sparc (Patch10)
  - fix problem with threads hanging (Patch11) (deb bug #144719)
  - fix problems with random SIGSEGVs when using Unix.Largefile.stat and friends
    are used (Patch12) (deb bug #191582)
  - fix problems with man pages (Patch13) (deb bug #195581)
  - check for .ocamlinit in not only current directory, but home directory too
    (Patch14) (deb bug #166199)

* Sun Apr 13 2003 Pixel <pixel@mandrakesoft.com> 3.06-6mdk
- ocaml-3.06-Tk_PhotoPutBlock-change-tk-8.4 patch

* Fri Nov  8 2002 Pixel <pixel@mandrakesoft.com> 3.06-5mdk
- unused local variables: don't warn about unused "parser_env" since a lot of
  those appear in the output of ocamlyacc

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.06-4mdk
- fix doc subpackage group

* Tue Oct  8 2002 Pixel <pixel@mandrakesoft.com> 3.06-3mdk
- add dlllabltk.so in ocamltk and move dlltkanim.so from ocaml to ocamltk
- add warning for unused local variables

* Tue Aug 20 2002 Pixel <pixel@mandrakesoft.com> 3.06-2mdk
- re-upload

* Tue Aug 20 2002 Pixel <pixel@mandrakesoft.com> 3.06-1mdk
- new release

* Mon Jul 29 2002 Pixel <pixel@mandrakesoft.com> 3.05-1mdk
- new release

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.04-9mdk
- Automated rebuild in gcc3.1 environment

* Tue Mar 19 2002 Pixel <pixel@mandrakesoft.com> 3.04-8mdk
- larger buffer for uncaught exception messages

* Sun Jan 13 2002 Pixel <pixel@mandrakesoft.com> 3.04-7mdk
- don't include camlp4o.opt since it's of no use (one gets "native-code program cannot do a dynamic load")

* Sat Dec 29 2001 Pixel <pixel@mandrakesoft.com> 3.04-6mdk
- cleanup (based on the "official" srpm)
- ensure ocamltags is there

* Fri Dec 14 2001 Pixel <pixel@mandrakesoft.com> 3.04-5mdk
- drop patch0 (not needed anymore)
- fix camlp4 build (again, hopefull ok now)

* Fri Dec 14 2001 Pixel <pixel@mandrakesoft.com> 3.04-4mdk
- fix camlp4 build

* Thu Dec 13 2001 Pixel <pixel@mandrakesoft.com> 3.04-3mdk
- cleanup the spec using PREFIX (as done in debian's package)
- ensure rpath is not used for /usr/X11R6/lib

* Thu Dec 13 2001 Pixel <pixel@mandrakesoft.com> 3.04-2mdk
- fix /usr/lib/ocaml/ld.conf

* Wed Dec 12 2001 Pixel <pixel@mandrakesoft.com> 3.04-1mdk
- new version
- split: ocaml-doc, ocamltk, camlp4
- have ocamlc and ocamlopt symlinked ocamlc.opt and ocamlopt.opt
- remove info doc, html is enough

* Thu Sep  6 2001 Pixel <pixel@mandrakesoft.com> 3.02-3mdk
- fix missing Provides

* Mon Jul 30 2001 Pixel <pixel@mandrakesoft.com> 3.02-2mdk
- better caml-font enabling (that don't conflict with ocamltags)

* Mon Jul 30 2001 Pixel <pixel@mandrakesoft.com> 3.02-1mdk
- new version

* Thu Jul 26 2001 Pixel <pixel@mandrakesoft.com> 3.01-3mdk
- have caml-font enabled

* Sun Mar 25 2001 Pixel <pixel@mandrakesoft.com> 3.01-2mdk
- oops, forgot the info patch

* Thu Mar 22 2001 Pixel <pixel@mandrakesoft.com> 3.01-1mdk
- new version

* Mon Mar 19 2001 Pixel <pixel@mandrakesoft.com> 3.00-25mdk
- fix the ocaml.el (\\. -> \\\\.)

* Tue Dec 12 2000 Pixel <pixel@mandrakesoft.com> 3.00-24mdk
- ocamltags--no-site-start.patch

* Thu Nov  2 2000 Pixel <pixel@mandrakesoft.com> 3.00-23mdk
- fix silly #define clashing with new glibc

* Tue Oct 10 2000 Pixel <pixel@mandrakesoft.com> 3.00-22mdk
- add ocamltags (needs emacs)

* Mon Sep  4 2000 Pixel <pixel@mandrakesoft.com> 3.00-21mdk
- rebuild with spec-helper fixed

* Tue Aug 29 2000 Pixel <pixel@mandrakesoft.com> 3.00-20mdk
- fix info pages

* Tue Aug 29 2000 Pixel <pixel@mandrakesoft.com> 3.00-19mdk
- remove menu entry

* Wed Aug 23 2000 Pixel <pixel@mandrakesoft.com> 3.00-18mdk
- add packager

* Wed Aug 23 2000 Pixel <pixel@mandrakesoft.com> 3.00-17mdk
- add obsolete %{name}-emacs

* Tue Aug 22 2000 Pixel <pixel@mandrakesoft.com> 3.00-16mdk
- nicer site-start.d/ocaml.el (use add-to-list)

* Tue Aug 22 2000 Pixel <pixel@mandrakesoft.com> 3.00-15mdk
- fix missing %%config, add install info

* Tue Aug 22 2000 Pixel <pixel@mandrakesoft.com> 3.00-14mdk
- use %{_sysconfdir}/emacs/site-start.d for the caml-mode.el
- merge %{name} and %{name}-emacs

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.00-13mdk
- automatically added BuildRequires

* Tue Aug 01 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.00-12mdk
- relink with the new and shiny tcltk

* Wed Jul 26 2000 Pixel <pixel@mandrakesoft.com> 3.00-11mdk
- use %%{optflags} with omit-frame-buffer removed

* Tue Jul 25 2000 Pixel <pixel@mandrakesoft.com> 3.00-10mdk
- use %%{optflags} (so that there is -mieee on alpha)

* Sat Jul 22 2000 Pixel <pixel@mandrakesoft.com> 3.00-9mdk
- patch for camldebug.el to workaround the silly ocamldebug command not looking
in cwd

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 3.00-7mdk
- more macro (use clean clean_menus)

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 3.00-6mdk
- macroization
- BM

* Sun Jun 04 2000 David BAUDENS <baudens@mandrakesoft.com> 3.00-5mdk
- Fix %%{doc}
- Use %%{_tmppath} for BuildRoot

* Thu Jun  1 2000 Pixel <pixel@mandrakesoft.com> 3.00-4mdk
- change copyright

* Thu Jun  1 2000 Pixel <pixel@mandrakesoft.com> 3.00-3mdk
- takes care of ocamlbrowser and ocamldebug (these must not be stripped)

* Tue May 16 2000 Pixel <pixel@mandrakesoft.com> 3.00-2mdk
- add README to ocaml-emacs

* Mon May  1 2000 Pixel <pixel@mandrakesoft.com> 3.00-1mdk
- new version

* Mon Apr 10 2000 Pixel <pixel@mandrakesoft.com> 2.04-9mdk
- fix groups

* Tue Mar 28 2000 Pixel <pixel@mandrakesoft.com> 2.04-8mdk
- really add menu

* Mon Mar 27 2000 Pixel <pixel@mandrakesoft.com> 2.04-7mdk
- add menu

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 2.04-6mdk
- new group + cleanup

* Mon Dec  6 1999 Pixel <pixel@linux-mandrake.com>
- 2.04

* Fri Nov 26 1999 Pixel <pixel@linux-mandrake.com>
- 2.03 + cleanup

* Tue Nov 23 1999 Pixel <pixel@linux-mandrake.com>
- build root added

* Tue Jun 01 1999 Pixel <pixel@linux-mandrake.com>
- Hacked to package properly ocamltk

* Tue Dec 29 1998 Alexey Nogin <ayn2@cornell.edu>
- Do not include any /usr/lib/ocaml/*.ml files

* Fri Dec 11 1998 Alexey Nogin <ayn2@cornell.edu>
- Updated to ocaml-2.01

* Sun Nov 29 1998 Alexey Nogin <ayn2@cornell.edu>
- Divided ocaml RPM into ocaml and ocaml-emacs RPMs 
  to make it easier to have both ocaml and caml installed
  on the same machine

* Wed Nov 10 1998 Alexey Nogin <ayn2@cornell.edu>
- Changed SRPM according to RHCN Package Requirements
- Added LICENSE, Changelog and README files to the doc directory
