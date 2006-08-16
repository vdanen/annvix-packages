#
# spec file for package gawk
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gawk
%define version		3.1.4
%define release		%_revrel

Summary:	The GNU version of the awk text processing utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text Tools
URL:		http://www.gnu.org/software/gawk/gawk.html
Source0:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.bz2
Source1:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}-ps.tar.bz2
Patch0:		gawk-3.1.3-getpgrp_void.patch
Patch1:		gawk-3.1.4-dfacache.patch
Patch2:		gawk-3.1.4-flonum.patch
Patch3:		gawk-3.1.4-nextc.patch
Patch4:		gawk-3.1.4-uplow.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	byacc

Provides:	awk
Requires(post):	info-install
Requires(preun): info-install

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -b 1
%patch0 -p1 -b .getpgrp_void
%patch1 -p1 -b .dfacache
%patch2 -p1 -b .flonum
%patch3 -p1 -b .nextc
%patch4 -p1 -b .uplow


%build
%configure
%make


%check
# all tests must pass
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall bindir=%{buildroot}/bin

%kill_lang %{name}
%find_lang %{name}

rm -f %{buildroot}%{_infodir}/dir

mkdir -p %{buildroot}{%{_bindir},%{_datadir}/awk,%{_mandir}/man1}

pushd %{buildroot}%{_datadir}
    for  i in *.awk;do
        mv -f $i awk
    done
popd

pushd %{buildroot}%{_mandir}
    for i in *;do
        mv -f $i man1 || true
    done
    pushd man1
       ln -sf gawk.1.bz2 awk.1.bz2
    popd
popd

pushd %{buildroot}%{_bindir}
    ln -sf ../../bin/awk %{buildroot}%{_bindir}/awk 
    ln -sf ../../bin/gawk %{buildroot}%{_bindir}/gawk 
    mv %{buildroot}/bin/pgawk %{buildroot}%{_bindir}
    rm -f %{buildroot}/bin/pgawk-%{version}
popd


%post
%_install_info gawk.info

%preun
%_remove_install_info gawk.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
%{_libdir}/*
%{_datadir}/awk

%files doc
%defattr(-,root,root)
%doc README COPYING FUTURES LIMITATIONS NEWS


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2
- spec cleanups
- remove locales

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2
- add -doc subpackage
- rebuild with gcc4
- move the make test to %%check

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-8avx
- 3.1.4
- sync patches with mandrake 3.1.4-1mdk (which in turn synced with Fedora)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-8avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-7avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-6avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.1.2-5avx
- require packages not files
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 3.1.2-4sls
- minor spec cleanups
- remove %%prefix
- remove the doc package

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 3.1.2-3sls
- OpenSLS build
- tidy spec
