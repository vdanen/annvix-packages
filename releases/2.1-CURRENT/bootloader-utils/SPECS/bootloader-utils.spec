#
# spec file for package bootlaoder-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bootloader-utils
%define version		1.6
%define release		%_revrel

Summary:	Small utils needed for the kernel
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/initscripts/mandrake/loader/
Source0:	%{name}-%{version}.tar.bz2
Source1:	memtest86.pm
Source2:	kheader-avx.init
Patch0:		bootloader-utils-1.6-avx-grub.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	perl-base
Requires:	perl(MDK::Common)
Requires(post):	runit >= 1.7.0
Requires(post):	initscripts >= 7.06-21mdk
Requires(post):	rpm-helper
Requires(preun): runit >= 1.7.0
Requires(preun): initscripts >= 7.06-21mdk
Requires(preun): rpm-helper

%description
Utils needed to install/remove a kernel.  Also for updating bootloaders.


%prep
%setup -q
cp %{_sourcedir}/memtest86.pm memtest86
%patch0 -p1 -b .avx


%build
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make ROOT=%{buildroot} mandir=%{_mandir} install

rm -rf %{buildroot}/etc/rc.d
mkdir -p %{buildroot}%{_initrddir}
install -m 0750 %{_sourcedir}/kheader-avx.init %{buildroot}%{_initrddir}/kheader


%post
%_post_service kheader


%preun
%_preun_service kheader


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/installkernel
%{_initrddir}/kheader
/sbin/installkernel
/sbin/kernel_remove_initrd
%{_sbindir}/detectloader
%{_sbindir}/rebootin
%dir /usr/share/loader
/usr/share/loader/common.pm
%ifarch ppc
/usr/share/loader/yaboot
%else
# x86 & hammer, default.
/usr/share/loader/grub
/usr/share/loader/lilo
/usr/share/loader/memtest86
%endif
/usr/share/loader/make-initrd
%{_mandir}/man8/detectloader.8.bz2
%{_mandir}/man8/rebootin.8.bz2


%changelog
* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- add requires on perl(MDK::Common)

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- S2: provide our own initscript

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- requires runit, not chkconfig

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- use %%{_sourcedir} instead of %%{SOURCEx}
- remove pre-Annvix changelog
- initscript is not a config file
- buildarch: noarch

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-12avx
- new-style requires
- NOTE: we need to find something to replace this; newer bootloader-utils
  rely too heavily on DrakX modules

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-11avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-10avx
- bootstrap build

* Sat Feb 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-9avx
- put back in the parts of the old patch we forgot
- also don't have detectloader look for lilo.conf

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.6-8avx
- try to fix installation of grub configuration when /boot is a
  raid device

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.6-7avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 1.6-6sls
- look for grub.conf rather than menu.lst

* Wed Mar  3 2004 Thomas Backlund <tmb@iki.fi> 1.6-5sls
- sync with mdk 1.6-7mdk
  * getroot() don't have arguement.
  * append is not null anymore.
  * ide-scsi removed from command line for all kernel (2.6 2.4).
  *  when boot loader is grub, do not remove unrelated kernel entries (#5952)
  * from Thomas Backlund <tmb@mandrake.org>:
    o typo fixes
    o make some messages somewhat more understandable
  *  fix detectloader typo (perl now reports an error instead of silently ignoring the pb)
- minor spec cleanups (vdanen)
- remove %%prefix (vdanen)

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.6-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
