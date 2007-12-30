#
# spec file for package lsof
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		lsof
%define version		4.78
%define release		%_revrel

%define dname		%{name}_%{version}

Summary:	Lists files open by processes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Free
Group:		Monitoring
URL:		ftp://vic.cc.purdue.edu/pub/tools/unix/lsof/
Source0:	ftp://vic.cc.purdue.edu/pub/tools/unix/%{name}/%{name}_%{version}.tar.bz2
Patch0:		lsof_4.64-perl-example-fix.patch
Patch1:		lsof_4.60-has-security.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Lsof's name stands for LiSt Open Files, and it does just that. It lists
information about files that are open by the processes running on a UNIX
system.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -c -n %{dname}

#
# Sort out whether this is the wrapped or linux specific tar ball.
#
[ -d %{dname} ] && cd %{dname}
[ -f %{dname}_src.tar ] && tar xf %{dname}_src.tar
[ -d %{dname}.linux -a ! -d %{dname} ] && \
	mv %{dname}.linux %{dname}
[ -d %{dname}_src ] && cd %{dname}_src
%patch0 -p1
%patch1 -p1


%build
[ -d %{dname}/%{dname}_src ] && cd %{dname}/%{dname}_src

LINUX_BASE=/proc
export LINUX_BASE
./Configure -n linux

%make DEBUG="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ -d %{dname}/%{dname}_src ] && cd %{dname}/%{dname}_src
mkdir -p %{buildroot}{%{_sbindir},%{_mandir}/man8}
install -s %{name} %{buildroot}%{_sbindir}
install -m 0644 lsof.8 %{buildroot}%{_mandir}/man8/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%attr(0755,root,kmem) %{_sbindir}/%{name}
%{_mandir}/man8/lsof.8*

%files doc
%defattr(644,root,root,755)
%doc %{dname}/00*


%changelog
* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 4.78
- 4.78

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.77
- 4.77
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.74
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.74
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.74-1avx
- 4.74

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.68-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.68-5avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.68-4avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 4.68-3sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.68-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
