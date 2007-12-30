#
# spec file for package make
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		make
%define version		3.81
%define release		%_revrel
%define epoch		1

Summary:	A GNU tool which simplifies the build process for users
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/directory/GNU/make.html
Source:		ftp://ftp.gnu.org/pub/gnu/make/%{name}-%{version}.tar.bz2
# to remove once those po files are included in standard sources
Source1:	%{name}-pofiles.tar.bz2
Patch0:		make-3.80-no-hires-timestamp.patch
Patch1:		make-3.80-lib64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext-devel

Requires(post):	info-install
Requires(preun): info-install


%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files.  Make
allows users to build and install packages without any significant
knowledge about the details of the build process.  The details about how
the program should be built are provided for make in the program's
makefile.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a1
# WARNING: only configure script is patched
%patch0 -p1 -b .no-hires-timestamp
%patch1 -p1 -b .lib64


%build
%configure2_5x
%make


%check
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

ln -sf make %{buildroot}%{_bindir}/gmake

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info make.info

%preun
%_remove_install_info make.info


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/make
%{_bindir}/gmake
%{_mandir}/man1/make.1*
%{_infodir}/make.info*

%files doc
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS ChangeLog README README.customs SCOPTIONS NEWS
%doc glob/COPYING.LIB glob/ChangeLog


%changelog
* Wed Nov 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.81
- rebuild against new gettext

* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.81
- rebuild

* Sat Dec 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.81
- 3.81
- drop P2; merged upstream
- rebuild against new gettext

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- spec cleanups
- remove locales

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- add -doc subpackage
- rebuild with gcc4
- put the test in %%check

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.80
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-13avx
- P2: fix memory exhausting (mdk bug #14626) (tvignaud)
- P1: linux32 fixes, aka resolve -llib only in */lib when running under
  a 32bit personality and some lib64 fixes (gbeauchesne)
- rebuild against new gettext

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-12avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-11avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.80-10avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.80-9avx
- require packages not files
- Annvix build

* Fri May 09 2004 Vincent Danen <vdanen@opensls.org> 3.80-8sls
- rebuild against new gettext

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 3.80-7sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.80-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
