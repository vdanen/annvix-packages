Summary: 	A utility for retrieving files using the HTTP or FTP protocols.
Name: 		wget
Version: 	1.8.2
Release: 	12mdk
Group: 		Networking/WWW
License: 	GPL
URL: 		http://www.gnu.org/directory/GNU/wget.html

Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.bz2
# alt: ftp://ftp.gnu.org/gnu/wget/

Source2: 	wget-1.6-zh_CN.GB2312.po

Patch0: 	wget-1.6-passive_ftp.patch.bz2

Patch1: 	wget-1.8-print_percentage.patch.bz2
Patch2:		wget-1.7-remove-rpath-from-binary.patch.bz2
Patch3:		wget-1.8-no-solaris-md5.h.patch.bz2
Patch4:		wget-1.8.1-etc.patch.bz2
Patch5:		wget-1.8.1-netrc.patch.bz2
Patch6:		wget-1.8.1-quote.patch.bz2
Patch7:		wget-1.8.2-url_password.patch.bz2
Patch8:		wget-1.8.2-filename.patch.bz2
Patch9:		wget-1.8.2-logstdout.patch.bz2
Patch10:	wget-1.8.2-referer-opt-typo.patch.bz2
Patch11:	wget-1.8.2-fix-fr-translation.patch.bz2

Provides: 	webclient webfetch
BuildRequires:	gettext
BuildRequires:	openssl-devel
BuildRequires:	texinfo
BuildRoot: 	%_tmppath/%name-%version-%release-root
Prereq: 	/sbin/install-info


%description
GNU Wget is a file retrieval utility which can use either the HTTP or FTP
protocols. Wget features include the ability to work in the background
while you're logged out, recursive retrieval of directories, file name
wildcard matching, remote file timestamp storage and comparison, use of
Rest with FTP servers and Range with HTTP servers to retrieve files over
slow or unstable connections, support for Proxy servers, and
configurability.

%prep

%setup -q
%patch0 -p1 -b .passive_ftp
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .md5
%patch4 -p1 -b .etc
%patch5 -p1 -b .netrc
%patch6 -p1 -b .quotes
%patch7 -p1 -b .url_password
%patch8 -p1 -b .filename
%patch9 -p1 -b .logstdout
%patch10 -p0 -b .typo
%patch11 -p0 -b .frtypo

%build
#aclocal
autoconf
%configure
%make
# all tests must pass (but where are they?)
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

install -m755 util/rmold.pl %buildroot/%_bindir/rmold

rm -fr $RPM_BUILD_ROOT%{_datadir}/locale/zh

# Install Chinese locales.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/{zh_TW.Big5,zh_CN.GB2312}/LC_MESSAGES
msgfmt -v %SOURCE2 -o $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN.GB2312/LC_MESSAGES/wget.mo
%find_lang %name


