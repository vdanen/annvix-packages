%define name	memtest86+
%define version	1.11
%define release	3sls

Summary: 	A stand alone memory test for i386 architecture systems
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Kernel and hardware
URL: 		http://www.memtest.org
Source0: 	http://www.memtest.org/download/memtest_source_v%{version}.tar.bz2
Source1: 	memtest86.pm

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires: 	dev86

Requires: 	initscripts
ExclusiveArch: 	%{ix86}
Obsoletes: 	memtest86
Provides: 	memtest86

%description
Memtest86 is thorough, stand alone memory test for i386 architecture
systems.  BIOS based memory tests are only a quick check and often
missfailures that are detected by Memtest86.    

%prep
%setup -q -n %{name}_v%{version} 

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
* Sun Apr  8 2004 Thomas Backlund <tmb@iki.fi> 1.11-3sls
- first OpenSLS specific build
- tidy spec (vdanen)

* Mon Mar 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.11-2mdk
- Fixed URLs.

* Sat Feb 07 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.11-1mdk
- initial release.
- Obsolete memtest86 (unmaintained)
