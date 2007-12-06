#
# spec file for package man-pages
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		man-pages
%define version		2.69
%define release 	%_revrel

Summary:	English man (manual) pages from the Linux Documentation Project
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL-style
Group:		System/Internationalization
URL:		http://www.kernel.org/doc/man-pages
Source0:	ftp://ftp.kernel.org/pub/linux/docs/man-pages/%{name}-%{version}.tar.bz2
Source1:	man-pages-extralocale.tar.bz2
Source2:	man9-19971126.tar.bz2
Source3:	man2.tar.bz2
Source4:	man-network.tar.bz2
Source5:	strptime.3
Patch0:		man-pages-1.44-ext3.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	man => 1.5j-8mdk

Requires:	man => 1.5j-8mdk
Requires:	sed
Requires:	grep
Autoreqprov:	false

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP).  The man pages are organized into the
following sections:

Section 1:  User commands (intro only)
Section 2:  System calls
Section 3:  Libc calls
Section 4:  Devices (e.g., hd, sd)
Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd, nfs)
Section 6:  Games (intro only)
Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
Section 8:  System administration (intro only)
Section 9:  Kernel internal routines


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 1 -a 2 -a 3 -a 4

cp -a %{_sourcedir}/strptime.3 man3

%patch0 -p1


%build
rm -f man1/{diff,chgrp,chmod,chown,cp,dd,df,dircolors,du,install,dir,vdir}.1
rm -f man1/{ln,ls,mkdir,mkfifo,mknod,mv,rm,rmdir,touch}.1
rm -f man2/modules.2 man2/quotactl.2 man2/get_kernel_syms.2 
rm -f man2/{create,delete,init,query}_module.2
rm -f man4/{console,fd}.4 man5/{exports,nfs,fstab}.5

# this one conflicts with bind-utils
rm -rf man5/resolver.5

# those conflict with glibc{,-devel} and ldconfig
rm -f man1/{getent,iconv,locale,localedef,sprof,ldd}.1
rm -f man8/{ldconfig,rpcinfo,ld.so}.8
rm -f man3/crypt.3

# this conflict with glibc
rm -f man1/rpcgen.1.bz2

# this conflicts with shadow-utils
rm -f man3/getspnam.3
				

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

set +x
mkdir -p %{buildroot}%{_mandir}
for n in 0p 1 1p 2 3 3p 4 5 6 7 8 9; do
    mkdir %{buildroot}%{_mandir}/man$n
done
for n in man*/*; do
    cp -a $n %{buildroot}%{_mandir}/$n
done

set -x

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-en.cron << EOF
#!/bin/bash
LANG='' /usr/sbin/makewhatis %{_mandir}/en
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-en.cron

mkdir -p  %{buildroot}/var/cache/man/en
mkdir -p  %{buildroot}{%{_mandir}/en,/var/catman/}

 
%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(0644,root,man,755)
%config(noreplace) %attr(755,root,root)%{_sysconfdir}/cron.weekly/makewhatis-en.cron
%dir %{_mandir}/en
%dir %{_mandir}/man*p/
%{_mandir}/man*/*

%files doc
%defattr(0644,root,man,755)
%doc README* *.Announce POSIX-COPYRIGHT Changes


%changelog
* Wed Dec 05 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.69
- 2.69
- update URL

* Mon Apr 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.44
- 2.44

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.43
- 2.43
- renumber sources and remove manpages that were later being deleted
- spec cleanups

* Thu Oct 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.08
- remove man3/getspnam.3 as it conflicts with shadow-utils

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.08
- add -doc subpackage
- fix requires

* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.08
- 2.08
- fix unowned directories
- drop merged patches P4, P5, P6

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.07
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.07
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.07
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.07-1avx
- 2.07
- include POSIX man pages

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-4avx
- remove crypt.3 manpage (in glibc)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-2avx
- bootstrap build

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.01-1avx
- 2.01
- spec cleanups

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.60-4avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.60-3sls
- minor spec cleanups
- remove icon

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.60-2sls
- OpenSLS build
- tidy spec
- don't generate the whatis database

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
