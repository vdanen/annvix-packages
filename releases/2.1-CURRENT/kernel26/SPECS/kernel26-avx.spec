#
# spec file for package kernel26
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define kname		kernel
%define kernelversion	2
%define patchlevel	6
%define sublevel	22
%define minlevel	12
%define avxrelease	%(echo %{revision}|cut -d ' ' -f 2)

%define kversion	%{kernelversion}.%{patchlevel}.%{sublevel}.%{minlevel}
%define tar_ver		%{kversion}
%define patchversion	avx%{avxrelease}
%define realrelease	%_revrel

# never touch the folowing two fields
%define rpmversion	1
%define rpmrelease	1avx

%define realversion	%{kernelversion}.%{patchlevel}.%{sublevel}.%{minlevel}
%define avxversion	%{kversion}-%{realrelease}
%define patches_ver	%{kversion}-%{patchversion}

# having different top level names for packges means that you have to remove them by hand :(
%define top_dir_name	%{kname}-%{_arch}
%define build_dir	${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir		%{build_dir}/linux-%{tar_ver}

%define build_debug	0
%define build_doc	0
%define build_source	1
%define build_devel	1
%define build_BOOT	0

# End of user definitions
%{?_without_BOOT: %global build_BOOT 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_devel: %global build_devel 0}
%{?_without_debug: %global build_debug 0}

%{?_with_BOOT: %global build_BOOT 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_devel: %global build_devel 1}
%{?_with_debug: %global build_debug 1}

%define build_nosrc 			0
%{?_with_nosrc: %global build_nosrc 1}

%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake		%make CC="$CC"
%else
%define kmake		%make
%endif
# there are places where parallel make don't work
%define smake		make

%define target_arch	%(echo %{_arch})
%define target_cpu	%(echo %{_target_cpu})

Summary:	The Linux %{kernelversion}.%{patchlevel} kernel (the core of the Linux operating system)
Name:		%{kname}-%{avxversion}
Version:	%{rpmversion}
Release:	%{rpmrelease}
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://www.kernel.org/
ExclusiveArch:	%{ix86} x86_64
ExclusiveOS:	Linux

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign

### This is for stripped SRC RPM
%if %{build_nosrc}
NoSource: 0
NoSource: 1
%endif

Source4:	README.annvix-kernel-sources
Source5:	README.Annvix

Source15:	linux-annvix-config.h
Source16:	annvix-linux-merge-config.awk

Source100:	linux-%{patches_ver}.tar.bz2

####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing

#END
####################################################################

# Defines for the things that are needed for all the kernels

%define requires1	module-init-tools >= 3.0

%define requires2	mkinitrd >= 3.4.43-15avx
%define requires3	bootloader-utils >= 1.6-5avx

%define conflicts	iptables <= 1.2.9-1avx
%define kprovides	kernel = %{kversion}

BuildRoot:	%{_buildroot}/%{kname}-%{kversion}
BuildRequires:	gcc >= 3.3.1-5avx
BuildRequires:	module-init-tools

Provides:	module-info
Provides:	%{kprovides}
Autoreqprov:	no
Requires:	%{requires1}
Requires:	%{requires2}
Requires:	%{requires3}
Conflicts:	%{conflicts}


%description
This is the default Annvix kernel %{kversion}.  It supports SMP
(multi-processor) systems with up to 64GB of RAM.


#
# kernel virtual rpm
#
%package -n %{kname}
Summary:	Virtual rpm for the latest %{kname} kernel
Version:	%{kversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-%{avxversion}
Provides:	kernel26-up
Provides:	%{kname}-up
Provides:	%{kname}-smp
Obsoletes:	%{kname}-up
Obsoletes:	%{kname}-smp

%description -n %{kname}
This package is a virtual rpm that aims to make sure you always have the
latest %{kname} installed.


#
# kernel-devel rpm
#
%package -n %{kname}-devel-%{avxversion}
Summary:	The kernel-devel files for the %{kname} kernel
Group:		Development/Kernel
Requires:	glibc-devel
Requires:	ncurses-devel
Requires:	make
Requires:	gcc
Requires:	perl
Provides:	kernel-devel = %{version}

%description -n %{kname}-devel-%{avxversion}
This package contains the kernel-devel files that should be sufficient to
build 3rd-party drivers againt for use with the %{kname} kernel.


#
# kernel-devel virtual RPM
#
%package -n %{kname}-devel
Summary:	Virtual rpm for the latest %{kname}-devel package
Version:	%{kversion}
Release:	%{realrelease}
Group:		Development/Kernel
Requires:	%{kname}-devel-%{avxversion}

%description -n %{kname}-devel
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-devel installed.


#
# kernel-boot: BOOT Kernel
#
%package -n %{kname}-BOOT-%{avxversion}
Summary:	The version of the Linux kernel used on installation boot disks
Group:		System/Kernel and hardware

%description -n %{kname}-BOOT-%{avxversion}
This package includes a trimmed down version of the Linux kernel.
This kernel is used on the installation boot disks only and should not
be used for an installed system, as many features in this kernel are
turned off because of the size constraints.


#
# kernel-BOOT virtual rpm
#
%package -n %{kname}-BOOT
Summary:	Virtual rpm for the latest %{kname}-BOOT kernel
Version:	%{kversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-BOOT-%{avxversion}
Provides:	kernel26-BOOT

%description -n %{kname}-BOOT
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-BOOT installed.


#
# kernel-source: Kernel source
#
%package -n %{kname}-source
Summary:	The source code for the Linux kernel
Version:	%{kversion}
Release:	%{realrelease}
Requires:	glibc-devel
Requires:	ncurses-devel
Requires:	make
Requires:	gcc
Group:		Development/Kernel

%description -n %{kname}-source
The kernel-source package contains the source code files for the Linux
kernel. These source files are needed to build most C programs, since
they depend on the constants defined in the source code. The source
files can also be used to build a custom kernel that is better tuned to
your particular hardware, if you are so inclined (and you know what you're
doing).


#
# kernel-doc: documentation for the Linux kernel
#
%package -n %{kname}-doc
Summary:	Various documentation bits found in the kernel source
Version:	%{version}
Release:	%{release}
Group:		Documentation

%description -n %{kname}-doc
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.



%prep
# now that we build out of svn, we need to dynamically create the patch tarball
pushd %{_sourcedir}
    if [ -d patches ]; then
        cp -a patches %{patches_ver}
        find %{patches_ver} -name .svn -print|xargs rm -rf
        rm -f linux-%{patches_ver}.tar.bz2
        tar cjf linux-%{patches_ver}.tar.bz2 %{patches_ver} && rm -rf %{patches_ver}
    fi
popd

%setup -q -n %{top_dir_name} -c
%setup -q -n %{top_dir_name} -D -T -a100

%define patches_dir ../%{patches_ver}/

#
# apply patches
#
pushd %{src_dir}
    %{patches_dir}/scripts/apply_patches


    #
    # setup the build
    #

    # Prepare all the variables for calling create configs
    %if %{build_debug}
    %define debug --debug
    %else
    %define debug --no-debug
    %endif

    %{patches_dir}/scripts/create_configs %{debug} --user_cpu="%{target_cpu}"

    # make sure the kernel has the sublevel we know it has...
    LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

    # get rid of unwanted files
    find . -name '*~' -o -name '*.orig' -o -name '*.append' | xargs rm -f
popd



%build
# Common target directories
%define _kerneldir	/usr/src/linux-%{avxversion}
%define _bootdir	/boot
%define _modulesdir	/lib/modules

# Directories definition needed for building
%define temp_root	%{build_dir}/temp-root
%define temp_source	%{temp_root}%{_kerneldir}
%define temp_boot	%{temp_root}%{_bootdir}
%define temp_modules	%{temp_root}%{_modulesdir}


PrepareKernel() {
    name=$1
    extension=$2
    echo "Make dep for kernel $extension"
    %{smake} -s mrproper

    if [ "$name" = "" ]; then
        cp arch/%{target_arch}/defconfig-smp .config
    else
        cp arch/%{target_arch}/defconfig-$name .config
    fi

    # make sure EXTRAVERSION says what we want it to say
    LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{minlevel}-$extension/" Makefile
    ### FIXME MDV bugs #29744, #29074, will be removed when fixed upstream
    LC_ALL=C perl -p -i -e "s/^source/### source/" drivers/crypto/Kconfig

    %{smake} oldconfig
}


BuildKernel() {
    KernelVer=$1
    echo "Building kernel $KernelVer"

    %{kmake} all

    ## Start installing stuff
    install -d %{temp_boot}
    install -m 0644 System.map %{temp_boot}/System.map-$KernelVer
    install -m 0644 .config %{temp_boot}/config-$KernelVer

    cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer

    # modules
    install -d %{temp_modules}/$KernelVer
    %{smake} INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}


SaveDevel() {
    devel_flavour=$1

    DevelRoot=/usr/src/linux-%{avxversion}-$devel_flavour-%{rpmrelease}
    TempDevelRoot=%{temp_root}$DevelRoot

    mkdir -p $TempDevelRoot
    for i in $(find . -name Makefile -o -name Makefile-* -o -name Makefile.*); do cp -R --parents $i $TempDevelRoot;done
    for i in $(find . -name Kconfig -o -name Kconfig.* -o -name Kbuild -o -name Kbuild.*); do cp -R --parents $i $TempDevelRoot;done
    cp -fR include $TempDevelRoot
    cp -fR scripts $TempDevelRoot
    cp -fR arch/%{target_arch}/kernel/asm-offsets.{c,s} $TempDevelRoot/arch/%{target_arch}/kernel/
    %ifarch %{ix86}
    cp -fR arch/%{target_arch}/kernel/sigframe.h $TempDevelRoot/arch/%{target_arch}/kernel/
    %endif
    cp -fR .config Module.symvers $TempDevelRoot
	
    # Needed for truecrypt build (Danny)
    cp -fR drivers/md/dm.h $TempDevelRoot/drivers/md/
	
    for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 mips m32r m68knommu parisc s390 sh sh64 v850 xtensa m68k ppc powerpc sparc sparc64; do
        rm -rf $TempDevelRoot/arch/$i
        rm -rf $TempDevelRoot/include/asm-$i
    done
	
    # fix permissions
    chmod -R a+rX $TempDevelRoot

    kernel_devel_files=../kernel_devel_files.$devel_flavour
	
    ### Create the kernel_devel_files.*
    cat > $kernel_devel_files <<EOF
%defattr(-,root,root)
%dir $DevelRoot
%dir $DevelRoot/arch
%dir $DevelRoot/include
$DevelRoot/Documentation
$DevelRoot/arch/i386
$DevelRoot/arch/x86_64
$DevelRoot/arch/um
$DevelRoot/block
$DevelRoot/crypto
$DevelRoot/drivers
$DevelRoot/fs
$DevelRoot/include/Kbuild
$DevelRoot/include/acpi
$DevelRoot/include/asm
$DevelRoot/include/asm-generic
$DevelRoot/include/asm-i386
$DevelRoot/include/asm-x86_64
$DevelRoot/include/asm-um
$DevelRoot/include/config
$DevelRoot/include/crypto
$DevelRoot/include/keys
$DevelRoot/include/linux
$DevelRoot/include/math-emu
$DevelRoot/include/media
$DevelRoot/include/mtd
$DevelRoot/include/net
$DevelRoot/include/pcmcia
$DevelRoot/include/rdma
$DevelRoot/include/rxrpc
$DevelRoot/include/scsi
$DevelRoot/include/sound
$DevelRoot/include/video
$DevelRoot/init
$DevelRoot/ipc
$DevelRoot/kernel
$DevelRoot/lib
$DevelRoot/mm
$DevelRoot/net
$DevelRoot/scripts
$DevelRoot/security
$DevelRoot/sound
$DevelRoot/usr
$DevelRoot/.config
$DevelRoot/Kbuild
$DevelRoot/Makefile
$DevelRoot/Module.symvers
EOF


    ### Create -devel Post script on the fly
    cat > $kernel_devel_files-post <<EOF
if [ -d /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease} ]; then
    rm -f /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease}/{build,source}
    ln -sf $DevelRoot /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease}/build
    ln -sf $DevelRoot /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease}/source
