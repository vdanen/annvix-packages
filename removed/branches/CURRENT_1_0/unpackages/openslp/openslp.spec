%define	name	openslp
%define	version	1.0.11
%define	release	9avx

%define	major		1
%define	libname		%mklibname %{name} %{major}
%define	libname_devel	%mklibname %{name} %{major} -d

Summary:	OpenSLP implementation of Service Location Protocol V2 
Name:		%name
Version:	%version
Release:	%release
License:	BSD-like
Group:		Networking/Other
URL:		http://www.openslp.org/
Source0:	ftp://openslp.org/pub/openslp/%{name}-%{version}/%{name}-%{version}.tar.bz2
Source1:	slpd.run
Source2:	slpd-log.run

BuildRoot:	%{_tmppath}/%{name}-root

PreReq:		rpm-helper
Requires:	%{libname}

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined 
by RFC 2608 and RFC 2614.  This package include the daemon, libraries, header 
files and documentation

%package -n %{libname}
Summary:	OpenSLP implementation of Service Location Protocol V2
Group:		System/Libraries
#Requires:	%name = %version-%release

%description -n %{libname}
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.  This package include the daemon, libraries, header
files and documentation

This package contains the %libname runtime library.

%package -n %{libname_devel}
Summary:	Development tools for programs which will use the %{name} library
Group:		Development/C
Requires:	%{libname} = %version-%release
Provides:	%{name}-devel = %version-%release
Provides:	lib%{name}-devel = %version-%release

%description -n %{libname_devel}
The %{name}-devel package includes the header files and static libraries
necessary for developing programs using the %{name} library.

If you are going to develop programs, you should install %{name}-devel.  
You'll also need to have the %{name} package installed.


%prep
%setup -q
rm -rf `find -name CVS`

%build
%serverbuild
%configure --localstatedir=/var
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
#fix doc
rm -rf installeddoc
mv %buildroot/%_prefix/doc/%{name}-%{version} installeddoc
rm -rf `find installeddoc -name CVS`

mkdir -p %buildroot/%_sysconfdir/sysconfig/daemons 
cat <<EOF  > %buildroot/%_sysconfdir/sysconfig/daemons/slpd
IDENT=slp
DESCRIPTIVE="SLP Service Agent"
ONBOOT="yes"
EOF

mkdir -p %{buildroot}%{_srvdir}/slpd/log
mkdir -p %{buildroot}%{_srvlogdir}/slpd
install -m 0750 %{SOURCE1} %{buildroot}%{_srvdir}/slpd/run
install -m 0750 %{SOURCE2} %{buildroot}%{_srvdir}/slpd/log/run

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_post_srv slpd

%preun 
%_preun_srv slpd

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%Files
%defattr(644,root,root,755)
%doc doc/*
%config(noreplace) %_sysconfdir/slp.conf
%config(noreplace) %_sysconfdir/slp.reg
%config(noreplace) %_sysconfdir/slp.spi
%config(noreplace) %_sysconfdir/sysconfig/daemons/slpd
%defattr(755,root,root,755)
%_sbindir/slpd
%_bindir/slptool
%dir %{_srvdir}/slpd
%dir %{_srvdir}/slpd/log
%{_srvdir}/slpd/run
%{_srvdir}/slpd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/slpd

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING
%_libdir/*.so.*

%files -n %{libname_devel}
%defattr(-,root,root)
%doc ChangeLog COPYING
%_libdir/*a
%_libdir/*.so
%_includedir/*


%changelog
* Mon Sep 20 2004 Vincent Danen <vdanen@annvix.org> 1.0.11-9avx
- update run scripts

* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.org> 1.0.11-8avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.0.11-7sls
- minor spec cleanups

* Wed Feb 04 2004 Vincent Danen <vdanen@opensls.org> 1.0.11-6sls
- remove initscript
- supervise scripts

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.0.11-5sls
- OpenSLS build
- tidy spec

* Tue Jul 15 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.11-4mdk
- Fix log directory

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.11-3mdk
- Rebuild


* Thu Jun 26 2003 Till Kamppeter <till@mandrakesoft.com> 1.0.11-2mdk
- Let the SLP library not require the daemon package, once, the daemon
  can run on a remote machine and second, a program (as CUPS) can be linked
  against libslp, but most users have the SLP functionality turned off. So
  they do not want to get a new daemon pulled in and started by urpmi.
- Added a "Requires:" to tell that openslp needs libslp (one can see this
  necessity by applying "rpm -qR" to openslp.
- Removed "Packager:" tag.

* Wed Jun 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0.11-1mdk
- 1.0.11
- use %%mklibname macro
- rm -rf $RPM_BUILD_ROOT in %%install
- cosmetics
- fix docs and permissions
- macroize

* Fri Jan 10 2003 Yves Duret <yves@zarb.org> 1.0.10-1mdk
- first mandrake version

* Wed Feb 06 2002 alain.richard@equation.fr
	Adapted to enable build under redhat 7.x (uses BuildRoot macro,
	install instead of installtool for non libraries objects,
	protected rm -r for install & clean)

* Wed Jun 13 2001 matt@caldera.com
        Removed server stuff.  We want on binary rpm again
	
* Wed Jul 17 2000 mpeterson@calderasystems.com
        Added lisa stuff
	
* Thu Jul 7 2000 david.mccormack@ottawa.com
	Made it work with the new autoconf/automake scripts.
 
* Wed Apr 27 2000 mpeterson
	started
