%define _mypost_service() if [ $1 = 1 ]; then /sbin/chkconfig --add %{1}; fi;

Summary: Small utils needed for the kernel
Name: bootloader-utils
Version: 1.6
Release: 3mdk
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Requires: perl-base
Prereq: chkconfig
PreReq: initscripts >= 7.06-21mdk
Url: http://www.linux-mandrake.com/cgi-bin/cvsweb.cgi/soft/initscripts/mandrake/loader/

%description

Utils needed to install/remove a kernel.  Also for updating bootloaders.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make ROOT=$RPM_BUILD_ROOT mandir=%{_mandir} install

%post
%_mypost_service kheader

%preun
%_preun_service kheader

%clean
rm -rf $RPM_BUILD_ROOT

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
