%define name	srv
%define version 0.1
%define release 2sls

Summary:	Tool to manage supervise-controlled services.
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Servers
URL:		http://opensls.org/cgi-bin/viewcvs.cgi/tools/srv/
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch

Requires:	daemontools >= 0.70
Obsoletes:	supervise-scripts
Provides:	supervise-scripts
PreReq:		rpm-helper

%description
A tool to manage supervise-controlled services.


%prep
%setup -q


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}


%install
mkdir -p %{buildroot}{%{_sbindir},%{_mandir}/man8,%{_initrddir}}
install -m 0755 srv %{buildroot}%{_sbindir}
install -m 0755 srv-start %{buildroot}%{_sbindir}
install -m 0755 srv-stop %{buildroot}%{_sbindir}
install -m 0755 srv-addinit %{buildroot}%{_sbindir}
install -m 0755 srv.init %{buildroot}%{_initrddir}/srv
install -m 0644 srv.8 %{buildroot}%{_mandir}/man8


%post
%_post_service srv


%preun
%_preun_service srv

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%files
%defattr(-,root,root)
%{_sbindir}/*
%config(noreplace) %{_initrddir}/srv
%{_mandir}/man8/srv.8*


%changelog
* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 0.1-2sls
- PreReq: rpm-helper
- add %%post and %%preun service stuff

* Fri Jan 02 2004 Vincent Danen <vdanen@opensls.org> 0.1-1sls
- 0.1
