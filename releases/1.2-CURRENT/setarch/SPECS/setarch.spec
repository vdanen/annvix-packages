#
# spec file for package setarch
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		setarch
%define version		1.8
%define	release		%_revrel

Summary:	Kernel personality setter
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
Source0:	%{name}-%{version}.tar.gz
Patch0:		setarch-1.3-linux64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Provides:	linux32

%description
This utility tells the kernel to report a different architecture than the 
current one, then runs a program in that environment.


%prep
%setup -q
%patch0 -p1 -b .linux64


%build
%{__cc} -o setarch setarch.c %{optflags}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -m 0644 setarch.8 -D %{buildroot}%{_mandir}/man8/setarch.8
install -s -m 0755 setarch -D %{buildroot}%{_bindir}/setarch


LINKS="linux32"
%ifarch s390 s390x
LINKS="$LINKS s390 s390x"
%endif
%ifarch x86_64 i386
LINKS="$LINKS i386 x86_64"
%endif
%ifarch ppc ppc64
LINKS="$LINKS ppc ppc64 ppc32"
%endif
%ifarch sparc sparc64
LINKS="$LINKS sparc sparc64 sparc32"
%endif
%ifarch ia64
LINKS="$LINKS i386 ia64"
%endif
%ifarch x86_64 ppc64 sparc64 ia64
LINKS="$LINKS linux64"
%endif
for I in $LINKS; do 
    ln %{buildroot}%{_bindir}/setarch %{buildroot}%{_bindir}/$I
    echo ".so setarch.8" > %{buildroot}%{_mandir}/man8/$I.8
done


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man8/*.8*


%changelog
* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org>
- 1.8

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-2avx
- rebuild

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-1avx
- first Annvix build

* Thu Feb 17 2005 Per ??yvind Karlsen <peroyvind@linux-mandrake.com> 1.7-1mdk
- sync with fedora

* Wed Dec 22 2004 Per ??yvind Karlsen <peroyvind@linux-mandrake.com> 1.6-1mdk
- 1.6

* Wed Jun 02 2004 Per ??yvind Karlsen <peroyvind@linux-mandrake.com> 1.4-1mdk
- 1.4

* Wed Feb 11 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3-1mdk
- First Mandrake Linux package
