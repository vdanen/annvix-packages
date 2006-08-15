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
%define version		4.2.1
%define release		%_revrel

Summary:	The GNU shar utilities for packaging and unpackaging shell archives
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving
URL:		http://www.gnu.org/software/sharutils/
Source:		ftp://prep.ai.mit.edu/pub/gnu/%{name}/%{name}-%{version}.tar.bz2
Patch1:		sharutils-4.2-gmo.patch
Patch2:		sharutils-4.2-man.patch
Patch3:		sharutils-4.2-po.patch
Patch4:		sharutils-4.2-share.patch
Patch5:		sharutils-4.2-uudecode.patch
Patch6:		sharutils-4.2.1-mktemp.patch
Patch7:		sharutils-4.2.1-uudecode.patch
Patch10:	sharutils-4.2.1-remsync-typo.patch
Patch11:	sharutils-4.2.1-bogus-entries.patch
Patch12:	sharutils-4.2.1-CAN-2004-1772.patch
Patch13:	sharutils-4.2.1-CAN-2004-1773.patch
Patch14:	sharutils-4.2.1-deb-302412.patch

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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p0 -b .can-2004-1772
%patch13 -p1 -b .can-2004-1773
%patch14 -p1 -b .deb-302412


%build
%configure

# do not need to link with libintl explicitly for gettext support
perl -pi -e 's/-lintl//g' src/Makefile

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall install-man

# fix japanese catalog file
if [ -d %{buildroot}/%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
    pushd %{buildroot}%{_datadir}/locale
        mv ja_JP.EUC ja
    popd
fi

%kill_lang %{name}
%find_lang %{name}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,755)
%{_bindir}/*
%{_infodir}/sharutils*
%{_infodir}/remsync*
%{_mandir}/man?/*


%changelog
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
