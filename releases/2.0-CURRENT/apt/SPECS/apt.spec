#
# spec file for package apt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apt
%define version		0.5.15lorg3.1
%define release		%_revrel

%define major		0
%define libname		%mklibname %{name} %{major}

Summary:	Debian's Advanced Packaging Tool with RPM support 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://apt-rpm.org/
Source0:	http://apt-rpm.org/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}-apt.conf
Source2:	%{name}-sources.list
Source3:	%{name}-vendors.list
Source4:	%{name}-rpmpriorities
Source5:	%{name}-annvix.conf
Source6:	apt-man.tar.bz2
Patch0:		apt-0.5.15lorg3.1-invalid-lc-messages-dir.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	gettext-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel >= 4.2
BuildRequires:  python-devel
Requires:	gnupg

%description
A port of Debian's apt tools for RPM based distributions.  It provides
the apt-get utility that provides a simpler, safer way to install and
upgrade packages.  APT features complete installation ordering,
multiple source capability and several other unique features. 


%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Requires:	%{name}

%description -n %{libname}
This package contains APT's libapt-pkg package manipulation library
modified for RPM.

%package -n %{libname}-devel
Summary:	Development files for %{name}
Group:		Development/C
Provides:	%{_lib}apt-devel
Provides:	apt-devel
Requires:	%{libname} = %{version}-%{release}

%description -n %{libname}-devel
This package contains the header files and static libraries for
developing with APT's libapt-pkg package manipulation library,
modified for RPM.

%package -n python-%{name}
Summary:	Python extension for %{name}
Group:		Development/Python

%description -n python-%{name}
This package contains a python modules to access to libapt-pkg. 
With it, you can use the apt configuration file, and access to 
the database of packages.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 6
%patch0 -p1 -b .bad_lc

%build
%configure2_5x \
    --disable-docs
pushd po
    cp -f de_DE.po de.po
    cp -f es_ES.po es.po
    cp -f it_IT.po it.po
popd

%make

( cd python; %make )


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}/var/cache/apt/archives/partial
mkdir -p %{buildroot}%{_localstatedir}/apt/lists/partial
mkdir -p %{buildroot}%{_includedir}/apt-pkg
mkdir -p %{buildroot}%{_sysconfdir}/apt/{apt.conf.d,translate.list.d}

mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/apt-pkg

install -m 0644 %{_sourcedir}/%{name}-apt.conf %{buildroot}%{_sysconfdir}/apt
install -m 0644 %{_sourcedir}/%{name}-rpmpriorities %{buildroot}%{_sysconfdir}/apt
install -m 0644 %{_sourcedir}/%{name}-annvix.conf %{buildroot}%{_sysconfdir}/apt/apt.conf.d
install -m 0644 %{_sourcedir}/%{name}-sources.list %{buildroot}%{_sysconfdir}/apt
install -m 0644 %{_sourcedir}/%{name}-vendors.list %{buildroot}%{_sysconfdir}/apt

# (misc) remove this once the librpm package is fixed and do not
# contain reference to /home, no rpmlint warning.
perl -pi -e 's#-L/home/\w+##g' %{buildroot}/%{_libdir}/*.la

%kill_lang %{name}
%find_lang %{name}
%kill_lang libapt-pkg3.3
%find_lang libapt-pkg3.3
cat libapt-pkg3.3.lang >> %{name}.lang
rm -f libapt-pkg3.3.lang

# Python
mkdir -p %{buildroot}/%{py_sitedir}
install -m 0644 python/_apt.so  %{buildroot}/%{py_sitedir}/
install -m 0644 python/apt.py %{buildroot}/%{py_sitedir}/

# our manpages since we will never ship docbook just to compile these manpages
mkdir -p %{buildroot}%{_mandir}/man[58]
install -m 0644 man/*.5 %{buildroot}%{_mandir}/man5/
install -m 0644 man/*.8 %{buildroot}%{_mandir}/man8/

# install lua scripts
mkdir -p %{buildroot}%{_datadir}/apt/scripts
install -m 0600 contrib/gpg-check/gpg-import.lua %{buildroot}%{_datadir}/apt/scripts/


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%attr(0700,root,root) %{_bindir}/apt-cache
%attr(0700,root,root) %{_bindir}/apt-cdrom
%attr(0700,root,root) %{_bindir}/apt-config
%attr(0700,root,root) %{_bindir}/apt-get
%attr(0700,root,root) %{_bindir}/apt-shell
%{_bindir}/countpkglist
%{_bindir}/genbasedir
%{_bindir}/genpkglist
%{_bindir}/gensrclist
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/apt
/var/cache/apt
%{_localstatedir}/%{name}
%dir %{_datadir}/apt
%{_datadir}/apt/scripts
%dir %{_sysconfdir}/apt
%config(noreplace) %{_sysconfdir}/apt/apt.conf 
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%config(noreplace) %{_sysconfdir}/apt/rpmpriorities
%dir %{_sysconfdir}/apt/apt.conf.d
%config(noreplace) %{_sysconfdir}/apt/apt.conf.d/annvix.conf
%dir %{_sysconfdir}/apt/translate.list.d

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/apt-pkg
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la

%files -n python-%{name}
%defattr(-,root,root)
%{py_sitedir}/*

%files doc
%defattr(-,root,root)
%doc COPYING* TODO doc/*.txt doc/examples AUTHORS*


%changelog
* Tue Jul 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.5.15lorg3.1
- set RPM::Order "true" in the default config to use rpm's ordering rather than
  apt's ordering or we run into problems with apt ignoring things like Requires(pre)

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.5.15lorg3.1
- 0.5.15lorg3.1
- don't use the gpg-import lua script anymore; the installer will install the
  appropriate gpg key or the admin should
- cleanup the sources.list example
- use the updated manpages that have been committed upstream for the next version
- rebuild against new python and readline

* Sat May 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.5.15lorg3
- make apt-doc to contain all documentation

* Thu May 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.5.15lorg3
- add the gpg-check lua script and update the configs to use it

* Thu May 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.5.15lorg3
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
