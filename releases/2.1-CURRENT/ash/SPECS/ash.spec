#
# spec file for package ash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ash
%define version		0.3.8
%define release		%_revrel

# shouldn't required, but define it regardless
%define %_ssp_cflags	%nil

Summary:	The Almquist shell
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Shells

Source:		%{name}-%{version}.tar.gz
Patch0:		ash-0.3.8-gcc.patch
Patch1:		ash-0.3.8-defpath.patch
Patch2:		ash-0.3.8-dietlibc.patch
Patch3:		ash-0.3.8-stat.patch
Patch4:		ash-0.3.8-fixyaccparser.patch
Patch5:		ash-0.3.8-getcwd.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	binutils
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	byacc
BuildRequires:	dietlibc-devel

Requires(post):	setup
Provides:	ash-static = %{version}-%{release}

%description
The Almquist shell is a clone of Berkeley's Bourne shell. Ash
supports all of the standard sh shell commands and is considerably
smaller than bash. The ash shell lacks some features (for example,
command-line history), but needs a lot less memory.

This package contains a small, statically linked version of ash 
that can be handy for system recovery or as a fail-safe interactive
shell for the superuser.


%prep
%setup -q
%patch0 -p1 -b .gcc
%patch1 -p1 -b .defpath
%patch2 -p1 -b .dietlibc
%ifarch s390 alpha
%patch3 -p1 -b .stat
%endif
%patch4 -p1 -b .fixyaccparser
%patch5 -p1 -b .getcwd


%build
%ifarch x86_64
perl -pi -e 's|diet gcc|diet x86_64-annvix-linux-gnu-gcc|g' Makefile
%endif

make STATIC=-static


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -D -m 0755 sh %{buildroot}/sbin/bsh
install -D -m 0644 sh.1 %{buildroot}%{_mandir}/man1/ash.1

mkdir %{buildroot}/bin
ln -s /sbin/bsh %{buildroot}/bin/ash
ln -s /sbin/bsh %{buildroot}/bin/bsh
ln -s ash.1 %{buildroot}%{_mandir}/man1/bsh.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -p /bin/ash
# Add /etc/shells entry without using external commands
SHELLS=%{_sysconfdir}/shells
for sh in /bin/ash /bin/bsh; do
    while read i; do [ "$i" = "$sh" ] && break; done < $SHELLS
    [ "$i" = "$sh" ] || echo $sh >> $SHELLS
done


%preun -p /bin/ash
# Remove /etc/shells entry without using external commands
if [ "$1" = "0" ]; then
    SHELLS=%{_sysconfdir}/shells
    TEMP=${SHELLS}-
    for sh in /bin/ash /bin/bsh; do
        while read i; do echo $i; done < $SHELLS > $TEMP
        while read i; do
            [ "$i" = "$sh" ] || echo $i
        done < $TEMP > $SHELLS
    done
fi


%files
%defattr(-,root,root)
/sbin/bsh
/bin/ash
/bin/bsh
%{_mandir}/man1/ash.1*
%{_mandir}/man1/bsh.1*


%changelog
* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8
- rebuild with new binutils

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8
- fix requires
- versioned provides

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8
- dietlibc fixes

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8
- Clean rebuild

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8-3avx
- rebuild against new dietlibc

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8-2avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.3.8-1avx
- first Annvix build
- make it always build with dietlibc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
