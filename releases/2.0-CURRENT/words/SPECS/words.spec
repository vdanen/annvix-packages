#
# spec file for package words
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		words
%define version		2
%define release		%_revrel

%define _dict_dir	/usr/share/dict/

Summary:	A dictionary of English words for the /usr/dict directory
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		Text Tools
URL:		http://sunsite.unc.edu/pub/Linux/libs/
Source:		ftp://sunsite.unc.edu/pub/Linux/libs/linux.words.2.tar.bz2
Patch0:		linux.words.2-jbj.patch
Patch1:		linux.words.2-mmm.patch
Patch2:		linux.words.2-meat.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
The words file is a dictionary of English words for the /usr/dict
directory.  Programs like ispell use this database of words to check
spelling.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_dict_dir}

cp usr/dict/linux.words %{buildroot}/%{_dict_dir}
ln -sf linux.words %{buildroot}%{_dict_dir}words


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_dict_dir}linux.words
%{_dict_dir}words

%files doc
%defattr(-,root,root)
%doc usr/dict/README.linux.words
%doc usr/dict/README2.linux.words


%changelog
* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2
- add -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2-24avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2-23avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2-22avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2-21sls
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2-20sls
- OpenSLS build
- tidy spec

* Sat Jul 12 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2-19mdk
- rebuild

* Tue Dec  4 2001 Warly <warly@mandrakesoft.com> 2-18mdk
- rpmlint fixes

* Fri Sep 21 2001 Vincent Saugey <vince@mandrakesoft.com> 2-17mdk
- Correct Distribution Flag

* Mon Jul 24 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2-16mdk
- BM

* Sat Apr 08 2000 - Christopher Molnar <molnarc@mandrakesoft.com> 2-15mdk
- Chnaged to new groups

* Wed Nov 24 1999 - David BAUDENS <baudens@mandrakesoft.com>
- Build release
- Remove de locale

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- add de locale

* Wed Sep 30 1998 Bill Nottingham <notting@redhat.com>
- take out extra.words (they're all in linux.words)

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- correct desiccate (problem #794)

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
