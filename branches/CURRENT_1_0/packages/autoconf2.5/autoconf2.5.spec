%define name	autoconf2.5
%define version	2.57
%define release 7sls
%define epoch	1

# Factorize uses of autoconf libdir home and
# handle only one exception in rpmlint
%define aclibdir %{_prefix}/lib/autoconf

Summary:	A GNU tool for automatically configuring source code.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Development/Other
URL:		http://sourceware.cygnus.com/autoconf/
Source:		ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.bz2
Source2:	special_readme2.5
Source10:	autoconf-site-start
Patch0:		autoconf-2.57-fix-info.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot/
BuildArch:	noarch
BuildRequires:	texinfo

Prereq:		/sbin/install-info
Requires:	gawk, m4, mktemp, /usr/bin/perl
Requires:	%{aclibdir}/ac-wrapper.pl

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your 
source code packages. If you are installing Autoconf, you will also
need to install the GNU m4 package.

Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script; 
Autoconf is only required for the generation of the scripts, not
their use.

%{expand:%(cat %{SOURCE2})}

%prep
%setup -q -n autoconf-%{version}
%patch0 -p0
install -m644 %{SOURCE2} IMPORTANT.README.OpenSLS

%build
%configure2_5x
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f $RPM_BUILD_ROOT%{_infodir}/standards*

for i in autoconf autoheader autoreconf autoscan autoupdate ifnames autom4te; do
		mv $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_bindir}/$i-2.5x
done
# new in 2.5x
ln -s ../..%{aclibdir}/ac-wrapper.pl $RPM_BUILD_ROOT%{_bindir}/autom4te

mv $RPM_BUILD_ROOT%{_infodir}/autoconf.info $RPM_BUILD_ROOT%{_infodir}/autoconf-2.5x.info


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%_install_info autoconf-2.5x.info

%preun
%_remove_install_info autoconf-2.5x.info

%files
%defattr(-,root,root)
%doc README IMPORTANT.README.OpenSLS
%{_bindir}/*
%{_datadir}/autoconf
%{_infodir}/*
%{_mandir}/*/*

%changelog
* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.57-7sls
- remove %%build_opensls macro
- remove emacs files
- more spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.57-6sls
- OpenSLS build
- tidy spec
- use %%build_opensls to remove emacs files

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.57-5mdk
- fix info files packaging

* Fri Apr 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.57-4mdk
- per suggestion of fcrozat, include description info (about the two
  versions of autoconf coexisting) in a readme file

* Thu Dec 19 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.57-3mdk
- fix info coexistance between autoconf and autoconf2.5

* Thu Dec 19 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.57-2mdk
- don't buildrequires on emacs-bin (this is a core package, this is
  not good)
- when emacs-bin would not be here, *.el/elc will not be created, install
  *.el files anyway

* Fri Dec 13 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.57-1mdk
- new version
- add info file

* Wed Oct  9 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.54-1mdk
- new version

* Wed Jul 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.53-3mdk
- Forcibly Requires: ac-wrapper.pl in %{_prefix}/lib/autoconf/

* Thu May  9 2002 Stefan van der Eijk <stefan@eijk.nu> 2.53-2mdk
- BuildRequires: emacs-bin

* Tue Mar 12 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.53-1mdk
- new version (now provides Emacs mode for configure.in, cool ;p)
- mawk patch integrated upstream

* Wed Oct 17 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.52d-1mdk
- bump up to 2.52d with help from Abel Cheung <maddog@linux.org.hk>
- runs through ac-wrapper.pl for transparent co-existance with 2.13
- provide man pages

* Thu Aug 30 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-9mdk
- rebuild to change distribution tag

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 2.13-8mdk
- Use %%_tmppath for BuildRoot

* Mon Oct 16 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-7mdk
- fix for compiling c++ code with gcc-2.96 in some cases

* Thu Aug 24 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-6mdk
- rebuild to fix %preun script (pixel sucks)

* Wed Aug 23 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-5mdk
- automatically added packager tag

* Tue Jul 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-4mdk
- macros for install-info

* Mon Jul 10 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-3mdk
- cleanup and macros

* Fri Mar 31 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-2mdk
- new groups

* Mon Mar  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.13-1mdk
- Back to last 2.13 and stable version, add a serial.

* Wed Oct 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge change of Jeff package.

* Thu May 13 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- 2.14.1

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add patch to help autoconf clean after itself and not leave /tmp clobbered
  with acin.* and acout.* files (can you say annoying?)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)
- use gawk, not mawk

* Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
- moved /usr/lib/autoconf to /usr/share/autoconf (with automake)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.13.

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- requires perl

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- patch for fixing /tmp race conditions

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- spec file cleanups
- made a noarch package
- uses autoconf
- uses install-info

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built with glibc

