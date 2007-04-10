#
# spec file for package ed
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ed
%define version		0.2
%define release		%_revrel

%define _exec_prefix	/

Summary:	The GNU line editor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text Tools
URL:		http://www.gnu.org/software/ed/ed.html 
Source:		ftp://ftp.gnu.org/pub/gnu/ed/ed-0.2.tar.bz2
Patch0:		ed-0.2-security-tempfile.patch
Patch1:		ed-0.2-fixinfo.patch
Patch2:		ed-0.2-li18nux-patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.1

Requires(post):	info-install
Requires(preun): info-install

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it much.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
rm -f ./configure
WANT_AUTOCONF_2_1=1 autoconf
rm -f regex.*
%configure

%make CFLAGS="%{optflags}"


%check
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall mandir=%{buildroot}%{_mandir}/man1/


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,0755)
/bin/ed
/bin/red
%{_infodir}/ed.info*
%{_mandir}/*/*

%files doc
%defattr(-,root,root,0755)
%doc NEWS POSIX README THANKS


%changelog
* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-37avx
- fix requires

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-36avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-35avx
- rebuild for new gcc

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.2-34avx
- bootstrap build
- for the use of autoconf2.1 (peroyvind)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.2-33avx
- Annvix build
- require packages not files

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.2-32sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 0.2-31sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
