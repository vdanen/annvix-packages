#
# spec file for package gzip
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gzip
%define version		1.3.12
%define release 	%_revrel

Summary:	The GNU data compression program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.gzip.org/
Source:		ftp://alpha.gnu.org/pub/gnu/gzip/gzip-%{version}.tar.gz
Patch0:		gzip-1.3.12-openbsd-owl-tmp.patch
Patch1:		gzip-1.3.5-zforce.patch
Patch2:		gzip-1.3.9-stderr.patch
Patch3:		gzip-1.3.10-zgreppipe.patch
Patch4:		gzip-1.3.9-rsync.patch
Patch5:		gzip-1.3.3-window-size.patch
Patch6:		gzip-1.3.9-addsuffix.patch
Patch7:		gzip-1.3.5-cve-2006-4335.patch
Patch8:		gzip-1.3.5-cve-2006-4336.patch
Patch9:		gzip-1.3.5-cve-2006-4338.patch
Patch10:	gzip-1.3.9-cve-2006-4337.patch
Patch11:	gzip-1.3.5-cve-2006-4337_len.patch
Patch12:	gzip-1.3.12-futimens.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires:	mktemp
Requires:	less
Requires(post):	info-install
Requires(preun): info-install

%description
The gzip package contains the popular GNU gzip data compression program.
Gzipped files have a .gz extension.  


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .owl-tmp
%patch1 -p1 -b .zforce
%patch2 -p1 -b .stderr
%patch3 -p1 -b .nixi
%patch4 -p1 -b .rsync
%patch5 -p1 -b .window-size
%patch6 -p1 -b .addsuffix
%patch7 -p1 -b .4335
%patch8 -p1 -b .4336
%patch9 -p1 -b .4338
%patch10 -p1 -b .4337
%patch11 -p1 -b .4337l
%patch12 -p1 -b .futimens


%build
export DEFS="-DNO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"

%configure2_5x
%make


%check
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_mandir},/bin}

%makeinstall_std

for i in gzip gunzip zcat; do
    mv -f %{buildroot}%{_bindir}/$i %{buildroot}/bin/$i
    ln -sf ../../bin/$i %{buildroot}%{_bindir}/$i
done

for i in zcmp zdiff zforce zgrep zmore znew ; do
    sed -e "s|%{buildroot}||g" < %{buildroot}%{_bindir}/$i > %{buildroot}%{_bindir}/.$i
    rm -f %{buildroot}%{_bindir}/$i
    mv %{buildroot}%{_bindir}/.$i %{buildroot}%{_bindir}/$i
    chmod 0755 %{buildroot}%{_bindir}/$i
done

# this is part of ncompress
rm -f %{buildroot}%{_bindir}/uncompress

cat > %{buildroot}%{_bindir}/zless <<EOF
#!/bin/sh
export LESSOPEN="|lesspipe.sh %s"
less "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/zless


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*

%files doc 
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog


%changelog
* Thu Nov 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.3.12
- 1.3.12
- dropped all patches (P1, P2, P3: merged upstream)
- added patches from Fedora
- gzip no longer does anything special when called as gunzip or zcat,
  so keep the real binaries
- remove uncompress as it's in the ncompress package
- run make check

* Mon Sep 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.5
- P4: security fix for CVE-2006-433[45678]

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.5
- 1.3.5
- drop P0-P8, P10
- updated P9, P12 from Mandriva (new P0, P2)
- updated P13 from Fedora (new P3)
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a
- fix group

* Mon Jan 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a
- update P13 to have a more comprehensive fix for CVE-2005-0758

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a-21avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a-20avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a-19avx
- bootstrap build

* Wed May 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a-18avx
- P11: security fix for CAN-2005-1228
- P12: security fix for CAN-2005-0988
- P13: security fix for CAN-2005-0758

* Tue Jun 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a-17avx
- P10: fix temp file probs in zdiff (CAN-2004-0970)

* Tue Jun 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a-16avx
- change description

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4a-15avx
- require packages not files
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.2.4a-14sls
- minor spec cleanups

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 1.2.4a-13sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
