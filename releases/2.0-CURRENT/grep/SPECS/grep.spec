#
# spec file for package grep
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		grep
%define version 	2.5.1a
%define release 	%_revrel

%define _bindir 	/bin

Summary:	The GNU versions of grep pattern matching utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://www.gnu.org/software/grep/grep.html
Source:		ftp://ftp.gnu.org/pub/gnu/grep/%{name}-%{version}.tar.bz2
Patch1:		grep-2.5.1-i18n-0.1.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	pcre-devel
BuildRequires:	texinfo

Requires:	libpcre

%description
The GNU versions of commonly used grep utilities.  Grep searches one or
more input files for lines which contain a match to a specified pattern
and then prints the matching lines.  GNU's grep utilities include grep,
egrep and fgrep.  


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1 -b .i18n


%build
%configure2_5x \
    --exec-prefix=/ \
    --without-included-regex
%make

make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_infodir}

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc AUTHORS THANKS TODO NEWS README ChangeLog


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a
- spec cleanups
- remove locales

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1a-1avx
- 2.5.1a
- rebuild against new pcre

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1-12avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1-11avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1-10avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-9avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-8sls
- Requires: libpcre, not /lib/libpcre.so.0

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-7sls
- drop unapplied P0
- drop BuildRequires: bison
- use %%makeinstall_std
- drop S10 and S11
- updated P1 from openi18n (re: abel)

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-6sls
- minor spec cleanups
- get rid of doc package (who needs info pages for grep anyways?!?)

* Sat Jan 04 2004 Vincent Danen <vdanen@opensls.org> 2.5.1-5sls
- requires pcre-devel not libpcre-devel (for amd64)

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 2.5.1-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
