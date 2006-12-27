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
%define version		1.3.5
%define release 	%_revrel

Summary:	The GNU data compression program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.gzip.org/
Source:		ftp://alpha.gnu.org/pub/gnu/gzip/gzip-%{version}.tar.gz
Patch0:		gzip-1.3.5-mdv-znew.patch
Patch1:		gzip-1.2.4a-CAN-2005-1228.patch
Patch2:		gzip-1.3.5-mdv-CAN-2005-0988.patch
Patch3:		gzip-1.3.5-fdr-zgrep-sed.patch
Patch4:		gzip-1.3.5-goo-sec.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires:	mktemp
Requires:	less
Requires(post):	info-install
Requires(preun): info-install

%description
The gzip package contains the popular GNU gzip data compression
program.  Gzipped files have a .gz extension.  


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .znew
%patch1 -p1 -b .can-2005-1228
%patch2 -p1 -b .can-2005-0988
%patch3 -p0 -b .cve-2005-0758
%patch4 -p1 -b .cve-2006-4334_8


%build
export DEFS="-DNO_ASM"
%configure
%make all gzip.info


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_mandir},/bin}

%makeinstall mandir=%{buildroot}%{_mandir}

mv -f %{buildroot}%{_bindir}/gzip %{buildroot}/bin/gzip

rm -f %{buildroot}%{_bindir}/gunzip
rm -f %{buildroot}%{_bindir}/zcat

ln -f %{buildroot}/bin/gzip %{buildroot}/bin/gunzip
ln -f %{buildroot}/bin/gzip %{buildroot}/bin/zcat
ln -sf ../../bin/gzip %{buildroot}%{_bindir}/gzip
ln -sf ../../bin/gunzip %{buildroot}%{_bindir}/gunzip

for i in zcmp zdiff zforce zgrep zmore znew ; do
    sed -e "s|%{buildroot}||g" < %{buildroot}%{_bindir}/$i > %{buildroot}%{_bindir}/.$i
    rm -f %{buildroot}%{_bindir}/$i
    mv %{buildroot}%{_bindir}/.$i %{buildroot}%{_bindir}/$i
    chmod 0755 %{buildroot}%{_bindir}/$i
done

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
%doc NEWS README


%changelog
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
