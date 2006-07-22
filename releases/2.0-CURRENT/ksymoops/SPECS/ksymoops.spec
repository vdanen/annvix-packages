#
# spec file for package ksymoops
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ksymoops
%define version 	2.4.9
%define release 	%_revrel

Summary:	Kernel oops and error message decoder
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		ftp://ftp.kernel.org/pub/linux/utils/kernel/ksymoops/v2.4/
Source0:	%{name}-%{version}.tar.bz2
Source1:	ksymoops-gznm
Source2:	ksymoops-script
Source3:	README.annvix
Patch1:		ksymoops-2.4.3-add_gz_modules_support

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	binutils-devel
Requires:	binutils
ExclusiveOS:	Linux


%description
The Linux kernel produces error messages that contain machine specific
numbers which are meaningless for debugging.  ksymoops reads machine
specific files and the error log and converts the addresses to
meaningful symbols and offsets.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1


%build
CFLAGS="%{optflags}" make DEF_MAP=\\\"/boot/System.map-*r\\\" all

 
%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make INSTALL_PREFIX=%{buildroot}%{_prefix} INSTALL_MANDIR=%{buildroot}%{_mandir}/ install
mv %{buildroot}%{_bindir}/ksymoops %{buildroot}%{_bindir}/ksymoops.real
install -m 0755 %{SOURCE1} %{buildroot}%{_bindir}
install -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/ksymoops
install -m 0644 %{SOURCE3} .


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/ksymoops
%{_bindir}/ksymoops-gznm
%{_bindir}/ksymoops.real
%{_mandir}/man8/ksymoops.8*

%files doc
%defattr(-,root,root)
%doc COPYING README INSTALL Changelog README.annvix


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.9
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.9
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.9
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.9-5avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.9-4avx
- rebuild

* Tue Feb 15 2005 Vincent Danen <vdanen@mandrakesoft.com> 2.4.9-3avx
- first Annvix build

* Fri Sep  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.9-2mdk
- fix deps

* Wed Aug 13 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.9-1mdk
- don't provide kernel-utils anymore.
- 2.4.9.

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.4.8-2mdk
- rebuild
- drop Prefix tag
- rm -rf %%{buildroot} at the beginning of %%install
- macroize

* Mon Dec  9 2002 Juan Quintela <quintela@mandrakesoft.com> 2.4.8-1mdk
- 2.4.8.

* Wed Apr 10 2002 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-1mdk
- compile with RPM_OPT_FLAGS.
- 2.4.5.

* Tue Feb 26 2002 Juan Quintela <quintela@bi.mandrakesoft.com> 2.4.3-4mdk
- Corrected a missing space in the find command line (Duclos Andre).

* Mon Feb 25 2002 Juan Quintela <quintela@bi.mandrakesoft.com> 2.4.3-3mdk
- Corrected permissions of README.mandrake (Duclos Andre).

* Wed Feb  6 2002 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-2mdk
- s/%%{buildroot}/$buildroot/.
- add ksymoops script to put the KSYMOOPS_NM to find the gznm instead of nm.
- add gznm script to make nm <module> work indepently if it is gzipped or not.
- add support for gzipped modules.

* Mon Oct  8 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-1mdk
- Provides kernel-utils.
- 2.4.3.
- s/Copyright/License/.

* Wed May  2 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.1-1mdk
- 2.4.1.

* Sun Mar  4 2001 Pixel <pixel@mandrakesoft.com> 2.4.0-3mdk
- better require binutils (as objdump is required too)

* Sun Mar  4 2001 Pixel <pixel@mandrakesoft.com> 2.4.0-2mdk
- add require on /usr/bin/nm

* Wed Feb 14 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.0-1mdk
- First spec file for Mandrake distribution.

# end of file
