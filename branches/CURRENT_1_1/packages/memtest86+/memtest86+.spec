%define name	memtest86+
%define version	1.15
%define release	2avx

Summary: 	A stand alone memory test for i386 architecture systems
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Kernel and hardware
URL: 		http://www.memtest.org
Source0: 	http://www.memtest.org/download/memtest_source_v%{version}.tar.bz2
Source1: 	memtest86.pm
Patch0:		memtest86-1.15-avx-nostack.patch.bz2

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires: 	dev86

Requires: 	initscripts
ExclusiveArch: 	%{ix86} x86_64
Obsoletes: 	memtest86
Provides: 	memtest86

%description
Memtest86 is thorough, stand alone memory test for i386 architecture
systems.  BIOS based memory tests are only a quick check and often
missfailures that are detected by Memtest86.    

%prep
%setup -q -n %{name}_v%{version} 
%patch0 -p0

%build
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/boot
install -m 644 memtest.bin %{buildroot}/boot/memtest-%{version}.bin
mkdir -p %{buildroot}%{_datadir}/loader/
install -m755 %{SOURCE1} %{buildroot}%{_datadir}/loader/memtest86

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post 
%{_datadir}/loader/memtest86 %{version}

%preun
%{_datadir}/loader/memtest86 -r %{version}

%files
%defattr(-,root,root)
%doc README
%dir %{_datadir}/loader
/boot/memtest-%{version}.bin
%{_datadir}/loader/memtest86

%changelog
* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 1.15-2avx
- rebuild
- P0: don't build with stack protection

* Sat Jun 19 2004 Thomas Backlund <tmb@annvix.org> 1.15-1avx
- 1.15
- swith to new name: Annvix / avx

* Sun Apr  8 2004 Thomas Backlund <tmb@iki.fi> 1.11-3sls
- first OpenSLS specific build
- tidy spec (vdanen)

* Mon Mar 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.11-2mdk
- Fixed URLs.

* Sat Feb 07 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.11-1mdk
- initial release.
- Obsolete memtest86 (unmaintained)
