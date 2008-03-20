#
# spec file for package unzip
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		unzip
%define version 	5.52
%define release 	%_revrel
%define src_ver 	552

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		Archiving
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:	ftp://ftp.icce.rug.nl/infozip/src/%{name}%{src_ver}.tar.bz2
Patch1:		unzip542-size-64bit.patch
Patch2:		unzip-5.52-CAN-2005-2475.patch
Patch3:		unzip-5.52-CVE-2005-4667.patch
Patch4:		unzip-5.52-deb-CVE-2008-0888.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.



%prep
%setup -q
%patch1 -p0
%patch2 -p1 -b .can-2005-2475
%patch3 -p1 -b .cve-2005-4667
%patch4 -p0 -b .cve-2008-0888


%build
%ifarch %{ix86}
%make -ef unix/Makefile linux CF="-DLZW_CLEAN %{optflags} -Wall -I. -DASM_CRC" CC=gcc LD=gcc AS=gcc AF="-Di386" CRC32=crc_gcc
%else
%make -ef unix/Makefile linux_noasm CF="-DLZW_CLEAN %{optflags} -Wall -I."
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

ln -sf unzip zipinfo
for i in unzip funzip unzipsfx zipinfo;	do install $i %{buildroot}%{_bindir}; done
install unix/zipgrep %{buildroot}%{_bindir}

for i in man/*.1; do install -m 0644 $i %{buildroot}%{_mandir}/man1/; done

cat > README.IMPORTANT.ANNVIX << EOF
This version of unzip is a stripped-down version which doesn't include
the "unreduce" and "unshrink" algorithms. The first one is subject to
a restrictive copyright by Samuel H. Smith which forbids its use in
commercial products; and Unisys claimed a patent ("Welsh patent") on the 
second one (while their licensing would seem to mean that an
extractor-only program would not be covered).

Since the rest of the code is copyrighted by Info-Zip under a BSD-like
license, this Annvix package is covered by this license.

Please note that currently, default compilation of the Info-Zip
distribution also excludes the unreduce and unshrink code.
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files doc
%defattr(-,root,root)
%doc BUGS COPYING.OLD Contents History.* INSTALL README ToDo WHERE README.IMPORTANT.ANNVIX
%doc proginfo/


%changelog
* Thu Mar 20 2008 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- P4: security fix for CVE-2008-0888

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- rebuild

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- fix group

* Sat Mar 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- P3: security fix for CVE-2005-4667

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.52
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Oct 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.52-2avx
- P2: fix for CAN-2005-2475

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.52-1avx
- 5.52
- drop P0 and define LZW_CLEAN instead (waschk)
- drop P2; fixed upstream

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.50-15avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.50-14avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.50-13avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.50-12avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 5.50-11sls
- minor spec cleanups
- s/MANDRAKE/OPENSLS/ for important README

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 5.50-10sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
