%define name	kudzu
%define version	1.1.51
%define release	3sls

Summary:	The Red Hat Linux hardware probing tool.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Applications/System
URL:		http://rhlinux.redhat.com/kudzu/
Source:		kudzu-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-root
BuildPrereq:	pciutils-devel >= 2.1.11-1, python-devel python newt-devel
%ifarch %{ix86}
BuildPrereq:	dietlibc
%endif

Obsoletes:	rhs-hwdiag setconsole
Prereq:		chkconfig, modutils >= 2.3.11-5, /etc/init.d
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

# hack: do not start kudzu on s390/s390x on bootup
%ifarch s390 s390x
perl -pi -e "s/345/-/g" kudzu.init
%endif

%build
ln -s `pwd` kudzu

make RPM_OPT_FLAGS="%{optflags} -I." all kudzu

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install install-program DESTDIR=%{buildroot} libdir=%{buildroot}%{_prefix}/%{_lib}

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
%{_sbindir}/updfstab
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/sysconfig/kudzu
%config %{_initrddir}/kudzu
%config(noreplace) %{_sysconfdir}/updfstab.conf
%config %{_sysconfdir}/updfstab.conf.default
%{_libdir}/python*/site-packages/*

%Files devel
%defattr(-,root,root)
%{_libdir}/libkudzu.a
%{_libdir}/libkudzu_loader.a
%{_includedir}/kudzu

%changelog
* Thu Mar 18 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-3sls
- fix deps for amd64

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-2sls
- Requires: s/newt/libnewt0.51/

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> - 1.1.51-1sls
- first OpenSLS build; from Fedora
