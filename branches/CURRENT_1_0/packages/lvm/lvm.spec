%define name	lvm
%define version 1.0.8
%define release 1sls

Summary:	Logical Volume Manager administration tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.sistina.com/products_lvm.htm
Source0:	ftp://ftp.sistina.com/pub/LVM/1.0/%{name}_%{version}.tar.bz2

Patch1:		LVM-1.0.1-fix-kernel-headers-build.patch.bz2
Patch2:		LVM-1.0.1-static.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadd(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.

%prep
%setup -q -n LVM
cd %{version}
%patch1 -p2 -b .fixkheaders
%patch2 -p2 -b .static

%build
cd %{version}
%configure --sbindir=/sbin --libdir=/%{_lib} --disable-static_link
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
cd %{version}
%makeinstall_std OWNER=$UID GROUP=$GROUPS staticlibdir=%{_libdir}
rm -rf $RPM_BUILD_ROOT/%{_lib} $RPM_BUILD_ROOT/%{_libdir}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{version}/ABSTRACT %{version}/CHANGELOG %{version}/CONTRIBUTORS %{version}/COPYING
%doc %{version}/COPYING.LIB %{version}/FAQ %{version}/LVM-HOWTO %{version}/README
%doc %{version}/TODO %{version}/WHATSNEW
/sbin/*
%{_mandir}/man8/*

%changelog
* Fri Mar  5 2004 Thomas Backlund <tmb@mandrake.org> 1.0.8-1sls
- update to 1.0.8 to match 2.4.25 kernel and support
  future move to lvm2
  
* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 1.0.7-3sls
- OpenSLS build
- tidy spec
- remove %%_prefix

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

