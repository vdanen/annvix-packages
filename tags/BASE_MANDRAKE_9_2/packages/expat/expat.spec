%define name   expat
%define version 1.95.6
%define release 4mdk
%define libname_orig libexpat
%define major 0
%define libname %mklibname %{name} %{major}

Summary:	Expat is an XML parser written in C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MPL or GPL
Group:		Development/Other
URL:		http://www.jclark.com/xml/expat.html
Source:		ftp://ftp.jclark.com/pub/xml/%{name}-%{version}.tar.bz2
Patch:		expat-1.95.6-enum.patch.bz2
Requires:   %{libname} = %{version}-%{release}
BuildRoot:	%_tmppath/%name-%version-%release-root

%description
Expat is an XML 1.0 parser written in C by James Clark.  It aims to be
fully conforming. It is currently not a validating XML parser.

%package -n %{libname}
Summary: Main library for expat
Group: Development/C
Obsoletes: libexpat1_95
Provides: libexpat1_95 = %version-%release

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with expat.

%package -n %{libname}-devel
Summary:	Development environment for the expat XML parser
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:       %{libname_orig}-devel = %{version}-%{release} %{name}-devel = %{version}-%{release}
Obsoletes:      %{name}-devel
Obsoletes:      libexpat1_95-devel
Provides:       libexpat1_95-devel = %version-%release

%description -n %{libname}-devel
Development environment for the expat XML parser

%prep
%setup -q -n %name-%{version}
%patch -p1

%build
%configure
# fredl: parallel make is broken
%make
 
%install
%makeinstall mandir=$RPM_BUILD_ROOT/%{_mandir}/man1

install -D -m 0644 doc/reference.html %buildroot%_docdir/%name-%version/reference.html

rm -f $RPM_BUILD_ROOT/%{_mandir}/xmlwf.1*

%clean
rm -rf %buildroot

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%_bindir/xmlwf
%_mandir/man*/*

%files -n %{libname}
%defattr(-,root,root)
%_libdir/libexpat.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%defattr(-,root,root)
%_libdir/libexpat.so
%_includedir/expat.h
%_libdir/libexpat.a
%doc %_docdir/%{name}-%{version}
%_libdir/libexpat.la

%changelog
* Wed Jul  9 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.95.6-4mdk
- Rebuild for new deps

* Mon Jun  2 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.95.6-3mdk
- patch to fix XML_Status enum in expat.h (fix Sablotron build)

* Wed May 14 2003 Stefan van der Eijk <stefan@eijk.nu> 1.95.6-2mdk
- rebuild

* Sat Apr 26 2003 Stefan van der Eijk <stefan@eijk.nu> 1.95.6-1mdk
- 1.95.6

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.95.5-1mdk
- 1.95.5
- use %%mklibname

* Wed Jun 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.95.2-4mdk
- libtoolize to get updated config.guess, rebuild with gcc3.1

* Wed May  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.95.2-3mdk
- corrected libification
- link xmlwf dynamically

  * Wed May 1 2002 Vaclav Slavik <vaclav.slavik@matfyz.cz> 1.95.2-3mdk
- correctly install documentation
- move .la file to libexpat-devel

* Thu Feb 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.95.2-2mdk
- parallel make is broken

* Mon Jul 30 2001 Daouda LO <daouda@mandrakesoft.com> 1.95.2-1mdk
- release 1.95.2
- libification.

* Sat Jun 23 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.95.1-4mdk
- remove trailing "/" from install path, to fix build

* Thu Feb 15 2001  Daouda Lo <daouda@mandrakesoft.com> 1.95.1-3mdk
- real version is 1.95.1 
- reenable optimisations 

* Thu Feb 15 2001  Daouda Lo <daouda@mandrakesoft.com> 1.95-1mdk
- release .

* Sun Jan 07 2001 David BAUDENS <baudens@mandrakesoft.com> 1.1-2mdk
- Don't try to use optimizations
- Bzip2 sources

* Mon Nov 20 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.1-1mdk
- first version