fi
exit 0
EOF


    ### Create -devel Preun script on the fly
    cat > $kernel_devel_files-preun <<EOF
if [ -L /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease}/build ]; then
    rm -f /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease}/build
fi
if [ -L /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease}$devel_cpu/source ]; then
    rm -f /lib/modules/%{avxversion}-$devel_flavour-%{rpmrelease}/source
fi
exit 0
EOF
}


CreateFiles() {
    kernel_flavour=$1
	
    kernel_files=../kernel_files.$kernel_flavour
	
    ### Create the kernel_files.*
    cat > $kernel_files <<EOF
%defattr(-,root,root)
%{_bootdir}/System.map-%{avxversion}$kernel_flavour
%{_bootdir}/config-%{avxversion}$kernel_flavour
%{_bootdir}/vmlinuz-%{avxversion}$kernel_flavour
%dir %{_modulesdir}/%{avxversion}$kernel_flavour/
%{_modulesdir}/%{avxversion}$kernel_flavour/kernel
%{_modulesdir}/%{avxversion}$kernel_flavour/modules.*
EOF


    ### Create kernel Post script
    cat > $kernel_files-post <<EOF
/sbin/installkernel -g -s -c %{avxversion}$kernel_flavour
pushd /boot >/dev/null 2>&1
    if [ -L vmlinuz-$kernel_flavour ]; then
        rm -f vmlinuz-$kernel_flavour
    fi
    ln -sf vmlinuz-%{avxversion}$kernel_flavour vmlinuz-$kernel_flavour
    if [ -L initrd-$kernel_flavour.img ]; then
        rm -f initrd-$kernel_flavour.img
    fi
    ln -sf initrd-%{avxversion}$kernel_flavour.img initrd-$kernel_flavour.img
popd >/dev/null 2>&1
%if %build_devel
if [ -d /usr/src/linux-%{avxversion}$kernel_flavour ]; then
    rm -f /lib/modules/%{avxversion}$kernel_flavour/{build,source}
    ln -sf /usr/src/linux-%{avxversion}$kernel_flavour /lib/modules/%{avxversion}$kernel_flavour/build
    ln -sf /usr/src/linux-%{avxversion}$kernel_flavour /lib/modules/%{avxversion}$kernel_flavour/source
fi
%endif
exit 0
EOF


    ### Create kernel Preun script on the fly
    cat > $kernel_files-preun <<EOF
/sbin/installkernel -g -s -c -R %{avxversion}$kernel_flavour
pushd /boot >/dev/null 2>&1
    if [ -L vmlinuz-$kernel_flavour ]; then
        if [ \$(readlink vmlinuz-$kernel_flavour) = "vmlinuz-%{avxversion}$kernel_flavour" ]; then
            rm -f vmlinuz-$kernel_flavour
        fi
    fi
    if [ -L initrd-$kernel_flavour.img ]; then
        if [ \$(readlink initrd-$kernel_flavour.img) = "initrd-%{avxversion}$kernel_flavour.img" ]; then
            rm -f initrd-$kernel_flavour.img
        fi
    fi
popd >/dev/null 2>&1
%if %build_devel
if [ -L /lib/modules/%{avxversion}$kernel_flavour/build ]; then
    rm -f /lib/modules/%{avxversion}$kernel_flavour/build
fi
if [ -L /lib/modules/%{avxversion}$kernel_flavour/source ]; then
    rm -f /lib/modules/%{avxversion}$kernel_flavour/source
fi
%endif
exit 0
EOF


    ### Create kernel Postun script on the fly
    cat > $kernel_files-postun <<EOF
/sbin/kernel_remove_initrd %{avxversion}$kernel_flavour
exit 0
EOF
}


