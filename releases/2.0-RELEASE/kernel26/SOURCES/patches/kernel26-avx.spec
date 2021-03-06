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
%define kernelver	2
%define patchlevel	6
%define sublevel	16
%define minlevel	53
%define avxrelease	%(echo %{revision}|cut -d ' ' -f 2)

%define tar_version	%{kernelver}.%{patchlevel}.%{sublevel}.%{minlevel}
%define patchversion	avx%{avxrelease}
%define realrelease	%{avxrelease}avx

# never touch the folowing two fields
%define rpmversion	1
%define rpmrelease	1avx
%define realversion	%{kernelver}.%{patchlevel}.%{sublevel}.%{minlevel}
%define avxversion	%{realversion}-%{realrelease}
%define patches_ver	%{realversion}-%{patchversion}


# having different top level names for packges means
# that you have to remove them by hard :(
%define top_dir_name	%{kname}-avx
%define build_dir	${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir		%{build_dir}/linux-%{tar_version}
%define KVERREL		%{realversion}-%{realrelease}

# this is the config that contains all the drivers for the hardware/
# things that I use (Juan Quintela).
%define build_minimal	0

%define build_kheaders	0
%define build_debug	0
%define build_doc	0
%define build_source	1
%define build_BOOT	1
%define build_build	0
%define build_up	1
%define build_smp	1
%define build_xen	0

# End of user definitions
%{?_without_BOOT: %global build_BOOT 0}
%{?_without_build: %global build_build 0}
%{?_without_up: %global build_up 0}
%{?_without_smp: %global build_smp 0}
%{?_without_xen: %global build_xen 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_minimal: %global build_minimal 0}
%{?_without_debug: %global build_debug 0}

%{?_with_BOOT: %global build_BOOT 1}
%{?_with_build: %global build_build 1}
%{?_with_up: %global build_up 1}
%{?_with_smp: %global build_smp 1}
%{?_with_xen: %global build_xen 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_minimal: %global build_minimal 1}
%{?_with_debug: %global build_debug 1}

%{?_with_kheaders: %global build_kheaders 1}

%define build_nosrc 			0
%{?_with_nosrc: %global build_nosrc 1}



%define kmake	%make
# there are places where parallel make don't work
%define smake	make

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/")

Summary:	The Linux %{kernelver}.%{patchlevel} kernel (the core of the Linux operating system)
Name:		%{kname}-%{avxversion}
Version:	%{rpmversion}
Release:	%{rpmrelease}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.kernel.org/
ExclusiveArch:	%{ix86} x86_64 amd64
ExclusiveOS:	Linux

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelver}.%{patchlevel}/linux-%{tar_version}.tar.bz2
Source1: ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelver}.%{patchlevel}/linux-%{tar_version}.tar.bz2.sign

### This is for stripped SRC RPM
%if %build_nosrc
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
%define kprovides	kernel = %{realversion}

BuildRoot:	%{_buildroot}/%{kname}-%{realversion}
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
This is the default Annvix kernel version %{realversion} for single-CPU
systems.


#
# kernel-up virtual rpm
#

