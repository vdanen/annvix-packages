%define name	urpmi
%define version	4.6.23
%define release 2avx

%{expand:%%define compat_perl_vendorlib %(perl -MConfig -e 'printf "%%s\n", "%{?perl_vendorlib:1}" ? "%%{perl_vendorlib}" : "$Config{installvendorlib}"')}

%define use_locale	1
%define allow_karun	0
%define buildreq_locale	perl-MDK-Common-devel

Summary:	Command-line software installation tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Packaging
URL:		http://cvs.mandrakesoft.com/cgi-bin/cvsweb.cgi/soft/urpmi
Source0:	%{name}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	%{buildreq_locale} bzip2-devel rpm-devel >= 4.0.3 gettext
BuildArch:	noarch

Requires:	webfetch eject gnupg
PreReq:		perl-Locale-gettext >= 1.01-15avx rpmtools >= 5.0.2 perl-URPM >= 1.08
Conflicts:	curl < 7.13.0

%description
urpmi takes care of dependencies between rpms, using a pool (or pools) of rpms.

urpmi is Annvix's console-based software installation tool, developed by
Mandrakesoft. urpmi will follow package dependencies -- in other words, it will
install all the other software required by the software you ask it to install --
and it's capable of obtaining packages from a variety of media, including 
installation CD-ROMs, your local hard disk, and remote sources such as web or FTP
sites.


%if %{allow_karun}
%package -n urpmi-parallel-ka-run
Summary:	Parallel extension to urpmi using ka-run
Requires:	urpmi >= %{version}-%{release} ka-run >= 2.0-15mdk
Group:		%{group}

%description -n urpmi-parallel-ka-run
urpmi-parallel-ka-run is an extension module to urpmi for handling
distributed installation using ka-run tools.
%endif

%package -n urpmi-parallel-ssh
Summary:	Parallel extension to urpmi using ssh and scp
Requires:	urpmi >= %{version}-%{release} openssh-clients perl
Group:		%{group}

%description -n urpmi-parallel-ssh
urpmi-parallel-ssh is an extension module to urpmi for handling
distributed installation using ssh and scp tools.

%prep
%setup -q -n %{name}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%{__make} PREFIX=%{buildroot} MANDIR=%{buildroot}%{_mandir} install

# remove gurpmi
rm -f %{buildroot}%{_sbindir}/gurpmi*
rm -f %{buildroot}%{_bindir}/gurpmi*

for dir in partial headers rpms
do
  install -d %{buildroot}/var/cache/urpmi/$dir
done

cat <<EOF >%{buildroot}%{_sysconfdir}/urpmi/inst.list
# Here you can specify packages that need to be installed instead
# of being upgraded.
EOF

mkdir -p %{buildroot}%{compat_perl_vendorlib}
install -m 644 urpm.pm %{buildroot}%{compat_perl_vendorlib}/urpm.pm
mkdir -p %{buildroot}%{compat_perl_vendorlib}/urpm

for p in args cfg download msg sys util parallel_ka_run parallel_ssh
do
    install -m 0644 urpm/$p.pm %{buildroot}%{compat_perl_vendorlib}/urpm/$p.pm
done

mkdir -p %{buildroot}%{_mandir}/man3
pod2man urpm.pm >%{buildroot}%{_mandir}/man3/urpm.3

mv -f %{buildroot}%{_bindir}/rpm-find-leaves %{buildroot}%{_bindir}/urpmi_rpm-find-leaves

# logrotate
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%if ! %{allow_karun}
rm -f %{buildroot}%{compat_perl_vendorlib}/urpm/parallel_ka_run.pm
%endif


