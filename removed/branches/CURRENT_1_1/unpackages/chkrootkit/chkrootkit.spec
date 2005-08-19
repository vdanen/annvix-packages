#
# spec file for package chkrootkit
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		chkrootkit
%define version		0.43
%define release		5avx

%define build_diet 	1

Summary:	Checks system for rootkits
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Monitoring
URL:		http://www.chkrootkit.org/
Source0:	ftp://ftp.pangeia.com.br/pub/seg/pac/%{name}-%{version}.tar.gz
Patch0:		chkrootkit-0.43-lib-path.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  glibc-static-devel

Requires:	binutils, fileutils, findutils, gawk, grep, net-tools, procps, sed, sh-utils, textutils
%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.20-1mdk
%endif

%description
Chkrootkit is a tool to locally check for signs of a rootkit.


%prep
%setup -q
%patch -p0 -b .lib-path


%build
%if %{build_diet}
# OE: use the power of dietlibc
make CC="diet gcc" CFLAGS="-DHAVE_LASTLOG_H -DLASTLOG_FILENAME='\"/var/log/lastlog\"' -DWTEMP_FILENAME='\"/var/log/wtmp\"' -Os  -s -static" LDFLAGS=-static
%else
make CFLAGS="-DHAVE_LASTLOG_H -DLASTLOG_FILENAME='\"/var/log/lastlog\"' -DWTEMP_FILENAME='\"/var/log/wtmp\"'" LDFLAGS=-static
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_prefix}/lib/%{name}

install -m 0755 chkrootkit %{buildroot}%{_sbindir}/
install -m 0755 check_wtmpx chklastlog chkproc chkwtmp ifpromisc %{buildroot}%{_prefix}/lib/%{name}/
install -m 0755 strings-static %{buildroot}%{_prefix}/lib/%{name}/strings


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README* COPYRIGHT
%{_sbindir}/*
%{_prefix}/lib/%{name}


%changelog
* Fri Aug 19 2005 Vincent Danen <vdanen@annvix.org> 0.43-5avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 0.43-4avx
- rebuild

* Fri Feb 04 2005 Vincent Danen <vdanen@annvix.org> 0.43-3avx
- rebuild against new dietlibc

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 0.43-2avx
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 0.43-1sls
- 0.43
- rediff P0
- make it amd64 friendly and just use /usr/lib rather than %%{_libdir}

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.42b-3sls
- remove the --with diet stuff because it's redundant
- remove %%prefix
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.42b-2sls
- OpenSLS build
- tidy spec

* Sat Dec  6 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.42b-1mdk
- rediff patch0
- 0.42b

* Tue Jul 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.41-1mdk
- 0.41
- added rediffed patch by David Coe, thanks man!
- build statically against dietlibc per default (mr. lint hates this...)
- misc spec file fixes

* Sat Apr 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.40-1mdk
- 0.40
- use spec file magic to enable builds against dietlibc

* Fri Jan 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.39-1mdk
- 0.39
- rediff P0

* Mon Jan 27 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.38-2mdk
- build release

* Sun Dec 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.38-1mdk
- new version

* Wed Sep 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.37-1mdk
- new version
- rediff
- misc spec file fixes

* Thu Jul  4 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.36-1mdk
- new version
- added md5 file (S1)

* Mon Jan 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.35-1mdk
- 0.35

* Wed May  9 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.32-1mdk
- first version.

# end of file
