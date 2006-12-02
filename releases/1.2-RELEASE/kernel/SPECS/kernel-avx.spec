#
# spec file for package kernel
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define kname		kernel
%define sublevel	33
%define subsublevel	4
%define avxrelease	%(echo %{revision}|cut -d ' ' -f 2)

%define tar_version	2.4.%{sublevel}.%{subsublevel}
%define patchversion	avx%{avxrelease}
%define realrelease	%{avxrelease}avx

# never touch the folowing two fields
%define rpmversion	1
%define rpmrelease	1avx
%define realversion	2.4.%{sublevel}
%define avxversion	%{tar_version}-%{realrelease}
%define patches_ver	2.4.%{sublevel}-%{patchversion}


# having different top level names for packges means
# that you have to remove them by hard :(
%define top_dir_name	%{kname}-avx
%define build_dir	${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir		%{build_dir}/linux-%{tar_version}
%define KVERREL		%{realversion}-%{realrelease}

# this is the config that contains all the drivers for the hardware/
# things that I use (Juan Quintela).
%define build_minimal	0
%define build_acpi	1

%define build_kheaders	0
%define build_debug	0
%define build_doc	0
%define build_source	1
%define build_BOOT	1
# re-enable once we re-introduce RSBAC
%define build_build	0
%define build_up	1
%define build_smp	1

# End of user definitions
%{?_without_BOOT: %global build_BOOT 0}
%{?_without_build: %global build_build 0}
%{?_without_up: %global build_up 0}
%{?_without_smp: %global build_smp 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}
%{?_without_minimal: %global build_minimal 0}
%{?_without_debug: %global build_debug 0}
%{?_without_acpi: %global build_acpi 0}

%{?_with_BOOT: %global build_BOOT 1}
%{?_with_build: %global build_build 1}
%{?_with_up: %global build_up 1}
%{?_with_smp: %global build_smp 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}
%{?_with_minimal: %global build_minimal 1}
%{?_with_debug: %global build_debug 1}
%{?_with_acpi: %global build_acpi 1}

%{?_with_kheaders: %global build_kheaders 1}

%define build_modules_description	1

%define build_nosrc 			0
%{?_with_nosrc: %global build_nosrc 1}



%define kmake	%make
# there are places where parallel make don't work
%define smake	make

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/")

Summary:	The Linux kernel (the core of the Linux operating system)
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
Source0: ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-%{tar_version}.tar.bz2

### This is for stripped SRC RPM
%if %build_nosrc
NoSource: 0
%endif
Source1: linux-%{tar_version}.tar.bz2.info

Source4:	README.annvix-kernel-sources
Source5:	README.Annvix

Source15:	linux-annvix-config.h
Source16:	annvix-linux-merge-config.awk
Source17:	annvix-linux-merge-modules.awk

Source100:	linux-%{patches_ver}.tar.bz2

####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v2.4/testing

#END
####################################################################

# Defines for the things that are needed for all the kernels

%define requires1	modutils >= 2.4.25-3avx

%define requires2	mkinitrd >= 3.4.43-15avx
%define requires3	bootloader-utils >= 1.6-5avx

%define conflicts	iptables <= 1.2.9-1avx
%define kprovides	kernel = %{realversion}

BuildRoot:	%{_buildroot}/%{kname}-%{realversion}-build
BuildRequires:	gcc >= 3.3.1-5avx

Provides:	kernel-up, module-info, %kprovides
Autoreqprov:	no
Requires:	%requires1
Requires:	%requires2
Requires:	%requires3
Conflicts:	%conflicts

%description
This is the default Annvix kernel version %{realversion} for single-CPU
systems.


#
# kernel-smp: Symmetric MultiProcessing kernel
#

%package -n %{kname}-smp-%{avxversion}
Summary:	The Linux Kernel compiled for SMP machines
Group:		System/Kernel and hardware
Provides:	%kprovides
Requires:	%requires1
Requires:	%requires2
Requires:	%requires3

%description -n %{kname}-smp-%{avxversion}
This is the default Annvix kernel %{realversion} for 4GB SMP systems.
It is required only on machines with two or more CPUs, although it
should work find on single-CPU systems.


#
# kernel-build: standard up kernel without security features
#

%package -n %{kname}-build-%{avxversion}
Summary:	The Linux kernel compiled without security features
Group:		System/Kernel and hardware
Provides:	%kprovides
Requires:	%requires1
Requires:	%requires2
Requires:	%requires3

%description -n %{kname}-build-%{avxversion}
This is the "build" Anvix kernel version %{realversion}, which does not
include any security enhancements and is only suitable for dedicated build
systems that are otherwise adequately secured and non-public.


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
# kernel-source: Kernel source
#

%package -n %{kname}-source
Summary:	The source code for the Linux kernel
Version:	%{realversion}
Release:	%{realrelease}
Requires:	glibc-devel, ncurses-devel, make, gcc
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
Group:		Books/Computer books

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

%if %{build_acpi}
%define acpi --acpi
%else
%define acpi --no-acpi
%endif

%if %{build_minimal}
%define minimal --minimal
%else
%define minimal --no-minimal
%endif

%{patches_dir}/scripts/create_configs %{debug} %{acpi} %{minimal} --user_cpu="%{target_cpu}"

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

DependKernel() {
    name=$1
    extension=$2
    echo "Make dep for kernel $extension"
    %{smake} -s mrproper

    # We can't use only defconfig anyore because we have the autoconf patch,

    if [ -z "$name" ]; then
        config_name="defconfig"
    else
        config_name="defconfig-$name"
    fi
    cp arch/%{target_arch}/$config_name .config

    # make sure EXTRAVERSION says what we want it to say
    LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
    %{smake} oldconfig
    %{smake} dep
}

BuildKernel() {
    KernelVer=$1
    echo "Building kernel $KernelVer"

    %ifarch %{ix86} x86_64
    %{kmake} bzImage
    %endif

    %{kmake} modules

    # first make sure we are not loosing any .ver files to make mrporper's
    # removal of zero sized files.
    find include/linux/modules -size 0 | while read file ; do \
        echo > $file
    done

    ## Start installing stuff
    install -d %{temp_boot}
    install -m 0644 System.map %{temp_boot}/System.map-$KernelVer
    install -m 0644 .config %{temp_boot}/config-$KernelVer

    %ifarch %{ix86}
    cp -f arch/i386/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
    %endif
    %ifarch x86_64
    cp -f arch/x86_64/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
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
    echo "Saving hearders for $flavour %{target_cpu}"

    # deal with the kernel headers that are version specific
    install -d $HeadersArch
    install -m 0644 include/linux/autoconf.h $HeadersArch/autoconf.h
    install -m 0644 include/linux/version.h $HeadersArch/version.h
    mv include/linux/modules $HeadersArch
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
    echo "%doc README.annvix-kernel-sources" >> $output
    echo "%doc README.Annvix" >> $output
}

CreateKernel() {
    flavour=$1

    if [ "$flavour" = "up" ]; then
        KernelVer=%{KVERREL}
        DependKernel "" %realrelease
    else
        KernelVer=%{KVERREL}$flavour
        DependKernel $flavour %{realrelease}$flavour
    fi

    BuildKernel $KernelVer
    if [[ "$flavour" != "BOOT" ]];then	
        SaveHeaders $flavour
    fi
    CreateFiles $KernelVer
}


CreateKernelNoName() {
    arch=$1
    nprocs=$2
    memory=$3

    name=$arch-$nprocs-$memory
    extension="%{realrelease}-$name"

    KernelVer="%{KVERREL}-$arch-$nprocs-$memory"
    DependKernel $name $extension
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

#make sure we are in the directory
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

# We don't make to repeat the depend code at the install phase
%if %{build_source}
DependKernel "" %{realrelease}custom
%endif


###
### install
###
%install
install -m 0644 %{SOURCE4}  .
install -m 0644 %{SOURCE5}  .

cd %src_dir
# Directories definition needed for installing
%define target_source	%{buildroot}/%{_kerneldir}
%define target_boot	%{buildroot}%{_bootdir}
%define target_modules	%{buildroot}%{_modulesdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %{build_source}
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
chmod -R a+rX %{target_source}

# we remove all the source files that we don't ship

# first architecture files
for i in alpha arm cris m68k mips mips64 parisc ppc ppc64 s390 s390x sh sh64 sparc sparc64; do
    rm -rf %{target_source}/arch/$i
    rm -rf %{target_source}/include/asm-$i
done

# my patches dir, this should go in other dir
rm -rf %{target_source}/%{patches_ver}

# other misc files
rm -f %{target_source}/{.config.old,.depend,.hdepend}

# We need this to prevent someone doing a make *config without mrproper
touch %{target_source}/.need_mrproper

# copy README.Annvix
cp %{SOURCE5} %{target_source}/

# We used to have a copy of DependKernel here
# Now, we make sure that the thing in the linux dir is what we want it to be

# We need to fix the patchs in .*depend files  after we fix the paths
find %{target_source} -name ".*depend" | \
while read file ; do
    mv $file $file.old
    sed -e "s|[^ ]*\(/usr/src/linux\)|\1|g" < $file.old > $file
    rm -f $file.old
done

# Try to put some smarter autoconf.h and version.h and modversions.h files in place
pushd %{target_source}/include/linux ; {
    install -m 0644 %{SOURCE15} rhconfig.h
    rm -rf modules modversions.h autoconf.h version.h
    # create modversions.h
    cat > modversions.h <<EOF
#ifndef _LINUX_MODVERSIONS_H
#define _LINUX_MODVERSIONS_H
#include <linux/rhconfig.h>
#include <linux/modsetver.h>
EOF
    list=`find %{_savedheaders} -name "*.ver" -exec basename '{}' \; | sort -u`
    mkdir modules
    for l in $list; do
        sed 's,$,modules/'$l, %{_savedheaders}list | awk -f %{SOURCE17} > modules/$l
        touch -r modules/$l modules/`basename $l .ver`.stamp
        echo '#include <linux/modules/'$l'>' >> modversions.h
    done
    echo '#endif /* _LINUX_MODVERSIONS_H */' >> modversions.h
    # Create autoconf.h file
    echo '#include <linux/rhconfig.h>' > autoconf.h
    sed 's,$,autoconf.h,' %{_savedheaders}list | awk -f %{SOURCE16} >> autoconf.h
    # Create version.h
    echo "#include <linux/rhconfig.h>" >> version.h
    loop_cnt=0
    for i in smp up build; do
        if [ -d %{_savedheaders}%{target_cpu}/$i -a \
            -f %{_savedheaders}%{target_cpu}/$i/version.h ]; then
            name=`echo $i | sed 's/-/_/g'`
            if [ $loop_cnt = 0 ]; then
                buf="#if defined(__module__$name)"
                previous_i="$i"
                loop_cnt=1
            else
                echo "$buf" >> version.h
                grep UTS_RELEASE %{_savedheaders}%{target_cpu}/${previous_i}/version.h >> version.h
                buf="#elif defined(__module__$name)"
                previous_i="$i"
                loop_cnt=`expr $loop_cnt + 1`
            fi
        fi
    done
    #write last lines
    if [ $loop_cnt -eq 0 ]; then
        echo "You need to build at least one kernel"
        exit 1;
    fi

    if [ $loop_cnt -gt 1 ]; then
        echo "#else" >> version.h
    fi

    grep UTS_RELEASE %{_savedheaders}%{target_cpu}/${previous_i}/version.h >> version.h

    if [ $loop_cnt -gt 1 ]; then
        echo "#endif" >> version.h
    fi

    # Any of the version.h are ok, as they only differ in the first line
    ls %{_savedheaders}%{target_cpu}/*/version.h | head -n 1 | xargs grep -v UTS_RELEASE >> version.h
    rm -rf %{_savedheaders}
    } ;
popd
#endif build_source
%endif

# Gzip module and relink the link to a .gz module
find %{target_modules} -type f -name '*.o'|xargs gzip -9f
for i in $(find %{target_modules} -type l -name '*.o');do
    link=$(LC_ALL=C perl -e 'print readlink shift, "\n"' $i)
    ln -s $link.gz $i.gz
    rm -f $i
done

for i in %{target_modules}/*; do
    rm -f $i/build $i/modules.*
    rm -rf  $i/pcmcia/
done

# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here

pushd %{target_modules}
    for i in *; do
        /sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
        echo $?
    done

    %if %{build_modules_description}
    for i in *; do
        pushd $i
            echo "Creating module.description for $i"
            modules=`find . -name "*.o" -o -name "*.o.gz"`
            /sbin/modinfo -f '%{filename} %{description}\n' $modules \
                | perl -lne 'print "$1\t$3" if m|([^/]*)\.o(\.gz)? "(.*)"|'  > modules.description
        popd
    done
    %endif
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
for i in /lib/modules/%{KVERREL}*/build; do
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
%endif

%if %{build_smp}
%files -n %{kname}-smp-%{avxversion} -f kernel_files.%{KVERREL}smp
%endif

%if %{build_build}
%files -n %{kname}-build-%{avxversion} -f kernel_files.%{KVERREL}build
%endif

%if %{build_BOOT}
%files -n %{kname}-BOOT-%{avxversion} -f kernel_files.%{KVERREL}BOOT
%endif

%if %{build_source}
%files -n %{kname}-source
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/.need_mrproper
#%{_kerneldir}/3rdparty
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/README.Annvix
%{_kerneldir}/REPORTING-BUGS
%{_kerneldir}/Rules.make
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/ia64
%{_kerneldir}/arch/x86_64
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
%{_kerneldir}/rsbac
%{_kerneldir}/security
%{_kerneldir}/scripts
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-ia64
%{_kerneldir}/include/asm-x86_64
%{_kerneldir}/include/asm
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/rsbac
%{_kerneldir}/include/scsi
%{_kerneldir}/include/video
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
%doc README.annvix-kernel-sources
%doc README.Annvix
#endif %build_source
%endif

%if %{build_doc}
%files -n %{kname}-doc
%defattr(-,root,root)
%doc linux-%{tar_version}/Documentation/*
%endif


%changelog
* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.33.4
- 2.4.33.4: fixes CVE-2006-4997
- CA07: support for the VIA 8251 chipset

* Mon Sep 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.33.3
- 2.4.33.3
- includes the following security fixes: CVE-2006-3745, CVE-2006-1528,
  CVE-2006-0039, CVE-2006-1857, CVE-2006-1858, CVE-2006-1864,
  CVE-2006-2271, CVE-2006-2272, CVE-2006-1525, CVE-2006-2274,
  CVE-2006-1524, CVE-2004-1058, CVE-2005-3180, CVE-2005-2709,
  CVE-2005-2708, CVE-2005-2490, CVE-2006-4145
- Openwall patch for 2.4.33 (rediffed)
- RSBAC 1.2.8
  - set CONFIG_RSBAC_RMSG_MAXENTRIES=200
- change the versioning a bit to reflect the fourth digit in the package
  name

* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.32
- re-introduce RSBAC (1.2.5.1) (SL60, SL61)
- rediff Openwall patch to work with RSBAC and move it (now SL70)
- put back SL65 (remove -rsbac from EXTRAVERSION)
- only enable JAIL, DAZ, CAP, RES, and REG as the least intrusive
  (AUTH, RC, and ACL will come once we build some default policies)
- disable CONFIG_RSBAC_NET entirely as this seems to cause some
  (relatively) harmless oopses when looking at socket files like
  /dev/log
- enable CONFIG_RSBAC_RMSG_EXCL to exclusively write RSBAC messages to
  /proc/rsbac-info/rmsg

* Sat Jan 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.32
- fix bug #17 by making the patch tarball dynamically if one
  doesn't already exist and a patches/ subdir exists (allows us to
  still keep the patches uncompressed in svn)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.32
- Clean rebuild

* Wed Nov 30 2005 Vincent Danen <vdanen-at-build.annvix..org> 2.4.32
- Obfuscate email addresses and new tagging
- add CA06_avx-2.4.32-net-tools-fix.patch to fix a problem with compiling
  net-tools 1.60

* Wed Nov 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.32-1avx
- 2.4.32 and 2.4.32-ow1
- fix build so we can work out of subversion
- drop CA02; merged upstream

* Mon Oct 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.31-6avx
- updated README.Annvix and put a copy in the source dir

* Sun Oct 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.31-5avx
- enable CONFIG_FILTER and CONFIG_NETFILTER for the BOOT kernel
  (should fix the problem with dhcpcd not working properly)

* Fri Sep 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.31-4avx
- include the ia64 files; needed for an x86_64 build

* Mon Sep 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.31-3avx
- silence pushd/popd in kernel-source %%post
- clean out the patches tarball and remove all unapplied patches from it

* Thu Sep 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.31-2avx
- bootstrap build (new gcc, new glibc)
- drop every single patch except for the openwall patch, frandom
  support, more boottime args, the chum FB logo, (I'm tired of
  maintaining all this crap)
- add a few patches from Gentoo:
  - support for ECC error checking (CA04)
  - gcc optimizations (CA05)
- add CA02: fix build with newer binutils
- CA03* series of patches from the lck pathset:
  - 010: batch O(1) scheduler, kernel preemption, low latency and CK
    interactivity (kernel preemption is off by default tho)
  - 011: Read Latency2
  - 012: 64-bit jiffies
  - 013: variable HZ settings
  - 030: fs extended attribute support 0.8.73 (rediffed)
  - 031: POSIX ACLs 0.8.73
  - 032: NFS ACL support 0.8.73
  - 033: ACL security attribute support 0.8.73
  - 999: fix sched.h so that the -lck patchset compiles properly for smp
  - NOTE:
    ** The lck patchset is in pending/lck-patchset right now due to build
    ** failures on x86_64 that need more investigation
- don't build kernel-build by default since we're not shipping RSBAC
  right now and it was there to be a non-RSBAC maintenance kernel
- disable CONFIG_LOLAT on smp and BOOT kernels

* Sat Jun 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.31-1avx
- 2.4.31 (includes CAN-2005-1263 fix upstream)
- rediff DC12, DL01
- update DN13 with latest netfilter time patch (required to build
  the latest iptables)
- Openwall kernel patch 2.4.31-ow1 (SL80, rediffed)
- SL82: don't build with -fstack-protector-all
- x86_64: CONFIG_SWIOTLB=y

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.30-2avx
- Openwall kernel patch 2.4.30-ow3 (SL80, rediffed)
- this update fixes CAN-2005-0794, CAN-2005-0750, CAN-2005-0384
  (mainline) and CAN-2005-1263 (via Openwall patch)

* Wed Apr 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.30-1avx
- 2.4.30
- rediff DL01, HB06
- Openwall kernel patch 2.4.30-ow1 (SL80, rediffed)
- set CONFIG_SCSI_SATA_QSTOR=m
- pass -g to installkernel rather than -a because it always wants to
  find lilo.conf otherwise (and since we don't ship lilo, we don't care
  about lilo)

* Wed Mar 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.29-6avx
- disable RSBAC for 1.0-CURRENT; we'll try to get the policies and
  everything in place for 1.1-RELEASE if we can, but right now even
  in softmode RSBAC is too noisy; patches are moved into todo_patches

* Wed Mar 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.29-5avx
- RSBAC 1.2.4
  - set CONFIG_RSBAC_LIST_TRANS=y
  - set CONFIG_RSBAC_LIST_TRANS_MAX_TTL=3600
  - set CONFIG_RSBAC_LIST_TRANS_RANDOM_TA=n
  - set CONFIG_RSBAC_UM=n
  - set CONFIG_RSBAC_AUTH_GROUP=n
  - set CONFIG_RSBAC_CAP_LOG_MISSING=y
  - unset CONFIG_RSBAC_LOG_PROGRAM_FILE
  - unset CONFIG_RSBAC_LOG_PSEUDO
  - set CONFIG_RSBAC_DAC_GROUP=y
  - set CONFIG_RSBAC_FREEZE=y
- include RSBAC bugfix 1 and 2
- set CONFIG_HARDEN_STACK_SMART=n

* Wed Feb 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.29-4avx
- set CONFIG_USB_UHCI_ALT=m

* Wed Feb 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.29-3avx
- enable USB and USB keyboard support by default:
  - CONFIG_USB=y
  - CONFIG_USB_KBD=y
  - CONFIG_USB_EHCI_HCD=y  
  - CONFIG_USB_UHCI=y
  - CONFIG_USB_UHCI_ALT=y
  - CONFIG_USB_OHCI=y
  - CONFIG_INPUT=y
  - CONFIG_KEYBDEV=y
  - CONFIG_MOUSEDEV=y

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.29-2avx
- apply 2.4.29-ow1 patch
- cleanup README.patches.index
- remove ZY01 (SSP support) as apparently SSP won't protect the
  kernel (we'll let Owl do this)
- rediff SL80 to work with RSBAC and HB09 patch [fs/binfmt_elf.c,
  fs/namei.c, fs/read_write.c]
- add SL81: adds /dev/frandom and /dev/erandom
- config changes:
  - CONFIG_BINFMT_ELF_AOUT=n
  - CONFIG_FRANDOM=y
  - CONFIG_HARDEN_STACK=y
  - CONFIG_HARDEN_STACK_SMART=y
  - CONFIG_HARDEN_LINK=y
  - CONFIG_HARDEN_FIFO=y
  - CONFIG_HARDEN_PROC=y  
  - CONFIG_HARDEN_RLIMIT_NPROC=y
  - CONFIG_HARDEN_SHM=n
- disable CONFIG_HARDEN_* and CONFIG_FRANDOM in BOOT kernels
- build reiserfs, xfs, ext3 and md[015] support into the BOOT kernel
  rather than as modules
- disable DEVFS_FS in BOOT kernels
- increase BLK_DEV_RAM_SIZE to 32k from 4k for x86_64

* Wed Jan 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.29-1avx
- 2.4.29

* Tue Jan 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.29-0.rc3.1avx
- 2.4.29-rc3
- rediff SL61, HB33, DL01
- update config: CONFIG_SCSI_SATA_AHCI=m
- add RSBAC bugfixes #6 (General: Various small fixes) (SL69) and #9
  (General: More small fixes) (SL70)
- remove SL68; it's meant for a 2.6 kernel and interferes with SL69

* Wed Dec 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.28-6avx
- revert I2O changes on x86_64 to attempt to isolate what's causing the
  panics in 4avx and 5avx
- also revert CONFIG_BLK_DEV_RAM_SIZE since the I2O reversion made no
  difference

* Sun Dec 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.28-5avx
- remove DEVFS-related comments from x86_64 (see if this makes a difference
  because 4avx refuses to boot on x86_64)
- increase CONFIG_BLK_DEV_RAM_SIZE to 32000 on x86_64 (like x86)

* Sat Dec 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.28-4avx
- add DEVFS-related comments to x86_64 config (similar to x86)
- disable CONFG_BLK_DEV_XD in x86
- disable CONFIG_IDE_TASK_IOCTL in x86
- increase CONFIG_UNIX98_PTY_COUNT to 2048 in x86 (like x86_64)
- enable CONFIG_I2O in x86_64
- Requires: mkinitrd >= 3.4.43-15avx; NOTE: mkinitrd has a temporary
  fix for something that needs to be found in the kernel...  x86
  requires "mkdevices /dev" in initrd whereas x86_64 is the reverse

* Sat Dec 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.28-3avx
- spoke too soon... mkinitrd changes work on x86, but the inverse is true
  for x86_64.. back to the drawing board
- normalize differences between x86 and x86_64:
  - disable CONFIG_KHTTPD in x86
  - disable CONFIG_PHONE* in x86
  - enable CONFIG_UDF_RW in x86
  - disable CONFIG_ARCNET* in x86 (ARCnet)
  - disable CONFIG_TR* in x86 (Token Ring)
  - disable CONFIG_HAMRADIO/CONFIG_AX25*/etc. in x86 (Amateur/Packet Radio)
  - disable CONFIG_INPUT_(GAMEPORT|NS558|LIGHTNING|PCIGAME|CS461X|EMU10K1)
    in x86 (gameports)
  - disable all remaning joystick drivers (CONFIG_INPUT_*) in x86 and
    x86_64
  - disable CONFIG_QIC02_TAPE in x86
  - disable CONFIG_RADIO_* in x86 and x86_64
  - enable CONFIG_AUTOFS_FS module in x86
  - CONFIG_NFS_FS, CONFIG_LOCKD, and CONFIG_SUNRPC compiled in (not
    module) on x86_64
  - disable CONFIG_USB_AUDIO, CONFIG_USB_MIDI
  - disable CONFIG_USB_EMI26 on x86
  - disable CONFIG_SOUND
  - config CONFIG_CRYPTO_SHA256 compiled in (not module) on x86_64

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.28-2avx
- enable CONFIG_USB_{KBD,MOUSE} on x86_64
- wOOp!  kernels boot now... bloody mkinitrd

* Fri Nov 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.28-1avx
- 2.4.28
- remove a bunch of patches that are pretty useless for us
- add Openwall 2.4.28-ow1 patch
- build reiserfs, xfs, raid/md, and ext3 support into the BOOT kernel
  rather than as modules
- remove and add a bunch of other necessary modules for BOOT
- remove opensls remnants
- update RSBAC patch to 2.4.28-v1.2.3 (SL61)
- rediff CE27, DC35, DF05, DL01, DP01, DU01, FS71, SL21, SL01 (drop befs/linuxvfs support), ZT03
- update configs
- remove BG03, BG05, DC47, DC50, DC59, DI01, DI02, DI03, FN04, HB33 (merged upstream)
- don't apply DU30, HB16, HB25

* Wed Aug 04 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.26-5avx
- revert DVD-RW write support for now (DI04)

* Sun Jul 25 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.26-4avx
- remove -rsbac from EXTRAVERSION (SL65)
- fix RSBAC pm_getname-rsbac_pm_all_list_t (SL66)
- remove RSBAC unneded __fput (SL67)
- fix rsbac_is_initialized checks (SL68)
- remove ipsec buildtime symlinks with mrproper (ZZ02)

* Wed Jul 21 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.26-3avx
- add RSBAC x86_64 missing defines bugfix v1.2.3-4 (SL64)
- enable RSBAC_SOFTMODE
- enable RSBAC_DEBUG

* Tue Jul 20 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.26-2avx
- disable openswan 2.1.4 patches (DF02, DF03)
- add openswan 1.0.6 support (DF05)
- add RSBAC v1.2.3 core files (SL60)
- integrate RSBAC v1.2.3 in kernel (SL61)
- add RSBAC AUTH bugfix v1.2.3-1 (SL62)
- add RSBAC JAIL bugfix v1.2.3-3 (SL63)
- update spec and config scripts for RSBAC and openswan
- update configs

* Sat Jul 17 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.26-1avx
- upgrade to kernel.org 2.4.26
- drop patches merged upstream: 
  * (BA58, BG08, BJ04, DI02, HB05, ND01)
  * (ZY58, ZY59, ZY60, ZY61, ZY62, ZY64)
- drop patches fixed upstream: (DC03, ZY66)
- drop selinux support: (SL51)
- rediff/fix patches (DI97, DM09, DU21, ZY65)
- update libata to 2.4.27-rc3 (DI01)
- update ide subsystem to 2.4.27-rc3 (DI02)
- add ide/libata fixes and nvida sata_support from Jeff Garzik (DI03)
- add fix for hang on C1 Halt Disconnect on nForce2 boards (CB11)
- add missing WARN_ON define (CB06)
- add misssing ifdef CONFIG_SWIOTLB on x86_64 pci-gart (HB33)
- update configs

* Wed Jul 03 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.25-19avx
- security and bugfixes:
  * chown DAC check (ZY71)
  * asus acpi fix (ZY73)
  * br_crash fish (ZY74)
  * decnet fix (ZY75)
  * airo fix (ZY76)
  * mpu401 fix (ZY77)
  * msnd fix (ZY78)
  * pss fix (ZY79)
- fix forgotten namechange OpenSLS -> Annvix in kernel docs

* Wed Jun 30 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.25-18avx
- update openswan patches to 2.1.4 (DF02, DF03)
  * fixes CAN-2004-0590
- disable devfs completely for all kernels but BOOT, by
  setting CONFIG_DEVFS_FS=n
  
* Tue Jun 22 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.25-17avx
- e1000 ethtool gregs max length (ZY69)
- redo DI02, as all nForce2 and nForce3 are capable of UDMA133

* Sun Jun 20 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.25-16avx
- redo ZY67 patch for fpu_state fix, I forgot to apply it to x86_64

* Sat Jun 19 2004 Thomas Backlund <tmb-at-build.annvix.org> 2.4.25-15avx
- Update patch CD04 with better logo
- Switch names to annvix / avx

* Tue Jun 15 2004 Thomas Backlund <tmb@iki.fi> 2.4.25-14sls
- add OpenSLS mascot Chud as framebuffer logo (CD04)
- add zisofs support to BOOT kernel for installer
- fix clear_cpu kernel crashing macro on ix86 (ZY67)

* Wed Jun 02 2004 Thomas Backlund <tmb@iki.fi> 2.4.25-13sls
- make standard kernel provide kernel-up for the installer
- update iteraid to 1.45 (MB60, MB61)
  * 64bit fixes, finally works on amd64
  * redo iteraid Makefile so it actually will be built
- update Broadcom 57xx nic to 7.1.22 (MB30)
- fix nls codepage 936 (FN10)
- add missing bitopts.h include in sctp ipv6 (HB32)
- remove sctp debuginfo (ZY66)

* Sat May 22 2004 Thomas Backlund <tmb@iki.fi> 2.4.25-12sls
- CAN-2004-0394 panic() issue (ZY63)
- do_fork issue (ZY64)
- CAN-2004-0424 mcast_mfilter issue (ZY65)
- make /proc/kmsg group readable by klogd (CA01)
- drop freeswan patch (DF01)
- add openswan 2.1.2 (DF02)
- add openswan nat-traversal support (DF03)
- update iteraid to 1.44 (MB60, MB61)

* Mon Apr 19 2004 Thomas Backlund <tmb@iki.fi> 2.4.25-11sls
- CAN-2004-0109 isofs rockridge issue (ZY58)
- CAN-2004-0133 xfs filesystem issue (ZY59)
- CAN-2004-0177 ext3/jbd filesystem issue (ZY60)
- CAN-2004-0178 sb_audio issue (ZY61)
- CAN-2004-0181 jfs filesystem issue (ZY62)

* Fri Apr  2 2004 Thomas Backlund <tmb@iki.fi> 2.4.25-10sls
- DI01_2.4.25-libata15.patch
  * adds support for latest libata (SATA support)
- MB60_iteraid_1.43.tar
  * adds support for IT8212 RAID controller
- MB61_iteraid_fix_includes.patch
  * correct includes for relocation to 3rdparty
- update ND01_forcedeth to 0.25
- update SL01_ea patch to 0.8.71
- update SL11_acl patch to 0.8.71
- update SL21_nfsacl patch to 0.8.71
- update SL31_sec patch to 0.8.71
- update SL51_selinux1 to 2.4.25 final
- drop SL41_enable_xfs_acl.patch (merged in 0.8.71 series)

* Wed Mar 31 2004 Thomas Backlund <tmb@iki.fi> 2.4.25-9sls
- add support for 3rdparty drivers
- minor cleanups
- full patchlist:
- DC45_pci.ids_20040331tmb.patch
  * updates pci.ids to 2004-03-31 + my addons
- MB01_3rdparty-1.0.tar
  * basesystem for 3rdparty modules
- MB02_3rdparty_merge.patch
  * 3rdparty config and makefile handling
- MB10_bcm5820_ssl_accelerator.tar
  * add support for Broadcom bcm5820 SSL accelerator
- MB11_bcm5820_license_tag.patch
  * fixes license on bcm5820
- MB12_bcm5820_rotate_left.patch
  * fix bcm5820 rotate_left
- MB13_bcm5820_lots_of_fixes.patch
  * more fixes to bcm5820
- MB20_bcm44xx_3.0.7.tar
  * add support for Broadcom 44xx series NIC
- MB30_bcm57xx_7.1.9.tar
  * add support for Broadcom 57xx series NIC
- MB40_pdc_ultra_1.00.0.10.tar
  * support Promise ultra IDE controllers
- MB41_pdc_ultra_no_mmio.patch
  * add missing ifdef MMIO to pdc_ultra
- MB42_pdc_20376.patch
  * support another Promise SATA150 chip
- MB43_pdc_20319.patch
  * support another Promise SATA150 TX4 chip
- MB44_pdc-ultra_unused_var.patch
  * remove unused var from pdc-ultra
- MB45_pdc_ultra_updates.patch
  * more updates to Promise pdc_ultra and some security fixes
- MB50_ppp-mppe-0.9.6.tar
  * adds support for mppe en+crypted pptp
- ZA01_license_tags.patch
  * fix some missing license tags
- ZA02_endif_compilation_fixes.patch
  * removes some compilation complaints
- ZZ01_fix_bugreport_addresses.patch
  * fix bugreport address to point to OpenSLS, 
    and remove some obsolete info

* Mon Mar 29 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-8sls
- add support for i2c/lmsensors
- usb fixes, filesystem fixes
- amd64 fixes
- full patchlist:
- DL01_i2c_2.8.4.patch
  * adds i2c monitoring support
- DL03_lm_sensors_2.8.4.patch
  * adds lm-sensors support
- DL04_add_sensors.h.patch
  * fix missing sensors.h
- DL05_scx200_acb_i2c_fixes.patch
  * fixes scx200_acb i2c for 2.8.4
- DL06_scx200_i2c_fixes.patch
  * fixes scx200 i2c for 2.8.4
- DL07_stradis_i2c_fixes.patch
  * fixes stradis i2c for 2.8.4
- DL08_acorn_char_i2c_fixes.patch
  * fixes acorn i2c for 2.8.4
- DL09_i2c-adap-ite_i2c_fixes.patch
  * fixes adap-ite i2c for 2.8.4
- DL10_i2c_nforce2.patch
  * adds missing i2c support for nForce2
- DL13_dmasound_i2c_fix.patch
  * fixes dmasound i2c for 2.8.4
- DM04_fosa340S_incorrect_apm_version.patch
  * workaround buggy fosa3340S that reports wrong apm version
- DM05_legacyfree_e-pc43.patch
  * fix for legacyfree keyboards on e-pc
- DM06_hp_local_apic_kill_bios.patch
  * disable local apic on hp e-pc
- DM07_more_no_local_apic.patch
  * blacklist local apic on Compaq Presario 711EA, MSI-6380E
- DM08_acpi_apm_blacklist.patch
  * blacklist acpi_table_dsdt  on Via964, IBM TP-16/T21, 
    Intel Trajan, Sharp QS1.
  * blacklist apm on Sony Vaio PCG-Z600RE
- DM09_hp_d325_pci_noacpi.patch
  * disable acpi on hp d325
- DM10_toshiba_sattellite_noapic.patch
  * disable apic on Toshiba Satellite 2435
- DM11_disable_local_apic_hp_pavillion_ze43xx.patch
  * disable local apic on hp pavillion ze43xx
- DS04_trident_fixes.patch
  * fix trident/ali ac97 audio driver
- DU01_usbserial_fix_disconnect.patch
  * fix disconnect on usbserial
- DU03_kaweth_disable_debug.patch
  * disable debugging on kaweth
- DU04_du_e100_support.patch
  * adds another usb ethernet support
- DU06_usbdnet_update.patch
  * update usbnet, adds support for usb host to host transfers
  * adds support for safe (encapsulated) usb serial transfers
- DU15_usbdnet_usb_serial_device_type_changed.patch
  * fix safe_serial module
- DU18_ibm_ix00_lookup.patch
  * fix usb hangs on IBM i1200/i1300
- DU19_usb_vai_pcg_fx503_fix.patch
  * fix usb irq on sony vaios
- DU20_scanlogic_support.patch
  * fix for Scanlogic usb-ide
- DU21_usb_storage_unusual_devs.patch
  * add support for many usb storage devices
- DU23_usb_storage_US_FL_INIT_RESET.patch
  * add support for usb reset on init
- DU26_safe_serial_cleanup.patch
  * clean up safe_serial drivers
- DU30_w9968_fix_compilation.patch
  * fixes compilation errors on usb w9968
- DV08_i810fb-0.23.patch
  * add support for i81x framebuffer
- DV21_vesafb_vram_option_docs.patch
  * fix text vesafb documentation
- DV22_video_i2c_fixes.patch
  * fix video i2c for 2.8.4
- FB02_autoload_freevxfs.patch
  * fix freevxfs autoloading
- FB04_enable_xfs_acl.patch
  * readd support for ACL on XFS
- FC01_davfs_0.2.4.patch
  * add support for WebDAV filesystems
- FC02_davfs__FUNCTION__.patch
  * fix WebDAV driver
- FD01-devfs-dynamic-disk.patch
  * devfs dynamic disk support
- FD02_devfs_for_rawio.patch
  * devfs rawio support
- FD03_devfs_minilogd_fix.patch
  * fix devfs minilog hang
- FD04_dos_partition_table_consistency.patch
  * adds check for partition table consitency
- FE02_BUF_LOCKED.patch
  * fix post-processing on locked buffers
- FN05_iocharset.patch
  * disable complaints about ntfs "iocharset is depreceated, use nls=..."
- FS63_fat_not_readonly.patch
  * disable extra readonly chack as the VFS alrady have checked it
- FS91_file_readahead_ide_cd_and_floppy.patch
  * modifiy readaheads for ide-cd and floppys
- FX10_fix_xfs_VM_IO.patch
  * adds missing VM_IO to xfs
- G01_ppa_no_cable_warning.patch
  * suppress warning about nonexistant ppa cable
- G02_ldm_validate_partition_table.patch
  * fix ldm partition table warnings
- HB09_binfmt_name.patch
  * fix binfmt name on amd64
- HB25_aa_mm.patch
  * fix mm on amd64
- HB26_aa_numa.patch
  * fix numa on amd64
- HB29_amd64_kallsyms.patch
  * add kallsyms to amd64
- HB30_acpi_on.patch
  * support acpi=on boot option for amd64

* Sat Mar 27 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-7sls
- mostly driver fixes, some addons
- adds aes encrypted loop support
- full patchlist:
- DB07_scsi_kmod_fix_pb_initrd.patch
  * dont have kmod request scsi_hostadapter when scsi support 
    is built as modules
- DC01_scsi_timeout.patch
  * change scsi scan timeout from 30 to 60 sec
- DC03_hide_ip_interface.patch
  * add support for hiding ip addresses
- DC04_sse_for_raid5xor.patch
  * use sse intructions for raid5 xor if possible
- DC05_eepro100_fix.patch
  * fix eepro100 nic loosing resources
- DC08_e820_proc.patch
  * add suooprt for e820
- DC10_isdn_olitec_gazel.patch
  * add support for ISDN olitec
- DC12_loop_AES_1.7a.patch
  * add support for encrypted loopback
- DC15_ecc_check.patch
  * add support for eec checking
- DC18_ppp_mppe_support.patch
  * add support for mppe in ppp headers
- DC22_ecc_add_another_amd.patch
  * add support for another ecc system
- DC23_legacyfree_keyboard.patch
  * add support for systems with legacyfree boards
- DC24_md_quiet.patch
  * quiet down md messages
- DC26_scsi_error_timeout.patch
  * fix scsi timing out errors
- DC29_convert_aes_to_module.patch
  * converts aes to module
- DC30_loop_set_current_state.patch
  * fix aes loop stuck in 'D' state
- DC31_aes_module_license.patch
  * correct aes licence
- DC34_eepro100_ICH5.patch
  * add ICH5 ids to eepro100 driver
- DC35_aic7xxx_build_fixes.patch
  * add missing ifdef MMAPIO
- DC38_mmc3_support.patch
  * add support for mmc-3 dwd+rw
- DC47_sungem_64bit_ULL.patch
  * sungem needs to be 64bit ULL
- DC50_cciss_size_of_vars.patch
  * ccis needs to be 64bit ULL
- DC59_scsi_qlogic_fixes.patch
  * qlogic needs to be 64bit ULL
- DI93_ide_scsi_device_selection.patch
  * ide-scsi should only claim requested drives
- DI95_ide_small.patch
  * make ide subsystem small in BOOT kernels
- DI97_quiet_ide.patch
  * quiet down ide complaints
- DI98_ide_proc_write_driver.patch
  * fix /proc/ide/hdX/driver for ide_scan_device

* Fri Mar 26 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-6sls
- some kernel fixes, some acpi fixes, some apic fixes
- add upport for DSDT in initrd
- add Andreas VM, kernel debugger
- add Juans mini-lowlatency fixes
- full patchlist:
- CA05_main-more-args.patch
  * adds support for more kernel boottime args
- CB02_speed_bootmem_check.patch
  * speedup bootmem check
- CB05_warn_if_not_ulong.patch
  * warn if parameters are not ulong
- CB07_enable_lapic_as_default.patch
  * enables local apic by default
- CB08_fix_menuconfig.patch
  * fix menuconfig for long menus
- CB09_fix_ver_linux_head.patch
  * fix ver_linux report
- CB10_dmi_data_fixes.patch
  * fix dmi_scan checks
- CC02_vm-cleanups-3.patch
  * use Andrea Arcangeli's VM
- CC03_vm_raend-race-1.patch
  * use Andrea Arcangeli's VM
- CC04_VM_IO-4.patch
  * use Andrea Arcangeli's VM
- CC05_silent-stack-overflow-20.patch
  * use Andrea Arcangeli's VM
- CC06_anon-lrp-race-butter-fix-1.patch
  * use Andrea Arcangeli's VM
- CC07_execve-mm-fast-path-safe-1.patch
  * use Andrea Arcangeli's VM
- CC12_try_to_free_pages_nozone-4.patch
  * use Andrea Arcangeli's VM
- CC14_read_write_tweaks-3.patch
  * use Andrea Arcangeli's VM
- CC16_activate_page_cleanup-1.patch
  * use Andrea Arcangeli's VM
- CC18_active_page_swapout-1.patch
  * use Andrea Arcangeli's VM
- CC21_buffer-page-uptodate-1.patch
  * use Andrea Arcangeli's VM
- CC24_rt-alloc-1.patch
  * use Andrea Arcangeli's VM
- CC25_vm-anon-lru-3.patch
  * use Andrea Arcangeli's VM
- CC26-per-cpu-pages-4.patch
  * use Andrea Arcangeli's VM
- CC28_try_to_free_buffers-invariant-1.patch
  * use Andrea Arcangeli's VM
- CC29_rest-2.patch
  * use Andrea Arcangeli's VM
- CC30_pte-dirty-bit-in-hardware-1.patch
  * use Andrea Arcangeli's VM
- CC40_numa-mm-7.patch
  * use Andrea Arcangeli's VM
- CD05_print_also_hexblocknumber.patch
  * printt inode block as hex too
- CD06_cardmanager_version.patch
  * fix reported cardmanager version
- CD09_lowlatency-fixes-14.patch
  * Juans mini-lowlatency patch
- CE01_keyboardsilence.patch
  * dont report keyboard timeouts
- CE03_apic_quiet.patch
  * make apic errors more silent
- CE04_oomavoidance.patch
  * fix pgalloc schedule_timeout
- CE05_no_ps2mouse.patch
  * fix missing ps2mouse init
- CE06_tcp_allow_options_after_00.patch
  * allow netfilter ipt_unclean options after 00
- CE08_Makefile_need_mrproper_support.patch
  * make sure kernel build knows when mrproper is needed
- CE12_twaked_dsdt_initrd.patch
  * allow support for loading tweaked DSDT table from initrd
- CE13_boot_kernel_edid_vbe_info.patch
  * pass edid and vbe info from bootkernel (can be used in a graphical installer)
- CE20_lsb_ttyio.patch
  * fix ttyip pgrp check
- CE21_console_fix_overlapping_mem.patch
   fix console overlapping memory
- CE25_acpi=on.patch
  * add acpi=on support for ix86
- CE27_BadRAM.patch
  * add support for BadRAM excusions (light version of IBM ChipKill)
- CK01_kdb-v4.3-2.4.25-common-2.patch
  * add kernel debugger support
- CK02_kdb-v4.3-2.4.25-i386-1.patch
  * add kernel debugger support
- CK03_kdb_vmlinux.lds.patch
  * add kernel debugger support
- CK04_kdb_local_pages_dont_exist.patch
  * add kernel debugger support

* Wed Mar 24 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-5sls
- mostly code cleanups, patchlist follows:
- BA02_setup_move_functions.patch
  * reloacates flag_is_changeable macro
- BA03_usb_kaweth.patch
  * fixes private_header declaration
- BA10_i2o_block_unused_function.patch
  * removes unused function
- BA11_via_8231_irqrouter.patch
  * adds 2 VIA irq routers
- BA19_video_aty128fb_pmac_only_idfdefs.patch
  * aty128fb is pmac only
- BA20_video_pm3fb_ulong_cast.patch
  * fixes pm3fb ulong release_mem_region
- BA24_NCR820_unused_functions.patch
  * remove unused functions in NCR820
- BA28_i2o_pci_missing_prototype.patch
  * adds missing prototype
- BA42_awe_wave_right_isapnp_declaration.patch
  * fix sb awe isapnp declaration
- BA43_wd7000_initialize_p.patch
  * disables broken initializion check
- BA44_atm_mpc_right_colocation_attribute.patch
  * fix mpc attribute
- BA56_sound_ad1889.patch
  * fix ad1889 check
- BA58_ide_siimage.patch
  * adds missing return
- BA59_cardbus.patch
  * fix pci_device_scan
- BB02_fix_flags_definitions.patch
  * fix sym53c8xx flags variable
- BB04_befs_ULL.patch
  * make befs_bt_inval ULL
- BB05_matroxfb_remove_MINFO.patch
  * remove MINFO_FROM(md) call
- BE03_sstfb_debug_fix.patch
  * move variable that is used only for debugging
- BG01_af_irda.patch
  * removes unneeded length check
- BG04_video_riva_remove_error_out_kfree.patch
  * removes unused error_out_kfree
- BG05_usb_storage_sddr.patch
  * disables sddr09_request_sense
- BG08_amd74xx.patch
  * removes unused ata66_amd74xx check
- BG09_ide_generic.patch
  * disables unknown_chipset
- BG10_ns83820_PHY_CODE_IS_FINISHED.patch
  * adds missing ifdef...endif
- BG11_mtd_amd76xrom_err_out_none.patch
  * disables err_out_none
- BH02_intermezzo_fix_init.patch
  * fix intermezzo init
- BH03_hfs_variables.patch
  * fix variables init
- BH04_coda_vdir.patch
  * fix vdir check
- BH05_sound_ali5455.patch
  * fix variables init
- BI01_hamradio_scc.patch
  * fix hamradio variable init
- BI03_char_vt.patch
  * fix vt vhecks
- BI04_cpqhp_pci.patch
  * fix tdevice variable init
- BI05_isdn_fourbri.patch
  * fix variable init
- BJ01_hiddev_report_event.patch
  * add missing hiddev_report_event
- BJ02_isdn_ppp.patch
  * fix uprog.len check
- BJ04_net_bonding_bond_alb.patch
  * fix bond_alb_xmit check
- BJ05_iph5526_service_params_check.patch
  * fix iph5526 fibre channel service_params check
- BJ06_ppp_generic.patch
  * fix uprog.len check
- BJ07_tokenring_3c359.patch
  * fix variable init
- BJ08_pcmcia_DONT_SEND.patch
  * fix pcmcia transfer check
- BJ09_scsi_AM53C974.patch
  * fix hostdata transfer

* Fri Mar  5 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-4sls
- require atleast bootloader-utils 1.6-5sls
- conflict older iptables than 1.2.9-2sls
- BA16_nfs_rpc_call_sync_rename.patch
  * rename rpc call so it wont conflict
- BA29_pci-pc_lcall_right.patch
  * fix lcall
- BA30_apm_lcall_right.patch
  * fix lcall
- BA31_bootsect_lcall_right.patch
  * fix lcall
- BA32_setup_lcall_right.patch
  * fix lcall
- BA35_doc1000_smp.patch
  * doc1000 driver does not work with smp
- BI02_kmap.patch
  * fix kmap size
- CE02_autoconf.patch
  * autoconf magic by Chmouel to keep only one source for all kernels
- CE07_Makefile_preconfig_target.patch
  * include version.h in preconfig
- CE09_boot_kernel.patch
  * special buildoptions to make bootkernel smaller
- CE10_boot_kernel_video_tweaks.patch
  * video fallback if the selected one don't work
- CE11_i586-if-no-cmov.patch
  * treat all cpus that does not support cmov as i586
- DI02_ide_nforce3.patch
  * support nforce2, nforce3 and amd8111 ide chipsets up to udma133
- FA01_b_journal_head-1.patch
  * adds missing journal_head
- FA02_write_times.patch
  * fix update inode times
- FB03_fcntl_O_LARGEFILE.patch
  * adds O_LARGEFILE check to fcntl
- FF01_cifs_1.0.3cvs.patch
  * adds support for cifs protocol (better than smb)
- FN01_ntfs_2.1.6a.patch
  * updates ntfs support
- FN02_ntfs_ksyms_fix.patch
  * fix ksyms for ntfs and reiserfs
- FN03_end_buffer_io_async_prototype.patch
  * add missing prototype
- FN04_64bits_needs_ULL.patch
  * update to ULL to support 64bit
- FR01_reiserfs_sync_fs-4.patch
  * fix reiserfs sync
- FR02_reiserfs_data_logging-39.patch
  * add support for data logging
- FR03_reiserfs_quota-28.patch
  * add support for quota
- FR04_reiserfs_jh-3.patch
  * fix reiserfs journal head
- FR05_reiserfs_quota_link_fix.patch
  * fix resierfs quota link
- HB02-1_rng_support.patch
  * add another amd8111 systems manager support
- HB03_bigger_dmesg_buffer.patch
  * make larger dmesg buffer
- HB04_ioctl32_null_conversion.patch
  * fix ioctl32 null conversion
- HB05_amd64_exports.patch
  * add missing exports
- HB06_specific.patch
  * disable token ring on amd64
- HB08_define_fls.patch
  * add missing fls define
- HB09_binfmt_name.patch
  * add names to binfmt
- HB11_open_ia32_hack.patch
  * fix fs_open
- HB15_do_gettimeoffest_safe.patch
  * add gettimeoffset_safe to timer
- HB16_expand_stack.patch
  * fix expand stack
- HB21-2_cflags_optimize.patch
  * disable some optimizations
- HB22_include_lib_config.in.patch
  * include lib in kernel config
- HB24_dont_use_do_gettimeoffset_safe.patch
  * use gettimeoffset instead of gettimeoffset_safe
- HB28_amd64_boot_kernel.patch
  * optimize boot kernels for size
- HB29_amd64_kallsyms.patch
  * add kallsyms support to amd64
- HB31_amd64_pcmcia.patch
  * fix pci mem allocations
- ND01_forcedeth.patch
  * add support for nforce ethernet

* Wed Mar  3 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-3sls
- AA01_compile_fixes.patch
  * fixes mips specific code
- AA01_fix_Rules_make.patch
  * fixes Rules.make
- AA02_force-inline-memcmp.patch
  * workaround newer gcc when building with __OPTIMIZE_SIZE__
- AD01_rename_vmlinux.lds_vmlinux.lds.in.sh
  * renames vmlinux.lds and...
- AD02_generate_vmlinux.lds.patch
  * recreates a correct one
- DP01_imq.patch
  * adds support for Intermediate Queueing device, needed for QoS
- enable IMQ provided by DN20, DN21
- SL01_ea_0.8.68.patch
  * adds support for extended attributes
- SL11_acl_0.8.70.patch
  * adds support for Access Control Lists
- SL21_nfsacl_0.8.70.patch
  * adds ACL for NFS
- SL31_sec_0.8.69.patch
  * adds support for security descriptors 
- SL41_enable_xfs_acl.patch
  * enables ACL on XFS
- SL51_selinux1.patch
  * adds NSA SELinux 
    
* Mon Mar  1 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-2sls
- DF01_freeswan-2.0.5.patch
  * adds support for freeswan ipsec vpn
- add full iptables capabilities (based on mdk patches):
  * DN02_74_nat-range-fix.patch
    - fixes logic bug in NAT range calulations
  * DN10_nth.patch
    - adds support for Nth match filtering rules on IPv4
  * DN11_nth6.patch
    - adds support for Nth match filtering rules on IPv6
  * DN12_psd.patch
    - adds support for psd filtering rules, detects tcp/udp portscans
  * DN13_time.patch
    - adds support for packet arrival/departure filtering rules
  * DN14_h323_conntrack-nat.patch
    - adds NAT connection tracking for h.323 protocol 
  * DN15_ipt_TARPIT.patch
    - adds support for TARPIT filtering rules
  * DN16_pptp_conntrack-nat.patch
    - adds NAT connection tracking for pptp protocol 
  * DN17_string.patch
    - adds support for filtering based on specific strings
  * DN20_IMQ.patch
    - adds IMQ target support for IPv4
  * DN21_IMQ_ipv6.patch
    - adds IMQ target support for IPv6
  * DN90_match_stealth.patch
    - add support for stealth filtering of syn packets
  * DN91_iplimit.patch
    - adds support for limiting connections by IP address or address blocks
  * DN92_license_tags.patch
    - adds missing licences

* Sun Feb 29 2004 Thomas Backlund <tmb@mandrake.org> 2.4.25-1sls
- Start fresh with 2.4.25 - First OpenSLS specific build
- base specs/buildsystem on current kernel-tmb and mdk specs
  * remove unneeded info/functions/defines from spec and scripts
- rename kernel top_dir to kernel-sls so it can coexist with mdk
- rename all files in SOURCES so they can coexist with mdk kernels
- make kernel-source always readable by all (chmod -R a+rX)
- kernel-build is now smp + highmem
- add .desc description files for patches tree
- add patch.index in the patch tarball to keep track of all patches
- ZY01_ProPolice.patch
  * enable propolice stack protection

# Local Variables:
# rpm-spec-insert-changelog-version-with-shell: t
# End:
