# OE: conditional switches
#(ie. use with rpm --rebuild):
#	--with diet	Compile chkrootkit against dietlibc

%define build_diet 1

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

%define name	chkrootkit
%define version	0.42b
%define release	1mdk

Summary:	Check rootkits
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.pangeia.com.br/pub/seg/pac/%{name}-%{version}.tar.bz2
Patch0:		chkrootkit-0.42b-lib-path.patch.bz2
URL:		http://www.chkrootkit.org/
License:	BSD
Group:		Monitoring
Requires:	binutils, fileutils, findutils, gawk, grep, net-tools, procps, sed, sh-utils, textutils
BuildRequires:  glibc-static-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot
Prefix:		%{_prefix}

%if %{build_diet}
BuildRequires:	dietlibc-devel >= 0.20-1mdk
%endif

%description
Chkrootkit is a tool to locally check for signs of a rootkit.

%prep

%setup -q
%patch -p1 -b .lib-path

%build

%if %{build_diet}
# OE: use the power of dietlibc
make CC="diet gcc" CFLAGS="-DHAVE_LASTLOG_H -DLASTLOG_FILENAME='\"/var/log/lastlog\"' -DWTEMP_FILENAME='\"/var/log/wtmp\"' -Os  -s -static" LDFLAGS=-static
%else
make CFLAGS="-DHAVE_LASTLOG_H -DLASTLOG_FILENAME='\"/var/log/lastlog\"' -DWTEMP_FILENAME='\"/var/log/wtmp\"'" LDFLAGS=-static
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}/%{name}

install chkrootkit %{buildroot}%{_sbindir}/
install check_wtmpx chklastlog chkproc chkwtmp ifpromisc strings %{buildroot}%{_libdir}/%{name}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README* COPYRIGHT
%{_sbindir}/*
%{_libdir}/%{name}

%changelog
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
