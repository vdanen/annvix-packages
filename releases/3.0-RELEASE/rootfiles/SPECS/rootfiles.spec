#
# spec file for package rootfiles
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rootfiles
%define version		10.2
%define	release		%_revrel

Summary:	The basic required files for the root user's directory
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Base
URL:		http://annvix.org/
Source:		%{name}-%{version}.tar.bz2
Patch0:		rootfiles-9.1-avx-rootwarning.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
The rootfiles package contains basic required files that are placed
in the root user's account.


%prep


%setup -q
%patch0 -p0 -b .warn


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}/root
make install RPM_BUILD_ROOT=%{buildroot}

rm -f %{buildroot}/root/.bash_completion


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) /root/.Xdefaults
%config(noreplace) /root/.bash_logout
%config(noreplace) /root/.bash_profile
%config(noreplace) /root/.bashrc
%config(noreplace) /root/.cshrc
%config(noreplace) /root/.tcshrc
%config(noreplace) /root/.vimrc
%attr(0700,root,root) /root/tmp/


%changelog
* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 10.2
- rebuild

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.2
- rebuild for 2.0
- remove pre-Annvix changelog

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 10.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 10.2-1avx
- mandriva 10.2-2mdk:
  - modernize root's .vimrc
  - clean description
- get rid of bash completion junk

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.1-6avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 9.1-5avx
- bootstrap build

* Mon Jul 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.1-4avx
- update P0 so that if one connects via rsync (where logname is undefined)
  the error doesn't go to STDOUT
- patch policy

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 9.1-3avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 9.1-2sls
- minor spec cleanups
- remove the %%pre backup of Xclients files
- add warning about logging in as root
- remove Changelog doc (no one cares)

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 9.1-1sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
