#
# spec file for package ocaml
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ocaml
%define version		%{major}.%{minor}
%define release		%_revrel

%define major		3.09
%define minor		2

%define build_ocamlopt	1
%define build_ocamltk	0

# otherwise the auto-requires will add a requires on the currently installed ocaml
%define _requires_exceptions ocaml

Summary:	The Objective Caml compiler and programming environment
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	QPL & LGPL
Group:		Development/Other
URL:		http://www.ocaml.org/
Source0:	ftp://ftp.inria.fr/INRIA/cristal/caml-light/%{name}-%{major}/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.inria.fr/INRIA/cristal/caml-light/%{name}-%{major}/%{name}-%{major}-refman.html.tar.bz2
Patch0:		ocaml-3.00-ocamltags--no-site-start.patch
Patch1:		ocaml-3.04-do-not-add-rpath-X11R6_lib-when-using-option-L.patch
Patch2:		ocaml-3.05-no-opt-for-debug-and-profile.patch
Patch3:		ocaml-3.04-larger-buffer-for-uncaught-exception-messages.patch
Patch5:		ocaml-3.06-lib64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	XFree86-devel
BuildRequires:	ncurses-devel
BuildRequires:	tcl
BuildRequires:	tk

%description
Objective Caml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler and an
optimizing native-code compiler), an interactive toplevel system, Lex&Yacc
tools, a replay debugger, and a comprehensive library.


%package -n camlp4
Summary:	Preprocessor for OCaml
Group:		Development/Other
Requires:	%{name} = %{version}

%description -n camlp4
Preprocessor for OCaml

%if %{build_ocamltk}
%package -n ocamltk
Summary:	Tk toolkit binding for OCaml
Group:		Development/Other
Requires:	%{name} = %{version}

%description -n ocamltk
Tk toolkit binding for OCaml
%endif


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -T -b 0
%setup -q -T -D -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1 -b .lib64

rm -rf `find -name .cvsignore`


%build
%ifarch alpha
echo %{optflags} | grep -q mieee || { echo "on alpha you need -mieee to compile ocaml"; exit 1; }
%endif

./configure \
    -bindir %{_bindir} \
    -libdir %{_libdir}/ocaml \
    -mandir %{_mandir}/man1
make world
%if %{build_ocamlopt}
make opt opt.opt
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install BINDIR=%{buildroot}%{_bindir} LIBDIR=%{buildroot}%{_libdir}/ocaml MANDIR=%{buildroot}%{_mandir}

# remove stupid camlp4o.opt which can't work
rm -f %{buildroot}%{_bindir}/camlp4*.opt
rm -f %{buildroot}%{_mandir}/man1/camlp4*.opt.*

# fix
perl -pi -e "s|%{buildroot}||" %{buildroot}%{_libdir}/ocaml/ld.conf

%if %{build_ocamlopt}
# only keep the binary versions (which are much faster, and have no drawbacks (?))
for i in %{buildroot}%{_bindir}/*.opt ; do
    nonopt=`echo $i | sed "s/.opt$//"`
    rm -f $nonopt
    ln -s `basename $i` $nonopt
done
%endif


# don't package mano man pages since we have the html files
rm -rf %{buildroot}%{_mandir}/mano
# remove the other manpages we don't want
rm -rf %{buildroot}%{_mandir}/man3


rm -f %{name}.list
n="labltk|camlp4|ocamlbrowser|tkanim"
(cd %{buildroot} ; find usr/bin ! -type d -printf "/%%p\n" | egrep -v $n) >> %{name}.list
(cd %{buildroot} ; find usr/%{_lib}/ocaml ! -type d -printf "/%%p\n" | egrep -v $n) >> %{name}.list
(cd %{buildroot} ; find usr/%{_lib}/ocaml   -type d -printf "%%%%dir /%%p\n" | egrep -v $n) >> %{name}.list


%if !%{build_ocamltk}
rm -f %{buildroot}%{_bindir}/*labltk*
rm -f %{buildroot}%{_bindir}/ocamlbrowser
rm -rf %{buildroot}%{_libdir}/ocaml/*labltk*
rm -f %{buildroot}%{_libdir}/ocaml/stublibs/{dlllabltk,dlltkanim}.so
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.list
%defattr(-,root,root)
%{_mandir}/man*/*ocaml*
%{_mandir}/man*/*ocpp*

%if %{build_ocamltk}
%files -n ocamltk
%defattr(-,root,root)
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

%files doc
%defattr(-,root,root)
%doc Changes LICENSE README
%doc otherlibs/labltk/README otherlibs/labltk/example*


%changelog
* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.09.2
- rebuild against new ncurses
- clean spec

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.09.2
- 3.09.2
- drop P4; included upstream
- don't build ocamltk; nothing needs it and we don't want it
- fix some requires_on_release
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.08.3
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.08.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.08.3-2avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.08.3-1avx
- 3.08.3
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.08-2avx
- bootstrap build

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.08-1avx
- 3.08.0
- drop patches applied upstream
- drop S0 (don't need the menu)
- renumber patches
- no need to exclude from strip ocamldebug ocamlbrowser (they are now ocamlrun
  scripts) (pixel)
- don't modify BYTECCCOMPOPTS and NATIVECCCMPOPTS, otherwise
  -D_FILE_OFFSET_BITS=64 is dropped (bugzilla #9502)
  => don't pass optflags (hope it won't break AXP with needs -mieee) (pixel)
- have less warnings when compiling (pixel)
- BuildRequires: tcl (cjw)

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.06-15avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 3.06-14sls
- minor spec cleanups
- remove %%build_opensls macro
- remove emacs files

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 3.06-13sls
- OpenSLS build
- tidy spec
- use %%build_opensls to not build -doc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
