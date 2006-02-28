#
# spec file for package sash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sash
%define version		3.7
%define release 	%_revrel

Summary:	A statically linked shell, including some built-in basic commands
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Shells
URL:		http://www.canb.auug.org.au/~dbell/
Source0:	http://www.canb.auug.org.au/~dbell/programs/%{name}-%{version}.tar.bz2
Patch0:		sash-3.5-optflags.patch
Patch2: 	sash-3.4-losetup.patch
Patch3: 	sash-3.4-fix-loop__remove_it_when_kernel_headers_are_fixed.patch
Patch4:		sash-3.7-linux2.6-buildfix.patch
Patch5:		sash-3.6-scriptarg.patch
Patch6:		sash-pwdfunc.patch
Patch7:		sash-3.7-segfault.patch
Patch8:		sash-3.7-special-script-call-esp-for-glibc-post.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	zlib-devel glibc-static-devel e2fsprogs-devel

%description
Sash is a simple, standalone, statically linked shell which includes
simplified versions of built-in commands like ls, dd and gzip.  Sash
is statically linked so that it can work without shared libraries, so
it is particularly useful for recovering from certain types of system
failures.  Sash can also be used to safely upgrade to new versions of
shared libraries.


%prep
%setup -q
%patch0 -p1 -b .misc
%patch2 -p1 -b .losetup
%patch3 -p1
%patch4 -p1 -b .linux26
%patch5 -p1 -b .scriptarg
%patch6 -p1 -b .pwd
%patch7 -p1 -b .segf
%patch8 -p1 -b .scriptarg -z .pix


%build
make RPM_OPT_FLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{/sbin,%{_mandir}/man8}

install -s -m 0755 sash %{buildroot}/sbin
install -m 0644 sash.1 %{buildroot}%{_mandir}/man8/sash.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/sash
%{_mandir}/*/*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7-2avx
- rebuild against new e2fsprogs-devel

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.7-1avx
- 3.7
- P4: fix build with linux 2.6 (peroyvind)
- sync with Fedora (P5, P6, P7) (peroyvind)
- P8: P5 broke --ignore-remaining args special option (pixel)
- remove grep prereq

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5-11avx
- rebuild against new gcc

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.5-10avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.5-9avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.5-8sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 3.5-7sls
- OpenSLS build
- tidy spec

* Mon May  5 2003 Pixel <pixel@mandrakesoft.com> 3.5-6mdk
- add "BuildRequires: glibc-static-devel"

* Mon Jan 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.5-5mdk
- remove rpm-helper usage for drakx

* Tue Nov 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.5-4mdk
- Prereq:  grep, rpm-helper >= 0.7
- use new shell helpers

* Tue Aug 20 2002 Pixel <pixel@mandrakesoft.com> 3.5-3mdk
- make rpmlint happy

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.5-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Wed Mar 20 2002 Pixel <pixel@mandrakesoft.com> 3.5-1mdk
- new release

* Sat Feb  2 2002 Pixel <pixel@mandrakesoft.com> 3.4-10mdk
- add Url

* Thu Sep  6 2001 Pixel <pixel@mandrakesoft.com> 3.4-9mdk
- rebuild

* Wed Jun 27 2001 Stefan van der Eijk <stefan@eijk.nu> 3.4-8mdk
- BuildRequires:	zlib-devel

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 3.4-7mdk
- Use %%{_buildroot} for BuildRoot

* Thu Nov 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.4-6mdk
- ignore extra command line arguments.

* Thu Nov  2 2000 Pixel <pixel@mandrakesoft.com> 3.4-5mdk
- fix build (fix-loop__remove_it_when_kernel_headers_are_fixed)

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 3.4-4mdk
- cleanup, BM, macroization

* Sat Mar 25 2000 Pixel <pixel@mandrakesoft.com> 3.4-3mdk
- new group

* Mon Mar 13 2000 Pixel <pixel@mandrakesoft.com> 3.4-2mdk
- new version

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- rebuild against new glibc in the sparc tree

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 3.3 (#4301).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build
