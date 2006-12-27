#
# spec file for package time
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		time
%define version		1.7
%define release		%_revrel

Summary:	A GNU utility for monitoring a program's use of system resources
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://www.gnu.org/directory/GNU/time.html
Source:		http://ftp.gnu.org/pub/gnu/time/%{name}-%{version}.tar.bz2
Patch0:		time-1.7.info.patch
Patch1:		time-1.7-ressource.patch
Patch2:		time-1.7-quiet.1.patch
Patch3:		time-1.7-fixinfo.patch 
Patch4:		time-1.7-build.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo
BuildRequires:	automake1.4

Requires(post):	info-install
Requires(preun): info-install

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running and
displays the results.

Time can help developers optimize their programs.

The resources that `time' can report on fall into the general
categories of time, memory, I/O, and IPC calls.

The GNU version can format the output in arbitrary ways by using a 
printf-style format string to include various resource measurements.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p0

export FORCE_AUTOCONF_2_5=1
aclocal-1.4
autoconf
automake-1.4 -a
autoheader


%build
%configure
make LDFLAGS=-s


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files
%defattr(-,root,root)
%{_bindir}/time
%{_infodir}/%{name}.info*


%changelog
* Fri Jun 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7
- drop the docs for such a small package
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7
- BuildRequires: automake1.4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-31avx
- fix requires

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-30avx
- bootstrap build (new gcc, new glibc)

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-29avx
- bootstrap build
- force use of autoconf2.5 and automake-1.4 (peroyvind)
- spec cleanups

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.7-28avx
- require info-install rather than a file
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.7-27sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.7-26sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
