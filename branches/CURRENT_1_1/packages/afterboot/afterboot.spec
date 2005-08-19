#
# spec file for package afterboot
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: afterboot.spec,v 1.3 2004/07/15 04:05:34 vdanen Exp $


%define name		afterboot
%define version 	0.2
%define release 	4avx

Summary:	Dynamic afterboot manpage
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Base
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/afterboot/
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	man
PreReq:		rpm-helper

%description
A tool to create the dynamic 'afterboot' manpage.


%prep
%setup -q


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_datadir}/afterboot,%{_mandir}/man8}
install -m 0644 00_afterboot %{buildroot}%{_datadir}/afterboot
install -m 0644 99_afterboot %{buildroot}%{_datadir}/afterboot
install -m 0700 mkafterboot %{buildroot}%{_datadir}/afterboot
touch %{buildroot}%{_mandir}/man8/afterboot.8.bz2


%post
%_mkafterboot


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %attr(0700,root,root) %{_datadir}/afterboot
%{_datadir}/afterboot/*
%ghost %attr(0644,root,root) %{_mandir}/man8/afterboot.8.bz2


%changelog
* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 0.2-4avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.2-3avx
- bootstrap build

* Sat Oct 09 2004 Vincent Danen <vdanen@opensls.org> 0.2-2avx
- update a few things: s/supervise/runsv/ and s/setuidgid/chpst/

* Wed Jul 14 2004 Vincent Danen <vdanen@opensls.org> 0.2-1avx
- s/OpenSLS/Annvix in lots of places

* Fri Jun 18 2004 Vincent Danen <vdanen@opensls.org> 0.1-4avx
- Annvix build

* Mon Feb 09 2004 Vincent Danen <vdanen@opensls.org> 0.1-3sls
- some spec cleanups

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 0.1-2sls
- use %%_mkafterboot macro

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 0.1-1sls
- 0.1
