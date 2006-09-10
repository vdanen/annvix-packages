#
# spec file for package beecrypt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		beecrypt
%define version		3.1.0
%define release		%_revrel

%define libname		%mklibname %{name} 6
%define libnamedev	%{libname}-devel

%define	with_python_version	2.4%{nil}

Summary:	An open source cryptography library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		http://beecrypt.virtualunlimited.com/
Source0:	http://prdownloads.sourceforge.net/beecrypt/%{name}-3.1.0.tar.bz2
Patch0:		beecrypt-3.1.0-rh.patch
Patch1:		beecrypt-3.1.0-automake1.7.patch
Patch2:		beecrypt-3.1.0-configure.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildPreReq:	doxygen, python-devel >= %{with_python_version}
BuildRequires:	automake1.7

%description
Beecrypt is a general-purpose cryptography library.


%package -n %{libname}
Summary:	An open source cryptography library
Group:		System/Libraries

%description -n %{libname}
Beecrypt is a general-purpose cryptography library.


%package -n %{libnamedev}
Summary:	Files needed for developing applications with beecrypt
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libbeecrypt-devel = %{version}-%{release}

%description -n %{libnamedev}
Beecrypt is a general-purpose cryptography library.  This package contains
files needed for developing applications with beecrypt.


%package python
Summary:	Files needed for python applications using beecrypt.
Group:		Development/C
Requires:	python >= %{with_python_version}
Requires:	%{libname} = %{version}-%{release}

%description python
Beecrypt is a general-purpose cryptography library.  This package contains
files needed for using python with beecrypt.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .rh
%patch1 -p1 -b .automake1.7
%patch2 -p1 -b .configure

./autogen.sh


%build
%configure2_5x \
    --enable-shared \
    --enable-static \
    --with-python \
    CPPFLAGS="-I%{_includedir}/python%{with_python_version}"

%make
doxygen


%check
make check || :
cat /proc/cpuinfo
make bench || :


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# XXX nuke unpackaged files, artifacts from using libtool to produce module
rm -f %{buildroot}%{_libdir}/python%{with_python_version}/site-packages/_bc.*a


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so

%files python
%defattr(-,root,root)
%{_libdir}/python%{with_python_version}/site-packages/_bc.so

%files doc
%defattr(-,root,root)
%doc README BENCHMARKS BUGS docs/html docs/latex


%changelog
* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-6avx
- bootstrap build (new gcc, new glibc)

* Mon Aug 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-5avx
- P2: alpha doesn't use lib64
- minor spec cleanups

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-3avx
- bootstrap build
- always build with python support as we need python-devel to compile
  even without the python package (eh?)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-2avx
- Annvix build

* Fri May 09 2004 Vincent Danen <vdanen@opensls.org> 3.1.0-1sls
- OpenSLS build
- tidy spec

* Wed Feb 18 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.0-2mdk
- automake1.7

* Fri Jan 16 2004 Frederic Lepied <flepied@mandrakesoft.com> 3.1.0-1mdk
- initial Mandrake Linux packaging

* Mon Dec 22 2003 Jeff Johnson <jbj@jbj.org> 3.1.0-1
- upgrade to 3.1.0.
- recompile against python-2.3.3.

* Mon Jun 30 2003 Jeff Johnson <jbj@redhat.com> 3.0.1-0.20030630
- upstream fixes for DSA and ppc64.

* Mon Jun 23 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-2
- upgrade to 3.0.0 final.
- fix for DSA (actually, modulo inverse) sometimes failing.

* Fri Jun 20 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-1.20030619
- avoid asm borkage on ppc64.

* Thu Jun 19 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-1.20030618
- rebuild for release bump.

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-1.20030616
- try to out smart libtool a different way.
- use $bc_target_cpu, not $bc_target_arch, to detect /usr/lib64.

* Mon Jun 16 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-1.20030615
- use -mcpu=powerpc64 on ppc64.

* Fri Jun 13 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-1.20030613
- upgrade to latest snapshot.

* Fri Jun  6 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-1.20030605
- rebuild into another tree.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-0.20030603
- update to 3.0.0 snapshot, fix mpmod (and DSA) on 64b platforms.

* Mon Jun  2 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-0.20030602
- update to 3.0.0 snapshot, merge patches, fix gcd rshift and ppc problems.

* Thu May 29 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-0.20030529
- update to 3.0.0 snapshot, fix ia64/x86_64 build problems.

* Wed May 28 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-0.20030528
- upgrade to 3.0.0 snapshot, adding rpm specific base64.[ch] changes.
- add PYTHONPATH=.. so that "make check" can test the just built _bc.so module.
- grab cpuinfo and run "make bench".
- continue ignoring "make check" failures, LD_LIBRARY_PATH needed for _bc.so.
- skip asm build failure on ia64 for now.
- ignore "make bench" exit codes too, x86_64 has AES segfault.

* Wed May 21 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-0.20030521
- upgrade to 3.0.0 snapshot, including python subpackage.
- ignore "make check" failure for now.

* Fri May 16 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-0.20030516
- upgrade to 3.0.0 snapshot, including ia64 and x86_64 fixes.
- add %%check.
- ignore "make check" failure on ia64 for now.

* Mon May 12 2003 Jeff Johnson <jbj@redhat.com> 3.0.0-0.20030512
- upgrade to 3.0.0 snapshot.
- add doxygen doco.
- use /dev/urandom as default entropy source.
- avoid known broken compilation for now.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Aug  2 2002 Jeff Johnson <jbj@redhat.com> 2.2.0-6
- install types.h (#68999).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun  5 2002 Jeff Johnson <jbj@redhat.com>
- run ldconfig when installing/erasing (#65974).

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Jeff Johnson <jbj@redhat.com>
- upgrade to latest 2.2.0 (from cvs.rpm.org).

* Mon Jan 21 2002 Jeff Johnson <jbj@redhat.com>
- use the same beecrypt-2.2.0 that rpm is using internally.

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.0-1
- initial package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
