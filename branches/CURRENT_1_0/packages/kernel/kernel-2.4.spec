# -*- Mode: rpm-spec -*-
# 	$Id: kernel-2.4.spec,v 1.1 2001/09/25 08:55:44 chmou Exp chmou $

# First: Get versions names right is complicated (tm)
# Second: kernel allways have the version & release number in the name
#         this is done to preserving a working kernel when you install 
#         a new one
# Stored in %rpmrversion & %rpmrelease
#
# We want to reflect in the kernel naming:
#   - vanilla kernel in with is based (ex. 2.4.21) 
#     this version is stored in %realversion
#   - Number of Mandrake kernel based on this vanilla kernel (ex. 2mdk).
#     stored in %mdkrelease.
#    
# That gives us a nice name: 2.4.21.2mdk
# 
# As version and release are allways fixed, name of the package is 
# going to be:
#        kernel-2.4.21.2mdk-1-1mdk
#
# Confused already?
#
# Now there arrive pre/rc kernels.  This kernels have the particularity
# that they have the name of the new kernel, but they are based in the
# tar file of the old kernel, i.e. names are basically:
#  - vanilla kernel: 2.4.21
#  - patch name: 2.4.22-pre3
#    stored in %use_patch
#  - Number of Mandrake kernel based in this pre kernel 2mdk
#
# That gives us a nice name again: 2.4.22.pre3.2mdk
# Problems now are:
#   - sublevel of vanilla kernel 21 (needed for tar file)
#   - sublevel of kernel is 22 (needed for prepatch and naming 
#     the package).
# This explains the need of %tar_version, because this will be different
# of %real_version if there is a pre/rc patch.
# 
# Still with me?
# 
# There are still a problem, when real 2.4.22 cames out, it will have
# a mane like: 
#              2.4.22.1mdk
# this name is (for rpm ordering of versions) smaller than:
#              2.4.22.pre3.2mdk
# to fix that we add a 0 to the name (and appear the need of realrelease)
# in the pre/rc
# 	       2.4.22.0.pre3.2mdk
#
# Take one aspirine.  Relax.
#
# Problem now is that names are just really ugly, and specially
# lilo/grub names are very difficult to read/type.
# Notice that the extra .0 is there only to make visual comparations 
# easy, but it is an annoyance.
#
# Lilo name for this kernel will be:
#       2422-0.pre3.2mdk
# And as everybody knows, putting dot's in lilo names is not nice.
# Then we change the kernel name (for loaders, and directory names only)
# to a more userfriendly:
# 		2.4.22pre3-2mdk
# That way, smp, enterprise versions continue to have the well known names
# in the loader of:
#		2422pre3-2smp
#
# For a non pre/rc kernel define (real examples in brakets)
#     2.4.X.Ymdk [2.4.22.2mdk]
# where
#	%sublvel = X 	[22]
#   	%mdkrelease = Y [2]
#	%use_patch 0	[0]
#
# For a pre/rc kernel do:
#	2.4.X.0.Y.Zmdk [2.4.22.0.pre3.2mdk]
# where
#	%sublvel = X 	[22]
#   	%mdkrelease = Z [2]
#	%use_patch Y	[pre3]
#
# I hope this is all clear now. If you have any doubt, please mail me at:
#
# Juan Quintela <quintela@mandrakesoft.com>

%define sublevel 22
%define mdkrelease 21
%define use_patch 0

# You shouldn't have to change any kernel/patch/version number
# for 2.4 kernels

# When we are using a pre/rc patch, the tarball is a sublevel -1
%if %use_patch
%define tar_version 2.4.%(expr %sublevel - 1)
%define patchversion %{use_patch}q%{mdkrelease}
%define realrelease 0.%{mdkrelease}mdk
%else
%define tar_version 2.4.%sublevel
%define patchversion q%mdkrelease
%define realrelease %{mdkrelease}mdk
%endif

# never touch the folowing two fields
%define rpmversion 1
%define rpmrelease 1mdk
%define realversion 2.4.%{sublevel}
%define mdkversion %{realversion}.%{realrelease}
%define patches_ver 2.4.%{sublevel}-%{patchversion}

# having different top level names for packges means
# that you have to remove them by hard :(
%define top_dir_name kernel-2.4

%define build_dir ${RPM_BUILD_DIR}/%top_dir_name
%define src_dir %{build_dir}/linux-%tar_version
%define KVERREL %{realversion}-%{realrelease}

# this is the config that contains all the drivers for the hardware/
# things that I use (Juan Quintela).
%define build_minimal 0
%define build_acpi 1

%define build_kheaders 0
%define build_debug 0
%define build_doc 1
%define build_source 1

%define build_92 %(if [ `awk '{print $4}' /etc/mandrake-release` = 9.2 ];then echo 1; else echo 0; fi)
%define build_91 %(if [ `awk '{print $4}' /etc/mandrake-release` = 9.1 ];then echo 1; else echo 0; fi)
%define build_90 %(if [ `awk '{print $4}' /etc/mandrake-release` = 9.0 ];then echo 1; else echo 0; fi)
%define build_82 %(if [ `awk '{print $4}' /etc/mandrake-release` = 8.2 ];then echo 1; else echo 0; fi)

%define build_up 1
%define build_smp 1

%ifarch alpha x86_64 ia64
%define build_enterprise 0
%else
%define build_enterprise 1
%endif

%ifarch %{ix86} x86_64
%define build_BOOT 1
%else
%define build_BOOT 0
%endif

%ifarch %{ix86} x86_64
%define build_secure 1
%else
%define build_secure 0
%endif

%ifarch %{ix86}
%define build_i686_up_4GB 1
%define build_p3_smp_64GB 1
%else
%define build_i686_up_4GB 0
%define build_p3_smp_64GB 0
%endif

# End of user definitions
%{?_without_up: %global build_up 0}
%{?_without_smp: %global build_smp 0}
%{?_without_secure: %global build_secure 0}
%{?_without_enterprise: %global build_enterprise 0}
%{?_without_BOOT: %global build_BOOT 0}
%{?_without_i686up4GB: %global build_i686_up_4GB 0}
%{?_without_p3smp64GB: %global build_p3_smp_64GB 0}
%{?_without_minimal: %global build_minimal 0}
%{?_without_debug: %global build_debug 0}
%{?_without_doc: %global build_doc 0}
%{?_without_source: %global build_source 0}

%{?_with_up: %global build_up 1}
%{?_with_smp: %global build_smp 1}
%{?_with_secure: %global build_secure 1}
%{?_with_enterprise: %global build_enterprise 1}
%{?_with_BOOT: %global build_BOOT 1}
%{?_with_i686up4GB: %global build_i686_up_4GB 1}
%{?_with_p3smp64GB: %global build_p3_smp_64GB 1}
%{?_with_minimal: %global build_minimal 1}
%{?_with_debug: %global build_debug 1}
%{?_with_acpi: %global build_acpi 1}
%{?_with_doc: %global build_doc 1}
%{?_with_source: %global build_source 1}

%{?_with_kheaders: %global build_kheaders 1}
%{?_with_82: %global build_82 1}
%{?_with_90: %global build_90 1}
%{?_with_91: %global build_91 1}
%{?_with_92: %global build_92 1}

%define build_modules_description 1

%if %build_82
%define build_modules_description 0
%endif

%define kmake %make
# there are places where parallel make don't work
%define smake make

# Aliases for amd64 builds (better make source links?)
%define target_cpu	%(echo %{_target_cpu} | sed -e "s/amd64/x86_64/")
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/")

Summary: The Linux kernel (the core of the Linux operating system).
Name: kernel-%{mdkversion}
Version: %{rpmversion}
Release: %{rpmrelease}
License: GPL
Group: System/Kernel and hardware
ExclusiveArch: %{ix86} alpha ppc ia64 x86_64 amd64
ExclusiveOS: Linux
URL: http://www.kernel.org/

####################################################################
#
# Sources
#
Source0: ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-%{tar_version}.tar.bz2
Source4: README.kernel-sources
Source5: README.Mandrake

Source15: linux-mdkconfig.h
Source16: linux-merge-config.awk
Source17: linux-merge-modules.awk

Source100: linux-%{patches_ver}.tar.bz2

####################################################################
#
# Patches

#
# Patch0 to Patch100 are for core kernel upgrades.
#

# Pre linus patch: ftp://ftp.kernel.org/pub/linux/kernel/v2.4/testing

%if %use_patch
Patch1: patch-%realversion-%use_patch.bz2
%endif

#END
####################################################################

# Defines for the things that are needed for all the kernels
%if %build_82
%define requires1 modutils >= 2.4.13-3mdk
%else
%define requires1 modutils >= 2.4.15-1mdk
%endif

%define requires2 mkinitrd >= 3.1.6-24mdk
%define requires3 bootloader-utils >= 1.6

%define conflicts kernel-pcmcia-cs <= 2.4.8-26mdk, iptables <= 1.2.4-1mdk, ksympoops < 2.4.9
%define kprovides kernel = %{realversion}, alsa

BuildRoot: %{_tmppath}/%{name}-%{realversion}-build
Provides: module-info, %kprovides
Autoreqprov: no
Requires: %requires1
Requires: %requires2
Requires: %requires3
%if %build_92
BuildRequires: gcc >= 3.3.1-0.6mdk
%else
BuildRequires: gcc
%endif
Conflicts: %conflicts
Obsoletes: alsa, hackkernel, adiusbadsl_kernel
Provides: alsa, hackkernel, adiusbadsl_kernel


%description
The kernel package contains the Linux kernel (vmlinuz), the core of your
Mandrake Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

#
# kernel-smp: Symmetric MultiProcessing kernel
#

%package -n kernel-smp-%{mdkversion}
Summary: The Linux Kernel compiled for SMP machines.
Group: System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3

%description -n kernel-smp-%{mdkversion}
This package includes a SMP version of the Linux %{realversion} kernel. It is
required only on machines with two or more CPUs, although it should work
fine on single-CPU boxes.

%package -n kernel-secure-%{mdkversion}
Summary: The Linux Kernel compiled for SECURE machines.
Group: System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3

%description -n kernel-secure-%{mdkversion}
This package includes a SECURE version of the Linux %{realversion}
kernel. This package add options for kernel that make it more secure
for servers and such. See :

http://grsecurity.net/features.php

for list of features we have included.

#
# kernel-enterprise: Symmetric MultiProcessing kernel
#

%package -n kernel-enterprise-%{mdkversion}
Summary: The Linux Kernel compiled with options for Enterprise server usage.
Group: System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3

%description -n kernel-enterprise-%{mdkversion}
This package includes a kernel that has appropriate configuration options
enabled for the typical large enterprise server.  This includes SMP support
for multiple processor machines, support for large memory configurations
and other appropriate items.

#
# kernel-boot: BOOT Kernel
#

%package -n kernel-BOOT-%{mdkversion}
Summary: The version of the Linux kernel used on installation boot disks.
Group: System/Kernel and hardware
Url: https://kenobi.mandrakesoft.com/~chmou/kernel/BOOT/

%description -n kernel-BOOT-%{mdkversion}
This package includes a trimmed down version of the Linux kernel.
This kernel is used on the installation boot disks only and should not
be used for an installed system, as many features in this kernel are
turned off because of the size constraints.


%package -n kernel-i686-up-4GB-%{mdkversion}
Summary: The Linux Kernel compiled for smp with 4GB.
Group: System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3

%description -n kernel-i686-up-4GB-%{mdkversion}
This package includes a kernel that has appropriate configuration options
enabled for the typical desktop with more than 1GB of memory.


%package -n kernel-p3-smp-64GB-%{mdkversion}
Summary: The Linux Kernel compiled with options for pentium III, smp and 64GB memory.
Group: System/Kernel and hardware
Provides: %kprovides
Requires: %requires1
Requires: %requires2
Requires: %requires3

%description -n kernel-p3-smp-64GB-%{mdkversion}
This package includes a kernel that has appropriate configuration options
enabled for the typical large enterprise server.  This includes SMP support
for multiple processor machines, support for large memory configurations (64GB)
and support for pentium III.


%package -n kernel-source
Version: %{realversion}
Release: %{realrelease}
Requires: glibc-devel, ncurses-devel, make, gcc
Summary: The source code for the Linux kernel.
Group: Development/Kernel
Obsoletes: alsa-source
Provides: alsa-source

%description -n kernel-source
The kernel-source package contains the source code files for the Linux
kernel. These source files are needed to build most C programs, since
they depend on the constants defined in the source code. The source
files can also be used to build a custom kernel that is better tuned to
your particular hardware, if you are so inclined (and you know what you're
doing).

#
# kernel-doc: documentation for the Linux kernel
#
%package -n kernel-doc
Version: %{version}
Release: %{release}
Summary: Various documentation bits found in the kernel source.
Group: Books/Computer books

%description -n kernel-doc
This package contains documentation files form the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. You also might want install this
package if you need a reference to the options that can be passed to Linux
kernel modules at load time.

#
# End packages - here begins build stage
#
%prep
%setup -q -n %top_dir_name -c

%setup -q -n %top_dir_name -D -T -a100

%define patches_dir ../%{patches_ver}/

cd %src_dir
%if %use_patch
%patch1 -p1
%endif


%{patches_dir}/scripts/apply_patches

# PATCH END
#
# Setup Begin
#

# Prepare all the variables for calling create configs

%if %build_debug
%define debug --debug
%else
%define debug --no-debug
%endif

%if %build_acpi
%define acpi --acpi
%else
%define acpi --no-acpi
%endif

%if %build_minimal
%define minimal --minimal
%else
%define minimal --no-minimal
%endif

%{patches_dir}/scripts/create_configs %debug %acpi %minimal --user_cpu="%{target_cpu}"

# make sure the kernel has the sublevel we know it has...
LC_ALL=C perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile

# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' |xargs rm -f

%if %build_kheaders

kheaders_dirs=`echo $PWD/include/{asm-*,linux,sound}`

pushd %build_dir
install -d kernel-headers/
cp -a $kheaders_dirs kernel-headers/
tar cf kernel-headers-%mdkversion.tar kernel-headers/
bzip2 -9f kernel-headers-%mdkversion.tar
rm -rf kernel-headers/
# build_kheaders
%endif


%build
# Common target directories
%define _kerneldir /usr/src/linux-%{KVERREL}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _savedheaders ../../savedheaders/

# Directories definition needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}

DependKernel() {
	name=$1
	extension=$2
	echo "Make dep for kernel $extension"
	%smake -s mrproper

	# We can't use only defconfig anyore because we have the autoconf patch,

	if [ -z "$name" ]; then
		config_name="defconfig"
	else
		config_name="defconfig-$name"
	fi
		cp arch/%{target_arch}/$config_name .config

	# make sure EXTRAVERSION says what we want it to say
	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -$extension/" Makefile
	%smake oldconfig
	%smake dep
}

BuildKernel() {
	KernelVer=$1
	echo "Building kernel $KernelVer"

	%ifarch alpha
	%kmake boot
	%endif    

	%ifarch ppc
	%kmake zImage
	%endif

	%ifarch %{ix86} x86_64
	%kmake bzImage
	%endif

	%kmake modules

	# first make sure we are not loosing any .ver files to make mrporper's
	# removal of zero sized files.
	find include/linux/modules -size 0 | while read file ; do \
		echo > $file
	done

	## Start installing stuff
	install -d %{temp_boot}
	install -m 644 System.map %{temp_boot}/System.map-$KernelVer
	install -m 644 .config %{temp_boot}/config-$KernelVer

	%ifarch alpha
	cp -f arch/alpha/boot/vmlinux.gz %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%ifarch ppc
	cp -f vmlinux %{temp_boot}/vmlinuz-$KernelVer
	cp -f arch/ppc/boot/images/zImage.chrp-rs6k %{temp_boot}/vmlinuz-rs6k-$KernelVer

	%endif
	%ifarch %{ix86}
	cp -f arch/i386/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif
	%ifarch x86_64
	cp -f arch/x86_64/boot/bzImage %{temp_boot}/vmlinuz-$KernelVer
	%endif

	# modules
	install -d %{temp_modules}/$KernelVer
	%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=$KernelVer modules_install 
}

SaveHeaders() {
	flavour=$1
	flavour_name="`echo $flavour | sed 's/-/_/g'`"
%if %build_source
	HeadersRoot=%{temp_source}/savedheaders
	HeadersArch=$HeadersRoot/%{target_cpu}/$flavour
	echo "Saving hearders for $flavour %{target_cpu}"

	# deal with the kernel headers that are version specific
	install -d $HeadersArch
	install -m 644 include/linux/autoconf.h $HeadersArch/autoconf.h
	install -m 644 include/linux/version.h $HeadersArch/version.h
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
%ifarch ppc
	echo "%{_bootdir}/vmlinuz-rs6k-${kversion}" >> $output
%endif
	echo "%{_bootdir}/System.map-${kversion}" >> $output
	echo "%dir %{_modulesdir}/${kversion}/" >> $output
	echo "%{_modulesdir}/${kversion}/kernel" >> $output
	echo "%{_modulesdir}/${kversion}/modules.*" >> $output
	echo "%doc README.kernel-sources" >> $output
	echo "%doc README.Mandrake" >> $output
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
	extension="%realrelease-$name"

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
cd %src_dir

%if %build_BOOT
CreateKernel BOOT
%endif

%if %build_smp
CreateKernel smp
%endif

%if %build_secure
CreateKernel secure
%endif

%if %build_enterprise
CreateKernel enterprise
%endif

%if %build_i686_up_4GB
CreateKernelNoName i686 up 4GB
%endif

%if %build_p3_smp_64GB
CreateKernelNoName p3 smp 64GB
%endif

%if %build_up
CreateKernel up
%endif

# We don't make to repeat the depend code at the install phase
%if %build_source
DependKernel "" %{realrelease}custom
%endif

###
### install
###
%install
install -m 644 %{SOURCE4}  .
install -m 644 %{SOURCE5}  .

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}

# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

# Create directories infastructure
%if %build_source
install -d %{target_source} 

tar cf - . | tar xf - -C %{target_source}
ln -sf linux-%{KVERREL} %{buildroot}/usr/src/linux

# we remove all the source files that we don't ship

# first architecture files
for i in arm cris mips mips64 parisc ppc64 s390 s390x sh sh64 sparc sparc64; do
	rm -rf %{target_source}/arch/$i
	rm -rf %{target_source}/include/asm-$i
done
# ppc needs m68k headers
rm -rf %{target_source}/arch/m68k

# my patches dir, this should go in other dir
rm -rf %{target_source}/%{patches_ver}

# other misc files
rm -f %{target_source}/{.config.old,.depend,.hdepend}

# We need this to prevent someone doing a make *config without mrproper
touch %{target_source}/.need_mrproper

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
install -m 644 %{SOURCE15} rhconfig.h
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
for i in smp enterprise up secure i686-up-4GB p3-smp-64GB; do
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
} ; popd
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
done

# sniff, if we gzipped all the modules, we change the stamp :(
# we really need the depmod -ae here

pushd %{target_modules}
for i in *; do
	/sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
	echo $?
done

%if %build_modules_description
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

export EXCLUDE_FROM_STRIP="vmlinuz-rs6k-%{KVERREL} vmlinuz-rs6k-%{KVERREL}smp vmlinuz-rs6k-%{KVERREL}enterprise vmlinuz-rs6k-%{KVERREL}BOOT"

###
### clean
###

%clean
rm -rf %{buildroot}
# We don't want to remove this, the whole reason of its existence is to be 
# able to do several rpm --short-circuit -bi for testing install 
# phase without repeating compilation phase
#rm -rf %{temp_root} 

###
### scripts
###

%preun
/sbin/installkernel -a -R -S -c %{KVERREL}
exit 0

%post
/sbin/installkernel -a -s -c %{KVERREL}

%postun
/sbin/kernel_remove_initrd %{KVERREL}


%preun -n kernel-smp-%{mdkversion}
/sbin/installkernel -a -R -S -c %{KVERREL}smp
exit 0

%post -n kernel-smp-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}smp

%postun -n kernel-smp-%{mdkversion}
/sbin/kernel_remove_initrd %{KVERREL}smp


%preun -n kernel-enterprise-%{mdkversion}
/sbin/installkernel -a -R -S -c %{KVERREL}enterprise
exit 0

%post -n kernel-enterprise-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}enterprise

%postun -n kernel-enterprise-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}enterprise


%preun -n kernel-BOOT-%{mdkversion}
/sbin/installkernel -a -R -S -c %{KVERREL}BOOT
exit 0

%post -n kernel-BOOT-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}BOOT

%postun -n kernel-BOOT-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}BOOT


%preun -n kernel-secure-%{mdkversion}
/sbin/installkernel -a -R -S -c %{KVERREL}secure
exit 0

%post -n kernel-secure-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}secure

%postun -n kernel-secure-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}secure


%preun -n kernel-i686-up-4GB-%{mdkversion}
/sbin/installkernel -a -R -S -c %{KVERREL}-i686-up-4GB
exit 0

%post -n kernel-i686-up-4GB-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}-i686-up-4GB

%postun -n kernel-i686-up-4GB-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}-i686-up-4GB


%preun -n kernel-p3-smp-64GB-%{mdkversion}
/sbin/installkernel -a -R -S -c %{KVERREL}-p3-smp-64GB
exit 0

%post -n kernel-p3-smp-64GB-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}-p3-smp-64GB

%postun -n kernel-p3-smp-64GB-%{mdkversion}
/sbin/installkernel -a -s -c %{KVERREL}-p3-smp-64GB


%post -n kernel-source
cd /usr/src
rm -f linux
ln -snf linux-%{KVERREL} linux
/sbin/service kheader start 2>/dev/null >/dev/null || :
# we need to create /build only when there is a source tree.

for i in /lib/modules/${KVERREL}*; do
	if [ -d $i ]; then
		ln -sf /usr/src/linux-%{KVERREL} $i/build
	fi
done

%postun -n kernel-source
if [ -L /usr/src/linux ]; then 
    if [ -L /usr/src/linux -a `ls -l /usr/src/linux 2>/dev/null| awk '{ print $11 }'` = "linux-%{KVERREL}" ]; then
	[ $1 = 0 ] && rm -f /usr/src/linux
    fi
fi
# we need to delete <modules>/build at unsinstall
for i in /lib/modules/${KVERREL}*/build; do
	if [ -L $i ]; then
		rm -f $i
	fi
done
exit 0

###
### file lists
###

%if %build_up
%files -f kernel_files.%{KVERREL}
%endif

%if %build_smp
%files -n kernel-smp-%{mdkversion} -f kernel_files.%{KVERREL}smp
%endif

%if %build_enterprise
%files -n kernel-enterprise-%{mdkversion} -f kernel_files.%{KVERREL}enterprise
%endif

%if %build_BOOT
%files -n kernel-BOOT-%{mdkversion} -f kernel_files.%{KVERREL}BOOT
%endif

%if %build_secure
%files -n kernel-secure-%{mdkversion} -f kernel_files.%{KVERREL}secure
%endif

%if %build_i686_up_4GB
%files -n kernel-i686-up-4GB-%{mdkversion} -f kernel_files.%{KVERREL}-i686-up-4GB
%endif

%if %build_p3_smp_64GB
%files -n kernel-p3-smp-64GB-%{mdkversion} -f kernel_files.%{KVERREL}-p3-smp-64GB
%endif

%if %build_source
%files -n kernel-source
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/.need_mrproper
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/REPORTING-BUGS
%{_kerneldir}/Rules.make
%{_kerneldir}/arch/alpha
%{_kerneldir}/arch/i386
%{_kerneldir}/arch/ia64
%{_kerneldir}/arch/ppc
%{_kerneldir}/arch/x86_64
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/fs
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kdb
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/scripts
%{_kerneldir}/sound
%{_kerneldir}/3rdparty
%{_kerneldir}/grsecurity
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-alpha
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/asm-i386
%{_kerneldir}/include/asm-ia64
# This is needed by ppc
%{_kerneldir}/include/asm-m68k
%{_kerneldir}/include/asm-ppc
%{_kerneldir}/include/asm-x86_64
%{_kerneldir}/include/asm
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/video
%doc README.kernel-sources
%doc README.Mandrake
#endif %build_source
%endif

