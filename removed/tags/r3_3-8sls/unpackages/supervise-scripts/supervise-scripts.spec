%define name	supervise-scripts
%define version 3.3
%define release 8sls

Summary:	Utility scripts for use with supervise and svscan.
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Servers
URL:		http://em.ca/~bruceg/supervise-scripts/
Source:		%{name}-%{version}.tar.bz2
Source1:	supervise.init

BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch

Requires:	daemontools >= 0.70

%description
A set of scripts for handling programs managed with supervise and svscan.


%prep
%setup -q


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}


%install
mkdir -p %{buildroot}%{_initrddir}
make prefix=%{buildroot}%{_prefix} install
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/supervise

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
%doc COPYING README NEWS
%{_bindir}/*
%{_mandir}/man1/*
%config %{_initrddir}/supervise


%changelog
* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 3.3-8sls
- don't own /var/service
- no more -data package as each service will go with the owning package
- remove README.mdk

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 3.3-7sls
- OpenSLS build
- tidy spec

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
