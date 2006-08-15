#
# spec file for package readline
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sed
%define version		4.1.5
%define release		%_revrel

Summary:	A GNU stream text editor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Editors
URL:		http://www.gnu.org/software/sed/
Source0:	ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.gz

Buildroot:	%{_buildroot}/%{name}-%{version}

Requires(post):	info-install
Requires(preun): info-install

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x --bindir=/bin
%make LDFLAGS=-s


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -rf %{buildroot}%{_datadir}/doc

%kill_lang %{name}
%find_lang %{name}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
/bin/sed 
%{_infodir}/sed.info*
%{_mandir}/man1/sed.1*

%files doc
%defattr(-,root,root)
%doc BUGS NEWS README


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.5
- spec cleanups
- remove locales

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.5
- 4.1.5
- don't build the html version of the info pages
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-2avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.1.4-1avx
- 4.1.4
- spec cleanups

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.7-4avx
- require info-install rather than /sbin/install-info
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.0.7-3sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 4.0.7-2sls
- OpenSLS build
- use %%make macro
- tidy spec
