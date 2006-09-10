#
# spec file for package passwd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		passwd
%define version		0.71
%define release		%_revrel

Summary:	The passwd utility for setting/changing passwords using PAM
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Base
# This url is stupid, someone come up with a better one _please_!
URL:		http://www.freebsd.org
Source0:	passwd-%{version}.tar.bz2
Source1:	passwd.pamd

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glib2-devel
BuildRequires:	libuser-devel
BuildRequires:	pam-devel
BuildRequires:	popt-devel

Requires:	pam >= 0.59
Requires:	pwdb >= 0.58
Requires:	libuser
Requires(pre):	setup >= 2.5-5873avx

%description
The passwd package contains a system utility (passwd) which sets
and/or changes passwords, using PAM (Pluggable Authentication
Modules).


%prep
%setup -q


%build
%configure --without-selinux
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1

%makeinstall_std

install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/passwd
perl -p -i -e 's|use_authtok nullok|use_authtok nullok md5|' %{buildroot}%{_sysconfdir}/pam.d/passwd
rm -f %{buildroot}%{_bindir}/{chfn,chsh}
rm -f %{buildroot}%{_mandir}/man1/{chfn.1,chsh.1}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0640,root,shadow) %config(noreplace) %{_sysconfdir}/pam.d/passwd
%attr(2711,root,shadow) %{_bindir}/passwd
%{_mandir}/man1/passwd.1*

		
%changelog
* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.71
- require new setup (for group shadow)
- spec cleanups

* Sat Jul 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.71
- make passwd sgid shadow
- requires new setup
- S1: provide our own pam config

* Sat Jun 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.71
- 0.71
- rebuild against new pam

* Tue May 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.68
- rebuild against new libuser
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.68
- Clean rebuild

* Mon Jan 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.68
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-11avx
- rebuild against new glib2.0

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-9avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-8avx
- rebuild against new libuser and glib2

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.68-7avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 0.68-6sls
- Requires: libuser, not /etc/libuser.conf

* Mon May 17 2004 Vincent Danen <vdanen@opensls.org> 0.68-5sls
- security fixes from Steve Grubb

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.68-4sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 0.68-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
