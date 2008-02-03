#
# spec file for package sharutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		sharutils
%define version		4.7
%define release		%_revrel

Summary:	The GNU shar utilities for packaging and unpackaging shell archives
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.gnu.org/software/sharutils/
Source0:	ftp://ftp.gnu.org/pub/gnu/%{name}/REL-%{version}/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires(post):	info-install
Requires(preun): info-install

%description
The sharutils package contains the GNU shar utilities, a set of tools
for encoding and decoding packages of files (in binary or text format)
in a special plain text format called shell archives (shar).  This
format can be sent through email (which can be problematic for
regular binary files).  The shar utility supports a wide range of
capabilities (compressing, uuencoding, splitting long files for
multi-part mailings, providing checksums), which make it very flexible
at creating shar files.  After the files have been sent, the unshar
tool scans mail messages looking for shar files.  Unshar automatically
strips off mail headers and introductory text and then unpacks the shar
files.


%prep
%setup -q


%build
%configure2_5x --disable-rpath

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%kill_lang %{name}
%find_lang %{name}


%post
%_install_info %{name}.info


%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/sharutils*
%{_mandir}/man?/*


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.7
- 4.7
- drop all patches; merged upstream
- update source url

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1
- spec cleanups
- remove locales

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1-22avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1-21avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1-20avx
- bootstrap build

* Mon Apr 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1-19avx
- P12: security patch for CAN-2004-1772
- P13: security patch for CAN-2004-1773
- P14: security patch for debian bug #302412
- don't explicitly link with libintl for gettext support (abel)
- P3: fixed to add charset to po files (abel)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.2.1-18avx
- require info-install, not /sbin/install-info
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.2.1-17sls
- rebuild against new libintl

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.2.1-16sls
- minor spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 4.2.1-15sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
