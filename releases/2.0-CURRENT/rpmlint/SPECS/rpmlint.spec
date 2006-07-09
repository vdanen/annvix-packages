#
# spec file for package rpmlint
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rpmlint
%define version 	0.77
%define release 	%_revrel

Summary:	RPM correctness checker
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://rpmlint.zarb.org/
Source0:	http://rpmlint.zarb.org/download/%{name}-%{version}.tar.bz2
Source1:	rpmlint.annvix.config
Patch0:		rpmlint-0.77-fix-GROUPS.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	python, python-rpm

Requires:	python, python-rpm, binutils, gcc-cpp

%description
Rpmlint is a tool to check common errors on rpm packages.
Binary and source packages can be checked.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0


%build
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpmlint/config

rm -rf %{buildroot}%{_sysconfdir}/bash_completion.d

# temporary fix until upstream gets it right
touch %{buildroot}%{_datadir}/rpmlint/GROUPS


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,0755)
%{_bindir}/*
%{_datadir}/rpmlint
%{_mandir}/man1/rpmlint.1*
%dir %{_sysconfdir}/rpmlint
%config(noreplace) %{_sysconfdir}/rpmlint/config

%files doc
%defattr(-,root,root,0755)
%doc COPYING ChangeLog INSTALL README*


%changelog
* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.77
- P0: rpmlint craps out if /usr/share/doc/rpm-x.y.z/GROUPS doesn't exist so
  make it use a more sane location (/usr/share/rpmlint/GROUPS); upstream has
  been made aware of this
- provide an empty GROUPS file

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.77
- 0.77
- updated config

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.76
- fix buildrequires
- updated config

* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.76
- add -doc subpackage
- rebuild against new python
- updated rpmlint configuration

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.76
- adjust the default groups some more

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.76
- update the config some more to make it a) cleaner and b) adapt
  more to how we handle specs

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.76
- 0.76
- fix requires, buildrequires
- adapt default config to include some of the mandriva exceptions
- setup default policy of allowable group names

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.71
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.71
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.71-1avx
- 0.71

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67-1avx
- 0.67:
  - added obsolete-on-name error: a package sould not obsolete itself, as
    it can cause weird error in tools. (Michael)
  - added exceptions for perl and dyalog on  devel-file-in-non-devel-package.
  - Add a warning for MANIFEST* files in perl modules. (Rafael)
  - add ruby exceptions like perl and python.
  - TagsCheck.py: - added useless-explicit-provides ( check if there is
    2 times the same provides ) (Michael)
  - rpmlint.py: added option -I, to print description of the error
    passed on commandline (Michael)
  - * I18NCheck.py: Added Furlan language code (fur) (Pablo)
  - I18NCheck.py: Added recognition of "pa" (Punjabi) language code (Pablo)
    added some more language codes (Pablo)
  - MenuCheck.py: Fix menu capitalization (Frederic Crozat)
  - MenuCheck.py: Fix missing capitalization
  - Config.py: o added exceptions for kernel-source.* on 
    devel-file-in-non-devel-package reports.
      o cleanup exceptions (Michael Scherer)
      o some code factorisation
      o fix addCheck ( was not useable since it was a tuple instead-f a
        list) (Michael)
  - FilesCheck.py: o added dir-or-file-in-usr-local (Michael Scherer).
      o Minor nit in the regexp that checks that perl module rpms should come
        without the source tarball MANIFEST (Rafael).
  - BinariesCheck.py: allow soname in the form libfoo-X.Y.Z.so too
    (Guillaume Rousse) [bug #12522].
  - NamingPolicyCheck.py: o make exception to the python/perl/ruby/ocaml naming
    policy when the package contains executable (Guillaume Rousse) [bug #12521].
      o  ocaml naming policy (Guillaume Rousse)
  - I18NCheck.py: Don't tag .mo in webapps (Guillaume Rousse) [bug #12186]
  - TagsCheck.py: added summary-ended-with-dot (Guillaume Rousse) [bug #12520]
  - rpmlint.py: exit-n C-c (Michael Scherer)
  - PostCheck.py: doc for postin-without-ghost-file-creation (Pascal Terjan)
  - FilesCheck.py: o Check that pkg-config files and config script are in devel
    packages (Guillaume Rousse, bug #12662).
      o added htaccess-file check (Guillaume Rousse, bug #12661).
      o added executable-marked-as-config-file check.
      o lookup .cmi files as devel files too (Guillaume Rousse) [bug #12186].
  - Config.py: first pass to update load_policy.
  - TagsCheck.py: o added requires-on-release check
      o The Lucent Public Licence (Plan9) is opensource.org-approved. (Rafael)
  - SpecCheck.py: Clarify the use-of-RPM_SOURCE_DIR message explanation. (Rafael)
  - I18NCheck.py: o recognition of some more languages (bug #12216)
      o Added language codes (nr, nso, tn, ts) of South Africa that have efforts
        on creating localizations for them (source: http://www.translate.org.za/ ) (Pablo)
  - MenuCheck.py: added missing-menu-command (Michael Scherer)
  - FilesCheck.py: don't report non-conffile-in-etc on executable.
  - From Ville Skytt:
    - Flag installing files to /var/local as an error.
    - Improved perl temp file regexp.
    - Extended CVS internal file regexp to cover Subversion and GNU Arch.
    - "se" -> "sv" in I18NCheck
    - E:V-R should be consistent in package and changelog regardless if use_epoch i
      set or not.
    - Spelling fixes.
  - exceptions for %%multiarch policy
  - FilesCheck.py: Add a new warning for perl modules installed under site_perl instead
    of vendor_perl (Rafael)
  - FilesCheck.py: Perl modules go under vendor_perl, not site_perl (Rafael)
  - SpecCheck.py: added hardcoded-packager-tag, hardcoded-prefix-tag and
    redundant-prefix-tag checks (Guillaume Rousse, bug #12725).
  - FilesCheck.py: added wrong-script-interpreter, non-executable-script,
    script-without-shellbang, wrong-script-end-of-line-encoding and
    wrong-file-end-of-line-encoding. (Guillaume Rousse, bug #12725).
  - TagsCheck.py: o added the 'Graphical desktop/Xfce' group (bug #13141).
      o added Design Sciences License (Sebastian Savarin)
  - fixed Lucent Public License
  - rpmdiff: filter the provides on name-version-release for the package itself.
  - Pkg.py: Make check_versioned_dep ignore epoch when comparing versions (patch by
    Michael Scherer)
  - Config.py: o do not complain about explicit dependancy on liblua5 (else b/c of buggy
    lua, lua users accepted either lua4 or lua5 thus resulting in linkinkg issues at
    runtime)  (Thierry)
      o update drakconf rule (Thierry)
      o add exceptions for dkms packages

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.59-2avx
- Annvix build

* Mon May 31 2004 Vincent Danen <vdanen@opensls.org> 0.59-1sls
- 0.59
- include a tailored default config

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 0.52-2sls
- OpenSLS build
- tidy spec

* Fri Sep  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.52-1mdk
- TagsCheck.py: o added explicit-lib-dependency check
                o added invalid-build-requires check
- Config.py: o added exceptions for explicit-lib-dependency and
	     o invalid-build-requires do not report errors on debug packages

* Tue Aug  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.51.1-1mdk
- TagsCheck.py: don't check devel-dependency on source packages
- NamingPolicyCheck.py: corrected info reports

* Mon Aug  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.51-1mdk
- TagsCheck.py: added devel-dependency check
                fixed English typo (Pablo)
- SpecCheck.py: allow the following form for a patch instruction:
%%patch -P 1 (request from Stephan Kulow)
- NamingPolicyCheck.py: first version from Michael Scherer
- Pkg.py: in shell_var_value escape the var name to avoid a backtrace (Ville Skyttä)
- Config.py: don't warn on -debug packages (Ville Skyttä)
- InitScriptCheck.py: added init-script-name-with-dot check (Michael Scherer)
- I18NCheck.py: Added 'mn' to list of languages (Pablo)
                Added some more languages (Pablo)


* Thu May  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.50-1mdk
- Ship with rpmdiff
- Add Zope Public License
- Add %%ifarch-applied-patch warning
- Add hardcoded-library-path exceptions
- Add hidden-file-or-dir check (Michael Scherer)
- Fix Epoch tests (Ville Skyttä)

* Tue Apr 29 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.49-1mdk
- added support for rpm 4.2 (Ville Skyttä)
- Spelling fixes, new options: UseEpoch, ValidSrcPerms (Ville Skyttä).
- TagsCheck.py: Handle nosrc packages properly, add required Epoch
functionality (Ville Skyttä).
- SourceCheck.py: Made valid source permissions configurable (Ville Skyttä).
- I18NCheck.py: Fixed Maori ('mi', was wrongly coded as 'ma'), Added
various Indic languages that have Gnome/KDE translations, Added Xhosa
(xh), changed Ganda code lug -> lg (we standardize on two letter
codes) (Pablo)

* Fri Jan 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.48-2mdk
- BinariesCheck.py: Add lib64 paths
- FilesCheck.py: Errour out about outside-libdir-files only if it
  concerns a library package.  This is heuristically determined on the
  package name as '^(lib|.+-libs)'.

* Fri Jan 17 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.48-1mdk
 o rpmlint.py: added a way to load an alternative config file (using -f).
 o SpecCheck.py: * added lib-package-without-%%mklibname
                 * don't parse changelog section to find errors and
                 correct source_dir_regex.
 o FilesCheck.py: added outside-libdir-files
 o I18NCheck.py: * Added 'en_US' as valid locale name
                 * Added "lug" (Luganda) language as a valid code for
                 translations
                 * Added recognition of some more language codes
                 (Gnome includes some translations in those languages now)
 o various exceptions

* Thu Aug  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.47-1mdk
 o BinariesCheck.py: added /usr/lib/bonobo to no binary in /usr/lib exceptions
                     corrected wrong loop for /usr/lib check
 o Config.py: added handling of default values.
 o FHSCheck.py: Add lib64 as standard subdir in /usr (that's the /lib<qual> part of FHS)
 o FilesCheck.py: Add lib64 directories
                  use default values from Config.
 o I18NCheck.py: Added 'zh_HK' recognition
 o InitScriptCheck.py: allow to add/del service with rpm-helper scripts.
 o MenuCheck.py: add default values from Config.
 o PostCheck.py: added perl to dangerous command check trigger scripts too
                 check rpm-helper prereq.
                 corrected prereq test
 o SpecCheck.py: Also check for \{?_prefix}?/lib references

* Tue Jun  4 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.46-1mdk
 o BinariesCheck.py: added no-binary and only-non-binary-in-usr-lib

* Mon Jun  3 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.45-1mdk
 o SpecCheck.py: - Add configure-without-libdir-spec check
	         - Add hardcoded-library-path check

* Wed May 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.44-1mdk
 o added non-ghost-file check
 o added non-root-user-log-file and non-root-group-log-file.

* Wed May  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.43-1mdk
 o added no-prereq-on check.

 o check that the package tags are coherent with the file name.

 o added a --policy option.

 o build only one regexp for all exception and correct the broken ones.

* Fri Mar  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.42-2mdk
- corrected rpmdiff location

* Sun Mar  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.42-1mdk
 o  FilesCheck.py: allow perl and python dependencies to be on
perl-base and python-base. Manage Mandrake perl versionning.

 o I18NCheck.py: Added 'mt' to recognized locales

 o various exceptions.

* Sat Feb  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.41-1mdk
 o SpecCheck.py: report missing %clean section.

 o FilesCheck.py: check dependency on the right version of the
interpreter for python and perl modules.

 o various exceptions.

* Thu Jan 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.40-1mdk

 o MenuCheck.py: new check: invalid-menu-icon-type

 o TagsCheck.py: added libsafe.so as an invalid Requires.

 o sync with setup 2.2.0-18mdk (Chmouel).

 o various exceptions.

 o build the package in a way that rpm -V doesn't report warnings.

* Fri Nov 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.39-2mdk

 o BinariesCheck.py: search references to home or tmp in /usr/lib/pkgconfig/ files.

 o FilesCheck.py: .nosearch files are allowed to have a zero length.

 o Config.py: added some exceptions.

* Sun Nov 25 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.39-1mdk

 o TagsCheck.py: Corrected regexp to check devel provides.
                 Added the new check invalid-dependency.

 o InitScriptCheck.py: Added incoherent-init-script-name check.
	               Expand shell variable in incoherent-subsys check.

 o FilesCheck.py: Use list imported from the setup package for users
   and groups (from setuplist.py).

 o PostCheck.py: Don't print error about percent if post-script has a
                 %%. (Chmouel)
	         Check that RPM_BUILD_ROOT or RPM_BUILD_DIR isn't
	         used.

 o SpecCheck.py: Check also %_sourcedir.
                 Check that the BuildRoot tag doesn't contain a
                 hardcoded path.

 o BinariesCheck.py: Check if .la files contain tmp or home
   references.

* Tue Oct 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.38-1mdk

 o BinariesCheck.py: check that major version is present in package
name.

 o FilesCheck.py: check that regular files haven't a zero size.

 o I18NCheck.py: only check binary packages.

 o SpecCheck.py: don't allow space before tag name.

 o TagsCheck.py: * allow space after the release in a changelog entry.
                 * updated list of licenses from opensource.org and added non
                 opensource ones.
                * report a warning if no url tag is defined.

 o Config.py: various exceptions.

 o SourceCheck.py: correct boolean expression for strange-permission


* Tue Oct 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.37-1mdk

 o SourceCheck.py: allow 0755 as a valid mode for source.

 o Config.py: various exceptions

 o TagsCheck.py: added invalid-word check in description and summary.
                 added invalid-buildhost check.

 o FilesCheck.py: added .cvsignore to the list of cvs-internal-file.

 o BinariesCheck.py: check for new style of pic sections.

 o FilesCheck.py: Check if kernel modules are in the kernel package. (Chmouel)

 o PostCheck.py: track command with full path too.

 o FilesCheck.py: added squid group and user.

 o BinariesCheck.py: Warn for man pages without version in library packages.

 o DistributionCheck.py: More explicit path regexp check for info files. (Chmouel)


* Fri Sep 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.36-1mdk

- MenuCheck.py: check if a menu file is executable.

- rpmlint.py: added -n/--noexception option to display all the errors/warnings
without exceptions from Config.

- TagsCheck.py: added the bugzilla https address as a valid one.

- PostCheck.py: o ghost-files-without-postun => ghost-files-without-postin
		o check if /tmp or /var/tmp is used.
		o check if update-menus is called without a menu file.

- FilesCheck.py: added /etc/logrotate.d entry check.

- Config.py: various exceptions

* Tue Aug 21 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.35-1mdk

- BinariesCheck.py: o Make libraries not linked against libc errors
  and not warnings. (Bill Nottingham)

                    o libc doesn't need to be linked against libc,
  and the dynamic linker doesn't need dependeny information. (Bill Nottingham)

	            o Fix some of the library checks to be more correct. (Bill
  Nottingham)

- TagsCheck.py: added a check on obsoleted packages not provided.

- FilesCheck.py: check non readable files.

- PostCheck.py: check ~/ instead of ~ to allow awk scripts not to
  give false reports.

- MenuCheck.py: o added a check for / in menu titles.

                o Add missing menu entries. (FredC)

- I18NCheck.py: Added 'bs' as a valid language code name. (Pablo)

- Config.py: added a few exceptions.

* Sun Jul 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.34-1mdk
- added missing descriptions.
- added -a option to check all the installed packages.
- TagsCheck.py: handle the libbzip2_1-devel case.

* Fri Jul  6 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.33-2mdk
- Added descriptions for the -i option.

* Mon Jul  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.33-1mdk
- more descriptions from Christian Belisle.

- BinariesCheck.py: new check for files which can cause upgrade
 problems in the library packages.

- TagsCheck.py: try to check alpha/beta/pre version improper use.

- Filter.py: print description only if they aren't empty.

- SpecCheck.py: added a check for obsolete tags.

- FilesCheck.py: added named user and group to the exception list.

* Mon Jun 18 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.32-2mdk
- Added descriptions for the -i option.

* Wed Jun 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.32-1mdk
- rpmlint.py: o If the file given on the command line doesn't exist,
               try to use the name as an installed package to check.
              o new -i option to give explanation on the errors/warnings (not too much
               descriptions have been added ;-)

- MenuCheck.py: added new Office sub menus.

- FilesCheck.py: o added /usr/X11R6/man subdirs to the list of
	          STANDARD_DIRS.
	         o warn for .so file only if they are in a lib dir.
                 o warn for source files in a non devel package only if they are not
                  doc files.

- TagsCheck.py: corrected description-line-too-long check.

- FilesCheck.py: add the rpm user and group per request of Jeff
	         Johnson for the future version of rpm.

* Fri May 18 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.31-1mdk
- PostCheck.py: check that a script isn't only one command.
                check postin and prein instead of postun and preun
	        for ghost files creation.

- MenuCheck.py: don't check NO_XALF in menu command.

- FilesCheck.py: Add rpcuser.

- Config.py: Expections for ldconfig, initscripts, netkit-base and iputils.

- TagsCheck.py: check length of summary and description lines.

* Fri Feb 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.30-1mdk

- InitScriptCheck.py: check if runlevels are set

- MenuCheck.py: added support to check launchers.

- I18NCheck.py: check subdirs of /sur/share/man.

- PostCheck.py: check that the postun creates the ghost files
                added install to dangerous commands

- LSBCheck.py: first version

- TagsCheck.py: changed Window Maker to WindowMaker
                Add https as valid url.
                Used list of licenses from www.opensource.org/licenses
                Check the full license before splitting in it
                multiple parts.


* Thu Dec  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.29-1mdk

- PostCheck.py: Add /sbin/sash as VALID_SHELLS.

- Config.py: added exceptions for dev.

- FilesCheck.py: check dangling-symlink in the file index too to
avoid missing special files that aren't created when extracted as a
user.

- FilesCheck.py: added a generic way to avoid dangling-symlink
warnings.

- TagsCheck.py: for devel packages, check dependency on lib package
only when a .so file is present.

- Config.py: add some execptions for pam (0750 dir for /etc/default
is normal as weel to have gpasswd and chage as suid).

- Config.py: Don't check info-file-with-install-info for bash since
it's by default in the dir file.

* Fri Nov 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.28-1mdk
- TagsCheck.py: o check -devel package naming scheme only on binary
                packages.
                o report a warning if a -devel package comes with no
                major in its name.
                o added python licence and public domain.
                o check syntax of url tag.

- SourceCheck.py: only check compression on tar or diff files.

- Config.py: various exceptions added.

- BinariesCheck.py: o report the file location on objdump errors. 
                    o new error: executable in library package.

- I18NCheck.py: fuzzy check on packages without dependency on
locales

- FilesCheck.py: check if a package provides sources.

- PostCheck.py: force a separator before dangerous command.


* Mon Nov 13 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.27-1mdk
- FilesCheck.py: don't warn if a games is setgid games.
- README: RpmGamesGroup added to the list of available options.
- Config.py: added exception for xman.
- BinariesCheck.py: check ldconfig symlinks.
- TagsCheck.py: don't check no-version-in-changelog for source rpm.

* Fri Nov 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.26-1mdk

- Config.py: added various exceptions.

- TagsCheck.py: o allow multiple licenses.
                o don't report anymore the package-provides-itself warning because
                it's the default in rpm 4.
                o try to not report incoherent-version-in-changelog for sub-packages.

- MenuCheck.py: correct the non-transparent-xpm check.

- FilesCheck.py: don't report buggy length-symlink anymore.

* Thu Oct 12 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.25-1mdk

- Config.py: added exception for sympa, rpm and bcast.

- TagsCheck.py: o check that devel package depends on the base
                  package with the same version.
                o check that summary begins with a

- PostCheck.py: o check dangerous commands.
                ocheck reference to ~ or $HOME.

- MenuCheck.py: o check that titles and longtitles begin by a capital
                  letter.
                o check that no version is included in title and longtitle.
                o /lib/cpp errors to /dev/null for new cpp.

- FilesCheck.py: check package owning system dirs.

- SpecCheck.py: o new check.
                o check name of spec file.
                o check use of $RPM_SOURCE_DIR.
                o warn if a patch is not applied.

* Mon Oct  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.24-1mdk
- FilesCheck.py: added apache and postgres to standard groups.
- TagsCheck.py: spell check a la Debian.

* Fri Sep 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.23-1mdk
- MenuCheck.py: added Applications/Accessibility.
                check that menu	files are readable by everyone.
- Config.py: removed exception for /home.
             added exceptions for vixie-cron.
- FilesCheck.py: check cvs internal files.

* Tue Sep 12 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.22-1mdk
- PostCheck.py: print a warning on empty script.
- FilesCheck.py: added postgres and apache to default users.
- TagsCheck.py: added bugs@linux-mandrake.com as a valid packager address.
- I18NCheck.py: check *.mo for file-not-in-%lang, not only in /usr/share/locale
- TagsCheck.py, MenuCheck.py: replaced Networking/ICQ group with Networking/Instant messaging.

* Thu Aug 31 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.21-1mdk
- TagsCheck.py: check packager field compliance to a regexp.
- Config.py: imported default exceptions.
- TagsCheck.py: added Apache License, PHP Licence and BSD-Style.
- MenuCheck.py: check hardcoded path in icon field and large, mini, 
  normal icon files.
- PostCheck.py: Fix typo in check of /usr/bin/perl.
- PostCheck.py: Check perl script like we do for bash script.
- I18NCheck.py: updated locales list
- FilesCheck.py: Only check perl_temp_file in a /perl/ directory.

* Fri Aug 25 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.20-1mdk
- InitScriptCheck.py: new check for /etc/rc.d/init.d scripts.
- PostCheck.py: check when a script is present that the shell is valid.
- ConfigCheck.py: report warnings for app-defaults only
in /usr/X11R6/lib/X11/app-defaults.
- BinariesCheck.py: report the rpath warning if the directory isn't a
sub-directory of /usr/lib/.

* Fri Aug 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.19-1mdk
- BinariesCheck.py: check rpath only on system lib paths (ie /lib,
/usr/lib and /usr/X11R6/lib).  This can be configured with the
SystemLibPaths option.
- I18NCheck.py: warn if .mo is not registered in %%lang.
- MenuCheck.py: protected kdesu check.
- FilesCheck.py: check perl temporary files.
- rpmlint.py: added ExtractDir option usable in the config
file.
- PostCheck.py: check ] in if statement.  report warning for a
percent.

* Thu Aug 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.18-1mdk
- TagsCheck: check licence file.
- ConfigCheck: check files without no-replace flag.
- MenuCheck: allow depency on kdesu to point directly to /usr/bin/kdesu.
- FHSCheck: allow ftp and www in var (from upcoming FHS 2.2).

* Tue Aug  8 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.17-1mdk
- PostCheck: check bourne shell syntax (Chmouel).
- FileCheck: o check chkconfig calls for packages with a file in
             /etc/rc.d/init.d.
             o allow the call to install-info to be in %%preun.
- MenuCheck: o take care of kdesu (Chmouel).
- various exceptions added.

* Wed Jul 19 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.16-1mdk
- FHSCheck activated by default.
- FileCheck: o check dangling symlinks.
             o check info/dir.

* Tue Jun 27 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.15-1mdk
- 0.15:
 o check non transparent pixmaps in icon path
 o added a check for soname
 o added a warning for packages that provide themselves (for Pixel)
 o corrected check for needs in menu files.
 o various exceptions added.

* Mon Apr 17 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.14-1mdk
- 0.14:
 o MenuCheck: check old entries from KDE and GNOME and allow entries
for sections.
 o config: exceptions for urpmi, sash, octave, ghc, procmail, rsh.
 o extract temp files in <tmppath>/<pkgname>.<pid>

* Mon Apr 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.13-1mdk
- 0.13:
 o MenuCheck: issue a warning if no icon specified (Chmouel).
              corrected list of correct sections (Chmouel).
 o FilesCheck: check ldconfig calls in %%post and %%postun if the package
provide a library.
 o config: new exceptions added.
 o BinariesCheck: check non sparc32 binaries in sparc packages.

* Fri Mar 31 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.12-1mdk
- 0.12:
 o MenuCheck: check binaries launched by menus and
              check update-menus %%post and %%postun.
 o BinariesCheck: check for non sparc32 binaries in sparc rpms.

* Mon Mar 27 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.11-1mdk
- 0.11:
 o check menu files.

* Tue Mar 14 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.10-1mdk
- 1.10:
 o check .h, .a and .so in non devel package.
 o check files in /home.
 o corrected lists of groups.

* Mon Feb 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.2-1mdk
- added a dependency on rpm-python.
- corrected rpm 3.0.4 support.

* Wed Feb 23 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.1-1mdk
- updated to support the way rpm 3.0.4 stores file names.

* Thu Feb 10 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9-1mdk

- 0.9: * gpg support.
       * check release extension.
       * check non executable in bin directories.
       * new options: ValidGroups, ReleaseExtension and
	UseVersionInChangelog.

* Thu Dec 30 1999 Frederic Lepied <flepied@mandrakesoft.com> 0.8-1mdk

- 0.8: I18N checks, some exceptions added.

* Mon Nov 15 1999 Frederic Lepied <flepied@mandrakesoft.com>

- 0.7: more robust cleanup, filters are regexp now and added
exception for /var/catman subirs beeing setgid.

* Sat Oct 23 1999 Frederic Lepied <flepied@mandrakesoft.com>

- 0.6.1: corrected compilation step.

* Sat Oct 23 1999 Frederic Lepied <flepied@mandrakesoft.com>

- 0.6: filter output, documentation checks.

* Fri Oct 15 1999 Frederic Lepied <flepied@mandrakesoft.com>

- 0.5: FHS check, configuration files.

* Fri Oct  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add Doc.

* Thu Oct  7 1999 Frederic Lepied <flepied@mandrakesoft.com>

- version 0.4: pgp check and group name check.

* Wed Oct  6 1999 Frederic Lepied <flepied@mandrakesoft.com>

- version 0.3.

* Mon Oct  4 1999 Frederic Lepied <flepied@mandrakesoft.com>

- version 0.2.

* Fri Oct  1 1999 Frederic Lepied <flepied@mandrakesoft.com>

- First spec file for Mandrake distribution.

# rpmlint.spec ends here
