%define name	mcrypt
%define version 2.6.4
%define release 2sls

Summary:	Data encryption/decryption program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File tools
URL:		http://mcrypt.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libmhash-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	libtool-devel
BuildRequires:	autoconf2.5

Prefix:		%{_prefix}

%description
A replacement for the old unix crypt(1) command. Mcrypt
uses the following encryption (block) algorithms: BLOWFISH,
DES, TripleDES, 3-WAY, SAFER-SK64, SAFER-SK128, CAST-128, RC2
TEA (extended), TWOFISH, RC6, IDEA and GOST. The unix crypt
algorithm is also included, to allow compatibility with the
crypt(1) command.
CBC, ECB, OFB and CFB modes of encryption are supported.

%prep

%setup -q

%build
%serverbuild
#libtoolize --copy --force; aclocal; autoconf
./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

#    --build %{_target_platform} \
#    --host %{_target_platform} \
#    --target %{_target_platform} \

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

%find_lang %name

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS TODO doc/FORMAT doc/magic doc/sample*
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.6.4-2sls
- OpenSLS build
- tidy spec

* Mon Nov 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.6.4-1mdk
- 2.6.4
- new url
- fix invalid-build-requires

* Mon Jan 06 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.6.0-2mdk
- rebuilt against new libmcrypt

* Fri Oct 04 2002 Lenny Cartier <lenny@mandrakesoft.com> 2.6.3-1mdk
- 2.6.3

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.6.0-1mdk
- new version
- misc spec file fixes
- rebuilt against latest BuildRequires

* Sun May 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.13-3mdk
- rebuilt with gcc3.1

* Thu Apr 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.13-2mdk
- added BuildRequires: libltdl3-devel

* Thu Apr 25 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.13-1mdk
- new version
- misc spec file fixes

* Sun Dec 23 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.5.10-1mdk
- new version
- misc spec file fixes

* Wed Aug 29 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.5.7-1mdk
- added by Thomas Leclerc <leclerc@linux-mandrake.com> :
	- Initial Mandrake build

# end of file
