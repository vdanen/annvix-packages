#
# spec file for package rpm-rebuilder
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rpm-rebuilder
%define version		0.25
%define release		%_revrel

Summary:	Tools to build/check distributions
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Packaging
URL:		http://www.mandrivalinux.com/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	rpmlint strace rpm-build diffutils

%description
The rpm-rebuilder package contains a set of tools written in bourne
shell, python and perl to rebuild/check large sets of rpm source packages.

check-distrib: checks if a set of source and binary rpms are in sync.

rpm-rebuilder: build a set of rpms from a set of srpms.

compute-build-requires: trace an rpm build command to find the BuildRequires
it needs.

compute-compile-order: from the sets of binary and sources rpms, find the order
in which the source rpms must be recompiled.

rpmbuildupdate: download and rebuild the new version of a given srpm. 


%prep
%setup -q


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install

rm -rf %{buildroot}%{_sysconfdir}/bash_completion.d


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS README README.CVS ChangeLog
%{_bindir}/*
%{_sbindir}/*
%_datadir/rpm-rebuilder


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.25-1avx
- 0.25
- fix perms on spec file
- Requires: diffutils

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.22-1avx
- 0.22

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.21-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.21-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen@mandrakesoft.com> 0.21-1avx
- first Annvix build
- don't include bash completion stuff

* Mon Feb  7 2005 Frederic Lepied <flepied@mandrakesoft.com> 0.21-1mdk
- rpmbuildupdate:
	* new option execafterbuild, to run a script after build the rpm - add the
	  proper credit - version 0.5. (Michael)
	* do not hardcode path ( buchan idea ). (Michael)
	* cleanup usage. (Guillaume Rousse)
	* regexp cleanup. (Guillaume Rousse)
	* don't attempt to download files for simple
	  rebuilds. (Guillaume Rousse)
	* cleanup main function and removed useless options. (Guillaume Rousse)
	* sanitize indentation and args passing. (Guillaume Rousse)
	* --execute option. (Guillaume Rousse)
	* fix bug when %%changelog is present in the spec
	  file. (Michael)
	* use .rpmbuildupdaterc as personal configuration
	  file. (Guillaume Rousse)
	* fix the usage of spec file with a regular path
	  is given.  - add more magic for project hosted on gna and other
	  sourceforgelike sites. (Michael)
	* handle spaces in file names * better logging *
	  install packages individually. 
	* add --rpmoption, to provides options when
	  rebuilding - fix some escaping issue - remove old comment. (Michael)
	* DWIM, ie autodetection of the argument ( if a spec, build from spec, etc ). (Michael)
	* - allow to build from a spec file - add noupdate,
	  to not modify the specfile - allow multiple SRPM dir for --srpms
	  - add berlios.de autodetection - remove some dead code.  (Michael)
	* allows to give a relative path to --src. (Michael)
	* some perl_checker fix - allow to update php code ( no tarball in the spec ). (Michael)
	* do not replace %%{release} if it used in the Release: tag. (Michael)
	* perl_checker fix, remove obsolete construct (
	  &func ) - rebuild the package if no new version is given - add
	  two config file ( /etc/rpmbuildupdate.conf and
	  ~/.rpmbuildupdate.conf ) - add a new mirror to sourceforge ( ovh,
	  france ) - keep prefix (ie plfawarness ) - add a changelog option
	  to use another changelog message - check if options are valid and
	  show help if not - do not use %%packager if not defined. (Michael)
	* use rpm --eval , pterjan idea (Michael)
	* add a test to not try to bzip2 error html pages. (Michael)
	* replace ` and system with perl function.  -
	  replace some regexp by basename.  - remove useless wait ( system
	  already do 'wait', in perl ). (Michael)
	* do a chmod 644 on source tarball before
	  building ( Goetz Waschk idea ) (Michael)
	* better autodetection of sourceforge url. (Michael)
- chrooted-install:
	* added -N option to avoid asking a password for
	  the user.  correct init script to mount what is needed.
- rpm-rebuilder:
	* fix dependencies handling. (Guillaume Rousse)
	* fix 'too many arguments' failure. (Guillaume Rousse)
	* make all sudo call similar. (Guillaume Rousse)
	* fix 'too many arguments' failure. (Guillaume Rousse)
- rpmbuildupdate.bash-completion:
	* also complete on local files. (Guillaume Rousse)
	* options sync. (Guillaume Rousse)
	* new options complete on rpm name. (Guillaume Rousse)
	* first import. (Guillaume Rousse)
- README: document AUTOMAKE_DEP
- rpmold: fix epoch comparisons
- rpmheader: don't use handle signatures
- check-distrib: - check-distrib can now be interrupted with ctrl-C
	         - some factorisation. (Michael)

* Thu May  6 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.20-1mdk
- rpmbuildupdate:
  * fixed rpmmon mode
  * try to detect sources url with Url tag if
    Source not present - some code factorisation (Michael)
  * fixed some regexp causing problems when a
    whitespace is present at the end of the lines for spec files
    variables (Michael)
  * added --log option

* Wed Apr 14 2004 Michael Scherer <misc@mandrake.org> 0.19-1mdk
- add rpmbuildupdate in description
- rpmbuildupdate: 
  * subversion url support
  * https support
  * more robust

* Tue Apr  6 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.18-1mdk
- rpmbuildupdate:
  * added GNOME magic.
  * added -c|--nobuild option to download without building (useful to
    test with the same version).
  * date format in changelog entry compatible with emacs spec mode

* Mon Apr  5 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.17-1mdk
- rpmbuildupdate:
  * correctly handle .gz in redhat package
  * support Release tag not in a macro

* Thu Apr  1 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.16-1mdk
- added rpmbuildupdate

* Thu Mar  4 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.15-1mdk
- handle conflicts better

* Wed Feb  4 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.14-1mdk
- added -U option to chrooted-install to install base-system via the local urpmi
- added rebuild-rpm script

* Mon Oct  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.13-1mdk
- yet more fixes against command line size limitations

* Fri Sep 26 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.12-1mdk
- use doble -g invocation in order to avoid command line size limitations

* Thu Aug  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.11-1mdk
- fix rpmold typos

* Tue Aug  5 2003 Douglas Wilkins <douglasw@mweb.co.za> 0.10-1mdk
- ported check-distrib, rpmheader and rpmold to rpm 4.2, retaining
   backward compatibility
- own /usr/share/rpm-rebuilder (distlint)

* Fri Aug  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9-1mdk
- adapted rpmheader for rpm 4.2

* Tue May  6 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.8-1mdk
- adapted chrooted-install for 9.[12]
- move chrooted-install to /usr/sbin because it needs to be run as root
- ported compute-build-requires to rpm 4.2

* Mon Jan 20 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.7.1-1mdk
- Make sure to reinstall automake-1.4 for MDK version >= 9.0
- Make LOCAL_ARCH default to uname -m, but make sure all x86 arches
  default to "i386" in that case

* Mon Mar  4 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.7-1mdk
- adapted for 8.2

* Fri Oct  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.6-1mdk
- added the missing head-grep.py file
- added -S to run the rpm scriptlets after installing the base system
- added -y to install ypbind and configure it like in the host system
- added -m to use pam_mkhomedir in pam config of sshd

* Tue May  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.5-1mdk
- chrooted-install: install the base rpms with --noscripts and run the
scripts afterward.

* Tue Feb 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.4-1mdk
- corrected compute-build-requires to work with rpm 4.

* Thu Nov 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.3-1mdk
- handle EXCLUDEARCH tag in rpm-rebuilder.

* Thu Oct 26 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.2-1mdk
- added chrooted-install which installs a basesystem in a chrooted environment
and then starts a chrooted ssh daemon on an alternative port.

* Sun Oct  1 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.1-1mdk
- first rpm version.

# rpm-rebuilder.spec ends here