%clean
rm -fr %buildroot

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files -f %name.lang
%defattr(-,root,root,-)
%verify(not md5 size mtime) %config(noreplace) %_sysconfdir/wgetrc
%doc AUTHORS COPYING ChangeLog MACHINES MAILING-LIST NEWS README TODO
%_bindir/*
%_infodir/*
%_mandir/man1/wget.1*

%changelog
* Sat Sep 06 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-12mdk
- fix wrong french translation (#4915)

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.8.2-11mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install

* Thu Jun 05 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-10mdk
- patch 10: support correct spelling of '--referrer' in options (#3991)
  (from Wes Landaker, hand edited by me so that patch succeed in applying it)

* Tue Feb 11 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.2-9mdk
- enable parallel build

* Wed Jan 22 2003 François Pons <fpons@mandrakesoft.com> 1.8.2-8mdk
- created patch so that -o - allow log to stdout.

* Wed Jan 15 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8.2-7mdk
- Rebuild again agains latest SSL.

* Tue Jan 14 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.8.2-6mdk
- Sync with latest OpenSSL.

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-5mdk
- build release

* Wed Dec 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.2-4mdk
- fix url (yura gusev)

* Tue Dec 10 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.8.2-3mdk
- P8: security fix for directory traversal problem
- remove double %%_mandir entry in %%files

* Wed Sep 04 2002 François Pons <fpons@mandrakesoft.com> 1.8.2-2mdk
- created patch 7 to allow @ in url password.

* Sun Jul 07 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8.2-1mdk
- Bump!
- Run make check in build.
- Patch cleanup and remove applied patches.

* Thu Jun  6 2002 Stefan van der Eijk <stefan@eijk.nu> 1.8.1-4mdk
- BuildRequires
- fixed %%configure

* Tue Apr 16 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.8.1-3mdk
- config file is in /etc, not in /usr/local [Patch10]
- warns of passwords in process list [Patch11]
- let DO_REALLOC_FROM_ALLOCA from wget.h work [Patch12]
- fix handling of <meta http-equiv=Refresh> (without "a content") [Patch13]
- fix .netrc parsing [Patch14]
- fix quotations of : and @ in username and password [Patch15]

* Thu Dec 27 2001 Stew Benedict <sbenedict@mandrakesoft.com> 1.8.1-2mdk
- drop PPC segfault patch

* Thu Dec 27 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8.1-1mdk
- Wget 1.8.1 (Abel).

* Wed Dec 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.8-1mdk
- The all-new-ad-shiny 1.8 out for download.
- Don't use /usr/include/md5.h but /usr/include/openssl/md5.h.

* Wed Nov 28 2001 François Pons <fpons@mandrakesoft.com> 1.7.1-3mdk
- added provides to webfetch (used by urpmi).

* Tue Nov 27 2001 Stew Benedict <sbenedict@mandrakesoft.com> 1.7.1-2mdk
- remove rpath, patch core dump on long URL - PPC

* Wed Nov 21 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.7.1-1mdk
- Make a shiny 1.7.1 for the cooker folks.

* Thu Jul 05 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.7-2mdk
- gcc accepts "-R" argument instead of "-rpath". Let configure determine
  the fact intself, hence properly enabling SSL. (patch4).
- Add missing manpage
- BuildRequires: libopenssl0-devel

* Wed Jun 06 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7-1mdk
- removed obsolete patches
- added patch 3
- Geoffrey Lee <snailtalk@mandrakesoft.com>
  - Remove Abel's translation, seems to have been integrated in wget already.
  
* Thu Apr 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.6-7mdk
- Add an updated Big5 translation from Abel Cheung (maddog@linuxhall.org).

* Tue Apr 10 2001 François Pons <fpons@mandrakesoft.com> 1.6-6mdk
- made --passive-ftp on by default.

* Tue Mar 27 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.6-5mdk
- Make a patch for a missing setlocale() call (Andrew Lee, YCheng).

* Sat Mar 03 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.6-4mdk
- Port SSL patch to 1.6 and activate it (please let me know if you found
  problems and no to the maintainner).

* Sun Jan 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.co> 1.6-3mdk
- remove bogus zh locale.
 
* Sun Jan 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.6-2mdk
- put in Chinese locales.

* Wed Jan 03 2001 David BAUDENS <baudens@mandrakesoft.com> 1.6-1mdk
- 1.6
- Spec clean up

* Fri Dec  8 2000  Daouda Lo <daouda@mandrakesoft.com> 1.5.3-13mdk
- bug fix (rfc 1738 reserves some character for special meaning) thanx Anon
- remove duplicate description

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5.3-12mdk
- BM

* Wed Jul 12 2000 Christian Zoffoli <czoffoli@linux-mandrake.com> 1.5.3-11mdk
- removed %group
- removed _sysconfdir 

* Tue Jul 11 2000 Christian Zoffoli <czoffoli@linux-mandrake.com> 1.5.3-10mdk
- macroszifications

* Sun Jul 02 2000 Christian Zoffoli <czoffoli@linux-mandrake.com> 1.5.3-9mdk.ipv6
- IPv6 support
- Merge with PLD distro

* Fri May 19 2000 Jerome Martin <jerome@mandrakesoft.com> 1.5.3-9mdk
- rebuilded package to fix distribution tag

* Wed Apr  5 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.5.3-8mdk
- updated BuildRoot
- new group Networking/WWW
- new home URL for source tarball

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- don't permit chmod 777 on symlinks.

* Wed Jul 21 1999 Gregus <gregus@etudiant.net>
- fr locale

* Wed May  5 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree
- add Provides

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.5.3

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.5.2
* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- modified group to Applications/Networking

* Wed Apr 22 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5.0
- they removed the man page from the distribution (Duh!) and I added it back
  from 1.4.5. Hey, removing the man page is DUMB!

* Fri Nov 14 1997 Cristian Gafton <gafton@redhat.com>
- first build against glibc
