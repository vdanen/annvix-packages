%define name	acl
%define version 2.2.13
%define release 4sls

%define lib_name_orig	libacl
%define lib_major	1
%define lib_name	%mklibname acl %{lib_major}

Summary:	Command for manipulating access control lists
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	attr-devel

Requires:	%{lib_name} = %{version}-%{release}

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n %{lib_name}
Summary:	Main library for %{lib_name_orig}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n %{lib_name}
This package contains the l%{lib_name_orig} dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n %{lib_name}-devel
Summary:	Access control list static libraries and headers.
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	acl-devel = %{version}-%{release}
Obsoletes:	acl-devel

%description -n %{lib_name}-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

You should install %{lib_name}-devel if you want to develop programs
which make use of ACLs.  If you install %{lib_name}-devel, you will
also want to install %{lib_name}.

%prep
%setup -q

%build
%configure2_5x --libdir=/%{_lib} --sbindir=/bin
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/

rm -rf %{buildroot}%{_docdir}/acl
%find_lang %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/LICENSE README
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%doc doc/LICENSE
/%{_lib}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc/extensions.txt doc/LICENSE doc/libacl.txt
/%{_lib}/*.so
/%{_lib}/*a
%{_libdir}/*.so
%{_libdir}/*a
%{_mandir}/man[235]/*
%dir %{_includedir}/acl
%{_includedir}/acl/libacl.h
%{_includedir}/sys/acl.h

%changelog
* Mon Feb 09 2004 Vincent Danen <vdanen@opensls.org> 2.2.13-4sls
- more spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.2.13-3sls
- OpenSLS build
- tidy spec

* Fri Aug 29 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.13-2mdk
- /usr/include/acl belongs to acl-devel.

* Fri Aug  8 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.13-1mdk
- 2.2.13

* Tue Aug  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.10-2mdk
- Enforce current practise to BuildRequires: libacl-devel

* Fri Jul 18 2003 Juan Quintela <quintela@mandrakesoft.com> 2.2.10-1mdk
- 2.2.10.

* Wed Jun 18 2003 Juan Quintela <quintela@trasno.org> 2.2.4-1mdk
- mklibname (different way).
- 2.2.4.

* Mon Jun 14 2003 Götz Waschk <waschk@linux-mandrake.com> 2.1.1-2mdk
- configure2_5x macro
- mklibname macro

* Thu Jun 13 2003 Vincent Danen <vdanen@mandrakesoft.com> 2.1.1-1mdk
- 2.1.1

* Fri May 23 2003 Götz Waschk <waschk@linux-mandrake.com> 2.0.11-2mdk
- clean out unpackaged files
- rebuild for devel provides

* Wed Jul 24 2002 Buchan Milne <bgmilne@linux-mandrake.com> 2.0.11-1mdk
- 2.0.11

* Wed Jul 10 2002 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.9-1mdk
- 2.0.9

* Fri Mar 22 2002 David BAUDENS <baudens@mandrakesoft.com> 2.0.0-2mdk
- BuildRequires: libattr1, libattr1-devel
- Requires: %%version-%%release and not only %%version or %%name

* Thu Mar  7 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.0.0-1mdk
- 2.0.0

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.3-1mdk
- 1.1.3.

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.2-2mdk
- Fix provides.

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.2-1mdk
- Rework the .spec.
- Make libs in subpackage.
- 1.1.2.

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.1-1mdk
- First attempt.
