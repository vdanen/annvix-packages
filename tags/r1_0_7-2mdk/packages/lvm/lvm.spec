%define name lvm
%define version 1.0.7
%define release 2mdk

Summary: Logical Volume Manager administration tools
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://linux.msede.com/lvm/current/%{name}_%{version}.tar.bz2
License: GPL
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
URL: http://lvm.msede.com/lvm/
Patch1: LVM-1.0.1-fix-kernel-headers-build.patch.bz2
Patch2: LVM-1.0.1-static.patch.bz2

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadd(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -n LVM
cd %{version}
%patch1 -p2 -b .fixkheaders
%patch2 -p2 -b .static

%build
cd %{version}
%configure --sbindir=/sbin --libdir=/%{_lib} --disable-static_link
%make

%install
rm -rf $RPM_BUILD_ROOT
cd %{version}
%makeinstall_std OWNER=$UID GROUP=$GROUPS staticlibdir=%{_libdir}
rm -rf $RPM_BUILD_ROOT/%{_lib} $RPM_BUILD_ROOT/%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/sbin/*
%{_mandir}/man8/*
%doc %{version}/ABSTRACT %{version}/CHANGELOG %{version}/CONTRIBUTORS %{version}/COPYING
%doc %{version}/COPYING.LIB %{version}/FAQ %{version}/LVM-HOWTO %{version}/README
%doc %{version}/TODO %{version}/WHATSNEW

%changelog
* Fri Aug 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-2mdk
- lib64 fixes

* Mon Jul 21 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.0.7-1mdk
- 1.0.7

* Tue Jan  7 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.6-1mdk
- Remove DAC960, disable-profiling patch (merged upstream).
- Bump to version 1.0.6.

* Mon Aug  5 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.1-2mdk
- don't redefine _sbindir, _libdir
- rpmlint fixes: hardcoded-library-path

* Tue Jan 22 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.0.1-1mdk
- Add DAC960 support from debian.
- Fix build with local headers not with /usr/src/linux one.
- 1.0.1.

* Sat Sep 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9-3mdk
- corrected access rights to doc

* Sun Jul 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9-2mdk
- build the tools statically

* Thu Mar  1 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9-1mdk
- 0.9

* Fri Sep 08 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.8final-0.2mdk 
- used srpm from Jan Niehusmann <jan@gondor.com> :
	- merged patches from Andreas Dilger <adilger@turbolinux.com> 

* Wed Aug 23 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.8final-0.1mdk
- clean files section
- used srpm from Jan Niehusmann <jan@gondor.com>
	- First lvm rpm for Mandrake distribution.

