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
%define version 	0.81
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
Patch0:		rpmlint-0.78-avx-fix-GROUPS.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python-rpm

Requires:	python
Requires:	python-rpm
Requires:	binutils
Requires:	gcc-cpp

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
install -m 0644 %{_sourcedir}/rpmlint.annvix.config %{buildroot}%{_sysconfdir}/rpmlint/config

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
* Mon Oct 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.81
- 0.81
- updated config

* Tue May 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.80
- 0.80
- updated config

* Mon Oct 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.78
- 0.78
- update P0 (the old P0 was submitted upstream, not sure why it wasn't
  fixed there)

* Fri Sep 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.77
- updated rpmlint config
- spec cleanups

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