%package -n %{kname}-up
Summary:	Virtual rpm for the latest %{kname}-up kernel
Version:	%{realversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-%{avxversion}
Provides:	kernel26-up

%description -n %{kname}-up
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-up installed.


#
# kernel-smp: Symmetric MultiProcessing kernel
#

%package -n %{kname}-smp-%{avxversion}
Summary:	The Linux Kernel compiled for SMP machines
Group:		System/Kernel and hardware
Provides:	%{kprovides}
Requires:	%{requires1}
Requires:	%{requires2}
Requires:	%{requires3}

%description -n %{kname}-smp-%{avxversion}
This is the default Annvix kernel %{realversion} for 4GB SMP systems.
It is required only on machines with two or more CPUs, although it
should work find on single-CPU systems.


#
# kernel-smp virtual rpm
#

%package -n %{kname}-smp
Summary:	Virtual rpm for the latest %{kname}-smp kernel
Version:	%{realversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-smp-%{avxversion}
Provides:	kernel26-smp

%description -n %{kname}-smp
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-smp installed.


#
# kernel-build: standard up kernel without security features
#

%package -n %{kname}-build-%{avxversion}
Summary:	The Linux kernel compiled without security features
Group:		System/Kernel and hardware
Provides:	%{kprovides}
Requires:	%{requires1}
Requires:	%{requires2}
Requires:	%{requires3}

%description -n %{kname}-build-%{avxversion}
This is the "build" Anvix kernel version %{realversion}, which does not
include any security enhancements and is only suitable for dedicated build
systems that are otherwise adequately secured and non-public.


#
# kernel-build virtual rpm
#

%package -n %{kname}-build
Summary:	Virtual rpm for the latest %{kname}-build kernel
Version:	%{realversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-build-%{avxversion}
Provides:	kernel26-build

%description -n %{kname}-build
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-build installed.


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
Version:	%{realversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-BOOT-%{avxversion}
Provides:	kernel26-BOOT

%description -n %{kname}-BOOT
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-BOOT installed.


#
# kernel-xen0: XEN Kernel
#

%package -n %{kname}-xen0-%{avxversion}
Summary:	The XEN hypervisor kernel
Group:		System/Kernel and hardware

%description -n %{kname}-xen0-%{avxversion}
This package contains the XEN hypervisor kernel which provides device
services to unprivileged guests.


#
# kernel-xen0 virtual rpm
#

%package -n %{kname}-xen0
Summary:	Virtual rpm for the latest %{kname}-xen0 kernel
Version:	%{realversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-xen0-%{avxversion}
Provides:	kernel26-xen0

%description -n %{kname}-xen0
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-xen0 installed.


#
# kernel-xenU: XEN Kernel
#

%package -n %{kname}-xenU-%{avxversion}
Summary:	The XEN guest kernel
Group:		System/Kernel and hardware

%description -n %{kname}-xenU-%{avxversion}
This package contains the XEN guest kernel which runs in XEN unprivileged
guest VMs.


#
# kernel-xenU virtual rpm
#

%package -n %{kname}-xenU
Summary:	Virtual rpm for the latest %{kname}-xenU kernel
Version:	%{realversion}
Release:	%{realrelease}
Group:		System/Kernel and hardware
Requires:	%{kname}-xenU-%{avxversion}
Provides:	kernel26-xenU

%description -n %{kname}-xenU
This package is a virtual rpm that aims to make sure you always have the
latest %{kname}-xenU installed.


#
# kernel-source: Kernel source
#

%package -n %{kname}-source
Summary:	The source code for the Linux kernel
Version:	%{realversion}
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

#
# End packages - here begins build stage
#

%prep
# now that we build out of svn, we need to dynamically create the
# patch tarball
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

cd %{src_dir}


%{patches_dir}/scripts/apply_patches

# PATCH END
#
# Setup Begin
#

# Prepare all the variables for calling create configs

%if %{build_debug}
%define debug --debug
%else
%define debug --no-debug
%endif

%if %{build_minimal}
%define minimal --minimal
%else
%define minimal --no-minimal
%endif

%{patches_dir}/scripts/create_configs %{debug} %{minimal} --user_cpu="%{target_cpu}"

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' |xargs rm -f

%if %build_kheaders

kheaders_dirs=`echo $PWD/include/{asm-*,linux,sound}`

pushd %{build_dir}
    install -d kernel-headers/
    cp -a $kheaders_dirs kernel-headers/
    tar cf kernel-headers-%{avxversion}.tar kernel-headers/
    bzip2 -9f kernel-headers-%{avxversion}.tar
    rm -rf kernel-headers/
    # build_kheaders
popd
%endif


%build
# Common target directories
%define _kerneldir	/usr/src/linux-%{KVERREL}
%define _bootdir	/boot
%define _modulesdir	/lib/modules
%define _savedheaders	../../savedheaders/

# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}

PrepareKernel() {
    name=$1
    extension=$2
    echo "Prepare compilation for kernel $extension"

    # We can't use only defconfig anyore because we have the autoconf patch,

    if [ -z "$name" ]; then
        config_name="defconfig"
    else
        config_name="defconfig-$name"
    fi

    # make sure EXTRAVERSION says what we want it to say
    LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%{minlevel}-$extension/" Makefile

    %{smake} -s mrproper
    cp arch/%{target_arch}/$config_name .config
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

    %ifarch %{ix86}
    if [ "$KernelVer" == "%{KVERREL}xen0" -o "$KernelVer" == "%{KVERREL}xenU" ]; then
        cp -f vmlinuz %{temp_boot}/vmlinuz-$KernelVer
    else
        cp -f arch/i386/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
    fi
    %endif
    %ifarch x86_64
    if [ "$KernelVer" == "%{KVERREL}xen0" -o "$KernelVer" == "%{KVERREL}xenU" ]; then
        cp -f vmlinuz %{temp_boot}/vmlinuz-$KernelVer
    else
        cp -f arch/x86_64/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
    fi
    %endif

    # modules
    install -d %{temp_modules}/$KernelVer
    %{smake} INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}

SaveHeaders() {
    flavour=$1
    flavour_name="`echo $flavour | sed 's/-/_/g'`"

%if %{build_source}
    HeadersRoot=%{temp_source}/savedheaders
    HeadersArch=$HeadersRoot/%{target_cpu}/$flavour
    echo "Saving headers for $flavour %{target_cpu}"

    # deal with the kernel headers that are version specific
    install -d $HeadersArch
    install -m 0644 include/linux/autoconf.h $HeadersArch/autoconf.h
    install -m 0644 include/linux/version.h $HeadersArch/version.h
    echo "%{target_cpu} $flavour_name %{_savedheaders}%{target_cpu}/$flavour/" >> $HeadersRoot/list
%endif
}

CreateFiles() {
    kversion=$1
    output=../kernel_files.$kversion

    echo "%defattr(-,root,root)" > $output
    echo "%{_bootdir}/config-${kversion}" >> $output
    echo "%{_bootdir}/vmlinuz-${kversion}" >> $output
    echo "%{_bootdir}/System.map-${kversion}" >> $output
    echo "%dir %{_modulesdir}/${kversion}/" >> $output
    echo "%{_modulesdir}/${kversion}/kernel" >> $output
    echo "%{_modulesdir}/${kversion}/modules.*" >> $output
}

CreateKernel() {
    flavour=$1

    if [ "$flavour" = "up" ]; then
        KernelVer=%{KVERREL}
        PrepareKernel "" %realrelease
    else
        KernelVer=%{KVERREL}$flavour
        PrepareKernel $flavour %{realrelease}$flavour
    fi

    BuildKernel $KernelVer
    SaveHeaders $flavour
    CreateFiles $KernelVer
}


CreateKernelNoName() {
    arch=$1
    nprocs=$2
    memory=$3

    name=$arch-$nprocs-$memory
    extension="%{realrelease}-$name"

    KernelVer="%{KVERREL}-$arch-$nprocs-$memory"
    PrepareKernel $name $extension
    BuildKernel $KernelVer
    SaveHeaders $name
    CreateFiles $KernelVer
}

###
# DO it...
###

# Create a simulacro of %buildroot
rm -rf %{temp_root}
install -d %{temp_root}

# make sure we are in the directory
cd %{src_dir}

%if %{build_BOOT}
CreateKernel BOOT
%endif

%if %{build_smp}
CreateKernel smp
%endif

%if %{build_build}
CreateKernel build
%endif

%if %{build_up}
CreateKernel up
%endif

%if %{build_xen}
CreateKernel xen0
CreateKernel xenU
%endif

# We don't make to repeat the depend code at the install phase
%if %{build_source}
PrepareKernel "" %{realrelease}custom
# From > 2.6.13 prepare-all is deprecated and relies on include/linux/autoconf
# To have modpost and other scripts, one has to use the target scripts
%{smake} -s prepare
%{smake} -s scripts
%endif


###
### install
###
%install
install -m 0644 %{_sourcedir}/README.annvix-kernel-sources  .
install -m 0644 %{_sourcedir}/README.Annvix  .

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
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}

# we remove all the source files that we don't ship

# first architecture files
for i in alpha arm cris m68k mips mips64 parisc ppc ppc64 powerpc s390 s390x sh sh64 arm26 sparc sparc64 h8300 m68knommu v850 m32r frv xtensa; do
    rm -rf %{target_source}/arch/$i
    rm -rf %{target_source}/include/asm-$i
done

# remove config split dir
rm -rf %{target_source}/include/config

# my patches dir, this should go in other dir
rm -rf %{target_source}/%{patches_ver}

# other misc files
rm -f %{target_source}/{.config.old,.config.cmd}
%if %{build_xen}
rm -f %{target_source}/include/.asm-ignore
rm -f %{target_source}/vmlinux-stripped
rm -f %{target_source}/vmlinuz
%endif


# copy README's
cp %{_sourcedir}/README.Annvix %{target_source}/
cp %{_sourcedir}/README.annvix-kernel-sources %{target_source}/

pushd %{target_source}/include/linux ; {
    install -m 0644 %{_sourcedir}/linux-annvix-config.h rhconfig.h
    rm -rf autoconf.h version.h
    # Create autoconf.h file
    echo '#include <linux/rhconfig.h>' > autoconf.h
    sed 's,$,autoconf.h,' %{_savedheaders}list | awk -f %{_sourcedir}/annvix-linux-merge-config.awk >> autoconf.h
    # Create version.h
    echo "#include <linux/rhconfig.h>" > version.h
    loop_cnt=0
    for i in BOOT up smp build xen0; do
        if [ -d %{_savedheaders}%{target_cpu}/$i -a -f %{_savedheaders}%{target_cpu}/$i/version.h ]; then
            name=`echo $i | sed 's/-/_/g'`
            if [ $loop_cnt = 0 ]; then
                buf="#if defined(__module__$name)"
            else
                buf="#elif defined(__module__$name)"
            fi
            echo "$buf" >> version.h
            grep UTS_RELEASE %{_savedheaders}%{target_cpu}/$i/version.h >> version.h
            loop_cnt=$[loop_cnt + 1]
        fi
    done
    # write last lines
    if [ $loop_cnt -eq 0 ]; then
        echo "You need to build at least one kernel"
        exit 1;
    fi
    echo "#else" >> version.h
    echo '#define UTS_RELEASE "'%{KVERREL}custom'"' >> version.h
    echo "#endif" >> version.h

    # Any of the version.h are ok, as they only differ in the first line
    ls %{_savedheaders}%{target_cpu}/*/version.h | head -n 1 | xargs grep -v UTS_RELEASE >> version.h
    rm -rf %{_savedheaders}
    } ;
popd
#endif build_source
%endif

# Gzip modules
find %{target_modules} -type f -name '*.ko'|xargs gzip -9f

for i in %{target_modules}/*; do
    rm -f $i/build $i/source $i/modules.*
    rm -rf  $i/pcmcia/
done

# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here

pushd %{target_modules}
    for i in *; do
        /sbin/depmod-25 -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
        echo $?
    done

    for i in *; do
        pushd $i
            echo "Creating module.description for $i"
            modules=`find . -name "*.ko.gz"`
            echo $modules | xargs /sbin/modinfo-25 \
              | perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
        popd
    done
popd


###
### clean
###

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 

###
### scripts
###

%define options_preun -g -R -S -c
%define options_post -g -s -c


# up kernel
%preun
/sbin/installkernel %options_preun %{KVERREL}
exit 0

%post
/sbin/installkernel %options_post %{KVERREL}

%postun
/sbin/kernel_remove_initrd %{KVERREL}


# smp kernel
%preun -n %{kname}-smp-%{avxversion}
/sbin/installkernel %options_preun %{KVERREL}smp
exit 0

%post -n %{kname}-smp-%{avxversion}
/sbin/installkernel %options_post %{KVERREL}smp

%postun -n %{kname}-smp-%{avxversion}
/sbin/kernel_remove_initrd %{KVERREL}smp


# build kernel
%preun -n %{kname}-build-%{avxversion}
/sbin/installkernel %options_preun %{KVERREL}build
exit 0

%post -n %{kname}-build-%{avxversion}
/sbin/installkernel %options_post %{KVERREL}build

%postun -n %{kname}-build-%{avxversion}
/sbin/kernel_remove_initrd %{KVERREL}build


# BOOT kernel
%preun -n %{kname}-BOOT-%{avxversion}
/sbin/installkernel %options_preun %{KVERREL}BOOT
exit 0

%post -n %{kname}-BOOT-%{avxversion}
/sbin/installkernel %options_post %{KVERREL}BOOT

%postun -n %{kname}-BOOT-%{avxversion}
/sbin/kernel_remove_initrd %{KVERREL}BOOT


### kernel source
%post -n %{kname}-source
pushd /usr/src >/dev/null 2>&1
    rm -f linux
    ln -snf linux-%{KVERREL} linux
    /sbin/service kheader start 2>/dev/null >/dev/null || :
    # we need to create /build only when there is a source tree.

    for i in /lib/modules/%{KVERREL}*; do
        if [ -d $i ]; then
            ln -sf /usr/src/linux-%{KVERREL} $i/build
            ln -sf /usr/src/linux-%{KVERREL} $i/source
        fi
    done
popd >/dev/null 2>&1

%postun -n %{kname}-source
if [ -L /usr/src/linux ]; then 
    if [ -L /usr/src/linux -a `ls -l /usr/src/linux 2>/dev/null| awk '{ print $11 }'` = "linux-%{KVERREL}" ]; then
        [ $1 = 0 ] && rm -f /usr/src/linux
    fi
fi
# we need to delete <modules>/build at unsinstall
for i in /lib/modules/%{KVERREL}*/{build,source}; do
    if [ -L $i ]; then
        rm -f $i
    fi
done
exit 0

###
### file lists
###

%if %{build_up}
%files -f kernel_files.%{KVERREL}

%files -n %{kname}-up
%defattr(-,root,root)
%endif

%if %{build_smp}
%files -n %{kname}-smp-%{avxversion} -f kernel_files.%{KVERREL}smp

%files -n %{kname}-smp
%defattr(-,root,root)
%endif

%if %{build_build}
%files -n %{kname}-build-%{avxversion} -f kernel_files.%{KVERREL}build

%files -n %{kname}-build
%defattr(-,root,root)
%endif

%if %{build_BOOT}
%files -n %{kname}-BOOT-%{avxversion} -f kernel_files.%{KVERREL}BOOT

%files -n %{kname}-BOOT
%defattr(-,root,root)
%endif

%if %{build_xen}
%files -n %{kname}-xen0-%{avxversion} -f kernel_files.%{KVERREL}xen0

%files -n %{kname}-xen0
%defattr(-,root,root)

%files -n %{kname}-xenU-%{avxversion} -f kernel_files.%{KVERREL}xenU

%files -n %{kname}-xenU
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
%{_kerneldir}/.kconfig.d
%{_kerneldir}/.kernelrelease
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
%{_kerneldir}/arch/ia64
%{_kerneldir}/arch/x86_64
%{_kerneldir}/arch/um
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/init
%{_kerneldir}/ipc
#%{_kerneldir}/kdb
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/security
%{_kerneldir}/sound
%{_kerneldir}/scripts
%{_kerneldir}/usr
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-ia64
%{_kerneldir}/include/asm-x86_64
%{_kerneldir}/include/asm-um
%{_kerneldir}/include/asm
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
#%{_kerneldir}/include/xen
#Openswan 2.x.x
%{_kerneldir}/include/crypto
%{_kerneldir}/include/des
%{_kerneldir}/include/mast.h
%{_kerneldir}/include/openswan.h
%{_kerneldir}/include/openswan
%{_kerneldir}/include/pfkey.h
%{_kerneldir}/include/pfkeyv2.h
%{_kerneldir}/include/zlib
%{_kerneldir}/README.openswan-2
#endif %build_source
%endif

%if %{build_doc}
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_version}/Documentation/*
%endif


%changelog
* Fri Oct 05 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.53
- smp and build kernels now support 64GB RAM, and up/BOOT kernels support 4GB

* Sat Aug 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.16.53
- 2.6.16.53: various fixes and security fix for CVE-2007-2876

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
