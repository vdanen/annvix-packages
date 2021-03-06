#
# spec file for package memtest86+
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		memtest86+
%define version		1.60
%define release		1avx

Summary: 	A stand alone memory test for i386 architecture systems
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Kernel and hardware
URL: 		http://www.memtest.org
Source0: 	http://www.memtest.org/download/%{version}/%{name}-%{version}.tar.bz2
Patch0:		memtest86-1.15-avx-nostack.patch.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires: 	dev86

Requires: 	initscripts
Requires(post):	bootloader-utils >= 1.6-12avx
Requires(preun): bootloader-utils >= 1.6-12avx
ExclusiveArch: 	%{ix86} x86_64
Obsoletes: 	memtest86
Provides: 	memtest86

%description
Memtest86 is thorough, stand alone memory test for i386 architecture
systems.  BIOS based memory tests are only a quick check and often
missfailures that are detected by Memtest86.    


%prep
%setup -q
# don't apply the patch to disable SSP when we're not using it
#%patch0 -p0


%build
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/boot
install -m 0644 memtest.bin %{buildroot}/boot/memtest-%{version}.bin


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
/usr/share/loader/memtest86 %{version}

%preun
/usr/share/loader/memtest86 -r %{version}


%files
%defattr(-,root,root)
%doc README
/boot/memtest-%{version}.bin


%changelog
* Sat Sep 17 2005 Vincent Danen <vdanen@annvix.org> 1.60-1avx
- 1.60
- the memtest86 bootloader stuff is now in bootloader-utils so
  we need to require it

* Wed Aug 17 2005 Vincent Danen <vdanen@annvix.org> 1.15-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 1.15-2avx
- rebuild
- P0: don't build with stack protection

* Sat Jun 19 2004 Thomas Backlund <tmb@annvix.org> 1.15-1avx
- 1.15
- swith to new name: Annvix / avx

* Sun Apr  8 2004 Thomas Backlund <tmb@iki.fi> 1.11-3sls
- first OpenSLS specific build
- tidy spec (vdanen)

* Mon Mar 01 2004 Giuseppe Ghib? <ghibo@mandrakesoft.com> 1.11-2mdk
- Fixed URLs.

* Sat Feb 07 2004 Giuseppe Ghib? <ghibo@mandrakesoft.com> 1.11-1mdk
- initial release.
- Obsolete memtest86 (unmaintained)
