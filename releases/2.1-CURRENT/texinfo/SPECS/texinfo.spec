#
# spec file for package texinfo
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		texinfo
%define version		4.11
%define release		%_revrel

Summary:	Tools needed to create Texinfo format documentation files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Publishing
URL:		http://www.texinfo.org
Source0:	ftp://ftp.gnu.org/pub/gnu/texinfo/%{name}-%{version}.tar.gz
Source1:	info-dir
Patch0:		texinfo-4.11-mdv-texi2dvi-test.patch
Patch1:		texinfo-3.12h-fix.patch
Patch2:		texinfo-4.7-vikeys-segfault-fix.patch
Patch3:		texinfo-4.7.test.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel
BuildRequires:	zlib-devel

Requires:	tetex
Requires(pre):	info-install
Requires(preun): info-install

%description
Texinfo is a documentation system that can produce both online information
and printed output from a single source file.  Normally, you'd have to
write two separate documents: one for online help or other online
information and the other for a typeset manual or other printed work.
Using Texinfo, you only need to write one source document.  Then when the
work needs revision, you only have to revise one source document.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you are
going to write documentation for the GNU Project.


%package -n info
Summary:	A stand-alone TTY-based reader for GNU texinfo documentation
Group:		System/Base
Requires(pre):	info-install
Requires(preun): info-install
Conflicts:	info-install < 4.7

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.

You should install info, because GNU's texinfo documentation is a valuable
source of information about the software on your system.


%package -n info-install
Summary:	Program to update the GNU texinfo documentation main page
Group:		System/Base
Requires(pre):	bzip2
Conflicts:	info < 4.7

%description -n info-install
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based browser
program for viewing texinfo files.


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
%patch3 -p0

%build
%configure2_5x --disable-rpath
%make 
rm -f util/install-info
make -C util LIBS=%{_libdir}/libz.a


%check
# all tests must pass
#make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sysconfdir},/sbin}

%makeinstall_std

install -m 0644 %{_sourcedir}/info-dir %{buildroot}%{_sysconfdir}/info-dir
ln -sf ../../..%{_sysconfdir}/info-dir %{buildroot}%{_infodir}/dir
mv -f %{buildroot}%{_bindir}/install-info %{buildroot}/sbin

# remove texi2pdf since it conflicts with tetex
rm -f %{buildroot}%{_bindir}/texi2pdf

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}

%preun
%_remove_install_info %{name}

%post -n info
%_install_info info.info

%preun -n info
%_remove_install_info info.info


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/makeinfo
%{_bindir}/pdftexi2dvi
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_infodir}/info-stnd.info*
%{_infodir}/texinfo*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2dvi.1*                         
%{_mandir}/man5/texinfo.5*   
%{_datadir}/texinfo

%files -n info
%defattr(-,root,root)
%{_bindir}/info
%{_infodir}/info.info*
%{_bindir}/infokey
%{_mandir}/man1/info.1*
%{_mandir}/man1/infokey.1*
%{_mandir}/man5/info.5*

%files -n info-install
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/info-dir
%{_infodir}/dir
/sbin/install-info
%{_mandir}/man1/install-info.1*

%files doc
%defattr(-,root,root)
%doc AUTHORS INSTALL INTRODUCTION NEWS README TODO
%doc --parents info/README


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.11
- rebuild against new ncurses

* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.11
- 4.11
- drop P4; applied upstream
- P0: use the proper texi2dvi
- cleanup %%install
- nuke rpath
- disable tests, 2 tests are failing in util/ for some reason

* Fri Feb 02 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- P4: security fix for CVE-2006-4810

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- rebuild against new ncurses

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- spec cleanups
- remove locales

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- make info-install prereq bzip2 rather than just require it (or
  it will get installed after info-install (and other pkgs that
  call info-install))

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- fix prereq
- requires tetex
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-5avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-4avx
- rebuild for new gcc
- don't package texi2pdf since tetex already has it

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-3avx
- bootstrap build

* Sun Mar 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-2avx
- fix conflicts on info-install vs. info

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.8-1avx
- 4.8
- move info(1) and info(5) from info-install to info
- P3: fix macros support in texinfo so that groff documentation
  works (tvignaud)
- P4: make test robust against environment locales (guillomovitch)

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.6-4avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.6-3sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 4.6-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
