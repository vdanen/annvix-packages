# $Id: srv.spec,v 1.7 2004/07/15 01:33:18 vdanen Exp $

%define name	srv
%define version 0.6
%define release 1avx

Summary:	Tool to manage supervise-controlled services.
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		System/Servers
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/srv/
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
mkdir -p %{buildroot}{/sbin,%{_bindir},%{_sbindir},%{_mandir}/man8}
install -m 0755 srv %{buildroot}%{_sbindir}
install -m 0755 srv-start %{buildroot}/sbin
install -m 0755 srv-stop %{buildroot}/sbin
install -m 0755 srv-addinit %{buildroot}/sbin
install -m 0644 srv.8 %{buildroot}%{_mandir}/man8
install -m 0755 nothing %{buildroot}%{_bindir}

# supervise scripts
pushd supervise-scripts-3.3
make prefix=%{buildroot}%{_prefix} install
popd

# move manpages to appropriate location
mkdir -p %{buildroot}%{_mandir}/man1
mv -f %{buildroot}%{_prefix}/man/man1/* %{buildroot}%{_mandir}/man1

# remove unwanted files and move stuff around
rm -f %{buildroot}%{_bindir}/svscan*
mv %{buildroot}%{_bindir}/svc* %{buildroot}%{_sbindir}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
echo "Adding svscan to inittab if required..."
/sbin/srv-addinit >/dev/null 2>&1

%files
%defattr(-,root,root)
/sbin/srv-addinit
/sbin/srv-start
/sbin/srv-stop
%{_sbindir}/srv
%{_sbindir}/svc-add
%{_sbindir}/svc-isdown
%{_sbindir}/svc-isup
%{_sbindir}/svc-remove
%{_sbindir}/svc-start
%{_sbindir}/svc-status
%{_sbindir}/svc-stop
%{_sbindir}/svc-waitdown
%{_sbindir}/svc-waitup
%{_bindir}/nothing
%{_mandir}/man8/srv.8*
%{_mandir}/man1/svc-add.1*
%{_mandir}/man1/svc-remove.1*
%{_mandir}/man1/svc-start.1*
%{_mandir}/man1/svc-stop.1*

%changelog
* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 0.6-1avx
- numerous fixes; there was some bad bash going on (this solves
  the problem with every service taking 15s to shutdown, they should
  be instant now)
- it is prefered to run svscan from init so that it can be restarted
  should something happen, so the initscript is gone
- don't remove the build directory by default
- move most of the files in %%{_bindir} to %%{_sbindir} because only
  root can really do anything with services

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 0.5-2avx
- Annvix build

* Tue May 11 2004 Vincent Danen <vdanen@opensls.org> 0.5-1sls
- 0.5:
  - nice overall status summary
  - fixed the handling of services that don't come with a log service

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.4-2sls
- fix from Oden to handle restarts better

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
