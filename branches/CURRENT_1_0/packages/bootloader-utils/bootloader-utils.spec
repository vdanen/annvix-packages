%define name	bootloader-utils
%define version	1.6
%define release	7avx

%define _mypost_service() if [ $1 = 1 ]; then /sbin/chkconfig --add %{1}; fi;

Summary:	Small utils needed for the kernel
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.linux-mandrake.com/cgi-bin/cvsweb.cgi/soft/initscripts/mandrake/loader/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		bootloader-utils-1.6-opensls.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot

Requires:	perl-base
Prereq:		chkconfig, initscripts >= 7.06-21mdk

%description
Utils needed to install/remove a kernel.  Also for updating bootloaders.

%prep
%setup -q
%patch0 -p0 -b .opensls

%build
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make ROOT=%{buildroot} mandir=%{_mandir} install

%post
%_mypost_service kheader

%preun
%_preun_service kheader

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/installkernel
%config(noreplace) /etc/rc.d/init.d/kheader
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
%endif
/usr/share/loader/make-initrd
%{_mandir}/man8/detectloader.8.bz2
%{_mandir}/man8/rebootin.8.bz2


%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 1.6-7avx
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

* Wed Sep 17 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.6-3mdk
- grub: fix finding root partition when fstan has commented out
  entries

* Mon Sep  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.6-2mdk
- PreReq initscripts >= 7.06-21mdk

* Fri Sep  5 2003 Juan Quintela <quintela@mandrakesoft.com> 1.6-1mdk
- make i686-up-4GB names something reasonable like: 2422i686up4GB-5.
- make kheader know all mdk kernels.

* Wed Sep  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.5-1mdk
- kheader is in this package now

* Fri Aug 29 2003 Juan Quintela <quintela@mandrakesoft.com> 1.4-1mdk
- i686-up-4GB and p3-smp-64GB are also mdk kernels.
- /usr/share/loader dir belong to this package.

* Thu Aug 21 2003 Juan Quintela <quintela@mandrakesoft.com> 1.3-1mdk
- "name" and name are valid lilo names.
- cd $$boot only when NOCOPY.

* Mon Aug 18 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.2-1mdk
- switch to new name

* Wed Aug 13 2003 Juan Quintela <quintela@mandrakesoft.com> 1.1-1mdk
- Argh, upload wrong old 1.0 version.

* Wed Aug 13 2003 Juan Quintela <quintela@mandrakesoft.com> 0.8-1mdk
- put lot ot quotes.
- don't put spaces between variables and asignations :(

* Wed Aug 13 2003 Juan Quintela <quintela@mandrakesoft.com> 0.7-1mdk
- arghh, why previous one failed to compile is a mystery yet :(
- no mystery, I have to commit the spec file also :(

* Wed Aug 13 2003 Juan Quintela <quintela@mandrakesoft.com> 0.6-1mdk
- installkernel -S and -s should work.

* Fri Aug  8 2003 Juan Quintela <quintela@mandrakesoft.com> 0.3-1mdk
- work well when there are spaces at the end of kernel name in lilo.conf
  (chmou).

* Mon Aug  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.2-1mdk
- put the Conflicts on the right version og initscripts

* Fri May  9 2003 Juan Quintela <quintela@mandrakesoft.com> 0.1-1mdk
- 1st version.
- splitted from initscripts.

# end of file
