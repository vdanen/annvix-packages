%define	name	libprelude
%define	version	0.8.5
%define	release 2mdk
%define	major	0
%define libname	%mklibname prelude %{major}

%define _localstatedir /var

Summary:	Prelude Hybrid Intrusion Detection System Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.prelude-ids.org/
License:	GPL
Source0:	%{name}-%{version}.tar.bz2
Patch0:		libprelude-0.8.5-ltdl_fix.diff.bz2
BuildRequires:  openssl-devel
BuildRequires:  libltdl-devel
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The Prelude Library is a collection of generic functions providing
communication between the Prelude Hybrid IDS suite components. It
provides a convenient interface for sending alerts to Prelude
Manager with transparent SSL, failover and replication support,
asynchronous events and timer interfaces, an abstracted
configuration API (hooking at the commandline, the configuration
line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite
security program into a Prelude sensor.

%package -n	%{libname}
Summary:	Prelude Hybrid Intrusion Detection System Library
Group:          System/Libraries
Provides: %{name}
Provides: %{name} = %{version}

%description -n	%{libname}
The Prelude Library is a collection of generic functions providing
communication between the Prelude Hybrid IDS suite components. It
provides a convenient interface for sending alerts to Prelude
Manager with transparent SSL, failover and replication support,
asynchronous events and timer interfaces, an abstracted
configuration API (hooking at the commandline, the configuration
line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite
security program into a Prelude sensor.

%package -n	prelude-tools
Summary:	The interface for %{libname}
Group:          Networking/Other
Requires:	%{libname} = %{version}

%description -n	prelude-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%package -n	%{libname}-devel
Summary:	Libraries, includes, etc. to develop Prelude IDS sensors
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	openssl-devel
Requires:	libltdl-devel
Provides:	%{name}-devel

%description -n	%{libname}-devel
Libraries, include files, etc you can use to develop Prelude IDS
sensors using the Prelude Library. The Prelude Library is a
collection of generic functions providing communication between
the Prelude Hybrid IDS suite componentst It provides a convenient
interface for sending alerts to Prelude Manager with transparent
SSL, failover and replication support, asynchronous events and
timer interfaces, an abstracted configuration API (hooking at the
commandline, the configuration line, or wide configuration,
available from the Manager), and a generic plugin API. It allows
you to easily turn your favorite security program into a Prelude
sensor.

%prep

%setup -q
%patch0 -p1

%build
# this is ugly, but it works...
export INCLTDL="-I%{_includedir}"
export LIBLTDL="%{_libdir}/libltdl.la"
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal; autoconf; automake

%configure2_5x \
    --enable-static \
    --enable-shared \
    --disable-ltdl-convenience \
    --disable-ltdl-install \
    --includedir=%{_includedir}/%{name} \
    --with-html-dir=%{_datadir}/doc/%{name}-devel-%{version}
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

mv %{buildroot}/%{_prefix}/%{name}/include/*  %{buildroot}/%{_includedir}/%{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_libdir}/lib*.so.*

%files -n prelude-tools
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_bindir}/sensor-adduser
%config(noreplace) %{_sysconfdir}/prelude-sensors/*
%dir /var/spool/prelude-sensors

%files -n %{libname}-devel
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}-devel-%{version}
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_includedir}/%{name}

%changelog
* Tue Sep 09 2003 Florin Grad <florin@mandrakesoft.com> 0.8.5-2mdk
- rename the include dir

* Sun Sep 07 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.5-1mdk
- initial cooker contrib, used parts from the spec file by Sylvain GIL 
