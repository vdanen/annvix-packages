%define name	gradm
%define version	2.0
%define release	0.6sls

%define pre_rc		rc3
%define build_diet	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_diet: %{expand: %%define build_diet 1}}

Summary:	Userspace ACL parsing and authentication for grsecurity
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://www.grsecurity.net/
Source0:	%{name}-%{version}-%{pre_rc}.tar.gz
Source1:	%{name}-%{version}-%{pre_rc}.tar.gz.sign
Source2:	%{name}-ACL.tar.bz2
Patch1:		remove_devfs_from_makefile.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	binutils flex findutils byacc bison glibc-static-devel

#Requires:	kernel-secure >=2.4.22-0.1mdk

%if %{build_diet}
BuildRequires:	/usr/bin/diet
BuildRequires:	dietlibc-devel >= 0.20-1mdk
%endif

%description
grsecurity aims to be a complete security system for Linux 2.4.
gradm performs several tasks for the ACL system including authen-
ticated via a password to the kernel and parsing ACLs to be
passed to the kernel.

%prep
%setup -q -n %{name}2 -a2

%patch1 -p1


%build
%if %{build_diet}
# OE: use the power of dietlibc
# NOTE: currently it just segfaults, but it may work in the future
make CC="diet gcc" CFLAGS="-Os -s -static" LDFLAGS=-static
%else
%make CFLAGS="%{optflags}"
%endif

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR="%{buildroot}" install

# fix strange perms
#chmod 644 debian_secure_acls/*
#chmod 644 gradm-ACL/debian_secure_acls/* gradm-ACL/gentoo_secure_acls/*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
if [ -z "`cut -d" " -f3 /proc/mounts | grep "^devfs"`" ] ; then 
	rm -f /dev/grsec ; 
	if [ ! -e /dev/grsec ] ; then 
		/bin/mknod -m 0622 /dev/grsec c 1 10 ; 
	fi 
fi
       

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/grsec
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/grsec/acl
%attr(0754,root,root) /sbin/%{name}
%attr(0754,root,root) /sbin/grlearn
%attr(0644,root,root) %{_mandir}/man8/%{name}.8*

%changelog
* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.0-0.6sls
- minor spec cleanups

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 2.0-0.5sls
- OpenSLS build
- tidy spec
- remove %%_prefix

* Tue Dec 30 2003 Michael Scherer <misc@mandrake.org> 2.0-0.4mdk 
- fix [DIRM] %{_sysconfdir}/grsec

* Thu Nov 20 2003 Thomas Backlund <tmb@iki.fi> 2.0-0.3mdk
- rc3

* Thu Sep 18 2003 Thomas Backlund <tmb@iki.fi> 2.0-0.2mdk
- move devfs checks to %post from makefile

* Wed Sep 17 2003 Thomas Backlund <tmb@iki.fi> 2.0-0.1mdk
- initial cooker contrib
- gradm 2.0-rc2
- spec based on 1.9.9d rpm package by Oden Eriksson that 
  never got uploaded due to kernel mismatch
