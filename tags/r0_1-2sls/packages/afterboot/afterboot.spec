%define name	afterboot
%define version 0.1
%define release 2sls

Summary:	Dynamic afterboot manpage
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Base
URL:		http://opensls.org/cgi-bin/viewcvs.cgi/tools/afterboot/
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch

Requires:	man
PreReq:		rpm-helper

%description
A tool to create the dynamic 'afterboot' manpage.


%prep
%setup -q


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%install
mkdir -p %{buildroot}{%{_datadir}/afterboot,%{_mandir}/man8}
install -m 0644 00_afterboot %{buildroot}%{_datadir}/afterboot
install -m 0644 99_afterboot %{buildroot}%{_datadir}/afterboot
install -m 0700 mkafterboot %{buildroot}%{_datadir}/afterboot
touch %{buildroot}%{_mandir}/man8/afterboot.8.bz2


%post
%_mkafterboot

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(-,root,root)
%dir %attr(0700,root,root) %{_datadir}/afterboot
%{_datadir}/afterboot/*
%ghost %attr(0644,root,root) %{_mandir}/man8/afterboot.8.bz2


%changelog
* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 0.1-2sls
- use %%_mkafterboot macro

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 0.1-1sls
- 0.1