CreateKernel() {
    flavour=$1

    PrepareKernel $flavour %{realrelease}$flavour

    BuildKernel %{avxversion}$flavour
    SaveDevel $flavour
    CreateFiles $flavour
}


#
# time to do the actual build
#

# create a fake buildroot
rm -rf %{temp_root}
mkdir -p %{temp_root}

cd %{src_dir}

# create the kernels; "smp" is the default flavour
CreateKernel smp
#CreateKernel BOOT

# We don't make to repeat the depend code at the install phase
%if %{build_source}
PrepareKernel "" %{realrelease}custom
%{smake} -s prepare
%{smake} -s scripts
%endif



%install
cd %{src_dir}
# Directories definition needed for installing
%define target_source	%{buildroot}/%{_kerneldir}
%define target_boot	%{buildroot}%{_bootdir}
%define target_modules	%{buildroot}%{_modulesdir}

# We want to be able to test several times the install part
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %{build_source}
mkdir -p %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}

# remove all the source files that we don't ship
#
# first architecture files
for i in alpha arm avr32 blackfin cris ia64 m68k mips mips64 parisc ppc ppc64 powerpc s390 s390x sh sh64 arm26 sparc sparc64 h8300 m68knommu v850 m32r frv xtensa; do
    rm -rf %{target_source}/arch/$i
    rm -rf %{target_source}/include/asm-$i
