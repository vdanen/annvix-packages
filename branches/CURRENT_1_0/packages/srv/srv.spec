%define name	srv
%define version 0.4
%define release 1sls

Summary:	Tool to manage supervise-controlled services.
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Servers
URL:		http://opensls.org/cgi-bin/viewcvs.cgi/tools/srv/
Source:		%{name}-%{version}.tar.bz2
Source1:	http://em.ca/~bruceg/supervise-scripts/supervise-scripts-3.3.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root

Requires:	daemontools >= 0.70
Obsoletes:	supervise-scripts
Provides:	supervise-scripts
PreReq:		rpm-helper

%description
A tool to manage supervise-controlled services.


%prep
%setup -q
%setup -q -n %{name}-%{version} -D -T -a1


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}
gcc nothing.c -o nothing

%install
mkdir -p %{buildroot}{%{_bindir},%{_sbindir},%{_mandir}/man8,%{_initrddir}}
install -m 0755 srv %{buildroot}%{_sbindir}
install -m 0755 srv-start %{buildroot}%{_sbindir}
install -m 0755 srv-stop %{buildroot}%{_sbindir}
install -m 0755 srv-addinit %{buildroot}%{_sbindir}
install -m 0755 srv.init %{buildroot}%{_initrddir}/srv
install -m 0644 srv.8 %{buildroot}%{_mandir}/man8
install -m 0755 nothing %{buildroot}%{_bindir}

# supervise scripts

pushd supervise-scripts-3.3
make prefix=%{buildroot}%{_prefix} install
popd

# move manpages to appropriate location
mkdir -p %{buildroot}%{_mandir}/man1
mv -f %{buildroot}%{_prefix}/man/man1/* %{buildroot}%{_mandir}/man1


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
%{_bindir}/*
%config(noreplace) %{_initrddir}/srv
%{_mandir}/man8/srv.8*
%{_mandir}/man1/*

%changelog
* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.4-1sls
- 0.4
- include Bruce's supervise-scripts (3.3)

* Mon Jan 26 2004 Vincent Danen <vdanen@opensls.org> 0.3-2sls
- include nothing

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 0.3-1sls
- 0.3

* Tue Jan 13 2004 Vincent Danen <vdanen@opensls.org> 0.2-1sls
- 0.2

* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 0.1-2sls
- PreReq: rpm-helper
- add %%post and %%preun service stuff

* Fri Jan 02 2004 Vincent Danen <vdanen@opensls.org> 0.1-1sls
- 0.1
