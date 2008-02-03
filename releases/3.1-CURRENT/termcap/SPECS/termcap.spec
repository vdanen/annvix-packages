#
# spec file for package termcap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		termcap
%define version 	11.0.1
%define release 	%_revrel

Summary:	The terminal feature database used by certain applications
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	none
Group:		System/Libraries
URL:		http://www.catb.org/~esr/terminfo/
Source0:	http://www.ccil.org/~esr/terminfo/termtypes.tc
Patch0:		termcap-linuxlat.patch
Patch1:		termcap-xtermchanges.patch
Patch2:		termcap-utf8.patch
# (fc) 11.0.1-4mdk patch to correctly handle Home/End with X11R6 keycode
Patch3:		termcap-xtermX11R6.patch
# (vdanen) 11.0.1-6mdk patch so Eterm is seen as a color-capable term
Patch4:		termcap-Eterm.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch


%description
The termcap package provides the /etc/termcap file.  /etc/termcap is
a database which defines the capabilities of various terminals and
terminal emulators.  Certain programs use the /etc/termcap file to
access various features of terminals (the bell, colors, and graphics,
etc.).


%prep
%setup -q -T -c %{name}-%{version}
cp %{_sourcedir}/termtypes.tc termcap
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}

install -m 0644 termcap %{buildroot}%{_sysconfdir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/termcap


%changelog
* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1
- drop the sparc conditionals

* Thu Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1
- set the URL

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1
- remove pre-Annvix changelog

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1-15avx
- buildarch is noarch
- spec cleanups (peroyvind)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1-14avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1-13avx
- do the patching and "building" in %%_builddir like a good boy

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1-12avx
- bootstrap build

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 11.0.1-11avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 11.0.1-10sls
- minor spec cleanups

* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 11.0.1-9sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
