%define name	pwdb
%define version	0.62
%define release	1avx

%define majver		0
%define lib_name_orig	%mklibname pwdb
%define lib_name	%{lib_name_orig}%{majver}

Summary:	The password database library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
Source:		pwdb-%{version}.tar.bz2
Patch0:		pwdb-0.62-includes.patch.bz2

BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	gcc

%description
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

%package conf
Summary:	The password database library config
Group:		System/Libraries

%description conf
Configuration package for the libpwdb, the password database library.

%package -n %{lib_name}
Summary:	The password database library
Group:		System/Libraries
Requires:	%{name}-conf
Provides:	pwdb = %{version}-%{release}
Obsoletes:	pwdb

%description -n %{lib_name}
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

%package -n %{lib_name}-devel
Summary:	The pwdb include files and link library
Group:		Development/C
Requires:	%{lib_name} = %version-%release
Provides:	pwdb-devel = %version-%release
Conflicts:	pwdb-devel <= 0.61

%description -n %{lib_name}-devel
The development header / link library for pwdb.

%package -n %{lib_name}-static-devel
Summary:	The pwdb static library
Group:		Development/C
Requires:	%{lib_name}-devel = %version-%release
Provides:	pwdb-static-devel = %version-%release

%description -n %{lib_name}-static-devel
The static development library for pwdb.

%prep
%setup -q
%patch0 -p1 -b .includes

rm default.defs
ln -s defs/redhat.defs default.defs
# checking out of the CVS sometimes preserves the setgid bit on
# directories...
chmod -R g-s .

%build
# this package doesn't compile with ssp enabled
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-stack-protector" %make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/{%{_lib},%{_sysconfdir},%{_includedir}/pwdb}

make	INCLUDED=$RPM_BUILD_ROOT%{_includedir}/pwdb \
	LIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	LDCONFIG=":" \
	install

install -m 644 conf/pwdb.conf $RPM_BUILD_ROOT%{_sysconfdir}/pwdb.conf

ln -sf lib%{name}.so.%{version} $RPM_BUILD_ROOT/%{_lib}/lib%{name}.so.%{majver}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files conf
%defattr(-,root,root)
%doc Copyright doc/pwdb.txt doc/html
%config(noreplace) %_sysconfdir/pwdb.conf

%files -n %{lib_name}
%defattr(-,root,root)
/%{_lib}/libpwdb.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
/%{_lib}/libpwdb.so
%_includedir/pwdb

%files -n %{lib_name}-static-devel
%defattr(-,root,root)
/%{_lib}/libpwdb.a

%changelog
* Fri Sep 24 2004 Vincent Danen <vdanen@annvix.org> 0.62-1avx
- 0.62

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 0.61.2-6avx
- Annvix build
- remove %%build_propolice macro; pass -fno-stack-protector by default

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.61.2-5sls
- minor spec cleanups
- change %%build_opensls to %%build_propolice

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 0.61.2-4sls
- OpenSLS build
- tidy spec
- build without stack protection due to some symbol problems

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.61.2-3mdk
- mklibname

* Tue Apr  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.61.2-2mdk
- Rebuild to handle biarch struct utmp. Though this was not needed
  since pwdb_posix_getlogin() only accesses ut_pid & ut_user fields
  which were not affected. Besides, the struct is smaller on biarch
  systems, thusly not corrupting other stack data. But let's be on
  safe side. In real world, I don't know who used that anyway.

* Mon Aug 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.61.2-1mdk
- 0.61.2
- libification

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.61-7mdk
- Patch0: Add missing includes
- Rpmlint fixes: hardcoded-library-path

* Fri Feb 15 2002 Stefan van der Eijk <stefan@eijk.nu> 0.61-6mdk
- BuildRequires

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 0.61-5mdk
- Use %%_tmppath for BuildRoot
- Requires: %%name = %%version-%%release and not only %%version

* Tue Aug 29 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.61-4mdk
- License is GPL
- /etc/pwdb.conf -> noreplace

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 0.61-3mdk
- add soname

* Thu Apr 13 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.61-2mdk
- Fix bad tag value.
- Added a devel package.

* Mon Mar 20 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.61-1mdk
- 0.61

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix setting the password for passwordless accounts. Patch from Thomas
  Sailer

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies
