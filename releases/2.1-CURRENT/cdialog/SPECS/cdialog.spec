#
# spec file for package cdialog
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cdialog
%define version		1.1
%define release		%_revrel

%define datetag 	20070930

Summary:	A utility for creating TTY dialog boxes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPLv2+
Group:		Development/Other
URL:		http://invisible-island.net/dialog/
Source:		ftp://invisible-island.net/dialog/dialog-%{version}-%{datetag}.tgz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel

Obsoletes:	dialog
Provides:	dialog

%description
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces.  Dialog is called
from within a shell script.  The following dialog boxes are implemented:
yes/no, menu, input, message, text, info, checklist, radiolist, and
gauge.  


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n dialog-%{version}-%{datetag}


%build
%configure
%make OPTIM="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
%makeinstall \
    BINDIR=%{buildroot}%{_bindir} \
    MANDIR=%{buildroot}%{_mandir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/dialog
%{_mandir}/man1/dialog.1*

%files doc
%defattr(-,root,root)
%doc README samples


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- rebuild against new ncurses

* Wed Oct 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- 1.1-20070930
- correct license

* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- rebuild against new ncurses
- clean spec

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-10avx
- version 0.9b-20040421

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-8avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-7avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.9b-6sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 0.9b-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
