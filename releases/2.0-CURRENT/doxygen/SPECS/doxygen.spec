#
# spec file for package doxygen
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		doxygen
%define version 	1.4.6
%define release 	%_revrel

Summary:	Doxygen is THE documentation system for C/C++
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Development/Other
URL:		http://www.stack.nl/~dimitri/doxygen/
Source:		ftp://ftp.stack.nl/pub/users/dimitri/%{name}-%{version}.src.tar.gz
Patch0:		doxygen-1.2.12-fix-latex.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex
BuildRequires:	gcc-c++

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

perl -pi -e "s|^TMAKE_CFLAGS_RELEASE.*|TMAKE_CFLAGS_RELEASE = $RPM_OPT_FLAGS|" tmake/lib/linux-g++/tmake.conf
%ifarch x86_64 sparc64 ppc64 s390x
perl -pi -e 's/^LIBDIR=.*/LIBDIR=%{_lib}/' configure
perl -pi -e "s|/lib$|/%{_lib}|" tmake/lib/linux-g++/tmake.conf
%endif
find -type d -exec chmod 0755 {} \;


%build
./configure


%make
perl -pi -e 's|^#!perl|#!%{__perl}|' examples/tag/html/installdox


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -s bin/doxy* %{buildroot}%{_bindir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/doxygen
%{_bindir}/doxytag


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.6
- 1.4.6
- drop the README file (boring)
- use the real source file
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.4
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.4-1avx
- 1.4.4
- fix perl path in installdox
- drop P1; fixed upstream
- drop the LICENSE file

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3-8avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3-7avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3-6avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.3-5avx
- Annvix build
- remove BuildReq on XFree86-devel

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 1.3.3-4sls
- remove %%build_opensls macro
- minor spec cleanups
- remove %%builddoc... we're never going to build them

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.3.3-3sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to not build doxywizard (removes qt3-devel dep)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
