#
# spec file for package basesystem
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		basesystem
%define version 	2.0
%define release 	%_revrel
%define epoch		1

Summary:	The skeleton package which defines a simple Annvix system
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Base
URL:		http://annvix.org/

BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires:	afterboot
Requires:	annvix-release
Requires:	bootloader
Requires:	chkconfig
Requires:	common-licenses
Requires:	console-tools
Requires:	coreutils
Requires:	crond
Requires:	crontabs
Requires:	dev
Requires:	e2fsprogs
Requires:	etcskel
Requires:	filesystem
Requires:	findutils
Requires:	grep
Requires:	gzip
Requires:	initscripts
Requires:	kernel
Requires:	ldconfig
Requires:	less 
Requires:	libgcc >= 3.2-1mdk
Requires:	logrotate
Requires:	losetup
Requires:	mingetty
Requires:	mkinitrd
Requires:	modutils
Requires:	mount
Requires:	net-tools
Requires:	passwd
Requires:	perl-base
Requires:	procps
Requires:	psmisc
Requires:	rootfiles
Requires:	rpm
Requires:	runit
Requires:	sash
Requires:	sed
Requires:	setup
Requires:	shadow-utils 
Requires:	srv
Requires:	stat
Requires:	syslog
Requires:	SysVinit
Requires:	tar
Requires:	termcap
Requires:	time
Requires:	timezone
Requires:	utempter
Requires:	util-linux
Requires:	vim
Requires:	which
# (sb) need pdisk hfsutils mktemp to setup bootloader PPC
%ifarch ppc
Requires:	hfsutils
Requires:	mktemp
Requires:	pdisk
Requires:	pmac-utils
%endif

%description
Basesystem defines the components of a basic Annvix system (for
example, the package installation order to use during bootstrapping).
Basesystem should be the first package installed on a system, and it
should never be removed.


%files


%changelog
* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- 2.0
- make mkinitrd required by every arch

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- 1.2
- Requires: s/sysklogd/syslog/

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-1avx
- 1.1
- drop bdflush from requires

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-8avx
- bootstrap build

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0-7avx
- Requires: runit
- remove Requires: daemontools, ucspi-tcp, mkbootdisk

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0-6avx
- Annvix build
- Requires: s/opensls-release/annvix-release/

* Sat Mar 13 2004 Vincent Danen <vdanen@opensls.org> 1.0-5sls
- Requires: s/mandrake-release/opensls-release/

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.0-4sls
- Requires: afterboot
- remove specific requires for bootloaders for multiple archs, instead make
  sure they all provide "bootloader" and Requires: bootloader

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 1.0-3sls
- Requires: crond, not dcron or any specific flavour of cron

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 1.0-2sls
- Requires: dcron, srv, daemontools, ucspi-tcp
- remove Requires: vixie-cron

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.0-1sls
- change for OpenSLS
- tidy spec
- Epoch: 1

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