%find_lang %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%preun
if [ "$1" = "0" ]; then
  cd /var/lib/urpmi
  rm -f compss provides depslist* descriptions.* *.cache hdlist.* synthesis.hdlist.* list.*
  cd /var/cache/urpmi
  rm -rf partial/* headers/* rpms/*
fi
exit 0

%post -p /usr/bin/perl
use urpm;
if (-e "/etc/urpmi/urpmi.cfg") {
    $urpm = new urpm;
    $urpm->read_config;
    $urpm->update_media(nolock => 1, nopubkey => 1);
}


%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog
%dir %{_sysconfdir}/urpmi
%dir /var/lib/urpmi
%dir /var/cache/urpmi
%dir /var/cache/urpmi/partial
%dir /var/cache/urpmi/headers
%dir /var/cache/urpmi/rpms
%config(noreplace) %{_sysconfdir}/urpmi/skip.list
%config(noreplace) %{_sysconfdir}/urpmi/inst.list
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/urpmi_rpm-find-leaves
%{_bindir}/urpmf
%{_bindir}/urpmq
%{_sbindir}/urpmi
%{_sbindir}/urpme
%{_sbindir}/urpmi.*
%{_mandir}/man?/urpm*
%{_mandir}/man?/proxy*
# find_lang isn't able to find man pages yet...
%lang(cs) %{_mandir}/cs/man?/urpm* 
%lang(et) %{_mandir}/et/man?/urpm* 
%lang(eu) %{_mandir}/eu/man?/urpm* 
%lang(fi) %{_mandir}/fi/man?/urpm* 
%lang(fr) %{_mandir}/fr/man?/urpm* 
%lang(nl) %{_mandir}/nl/man?/urpm* 
%lang(ru) %{_mandir}/ru/man?/urpm* 
%lang(uk) %{_mandir}/uk/man?/urpm*
%{compat_perl_vendorlib}/urpm.pm
%dir %{compat_perl_vendorlib}/urpm 
%{compat_perl_vendorlib}/urpm/args.pm
%{compat_perl_vendorlib}/urpm/cfg.pm
%{compat_perl_vendorlib}/urpm/download.pm
%{compat_perl_vendorlib}/urpm/msg.pm
%{compat_perl_vendorlib}/urpm/sys.pm
%{compat_perl_vendorlib}/urpm/util.pm

%if %{allow_karun}
%files -n urpmi-parallel-ka-run
%defattr(-,root,root)
%doc urpm/README.ka-run
%{compat_perl_vendorlib}/urpm/parallel_ka_run.pm
%endif

%files -n urpmi-parallel-ssh
%defattr(-,root,root)
%doc urpm/README.ssh
%{compat_perl_vendorlib}/urpm/parallel_ssh.pm

%changelog
* Mon Mar 28 2005 Vincent Danen <vdanen@annvix.org> 4.6.23-2avx
- sync with 4.6.23-5mdk

* Thu Mar 17 2005 Vincent Danen <vdanen@annvix.org> 4.6.23-1avx
- 4.6.23

* Tue Mar 01 2005 Vincent Danen <vdanen@annvix.org> 4.6.20-1avx
- 4.6.20
- requires perl-URPM 1.08
- conflicts curl < 7.13.0

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 4.6.14-1avx
- 4.6.14
- update description
- PreReq: perl-URPM >= 1.04, rpmtools >= 5.0.2

* Tue Sep 14 2004 Vincent Danen <vdanen@annvix.org> 4.5-1avx
- 4.5
- Requires: perl (on urpmi-parallel-ssh)
- remove gurpmi completely
- remove bash_completion stuff
- kernel stuff doesn't need to be in inst.lst anymore

* Fri Jun 18 2004 Vincent Danen <vdanen@annvix.org> 4.4-50avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.4-49sls
- remove %%build_opensls macro
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 4.4-48sls
- new macro: %%allow_karun which is off for OpenSLS builds
- fix %%allow_gurpmi macro
- don't build gurpmi

* Fri Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.4-47sls
- OpenSLS build
- tidy spec
- do a lot of %%define forces using %%build_opensls macro
- remove Distribution tag
- don't use %%real_release

* Sun Dec 14 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-46mdk
- fixed improper restart and possible loop of restart.

* Tue Dec  9 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-45mdk
- added compability with RH 7.3.

* Fri Dec  5 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-44mdk
- fixed bug 6013, 6386, 6459.
- fixed restart of urpmi in test mode which should be avoided.
- added executability if perl-Locale-gettext is missing.

* Wed Nov  5 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 4.4-43mdk
- urpmi: fix exitcode always true when running in gurpmi mode, by
  using _exit instead of exit, probably some atexit gtk stuff in the way

* Wed Nov 05 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 4.4-42mdk
- added bash-completion
- spec cleanup
- bziped additional sources

* Thu Oct 30 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-41mdk
- added the Erwan feature (update rpm, perl-URPM or urpmi first and
  restart urpmi in such case).
- added contributors section in man page (please accept I may have
  forget you, so ask to authors in such case).

* Tue Oct 21 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-40mdk
- fixed invalid signature checking when using --media on first
  package listed.

* Tue Oct  7 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-39mdk
- fixed names.XXX file not always regenerated.

* Tue Sep 23 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-38mdk
- fixed md5sum or copy of hdlist of virtual media uneeded.
- fixed bug 5807 for names.XXX files still present after removing
  medium XXX.
- fixed bug 5802 about exotic character recognized as default answer.
- fixed bug 5833 about urpme having Y for removing packages by default.
- fixed parallel urpme on some cases.

* Wed Sep 17 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-37mdk
- fixed virtual media examination of list file.

* Tue Sep 16 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-36mdk
- fixed virtual media examination of descriptions or pubkey files.
- fixed adding medium on a directory directly under root, as in
  file://tmp for example.
- removing stale logs.

* Wed Sep 10 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-35mdk
- get back skipping warning as log (so disabled by default for urpmi).
- make sure one package is only displayed once for skipping and
  installing log.
- translation and cs man pages updates.
- fixed urpmf man pages.

* Mon Sep  8 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-34mdk
- make sure --force will answer yes for all question (except
  choosing a package and changing removable media, this means that
  signature checking is also disabled).
- force second pass if virtual media using hdlist are used.
- improved probing files for hdlist or synthesis.

* Sat Sep  6 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-33mdk
- added automatic generation of /var/lib/urpmi/names.<medium>
  for completion to be faster.
- skipped or installed entries are first tested against
  compatible arch.

* Fri Sep  5 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-32mdk
- fixed symlink in current working directory.
- added fixes from gc (signature checking improvement and
  basename usage).
- fixed bad reason with standalone star in text.
- skipping log are now always displayed.

* Thu Sep  4 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-31mdk
- removed obsoleted and no more used -d of urpmi.update.
- fixed --bug to handle local pakcages and virtual media.
- added -z option to urpmi, urpmi.addmedia and urpmi.update for
  handling on the fly compression if possible, only handled for
  rsync:// and ssh:// protocol currently.
- removed -z option by default for rsync:// protocol.
- avoid trying locking rpmdb when using --env.
- fixed media updating on second pass when a synthesis
  virtual medium is used.

* Tue Sep  2 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-30mdk
- improved checking to be safer and smarter.
- added urpm::check_sources_signatures.

* Mon Sep  1 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-29mdk
- fixed @EXPORT of *N to be N only (avoid clashes with rpmdrake
  or others, and fix #5090)
- added urpmi.cfg man page in section 5.
- fixed bug 5058.

* Thu Aug 28 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-28mdk
- fixed transaction number restarting at 1 in split mode.
- updated C and fr man pages.
- added urpme man page.

* Thu Aug 28 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-27mdk
- update /var/lib/urpmi/MD5SUM for managing md5sum of files.
- make sure cwd is changed when downloading to cache directory.

* Tue Aug 26 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-26mdk
- added -z for rsync:// protocol by default.
- fixed some cosmetic log glitches when progressing download.
- fixed multiple removable device management.
- fixed urpmi not locking urpmi db.

* Fri Aug 22 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-25mdk
- automatically fork transaction if they are multiple.

* Thu Aug 21 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-24mdk
- updated with newer perl-URPM (changes in URPM::Signature).

* Wed Aug 20 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-23mdk
- fixed bad key ids recognized from pubkey during update of media.
- simplified list and pubkey location to be more compatible with
  previous version and avoid probing too many files.
- simplified log to be more explicit when a key is imported.

* Tue Aug 19 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-22mdk
- fixed MD5SUM and pubkey management for local media.
- fixed post deadlock with rpm < 4.2.

* Mon Aug 11 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-21mdk
- added -a flag for urpmq (so that urpmq -a -y -r will do what
  is requested more or less).
- fixed rsync:// and ssh:// protocol with integer limit-rate not
  multiple of 1024.
- removed requires on perl-DateManip (as it now optional).

* Mon Aug 11 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-20mdk
- fixed bug 4637 and add reason for removing package in urpme.
- fixed handling of pubkey file.
- fixed proxy typo when using curl (Guillaume).

* Wed Aug  6 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-19mdk
- fixed local package not found when using curl and without an
  absolute path.
- added signature support on distant media (in pubkey file).
- fixed bug 4519.
- fixed bug 4513 (--no-md5sum added for test purpose, workaround).

* Fri Aug  1 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-18mdk
- fixed shared locks management by simple user.

* Fri Aug  1 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-17mdk
- fixed shared locks management (were always exclusive).

* Thu Jul 31 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-16mdk
- fixed transaction number when split is active.
- fixed transaction which should not be splited in parallel mode.
- use a regular file opened in write mode for locking.
- added shared lock for urpmi, urpmq and urpmf (exclusive lock
  are done by urpmi.addmedia, urpmi.removemedia and urpmi.update).

* Tue Jul 29 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-15mdk
- fixed urpme --parallel --auto still asking the user.
- fixed --keep for parallel mode.

* Tue Jul 29 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-14mdk
- fixed urpme --auto disabling fuzzy report.
- fixed urpme --parallel which was not handling log.
- fixed urpme to always ask user in parallel mode.
- fixed urpme --parallel when one node has not a package.
- make package compilable and workable directly on
  Mandrake Clustering which is a 9.0 based distribution.

* Mon Jul 28 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-13mdk
- fixed trying to promote ARRAY(...) message.
- fixed output of urpmq to be sorted.
- added support for --keep in urpmi and urpmq to give an hint
  for resolving dependencies about trying to keep existing
  packages instead of removing them.
- added some translations to french man page of urpmi.

* Mon Jul 28 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-12mdk
- avoid spliting transaction if --test is used.

* Mon Jul 28 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-11mdk
- fixed bug 4331.
- printing error again at the end of installation when multiple
  transaction failed.

* Fri Jul 25 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-10mdk
- added urpme log and urpmi removing log (bug 3889).
- fixed undefined subroutine ...N... when using parallel
  mode (bug 3982).
- fixed moving of files inside the cache (bug 3833).
- fixed not obvious error message (bug 3436).
- fixed parallel installation of local files.

* Thu Jul 17 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-9mdk
- fixed error code reporting after installation.
- fixed if packages have not been found on some cases.

* Thu Jun 26 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-8mdk
- fixed urpmq -d not working if package given has unsatisfied
  dependencies as backtrack is active, now -d use nodeps.
- added @unsatisfied@ info with -c of urpmq.
- fixed lock database error when upgrading urpmi.
- added hack to avoid exiting installation with --no-remove
  if --allow-force is given, avoid removing packages in such
  cases.

* Thu Jun 26 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-7mdk
- fixed building of hdlist.

* Fri Jun 20 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-6mdk
- fixed --virtual to work with synthesis source.

* Thu Jun 19 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-5mdk
- fixed everything already installed annoying message.
- added --virtual to urpmi.addmedia to handle virtual media.
- added promotion message reason for backtrack.

* Wed Jun 18 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-4mdk
- added --env to urpmq and urpmf (simplest to examine now).
- fixed --allow-nodeps and --allow-force no more taken into
  account (bug 4077).

* Wed Jun 18 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-3mdk
- changed --split-level behaviour to be a trigger (default 20).
- added --split-length to give minimal transaction length (default 1).
- added missing log for unselected and removed packages in auto mode.

* Tue Jun 17 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-2mdk
- fixed parallel handler with removing.
- fixed glitches with gurpmi.
- fixed bad test report.
- fixed bad transaction ordering and splitting on some cases.

* Mon Jun 16 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.4-1mdk
- added preliminary support for small transaction set.
- internal library changes (compabilility should have been kept).

* Fri Jun 13 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-15mdk
- fixed incorrect behaviour when no key_ids options are set.
- created retrieve methods and translation methods for packages
  unselected or removed.

* Fri Jun 13 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-14mdk
- added key_ids global and per media option to list authorized
  key ids.
- improved signature checking by sorting packages list and give
  reason as well as signature results (may be hard to read but
  very fine for instance).
- need perl-URPM-0.90-10mdk or newer for signature handling.

* Thu Jun  5 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-13mdk
- added patch from Micha?l Scherer to add --no-uninstall
  (or --no-remove) and assume no by default when asking to
  remove packages.
- updated urpmq with newer perl-URPM 0.90-4mdk and better.
- fixed bad display of old package installation reason.

* Mon May 26 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-12mdk
- updated for newer perl-URPM 0.90 series.
- give reason of package requested not being installed.

* Fri May 16 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-11mdk
- try to handle resume connection (do not always remove previous
  download, only works for hdlist or synthesis using rsync).
- updated for perl-URPM-0.84 (ask_remove state hash simplified).

* Tue May 13 2003 Pons Fran?ois <fpons@mandrakesoft.com> 4.3-10mdk
- updated to use latest perl-URPM (simplified code, no interface
  should be broken).

* Mon May 12 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 4.3-9mdk
- internalize grpmi in gurpm.pm so that we can share graphical
  progression of download and installation between gurpmi and
  rpmdrake

* Fri Apr 25 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-8mdk
- added -i in urpmq --help (fix bug 3829).
- fixed many urpmf options: --media, --synthesis, -e.
- added --excludemedia and --sortmedia to urpmf.
- fixed --sortmedia not working properly.
- slightly modified cache management for rpms, not always use
  partial subdirectory before transfering to rpms directory.
- improved --list-aliases, --list-nodes and --list-media to be
  much faster than before.

* Thu Apr 24 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-7mdk
- added -v to urpme and removed default log.
- avoid curl output to be seen.
- make require of Date::Manip optional (urpmi manage to continue
  evan if Date::Manip is not there of fail due to unknown TZ).

* Wed Apr 23 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-6mdk
- added more log when installing packages.
- urpmf: added --sourcerpm, --packager, --buildhost, --url, --uniq
  and -v, -q, -u (as alias to --verbose, --quiet, --uniq).

* Tue Apr 22 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-5mdk
- improved output of urpmq -i (with packager, buildhost and url).
- fixed output of download informations (without callback).
- fixed error message of urpmi.update and urpmi.removemedia when
  using -h or --help.
- fixed urpmq -i to work on all choices instead of the first one.

* Fri Apr 18 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-4mdk
- added urpmq -i (the almost same as rpm -qi).

* Thu Apr 17 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-3mdk
- fixed readlink that make supermount sloowwwwwiiiinnnngggg.
- improved find_mntpoints to follow symlink more accurately
  but limit to only one mount point.
- fixed media which are loosing their with_hdlist ramdomly.

* Wed Apr 16 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-2mdk
- added --sortmedia option to urpmi and urpmq.
- improved MD5SUM file for hdlist or synthesis management, added
  md5sum in /etc/urpmi/urpmi.cfg for each media when needed.
- improved output when multiple package are found when searching.

* Mon Apr 14 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.3-1mdk
- avoid scanning all urpmi cache for checking unused rpm files.
- added smarter skip.list support (parsed before resolving requires).
- added --excludemedia options to urpmi and urpmq.
- obsoleted -h, added --probe-synthesis, --probe-hdlist,
  --no-probe, now --probe-synthesis is by default.
- added --excludedocs option.
- fixed --excludepath option.

* Fri Mar 28 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 4.2-35mdk
- add perl-MDK-Common-devel in the BuildRequires: because we need
  perl_checker to build (silly, no?), thx Stefan

* Thu Mar 27 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 4.2-34mdk
- fix MandrakeClub downloads problem: take advantage of
  --location-trusted when available (available in curl >=
  7.10.3-2mdk)

* Thu Mar 13 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-33mdk
- fix bug 3258 (use curl -k only for https for curl of 9.0).

* Wed Mar 12 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-32mdk
- added https:// protocol. (avoid curl limitation and fix bug 3226).

* Mon Mar 10 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-31mdk
- try to be somewhat perl_checker compliant.
- strict require on urpmi.

* Thu Mar  6 2003 Pons Fran?ois <fpons@mandrakesoft.com> 4.2-30mdk
- fixed %%post script to be simpler and much faster.

* Thu Mar  6 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-29mdk
- reworked po generation completely due to missing translations
  now using perl_checker. (pablo)
- changed library exports (now N function is always exported).

* Tue Mar  4 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 4.2-28mdk
- fixed french translations.
- fix bug 2680.

* Mon Mar  3 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-27mdk
- avoid mounting or unmounting a supermounted device.
- updated french translations (some from Th?venet C?dric).

* Fri Feb 28 2003 Pons Fran?ois <fpons@mandrakesoft.com> 4.2-26mdk
- added sanity check of list file used (fix bug 2110 by providing
  a reason why there could be download error).

* Fri Feb 28 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-25mdk
- fixed callback behaviour for rpmdrake.

* Thu Feb 27 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-24mdk
- fixed removable devices not needing to be umouting if
  supermount is used.
- umount removable devices after adding or updating a medium.

* Mon Feb 24 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-23mdk
- fixed bug 2342 (reported exit code 9 for rpm db access failure)

* Fri Feb 21 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-22mdk
- fixed callback not sent with wget if a file is not downloaded.
- fixed rsync:// protocol to support :port inside url.
- simplified propagation of download callback, always protect
  filename for password.
- added newer callback mode for rpmdrake.

* Thu Feb 20 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-21mdk
- modified --test output to be consistent about the same
  message displayed if installation is possible whatever
  verbosity (fixed bug 1955).

* Thu Feb 20 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-20mdk
- fixed bug 1737 and 1816.

* Mon Feb 17 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-19mdk
- fixed bug 1719 (ssh distributed mode not working).
- fixed english typo.

* Fri Feb 14 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-18mdk
- fixed bug 1473 and 1329.
- fixed bug 1608 (titi sucks).

* Wed Feb 12 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-17mdk
- added some perl_checker suggestions (some from titi).
- help urpmf probe if this is a regexp or not (only ++ checked).

* Wed Jan 29 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-16mdk
- fixed limit-rate and excludepath causing error in urpmi.cfg.
- take care of limit-rate in urpmi.update and urpmi.addmedia.

* Tue Jan 28 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-15mdk
- fixed verify-rpm (both in urpmi.cfg or command line).
- fixed default options activated.
- fixed error message about unknown options use-provides and
  post-clean.

* Mon Jan 27 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-14mdk
- added more global options to urpmi.cfg: verify-rpm, fuzzy,
  allow-force, allow-nodeps, pre-clean, post-clean, limit-rate,
  excludepath.

* Mon Jan 27 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-13mdk
- simplified portage to perl 5.6.1, because the following
  open F, "-|", "/usr/bin/wget", ... are 5.8.0 restrictive.
- fixed problem accessing removable media.

* Mon Jan 27 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-12mdk
- fixed stupid typo using curl.

* Fri Jan 24 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-11mdk
- add --limit-rate option to urpmi, urpmi.addmedia and
  urpmi.update.
- add preliminary support for options in urpmi.cfg, only
  verify-rpm is supported yet, format is as follow
    {
      verify-rpm : on|yes
      verify-rpm
      no-verify-rpm
    }

* Thu Jan 23 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-10mdk
- added download log support for rsync and ssh protocol.
- make log not visible in log file instead url.

* Thu Jan 23 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-9mdk
- fix bug 994 according to Gerard Patel.
- added download log for urpmi.addmedia and urpmi.update.
- fixed wget download log with total size available.

* Wed Jan 22 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-8mdk
- add callback support for download (fix bug 632 and 387).

* Mon Jan 20 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-7mdk
- fixed bug 876.

* Thu Jan 16 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-6mdk
- fixed bug 778 (in cvs since January 11 but not uploaded).
- more translations.

* Fri Jan 10 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-5mdk
- added a reason for each removed package.

* Wed Jan  8 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-4mdk
- updated english man pages and french version of urpmi.

* Mon Jan  6 2003 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-3mdk
- fixed -q to avoid a message.
- made -q and -v opposite.
- added -i to urpmf.
- check rpmdb open status (should never fails unless...) in order
  to give a better error message.
- added et man pages.

* Thu Dec 19 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-2mdk
- added log for package download if verbose.
- fixed using hdlist if no synthesis available or invalid.

* Wed Dec 18 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.2-1mdk
- fixed file:// protocol now checking file presence.
- added distributed urpme (both ka-run and ssh module).
- updated perl-URPM and urpmi requires on version (major
  fixes in perl-URPM-0.81 and extended urpme in urpmi-4.2).

* Fri Dec 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-18mdk
- fixed urpmf so that if callback is not compilable display help.
- fixed urpmq and urpmi call without parameter to display help.
- added donwload lock to avoid clashes from urpmi.update.

* Fri Dec 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-17mdk
- added mput or scp exit code checking.
- temporaly using hdlist file for --summary of urpmf.
- fixed perl warning (useless code which was not really useless but
  by side effects in fact).

* Fri Dec 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-16mdk
- fixed warning message from distributed module for local rpms.
- fixed bad test including a 0 for distributed install.

* Wed Dec 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-15mdk
- improve speed of urpmf dramatically if no --files (default if
  no flags given) nor --description are given.
- removed not coded --prereqs of urpmf (use --requires with [*]
  instead).

* Wed Dec 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-14mdk
- changed fuzzy search on provides to be deactived by default,
  use --fuzzy for that now (previous behaviour of --fuzzy is kept).
- fixed urpmf --provides, --requires, ...
- added -f to urpmf (as used by urpmq).

* Wed Dec 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-13mdk
- fixed error management about missing files after download.
- fixed urpme dependencies output to be user friendly.

* Wed Dec 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-12mdk
- fix symlink download with wget.
- urpme now print possible errors.

* Tue Dec 10 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-11mdk
- fixed source installation in / when installing dependencies.
- added --install-src to avoid probing on root/user mode.
- fixed no log available when user mode.
- changed obsoleted -c of urpmq to complete output with package
  to removes (needed for parallel distributed urpme).
- allow distribution of local files.
- fixed small typos in urpme.

* Fri Dec  6 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-10mdk
- fixed indexation when using --distrib-XXX for urpmi.addmedia.
- fixed wget output to be far more quietly.

* Fri Dec  6 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-9mdk
- improved urpmf from sh to perl, now a lot of options and
  support of synthesis only media.
- make medium name mandatory when adding a source with
  --distrib-XXX using urpmi.addmedia.
- fix parallel installation when one node is already up-to-date.
- improved callback usage of urpm::configure to use newer
  perl-URPM interface (much faster and smart with memory, but
  unstable).

* Tue Dec  3 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-8mdk
- added --excludepath option (fix bug 577).
- fixed missing options given to parallel plugins.
- fixed missing files not given to user.

* Mon Dec  2 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-7mdk
- fixed rsync:// protocol, now it really works, tested.

* Mon Dec  2 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-6mdk
- fixed mutliple second or more medium being ignored when not
  using a list file.
- fixed problem of package not found when not using list file.
- fixed urpmi --auto.

* Fri Nov 29 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-5mdk
- changed urpmi.addmedia behaviour to use /etc/urpmi/mirror.config
  and allow it to parse urpmi.setup mirror configuration as
  well as Mandrake (old) mirror configuration.
- allow blank url to be given to get all mirror for a given version
  and architecture.

* Fri Nov 29 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-4mdk
- allow urpmi <url> to work with rpm filename with all supported
  protocols (ftp, http, ssh, rsync).
- fixed rsync:// protocol not to use rsync with -e along with
  an rsync server.
- fixed missing list creation update.

* Thu Nov 28 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-3mdk
- added mirrors management for urpmi.addmedia, so added
  --distrib-XXX, --from, --version, --arch options. <url>
  is now just a regex for choosing a mirror, and <name>
  will have an numeric index appended to it.
  anyway for more info, look in the code or guess with
  --help ;-) too late here in Paris ...
- urpmi.addmedia now delete failing media to create.
- added --update option to urpmi.update, guess for what ?

* Thu Nov 28 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-2mdk
- allow creating medium without list file.
- better handling of url without password to be displayed
  in urpmi.cfg.
- fixed remaining list file in partial cache causing bad list file
  generation.

* Wed Nov 27 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.1-1mdk
- fixed checking md5 of rpm files in cache.
- allow rpm files to be downloaded from alternate site.
- allow medium to not use a list file.

* Wed Nov 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-25mdk
- fixed --noclean not really completely noclean.
- avoid possible lost of with_hdlist parameter on some case
  when updating a medium.

* Thu Nov  7 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-24mdk
- fixed still present debug output of urpmq -R.
- fixed bad use of cached list file for file or nfs media.

* Tue Oct 29 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-23mdk
- added MD5SUM file support for downloading hdlist/synthesis.
- added -R option to urpmq to search what may provide packages.

* Thu Oct 24 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-22mdk
- fixed online help of tools to be more consistent.
- added some times missing --help options.
- fixed bad version displayed by urpmq.
- added --list-aliases to list parallel aliases.
- fixed bad rpm in cache by checking only MD5 signature.

* Wed Oct 16 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-21mdk
- fixed bad copy of files when a relative symlink is used.
- added minimal README documentation files for distributed modules.
- fixed urpmi -P with package name already used by provides of
  other package.

* Tue Sep 17 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-20mdk
- gc: fixed curl proxy management.

* Mon Sep 16 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-19mdk
- fixed possible problem with http proxy for wget.
- umount removable device automatically mounted.

* Fri Sep 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-18mdk
- removed apache2-conf from skip.list as it doesn't work
  when trying to install apache2.

* Thu Sep 12 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-17mdk
- fixed possible no clean of distributed module.
- added apache2-conf to skip.list by default.
- fixed gurpmi usability.

* Wed Sep 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-16mdk
- improved ka-run distributed module to copy all files with one
  invocation (newly supported in ka-run-2.0-15mdk).
- daouda: InitialPreference for gurpmi (clicking on a rpm under
          konqueror should launch gurpmi instead of kpackage).

* Fri Sep  6 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-15mdk
- fixed previous fix not correctly fixed.

* Fri Sep  6 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-14mdk
- fixed ka-run distributed module.

* Thu Sep  5 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-13mdk
- simplified --proxy usage (http:// leading now optional).
- fixed --proxy and --proxy-user or urpmq.

* Thu Sep  5 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-12mdk
- fixed bad englist message.
- updated translation.

* Fri Aug 30 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-11mdk
- fixed no post-clean when testing or if errors occured.
- (fcrozat) fixed missing %%post and %%postun for gurpmi, fixed
  bad consolehelper require.

* Fri Aug 30 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-10mdk
- fixed cache management (there could exist some files left in cache
  which were never deleted).
- added default cache management to post-clean (remove files of
  package correctly installed), it is still possible to keep old
  behaviour with "--pre-clean --no-post-clean".
- added --clean options to urpmi to clean cache completely.
- improved urpme to no more use rpm executable.
- (fcrozat) Move gurpmi to /usr/sbin and add consolehelper support for it 
  and register it to handle application/x-rpm mimetype.

* Thu Aug 29 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-9mdk
- added --list-nodes to list nodes used when in parallel mode.
- moved some initialisation for parallel mode to allow user
  execution of --list-nodes.
- updated man pages with newer options.

* Thu Aug 29 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-8mdk
- added --parallel option to urpmq.
- allowed test upgrade in parallel mode.
- improved first choices in parallel mode a little.

* Wed Aug 28 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-7mdk
- added --list-media to urpmq.
- fixed old package not upgraded.

* Tue Aug 27 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-6mdk
- fixed skip.list new format.

* Tue Aug 27 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-5mdk
- fixed urpmq --auto-select disabling its selection.
- open read-only rpmdb when testing installation (--test).
- added reverse media parameter from parallel configuration.
- improved error management of parallel extension module.

* Mon Aug 26 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-4mdk
- english typo fixed.
- improved skip.list contents to provides using sense and regexp
  on package fullname.
- added --test options to urpmi to test installation.
- made --verify-rpm the default (use --no-verify-rpm to avoid).
- fixed command line not seen in log.
- improved parallel module to check installation on all nodes before
  doing it effectively.

* Fri Aug 23 2002 Warly <warly@mandrakesoft.com> 4.0-3mdk
- fix urpme '/' pb

* Fri Aug 23 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-2mdk
- added ssh parallel module extension.
- fixed check of capabilities of distant urpmi.
- fixed wrong installation of extension modules.

* Fri Aug 23 2002 Fran?ois Pons <fpons@mandrakesoft.com> 4.0-1mdk
- added --parallel options for distributed urpmi.
- added urpmi module extensions support (only --parallel).
- added --synthesis options for urpmq/urpmi to use a specific
  environment.
- use cache files even if no medium have been defined (for use
  with --synthesis).

* Tue Aug 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-8mdk
- fixed development log still done for progression status, now
  removed.
- ignore noauto: hdlists flags.

* Mon Aug 12 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-7mdk
- fixed --auto not taken into account for removing or unselecting
  packages in urpmi.
- fixed modified flag ignored in urpmi.cfg (may cause side effects
  as remove media not asked next time urpmi.removemedia is called).
- added --verify-rpm to urpmi in order to check rpm signature.

* Tue Aug  6 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-6mdk
- added --allow-nodeps and --allow-force option to urpmi.
- globing multiple media name select them all instead of error.
- answering no to remove package cause urpmi to exit immediately.
- added support for X for asking user to unselect package or to
  remove package.

* Fri Jul 26 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-5mdk
- fixed man pages typo.
- sorted package to remove list.
- always copy rpm if using supermount on a cdrom (avoid being too slow).

* Thu Jul 25 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-4mdk
- fixed urpmq -u.

* Wed Jul 24 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-3mdk
- added more log.
- use perl-URPM-0.50-4mdk or better for correct generation of
  synthesis file for unresolved provides when packages are
  multiply defined.

* Tue Jul 23 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-2mdk
- updated urpme to use perl-URPM and speed it up (no more
  rpm -e --test ...).
- updated rpm-find-leaves to use perl-URPM.
- dropped build requires to rpmtools (but need rpm >= 4.0.3).

* Tue Jul 23 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.9-1mdk
- updated to use perl-URPM >= 0.50.

* Mon Jul 22 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.8-3mdk
- fixed ldconfig cannot be installed.
- added translation support on error.

* Mon Jul 22 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.8-2mdk
- fixed no dependencies or forced install error.

* Fri Jul 19 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.8-1mdk
- removing, installing and upgrading packages is done in only
  one transaction.
- changed installation progress to look like rpm one.

* Wed Jul 17 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.7-6mdk
- fixed uncatched die, now produce error message.

* Tue Jul 16 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.7-5mdk
- fixed no progression of download.
- fixed bad proxy support on command line.

* Fri Jul 12 2002 Pixel <pixel@mandrakesoft.com> 3.7-4mdk
- fix problem with no proxy

* Thu Jul 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.7-3mdk
- incorporated proxy patch of Andre Duclos <shirka@wanadoo.fr>.
- added tempory error message (before message and translation are
  done).

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 3.7-2mdk
- rebuild for perl 5.8.0

* Mon Jul  8 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.7-1mdk
- added new methods to handle directly installation of package (no
  more rpm binary needed).
- fixed some english typo (thanks to Mark Walker).

* Tue Jul  2 2002 Pixel <pixel@mandrakesoft.com> 3.6-5mdk
- use perl-Locale-gettext instead of perl-gettext
  (ie. Locale::gettext instead of Locale::GetText)

* Fri Jun 28 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.6-4mdk
- increase retry count to 10 instead of 3 for rsync and ssh protocol.
- support prefered tools to download files (grpmi only handles ftp
  and http protocol currently).
- change behaviour of no answered to remove package to simply ignore
  remove instead of exiting.

* Fri Jun 28 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.6-3mdk
- fix deadlock on removing package.
- fix rsync download for mulitples files.

* Thu Jun 27 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.6-2mdk
- added rsync:// and ssh:// protocol to urpmi.

* Thu Jun 27 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.6-1mdk
- removed no more used methods in urpm module.
- make sure absent synthesis force synthesis regeneration.
- add initial support to remove package wich will breaks upgrade
  for urpmi only (ignored in urpmq).

* Thu Jun 20 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-8mdk
- added back version lost for some time (Guillaume Rousse).
- added --list to urpmq to list package.
- added regression test (explicit make test for instance).

* Wed Jun 19 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-7mdk
- fixed urpmq to no more use old resolution methods in urpm.pm.
- fixed urpmq to take care of choices correctly (no default selection).

* Tue Jun 18 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-6mdk
- fixed --bug on required file not provided for generating rpmdb.cz.

* Mon Jun 17 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-5mdk
- fixed urpmi --auto-select with no update and question asked.
- fixed urpmq --auto-select with error on HASH...

* Mon Jun 17 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-4mdk
- fixed urpmq --headers on some cases.

* Thu Jun 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-3mdk
- fixed --auto-select and skip.list.

* Thu Jun 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-2mdk
- added --env option to urpmi to replay bug report.

* Thu Jun 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.5-1mdk
- use perl-URPM >= 0.04-2mdk for new require resolution algorithms.

* Mon Jun 10 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-9mdk
- fixed no output if root.
- use message function as most as possible. (why it wasn't used ?)
- fix message to output more if bug report.
- list of package is LF separated instead of space separated.

* Mon Jun 10 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-8mdk
- added --bug option to report bug report.
- fixed --auto-select and skip.list.

* Fri Jun  7 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-7mdk
- fixed still present log on standard output.

* Fri Jun  7 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-6mdk
- fixed skip.list to skip according provides (even not the best).
- fixed package id 0 always selected (generally ldconfig or lsbdev).

* Wed Jun  5 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-5mdk
- fixed fuzzy search on package (error in urpm.pm around line 1404-1409).

* Wed Jun  5 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-4mdk
- fixed urpmq.
- fixed incomplete requires on some cases.
- fixed reading of rpm files.

* Wed Jun  5 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-3mdk
- avoid sub of sub with different level of variable closure in perl,
  this cause the interpreter to lose its memory usage.

* Wed Jun  5 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-2mdk
- fix rpmdb non closed when traversing it.
- fix ftp and http medium with bad list generation.
- improved urpmi.update to avoid two pass all the time.

* Tue Jun  4 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.4-1mdk
- use URPM perl module instead of rpmtools.

* Thu Apr 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-25mdk
- fixed a problem for searching package according to name when
  nothing should be found but other package are proposed.

* Wed Apr 10 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-24mdk
- fixed package that need to be upgraded but which is provided
  by another package (Mesa and XFree86-libs).

* Wed Apr 10 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-23mdk
- fixed diff_provides on unversioned property not taken into 
  account (libbinutils2 with binutils).
- fixed virtual version only requires against virtual version and
  release provides when resolver try to check release
  (libgtk+-x11-2.0_0-devel with gtk+2.0-backend-devel).

* Mon Mar 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-22mdk
- added --wget/--curl support to urpmq (needed by rpmdrake).

* Thu Mar  7 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-21mdk
- fix --wget and --curl for urpmi.addmedia.

* Thu Mar  7 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-20mdk
- fixed when console has been closed and urpmi ask for changing
  medium (currently it open/eject the device).

* Tue Mar  5 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-19mdk
- fixed parse_synthesis when a the src package is following its
  binary counterpart (overidding its description).

* Mon Mar  4 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-18mdk
- added patch from Andrej Borksenkow modified.

* Thu Feb 28 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-17mdk
- added (undocumented) --root option to urpmi/urpmq to install in a
  given root.
- rebuild with newer po.

* Wed Feb 27 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-16mdk
- fixed possible problem on urpmi update db (perl die workarounded).

* Mon Feb 25 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-15mdk
- fixed not to require Fcntl module (in perl package).
- fixed bad behaviour on src package as user (no message).
- fixed src package listed on package to be installed (which is
  wrong).
- removed kernel-source in inst.list which may breaks on some
  case (workaround).

* Thu Feb 21 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-14mdk
- build package as noarch as there is no more any binary inside.
- fixed urpme to avoid removing base package.

* Thu Feb 21 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-13mdk
- removed staling debug log.
- try to mount a removable device before examining if an available
  device is present.

* Wed Feb 20 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-12mdk
- fixed installing dependancies of given src.rpm filename.
- fixed to keep removable device already mounted before asking
  user to change.

* Tue Feb 19 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-11mdk
- fixed obsoletes on direct requires when a sense is given.
- added a tracking method in urpm library for allowing upgrade.

* Mon Feb 18 2002 Pixel <pixel@mandrakesoft.com> 3.3-10mdk
- remove autoirpm until it's fixed (or used/advertised)

* Mon Feb 18 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-9mdk
- fixed requires resolution regression when old package provides
  property removed by newer (libification).

* Mon Feb 18 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-8mdk
- added missing build requires on rpmtools.
- fixed too verbose erroneous output that may hurt the user.
- fixed reduce_pathname with real url which reduce a bit
  too much.

* Sat Feb 16 2002 Stefan van der Eijk <stefan@eijk.nu> 3.3-7mdk
- BuildRequires

* Thu Feb 14 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-6mdk
- use reduce_pathname even for downloading distant file.
- fixed typo.

* Wed Feb 13 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-5mdk
- fixed source package given on command line in urpmi.
- fixed management of obsoletes in --auto-select.

* Tue Feb 12 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-4mdk
- fixed bad method reference in urpmq (used by rpmdrake).
- fixed urpmq -d behaviour.
- fixed bad signal handler behaviour.

* Tue Feb 12 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-3mdk
- package installed (and not upgraded) are by default using --nodeps
  (typically kernel-source).
- updated man pages.

* Mon Feb 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-2mdk
- fixed multiple mounts of removable device.

* Mon Feb 11 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.3-1mdk
- added --fuzzy as alias to -y (sorry Andrej to be late on this).
- added --src (aliased to -s) to handle src rpm in medium.
- added --noclean (only urpmi) to avoid cleaning the cache of rpm.
- try handling src in medium (there is still weirdness for access
  right, need to be root first and user after).

* Thu Feb  7 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-8mdk
- fixed a requires resolution when a package C is upgraded which
  need a package A with a specific version and release, but a
  package B is already installed providing A with a better version
  and release, in such case urpmi doesn't think it is necessary
  to upgrade A.

* Thu Jan 31 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-7mdk
- fixed regexp in supermount fstab management.
- simply kill urpmi logger which avoid losing 1 second.
- early check of installed package.
- fixed operator comparison when version are equal and operator
  is strict and release is present for conflicts, provides and
  requires tags elements.

* Wed Jan 30 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-6mdk
- fixed some case where removable device are not ejected.

* Tue Jan 29 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-5mdk
- added -y options to urpmi/urpmq to impose fuzzy search.
- cleaned dependancy resolver algorithm.
- fixed package asked to be installed but already installed (rare).
- fixed TERM signal send to itself.

* Mon Jan 28 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-4mdk
- integrated patch for supermount from Andrej Borsenkow.
- fixed --wget (or --curl) not used in urpmi.update.
- try to manage .src.rpm file in a usable way.
- fixed requires resolution on multiple requires with
  sense and without sense informations on the same
  package (menu bug).
- fixed typo in po/fr.po (multiple -f for help page).

* Wed Jan 23 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-3mdk
- fixed possible conflicts management error.
- fixed --mediums for upload of same package in different media.
- changed --mediums to --media but kept --mediums.

* Thu Jan 17 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-2mdk
- added urpm.3 man pages.
- improved urpmi.removemedia (help, added -c flag, noclean headers).

* Wed Jan 16 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.2-1mdk
- fixed bad use of update flag.
- fixed urpmi_rpm-find-leaves to use rpm db directly.
- added --mediums to urpmi/urpmq to select medium explicitely.
- added workaround to make sure synthesis file are built,
  using specific rpmtools-4.0-4mdk and above parsehdlist.
- release 3.2 (urpmi_rpm-find-leaves changes, --mediums flag).

* Wed Jan 16 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-8mdk
- improved dependencies resolution (typically XFree86 newer
  packages).
- removed log on uploading with curl.

* Tue Jan 15 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-7mdk
- manage conflicts for dependencies resolution.
- added conflicts tag and obsoletes tag in synthesis.

* Thu Jan 10 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-6mdk
- fixed distant list file support.
- allow shadow approach of list file, the same list file (global)
  can be used for each intermediate medium, urpmi choose the right
  entry for each medium from the same source.
- added /./ as string marker to probe url, this means the heading
  ./ of find . -name "*.rpm" -print should be kept.

* Wed Jan  9 2002 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-5mdk
- added lock urpmi database features.
- added support for distant list file.

* Thu Dec 20 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-4mdk
- make sure curl fail if http url does not exists.
- added probe for http or ftp hdlist or synthesis when adding
  a medium (-h).
- added probe for synthesis.hdlist2.cz (contrib medium).
- added signal handler when opening rpm database to make sure
  it will be closed on SIGINT or SIGQUIT.
- urpmi use -p by default.
- allow urpmq to download rpm with http or ftp protocol when
  invoked with --headers (fix rpminst behaviour).

* Mon Dec 17 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-3mdk
- fixed choice listing.
- somewhat fixed -p kernel.
- fixed installation of package with naming convention changed to
  make upgrade identical to install (kernel and kernel-source).
- allow not to use parsehdlist during --auto-select (now disabled
  by default)
- fix curl support broken for http files and missing ftp files.

* Fri Dec 14 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-2mdk
- added time conditionnal download to curl interface for both http
  and ftp protocol (so need Date::Manip because urpm library use it
  for ftp as no support in curl).
- updated urpm library version to 3.1.

* Thu Dec 13 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.1-1mdk
- added --distrib flag to urpmi.addmedia to add all media from the
  installation medium.
- fixed update on removable medium (the second to more).
- added probe on name to select media (urpmi.update and urpmi.removemedia).
- added log when adding or removing media.
- release 3.1 (interface change, removed method in urpm library).

* Wed Dec 12 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.0-6mdk
- fixed removable device probe for addition of medium.
- fixed synthesis size checking.
- added log when copying file (nfs).
- removed error when description file is not retrieved successfully.
- added -h option to urpmi.addmedia to probe for synthesis or hdlist.
- modified --force of urpmi.update to behave smootly (given once to
  force copy of file, given twice to force regeneration of hdlist).

* Mon Dec 10 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.0-5mdk
- fixed %%post again.
- added kernel-source in /etc/urpmi/inst.list.

* Fri Dec  7 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.0-4mdk
- fixed in urpmq to handle --headers (needed by rpminst) when
  no hdlist are present.

* Fri Dec  7 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.0-3mdk
- fixed back /etc/urpmi/urpmi.cfg update.
- fixed back synthesis source management.
- fixed extraction of epoch tag for old synthesis.

* Fri Dec  7 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.0-2mdk
- fixed %%post with exit code.
- removing sense data in provides (internally).
- optimized depslist relocation for provides cleaning.
- optimized synthesis parsing.
- make sure /etc/urpmi/urpmi.cfg is written on modification.

* Thu Dec  6 2001 Fran?ois Pons <fpons@mandrakesoft.com> 3.0-1mdk
- 3.0 so urpm library interface change and method removal.
- depslist*, compss, provides are obsoleted, synthesis file
  are now used instead (this will help rpmdrake caching).
- added missing requires on perl for autoirpm.

* Thu Dec  6 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.2-2mdk
- fixed bad reference with -p.
- changed -p ... to use choice instead of mutliple packages.

* Wed Dec  5 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.2-1mdk
- match rpmtools-4.0.
- updated help on-line and fixed options invocation.
- update translation (thierry)

* Thu Nov 29 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.1-7mdk
- fixed -p flag with choices.
- fixed -p kernel which may glob another kernel package.

* Wed Nov 28 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.1-6mdk
- updated requires to webfetch.
- updated requires to last rpmtools needed.

* Wed Nov 28 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.1-5mdk
- fixed URL with trailing slashes.
- added download log.

* Wed Nov 28 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.1-4mdk
- fixed incovation of sync method even when no files to sync.
- fixed urpmq option management (-m|-M equ -du but necessary by default).
- fixed %%preun of autoirpm to check previous installation.
- added small doc in /etc/urpmi/inst.list file.

* Tue Nov 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.1-3mdk
- added curl support (kept wget support).
- updated help for urpmi, urpmi.update and urpmi.addmedia.
- fixed bad check of urpmi.addmedium for existing name.
- avoid some error message if description is missing (not all).
- allow any prefix for url (especially removable://...).

* Tue Nov 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.1-2mdk
- removed old optimization to get existing depslist instead
  of rebuilding it.

* Mon Nov 26 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.1-1mdk
- removed obsoleted code in urpm module.
- ignore -m, -M and -c flag of urpmi/urpmq.
- fixed group display of urpmq.
- added -f for urpmq to display full package name.
- fixed -d of urpmq.
- fixed --auto-select and files of package not obsoleted but
  present in other registered package (no more selected).
- fixed call to grpmi (no more only installation).

* Wed Nov 21 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0-7mdk
- fixed missing urpmi configuration file not read.
- fixed bad output of rpm files to be installed or upgraded.
- fixed bad check of missing rpm files.

* Mon Nov 19 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0-6mdk
- fixed --auto-select and rpm file upload.

* Fri Nov 16 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0-5mdk
- added /etc/urpmi/inst.list support.

* Thu Nov 15 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0-4mdk
- first stable support for updating synthesis file.

* Mon Nov 12 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0-3mdk
- added minimal support for updating synthesis file (untested).
- fixed requires resolution bug (thanks to Borsenkow Andrej).

* Fri Nov  9 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0-2mdk
- added error message if not root.
- fixed some removable device bad regexp (to support new format).
- avoid installing source package (downloaded but ignored).

* Tue Nov  6 2001 Fran?ois Pons <fpons@mandrakesoft.com> 2.0-1mdk
- no more need for removable device selection in URL (autoprobe but need removable://)
  but old description still accepted.
- fix some mount/umount problem.
- improve -m mode speed.
- obsolete -M mode (-M is still recognized on command line but same as -m).
- depslist is no more calculated with dependencies (now optional).
- everything now as 2.0 version.

* Sat Oct 27 2001 Pixel <pixel@mandrakesoft.com> 1.7-15mdk
- fix urpme with i18n (thanks to Andrej Borsenkow)
- fix urpme with regexp-like arguments (mainly things with "++") (thanks to Alexander Skwar)

* Mon Sep 24 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-14mdk
- fixed stale rpm file (filesize set to 0) in urpmi cache.

* Wed Sep 19 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-13mdk
- avoid possible error on trying to remove package.
- avoid error message which are more warning.

* Mon Sep 17 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-12mdk
- fixed urpmq usage of urpm library.

* Tue Sep 11 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-11mdk
- fixed unable to add a ftp or http medium when with_hdlist
  is set to a value without / inside.

* Tue Sep 11 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-10mdk
- fixed error about urpmi saying package already installed.
- fixed wrong propagation of indirect updates (-m mode only).

* Mon Sep 10 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-9mdk
- moved depslist computation out of loop of reading.

* Mon Sep  3 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-8mdk
- updated fr man pages (pablo).
- avoid eject removable medium if --auto is given.
- avoid stat in /dev directory.

* Fri Aug 31 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-7mdk
- added --allow-medium-change to urpmi.
- moved autoirpm french man page to autoirpm package.

* Wed Aug 29 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-6mdk
- fixed multiple asking of same choices.
- possibly fixed array error in resolving choices.
- fixed wrong reference to fr man pages.

* Wed Aug 29 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-5mdk
- rebuild with latest rpm.

* Thu Jul 26 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-4mdk
- fixed tentative to always install package with -m mode.

* Wed Jul 25 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-3mdk
- really fix crazy behaviour of --auto-select.
- fixed local packages install.

* Wed Jul 25 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-2mdk
- fixed crazy behaviour of --auto-select that try to select
  the whole word (no filtering of installed packages).

* Mon Jul 23 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.7-1mdk
- updated to use newer rpmtools 3.1.

* Mon Jul 16 2001 Daouda Lo <daouda@mandrakesoft.com> 1.6-14mdk
- resync with cvs.

* Sat Jul 14 2001  Daouda Lo <daouda@mandrakesoft.com> 1.6-13mdk
- added urpmi logrotate file 
- more macroz

* Thu Jul  5 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-12mdk
- fixed wrong dependencies resolution for local packages
  in minimal mode.
- improved urpmf.
- updated man pages.

* Thu Jul  5 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-11mdk
- take care of local packages.

* Wed Jul  4 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-10mdk
- fixed bad packages installed on some cases.

* Mon Jul  2 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-9mdk
- fixed missing rpmtools reference in urpm library.
- changed die in fatal error.

* Mon Jul  2 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-8mdk
- fixed typo by pixel.
- fixed bad reference in urpm reported by Michael Reinsch.
- fixed dependencies for closure with old packages.
- added --update flag to urpmi.addmedia

* Thu Jun 28 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-7mdk
- added update flag to medium.
- fixed -M algortihms with epoch (serial) uses.

* Wed Jun 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-6mdk
- fix problem interpreting serial.

* Wed Jun 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-5mdk
- take care of epoch (serial) for version comparison.

* Tue Jun 26 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-4mdk
- cleaned source package extraction algorithm.

* Mon Jun 25 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-3mdk
- reworked algorithms to search packages, added -p options to
  urpmi and urpmq.

* Thu Jun 21 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-2mdk
- finished i18n support for urpmi.*media.

* Wed Jun 20 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.6-1mdk
- simplified urpmf.
- fixed typo in %%post.
- fix i18n support and allow l10n of all error message.
- simplified error code of urpmi/urpmq.
- new version.

* Thu Jun 14 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-41mdk
- build release for new rpm.

* Wed May 30 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-40mdk
- avoid including bad rpm filename or with src arch.
- make sure not to reference basesystem if it does not exists.
- fixed --auto to avoid user intervention.

* Tue May 29 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-39mdk
- fixed broken dependancies.

* Wed May 23 2001 Pixel <pixel@mandrakesoft.com> 1.5-38mdk
- really remove all group urpmi

* Wed May 23 2001 Pixel <pixel@mandrakesoft.com> 1.5-37mdk
- removed setuid bit, now stop yelling or go get f*

* Tue May 22 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-36mdk
- fixed warning if src rpm are in repository.

* Tue May 22 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-35mdk
- added synthesis file filtering.
- added arch chekc support.

* Tue Apr 17 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-34mdk
- fixed sorting of list file.

* Tue Apr 17 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-33mdk
- make sure building of synthesis files are done.
- return error if file given are wrong.

* Fri Apr 13 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-32mdk
- fixed typo on urpmf man pages.
- fixed urpmi return exit code of grpmi on error.
- fixed cancel on medium change dialog (gurpmi or --X).

* Tue Apr 10 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-31mdk
- fixed error on .listing file in rpms cache directory.

* Tue Apr 10 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-30mdk
- fixed header clean-up.
- updated man pages.

* Mon Apr  9 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-29mdk
- fixed some missing requires for -m mode.
- fixed bad search with version and release.

* Thu Apr 05 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-28mdk
- updated man pages.
- fixed remove of synthesis file before update.
- fixed remanent rpm file in cache.

* Tue Apr  3 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-27mdk
- added better error management.
- fixed some typo for cache management (creating /partial).

* Tue Mar 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-26mdk
- added --WID=id
- let grpmi make the upload of packages.

* Mon Mar 26 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-25mdk
- sort list file so that rpm are sorted when installed.
- increase speed for --auto-select: implies -M by default.
- added support for retrieving descriptions file.

* Mon Mar 26 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-24mdk
- fixed annoying message when adding a medium (cp).

* Fri Mar 23 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-23mdk
- added synthesis hdlist file support to speed up -m mode.

* Sun Mar 18 2001 Pixel <pixel@mandrakesoft.com> 1.5-22mdk
- fix for gmessage and quotes
- adapt autoirpm.update to new hdlists

* Thu Mar 15 2001 Pixel <pixel@mandrakesoft.com> 1.5-21mdk
- update urpmi_rpm-find-leaves

* Fri Mar  9 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-20mdk
- check whatprovides by examining path too for mode -m.
- fixed incorrect requires/provides association for mode -m.

* Wed Mar  7 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-19mdk
- fixed default -m mode for urpmq.
- added log for getting packages (wget) and installing them.
- avoid asking user if everything is already installed.

* Wed Mar  7 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-18mdk
- fixed last line not printed for rpm output.

* Mon Mar  5 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-17mdk
- fixed ask choices for urpmi -m mode.
- changed default behaviour to abort transaction on error.

* Mon Mar  5 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-16mdk
- make sure to kill sub process that are doing log to
  avoid lock.

* Sat Mar  3 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-15mdk
- urpmi mode set to -m by default.

* Thu Mar  1 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-14mdk
- update with newer rpmtools interface.

* Tue Feb 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-13mdk
- fixed removable cdrom old format extraction.
- fixed bad i18n usage.

* Tue Feb 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-12mdk
- removed use of tee, now forked.

* Tue Feb 27 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-11mdk
- fixed cohabitation of --auto-select and skip list.
- added -m mode for urpmq.
- added --sources flag for urpmq.

* Mon Feb 26 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-10mdk
- fixed auto-select flag to use dependancies resolver after.

* Mon Feb 26 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-9mdk
- fixed big bug of provides files completely read but only
  files should be extracted with no package description.
- added log for depslist computation.

* Fri Feb 23 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-8mdk
- fix --auto-select and skip list.

* Fri Feb 23 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-7mdk
- added /etc/urpmi/skip.list for package that should not
  be upgraded.
- remove -v option of urpmq to match -v as verbose.

* Mon Feb 19 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-6mdk
- fixed urpmq --headers with exotic rpm filename.
- fixed closing using tee (need testing).
- fixed missing dependancies resolution using -m mode.

* Mon Feb 19 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-5mdk
- fixed -m mode for prompting user if needed.
- fixed -m mode with depandancies resolving.
- avoid update urpmi db except if old urpmi.

* Fri Feb 16 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-4mdk
- fixed -m mode with failed depandancies.

* Fri Feb 16 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-3mdk
- added -m flag to urpmi for minimal upgrade.
- fixed urpmq olding approach of local rpm (added --force too
  as in urpmi).
- fixed some i18n usage.

* Wed Feb 14 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-2mdk
- removable medium are not automatically updated now.
- remove need of number removable device when adding a new medium.

* Wed Feb 14 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.5-1mdk
- added --auto-select flag for urpmi and urpmq.
- added --headers flag to urpmq.
- changed help screen for both urpmi and urpmq.

* Mon Feb 05 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.4-7mdk
- fixed wrong probing of medium list file.

* Mon Feb  5 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.4-6mdk
- fixed missing mounting on non removable device like nfs.
- flush STDERR and STDOUT before exiting.

* Tue Jan 30 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.4-5mdk
- added medium change code.
- fixed urpmi with local file.
- changed default option to verbose when invoking rpm.


* Thu Jan 25 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.4-4mdk
- added code to search for source rpms file to install.
- modified manipulation of ignore flag, keep media name unique.
- added missing cache directory in spec file.
- lot of fixes on urpm core library.

* Thu Jan 25 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.4-3mdk
- need rpmtools-2.1-9mdk or above for hdlist building extension.
- introduced cache directory for medium and rpms manipulation.

* Wed Jan 17 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.4-2mdk
- removed PreReq on genbasefiles, now PreReq rpmtools-2.1-8mdk or above.
- fixed glitches in urpm.pm module about old format of urpmi.cfg.

* Tue Jan 16 2001 Fran?ois Pons <fpons@mandrakesoft.com> 1.4-1mdk
- extract urpmi/urpmq common code and newer code for medium
  management in perl module urpm.
- rewrite tools to use the module.

* Mon Nov 27 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-12mdk
- fixed urpmi.addmedia if already added media are no more accessible.

* Thu Nov 16 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-11mdk
- fixed compilation problems.

* Mon Sep 25 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-10mdk
- updated urpme to depslist.ordered.

* Wed Sep 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3-9mdk
- in --auto under X, does not display anymore the sucking interactive dialog
  "everything already installed"

* Wed Sep 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.3-8mdk
- added option --best-output that selects X if available

* Wed Sep 13 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-7mdk
- trusting root only readable file list.*, fixes gurpmi with
  mutlitple media examination.
- removed setuid root on urpmq.

* Tue Sep 05 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-6mdk
- split query mode of urpmi into new tools urpmq.
- fixed -v option of urpmi.
- updated man pages of various tools.

* Sun Sep 03 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-5mdk
- fixed incorporation of media with already defined packages, choose the
  relocated one by rpmtools library.

* Fri Sep 01 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-4mdk
- fixed --auto usage (thanks to Garbage Collector).
- fixed urpmi.addmedia with glob on rpm files only.

* Thu Aug 31 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-3mdk
- Oops, fixed typo in post.

* Tue Aug 31 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-2mdk
- added code to proper upgrade of urpmi 1.2.
- added small correction in urpmi for basesystem selection.
- fixed help invocation (thanks to Bryan Paxton).
- modified urpmf not to use rpmtools-compat.

* Mon Aug 28 2000 Fran?ois Pons <fpons@mandrakesoft.com> 1.3-1mdk
- 1.3 of urpmi.
- use rpmtools perl interface to access hdlist and build requires.

* Sun Aug  6 2000 Pixel <pixel@mandrakesoft.com> 1.2-4mdk
- use %%lang for i18n'd files
- clean /var/lib/urpmi on removal
- urpmi local_file only if local_file ends with .rpm

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 1.2-3mdk
- change versions of autoirpm and gurpmi
- macroization, BM

* Thu Jun 29 2000 Pixel <pixel@mandrakesoft.com> 1.2-1mdk
- nice fixes from diablero (mainly better generation of list.*)

* Tue Jun 13 2000 Pixel <pixel@mandrakesoft.com> 1.1-7mdk
- add require wget (needed for ftp hdlist's)

* Thu May  4 2000 Pixel <pixel@mandrakesoft.com> 1.1-6mdk
- urpmi: unset IFS

* Tue Apr  4 2000 Pixel <pixel@mandrakesoft.com> 1.1-5mdk
- urpmi: add option --force to ignore errors

* Sun Mar 26 2000 Pixel <pixel@mandrakesoft.com> 1.1-4mdk
- autoirpm.update: adapted to new hdlist format

* Sun Mar 26 2000 Pixel <pixel@mandrakesoft.com> 1.1-3mdk
- urpmi can handle package files given on command line. It finds out the
dependencies if possible.
- added rpme (try it, you'll like it!)
- don't try nodeps if file is missing
- new group
- adapted urpmi.addmedia to new hdlist's / multi-cd
- adapted autoirpm.update-all to new rpmlib

* Thu Mar 16 2000 Pixel <pixel@mandrakesoft.com> 1.1-2mdk
- increase version number of gurpmi and autoirpm

* Tue Mar  7 2000 Pixel <pixel@mandrakesoft.com> 1.1-1mdk
- new version, compatible with new DrakX and new rpmtools
- add man page for rpmf

* Mon Feb 28 2000 Pixel <pixel@mandrakesoft.com> 1.0-2mdk
- unset $BASH_ENV

* Sat Feb 12 2000 Pixel <pixel@mandrakesoft.com> 1.0-1mdk
- 1.0
- small urpmi man page change

* Thu Feb 10 2000 Pixel <pixel@mandrakesoft.com> 0.9-40mdk
- unset $ENV to please -U

* Wed Feb  9 2000 Pixel <pixel@mandrakesoft.com> 0.9-39mdk
- now really handle multiple args
- new option ``-a'' to install all the proposed packages
- add ability to --nodeps and --force in case of install errors

* Mon Jan 10 2000 Pixel <pixel@mandrakesoft.com>
- bug fix from Brian J. Murrell

* Fri Jan  7 2000 Pixel <pixel@mandrakesoft.com>
- urpmi: tty question now defaults to yes and acts that way!
- add an example to urpmi.addmedia.8

* Thu Jan  6 2000 Pixel <pixel@mandrakesoft.com>
- urpmi: tty question now defaults to yes (y/N -> N/y)

* Tue Jan  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.9-34mdk
- rpmf: use egrep.

* Tue Jan  4 2000 Pixel <pixel@mandrakesoft.com>
- urpmi.addmedia: replaced hdlist2files by hdlist2names
- rpmf: created 

* Mon Dec 27 1999 Pixel <pixel@mandrakesoft.com>
- fixed a bug in urpmi.addmedia

* Fri Dec 24 1999 Pixel <pixel@mandrakesoft.com>
- more i18n

* Wed Dec 22 1999 Pixel <pixel@mandrakesoft.com>
- added urpmi_rpm-find-leaves

* Mon Dec 20 1999 Pixel <pixel@mandrakesoft.com>
- bug fix in autoirpm.update

* Sun Dec 19 1999 Pixel <pixel@mandrakesoft.com>
- bug fix for autoirpm (bad directory)
- enhancement to urpmi (in place gzip'ing)
- small cute enhancements

* Sat Dec 18 1999 Pixel <pixel@mandrakesoft.com>
- a lot of i18n added (thx2pablo)

* Fri Dec 17 1999 Pixel <pixel@mandrakesoft.com>
- changed a message

* Thu Dec 16 1999 Pixel <pixel@mandrakesoft.com>
- added -follow to the find (thanx2(ti){2})

* Wed Dec 15 1999 Pixel <pixel@mandrakesoft.com>
- fixed a bug in dependencies

* Sat Dec 11 1999 Pixel <pixel@mandrakesoft.com>
- i18n using po-like style

* Wed Dec  8 1999 Pixel <pixel@linux-mandrake.com>
- fixed a bug (gmessage called with no double quotes and i18n)

* Thu Dec  2 1999 Pixel <pixel@linux-mandrake.com>
- better error output (both in /var/log/urpmi.* and stdout/stderr)

* Fri Nov 26 1999 Pixel <pixel@linux-mandrake.com>
- some bug fixes

* Tue Nov 23 1999 Pixel <pixel@linux-mandrake.com>
- include new man pages and doc from camille :)

* Mon Nov 22 1999 Pixel <pixel@mandrakesoft.com>
- s|sbin|bin| in requires (again) (wow already monday!)

* Sun Nov 21 1999 Pixel <pixel@mandrakesoft.com>
- autoirpm: added require gurpmi

* Sat Nov 20 1999 Pixel <pixel@mandrakesoft.com>
- urpmi.addmedia modified

* Wed Nov 17 1999 Pixel <pixel@mandrakesoft.com>
- corrected error in urpmi script
- replaced dependency perl by /usr/bin/suidperl

* Mon Nov 15 1999 Pixel <pixel@linux-mandrake.com>
- changed the handling of urpmi, added urpmi.addmedia...
