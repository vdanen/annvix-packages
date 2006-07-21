#
# spec file for package chkconfig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		chkconfig
%define version		1.3.25
%define release		%_revrel

Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		ftp://ftp.redhat.com/pub/redhat/code/chkconfig/
Source:		ftp://ftp.redhat.com/pub/redhat/code/chkconfig/chkconfig-%{version}.tar.bz2
Patch1:		ntsysv-mdkconf.patch
Patch3:		chkconfig-runleveldir.patch
Patch4:		ntsysv-tvman.patch
Patch5:		chkconfig-fix.patch
Patch7:		chkconfig-1.3.4-list.patch
Patch8:		chkconfig-1.3.4-skip-files-with-dot.patch
Patch10:	chkconfig-1.3.11-fix-errno-xinetddotd.patch
Patch11:	chkconfig-1.3.25-lsb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext, newt-devel, popt-devel, slang

Conflicts:	rpm-helper < 0.6

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc*.d, to relieve system administrators of some 
of the drudgery of manually editing the symbolic links.


%package -n ntsysv
Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Group:		System/Configuration
Requires:	chkconfig

%description -n ntsysv
ntsysv updates and queries runlevel information for system services.
ntsysv relieves system administrators of having to directly manipulate
the numerous symbolic links in /etc/rc*.d.


%prep
%setup -q
%patch1 -p0 -b .mdkconf
%patch3 -p1 -b .runleveldir
%patch4 -p0 -b .tvman
%patch5 -p0 -b .fix
%patch7 -p1 -b .list
%patch8 -p1 -b .skip-files-with-dot
%patch10 -p1 -b .fix-errno-xinetddotd
%patch11 -p1 -b .lsb


%build
%ifarch sparc
LIBMHACK=-lm
%endif

%make RPM_OPT_FLAGS="%{optflags}" LIBMHACK=$LIBMHACK


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make instroot=%{buildroot} MANDIR=%{_mandir} install

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc${n}.d
done

pushd %{buildroot}%{_sysconfdir}/
    ln -s rc.d/init.d init.d
popd

