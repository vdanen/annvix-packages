Summary: A dictionary of English words for the /usr/dict directory
Name: words
Version: 2
Release: 19mdk
License: Public Domain
URL: http://sunsite.unc.edu/pub/Linux/libs/
Group: Text tools
Source: ftp://sunsite.unc.edu/pub/Linux/libs/linux.words.2.tar.bz2
Patch0: linux.words.2-jbj.patch.bz2
Patch1: linux.words.2-mmm.patch.bz2
Patch2: linux.words.2-meat.patch.bz2
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/words-root

%define _dict_dir /usr/share/dict/

%description
The words file is a dictionary of English words for the /usr/dict
directory.  Programs like ispell use this database of words to check
spelling.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_dict_dir}

cp usr/dict/linux.words $RPM_BUILD_ROOT/%{_dict_dir}
ln -sf linux.words $RPM_BUILD_ROOT%{_dict_dir}words

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc usr/dict/README.linux.words
%doc usr/dict/README2.linux.words
%{_dict_dir}linux.words
%{_dict_dir}words

%changelog
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