done

# remove config split dir
rm -rf %{target_source}/include/config

# my patches dir, this should go in other dir
rm -rf %{target_source}/%{patches_ver}

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd,.mailmap,.missing-syscalls.d}

# copy README's
cp %{_sourcedir}/README.Annvix %{target_source}/
cp %{_sourcedir}/README.annvix-kernel-sources %{target_source}/
%endif

# Gzip modules
find %{target_modules} -type f -name '*.ko' | xargs gzip -9f

for i in %{target_modules}/*; do
    rm -f $i/build $i/source $i/modules.*
    rm -rf  $i/pcmcia/
done

# we need to call depmod -ae because when the modules were gzipped, the stamp was changed
pushd %{target_modules}
    for i in *; do
        /sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
        echo $?
    done

    for i in *; do
        pushd $i
            echo "Creating module.description for $i"
            modules=`find . -name "*.ko.gz"`
            echo $modules | xargs /sbin/modinfo \
              | perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
        popd
    done
popd



%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 



%preun -f kernel_files.smp-preun
%post -f kernel_files.smp-post
%postun -f kernel_files.smp-postun



%preun -n %{kname}-BOOT-%{avxversion} -f kernel_files.BOOT-preun
%post -n %{kname}-BOOT-%{avxversion} -f kernel_files.BOOT-post
%postun -n %{kname}-BOOT-%{avxversion} -f kernel_files.BOOT-postun



%post -n %{kname}-devel-%{avxversion} -f kernel_devel_files.smp-post
%preun -n %{kname}-devel-%{avxversion} -f kernel_devel_files.smp-preun



%post -n %{kname}-source
pushd /usr/src >/dev/null 2>&1
    rm -f linux
    ln -snf linux-%{avxversion} linux
    /sbin/service kheader start 2>/dev/null >/dev/null || :
    # we need to create /build only when there is a source tree.

    for i in /lib/modules/%{avxversion}*; do
        if [ -d $i ]; then
            ln -sf /usr/src/linux-%{avxversion} $i/build
            ln -sf /usr/src/linux-%{avxversion} $i/source
        fi
    done
popd >/dev/null 2>&1



%postun -n %{kname}-source
if [ -L /usr/src/linux ]; then 
    if [ -L /usr/src/linux -a `ls -l /usr/src/linux 2>/dev/null| awk '{ print $11 }'` = "linux-%{avxversion}" ]; then
        [ $1 = 0 ] && rm -f /usr/src/linux
    fi
fi
# we need to delete <modules>/build at unsinstall
for i in /lib/modules/%{avxversion}*/{build,source}; do
    if [ -L $i ]; then
        rm -f $i
    fi
