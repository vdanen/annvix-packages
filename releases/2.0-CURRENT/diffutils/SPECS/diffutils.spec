#
# spec file for package diffutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		diffutils
%define version 	2.8.4
%define release 	%_revrel

Summary:	A GNU collection of diff utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/diffutils/
Source:		ftp://ftp.gnu.org/pub/gnu/diffutils-%{version}.tar.bz2
Source1:	%{name}-manpages.tar.bz2
Patch0:		diffutils-2.8.4-i18n.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5

Requires(post):	info-install
Requires(preun): info-install

%description
Diffutils includes four utilities:  diff, cmp, diff3 and sdiff.

  * Diff compares two files and shows the differences, line by line.
  * The cmp command shows the offset and line numbers where two files differ,
    or cmp can show the characters that differ between the two files.
  * The diff3 command shows the differences between three files. Diff3 can be
    used when two people have made independent changes to a common original;
    diff3 can produce a merged file that contains both persons' changes and
    warnings about conflicts.
  * The sdiff command can be used to merge two files interactively.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .i18n


%build
autoconf
%configure
%make PR_PROGRAM=%{_prefix}/bin/pr


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_mandir}/man1
bzcat %{_sourcedir}/%{name}-manpages.tar.bz2 | tar xf - -C %{buildroot}%{_mandir}/man1/

rm -fr %{buildroot}%{_infodir}/dir
   
%kill_lang %{name}
%find_lang %{name}


%post 
%_install_info diff.info

%preun
%_remove_install_info diff.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/diff.info*

%files doc
%defattr(-,root,root)
%doc NEWS README


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- spec cleanups
- remove locales

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- fix changelog
- really remove docs from the main package

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-10avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-9avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-8avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.8.4-7avx
- requiere packages not files
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.8.4-6sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.8.4-5sls
- OpenSLS build
- tidy spec
