%define name	opensls-release
%define version	1.0
%define release	0.1sls

%define distrib	Loki
%define realversion 1.0-CURRENT

Summary:	Open Secure Linux Server release file
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://opensls.org/
Group:		System/Configuration/Other
Source:		%name.tar.bz2
Icon:		mandrake-small.gif

BuildRoot:	%{_tmppath}/%{name}-root

Obsoletes:	rawhide-release redhat-release mandrake-release
Provides:	redhat-release rawhide-release mandrake-release

%description
Open Secure Linux Server (OpenSLS) release file.

%prep
%setup -n opensls-release

%install
mkdir -p $RPM_BUILD_ROOT/etc
echo "OpenSLS release %{realversion} (%{distrib}) for %{_target_cpu}" > $RPM_BUILD_ROOT/etc/opensls-release
ln -sf opensls-release $RPM_BUILD_ROOT/etc/redhat-release
ln -sf opensls-release $RPM_BUILD_ROOT/etc/mandrake-release

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CREDITS
/etc/opensls-release
/etc/mandrake-release
/etc/redhat-release

%changelog
* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 1.0-0.1sls
- 1.0-CURRENT
- for lack of a better icon, we'll leave mandrake-small.gif for the time
  being
- tidy spec

* Tue Sep 16 2003 Warly <warly@mandrakesoft.com> 9.2-1mdk
- 9.2

* Mon Sep  8 2003 Warly <warly@mandrakesoft.com> 9.2-0.9mdk
- test version for updates

* Wed Aug 27 2003 Warly <warly@mandrakesoft.com> 9.2-0.7mdk
- post rc1 version with CREDITS in %%doc

* Tue Aug 26 2003 Warly <warly@mandrakesoft.com> 9.2-0.6mdk
- rc1
- add CREDITS file from qa.mandrakesoft.com/wiki

* Tue Aug  5 2003 Warly <warly@mandrakesoft.com> 9.2-0.5mdk
- beta 2

* Mon Jul 21 2003 Warly <warly@mandrakesoft.com> 9.2-0.4mdk
- beta 1

* Sun Apr 06 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 9.2-0.3mdk
- my bad, s/cooker/Cooker/

* Sun Apr 06 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 9.2-0.2mdk
- name is now 'cooker'

* Thu Mar 27 2003 Warly <warly@mandrakesoft.com> 9.2-0.1mdk
- I'm getting old...

* Tue Mar 11 2003 Warly <warly@mandrakesoft.com> 9.1-1mdk
- Bamboo

* Tue Oct  8 2002 Warly <warly@mandrakesoft.com> 9.1-0.1mdk
- tough one
- really tough one

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 9.0-0.3mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Jul 22 2002 Warly <warly@mandrakesoft.com> 9.0-0.2mdk
- post 9.0 beta 1

* Wed Jul 17 2002 Warly <warly@mandrakesoft.com> 9.0-0.1mdk
- beta 1

* Thu Mar 21 2002 David BAUDENS <baudens@mandrakesoft.com> 8.3-0.2mdk
- Fix %%realversion (ie replace 'cooker' by '8.3' to don't break build of
  packages which use it)

* Tue Mar 19 2002 Warly <warly@mandrakesoft.com> 8.3-0.1mdk
- never stop

* Fri Mar 15 2002 Warly <warly@mandrakesoft.com> 8.2-1mdk
- 8.2

* Fri Mar  8 2002 Warly <warly@mandrakesoft.com> 8.2-0.7mdk
- 8.2 rc 1

* Sat Mar  2 2002 Warly <warly@mandrakesoft.com> 8.2-0.6mdk
- 8.2 beta 4

* Mon Feb 18 2002 Warly <warly@mandrakesoft.com> 8.2-0.5mdk
- 8.2 beta 3

* Fri Feb  8 2002 Warly <warly@mandrakesoft.com> 8.2-0.4mdk
- 8.2 beta 2

* Fri Jan 25 2002 Warly <warly@mandrakesoft.com> 8.2-0.3mdk
- 8.2 beta 1

* Tue Dec 11 2001 Warly <warly@mandrakesoft.com> 8.2-0.2mdk
- life goes on

* Wed Sep 26 2001 Warly <warly@mandrakesoft.com> 8.2-0.1mdk
- yeeepeeee

* Sun Sep 23 2001 Warly <warly@mandrakesoft.com> 8.1-1mdk
- 8.1 final

* Thu Sep  6 2001 Warly <warly@mandrakesoft.com> 8.1-0.6mdk
- 8.1 beta 3

* Mon Aug 27 2001 Warly <warly@mandrakesoft.com> 8.1-0.5mdk
- 8.1 beta 2

* Thu Aug 16 2001 Warly <warly@mandrakesoft.com> 8.1-0.4mdk
- 8.1 beta 1

* Tue Jun 19 2001 Warly <warly@mandrakesoft.com> 8.1-0.3mdk
- fix noarch problem

* Mon Jun 11 2001 Warly <warly@mandrakesoft.com> 8.1-0.2mdk
- Name changed to Mandrake Linux

* Sun Apr 22 2001 Warly <warly@mandrakesoft.com> 8.1-0.1mdk
- Cooker for 8.1

* Fri Apr 6 2001 Warly <warly@mandrakesoft.com> 8.0-0.5mdk
- Traktopel release candidate 1

* Sun Apr 1 2001 Warly <warly@mandrakesoft.com> 8.0-0.4mdk
- Traktopel beta 3

* Mon Mar 12 2001 Warly <warly@mandrakesoft.com> 8.0-0.3mdk
- Traktopel beta 2

* Mon Feb 26 2001 Warly <warly@mandrakesoft.com> 8.0-0.2mdk
- Traktopel beta 1

* Wed Feb  7 2001 Warly <warly@mandrakesoft.com> 8.0-0.1mdk
- Pre 8.0

* Fri Dec 22 2000 Warly <warly@mandrakesoft.com> 7.3-0.1mdk
- Cooker

* Thu Oct  5 2000 Warly <warly@mandrakesoft.com> 7.2-1mdk
- Odyssey

* Mon Oct  2 2000 Warly <warly@mandrakesoft.com> 7.2-0.2mdk
- Cooker 7.2 release candidate 1

* Thu Aug 31 2000 Warly <warly@mandrakesoft.com> 7.2-0.1mdk
- Cooker 7.2b

* Mon Jun  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.1-0.3mdk
- Fix bad links.

* Mon Jun  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.1-0.2mdk
- Set redhat-relase link to mandrake-release.
- On other arch of x86 print the arch.

* Thu Apr 20 2000 Warly <warly@mandrakesoft.com> 7.1-0.1mdk
- 7.1b

* Wed Mar 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 7.0-2mdk
- Adjust groups.
- No need to have the files as +x.

* Sat Jan 08 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 7.0 (Air).

* Wed Dec 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 7.0b (Oxygen).

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 6.2b (Oxygen).

* Thu Jul 15 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Jumping to full cooker :).

* Tue Jul 13 1999 Pablo Saratxaga <pablo@linux-mandrake.com>
- I stupidely forgot to put add the '-l $LANG' to the descriptions...

* Mon Jul 12 1999 Pablo Saratxaga <pablo@linux-mandrake.com>
- added an icon and some descriptions

* Wed May 19 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- change release name for final

* Sun May 16 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 6.0.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- [was redhat-release]
- add de locale
- Mandrake adaptions

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr
