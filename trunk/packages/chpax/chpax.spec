%define name	chpax
%define version	0.5
%define release	4avx

Summary:	Tool that allows PaX flags to be modified on a per-binary basis
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Configuration/Other
URL:		http://pageexec.virtualave.net/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-%{version}-autotools.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	autoconf2.5 automake1.7

%description
A tool that allows PaX flags to be modified on a per-binary basis. PaX is part
of common security-enhancing kernel patches, like GrSecurity. Your system needs
to be running an appropriately patched kernel, like the one provided by the
kernel-secure package, for this program to have any effect.

%prep
%setup -q
%patch0 -p1

%build 
aclocal-1.7
autoheader-2.5x
autoconf-2.5x
automake-1.7 --foreign -a
%configure 
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root) 
%doc README ChangeLog
%{_mandir}/man1/chpax.1*
%{_sbindir}/chpax

%changelog 
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 0.5-4avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.5-3sls
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.5-2sls
- OpenSLS build
- tidy spec

* Tue Dec 30 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.5-1mdk
- from Omer Shenker <chpax@omershenker.net> :
	- Specfile for Mandrake
	- gz to bz2 compression
