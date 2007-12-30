#
# spec file for package mailx
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mailx
%define version		8.1.1
%define release		%_revrel

Summary:	The /bin/mail program, which is used to send mail via shell scripts
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Networking/Mail
Source:		ftp://ftp.debian.org/pub/debian/hamm/source/mail/mailx-8.1.1.tar.bz2
# not strictly debian patch, i modified it --Geoff
Patch0:		mailx-8.1.1.debian.patch
Patch1:		mailx-8.1.1.security.patch
Patch2:		mailx-8.1.1.nolock.patch
Patch3:		mailx-8.1.1.debian2.patch
Patch4:		mailx-noroot.patch
Patch6:		mailx-8.1.1-version.patch
Patch7:		mailx-8.1.1-forbid-shellescape-in-interactive-and-setuid.patch
Patch8:		mailx-8.1.1-help-files.patch
Patch9:		mailx-8.1.1-makefile-create-dirs.patch
Patch10:	mailx-8.1.1-includes.patch 
Patch11:	mailx-8.1.1-fseek.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	smtpdaemon

%description
The mailx package installs the /bin/mail program, which is used to send
quick email messages (i.e., without opening up a full-featured mail user
agent). Mail is often used in shell scripts.


%prep
%setup -q
%patch0 -p1 -b .debian
%patch1 -p1 -b .security
%patch2 -p1 -b .nolock
%patch3 -p1 -b .debian2
%patch4 -p1 -b .noroot
#%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1 -b .help-files
%patch9 -p1 -b .makefile-create-dirs
%patch10 -p1 -b .includes
%patch11 -p1 -b .fseek


%build
# We can't compile mailx with Optimisation

CFLAGS=$(echo %{optflags}|sed 's/-O.//g')
make CFLAGS="$CFLAGS -D_GNU_SOURCE"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_bindir}
ln -sf ../../bin/mail %{buildroot}%{_bindir}/Mail
ln -sf mail.1 %{buildroot}%{_mandir}/man1/Mail.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0755,root,mail) /bin/mail
%{_bindir}/Mail
%dir %{_datadir}/mailx
%{_datadir}/mailx/mail.help
%{_datadir}/mailx/mail.tildehelp
%config(noreplace) %{_sysconfdir}/mail.rc
%{_mandir}/man1/*


%changelog
* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1
- rebuild

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1-29avx
- requires smtpdaemon

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1-28avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1-27avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 8.1.1-26avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 8.1.1-25sls
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 8.1.1-24sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
