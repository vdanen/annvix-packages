%define name	kudzu
%define version	1.1.111
%define release	1avx

Summary:	The Red Hat Linux hardware probing tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Applications/System
URL:		http://fedora.redhat.com/projects/additional-projects/kudzu/
Source:		kudzu-%{version}.tar.gz
Patch0:		kudzu-1.1.95-avx-python2.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildPrereq:	pciutils-devel >= 2.1.11-1, python-devel python newt-devel

Prereq:		chkconfig, modutils >= 2.3.11-5, initscripts
Requires:	pam >= 0.74-17, hwdata, python-base
%ifarch x86_64 amd64
Requires:	lib64newt0.51
%else
Requires:	libnewt0.51
%endif

%description
Kudzu is a hardware probing tool run at system boot time to determine
what hardware has been added or removed from the system.

%package devel
Summary:	Development files needed for hardware probing using kudzu.
Group:		Development/Libraries
Requires:	pciutils-devel

%description devel
The kudzu-devel package contains the libkudzu library, which is used
for hardware probing and configuration.

%prep
%setup -q
%patch0 -p1 -b .python2

# hack: do not start kudzu on s390/s390x on bootup
%ifarch s390 s390x
perl -pi -e "s/345/-/g" kudzu.init
%endif

%build
ln -s `pwd` kudzu

make RPM_OPT_FLAGS="%{optflags} -I." all kudzu

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install install-program DESTDIR=%{buildroot} libdir=%{buildroot}%{_libdir}
install -m 0755 fix-mouse-psaux %{buildroot}%{_sbindir}

%find_lang %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_post_service kudzu

%preun
%_preun_service kudzu

%files -f %{name}.lang
%defattr(-,root,root)
%doc README hwconf-description
%{_sbindir}/kudzu
%{_sbindir}/module_upgrade
%{_sbindir}/fix-mouse-psaux
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/sysconfig/kudzu
%config %{_initrddir}/kudzu
%{_libdir}/python*/site-packages/*

%Files devel
%defattr(-,root,root)
%{_libdir}/libkudzu.a
%{_libdir}/libkudzu_loader.a
%{_includedir}/kudzu

%changelog
* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> - 1.1.95-1avx
- 1.1.111
- don't build with dietlibc anymore

* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> - 1.1.95-1avx
- 1.1.95
- update url
- P1: we don't rename python to python2 so fix Makefile

* Wed Jun 22 2004 Vincent Danen <vdanen@annvix.org> - 1.1.51-4avx
- require packages not files
- Annvix build

* Thu Mar 18 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-3sls
- fix deps for amd64

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-2sls
- Requires: s/newt/libnewt0.51/

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-1sls
- first OpenSLS build; from Fedora
