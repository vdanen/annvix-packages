#
# spec file for package dmidecode
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		dmidecode
%define version 	2.3
%define release 	4avx

Summary:	Tool for dumping a computer's DMI table contents
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.nongnu.org/dmidecode/
Source0:	http://www.nongnu.org/dmidecode/download/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

PreReq:		rpm-helper

%description
Dmidecode is a tool for dumping a computer's DMI (some say SMBIOS) table
contents in a human-readable format. This table contains a description of the
system's hardware components, as well as other useful pieces of information
such as serial numbers and BIOS revision. Part of its code can be found in
the Linux kernel, because DMI data may be used to enable or disable specific
portions of code depending on the hardware vendor. Thus, dmidecode is mainly
used to detect system "signatures" and add them to the kernel source code
when needed.


%prep
%setup -q


%build
%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
%makeinstall PREFIX=%{buildroot}%{_prefix}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README LICENSE AUTHORS CHANGELOG
%{_sbindir}/*


%changelog
* Thu Aug 18 2005 Vincent Danen <vdanen@annvix.org> 2.3-4avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 2.3-3avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 2.3-2avx
- Annvix build

* Fri Mar  5 2004 Thomas Backlundd <tmb@mandrake.org> 2.3-1sls
- fist OpenSLS build

* Fri Jan  9 2004 Frederic Lepied <flepied@mandrakesoft.com> 2.3-2mdk
- rename spec file
- removed lm_sensors stuff

* Wed Jan  7 2004 Warly <warly@mandrakesoft.com> 2.3-1mdk
- new package
