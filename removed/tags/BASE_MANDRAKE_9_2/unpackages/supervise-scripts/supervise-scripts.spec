%define name supervise-scripts
%define version 3.3
%define release 6rph

Name: 		%{name}
Summary:	Utility scripts for use with supervise and svscan.
Version:	%{version}
Release: 	%{release}
Copyright:	GPL
Group:		System/Servers
URL:		http://em.ca/~bruceg/supervise-scripts/
Source:		%{name}-%{version}.tar.bz2
Source1:	supervise.init
Source2:	README.mdk.supervise
Source3:	supervise-data.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch
Requires:	daemontools >= 0.70

%description
A set of scripts for handling programs managed with supervise and svscan.


%package data
Summary:	Collection of supervise-enabled directories
Group:		System/Servers
Requires:	%{name}

%description data
This is a collection of supervise-enabled directories for use with
supervise-scripts and daemontools.  These will allow you to run popular
services that are typically run through xinetd or inetd under tcpserver.  It
includes:  vsftpd, cvspserver, rsync, and proftpd.


%prep
%setup -q
%setup -q -n %{name}-%{version} -D -T -a3

%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}

%install
mkdir -p %{buildroot}{%{_initrddir},/var/service}
make prefix=%{buildroot}%{_prefix} install
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/supervise
cp %{SOURCE2} $RPM_BUILD_DIR/%{name}-%{version}/README.mdk

cd data
PREFIX=%{buildroot} ./install.sh

# move manpages to appropriate location
mkdir -p %{buildroot}%{_mandir}/man1
mv -f %{buildroot}%{_prefix}/man/man1/* %{buildroot}%{_mandir}/man1

%preun
%_preun_service supervise

%post
%_post_service supervise

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

%files
%defattr(-,root,root)
%doc COPYING README NEWS README.mdk
%{_bindir}/*
%{_mandir}/man1/*
%attr(1755,root,root) %dir /var/service
%config %{_initrddir}/supervise

%files data
%defattr(-,root,root)
%dir /var/service/vsftpd
/var/service/vsftpd/run
%dir /var/service/vsftpd/log
/var/service/vsftpd/log/run
%dir /var/service/cvspserver
/var/service/cvspserver/run
%dir /var/service/cvspserver/log
/var/service/cvspserver/log/run
%dir /var/service/rsync
/var/service/rsync/run
%dir /var/service/rsync/log
/var/service/rsync/log/run
%dir /var/service/proftpd
/var/service/proftpd/run
%dir /var/service/proftpd/log
/var/service/proftpd/log/run

%changelog
* Fri Aug  9 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.3-6rph
- build for 9.0

* Wed May 29 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.3-5rph
- grrr... fix stupid problem in initscript
- while we're at it, make the initscript much better anyways

* Wed May 29 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.3-4rph
- add a supervise initscript to run supervise (instead of calling it through
  init)
- add a README.mdk to give instructions
- create supervise-scripts-data sub-package which daemonizes several popular
  services available via xinetd (currently contains vsftpd, cvspserver,
  rsync, and proftpd).

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.3-3rph
- rebuild with rph extension

* Wed Oct 24 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.3-2mdk
- fix dependencies of daemontools from =0.70 to >=0.70

* Fri Feb 23 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.3-1mdk
- 3.3
- include manpages

* Sun Oct 15 2000 Vincent Danen <vdanen@mandrakesoft.com> 2.4-2mdk
- create /var/service and owned by this package

* Sun Oct 15 2000 Vincent Danen <vdanen@mandrakesoft.com> 2.4-1mdk
- first mandrake build