# corrected indonesian language code (it has changed from 'in' to 'id')
mkdir -p %{buildroot}%{_datadir}/locale/id/LC_MESSAGES
mv %{buildroot}%{_datadir}/locale/{in,in_ID}/LC_MESSAGES/* \
    %{buildroot}%{_datadir}/locale/id/LC_MESSAGES || :
rm -rf %{buildroot}%{_datadir}/locale/{in,in_ID} || :

# we use our own alternative system
rm -f %{buildroot}%{_sbindir}/{alternatives,update-alternatives} %{buildroot}%{_mandir}/man8/alternatives.8*

# remove invalid locales
rm -rf %{buildroot}%{_datadir}/locale/{bn_IN,si}

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%attr(0750,root,admin) /sbin/chkconfig
%{_mandir}/man8/chkconfig.8*
%attr(0750,root,admin) %dir %{_sysconfdir}/rc.d
%attr(0750,root,admin) %dir %{_sysconfdir}/rc.d/init.d
%attr(0750,root,admin) %dir %{_sysconfdir}/rc.d/rc*
%{_sysconfdir}/init.d

%files -n ntsysv
%defattr(-,root,root)
%{_sbindir}/ntsysv
%{_mandir}/man8/ntsysv.8*


%changelog
* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- remove the pre-req on initscripts as it really isn't needed
  (initscripts has a pre-req on this pkg), and it puts rpm into a loop
  that causes all kinds of stupidness

* Tue Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- 1.3.25
- updated P11 from Mandriva:
  - drop hybrid LSB support, mostly merged upstream
  - simplify requirements check on delete
  - check for requirements when on add
- drop P6; we don't use xinetd
- own and set perms for /etc/rc.d (750/root:admin)
- chkconfig doesn't need to be run by normal users so fix it's perms too
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20-1avx
- 1.3.20
- drop P9; fixed upstream
- rediff P12; now handles hybrid scripts like shorewall (sbenedict)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.13-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.13-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.13-1avx
- 1.3.13
- fix LSB logic (flepied)
- drop the zh po file (S1) and special accomodations

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.8-6avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.3.8-5sls
- minor spec cleanups

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.3.8-4sls
- OpenSLS build
- tidy spec

* Wed Sep  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.3.8-3mdk
- own /etc/init.d /etc/rc.d/*

* Mon Aug  4 2003 Pixel <pixel@mandrakesoft.com> 1.3.8-2mdk
- skip bad symlinks in /etc/rc.d/init.d (instead of dying)

* Thu Jul 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.3.8-1mdk
- 1.3.8

* Sun Nov 24 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.6-1mdk
- 1.3.6

* Thu Nov 14 2002 David BAUDENS <baudens@mandrakesoft.com> 1.3.4-12mdk
- Rebuild against newt 0.51

* Fri Sep  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.4-11mdk
- do the security stuff in rpm-helper (removed patch0)

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.4-10mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Jul  5 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.4-9mdk
- Patch9: Correctly link libpopt, statically

* Mon Jun 24 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.4-8mdk
- Really move eu.

* Mon Jun 24 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.4-7mdk
- eu_ES is no more, changed to eu (Pablo).

* Sun Jun 23 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.3.4-6mdk
- Remove Patch2: not needed anymore because ntsysv checks for root access
  before entering anyway.
- Remove zh locale: name is incorrect, and file is empty anyway.

* Sun Jun  2 2002 Stefan van der Eijk <stefan@eijk.nu> 1.3.4-5mdk
- BuildRequires

* Thu May 16 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.4-4mdk
- corrected release naming

* Fri May 10 2002 Andrej Borsenkow <arvidjaar@mail.ru> 1.3.4-3.1mdk
- patch8 - make chkconfig ignore the same file as ntsysv (with ~ or , or
. in name)

* Wed Apr  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.4-3mdk
- patched chkconfig --list to report even if all levels are off.

* Sun Mar 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.3.4-2mdk
- use a more reliable method to get the secure level

* Thu Mar 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.3.4-1mdk
- new release

* Thu Jan 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.2.24-9mdk
- oops corrected core dump.

* Wed Jan 30 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.2.24-8mdk
- work cleanly without msec.

* Tue Jan 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.2.24-7mdk
- don't exit with an error code when the service isn't authorized.

* Mon Jan 28 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.2.24-6mdk
- use DURING_INSTALL to see if we are called from the installer.
- add back the snf modification but check that SECURE_LEVEL > 3 before
checking /etc/security/msec/server.

* Sun Jan 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.2.24-5mdk
- corrected the msec patch (I think it has never worked).
- reverted the snf modifications because it broke level <= 3.

* Thu Jan 24 2002 Pixel <pixel@mandrakesoft.com> 1.2.24-4mdk
- remove "Requires: msec" (it still works specially together with msec, but it doesn't *need* msec)

* Thu Nov 08 2001 Florin <florin@mandrakesoft.com> 1.2.24-3mdk
- update the msec patch for snf. The --msec option uses
- the /etc/security/msec/server file, a link to the server$1 file

* Tue Oct 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.24-2mdk
- add %%url

* Tue Sep 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.24-1mdk
- New and shiny chkconfig.

* Fri Aug 03 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.23-1mdk
- new release
- ntsysv requirse chkconfig

* Wed Jul 11 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.22-2mdk
- build release

* Tue May 22 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.22-1mdk
- Bump out the 1.2.22 chkconfig for everyone in cooker.
- s/Copyright/License/;

* Sun Apr 29 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.19-4mdk
- Minor revision of the zh_TW.Big5 translation by Abel Cheung 
  <maddog@linuxhall.org>.
  
* Sat Apr 21 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.19-3mdk
- Include zh_TW.Big5 translation.

* Thu Mar 22 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.2.19-2mdk
- Wow, there was big error in chkconfig-msec.patch,
  I should have been very tired when I coded that...

* Fri Mar  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.19-1mdk
- 1.2.19.

* Sun Nov 05 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.17-1mdk
- new and shiny version from the good folks at RedHat.
- fix unclean BM aka /etc/rc*.d not /etc/rc.d.
- remove chmou patch 7.

* Sat Sep 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.12-1mdk
- Skip also .rpmmnew in chkconfig.
- 1.2.12.
- Support of xinetd in chkconfig (not only ntsysv).

* Thu Sep 14 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.7-4mdk
- bug fix : chkconfig didn't do its job when the sysadmin delete a link
  this is a rh stupidity (they duplicate the --del code for --add but
  alter the first withouth altering the second)

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 1.2.7-3mdk
- use find_lang

* Wed Aug 09 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.7-2mdk
- fix ntsysv man page

* Tue Aug 08 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.7-1mdk
- s|1.0.8|1.2.7|
- macros and BM from Stefan :-)
- redid yoann's msec patch for chkconfig

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.8-10mdk
- automatically added BuildRequires

* Tue May 30 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 1.0.8-9mdk
- patch: doesn't update runlevel stuff if you are not root

* Fri Apr 14 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 1.0.8-8mdk
- Change printf on secure level error to reflect the new msec location.

* Fri Mar 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.0.8-7mdk
- group fix.

* Wed Mar 08 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- Modified the msec patch to use the new filesystem hierarchy used by msec.
	chkconfig will no use /etc/security/msec/server.[45]
- Require msec 0.10

* Thu Dec 30 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add standard mandrake colors.

* Thu Nov 25 1999 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- Added the --msec option, used when called from 
  Mandrake Security scripts. 

* Thu Nov 25 1999 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- Oops, fixed a little problem.

* Thu Nov 25 1999 Yoann Vandoorselaere <yoann@mandrakesoft.com>
- Hacked chkconfig to interoperate with Mandrake security package.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.0.8.

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build Release.

* Fri Oct  1 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.0.7

* Fri Aug 06 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- corrected indonesian language code (it has changed from 'in' to 'id')

* Thu Apr 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- release for Red Hat 6.0

* Thu Apr  8 1999 Matt Wilson <msw@redhat.com>
- added support for a "hide: true" tag in initscripts that will make
  services not appear in ntsysv when run with the "--hide" flag

* Thu Apr  1 1999 Matt Wilson <msw@redhat.com>
- added --hide flag for ntsysv that allows you to hide a service from the
  user.

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- fix glob, once and for all. Really. We mean it.

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- revert fix for services@levels, it's broken
- change default to only edit the current runlevel

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- don't remove scripts that don't support chkconfig

* Tue Mar 09 1999 Erik Troan <ewt@redhat.com>
- made glob a bit more specific so xinetd and inetd don't cause improper matches

* Thu Feb 18 1999 Matt Wilson <msw@redhat.com>
- removed debugging output when starting ntsysv

* Thu Feb 18 1999 Preston Brown <pbrown@redhat.com>
- fixed globbing error
- fixed ntsysv running services not at their specified levels.

* Tue Feb 16 1999 Matt Wilson <msw@redhat.com>
- print the value of errno on glob failures.

* Sun Jan 10 1999 Matt Wilson <msw@redhat.com>
- rebuilt for newt 0.40 (ntsysv)

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- add ru.po.

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- translation updates

* Thu Oct 08 1998 Cristian Gafton <gafton@redhat.com>
- updated czech translation (and use cs instead of cz)

* Tue Sep 22 1998 Arnaldo Carvalho de Melo <acme@conectiva.com.br>
- added pt_BR translations
- added more translatable strings
- support for i18n init.d scripts description

* Sun Aug 02 1998 Erik Troan <ewt@redhat.com>
- built against newt 0.30
- split ntsysv into a separate package

* Thu May 07 1998 Erik Troan <ewt@redhat.com>
- added numerous translations

* Mon Mar 23 1998 Erik Troan <ewt@redhat.com>
- added i18n support

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>
- added --back