done
exit 0



%files -n %{kname}-%{avxversion} -f kernel_files.smp

%files -n %{kname}
%defattr(-,root,root)


%if %{build_BOOT}
%files -n %{kname}-BOOT-%{avxversion} -f kernel_files.BOOT

%files -n %{kname}-BOOT
%defattr(-,root,root)
%endif


%if %{build_devel}
%files -n %{kname}-devel-%{avxversion} -f kernel_devel_files.smp

%files -n %{kname}-devel
%defattr(-,root,root)
%endif


%if %{build_source}
%files -n %{kname}-source
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/.gitignore
%{_kerneldir}/Kbuild
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/README.Annvix
%{_kerneldir}/README.annvix-kernel-sources
%{_kerneldir}/REPORTING-BUGS
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/x86_64
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/scripts
%{_kerneldir}/usr
%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-x86_64
%{_kerneldir}/include/asm-um
%{_kerneldir}/include/asm
%{_kerneldir}/include/crypto
%{_kerneldir}/include/keys
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/media
%{_kerneldir}/include/mtd
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/rdma
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/video
#endif %build_source
%endif


%if %{build_doc}
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_ver}/Documentation/*
%endif


%changelog
* Thu Nov 08 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.22.12
- 2.6.22.12: fixes CVE-2006-6058

* Fri Oct 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.22.10
- normalize the x86_64 config
- some more spec cleaning
- remove config settings that are non-existant

* Thu Oct 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.22.10
- fix the calls to install-kernel; we're stuck with an older bootloader-utils
  as newer Mandriva bootloader-utils require drakx which we are not importing
  so adjust as necessary

* Thu Oct 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.22.10
- 2.6.22.10
- build -devel packages, ala Mandriva
- only build an smp kernel; no more build/BOOT/smp/up kernel flavours
  (NOTE: this depends on whether or not our netinstall ISO will boot with
  a "normal" kernel)
- rediff SL61
- SA[01-48]: Novell AppArmor 2.1.0 pre-release (commit 961, SUSE 10.3)
- drop the openswan patches; according to the website openswan can use the
  2.6 kernel's builtin NETKEY IPsec stack (as opposed to openswan's KLIPS)
- drop xen kernel build stuff
- updated configs and scripts to handle the new kernel

* Thu Oct 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.53
- 2.6.16.53; fixes CVE-2007-2876 amongst other issues
- smp and build kernels now support 64GB RAM, and up/BOOT kernels support 4GB

* Fri Jun 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.52
- 2.6.16.52
- updated SL60 (AppArmor fullseries v405)

* Sat May 05 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.50
- 2.6.16.50: various fixes and security fixes for CVE-2007-1357,
  CVE-2007-2242, CVE-2007-1861

* Sat Mar 31 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.46
- 2.6.16.46: various fixes and security fixes for CVE-2007-0005 and
  CVE-2007-1000
- start including the gpg sigs for kernel sources
- SL61: forward-port of the openwall patch (CONFIG_HARDEN_PROC) to
  protect /proc by default
- drop the RSBAC patches

* Tue Mar 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.43
- 2.6.16.43: various fixes and fixes for CVE-2007-0006, CVE-2006-5753,
  CVE-2007-0772, and probably quite a few other CVE names that weren't
  noted in the changelogs

* Wed Jan 31 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.39
- 2.6.16.39: various fixes and fixes for CVE-2006-5823, CVE-2006-6053,
  CVE-2006-6054, CVE-2006-6056, CVE-2006-5755, CVE-2006-6106, CVE-2006-5757,
  CVE-2006-6060, CVE-2006-5173, CVE-2006-5749, CVE-2006-4814, 
- rediff SL64

* Sat Jan 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.37
- set CONFIG_ISCSI_TCP=m (this builds iscsi_tcp.ko, scsi_transport_iscsi.ko
  was already being built) -- this should enable iscsi support
- revert some previous changes for xen that prevented us from building non-xen
  kernels (xen is going to have to wait, it's interfering with openswan)

* Thu Jan 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.37
- 2.6.16.37: various fixes
- disable CONFIG_RSBAC_CAP_AUTH_PROT and CONFIG_RSBAC_CAP_LOG_MISSING
  (we don't really need them)
- drop CA01; those SATA drivers are no longer marked experimental
- add support for building xen kernels (still need to do the patching tho)

* Mon Dec 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.35
- 2.6.16.35: security fixes for CVE-2006-4352, CVE-2006-5751
- update SL11 to apply (1 hunk to net/ipv4/udp.c)
- update SL64 to apply (kernel/kallsyms.c)
- NOTE: I had a modified PaX patch, but there were some errors in compiling
  and I'm suspecting RSBAC integration so I've left the patch out for the
  time being although the configs still reflect the PaX changes

* Fri Nov 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.32
- CZ01: add back the Chum framebuffer logo

* Fri Nov 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.32
- 2.6.16.32: security fixes for CVE-2006-3741, CVE-2006-4997, CVE-2006-4623,
  CVE-2006-4572, CVE-2006-5619, CVE-2006-5174, CVE-2006-4538, and many other
  bugs fixed
- update to AppArmor October snapshot (v154)

* Sun Oct 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.29
- enable experimental drivers

* Sat Oct 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.29
- 2.6.16.29 (many bugfixes)
- EXTRAVERSION now includes %%{minlevel} (i.e. the "28" in 2.6.16.28)
- add virtual rpm packages for kernel-up, kernel-smp, kernel-BOOT, and kernel-build
  based on tmb's ideas
- kernels are now kernel-foo, not kernel26-foo (since we're not doing a 2.4 anymore)

* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.28
- 2.6.16.28: security fixes for CVE-2006-3745, CVE-2006-4145, CVE-2006-4093,
  CVE-2006-2935, and other bug fixes
- add SL65: support for apparmor's 'm' flag
- add SL66: support for apparmor's Ux and Px modes
- updated SL60 from SUSE's 2.6.16.21-0.13 (patch dated 05/31/2006)
- fix source url
- rediff part of SL64 [arch/i386/Kconfig]

* Sun Aug 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.27
- actually commit CA01
- add SL10 and SL11: openswan is back

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.27
- cleanup the configs
- add CA01_remove_sata_experimental.patch (thanks Thomas) to mark some
  SATA drivers as not experimental

* Thu Aug 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.27
- enable building netfilter for the BOOT kernel so we can set some default
  firewall rules on the installer

* Wed Aug 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.27
- compile XFS, ext3, reiserfs, and md support in the BOOT kernel like we did
  for 2.4
- spec cleanups

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.27
- more slashing of unwanted config options (AX.25 network device drivers, 
  FIR device drivers, ARCnet support, Token Ring support, wireless network
  device drivers)

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.27
- drop the %%{_docdir} docs, they're in the kernel source tree anyways

* Mon Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.27
- 2.6.16.27 (fixes a whole bunch of security issues... I'm still not sure
  about using this as the default kernel...)

* Mon Jun 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.22
- 2.6.16.22
- renamed RSBAC to SL63 and SL64; updated to 1.2.7
- add AppArmor patches (SL60, SL61, SL62) (obtained from the SUSE 10.1
  kernel-source package) -- need to find the real location yet
- kernel config changes (lots not noted, but here's the important ones):
  - set CONFIG_SECURITY=y           
  - set CONFIG_SECURITY_NETWORK=y
  - set CONFIG_SECURITY_CAPABILITIES=m
  - set CONFIG_SECURITY_APPARMOR=m
  - set CONFIG_EXPERIMENTAL=n
  - set CONFIG_ELF_CORE=y
  - set CONFIG_SLAB=y
  - set CONFIG_DOUBLEFAULT=y
  - set CONFIG_NETFILTER_XTABLES*=m
  - set CONFIG_DEFAULT_AS=y
  - disabled a bunch of USB multimedia devices

* Fri May 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.14
- kernel26 provides kernel26-up, not kernel-up

* Sun May 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.14
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.14
- fix group

* Mon Apr 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.14
- 2.6 (based on 2.4 spec); first Annvix build
- remove build_acpi stuff
- only patches right now are RSBAC-related so comment out the openswan stuff
- name the kernel package 'kernel26' rather than 'kernel' to prevent issues
  with the 2.4 kernel ('kernel')

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
