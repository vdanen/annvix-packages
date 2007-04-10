#
# spec file for package procmail
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		procmail
%define	version		3.22
%define	release		%_revrel

Summary:	The procmail mail processing program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL/Artistic
Group:		System/Servers
URL:		http://www.procmail.org
Source0:	ftp://ftp.procmail.org/pub/procmail/%{name}-%{version}.tar.bz2
Patch1:		%{name}-3.22-lockf.patch
Patch2:		%{name}-3.22-pixelpb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Provides:	MailTransportAgent

%description
The procmail program can be used for all local mail delivery.  In
addition to just delivering mail, procmail can be used for automatic
filtering, presorting and other mail handling jobs.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1 -b .lockf
%patch2 -p1 -b .warly

find . -type d -exec chmod 755 {} \;


%build
echo -n -e "\n"|  %make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/{man1,man5}

make BASENAME=%{buildroot}/%{_prefix} install.bin install.man

#move the man pages
mv %{buildroot}/usr/man/man1/* %{buildroot}%{_mandir}/man1/
mv %{buildroot}/usr/man/man5/* %{buildroot}%{_mandir}/man5/

## duplicate in /usr/bin
rm -f examples/mailstat


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(6755,root,mail) %{_bindir}/procmail
%attr(2755,root,mail) %{_bindir}/lockfile
%{_bindir}/formail
%{_bindir}/mailstat
%{_mandir}/man1/*1*
%{_mandir}/man5/*5*

%files doc
%defattr(-,root,root)
%doc FAQ HISTORY README KNOWN_BUGS FEATURES examples


%changelog
* Thu Jun 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.22
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.22
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.22
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix description

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.22-9avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.22-8avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.22-7avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.22-6sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.22-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
