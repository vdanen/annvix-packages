#
# spec file for package lsof
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		lsof
%define version		4.77
%define release		%_revrel

%define dname		%{name}_%{version}

Summary:	Lists files open by processes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Free
Group:		Monitoring
URL:		ftp://vic.cc.purdue.edu/pub/tools/unix/lsof/
Source0:	ftp://vic.cc.purdue.edu/pub/tools/unix/%{name}/%{dname}.tar.bz2
Patch0:		lsof_4.64-perl-example-fix.patch
Patch1:		lsof_4.60-has-security.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Lsof's name stands for LiSt Open Files, and it does just that. It lists
information about files that are open by the processes running on a UNIX
system.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -c -n %{dname}

#
# Sort out whether this is the wrapped or linux specific tar ball.
#
[ -d %{dname} ] && cd %{dname}
[ -f %{dname}_src.tar ] && tar xf %{dname}_src.tar
[ -d %{dname}.linux -a ! -d %{dname} ] && \
	mv %{dname}.linux %{dname}
[ -d %{dname}_src ] && cd %{dname}_src
%patch0 -p1
%patch1 -p1


%build
[ -d %{dname}/%{dname}_src ] && cd %{dname}/%{dname}_src

LINUX_BASE=/proc
export LINUX_BASE
./Configure -n linux

%make DEBUG="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d %{dname}/%{dname}_src ] && cd %{dname}/%{dname}_src
mkdir -p %{buildroot}{%{_sbindir},%{_mandir}/man8}
install -s %{name} %{buildroot}%{_sbindir}
install -m 0644 lsof.8 %{buildroot}%{_mandir}/man8/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%attr(0755,root,kmem) %{_sbindir}/%{name}
%{_mandir}/man8/lsof.8*

%files doc
%defattr(644,root,root,755)
%doc %{dname}/00*


%changelog
* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.77
- 4.77
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.74
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.74
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.74-1avx
- 4.74

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.68-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.68-5avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.68-4avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 4.68-3sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.68-2sls
- OpenSLS build
- tidy spec

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.68-1mdk
- new release

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.65-3mdk
- build release

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.65-2mdk
- add url (Yura Gusev)

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.65-1mdk
- new release

* Wed Jul 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.64-1mdk
- new release
- get rid of useless prefix
- various spec cleaning
- rediff patch 0

* Tue Apr 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.60-2mdk
- fix example scripts to call perl in the proper location [Patch0]
- compile with the HASSECURITY option enabled meaning you can only see
  open files for your own processes [Patch1]

* Thu Jan 03 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.60-1mdk
- new release

* Sat Jul 21 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.57-1mdk
- 4.57 out for general consumption.
- s/Copyright/License/;

* Sat May 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.56-1mdk
- 4.56 for general consumption.
- Attempt to build without explicitly defining the kernel version.

* Sat Feb 17 2001 Geoffrey lee <snailtalk@mandrakesoft.com> 4.55-1mdk
- 4.55 out for general consumption.

* Fri Dec 08 2000 Geoffrey Lee <snailtlak@mandrakesoft.com> 4.53-1mdk
- new and shiny source.

* Wed Aug 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.51-1mdk
- new release
- stop manually stripping binaries and compressing man pages :-(

* Wed Aug 23 2000 Lenny Cartier <lenny@mandrakesoft.com> 4.49-2mdk
- Used srpm from Alexander Skwar <ASkwar@DigitalProjects.com> :
	A little bit more macros
	Only use "install" when actually needed, else use mkdir -p or cp

* Mon Apr 17 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 4.49-1mdk
- version 4.49

* Tue Apr 11 2000 Christopher Molnar <molnarc@mandrakesoft.com> 4.45-4mdk
- Updated group

* Wed Apr  5 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 4.45-3mdk
- updated BuildRoot

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Fri Oct  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 4.45.

* Sat Jul  3 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.de>
- 4.44
- remove obsolete kernel 2.2 patch
- handle RPM_OPT_FLAGS
- build for kernel 2.2.10

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Thu Apr 08 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 4.42 (security fix)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- turn off setgid kmem "just in case".

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- buffer overflow patch.
- upgrade to 4.40.

* Wed Dec 30 1998 Jeff Johnson <jbj@redhat.com>
- update to "official" 4.39 release.

* Wed Dec 16 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.39B (linux) with internal kernel src.

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.39A (linux)

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.37

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.36

* Thu Jul 23 1998 Jeff Johnson <jbj@redhat.com>
- upgrade to 4.35.
- rewrap for RH 5.2.

* Mon Jun 29 1998 Maciej Lesniewski <nimir@kis.p.lodz.pl>
  [4.34-1]
- New version
- Spec rewriten to use %%{name} and %%{version} macros
- Removed old log enteries

* Tue Apr 28 1998 Maciej Lesniewski <nimir@kis.p.lodz.pl>
- Built under RH5
- %%install was changed