%if %build_doc
%files -n kernel-doc
%defattr(-,root,root)
%doc linux-%{tar_version}/Documentation/*
%endif

%changelog
* Fri Oct 24 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-21mdk
- make xconfig should work again (svetoslav).
- remove packet writing patches (was killing LG CDROMS).
- ATM is now a module (and should work!).

* Fri Oct 24 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-20mdk
- enable support for ISDN & IrDA drivers
- really define CONFIG_BOOT_KERNEL on amd64 accordingly

* Thu Oct 23 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-19mdk
- update libata with sata_promise 0.83
- integrate the same -BOOT kernel video tweaks as for x86 to amd64
- add extraction of EDID & VBE blocks for amd64 & x86 -BOOT kernels

* Fri Oct 17 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-18mdk
- cloop 1.02.
- added Emulex driver (nplanel).
- grrr, more SATA hacking.

* Fri Oct 17 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-17mdk
- SATA should work again.

* Thu Oct 16 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-16mdk
- new adi id for ac97_codec.
- alsa-usb-audio fix (tmb).
- new qcamvc 1.0.6 driver, please told me if it works.
- ich3 minor ide fixes.
- nforce2 people have UDMA133 support (tmb).
- powernow k7 (from tmb), please test and report.
- redo acpi update to 2.4.23-pre6.
- fix BadRAM and HighMem (why nobody complained yet is a mistery).
- fix usb-audio.

* Wed Oct 15 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-15mdk
- fix exported symbols from libata
- really add support for VIA/nForce/8151 AGP

* Tue Oct 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-14mdk
- update libata state to 2003/10/10 with Promise SATA support
- lirc devfs fixes (nplanel)

* Tue Oct 14 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-13mdk
- lufs compiles again (as a side effect xconfig works again).
- hp d325 don't like pci acpi routing.
- tg3 update to 2.4.23-pre6.
- acpi update to 2.4.23-pre6.

* Fri Oct 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-12mdk
- Various updates to PDC ultra driver
- Various i810 audio fixes from 2.4.23pre5
- Add nForce3 IDE UDMA support
- Add VM overcommit accounting + new swapless mode
- Add (experimental) support for VIA/nForce3/8151 AGP
- AMD64 config updates:
  - Enable Intel ICH audio support (i810_audio)
  - Enable HW Random Number Generator support (hw_random)
- AMD64 updates from CVS (2003/10/10):
  - Fix pci=noacpi, maxcpus=0, noapic, nolocalapic options
  - Change ACPI to skip MADT APIC parsing when APICs are disabled
  - Fix RBP offset in ptrace.h and calling.h
  - Add missing smp_mb() in irq_enter()
  - Add Opteron prefetch errata
  - Remove unnecessary prefetches in copy_page, copy_user, csum_copy
  - Disable IO-APIC by default on Nvidia and VIA boards for now
  - Don't clear SMI IO-APIC pins
  - Workaround bugs in SMI override in some ACPI BIOS
  - Fix passing of __SI_POLL siginfo_t data to user space
  - IA-32 emulation layer fixes: stat, uids, statfs

* Tue Oct  7 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-11mdk
- av7 is good for acpi.
- libata driver for ICH5 and VIA SATA.
- 3ware patch to make smartmontools happy (erwan request).
- low latency fixes are back.
- enable TMPFS on BOOT (gc request).
- %%build_modules_description.

* Thu Sep 18 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-10mdk
- nfs fixes.
- disable PSC scanner.
- disable speedtouch module.

* Sat Sep 13 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-9mdk
- enable MTRR in BOOT.
- new i810fb driver.
- disable -fomit-frame-pointer at all. (break up somes modules ;()
- nfs fixies.
- fix reiserfs pb. (quintela)

* Thu Sep 11 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-8mdk
- enable local apic as default.
- fix ipt_MASQUERADE.
- change logic of refcnt pb.
- acpi irq reprogramming if it failed wwith standard descriptor. (quintela)
- alsa updates from cvs. (tmb)
   * ac97, emu10k1, es1968, ice1724, intel8x0
   * opl3sa2, pcm_native, via82xx

* Mon Sep  8 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-7mdk
- fixup linux-mdkconfig.h.
- Add usb-storage usbat2 CompactFlash reader.

* Sat Sep  6 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-6mdk
- fixup bad find ver hack (break up modversions hack when lots of kernel ;()
- LSB fix mprotect.
- fixup network layer, no more refcnt = 2 when you unloading network module ;).
- fix initrd sharing bug.
- fix precedence in filemap.
- ipc smp init.
- drm update.
- add 823x via irq router.
- reenable smbus on asus motherboard.
- update oss audio, new wd97xx ac97 driver.
- sk98lin 6.17.
- 3c59x pciids update.
- aacraid update.
- usbfs disconnect hack.
- fixup usb serial.
- net various fixes.
- icmp no BUG just drop.
- rework/update supermount to 1.2.9.
- following items from tmb:
  * hpt366 tune drive fix.
  * usb serial update.
  * usb storage update.
  * usb scanner update.
  * acx100 0.1h.
  * more alsa makfiles fixes.

* Fri Sep  5 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-5mdk
- make xconfig works again (lufs is fixed).
- fix another mising <linux/init.h> for firmware_class (gb).
- reenable i686-up-4GB and p3-smp-64GB, modversions should work now.
- mydsdt removed (now it is included in the initrd).

* Mon Sep  1 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-4mdk
- disable i686-up-4G and p3-smp-64GB until kernel-source get fixed.
- fix cardbus for AMD64 (gb).
- fix supermount for AMD64 (gb).
- AMD64 update (gb).
- print \n in tweaked dsdt.

* Fri Aug 29 2003 Juan Quintela <hummquintela@mandrakesoft.com> 2.4.22-3mdk
- redo the create_configs script in perl.
- after that and previous specfile changes, adding new kernels is a piece of cake.
- once there, make more sense of the BOOT kernels.
- enable w83527hf sensors module.
- update imq.
- remove ipvs (included upstream).
- new kernel-i686-up-4GB & kernel-p3-smp-64GB.

* Thu Aug 28 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-2mdk
- 2.4.23-pre1. (included in tarball to not break spec and .22 release
  for end of the distro)
- sam9407 1.0.4.
- mod_quickcam 0.5.1.
- super-freeswan 1.99.8.
- sheep_net 0.10.
- at76c503a_0.11beta4.
- drm savage & via.

* Mon Aug 25 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-1mdk
- 2.4.22 final.
- remove drm 20030816. (not the same branch than XFree)

* Sun Aug 24 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.22-0.8mdk
- 2.4.22-rc3.
- 2.4.22-rc3q8.
- acpi 20030813 (included in rc3).
- fix kdb with gcc3.1 frame pointer.
- now tweaked dsdt can be loaded from initrd. (like bootslash)
- cx2388x 20030820.
- netfilter TARPIT.
- dxr3 cvs 21082003. (fcrozat should be a happy man ;))
- prism25 0.2.1-pre11.
- atmelwlan 2.1.2.2.
- acx100-0.1g.

* Thu Aug 21 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-0.7mdk
- rename kernel-utils to bootloader-utils.
- 2.4.22-rc2q7.
  * lots of small fixes.  Warnings with gcc-3.3 moved from ~1000 to ~200.
    some of them were only cosmetic, but ~30 were real bugs.
  * small swsuspend fix.
  * BadRAM (tmb).
  * bluetooth_dynamic_firmware (tmb).
  * sbp2_enable_addrem_hack (tmb).
  * scsi_add_rem.patch (tmb).
  * update pwc 8.11.
  * i2c & lm_sensors addons (tmb).
  * update uss725 0.12).
  * update dri_20030816_and_via_cle (tmb).
  * update bttv-20030625 (tmb).
  * update cifs 0.8.7cvs (tmb).
  * agpgart ati igp (tmb).
  * update ipvs 1.0.10.
  * update acx100 0.1f (tmb).
  * supermount-ng 1.2.8 (tmb).
- fix grsecurity URL (tmb).
- use head -n (tmb).

* Fri Aug 15 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-0.6mdk
- disable ACPI_TWAKED_DSDT for x86_64.
- disable K8_NUMA for x86_64 BOOT_KERNEL.
- 2.4.22-rc2q6.

* Fri Aug 15 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-0.5mdk
- 2.4.22-rc2q5.
  * acpi update to 20030730-2.4.22-pre8.
  * xconfig works again.
  * ver_linux works again (tmb).
  * add alsa_rtc_support (tmb).
  * sk98lin update for 2.4.21.
  * add packet cdvd support (svetoslav).
  * update orinoco 0.13e.
  * add cloop 1.0 (tmb).
  * lots of i2c & alsa fixes (svetoslav).
  * stradis is back.
  * impi is back.
  * update audigy 0.20a (tmb).
  * update ov511 2.25.
  * add data journal & quota for reiserfs.
  * add devfs minilogd (tmb).
  * add cifs (tmb).
  * update vids (svetoslav?).
  * update mod_dvb (svetoslav).
  * update bcm5700 6.2.11 (tmb).
  * update bcm4400 2.0.2 (tmb).
  * update exaudio (svetoslav).
  * update hostap (tmb).
  * add mod_marvel (svetoslav & me).
  * add acx100 (svetoslav).
  * add mod_zoran (svetoslav).
  * add lufs (tmb).
  * lots of new alsa drivers (svetoslav).
  * fix the ipsec symlinks (tmb).
  * remove 3c990 and 3c990fx drives, obsoleted by typhoon.

* Wed Aug 13 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-0.4mdk
- 2.4.22-rc2q4.
- 2.4.22-rc2.
- conflict with ksymoops < 2.4.9 (kernel-utils name).
- %%files are now generated from the same template, no more repetitions.
- require kernel-utils >= 1.1.
- remove prereq.

* Mon Aug 11 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-0.3mdk
- Detect PDC20319, PDC20376 controllers
- Reintegrate NUMA fixes that got lost somehow

* Sun Aug 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.22-0.2mdk
- Fix build on AMD64: alsa (again!!), mptlinux, PnP driver in sound core
- Enable ACPI on AMD64
- Add Promise SATA150 drivers
- AMD64 updates (2003/08/10):
  * AGP aperture fixup
  * Make siginfo_t padding length match glibc
  * Handle CPUs with no own memory in NUMA discovery
  * Fix IOMMU TLB flush race
  * Handle SEMTIMEDOP in ipc32

* Fri Aug  8 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.22-0.1mdk
- remove low_latency patch, it hangs the system.
- depend on kernel-utils instead of initscripts.
- VIDEO_STRADIS don't build, disable for now.
- convince all 3rdparty i2c drivers to work with new api.
- rediff xfs.
- redo cryptoapi to convive with new crytpo in kernel.
- kdb 4.3 for 2.4.22-pre8.
- lm_sensors 2.8.0.
- i2c 2.8.0.
- update to andrea vm 2.4.22-pre6aa1.
- swsuspend 1.0.3.
- grsecurity 2.0-rc2.
- alsa 0.9.6.
- 2.4.22-pre10q1.
- 2.4.22-pre10.
- add amd64 to ExclusiveArch.

* Wed Jul 23 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.21-6mdk
- Fix generic console corruption (Ken Chen)
- Fix APIC version identification (Venkatesh Pallipadi)
- Fix Rules.make when compiling sources from other dirs
- Fix alsa ioctl32 on 64-bit platforms
- Fix amd64 ioctl32 with NULL conversion
- Fix megaraid/amd64 unresolved symbols
- Merge back AMD64 kernel:
  * Enable LOOP_AES, IPSEC, ACLs, GRKERNSEC (kernel secure)
  * Enable PCMCIA, I2C
  * Fix AMD64 NUMA with AA vm
  * Only printk for unhandled fault signals when exception_trace is set
  * Fix 32-bit getrlimit()/setrlimit()
  * Fix siginfo->si_band type and __SI_PAD_SIZE
  * Merge in grkernsec changes for AMD64 but without _PAX & _STACK stuff

* Tue Jul 22 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-5mdk
- require gcc-3.3.1-0.6mdk.
- s/-l/-L/.
- 2.4.21-q5.

* Mon Jul 21 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-4mdk
- update hostap 0.0.3.
- update adiusbadsl 1.0.4 (nplanel).
- update xfs for 2.4.21.
- update ntfs 2.1.4a.
- update sk98lin 6.12 (nplanel).
- update superfreeswan 1.99.7.3 (nplanel).
- update megaraid 1.18i (nplanel).
- update kdb 4.3.
- 2.4.21-q4.

* Fri Jul  4 2003 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- It should boot :p
- 2.4.21-q3.

* Mon Jun 30 2003 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- update adiusbadsl to 1.0.4-pre5.1 (and make sure that it compiles).
- compile the whole things with -fomit-frame-pointer, code is smaller.
- Don't you preffer -2mdk name instead of 0.0.2?
- Requires gcc-3.3-2mdk.
- 2.4.21-q2.

* Tue Jun 24 2003 Juan Quintela <quintela@trasno.org> 1-1mdk
- update cpufreq to 2.4.22-1 snapshot.
- update bootsplash to 3.0.7 (make warly happy).
- update andrea VM to rc8aa1.
- acpi 20030523.
- disabled several options 
- bcm4400 2.0.0 (thanks ronin).
- 2.4.21-final.

* Tue May  6 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.1mdk
- rediff patches for rc1.
- 2.4.21-rc1.

* Mon Apr 21 2003 Chmouel Boudjnah <chmouel@chmouel.com> 2.4s.21-0pre7.0.2mdk
- Fix ldm_validate_partition_table stuff (andrey).

* Wed Apr 16 2003 Nicolas Planel <nplanel@mandrakesoft.com> 2.4.21-0pre7.0.1mdk
- pre7.
- ACPI 20030218.
- cpufreq 20030414.
- cryptoapi 0.1.0. and super_freeswan 1.99.6.1.
- ov511 2.23.
- usbvision 0.3.3-test4.
- spca50x 0.30. (new camera driver)
- bttv 0.7.106 and bttv 0.9.10 (bttv9 module)
- saa7134 0.2.6.
- cx2388x 20030403. (connexant TV chipset)
- ntfs 2.1.2a.
- mmc3 support. (http://fy.chalmers.se/~appro/linux/DVD+RW)
- dxr3 0.13.0.
- mod_dvb 1.0.0-pre2.
- alsa 0.9.2.

* Thu Apr 10 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.16mdk
- swsuspend beta19 (chmouel).
- irq balance patch, now irq should be distrtibuted evenly in SMP.
- via-rhine 1.1.16 (tmb).
- ieee1394_rev848 (tmb).
- orinoco 1.13c (tmb).
- vesafb_vram_option (tmb).
- several ext3 updates (sct).

* Tue Apr  8 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.15mdk
- move last modules to 3rdparty.
- new thinkpad module (nplanel).
- updated adiusbadsl 1.0.3 (nplanel).
- new hostap (nplanel).
- update prims25 to 0.2.1 (nplanel).
- sis ioapic fix (nplanel).
- ptrace fix.
- set PDC202XX_FORCE.
- move around other %build_* options to make things clearer.
- re-add %build_doc, handy when you are testing kernels.
- remove %build_gcc mess, fron now on, it is expected that default gcc.
  is able to compile kernel.
- remove %build_80 and %build_81, and %build_91 and %build_92.

* Fri Mar 14 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.14mdk
- fix more machines that don't work with apic.
- support for audigy2 (Danny Tholen).
- fix menuconfig/xconfig with alsa.

* Fri Mar  7 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.13mdk
- alsa 0.9.0rc8a.
- fix for LSB testing (stew)

* Tue Mar  4 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.12mdk
- make /lib/modules/<version>/build link construction work.
- ntfs iocharset warning disable (pixel).
- ntfs 2.1.1a (chmouel request).
- disable local apic in more boards.
- enable FUSION in BOOT kernel (nplanel request).

* Thu Feb 20 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.pre4.10mdk
- bcm5700 6.0.2.
- new 3c90x driver.

* Thu Feb 20 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.pre4.9mdk
- integrate imq patch.
- Make XFS works with swsusp.
- Upgrade to IPVS-1.0.7.
- Add netfilter on Ethernet Bridging support (thanks
  luigiwalser@yahoo.com) (#1019).
- Integrate all IPVS patch from mpol@gmx.net (#721) :
- Connections/IP limit match support.
- Nth match support (allow you to make rules that match every Nth packet).
- Psd match support (tcp and udp rules matching).
- Time match support (match on the packet arrival time).
- Recent match support (allows you to create lists of recently seen
  source addresses).
- PPTP conntrack and NAT support (also GRE).

* Wed Feb 19 2003 Juan Quintela <quintela@mandrakesoft.com> 2421-0.pre4.8mdk
- 2.4.21-pre4q8.
  * tweaked_dst works again :p
  * put ACPI_DEBUG also in the .config.
  * really enable NFS_ROOT.
  * re-disable PANOEXEC.

* Tue Feb 18 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.21-0.pre4.7mdk
- Fix md.o as module.
- Update Orinocco drivers to 0.13.
- Update Radeon DRM from XFree cvs.
- Update ADIUSBADSL patch to latest (c5).
- Remove ADIUSBADSL from 3rdparty (again).

* Thu Feb 13 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.pre4.6mdk
- configure ACPI_DEBUG when you are creating a debug kernel.
- several alsa updates to make VIA sound work again.
- adiusbadls is back (it was lost during switch from 2.4.20 to 2.4.21-preX).
- hammer updates (gb).
- new supermount is in (same that kernel for updates 9.0).
- Create all the Matrox modules, no idea why they change it :(
- experimental fix for NForce2 motherboards & ACPI (thanks to Andy 
  Grover to explain me ACPI).
- now oops should give decoded symbols.
- put back kdb, compiling kgdb for a whole kernel is a nono (takes a 
  lot of time and needs still more space)
- fix headers generation (gb).

* Wed Feb 12 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.pre4.6mdk
- 2.4.21-pre4q6.

* Sat Feb  8 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.21-0.pre4.5mdk
- fix vt8235 problems.
- Don't allow to do a swapon on mounted devices.
- Add BCM4400 support.
- Add new mgm, spdg, drm suport patch.
- Make Journalised FS working with LVM.
- Make ACPI Compile with -Os.

* Fri Feb  7 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.pre4.4mdk
- 2.4.21-pre4q4.
  - fix config for ppc.
  - atmelwlan is now for sure.
  - alsa 0.9.0rc7.
  - fix a bug in loop.
  - aes is now a loadable module (instead of a unloadable one) :p

* Wed Feb  5 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.21-0.pre4.3mdk
- Add NFORCE2 in intel i810 audio alsa driver (thanks Quel Qun).
- Disable (CONFIG_GRKERNSEC_PAX_PAGEEXEC) (thanks Thomas Backlund <tmb@iki.fi>)
- Add Latest ACPI-20030125.
- Add Latest SWSUSP (B17).
- Make SWSUSP talk to latest ACPI and latest -pre?.
- Add i450 Support (thanks Thomas).
- add 450NX streaming quirk, add via northbridge detect.
- must disallow write combine on 450NX.
- add another legitimate P4 type.
- add scanlogic usb-storage support and fix it (thks OS).

* Tue Feb  4 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.pre4.2mdk
- 2.4.21-pre4q2
  * AES is now a module
  * add exaudio USB driver (via chmouel).
  * add ontrack_adu100  (via chmouel).
  * add drm_mgm_spdg support  (via chmouel).
  * atmelwlan 20021120 (via nplanel & chmouel)
  * plustek scanner drivers (Chmouel & till).
  * rework BOOT config to reduce kernel image 60kb.

* Wed Jan 29 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.21-0.pre4.1mdk
- Merge to -pre4.
- Add BCM5700 drivers.
- Add more ACPI/APM Blacklist (from ac).
- Remove Alternate AIRONET driver (use the one of /wireles/)
- Merge a new patch for ADI USB ADSL modem and remove the old one.

* Tue Jan 28 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.21-0.pre3.3mdk
- Ide scsi fix (Andrej).
- Readd XFS.
- Add quota32 syscall interface.
- 3c59x fix for undocumented transceiver power-up bit on some 3c566B's (DB).
- fix usb hang on sony vaio fx503.

* Thu Jan 23 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.21-0.pre3.2mdk
- Add lot of docs in the spec file about the version numbering.
- pre/rc kernels shoud be named now 2.4.21pre3-1mdk to make better lilo/grub names.
- Now, right releases names in changelog (courtesy of Chmouel last kernel hack).
- 2.4.21-q1.
  * fix warinngs in do_mounts.
  * update no_ps2_mouse (chmouel).
  * ppscsi support (till should be happy now).
  * ethtool_wireless (chmouel).
  * new ide from ac (chmouel).
  * audigy from rh kernel (chmouel).
  * new usb_epson scanner recognized.
  * fix an ibm_ix00_lookup (chmouel).

* Thu Jan 16 2003 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- chmouel rpm releases trick.
- sync the version/release code with kernel-linus version.
- 2.4.21-pre3q1.
  * 2.4.21-pre3.
  * netfilter_64bits integrated upstream.
  * aic7xxx integrated upstream.
  * new scx200_export_symbols.
  * new set_cpus_allowed.
  * new kksymmoops.
  * new hdlc integrate upstream.x
  * 3c920 pci ids (chmouel).
  * reddiff ov511.
  * drm 4.2.99.3 (flepied) a lot of work to integrate.
  * grsecurity 1.9.8.
  * binfmt_elf_hyperthreading fix (jmagallon).
  * scsi-error_timeout (Andry Borzenkov).
  * ide_proc_write_drive  (Andry Borzenkov).
  * slow_supermount_on_ide.patch (Andry Borzenkov).
  * file readahead ide-cd & floppy fix (Andry Borzenkov).
  * supermount fixes (Andrey Borzenkov).
- 2.4.21-pre3q1.

* Sat Jan  4 2003 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- remove %build_doc now all documentation is in kernel-linus.
- 2.4.21-pre2q1.
  * new acpi 20021212
  * new swsuspend_acpi20021201-beta16.
  * update net-irda warnings.
  * remove journal-api.tmpl integrated upstream.
  * new sbp2_right_prototypes.
  * new mpparse_acpi_fix.
  * updated loop AES 1.7a.
  * new ide has been integrated completely upstream (removed lots of 
    ide patches).
  * i2c 2.7.0.
  * lm_sensors 2.7.0.
  * xfs integrated upstream.
  * x86_64 patch for 2.4.20.
- 2.4.20-pre2q1.

* Mon Dec  9 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- s/kdb/debug/ in all the flags.
- ppc config update (stew).
- 
- remove RPM_SOURCE_DIR occurences from the changelog.
- 2.4.20-q8.
  * acpi 20021205.
  * swsupend beta16.
  * ppc fix_symbols(stew).
- 2.4.20-2mdk.

* Tue Dec  3 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- remove unused directories.

* Fri Nov 29 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.20.
- 2.4.20-q7.
  * ppc_rivafb_dfp.patch is back (stew).
- 2.4.20-1mdk.

* Wed Nov 27 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- <modules>/build is created now automagically.
- 2.4.20-rc4.
- mydsdt now really works (tm).
- _unpackaged_files_terminate_build is gone, now done the right thing.
- 2.4.20-q6.
  * cpufreq 20021125.
  * i2c 2.6.5.
  * lm_sensors 2.6.5.
- 2.4.20-0.6mdk.

* Tue Nov 26 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- %build_minimal support (this is only to compile with some drivers,
  casually just the ones that I need, Juan).
- %build_mydst support.  If your dsdt is broke, you want recompile with 
  this option, documentation will follow once that everything works
  well.
- provides/obsoletes adiusbadls_kernel.
- 2.4.20-q5.
  * mydsdt support.
  * make xconfig should work again (adiusbadsl fixed).
  * kgdb patch.
  * radeon suspend patch.
- 2.4.20-0.5mdk.

* Sun Nov 24 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- README.* are installed in right location now.
- clean a lot the %pre/rc_patch mesh.
- 2.4.20-q4.
  * first try and a bit of documentation about the build system.
  * 2.4.20-rc3
  * hammer compiles for sure.
  * disable CPQFC for x86_64.
- 2.4.20-0.4mdk.

* Fri Nov 22 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.20-q3.
  * swsuspend is back.
  * update to andrea vm 2.4.20rc2aa1.
  * update x86_64 to 20021122 cvs.
  * kdb is gone, kgdb will be in next kernel.
  * added support for uss705 usb (nplanel).
  * now alsa drivers are not only in the tarbal, also compiled (nplanel).
- 2.4.20-0.3mdk.

* Wed Nov 20 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.20-q2.
  * acpi 20021118.
  * following items from nplanel:
  * add support adiusbadsl 101 (Sagem Fast 800 ADSL modem)
  * update alsa rc6
  * update bttv 0.7.100 (tv)
  * update saa7134 0.2.1
  * update lirc 0.6.6
- 2.4.20-0.2mdk.

* Wed Nov 20 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- _unpackaged_files_terminate_build 0
- compile BOOT kernel for x86_64.
- 2.4.20-q1.
  * 2.4.20-rc2.
  * remove lots (~150 patches) already included in rc2.
  * update ACPI to 20021022.
  * update Andrea patch to 2.4.20-pre11aa1.
  * detect correctly via C3 (and similars) as i586.
  * now patches can also be shell scripts (.sh).
  * use that to rearange ide code.
  * update ov511 to 2.16 driver.
  * urb_t is gone. update 3rdparty usb drivers.
  * include fs.h from userspace should be safe now.
  * xfs 1.2pre3.
  * lots of other small fixes.
- 2.4.20-0.1mdk.

* Fri Nov  8 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- do *doc first (gb suggestion).
- support for RS/6000 (stew).
- Build SMP kernels on x86-64 (gb).
- 2.4.19-q19.
  * swsuspend beta 15 (AM03).
  * update several patches due to swsuspend.
  * IDE in x86-64 should work UDMA100 now.
  * another sony Vaio that has problems with APM.
  * x86-64 update for 20021103 (gb).
  * create_configs -> fix x86_64 things.
  * apply patches -> start/stop options.
  * update x86-64 core to CVS 2002/11/03 (gb).
  * update linux-wlan-ng to 0.1.16-pre6.
- 2.4.19-19mdk.

* Tue Oct 29 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- move documentation to group: Books/Computer books (tv).
- 2.4.19-q18.
  * Enable AB09 (ide_pci_enable_bar) with number DI98 (aka i845 should work 
    with UDMA).
  * new support for VIA C3 (gb) this should work.
  * more bootsplash code.
  * scsi_error timeout patch & several other patchs to improve supermount 
    feeling (cooker mailing list, Andrej Borsenkow mainly).
- 2.4.19-18mdk.

* Wed Oct  2 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- use acpi.
- 2.4.19-q17.
  * new AM02 acpi 20020918.
  * remove lots of small patches for old acpi.
- 2.4.19-17mdk.

* Fri Sep 20 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q16.
  * remove VFS: busy inodes on changed media message.
- 2.4.19-16mdk.

* Fri Sep 20 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q15.
  * if you put the Makefile, supermount compiles.
  * fix permissions (in the source code files) in acecad & freeswan 
    to be readable for other.
- 2.4.19-15mdk.

* Thu Sep 19 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q14.
  * updated support_hub_usb2.0 patch, now it should work also for 1.x hubs.
  * more supermount updates:
    - now does proper reference counting during the whole operation.
    - it _always_ check if the media changed, makes things like floppies 
      that don't have a proper locking mechanism work much better.
  * put ide-cd & ide-floppy in-kernel again (otherwise devfs get confused).
- 2.4.19-14mdk.

* Wed Sep 18 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q13.
  * new (AB07) aha152x update form 2.4.20-preX
  * new (AB08) pci_enable_device_bars.
  * new (AB09) ide_pci_enable_bars -> should make i845 works.
  * new (DU09) USB memstick signature.
  * new (DU10) USB hubs 2.0 support.
  * update (FS70) supermount should now play nice with konqueror & SMP.
- 2.4.19-13mdk.

* Mon Sep 16 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- Fix depmod return error to break rpm compilation (flepied).
- 2.4.19-q12.
  * supermount changes:
    * serialize all the mounts/umount operations with a new sem.
    * really remove underlying inodes(aka space is back after a delete).
    * only try once if you are using auto and there is no media.
  * ps2mouse patch is back.
  * ide-scsi modules problem is out.
- 2.4.19-12mdk.

* Fri Sep 13 2002 Nicolas Planel <nplanel@mandrakesoft.com> 1-1mdk
- md quiet patch now working
- fix kmod error message at initrd stage
- fix dmidecode for HP e-pc (noapic)
- ide-cd and ide-floppy as static now
- fix i810_dma lockup when X restarted
- 2.4.19-11mdk.


* Thu Sep 12 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- disable PAX in secure kernel no get X, java, & company working on it.
- make create_config arguments real arguments, not environment variables.
- 2.4.19-q10.
  * local_irq_* form Alan Cox.
  * DI[04-34[, big ide rewrote to be near the one in Alan kernel.
  * update FS60 (mediactl) doue to IDE changes.
  * kernel secure conf is now kernel-smp + GRKERNSEC - DEVFS.
- 2.4.19-10mdk.

* Fri Sep  6 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q9.
  * ver_linux patch (Steven Cole).
  * via C3 is a i586 (intel i686 & gcc i686 definition disagree)
  * legacy free keyboad (DC23).
  * md quiet (DC24), nplanel.
  * ide quiet (DI97), nplanel.
  * disable apic in fosa340S (DM04).
  * HP e-pc 43 is a legacy free machine (DM05).
  * some HPs don't like local apic (DM06).
  * update ext2/3 acl support to 0.8.50.
  * update NTFS to 2.1.0a.
  * remove sis_vid, declared obsolete upstream.
  * improve dvb support, tunner is now tunner-dvb.o.
  * em8300 improve little/big endian support.
  * get the right SMBUS register in p4b_smbus (MD27).
  * create_configs & configs now integrated.
  * new update_configs, now I don't have to cp the configs by hand :).
- 2.4.19-9mdk.

* Fri Aug 30 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q8.
  * fix ov511 unresolved symbols. why depmod -u didn't fail is 
    still a mystery.
- 2.4.19-8mdk.

* Fri Aug 30 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q7.
  * fix warining in e1000_ethtool (AB06).
  * add another ecc chipset signature (DC22).
  * big ide reorganization, this only moves files around to look like
    ac kernel ide structure, real meat will came later.
  * netfilter newnat (and h323) support.
  * reddiff usbvision patch.
  * update ov511 driver to 2.09 version.
  * update htb to v3.6.
  * update dc395x driver to 141.
  * new dvb 20020829 (MC25).
  * new Portman_PCS 1.4 (MC26).
  * fix r8169 compilation in ppc.
- 2.4.19-7mdk.

* Mon Aug 26 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- updated all configs.
- 2.4.19-q6.
  * remove no_ps2mouse patch (CE05), should work without it.
  * remove intermezzo_posix_acl_undef (FB01), new solution.
  * add new extended attributes to ext2/3 0.8.26 (FE01).
  * add new acl to ext2/3 0.8.28 (FE02).
  * updated mod_quickam 0.40c.
  * updated sam9407 1.0.3.
  * add vids for Mplayer for sis, mga and radeon cards.
  * alsa ppc sound compilation fix.
- 2.4.19-6mdk.

* Fri Aug 23 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q5.
  * freeswan 1.98b included.
  * video_buf fix (tv).
  * remove duplicate definition of MAX_PAGE_BUFFS in xfs.
  * remove malloc.h in several places still used.
  * Now all the 3rdparty modules should have correct Config.in & Makefile.
  * compile sheep_net.
  * p4b_smbus module for sensors.
  * m7101 module for sersors.
  * realtek r8169 Gigabit Ethernet.
  * fix compilation of sound/usb/*.
  * grsecurity big audit, now it only appears in kernel-secure.
- remove last vestiges of freeswan from SPEC, now in the patches.
- 2.4.19-5mdk.

* Mon Aug 19 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q4
  * more scanners (tim).
  * alsa 0.9.0rc3.
- remove amdtp module in ppc.
- remove CONFIG_PRIMS25 from alpha.
- 2.4.19-4mdk.

* Wed Aug 14 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q3
  * sundance 1.03a
  * tbconvert fix
  * v4l2-api upgrade (tv)
  * bttv upgrade to 0.7.96 (tv)
  * saa7134 0.1.10 (tv)
  * jfs 1.0.21
  * new supermount
     fix NFS stale problem (oden)
     remove a lot of cruft
     update struct initializers to C99.
- enable CONFIG_VIDEO_MEYE in up.
- 2.4.19-3mdk.

* Mon Aug 12 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q2.
  * e100 driver from 2.4.20pre1.
  * e1000 driver from 2.4.20pre1.
  * fix warning in CE05 (no_ps2mouse).
  * fix several warnings in i2c (DL08, DL09, DL10).
  * fix warning in i830_dma (DV12).
  * davfs is working now.
  * bunzip all the tarballs.
  * complete 3rdparty support rework (thankyou to pixel for improving 
    the perl part), now there is only one script, it is shorter 
    and clearer.
  * linux-wlan-ng-0.1.14, and there is also the prism2_cs driver.
- 2.4.19-2mdk.

* Thu Aug  8 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-q1.
  * updated boot-splash (CD02) from SuSE.
  * updated no_ps2mouse (CE05) to remove warning.
  * i2c-2.6.4.
  * lm_sensors-2.6.4.
  * fix sis compilation (DV01).
  * remove unused vars in i830_dma (DV11).
  * fix type in supermount (FS06).
  * remove empty label in quota code (FX10).
  * ipvs-1.0.4.
  * sheep_net driver.
  * bcm5820 from rh.
  * alsa is now really integrated into the kernel,
    a lot of "inspiration" from SuSE.
  * rediff compilation fixes, as alsa and bcm5820 went out.
- now kernel is in linux-%version.
- remove all alsa related bits in spec file.
- create module.description stuff for install people.
- 2.4.19.
- 2.4.19.1mdk.

* Thu Aug  1 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- 2.4.19-rc5q1.
- 2.4.19-rc5.
- ide via 8235 support.
- P821: fix alsa detection of ICH4 chipste (nplanel).
- davfs 0.2.4 support (nplanel).
- 2.4.18.23mdk.

* Thu Aug  1 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- reorganize for new gcc-3.2 version, now default is always /usr/bin/gcc.
- remove BuildRequires of gcc, rpm-build already requires it.
- andrea 2.4.19rc3aa4.
- kdb-2.2.
- grsecurity-1.9.5.
- 2.4.19-rc3.
- Big reorganization of patches.
- 2.4.18.22mdk.

* Tue Jul  2 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- update andrea vm to 2.4.19rc1aa1.
- new P648,P649, fix reboots with small packages & wireless.
- remove P821 (alsa-via8233), integrated upstream.
- rediff P723 (xfs).
- remove P668 (pci_ids).
- rediff P640 (i810fb).
- remove P466 (sisfb compilation problems).
- remove P242 (read_write_lsb), integrated upstream.
- reddiff andrea patches.
- remove P400 (eepro-io), it shouldn't be needed.
- remove OPT1621 & NS87415 from ppc config.
- alsa 0.9.0rc2.
- rediff P105 (local pages).
- 2.4.19-rc1.
- add LC_ALL=C to all the perl invocations.
- don't depend anymore of openssl libs.
- 2.4.18.21mdk.

* Fri Jun 14 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- disabling P241 (-Os), as actual gcc is not very good about that.
- make this things IDECD & IDEFLOPPY & FLOPPY modules.
- rediff P1302 (agp_uninornth), stew.
- remove P1300 (riva fixes for ppc), patch included upstream (stew).
- 2.4.18.20mdk.

* Wed Jun  5 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix sisfb complilation.
- jfs 1.0.18.
- remove P1406 (kernel-api), included upstream.
- rediff P664 (grsecurity).
- rediff P612 (usbvision).
- remove P462 (sdla_fr fix), included upstream.
- remove P450 (tychoon), never worked, and I don't have the hardware 
  handy anymore.
- remove P453 (ich4 sound), included upstream.
- remove P424 (tulip fix), at the end, it was included upstream.
- 2.4.19-pre10.
- fixed via8233 sound P821 (via tv).
- changed ppc .config (disable USB_EMI26, USB_RTL8150, LIRC, SPECIALIX, 
  SCSI_DEBUG) and enable BLK_DEV_IDECS.
- included .need_mrproper really in kernel-source 
  (bug found by Andrej Borsenkow).
- remove P219 (noathlon), as it didn't worked and nobody noticed, 
  discovered by Tim Lee.
- fix dxr3 Config.in, Tim Lee.
- fix lirc Config.in, Tim Lee.
- new P465 (ide-scan-devices), fix problems with naming of modules, 
  Andrej Borsenkow.
- update P459 (ide-scsi), fix race, Andrej Borsenkow.
- new P242, fix LSB failures, stew.
- added mppe 3rd-party module, stew.
- new P464 (terratec fix), from tv.
- new P463 (bttv update + jetway card + kworkld) from tv.
- 2.4.18.19mdk.

* Thu May 30 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- new P1406, fix docbook compilation with new utils.
- rediff P1025 (device).
- rediff P1302 (agp_uninorth)
- rediff P724 (xfs-misc).
- rediff P655 (grsecurity).
- rediff P640 (i810fb).
- rediff P612 (usbvision).
- remove P463 (umem_compilation), included upstream.
- remove P461 (up_ioapic), included upstream.
- remove P460 (ufs_fix), fixed upstream.
- remove P237 (xconfig array limits), fixed upstream.
- updated part of aa patches.
- remove P1030 (quiet CDROM), included upstream.
- remove P455 (i845G support), included upstream.
- updated P1400 (license tags).
- 2.4.19-pre9.
- updated P665 (hp_omnibook_onetouch).
- 2.4.18.18mdk.

* Tue May 21 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- make kernel-source work for any architecture that we support.
- P1203, get mrproper done automagically in kernel-source.
- modify 3rdparty to make a common part for *configs.
- P241, s/-O2/-Os/.
- 2.4.18.17mdk.

* Wed May  8 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix xfs to compile with gcc-3.1.
- use gcc-3.1 as default compiler.
- 2.4.18.16mdk.

* Tue May  7 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- new P463 (umem), fix compilation.
- new P462 (sdla_fr), get it to compile.
- include ia64 support.
- remove AUTOFS_FS support (AUTOFS4_FS should be better).
- rediff P1302 (agp_uninorth).
- rediff P1002 (dynamic-disk).
- remove P667 (ide_82801DB), included upstream.
- remove P666 (ehci24), included upstream.
- rediff P664 (grsecurity).
- rediff P649 (i2c-amd756).
- remove P648 (delayed init_apic), included upstream.
- updated lm_sensors to 2.6.3.
- updated i2c to 2.6.3.
- remove P639 (br2684), integrated upstream.
- rediff P603 (cipe).
- remove P457 (meye update), integrated upstream.
- remove P456 (videodev update), integrated upstream.
- remove P454 (eepro new id), integrated upstream.
- remove P426 (wacom update), integrated upstream.
- remove P239 (i8xx names), integrated upstream.
- remove P238 (upapic), integrated upstream.
- update to andrea 2.4.18-pre8aa1.
- 2.4.19-pre8.
- remove (P608), 3c90x, as 3c59x should handle better all that cards.
- BuildRequire: docbook-utils-pdf.
- really add P459.
- 2.4.18.16mdk.

* Fri May  3 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- xfs 1.1.
- kenel compiled by user is called x.y.z.amdkcustom instead of 
  overwritting mdk up kernel.
- freeswan 1.97.
- remove old iscsi patch and added iscsi-2.1.1.2.
- 2.4.18.15mdk.

* Sat Apr 27 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- remove P439 (viaudma33), if you have a VIA machine and you have 
  corruptions with that kernel, please let me know.  Notice that this patch 
  _should_ not be needed, it should have been fixed upstream, but last time 
  that I remove it in 2.4.7-1mdk, and then a couple of persons have the 
  problem again.
- P1201: lirc devfs support (fcrozat).
- updated linux-mdkconfig.h to get right modversions symbols (Andrej Borsenkow).
- P459: adds ide-scsi fix for devfs (Andrej Borsenkow).
- P458: adds v4l2 support to the linux kernel (tv).
- P457: adapt meye driver to videodev changes (tv).
- P456: new videodev design (support for usb unplug while in use) (tv).
- alsa-0.9.0rc1.
- smp, enterprise, secure are SMP again (Franco Silvestro).
- dxr3 compiles again.
- added ide support for ich4 (P667, P668).
- add ich4 support (P453.P454, P455).
- Get ehci update from usb mailing lists (P666).
- omnibook xe3 onetouch mouse should work accross resumes now.
- 2.4.18-pre7.
- 2.4.18.13mdk.

* Fri Apr 19 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix spelling of Christoph Hellwig in all the attributions (I hope to 
  get spelling right this time :p)
- remove P241 (lcall7_trace), other fix upstream, Christoph Hellwig.
- remove P401 (i2o_lookup), not needed anymore, Christoph Hellwig.
- remove P422 (cramfs_spinlock), not needed, Christoph Hellwig.
- remove P1303 (sis-fix-alpha-compile), not needed anymore, Christoph Hellwig.
- make as module FD, IDECD & FLOPPY for all the archs instead of builtin.
- lirc 0.6.5.
- dxr3 0.12.0.
- secure kernel is i586 no highmem no SMP now.
- 2.4.18.12mdk.
n
* Sun Apr 14 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- include alsa-headers also in kernel-headers for glibc.
  once there, clean a lot the kernel-headers generation.
- Remove modules/pcmcia symlinks & directory, it was a legacy thing.
- Remove numargs patch (P221), only needed for s390 (Christoph Hellwig).
- Remove tripelock patch (P223), not needed (Christoph Hellwig).
- include alsa headers in kernel-source (i.e. include/sound).
- 2.4.18.11mdk.

* Wed Apr 10 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- we need to have installed jadetex for kernel-doc*.
- disabling install headers part of alsa.
- disable NETLINK_DEV, that is an obsolete option, looking how many 
  things we break.
- disable CONFIG_IP_ROUTE_LARGE_TABLES, as this is only for people with 
  more than 64 route entries (i.e. almost nobody).
- more compilation fixes (P1405).
- remove P401 (i2o driver), not needed, Christoph Hellwig.
- remove P422 (cramfs spinlock) not needed, Christoph Hellwig.
- jfs 1.0.17.
- reddiff compilation fixes & endif patches.
- don't try to install as root (P821) (alsa).
- rediff grsecurity patch.
- rediff kdb patch to fix the FRAME_POINTER merged parts.
- remove P206 (sard), included upstream.
- use gcc30 by default.
- alsa 0.9.0pre12.
- 2.4.19-pre6.
- 2.4.18-10mdk.

* Fri Apr  5 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- rest of andrea vm.
- disable PCILYNX & FB_NEOMAGIC until they compile again.
- compilation fixes for several things that still don't compile.
- rediff boot patch.
- rediff several xfs patches.
- rediff P664 (grsecurity).
- remove P663 (more dmi updates), included upstream.
- rediff P652 (new_hdlc)
- rediff P640 (i810-fb).
- rediff P623 (kdb-i586).
- reddiff P432 (hidden-ip-interface).
- remove P431 (syskconnect dual support), integrated upstream.
- rediff P426 (wacom-update).
- remove P423 (xircom_update), included upstream.
- remove P410 (ethtool), included upstream.
- remove andrea_vm patch and get the splitted parts from Andrew Morton.
- rediff P213 (boot-splash-font-fix).
- remove P209 (rd-progress), things have changed a lot upstream.
- 2.4.18-pre5.
- 2.4.18-9mdk.

* Sat Mar 30 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- added patch P1403 (compilation-fixes) to make the thing to compile.
- disable PDC_ADMA driver (it is not there anymore).
- updated grsecurity to 1.9.4.
- remove show_stack from andrea patch (as ppc hasn't a definition for it).
- rediff P1006 (idefloppy devfs support).
- remove P1005 (idefloppy patch), different fix upstream.
- remove P662 (permedia fb), included upstream.
- remove usb update (P654,P655,P656,P657,P658,P659,P660), included upstream.
- disabled ov511 update from now.
- remove P650 (fujitsu_siemens dmi) included upstream.
- updated kdb, ov511 patches.
- remove P647 (early_dmy_scan), included upstream.
- remove P646 (boot_time_ioremap), included upstream.
- remove P645 (p4 watchdog), included upstream.
- remove P627 (remove avma1 cs support), included upstream.
- remove P452 (more ide updates), included upstream.
- remove P451 (smbfs fix), included upstream.
- remove P447 (amd 768 addition), included upstream.
- remove P446 (natsemi fix), included upstream.
- romeve P445 (tridentfb fix), included upstream.
- remove P444 (hpfs fix), included upstream.
- remove P441 (eepro100 fix), included upstream.
- remove P427 (ide_update), included upstream.
- remove P420 (lamstream update), new update upstream.
- remove P244 (personality fix), applied upstream.
- remove P243 (shm fix), applied upstream.
- remove P242 (request_starvation), applied upstream.
- remove zlib fix.
- andrea vm_32.
- Remove P207 (scsi_reset), included upstream.
- 2.4.19-pre4.
- 2.4.18-8mdk.

* Sat Mar 16 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- dmi update to fix apm in Dell Inspirons 2500.
- smbfs fix for Ooops.
- mini ide update (ultra safe mode): 
  * Release recognition of promise ide raid.
  * fix jiffies workaround things (ide-tape).
  * hpt37[24], don't oops if we find them
  * put another WD disk in the ide-dma black list.
  * fix Oops with hpt37x & a lot of controllers.
- 2.4.18-7mdk.

* Fri Mar 15 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix removal oops of pcmcia cards (dirty fix, akpm & jgarzik working
  in a better fix for upstream).
- 2.4.18-6mdk.

* Sat Mar  9 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- supermount fixes (symlinks works as expected).
- wacon update (flepied).
- 2.4.18-5mdk.

* Tue Mar  5 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- audigy driver for emu10k1 new cards.
- quotas fixed, at last (for the curious, jfs & reiserfs don't have 
  quota support, don't try).
- remove the quota patch, as it is integrated in the xfs one.
- xfs for 2.4.18.
- enable wireless support in BOOT kernels.
- 2.4.18-4mdk.

* Sun Mar  3 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- update ov511 to 1.57 version.
- addded Interphase fiber channel support in the cpqfc driver.
- re-merge quotas (this time it is supposed to work).
- re-merge xfs-2.4.17 again.
- change default config to be up again.
- new driver for prism2 wireless cards.
- allow options in tcp after the 0x00 (end of options).
  blame firewal people (aka florin).
- htb v2 (new queing system).
- added support to create_configs for athlon, k6, i486 & i386 
  (I think that rpm don't know more architectures).
- jfs 1.0.15.
- 2.4.18-3mdk.

* Thu Feb 28 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- support for AMD MPX (2.4.19-pre1).
- natsemi fix (2.4.19-pre1).
- add tridentfb fix and enable it again (2.4.19-pre1).
- set personality (2.4.19-pre1).
- hpfs fix (2.4.19-pre1).
- add shm-fix (2.4.19-pre1).
- add permedia pm3 fb driver (2.4.19-pre1).
- add request starvation fix Andrew Morton.
- add new sound blaster32 id (2.4.19-pre1-ac1).
- update new ps2mouse from 2.4.19-pre1-ac1.
- andrea vm_28.
- dmi fixes from 2.4.19-pre1, 2.4.19-pre1-ac1, 2.5.6-pre1. For the curious:
  * Dell laptops & ACPI.
  * Hp problems with interrups.
  * Fujitsu-Siemens with apci_timer.
- 2.4.18-2mdk.

* Wed Feb 27 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix the new hdlc code, this time for real.
- Improve speed of je uhci (660) (chmouel).
- Remove the big usb-update patch and split it with multiple patch (chmouel).
- Add USB auerswald driver (P655). (chmouel).
- Add the USB 2.0 controller and auerswald drivers to the build  
  process (P656). (chmouel).
- Add support to the USB visor driver for the Palm m515 and Sony Clie
  S-360 devices. (P657). (chmouel).
- Updates the USB ibmcam driver to the latest version (P658). (chmouel).
- Updates the USB uhci driver (P659). (chmouel).
- Moved acecad from patch to 3rdparty.
- 2.4.18.1mdk.

* Tue Feb 26 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- rediff grsecurity.
- update the o511 driver.
- fix for eepro100.
- added all the 3c990x network cards.
- fix por the people having problems with via dma.
- new patch pc300 for cyclades cards.
- added fixes for non native binaries.
- added andrea vm_27.
- added mini-low latency patch.
- added acecad tablet driver.
- added eboxit patch for vpn over adsl.
- added support for 3c990[fx] cards.
- update the Zaurus driver to be usbnet.
- fix kdb creations in create_configs.
- 2.4.17.22mdk.

* Fri Feb 22 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- redo the configuration code, now there is only one config file for arch
  and we generate the rest from here.
- upapic from rh.
- 2.4.18-rc4.
- fix the gcc3-version problem (Andre Duclos).
- remove %build_80 option, it don't work anyways.
- update for usb2.0 (chmouel).
- remove page_cache_size fix (included in latest adrea_vm)
- andrea vm_25 (from 2.4.18-rc2aa2).
- added i2c support for AMD 768 (Willy Tarreau <wtarreau@free.fr>).
- add license tags for all the modules without one.
- remove rhkmvtag.c & is uses, as it was a write only use.
- freeswan 1.95.
- 2.4.17.21mdk.

* Wed Feb 20 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- enable rpmhelper module in all the kernels for now on.
- 2.4.18-rc2.
- now xconfig has the correct values and works again.
- fix dependencies for boot-splash-screen font (jgarzik).
- fix in pcmcia modules names links (Andre Duclos).
- fix to kernel-hearders and new naming scheme (Andre Duclos).
- update Zaurus driver for ethernet over usb (Dave Seff).
- updated ppc configs (stew).
- 2.4.17.20mdk.

* Tue Feb 19 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1-1mdk
- Update gatos patch to get working the radeon drm.
- 2.4.17.19mdk.

* Thu Feb 14 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- redo all the configs.
- remove Tridentfb module, as it will hang.
- update ide patches to 02072002 version.
- 2.4.18-rc1.
- updated 3rdparty support.
- qla2x00 2001/08/28 version (from rh).
- Hope that this time the module.* thing is fixed.
- 2.4.17.18mdk.

* Wed Feb 13 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- remove patch to e100 compilation.
- new e100 driver (version 1.6.22) from rh.
- Intel e1000 driver (version 3.1.23) from rh.
- early dmi scan (from rh).
- new boot_time_ioremap patch.
- new p4 watchdog (from rh).
- allow autoload of freevxfs module (from rh).
- updated iscsi patch (from rh).
- fix rawio (from rh).
- added raid5xor module (from rh).
- added rpmhelper module (from rh).
- added build_BOOT define to make happy not x86 archs (stew).
- quotareturn fixes (P234) from rh.
- page_cache_size fix.
- redo all the configurations.
- remove netfilter patch.
- return compilation of VXFS_FS.
- 2.4.18-pre9.
- 2.4.17.17mdk.

* Thu Feb  7 2002  <quintela@kernel.mandrakesoft.com> 1-1mdk
- new supermount version, this is supposed not to Oops.
- add netfilter fixes (P436).
- added support for rawio to devfs (P1007).
- resync linux-merge-*.awk with rh versions (comments mainly).
- 2.4.17.16mdk.

* Wed Feb  6 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- requires mkinitrd >= 3.1.6-24mdk due to xfs changes.
- fix kernel to still export the name do_get_fast_time (P232).
- add buffer-fix-compilation-patch(231).
- disable VXFS for now.
- reddiff xfs-kernel patch.
- added defalt logo patch (P213) (chmouel).
- update xfs-act-extattr due to new syscalls.
- remove i810 audio update (P643), included upstream.
- parts of the drm upgrade was included upstream(P433).
- remove P232,P233 that fixed the problems with pre7.
- 2.4.18-pre8.
- really use andrea vm_24.
- 2.4.17.15mdk.

* Fri Feb  1 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- add -p to install to maintain timestamps.
- fix /build link to point to real source.
- rediff grsecurity patch.
- updated the xfs-quota patch.
- xfs for 2.4.17.
- andrea vm_24.
- really fix the autoconf issue with alsa.
- 2.4.17.14mdk.

* Thu Jan 31 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- disable jfs in alpha.
- make a new logo and support for splash logo (chmouel).
- remove ipfwadm fix as it is included in previous patch also.
- netfilter files missed in 2.4.18-pre7 are back in.
- now apply i810 patch & new sk card patch :(
- kernel-secure is kernel-enterprise based.
- 2.4.17.13mdk.

* Tue Jan 29 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- ext3 is a module again in up.
- s/kversion/realversion/, make greps easier.
- really include modules.* in the tarballs.
- jfs 1.0.14.
- 2.4.17.12mdk.

* Tue Jan 29 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- new i810 audio patch (chomuel).
- new sk card.
- new kdb-common patch.
- fix alsa compilation.
- fix kernel-source name (kernel-source-1-1mdk was bad :()
- 2.4.17.11mdk.

* Fri Jan 25 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- Make kernel-BOOT in the main distrib (chmou).
- Merge ide-small config-small patches with one patch depending of
  CONFIG_BOOT_KERNEL (chmou).
- Make BOOT patch conditional of CONFIG_BOOT_KERNEL (chmou).
- remove spurious Obsoletes & Requires of kernel-source.
- fix acenic unresolved symbols.
- 2.4.17.10mdk.

* Thu Jan 24 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- remove SYM/NCR53C8XX drivers as SYM53C8XX_2 should be better in all circunstances.
- remove part of the new netfilter modules, as the code is not there.
- removed dependency of devfsd, we don't really need it.
- ipvs-0.9.7 (from rh).
  at the same time removed the _two_ ipvs that we had.
- 2.4.18-pre7.
- reddiff xfs-kernel patch.
- andrea vm_23.
- make sane names for kernel-source & kernel-doc*.
- remove devfs v199.8 patch, included upstream.
- buffer-fix patch included upstream.
- 2.4.18-pre6.
- change gcc30 name to gcc-%%(gcc3-version).
- 2.4.17.9mdk


* Tue Jan 22 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- update devfs to v199.8, at the end we got an official devfs that works.
- build secure kernel only for x86.
- ppc update from stew.
- new drm for XFree 4.2.0.
- remove depmod from %post.
- enable options in secure kernel.
   CONFIG_GRKERNSEC_CHROOT_PTRACE
   CONFIG_GRKERNSEC_CHROOT_MKNOD
   CONFIG_GRKERNSEC_CHROOT_CHDIR
   CONFIG_GRKERNSEC_CHROOT_DOUBLE
- i830 drm patch.
- reddiff grsecurity.
- kdb 2.1.
- 2.4.17.8mdk

* Sat Jan 19 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- put 830mp support for suspend/resume.
- update all configs.
- drop radeon fb update in pre4.
- drop cs8241 update in pre4.
- rediff usbvision patch.
- rediff 3c90x patch.
- rediff ide update patch.
- remove agpgart_830mp fix (P231) included upstream.
- remove nfs-attr patch (P230), included upstream.
- 2.4.18-pre4.
- add support for compiling for: kgcc, gcc-2.96, gcc-3.0 & gcc-3.1.
- 2.4.17.7mdk

* Wed Jan 16 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix cipe DOS(642).
- i586-{up,BOOT} .config to use APIC in uniprocessors.
- agpgart i830mp support patch for i830 (Erwan, P231).
- new nfs-fattr patch (P230).
- reversed devfs patch.
- reddiff xfs-kernel patch.
- jfs 1.0.12.
- tryed devfs 199.7, still problems with no /dev/root.
- 2.4.17.6mdk

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1-1mdk
- Add secure kernel.
- 2.4.17.5mdk.

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1-1mdk
- Really fix that quota mess up (xfs guilty).
- 2.4.17.4mdk.

* Mon Jan 14 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1-1mdk
- New quota patch which this should work and recompile.
- 2.4.17.3mdk.

* Mon Jan  7 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- re-add loop-AES (v1.5b).
- remove international patch.
- 2.4.17.2mdk.

* Fri Jan  4 2002 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- Devfs don't create /dev/root anymore (P1007).
- rediff supermount patch.
- updated international cryto patch to 2.4.17.
- remove reverting devfs patches.
- 2.4.17.
- 2.4.17.1mdk.

* Wed Dec 19 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- remove no_persistence from devfs.
- remove devfs update.
- added quota from ac kernel, and fix xfs to use it.
- remove all alsa patches (acepted upstream, P822, P823, P824, P825).
- alsa 0.5.12a.
- nfs fixes.
- 2.4.17-rc1.
- 2.4.16-11mdk.

* Sat Dec 15 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- add hidden ip patch (P432).
- rediff new_stat.
- new xfs patch for 2.4.16.
- Removed brokenmptable patch (P200).
- Add fix for compilation of sis driver on alpha (P1303) from rh.
- get no_ps2 patch (P224) form caldera, this one makes sense.
- add dependency on e2fsprogs to reflect Documentatation/Changes.
- remove last vestiges or sparc suport (S14).
- 2.4.16-10mdk.

* Thu Dec 13 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- remove the devfs patch from pre8 (as usual it non boot).
- update .configs.
- reddiff xfs (P720).
- reddiff br2684 (P639).
- remove aacraid P622(better patch from Alan Cox integrated upstream).
- rediff scsimon patch (P619).
- reddiff kdb patch (P614).
- remove vlan patch (P432) integrated upstream.
- rediff xircomp-cb patch (P423).
- 2.4.17-pre8.
- SPEC name is again kernel-2.4.spec.
- 2.4.16-9mdk.

* Wed Dec 12 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- correct find arguments (-name instead of name).
- update mediactl patch.
- Remove hpt3xx update (integrated upstream) P430.
- update config-ide-small patch.
- update ide driver (12102001) (P427).
- new configs for alpha & ppc without CRYPTO stuff.
- new %build_source flag, to be able to do indeed less things in one 
  single compilation.
- updated ppc-confis (stew).
- 2.4.16-8mdk.

* Mon Dec 10 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix (again) /usr/src/linux link mess :(.
- add loop-jari patch to make crypto-patch work.
- remove *.append files only needed for kbuild-2.5.
- updated loop-AES to international crypto-patch (includes first one).
- provides & obsoletes kernel-source.
- 2.4.16-7mdk

* Sat Dec  8 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- new vlan patch (1.6).
- new newnat & h323 code (P620 & P621) (decided to wait this one, lot
  of incompatible changes.
- added i686 configs for Jeff.
- fix name of the /usr/src/linux-2.4.16-6mdk
- 2.4.16-6mdk.

* Fri Dec  7 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix the naming of the kernel to kernel-2.4.16-5mdk, this time in kenobi copy instead of local copy :(
- 2.4.16-5mdk.

* Wed Dec  5 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- jfs-1.0.10.
- kernel spec file is called again kernel.spec.
- new i810 patch (chmou).
- KVERREL is real kernel version, not mdkversion.
- kdb 2.4.16.
- 2.4.16.4mdk.

* Tue Dec  4 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- fix name of the kernel SRPM.
- fix /usr/src/linux symlink.
- update ide-floppy for devfs support (remove P1003, add P100[56]).
- add links for pcmcia modules to modules/pcmcia (chmou).
- fix generation of kernel-headers (chmou).
- 2.4.16.3mdk.

* Mon Dec  3 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- loop-AES 1.4h.
- really fix DC395x driver compilation.

* Fri Nov 30 2001 Juan Quintela <quintela@mandrakesoft.com> 1-1mdk
- compile again DC395x driver.
- fix mdksuffix big problems.  Why suffix is a reserverd word for rpm
  macros and where it is documunted it is still a mystery to me.
- From 2.4.13-12mdk
  * qla1280 v3.23.10 (P606).
  * update syskconnect driver to support dual-port (P426).
  * move install-kernel -R from postun to preun (chomuel & Borsenkow
    Andrej <Andrej.Borsenkow@mow.siemens.ru>)
  * remove all the other vestiges of kernel-headers.
  * Remove Kernel-Headers package moved to glibc package (chmou).
  * Add new rules build_kheaders to build tarball and patch for glibc
    package (chmou).
  * updated i586-BOOT config (chmouel).
  * updated all ppc configs to have pcmcia support (stew).
  * Remove redundant BuildRequires (Stefan van der Eijk <stefan@eijk.nu>).
  * new fb810 code P640 (chmouel).
  * small fix in pcmcia support (chmouel).
- update hpt3xx driver Tim Hockin <thockin@sun.com> (P428).
- lm_sensors-2.4.16.
- i2c 2.4.16.
- fix intermezo compilation (P429).
- remove P1301, included upstream.
- new new_stat, mediactl & supermount patches.
- 2.4.16.

* Fri Nov 23 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.15-1mdk
- 2.4.15 final.

* Fri Nov 23 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.14-1mdk
- remove devfs-v196 patch (P1005) integrated upstream.
- rediff ipvs patch.
- P801 integrated upstream.
- xfs 1.0.2 in.
- rediff jfs shared patch.
- Removed syncookies fix (P636) integrated upstream.
- split config-small patch in config-small & config-ide-small.
- added new ide patch 11062001 (P427).
- new kdb patch.
- Remove P602 patch (integrated upstream).
- Remove P208 blkioctl, it is only needed for ia64, and our kernel
  still don't work in ia64.
- Remove P202 TIOCDEV. it was a half merge, and nobody uses it.
- Remove P201 pge (not needed).
- Remove P415 (more sb ids) integrated upstream.
- Remove P414 (parport & pnp) not needed in linus tree.
- Remove P413 (blk io queue) as elevator is different in linus tree.
- Remove P405 (it is not needed).
- Remove parport backport (P402) as it is not needed in linus kernels.
- Move wacom update (P226) from core to update (P426).
- remove quota fix (P227) it is not applieble to linus kernels.
- parts of sard patch was in scsi reset patch, put things in its place.
- 2.4.15-pre6.

* Tue Nov 20 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-9mdk
- Update .configs.
- fix compilation for boot kernel (chmou).
- add fb for i810 P640 (chmou).

* Sat Nov 17 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-8mdk
- s/RPM_SOURCE_DIR/%_sourcedir/.
- fix xconfig problems with mtok driver.
- fix problem for compilation in the kernel of 3rdparty modules
  (Duclos Andre <shirka@wanadoo.fr).
- add BuildRequires: trasnfig (Duclos Andre <shirka@wanadoo.fr).
- Remove P211 (especial install-kernel) is it is not needed.

* Wed Nov 14 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-7mdk
- remove current patch (P2).
- added madge token ring drivers (S106).
- remove atm fix (P406).
- new devfs patch (P1005).
- jfs-1.0.9.
- deselect SUNGEM for ppc (stew request).
- redo all configs.
- updated dc395x_trm driver to 1.33.
- loop-AES.

* Thu Nov  8 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-6mdk
- activate supermount in enterprise kernel (I feel coraugeus today).
- added br2684 support (P639).
- removed spurious link line for smp %postun.
- fix all the compilation warnings in alsa (P822, P823, P824).
- remove P820 (alsa-compile-fix) as it is not needed anymore.
- alsa 0.5.12.

* Thu Nov  8 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-5mdk
- update configs.
- add conflict with old iptables.
- make kernel-doc-{html,ps,pdf} with the contents of the kernel books.
- rediff xfs patch (720).
- rediff kdb patch (614).
- part of patch P410 (ethtool was included upstream).
- ac8.

* Wed Nov  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.13-4mdk
- update alpha configs 
- add URL tag
- surround KDB option disable with %%ifarch %%ix86

* Tue Nov  6 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-3mdk
- added tulip patch (P424).
- fixed problem of nested %if for some rpms.
- updated all the configs.
- Remove P623 (integrated upstream) lba48.
- Remove P424 (applied upstream) appletalk fix.
- Rediff config-small (P212).
- Rediff blkioctl (P208).
- new ipatbles patches, we are:
	* compatible with vanilla kernels
	* h323 support 
	* talk support
- new iptables patch, including h323 & talk and dropping dropped
  table, we are supposed to be compatible with vanilla kernel again.
- ac6.

* Tue Oct 30 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-2mdk
- and then rework the .config to fix all the problem with ATALK.
- fix appletalk mess (P424).
- install config file also as .cnofig to evict problems with autoconf patch.
- Remove P203 (RUNTIM_FXSR don't exist anymore in the kernel).
- ac5.
- Redo P201, it was supposed to patch 686 not PIII.
- ac4.

* Sat Oct 27 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.13-1mdk
- updated all the configs.
- rediff devfs_dynamic (P1002).
- rediff xfs patch.
- update kdb (P614).
- ac3 (I have had no time to finish the patches creation :()
- ac2.
- 2.4.13.
- fix rpmlint errors in permissions.

* Sat Oct 27 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.12-6mdk
- wacom driver (flepied) (P226).
- added fix to symcookies (P636).
- remove comented patch626 (that don't exist anymore).

* Wed Oct 24 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.12-5mdk
- build enterprise for anything except alpha.
- this time I included the ppc&alpha smp/up confis in the SRPM.
- updated ppc configs, now they also use enterprise kernels (stew & me).
- fix lba48 for non ppc archs (P624) stew.
- add riva fb for ppc (P1300) stew.
- ac6.
- s/Linux Mandrake/Mandrake Linux/.

* Tue Oct 23 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.12-4mdk
- make -up & -smp config files until I found a better way to work with that.
- rebuilt all the .configs.
- supermount upgrade:
	* options passed to subfs should work when you change the cd
	* bug: cd /mnt/cdrom/any_dir; ls -l; switch cd; ls <BUG> should have gone.
	* That means that there is no more supremount bugs that I have heard of.
	* supermount with no fs type, or fs type of auto does what you expect:
		try iso9660, then vfat, then ext2.

- P702 included upstream (jfs fix crashes).
- jfs 1.0.8.
- rediff xfs patch (P720).
- rediff lba48 patch (P624).
- ide-cd integrated upstream (P403).
- rediff blkioctl patch (P208).
- ac5.

* Tue Oct 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.12-3mdk
- 2.4.12-ac3 (Rem: samsung-anycam-mpc-c10, ext3-update).

* Tue Oct 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.12-2mdk
- Fix provides kernel of sub kernel's.

* Mon Oct 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.12-1mdk
- 2.4.12-ac2.
 (Rem: scsi_scan, firewire patches, devfs upgrade patches, Adapt: lba48).

* Fri Oct 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.5-6mdk
- 2.4.10-ac12 (Rem: emu10k1 patches).
- Remove jfs-fixes, not needed anymore (P702).
- Fix important crashes with JFS (P702).
- Fix provides of kernel for smp.
- Fix build of lba48 with latest ac (P624).
- Upgrade ext3 to 0.9.12 (P428).
- Disable anxet_cs module (P626).

* Wed Oct 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.10-5mdk
- JFS-1.0.7 (P700, P701, P702).
- Add natsemi_old driver (P635).
- Add iscsi update (P601).
- Remove bcm5700 from 3rdparty and make it as patches and upgrade it
  btw (P627, P628, P629, P630, P631, P632).
- Upgrade bcm5820 driver (P616, P617).
- Upgrade xircom_cb to latest (P428).
- Add wvlan_cs pcmcia driver (P624).
- Add axnet_cs pcmcia driver (P623).
- Add avm_cs pcmcia driver (P627).
- Ad qla2100 driver (P604).
- Upgrade qla1280 driver (P605).
- Bring devfs to v195 (P1000, P1001).
- Update usb-uhci to latest of 2.4.11 (P622, Rem: 402, 411).
- Fix some rpmlint's.
- Reordering patches section.
- Fix conflicts of with kernel-pcmcia-cs.

* Mon Oct  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.10-4mdk
- 2.4.10-ac10 (Rem: P622, Up: P720, P1022 ). 
- Add support for samsung-anycam-mpc-c10 (P512).
- Fix compilation of e100 with latest kernel (P1203).
- Add fix for ide-floppy devfs patch (Andrej) (P1003).
- Add lba48 ide support (P622).
- devfs-v193 (P1001).
- Remove kernel from boot loader in %post when AUTOREMOVE=yes in
  /etc/sysconfig/installkernel is set.
- Disable PNP_BIOS, set ramdisk default size to 32000 enable IDE_CS.
- Fix changelog (2.4.8-2[56]mdk was gone).
- Conflicts with kernel-pcmcia-cs (need pcmcia-cs).

* Mon Oct  8 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.10-3mdk
- Fix OptionEnable to not work also in prefixes.
- don't removke -temp tree on clean.
- Split lm_sensors in its own package, we only need the drivers (P623).
- from i2c we only need the patch, we got it (P622).

* Thu Oct  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.10-2mdk
- 2.4.10-ac3 (Remove: P428).
- Remove pcmcia from here and move to the kernel pcmcia support.
- Add some BuildRequires: (stefan).
- Make some files as %dir in sources packages for upgrade.
- Fix i2c/lm_sensors build.

* Sat Sep 29 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.10-1mdk
- 2.4.10-ac3. (Remove 97 Patches | Add/Adapt/Rename 35 patches ).
- Big rework of patch sections.
- i2c/kdb/xfs/jfs latest.

* Sun Sep 23 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.8-26mdk
- new supermount patch, this time fixes the oops.
- stat fixes.

* Sat Sep 22 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.8-25mdk
- new supermount patch.

* Mon Sep 17 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-24mdk
- JFS-1.0.5 (P4005, P4006).
- Register usb core after hid (P4531) (P.Vojtech)
- Rework XFS patch for new supermount fixes (P4600) (juan).
- supermount fixes (a lot of them, this time should work). (P306). (juan)
- updated overflow patch to cope with previous patch (P501). (juan)
- added new stat patch from al viro (P305). (juan)
- this time right 8139too_cb driver (P166). (juan)
- introduced a build_kdb macro. (juan)
- now we use build_kgcc in all the places. (juan)

* Wed Sep 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-23mdk
- Remove sd many option from devfs patch it broke usb-storage (P4502).
- Add bunch of irda fixes (P4550, P4551, P4552, P4552, P4553, P4555,
  P4556, P4557).
- Radeon fixes (P4530) (S.Tweedie).
- PWC usb driver upgrade to 8.2 (P4529).
- Add support for dynamic disks with devfs (P4503) (K.Flemming).
- Pcmcia-Cs-3.1.29 (S1) (Remove: P163).
- NTFS 1.1.19 fixes (P4528).
- Upgrade to latest version of mod_quickcam driver (S102).
- Cleanup spec file of unnused patches.
- rename realtek_cb to 8139too_cb to evict confusions (P166) (juan).
- supermount upgrade (P305) (juan)

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-22mdk
- Fix process reporting crashing sigbus when is sigsev (P4526).
- Fix reparent children in nfsd (P4525) (N.Brown).
- Register the lowlevel ieee1394 driver to the subsystem. (P4524).
- Parse mainboard resources inline to pnp not as pci_device
  objects. (G.Knorr) (P4523).
- New update to latest firewire with number of fixes (P4515).
- Parse /proc/fs/nfs/exports like does /proc/mounts (which allow
  mountpoint with space) (P4522) (N.Brown).
- CONFIG_BLK_DEV_OFFBOARD=y in all .config (civileme).
- lm-sensors 2.6.1 (S9) (Remove: P101).
- Apply official xircom-pgsdb9 patch (P421).
- Fix mmap in emu10k1 driver (P504).
- Remove bits from i810_audio upgrade to make it works with artsd (P4506).
- MCE address reporting fix (P4521) (D.Jones)

* Fri Sep  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-21mdk
- Add XFS support (P4600, P4601) (R.Cattelan).
- Fix ntfs symbol errors (P4520).

* Thu Sep  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-20mdk
- Apply emu10k1-passthough patch for SMP (P503).
- NTFS upgrade to 1.1.18 (P4520).
- Irda-usb fixes (Adam J Richter) (P4519).
- Axnet pcmcia card fix (P163) (Stefan.Siegle).
- Upgrade updfstab pcmcia patch to call updfstab only when present
  (P160).
- Upgrade ipvs to 0.9.3 (P4008).
- Fix xircom patch (P162) (gc) 
- gdth update to lastest driver (P4517) (juan)
- realtek_cb cardbus driver (P166). (juan).
- Added sam9407 soundcards support (S105) (juan).
- Tulip downgrade to stable drivers (P4518) (juan).
- remove unused kgcc uses. (juan)

* Tue Sep  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-19mdk
- Correct Dell cable detection (A.Cox) (P4516).
- Add another 1885 ident in ac97_codec (A.Cox) (P4506).
- Remove unneeded modules from BOOT kernel (S26).
- Add xircom pcmcia ethernet card (GC) (P162).
- Really add /sbin/cardmgr for kernel-BOOT.

* Mon Sep  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-18mdk
- Added uptodate ext3 code from the ext3 abort-handle-branch
  to handle taking the filesystem offline/readonly on fatal error
  cleanly. (S.Tweedie) (P4019).
- Fix oops in NFS code (A.van de Ven) (P4016).
- Created 'noathlon' DMI blacklist entry for MSI MS-6330 motherboards
  (P4013).
- Fix NFS_STALE handling (T.Myklebust) (P4021).
- NFS reclaim patch that fix nfs going on zombie (H.J Lu) (P4028).
- Improve reiserfs block allocator when free space is low (Namesys)
  (P4035)
- Adds missing call to pathrelse() to error path (Namesys) (P4036).
- Upgrade i810_audio driver to latest 2.4.9-ac6 (P4506).
- Upgrade to latest firewire fixes from cvs. (P4515).
- Emu10k1 driver upgrade to get the ac3/midi sound update (P4007).

* Mon Sep  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-17mdk
- Add support for ide-floppy with devfs (P4510).
- BINFMT Fixes from jakub@redhat.com (P4511).
- fix i386 SMP interrupts that can corrupt registers from
  john.l.byrne@compaq.com (P4512).
- Se401 USB driver update (P4513).
- Rework (P4507) with Se401 update.
- Fix pcilynx pcmcia module with latest firewire (P165).
- Fix scsi removable disk (eg: USB scsi DSC-S30 camera) (P4514).

* Sun Sep  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-16mdk
- Upgrade to 2.4.9-ac4 i810_audio driver (P4505).
- Upgrade to 2.4.9-ac4 ac97_codec (P4506).
- Upgrade to latest USB fixes (kaweth/pegasus/se401/visor/usb-uhci)
  from 2.4.9-ac5 (P4507).
- Upgrade to latest usb-storage (P4508).
- Upgrade to devfs-v191 (P4501).
- Remove HP8200 CDWRITER driver patch (P25).
- Fix eUSB-SmartMedia device (P4509).

* Sat Sep  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-15mdk
- fix for kpnpbios <defunct> (P3017) (juan).
- Wacom updates (P3018) (flepied).
- Remove speedtouch, ppptoatm patches (P521, P518, P519) Rediff (P520)
  (damien).
- JFS-1.0.4 (P4005, P4006).
- Don't use kgcc anymore.

* Fri Aug 31 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.14-14mdk
- used kgcc for compilation.
- changed position of check for kgcc & boot

* Fri Aug 31 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.8-13mdk
- kernel-source don't require egcs anymore :)
- added kdb dir to the source rpm.
- fix pcilynx compilation (P165).
- remove parpot fix(P4020) merged upstream.
- rediff jfs-shared patch (P4005).
- removed kdb patch merdeg upstream (P3009).
- removed massstorage id75 (P522), merged upstream.
- supermount is back (and this time works ro, wait for more news).
- rediff multipath (P40).
- rediff speedtouch (P519).
- sony-clie merged upstream (P420).
- kdb patch to make it compile (P3016).
- updated kdb.
- 2.4.8-ac12.

* Thu Aug 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-12mdk
- Upgrade to latest devfs (P4500, P4501).
- added perl script for 80 drm building (giuseppe).

* Wed Aug 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-11mdk
- 2.4.8-ac9.

* Tue Aug 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-10mdk
- new version of the psaux fixes (from COL) (P4034).

* Tue Aug 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-9mdk
- Upgrade QLA1280 driver (P17) (remove P23 and adapt P348).
- JFS-1.0.3 (P4005, P4006).

* Tue Aug 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-8mdk
- 2.4.8-ac8.
- Remove (P487).
- Adapt (518).
- Fix Pcmcia Filelist (giuseppe).

* Mon Aug 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-7mdk
- Remove : iport-ethernet patch merged in upstream. (P165).
- Add /etc/pcmcia/cis to the files list of pcmcia.
- Build and ship lspnp utils in pcmcia package.
- RH-Patches:
- Make ext3 log in syslog (P4019).
- Add fixes for parport (P4020).
- Make the maximum init env bigger (P4022).
- Force MPTABLE parsing on defective Intel bioses (P4023).
- Fix elevator hang (P4024).
- Be more strict about the pdcraid signature (P4025).
- Allow VFAT exports over NFS (neilb) (P4026).
- Make the scsi timeout longer (P4027).
- Add ethtool for acenic and eepro (TODO: others mdk/net drivers)
  (P4029).
- Make the kernel shut up when there is no PSAUX keyboard (think usb) (P4030).
- Cramfs fixes (P4031).
- make oom killer less trigger happy (P4032).
- Patch the triplelock (P4033).

* Mon Aug 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-6mdk
- 2.4.8-ac7.
- Adapt (P1001).
- Remove (P4016).
- Add MassWorks ID-75 USB Driver (P522).
- Sym53c8xx fixes from sun (P486).
- USBcore fixes from zaitcev@redhat.com (P487).
- Add USB Sony clie support (P420).
- Upgrade Vlan to 1.4 (P1006).
- Add support for Xircom PGSDB9 (P421).
- Pcmcia-3.1.28.
- Remove (P158, P162, P163).
- Add ibmtr_compilation fix (P158).
- Giuseppe changes :
- fixed kernel-2.4.8-*.config config for 8.0.
- kernel-enterprise with 4GB RAM support instead of 64GB in HIGHMEM
- BuildRequires: libgr1-devel if %%build_80.
- added %dir in %%{_modulesdir}/%%{KVERREL}/ in %%files sections.

* Tue Aug 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-5mdk
- 2.4.8-ac5.
- Copy the cardmgr for install team when kernel BOOT.
- Remove (P4013).
- Adapt (P4018).

* Tue Aug 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-4mdk
- BLK_DEV_FD=y as module it's too much buggy.
- Merge RedHat Patches.
- Compile with gcc and not kgcc if build_boot to reduce the kernel.
- Make APIC error in syslog (P4012).
- Add ATA66 for Servraid (P4013).
- Add more sound_blaster ID (P4014).
- Use PNP_BIOS for parport only if compiled as modules (P4015).
- Add support for National Semiconductor DP8382 Card (P4016).
- Add Iscsi Card support (P4017).
- Add a Config-Small patch that make the kernel less bigger in case of
  BOOT kernel (P4018).

* Tue Aug 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-3mdk
- 2.4.8-ac3.
- Remove new dpt_i2o (P4000).

* Mon Aug 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-2mdk
- 2.4.8-ac2.
- Fix ATM (P485).
- Add id for NEC Picty900 (HP OEM) (USB printer) (P508).
- Fix --with BOOT macros.

* Sun Aug 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.8-1mdk
- 2.4.8-ac1.
- Remove emu10k1-mixer patch (P415).
- Add speedtouch driver fixes (dams) (P521).
- Add config for pcmcia iport ethernet card (P165).

* Fri Aug 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-14mdk
- 2.4.7-ac11.
- Upgrade lanstreamer tokernring driver (P3004).
- Upgrade BOOT config (S26).
- supermount -i disable if we are in update mode.

* Thu Aug  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-13mdk
- 2.4.7-ac10.
- Remove drm-update patch (P3004).
- Remove i810-fixes patch (P3005).
- Remove sis-fixes patch (P3006).
- Remove drm-silence (P508).
- Build old drm for if %%build_8 is here.

* Wed Aug  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-12mdk
- 2.4.7-ac9.
- Remove ac7_is_ac8 patch (P2003).

* Tue Aug  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-11mdk
- Add VLAN support (P1006) (Oden).
- Disabled new drm when build_80 enabled (giuseppe).
- Removed BuildRequires: netpbm,libnetpbm when build_80 enabled (giuseppe).
- Fixed a typo in %preun scripts (giuseppe).

* Tue Aug  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-10mdk
- 2.4.7-ac8.
- Remove atyfb-compilation-fix (P3008).
- Adapt jfs-shared patch (P4006).
- Ac8 is ac8 not ac7 (P2003).

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-9mdk
- BuildRequires update (stefan).
- New bootlogo from LN (S18).
- Patch for ohci1394_cs for the new ohci update of latest kernel (P164).

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-8mdk
- 2.4.7-ac7.
- Add bcm5820 crypto card support from RH (P4010, P4011).
- Fix AtyFB compilation (P3008).
- Add macros %%build_80 to generate update for 8.0 kernel.
- Add macros %%build_boot to generate BOOT kernel.

* Sun Aug  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-7mdk
- 2.4.7-ac6.
- Remove jffs2 fix (P3008).
- Remove floppy-fix (P3010).
- Remove ieee1394-fix (P3011).
- Remove aha152x-fix (P3012).
- Add kernel version just before the boot logo (P490).
- Apply %patch101 before doing mkpatch of lm_sensors (thanks: Andre Duclos).
- Adjust Buildrequires (thanks: Stefan).

* Sat Aug  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-6mdk
- Fix pcmcia network script (s.siegle)(S1000).
- JFS-1.0.2 (P4005, P4006).

* Sat Aug  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-5mdk
- 2.4.7-ac5.
- Adapt multipath patch (P40).

* Fri Aug  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-4mdk
- 2.4.7-ac4.
- Upgrade boot logo from LN (S18).
- Adapt multipath patch (P40).
- Adapt 3rdparty patch (P2000)
- Remove aironet4500-fix patch (P3013)
- Fix EXPORT_SYMTAB conflicts between ipvs patch and ext3 (P3015).
- Adjust Requires.

* Thu Aug  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-3mdk
- Depend of devfsd.
- 2.4.7-ac3.
- Adapt hp8200e patch (P25).
- Adapt speedtouch patch (P519).
- Adapt usbvision patch (P520).

* Wed Aug  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.7-2mdk
- Disable yenta patch.
- Fix rebuild of aic7xx firmware.
- Add JFS integration.

* Tue Jul 31 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.7-1mdk
- aironet4500 compilations fixes.
- axnet_cs compile fixes.
- aha152x fix.
- lots of s/wait_for_completion/wait_completion/ in pcmcia drivers.
- s/wait_for_completion/wait_completion/ in floppy driver.
- added jffs2 fix to use completion.
- disabling reiserfs quota (hangs at boot).
- added patch for detecting yenta socket in 2.4 (from rh) (#161).
- enabled DEVFS support (but not DEVFS_MOUNT), if you want it mounted on boot, use the devfs=mount option.
- updated reiserfs quota patch and applied it again.
- removed viadma patch (#515) as we are not using it for quite some time.
- Removing last vestiges of proc-fs (#600) patch (it wasn't applied).
- made gzip of modules less verbose (yes, I normally read rpm output).
- big pcmcia spec file update (we missed a lot of files).
- added scsimon module.
- added spectrum24t pcmcia driver, but it is quite buggy :(
- bttv update (#482) integrated upstream.
- ac2.
- Added a different fix for pcmcia man pages :(
- Removed the fix for pcmcia man pages.
- kernel-2.4-string (#11) is gone (was accepted upstream).
- fix pcmcia ohci breakage.
- usual update of .configs with new kernel.
- removed a lot of cruft in the version handling of the kernel, %srcversion 
  is now are now %kversion.
- removed spurious x of pcmcia-cs-3.1.27-network script, and while at that 
  check that we have a ifcfg-file for the device before calling the if*.
- added spectrum driver.
- added scsimon patch (#1004);
- Supermount is here again (and ppc shouldn't need additional patches anymore).
- enabled CONFIG_IPSEC_DEBUG in all .config.
- #490 (firewire) integrated upstream.
- sard rediff.
- ide-floppy rediff.
- more changes in the saveheaders thing, this time should be right :(
- ac1.
- 2.4.7.
- removed patch #157 (ibmtr-fix) integrated upstream pcmcia-cs.
- pcmcia-cs 3.1.27.
- s/Copyright/License/ (as everybody else).

* Tue Jul 17 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.6-5mdk
- include asm-generic in headers package.
- more drm re-patching :-(
- usb-printer-fix (#604) applied upstream.
- ac5.

* Sat Jul 14 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.6-4mdk
- update all the configs.
- now 3rdparty modules should be _all_ compiling again.
- cleaning problems with gcc/kgcc in BuildPCMCIA.
- ppc sync (stew).
- patch #3003: Add support for Silicom U2E (Kaweth driver) 
  (Alain Wenmaekers <spicyalan@pandora.be>).
- patch #399 (lm_sensors stuff) is gone (not needed neither alpha nor pcc now).
- syncronize provides/requires/prereq between kernels (and define macros to 
  not lost sync anymore).
- reorganization of saveheaders code (Ural Khassanov <ural@uwc.ufanet.ru), 
  modifide by me.
- du-e100 support (Mathias).
- two less RPM_SOURCE_DIR in the spec (still no idea how to fix the one 
  which remains.
- more pcmcia rearganization, now there is a %if %build_pcmcia by section.
- reorganise all the addons patches together indicating what package 
  they belog to.
- remove DependKernel code from install phase.

* Tue Jul 10 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.6-3mdk
- a lot of small alsa typos for getting 2.96 able to compile it.V
- create a dir macros and do all the substitutions.
	* _bootdir
	* _modulesdir
- create temp_root variable, now during build, we put everything in 
  $RPM_BUILD_DIR and later we install everything in $RPM_BUILD_ROOT
  (aka %{buildroot}.
- nice trick stolen from rh for defining what kernel compile from the 
  command line
- fix alsa to compile with gcc-2.96.
- cleaning up the uses of kgcc to be able to compile with other compilers.
- make include/linux/version.h is implicit in make dep, removing.
- dc395x_trm now is a 3rdparty module and compiled with gcc-2.96.

* Sat Jul  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.6-2mdk
- ac2.
- add 'if build_pcmcia' in a couple places
- do not build patch 399 on alpha, it breaks
- update alpha config
- update other configs for ac2

* Sat Jul  7 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.6-1mdk
- realmode-power-off is gone (together with the compilation option).
- Lots of rediff of patches to put here.
- Disable supermount (need a lot of work to make it work).
- Broadcom BCM5700 is a 3rdparty now.
- removed usb-quiet patch(#601). Merged upstream.
- removed netfilter-cpp patch (#503). Merged upstream.
- removed reisernfs patch (#472). Merged upstream.
- removed raid5readbypass (#454). Merged upstream.
- include include/pcmcia in source package to be able to compile in 
  kernel pcmcia. 
- new kdb patch.
- ac1.
- 2.4.6.
- quickcam is now also a 3rdparty module (and fixes from Andre Duclos).

* Wed Jun 27 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-9mdk
- SiS now have drm support.
- lot of drm testing & patchin it should work now.
- enable TMPFS (Jeff request some eons ago).
- new kdb version.
- lm_sensors 2.6.0.
- i2c 2.6.0.
- freeswan 1.91.
- ac18.
- update bttv patch to 0.7.68 (Thierry Vignaud).
- usb-audio-fix (#3002) integrated upstream.
- ac17.

* Fri Jun 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.5-8mdk
- Fix i810 drm.

* Thu Jun 21 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-7mdk
- redone the netfilter patches (you need to update iptables).
- redone the realmode patch.
- integrate autoconf patch (chmouel).
- integrate kdb.
- fix 3rdparty kernel source support.
- Upgrade dpt-i20 drivers (Viet).
- kawetch fix (chmouel).
- quickam driver update (chmouel).
- e100 update to 1.6.5 (1.6.6 is buggy) and e1000 update.  Now both are using 
  3rdparty module support.
- usb-audio fix (chmouel).
- ac15.

* Sat Jun 16 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-6mdk
- nice %setup macro invocations.
- ac14.
- fixes build on SMP (BuildAlsa) (kjx).
- remove lasts vestiges of alsa-beta.
- ppc patches (stew).
- 3rdparty jgarzik patch.

* Wed Jun 13 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-5mdk
- bandaid to get new drm to compile.
- drm update for XFree 4.1.0.
- usb printer fix.
- procfs fix patch.
- usbvision patch.
- add support to bcm5700 network card (from Dell merged from rh).
- /lib/modules/<version>/build is back (chmouel request).
- mdkuser xbis gone, now source is back to mdk (chmouel request).
- ac13.

* Mon Jun 11 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-4mdk
- disable 
- disable SUPERIO support (Jeff& Tim advice).
- renable OSB4.
- remove osb dangerous message, if Andre says it is safe, we trust on him.
- apm option real-mode-poweroff has been adopted upstream as realmode.
  Adapt the patch and print a warning if you are using the old option.
- ac12.
- redone all .configs.
- ppc updates (stew).
- make symlinks is gone (make oldconfig implies it).
- /lib/modules/<verions>/build link is gone as:
	a) it should be in the source package
	b) it doen't make sense since we compile several kernels from the 
           same source.
- now is possible to compile only one kernel (smp, up or enterprise).
- visor-palm pilot incorporated in new kernel.
- ac9.
- ac8.

* Mon Jun  4 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-3mdk
- new Cris Evan NFS patches.
- ac7.
- removed define for the update.

* Sat Jun  2 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-2mdk
- s/mkdir -p/install -d/ make SPEC file much more coherent.
- mandrake rpm build procces does the strip of binaries, we don't need to 
  do them (Andre Duclos).
- include all Andre DUCLOS patches.
- include_target, modules_target, boot_target also around.
- create kernel_dir /usr/src/linux-2.4.%{sublevel} and
         source_target %{buildroot}%{kernel_dir}  and use all over the place.
- s/$BUILD_RPM_ROOT/%{buildroot}/g.
- OSB4 disabled (it can corrupt data).
- use alsa-0.5.10b for the update, 0.5.11 for cooker.
- Big merge with ppc kernel (sorry stew for taking so long).
- Big change in Configure.help, that means 4 patches redone.
- ac6.

* Thu May 31 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.5-1mdk
- new daily freeswan snapshot (and several changes with that).
- ac5.
- Support for palm m5* for the visor patch.
- ide-cd fix (discussed with maintainer and will be incorporated in 
  next upstream patch).
- alsa, pcmcia and freeswan drivers don't exist anymore.
- lm_sensors: sensord patch (DUCLOS Andre <shirka@wanadoo.fr>).
- redone the SPEC file to be able to compile only smp, enterprise or up.
- including math-emu dir in source (jeff request)
- the bug was indeed in supermount (a spurious &).
- finding the bug fooling the bug sequence (I find the bug, arjan & viro did the patch). 
- wacom driver in ac2 is newer than our (removed patch).
- ac4 is out.
- less neil brown fixes.
- parport messages are out now.
- ac2.
- 2.4.5.

* Fri May 25 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.4-7mdk
- hga fix accepted upstream.
- remove usbdevfs-fix-mount-options parse (merged upstream).
- rediff wacom patch.
- rediff supermount patch.
- rediff speedtooch patch.
- ac17.
- update (again) the netfilter-addons patch as author recomendation.
- added patch for fealnx patch (bug jeff for it) (and later acepted upstream and removed).
- nobody else that me saw that version (as it didn't boot ....)

* Wed May 23 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.4-6mdk
- due to the lm_sensors change, redo again all the .config files.
- Macros in spec for updates(chmouel).
- Fix lm_sensors generation patch (DUCLOS Andre <shirka@wanadoo.fr>).
- update all the .config files.
- irc netfilter add-on is back (regenerated with last netfilter).
- fix alsa source packages naming (pointed by Chmouel).
	
* Tue May 22 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.4-5mdk
- 2.4.4-ac14.
- remove binfmt patch added in 4mdk, it is now in ac14.

* Tue May 22 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.4-4mdk
- bin_fmnt symbol problem (J Magallon).
- More merges of new Neil Brown patches.
- now parport messages should be right.
- serctorresync patch integrated in ac11 (#452).
- alsa-drivers 0.5.11.
- ac12.

* Mon May 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.4-3mdk
- Really fix the usbdevfs mount as user (and let the /proc don't crash).
- add libgr1-progs buildreq deps (jgarzik).

* Mon May 21 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.4-2mdk
- fix the make modules bug.
- linux-logo hga fb fix.
- ppc patches (2nd round) by stew.
- Neil Brown patches update.
	* mderror is included in ac.
- usb-uhci (patch #42) removed, better fix in ac.
- IDE_CD is compiled in the kenel again (I need to change first mkinitrd).
- We don't depend of rdev anymore as  we don't use it in the kernel rpm
  (not having that requeriment make ppc people happier).
- ac11.

* Tue May  8 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.4-1mdk
- ECN enabled & requires initscripts 5.83 for that reason.
- 2.4.4-ac9.
- removed ips patch (we had version 0.50 and alan integrated 0.78).
- created lm-ultils-devel subpacage (Oden.eriksson).
- Removed acpi (as we was not using it anyways)
- Big CleanUp of the Spec File.
- Now pcmcia-network get the right source file.
- /etc/sysconfig/pcmcia is a source file also.
- aic7xxx 6.1.13 is merged in ac9.
- merged ppc patches (some tweaking) by sbenedict.
- integrate usbvision support (patch #475).
- pcmcia-cs 2.1.26.
- integrate endian-reiserfs patch with 2.4.
- make ibmtr pcmcia driver to compile.
- enable ACENIC on alpha.
- remove psaux mouse workaround (it is working well here now).
- I don't remind all the things that I have changed.

* Mon May  7 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-27mdk
- redone the aic7xxx 6.1.13 patch completely.

* Sat May  5 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-26mdk
- fixes ./network resume eth0 (pcmcia).
- aic7xxx 6.1.13.

* Thu May  3 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-25mdk
- ide-cd returns to be a module.
- psaux driver return to wait 500 seconds.

* Mon Apr 30 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-24mdk
- Remove Neil Brown NFS patches.
- Introduce Chris Evans reiser NFS patches.
- now the parport messages are not in console by default (aka. Winbond xxxx)
  (this time I included the patch).
- psaux problem should be solved (thanks to Chmouel) for thinkpad's and the 
  old problem at the same time.
- Remove Neil Brown calltrace patch (it was ix86 only anyway, and of no use 
  for end users).
- Did the keyboard timeout handling less verbose (aka your shiny new 
  computer with keyboard & mouse USB don't give you AT keyboard warnings :)
- Undo ECN.

* Sat Apr 28 2001 Stefan van der Eijk <stefan@eijk.nu> 2.4.3-23mdk
- updated alpha .spec file --> CONFIG_ACENIC is not set.

* Wed Apr 25 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-22mdk
- ac13.

* Mon Apr 23 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-21mdk
- ac9^H10^H11.
- remove aic7xxx driver update (is in ac9).
- new NFSD patches from Neil Brown.
- reiserfs >4GB should work now.
- cleanup of enterprise and normal-kernels .config, now they are quite similar.
- cleanup specfile (requires libgr1-devel and no more yacc & db *)
- entreprise kernel is only for x86. Stefan van der Eijk.
- update alpha .config.
- now the parport messages are not in console by default (aka. Winbond xxxx).

* Sun Apr 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-20mdk
- Make supermount handle new FS_SINGLE type of filesystem.
- Make supermount works with rename files.
- Rework nologo patch to be active only when CONFIG_FB is set.

* Fri Apr 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-19mdk
- usbdevfs, fix mount with owner and gid.

* Fri Apr 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-18mdk
- Add ppptoe-pptoa patch for modem over ATM (matt).
- Add USB speedtouch drivers. (matt).
- Remove natsemi patch it's already fixed in an other form.
- Really apply the aic7xx upgrade.

* Thu Apr 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-17mdk
- Disable my netdebug patches since it doen't do anything.
- Disable CONFIG_APM_DISPLAY_BLANK.
- Fix compilation with rnfs nfsops when NFSD=n
- CONFIG_DEBUG_BUGVERBOSE is off.
- Merge with rh patches:
- fix an off by one error that results in memory overwrites
- Silence PS/2 code (no keyboard there if there is a USB keyboard)
- Make drm error sysloged and not printkconsoled.
- panic on oom during boot
- fix netgear fa31x boards powerstate
- Add mulipath-fixes from Ingo Molnar
- make scanning of sparselun devices work again
- advice as Dangerous the ServerWorks OSB4 chipset
- disabled dma66 for all via IDE chipsets to don't run in problems.
- Add USB message throttling
- fix printk in scsci messages

* Wed Apr 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-16mdk
- Don't do any link creation installkernel does it for us.
- Dependences of up at the last end of dependences system.

* Wed Apr 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-15mdk
- Add special enterprise kernel with 64Gb support Apic etc...
- Really make active ATM modules.

* Tue Apr 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-14mdk
- Redo complete dependences configuration to be able to recompile
  drivers between kernel (mainly inspired by the Red Hat work).
- Revert to -ac3 the 8139too as request by jeff.
- Don't depend on any ppm files.
- 2.4.3-ac4.
- Active ATM.
- iostat incremental no need anymore (by default in 99)

* Tue Apr 10 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.3-13mdk
- Add Ingo's ext2 corruption fix.

* Mon Apr  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-12mdk
- Upgrade to the latest cvs of firewire to get it works.

* Mon Apr  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-11mdk
- fix pcmcia again :p.
- fix kgcc call (prumph).

* Sat Apr  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-10mdk
- Add ln -sf /boot/config-version to /boot/config in %post.
- When inserting pcmcia module don't insmod module.o or module.o.gz
  just insmod module.
- Add option nologo to disable the logo display at boot.
- Launch pcmcia scrpt early before the network.

* Sat Apr  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-9mdk
- Fix logo in high resolution and leave some boot kernel message.

* Thu Apr  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-8mdk
- bttv upgrade to 0.7.62.

* Thu Apr  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-7mdk
- 2.4.3-ac3.
- Fix wait on psaux port (prumph).

* Thu Apr  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-6mdk
- Fix a SMP race (Ben Lahaise).
- Add MODULE_DEVICE_TABLE in some USB modules for USB detection (prumph).
- Add .config in /boot/config-version
- IPSEC-1.9.

* Thu Apr  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-5mdk
- Disable NETDEBUG.
- set CONFIG_IPV6_EUI64 CONFIG_IPV6_NO_PB

* Tue Apr  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-4mdk
- Upgrade of olympus token ring card.
- Provides Alsa also for kernel-smp.
- Add new mdk boot logo (and boot logo patches).
- Don't do SMP by default.
- CONFIG_LP_CONSOLE broke printer and useless disable it.
- Disable IP_AUTOCONFIGURATION (useless and slow the boot).
- Define CONFIG_PIIX_TUNING.
- Make IDEFLOPPY into the kernel and not as modules.
- Unactive CMS_FS filesystem (too beta).
- Active CONFIG_NCPFS_PACKET_SIGNING and CONFIG_NCPFS_STRONG.

* Mon Apr  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-3mdk
- Add support for gazel hisax R753 (Mattias).
- Remove %doc README to avoid conflicts when doing rpm -i

* Mon Apr  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.3-2mdk
- Add logiteck quickcam usb drivers.

* Mon Apr  2 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.3-1mdk
- 2.4.3.
- 2.4.3-q1 (aka 2.4.3-ac1 if Juan Quintela were Alan Cox).
- Updated to aic7xxx 6.1.8.
- Hacking the numbering to have to hack "only one place".

* Sun Apr  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-25mdk
- Reiserfs Quota disabled seems to make problems with rfs.

* Sun Apr  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-24mdk
- Merge latest neil brown patches.

* Sun Apr  1 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-23mdk
- Upgrade alpha config files (stefen).
- kernel-ource and BuildRequires: byacc.
- Update wacom usb drivers from fredl.
- Merge Red Hat patches.
- Fix alpha includes.
- Fix qla driver.
- Upgrade ide-floppy
- Upgrade to the latest ipvs patch
- Remove timer of the qla driver
- Skip broken mp table
- HP8200 CDWRITER driver
- Fix i2o lockup
- Add IRC netfilter addon.
- Move some printk to some LEVEL of errors.
- Don't printk when	polling CDROMs for disk change
- Add scci reset support
- Up some pcmcia delay.
- Adding a fix for usb-uhci to work when SLAB is not aligned
- Add alternate airo devices drivers
- Fix atp max units.
- Add an iotcl to block sector for ia64.
- Fix ext2 info errors.
- define DK_MAX_MAJOR to 64
- Revert some bogus changes to lp-parport.
- Add multipath for raid.
- Fix pge Config.in description
- Add sard profiling patch

* Thu Mar 29 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.2-22mdk
- Updated to ac28

* Thu Mar 29 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.2-21mdk
- Updated to ac25^H6^H7.
- Removed linux-2.4.1-ac3-es1371-new-ids.patch.bz2.

* Wed Mar 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-20mdk
- Define tone control in emu10k1 mixer.
- Fixes supermount to ally ejecting -EBUSY device.


* Tue Mar 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-19mdk
- Active Bigmem by default.
- Apply/adapt quota patch for reiserfs.
- Merge Suse Patches.
- Add progress indication when decompressing ramdisk
- Fix Config files with CONFIG_X86_RUNTIME_FXSR
- Add TIOCGDEV ioctl
- Make APM_REAL_MODE_POWER_OFF as option (at boot) not at compilte
  time option.

* Sun Mar 18 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.2-18mdk
- Fix overwite of Alpha fix patch from 2.4.2-15mdk.

* Fri Mar 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-17mdk
- Requires last initscripts.
- Add options -r to installkernel (to clean entry) if we are in
  beginner mode in /etc/sysconfig/system.

* Fri Mar 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-16mdk
- Make lm_sensors don't depend of libs.
- Upgrade dpt-i20 drivers (Viet).

* Wed Mar 14 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.2-15mdk
- Apply a fix to filesystem corruption in VIA chipsets.

* Wed Mar 14 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.2-14mdk
- The never released version

* Tue Mar 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-13mdk
- 2.4.2-ac20.
- Add wireless-pcmcia patch from rh.
- Fix pcmcia when modules is gzipped.
- Don't be SMP by default.

* Mon Mar 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-12mdk
- Update alpha config (jeff).
- 2.4.2-ac19.
- Pcmcia-3.1.25.
- Readd ipsec.

* Sun Mar 11 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.2-11mdk
- update alpha config
- fix alpha build

* Sun Mar 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-10mdk
- Remove aicasm binary generated.
- Remove initrd.img after uninstalling package.
- 2.4.2-ac18.

* Fri Mar  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-9mdk
- Fix atyfb as modules.
- (Build)Requires: flex, db3-devel, bison for kernel-source.
- Requires: modutils last version that support gz modules.
- 2.4.2-ac16.

* Thu Mar  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-8mdk
- Gzip modules.
- Fix pcmcia and aacraid..
- Upgrade to the last aacraid (and fix it ac13 among all others scsci
  patches).
- 2.4.2-ac14.
- Don't set IO-APCI on non SMP kernel (break PIV for example).

* Mon Mar 05 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.2-7mdk
- Making sure that non-SMP kernels are not SMP.
- Alan Cox patch 2.4.2-ac11-fixed.
- Spec cleanup.
- .config cleanup:
- Use APIC also now on uniprocessor.
- 	use E820.

* Wed Mar 03 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.2-6mdk
- Merged last neil patches.

* Wed Mar 03 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.2-5mdk
- Alan Cox patch 2.4.2-ac10.
- SPEC cleanup.
- New megaraid patch is ac kernel.

* Wed Feb 28 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.2-4mdk
- Alan Cox patch 2.4.2-ac6.

* Tue Feb 27 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.2-3mdk
- Alan Cox patch 2.4.2-ac5.
- Temporarily disable usb scanner update, patch breaks.
- Update i586 and alpha configs for new ac patch.

* Mon Feb 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-2mdk
- Fix sublevel.

* Sun Feb 25 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.2-1mdk
- Linux 2.4.2 release.
- Alan Cox patch 2.4.2-ac4.
- Update x86 and alpha configs.
- Remove loop fixes, already in newest 'ac' kernel.
- Temporarily disable ide-floppy, patch breaks.
- Temporarily disable ipsec, patch breaks.

* Wed Feb 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-22mdk
- 2.4.1-ac20.

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-21mdk
- Add ipsec 20001115 snapshot version (for 2.4.x kernel we need a snap).
- alsa-0.5.10b.

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-20mdk
- Add fixes from Red Hat for the loop problems.

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-19mdk
- Add support for COMET accton cards in tulip drivers (Jeff).
- Merge Neil-Brown nfs patches :
- Do permission checking for IRIX accessing special devices properly.
- Provide an "nfsd_operations" interface between knfsd and each filesystem.
- Add support for knfsd in reiserfs.
- isofs support for nfsd_operations.
- knfsd support for ufs.
- nfsd support for efs.
- Change raid resync code to work in sectors, not blocks.
- Make sure all raid5 IO requests are properly aligned.
- Modify the wdelay handling.
- Bypass stripe cache for reads.
- Disable the reboot notifier.
- Provide call trace in /proc/X/status.
- Use sector number of b_blocknr is raid1 bufferes.
- Return slightly more meaningful geometry for raid arrays.
- Change args of md_error to be mddev_t instead of kdev_t.

* Tue Feb 20 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-18mdk
- 2.4.1-ac19.

* Sun Feb 18 2001 Stefan van der Eijk <s.vandereijk@chello.nl> 2.4.1-17mdk
- 2.4.1-ac18
- updated alpha .config

* Sat Feb 17 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-16mdk
- 2.4.1-ac17.
- requires egcs and egcs-cpp to build the kernel source (due to
  problems with gcc-2.96).

* Fri Feb 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-15mdk
- 2.4.1-ac15.

* Thu Feb 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-14mdk
- 2.4.1-ac13.

* Wed Feb 14 2001 Juan Quintela <quintela@mandrakesoft.com> 2.4.1-13mdk
- Removes ksymoops from the kernel package
- Comment wvlan patch as we are not using kernel pcmcia
- Fix modutils version check

* Tue Feb 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-12mdk
- 2.4.1-ac12.

* Tue Feb 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-11mdk
- 2.4.1-ac11.

* Tue Feb 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-10mdk
- 2.4.1-ac10.
- Oden Eriksson <oden.eriksson@kvikkjokk.net>:
	* added TechWell TW98 i2c driver support, patch 504.

* Sat Feb 10 2001 Stefan van der Eijk <s.vandereijk@chello.nl> 2.4.1-9mdk
- 2.4.1-ac8
- add patch for lm_sensors prob with perm.h (alpha)

* Fri Feb  9 2001 Stefan van der Eijk <s.vandereijk@chello.nl> 2.4.1-8mdk
- 2.4.1-ac7
- moved patch 362 into the pcmcia section

* Thu Feb  8 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.1-7mdk
- update alpha config

* Wed Feb  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-6mdk
- 2.4.1-ac6.

* Wed Feb  7 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-5mdk
- make oldconfig && make dep before shipping kernel-source.
- Upgrade loop patch from jens axboe.
- Add alternatives Lucen Wavelan wireless support.
- Fix bad udelay with wavelan.
- Add aacraid drivers.
- Raid force to use SSE xor block to be able to write around L2.
- Fix assertion of kiobuf to map to user.
- Fix IRDA assertion.
- Add e810 Acpi proc information (not activated by default since we
  don't use ACPI).
- Add e1000 drivers.
- Upgrade e100 drivers.
- Desactive Devfs.
- Add 3c90x drivers.
- 2.4.1-ac4.
- pcmcia-3.1.24.

* Mon Feb  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-4mdk
- Upgrade qlogic drivers to 2.19.15.
- Upgrade swap limit to 32.
- Upgrade megaraid drivers.
- Add intel100 network drivers.
- Upgrade ips.
- Upgrade idetape.
- Add new ids for es1371 cards.
- Add dpt_i2o support.
- Add dc395 update.

* Mon Feb  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-3mdk
- 2.4.1-ac3.

* Mon Feb  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-2mdk
- fix the version field.

* Mon Feb 05 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-1mdk.
- 2.4.1-ac2.

* Sun Jan 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-12mdk
- Add loop fixes from jens axboe.
- Add patch from rh (emu10k1 fixes, overflow check, noghighmemdebug,
  netfilter cpp fixes).

* Sat Jan 27 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.0-11mdk
- Update alpha config

* Sat Jan 27 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-10mdk
- 2.4.0-ac12.

* Thu Jan 25 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-9mdk
- Make pcmcia config files as noreplace.
- Upgrade ide-floppy for ac11 (author).
- Really apply LVM fixes.

* Wed Jan 24 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-8mdk
- LVM proc fixes from andrea

* Wed Jan 24 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-7mdk
- Alsa-0.5.10b.
- Remove reiserfs-utils.
- 2.4.0-ac11.

* Tue Jan 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-6mdk
- Add upgrade of ide-floppy drivers.
- Add rivatv lm_sensors support (oden).
- Add lm_sensors package in the source (and generate the patch from
  package) (oden)
- really integrating ksymoops-2.4.0 (oden.eriksson@kvikkjokk.net).
- Upgrade usb scanner.
- Remove all modules.*
- Add NFSv3 Patches.

* Mon Jan 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-5mdk
- Upgrade smctr from ac series to get the bad_udelay symbol fixed.
- Supermount upgrade.

* Fri Jan 12 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-4mdk
- Reorganise spec files.
- ksymoops-2.4.0.

* Fri Jan 12 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.0-3mdk
- Update alpha config

* Tue Jan  9 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-2mdk
- Pcmcia-3.1.23.
- Alsa-0.5.10a.

* Tue Jan 09 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-1mdk
- 2.4.0
- Reiserf 3.6.25

* Wed Dec 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.15mdk
- Don't be SMP by default (jeff don't do titi-ries :p).
- Reiserfs-3.6.23.
- Reactive Reiserfs since i got it worked with supermount.

* Thu Dec 14 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.0-0.14mdk
- update .configs for i586 and alpha

* Tue Dec 12 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 2.4.0-0.13mdk
- 2.4.0-test12-final
- build on alpha
- 2.4.x does not require dev86

* Sat Dec  9 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.12mdk
- Add patches to fix initrd from aviro/linus.

* Fri Dec  8 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.11mdk
- Add support for Alpha from Jeff Garzik <jgarzik@mandrakesoft.com>
  and Stefan.

* Thu Dec  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.10mdk
- Make installkernel doing a -a when doing make install of sources.
- Disable pcilynx until get it fixed.
- alsa-0.5.10.

* Thu Dec  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.9mdk
- test12-pre7.

* Wed Dec  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.8mdk
- test12-pre6.
- Upgraded description.
- Disable reiserfs until get updated writepage patch (fix supermount
  BTW: but it's an another problem).

* Tue Dec  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.7mdk
- Add reiserfs (&bigmem unset).
- test12-pre5.

* Mon Dec  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.6mdk
- Really add pcmcia includes.
- Remove /home/chmou references.
- test12-pre3.
- Add supermount.
- Really remove devfsd depends.

* Sun Nov 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.5mdk
- Regenerates lm_sensors patches from cvs (112200).
- Include include/pcmcia in the source (thnks: C.Gennerat).
- remove devfsd dependences.

* Sun Nov 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.4mdk
- BuildRequires: egcs if enabling kgcc.
- Don't copy all configs file from RPM_SOURCES_DIR to configs/ copy
  one and the generated one.
- set CONFIG_BLK_DEV_OFFBOARD.
- unset CONFIG_INET_ECN.
- Don't update acpi (doen't build at the moment).
- test11(final).

* Sun Nov 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.3mdk
- copy the default mandrake config to defconfig before shipping.
- Remove patch200 (include with ksymoops2.3.5.)
- ksmoops 2.3.5.
- Last acpi.

* Thu Nov 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.2mdk
- mrproper the source before shipping.
- fix depmod.
- don't strip the vmlinuz.

* Tue Nov 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.0-0.1mdk
- First version to move on kernel-2.4.0 based on hackkernel. (aka: god
  pray for all of us).

# Local Variables:
# rpm-spec-insert-changelog-version-with-shell: t
# End:
