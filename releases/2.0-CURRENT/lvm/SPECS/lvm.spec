#
# spec file for package lvm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		lvm
%define version 	1.0.8
%define release 	%_revrel

Summary:	Logical Volume Manager administration tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.sistina.com/products_lvm.htm
Source0:	ftp://ftp.sistina.com/pub/LVM/1.0/%{name}_%{version}.tar.bz2
Source1:	lvm1-kheader.tar.bz2

Patch1:		LVM-1.0.1-fix-kernel-headers-build.patch
Patch2:		lvm-1.0.8-wrapper.patch
Patch3:		lvm-1.0.8-dietlibc.patch
Patch4:		lvm-1.0.8-gcc34.patch
Patch5:		lvm-1.0.8-perm.patch
Patch6:		lvm10-CAN-2004-0972.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadd(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n LVM
cd %{version}
bzip2 -dc %{SOURCE1} | tar xf -
%ifarch %{ix86}
ln -s asm-i386 asm
%else
ln -s asm-%{_arch} asm
%endif
%patch1 -p2 -b .fixkheaders
%patch2 -p2 -b .wrapper
%patch3 -p2 -b .diet
%patch4 -p2 -b .gcc34
%patch5 -p2 -b .perm
%patch6 -p2 -b .can-2004-0972


%build
cd %{version}
%ifarch x86_64
export CC="diet x86_64-annvix-linux-gnu-gcc"
%else
export CC="diet gcc"
%endif

%configure \
    --with-user=`id -un` \
    --with-group=`id -gn` \
    --sbindir=/sbin \
    --libdir=/%{_lib} \
    --enable-static_link
%make -C tools/lib WRAPPER=-DWRAPPER liblvm-10.a
%make -C tools vgwrapper WRAPPER=-DWRAPPER
mv tools/vgwrapper tools/vgwrapper.static
%make -C tools clean

unset CC

rm config.cache
%configure \
    --with-user=`id -un` \
    --with-group=`id -gn` \
    --sbindir=/sbin \
    --libdir=/%{_lib}
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
cd %{version}
%makeinstall_std OWNER=$UID GROUP=$GROUPS sbindir=/sbin staticlibdir=%{_libdir}
rm -f %{buildroot}/sbin/lvmcreate_initrd
rm -f %{buildroot}%{_mandir}/man8/lvmcreate_initrd.8
rm -rf %{buildroot}/%{_lib} %{buildroot}/%{_libdir}

# install static versions
install -m 0755 tools/vgwrapper.static %{buildroot}/sbin/vgwrapper

echo "update-alternatives --install /sbin/lvm lvm /sbin/lvm1 10 \\" > lvm1-setup-alternatives.sh

for i in %{buildroot}/sbin/*; do
    n=${i##*/} # basename
    mv $i %{buildroot}/sbin/lvm1-$n
    echo "--slave /sbin/$n $n /sbin/lvm1-$n \\" >> lvm1-setup-alternatives.sh
done
for i in %{buildroot}%{_mandir}/man8/*; do
    n=${i##*/} # basename
    mv $i %{buildroot}%{_mandir}/man8/lvm1-$n
    echo "--slave %{_mandir}/man8/$n.bz2 $n %{_mandir}/man8/lvm1-$n.bz2 \\" >> lvm1-setup-alternatives.sh
done
echo >> lvm1-setup-alternatives.sh

cat > %{buildroot}/sbin/lvm1 << EOF
#!/bin/sh
command=\$1
shift
if [ -x /sbin/lvm1-\$command ];then
    exec /sbin/lvm1-\$command "\$@"
fi
exit 1
EOF

chmod 0755 %{buildroot}/sbin/lvm1

rm -f %{buildroot}%{_libdir}/liblvm-*.*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -f %{version}/lvm1-setup-alternatives.sh


%postun
if [ $1 = 0 ]; then
    update-alternatives --remove lvm /sbin/lvm1
fi


%files
%defattr(-,root,root)
/sbin/*
%{_mandir}/man8/*

%files doc
%defattr(-,root,root)
%doc %{version}/ABSTRACT %{version}/CHANGELOG %{version}/CONTRIBUTORS %{version}/COPYING
%doc %{version}/COPYING.LIB %{version}/FAQ %{version}/LVM-HOWTO %{version}/README
%doc %{version}/TODO %{version}/WHATSNEW


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8 
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-5avx
- bootstrap build (new gcc, new glibc)
- merge with lvm1-1.0.8-5mdk:
  - make it build with recent gcc and glibc (bluca)
  - do not use getgrnam when statically built against glibc (bluca)
  - use dietlibc

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-4avx
- rebuild

* Wed Nov 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-3avx
- P3: security fix for CAN-2004-0972

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.8-2avx
- Annvix build

* Fri Mar  5 2004 Thomas Backlund <tmb@mandrake.org> 1.0.8-1sls
- update to 1.0.8 to match 2.4.25 kernel and support
  future move to lvm2
  
* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 1.0.7-3sls
- OpenSLS build
- tidy spec
- remove %%{_prefix}

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

