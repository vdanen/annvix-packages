#
# spec file for package rssh
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rssh
%define version		2.3.2
%define release		%_revrel

Summary:	Restricted shell for scp or sftp
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Networking/Remote Access
URL:		http://www.pizzashack.org/rssh/
Source0:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssh-clients
BuildRequires:	openssh-server

Requires:	openssh

%description
rssh is a restricted shell for use with ssh, which allows the system
administrator to restrict a user's access to a system via scp or sftp, or
both.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x \
    --with-sftp-server=%{_libdir}/ssh/sftp-server
%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
install -m 0755 -D conf_convert.sh %{buildroot}%_datadir/%{name}/conf_convert.sh


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(755,root,root) %{_bindir}/rssh
%attr(4755,root,root) %{_libexecdir}/rssh_chroot_helper
%dir %_datadir/%{name}
%_datadir/%{name}/conf_convert.sh
%{_mandir}/man*/*

%files doc
%defattr(-,root,root)
%doc AUTHORS ChangeLog CHROOT COPYING README SECURITY TODO


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2
- 2.3.2 (fixes some security issues)
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3-2avx
- forgot to clean the spec

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3-1avx
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
