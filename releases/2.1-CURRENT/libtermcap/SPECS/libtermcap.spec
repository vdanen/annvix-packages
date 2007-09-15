#
# spec file for package libtermcap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libtermcap
%define version		2.0.8
%define release		%_revrel

%define major		2
%define libname		%mklibname termcap %{major}
%define devname		%mklibname termcap -d

Summary:	A basic system library for accessing the termcap database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		ftp://metalab.unc.edu/pub/Linux/GCC/
Source:		termcap-%{version}.tar.bz2
Patch0:		termcap-2.0.8-shared.patch
Patch1:		termcap-2.0.8-setuid.patch
Patch2:		termcap-2.0.8-instnoroot.patch
Patch3:		termcap-2.0.8-compat21.patch
Patch4:		termcap-2.0.8-xref.patch
Patch5:		termcap-2.0.8-fix-tc.patch
Patch6:		termcap-2.0.8-ignore-p.patch
Patch7:		termcap-buffer.patch
# This patch is a REALLY BAD IDEA without patch #10 below....
Patch8:		termcap-2.0.8-bufsize.patch
Patch9:		termcap-2.0.8-colon.patch
Patch10:	libtermcap-aaargh.patch
# (gc) conflicting definition of `bcopy' against latest glibc 2.1.95
Patch11:	termcap-fix-glibc-2.2.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires:	termcap

%description
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.


%package -n %{libname}
Summary:        Development tools for programs which will access the termcap database
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{name}

%description -n %{libname}
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.


%package -n %{devname}
Summary:	Development tools for programs which will access the termcap database
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	termcap-devel = %{version}-%{release}
Obsoletes:	%mklibname termcap 2 -d

%description -n %{devname}
This package includes the libraries and header files necessary for
developing programs which will access the termcap database.

If you need to develop programs which will access the termcap database,
you'll need to install this package.  You'll also need to install the
libtermcap package.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n termcap-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .nochown
%patch3 -p1 -b .compat21
%patch4 -p1
%patch5 -p1 -b .fix-tc
%patch6 -p1 -b .ignore-p
%patch7 -p1 -b .buffer
%patch8 -p1 -b .bufsize
%patch9 -p1 -b .colon
%patch10 -p1 -b .aaargh
%patch11 -p0


%build
%make CFLAGS="%{optflags} -I."


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_lib}
install -m 0755 libtermcap.so.* %{buildroot}/%{_lib}/
ln -s libtermcap.so.2.0.8 %{buildroot}/%{_lib}/libtermcap.so
ln -s libtermcap.so.2.0.8 %{buildroot}/%{_lib}/libtermcap.so.2

mkdir -p %{buildroot}%{_libdir}
install -m 0644 libtermcap.a %{buildroot}%{_libdir}/
ln -s ../../%{_lib}/libtermcap.so.2.0.8 %{buildroot}%{_libdir}/libtermcap.so

mkdir -p %{buildroot}%{_infodir}
install -m 0644 termcap.info* %{buildroot}%{_infodir}/

mkdir -p %{buildroot}%{_includedir}
install -m 0644 termcap.h %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 termcap.src %{buildroot}%{_sysconfdir}/termcap

rm -f %{buildroot}%{_sysconfdir}/termcap


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{devname}
/sbin/install-info \
    --section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
    --info-dir=%{_infodir} %{_infodir}/termcap.info%{_extension}

%postun -n %{devname}
if [ $1 = 0 ]; then
    /sbin/install-info --delete \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info%{_extension}
fi


%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
/%{_lib}/*.so
%{_infodir}/termcap.info*
%{_libdir}/libtermcap.a
%{_libdir}/libtermcap.so
%_includedir/termcap.h

%files doc
%defattr(-,root,root)
%doc ChangeLog README


%changelog
* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8
- implement devel naming policy
- implement library provides policy

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8
- really add -doc subpackage

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8
- fix requires
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-41avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-40avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-39avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-38avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.0.8-37sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 2.0.8-36sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
