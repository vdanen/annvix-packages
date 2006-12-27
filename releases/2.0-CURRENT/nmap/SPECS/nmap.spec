#
# spec file for package nmap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		nmap
%define version		4.11
%define release		%_revrel
%define epoch		1

Summary:	Network exploration tool and security scanner
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Networking/Other
URL:		http://www.insecure.org/nmap/
Source0:	http://download.insecure.org/nmap/dist/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libpcre-devel
BuildRequires:	openssl-devel

%description
Nmap is a utility for network exploration or security auditing. It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, sunRPC scanning, reverse-identd scanning, and
more.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
perl  -pi -e 's|/lib\b|/%{_lib}|g' configure*


%build
# update config.* to recognize amd64-*
%{?__cputoolize: %{__cputoolize} -c nsock/src}
%configure2_5x \
    --with-openssl=%{_prefix} \
    --with-libpcap=%{_prefix} \
    --with-libpcre=%{_prefix} \
    --without-nmapfe

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall nmapdatadir=%{buildroot}%{_datadir}/nmap


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/nmap
%{_datadir}/%{name}
%{_mandir}/man1/nmap.1*

%files doc
%defattr(-,root,root)
%doc CHANGELOG COPYING* HACKING docs/README docs/nmap.usage.txt


%changelog
* Mon Nov 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.11
- 4.11
- rebuild against new pcre

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.00
- rebuild against new openssl
- spec cleanups

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.00
- add -doc subpackage
- rebuild with gcc4

* Tue Jan 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.00
- 4.00

* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.99
- 3.99
- fix BuildRequires
- lib64 fix
- build against system libs (except libdnet which we don't ship)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.81
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.81
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.81
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.81-2avx
- rebuild against new pcre

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.81-1avx
- 3.81

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.55-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.55-3avx
- rebuild

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.55-2avx
- rebuild against latest openssl

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.55-1avx
- 3.55
- better fix to recognize x86_64

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.48-4avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 3.48-3sls
- minor spec cleanups

* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 3.48-2sls
- OpenSLS build
- tidy spec
- don't build the frontend
- don't use %%configure(2_5x) on amd64 since it doesn't like the build name

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
