#
# spec file for package modutils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		modutils
%define version 	2.4.26
%define release 	%_revrel

%define url 		ftp://ftp.kernel.org:/pub/linux/utils/kernel/modutils/v2.4
%define priority 	10

%define toalternate	insmod lsmod modprobe rmmod depmod modinfo

Summary:	The kernel daemon (kerneld) and kernel module utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		%{url}
Source0:	%{url}/%{name}-%{version}.tar.bz2
Source1:	modules.conf
Source2:	macros
Patch0:		modutils-2.4.13-systemmap.patch
Patch1:		modutils-2.4.2-prepost.patch
Patch2:		modutils-2.4.6-silence.patch
Patch3:		modutils-2.4.12-ppc3264.patch
Patch4:		modutils-2.4.22-various-aliases.patch
Patch5:		modutils-2.4.13-no-scsi_hostadapter-off.patch
Patch6:		modutils-2.4.22-pre_post_and_usbmouse.patch
Patch7:		modutils-2.4.26-agpgart-26.patch
Patch8:		modutils-2.4.26-mdv-gcc4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	zlib-devel
BuildRequires:	gperf
BuildRequires:	glibc-static-devel

Requires(post):	rpm
Requires(postun): rpm
ExclusiveOs:	Linux
Obsoletes:	modules
Provides:	modules

%description
The modutils packages includes the kerneld program for automatic
loading and unloading of modules under 2.2 and 2.4 kernels, as well as
other module management programs.  Examples of loaded and unloaded
modules are device drivers and filesystems, as well as some other
things.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .systemmap
%patch1 -p1 -b .prepost
%patch2 -p1 -b .silence
%patch3 -p1 -b .ppc3264
%patch4 -p1 -b .various-aliases
%patch5 -p1 -b .scsi-off
%patch6 -p1 -b .ppost_and_usbmouse
%patch7 -p1 -b .agpgart-26
%patch8 -p1 -b .gcc4


%build
%serverbuild
%configure2_5x \
    --disable-compat-2-0 \
    --disable-kerneld \
    --enable-insmod-static \
    --exec_prefix=/ \
    --enable-zlib \
    --disable-combined \
    --enable-combined-insmod \
    --enable-combined-rmmod

%make dep all


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/lib/modutils
mkdir -p %{buildroot}/sbin
%makeinstall sbindir=%{buildroot}/sbin

pushd %{buildroot}/sbin
    for i in %{toalternate};do
        if [[ -L $i ]] && echo %{toalternate} | grep -q "$(readlink $i)"
        then
            ln -s "$(readlink $i)"-24 $i-24
            rm -f $i
        else
            mv -v $i $i-24
        fi
        ln -s $i-24 $i.old
    done
popd

pushd %{buildroot}/%{_mandir}/man8
    for i in %{toalternate};do
        mv -v $i.8 $i-24.8
        ln -s $i-24.8 $i.old.8
    done
popd

# security hole, works poorly anyway
rm -f %{buildroot}/sbin/request-route
#%ifarch %{ix86}
#rm -f %{buildroot}/sbin/*.static
#%endif

install -D -m 0644 %{SOURCE1} %{buildroot}/etc/modules.conf
install -D -m 0644 %{SOURCE2} %{buildroot}/lib/modutils/macros


%post 
for i in %{toalternate};do
    # needed for link to be created by alternatives
    rm -f /sbin/$i
    update-alternatives --install /sbin/$i $i /sbin/$i-24 %{priority}
    update-alternatives --install \
        %{_mandir}/man8/$i.8%{_extension} man-$i %{_mandir}/man8/$i-24.8%{_extension} %{priority}
    [ -e /sbin/$i ] || update-alternatives --auto $i
    [ -e %{_mandir}/$i.8%{_extension} ] || update-alternatives --auto man-$i
done


%postun
for i in %{toalternate};do
    if [ ! -f /sbin/$i-24 ]; then
        update-alternatives --remove $i /sbin/$i
    fi
    [ -e /sbin/$i ] || update-alternatives --auto $i

    if [ ! -f %{_mandir}/man8/$i-24.8%{_extension} ]; then
        update-alternatives --remove man-$i %{_mandir}/man8/$i.8%{_extension}
    fi
    [ -e %{_mandir}/man8/$i.8%{_extension} ] || update-alternatives --auto man-$i
done


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) /etc/modules.conf
%dir /lib/modutils
%config(noreplace) /lib/modutils/macros
/sbin/insmod_ksymoops_clean
/sbin/genksyms
/sbin/kallsyms
/sbin/kernelversion
/sbin/ksyms
/sbin/*old
/sbin/*24
#%ifnarch %{ix86}
/sbin/insmod.static
/sbin/rmmod.static
#%endif
%{_mandir}/*/*24*
%{_mandir}/*/*old*
%{_mandir}/man1/*
%{_mandir}/man2/*
%{_mandir}/man5/*
%{_mandir}/man8/genksyms.8*
%{_mandir}/man8/kallsyms.8*
%{_mandir}/man8/ksyms.8*

%files doc 
%defattr(-,root,root)
%doc COPYING README CREDITS TODO 
%doc ChangeLog NEWS example/kallsyms.c include/kallsyms.h


%changelog
* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26
- renumber patches
- P8: fix gcc4 build
- add -doc subpackage
- rebuild with gcc4
- remove the ghost files as they break alternatives on uninstall

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26
- install {insmod,rmmod}.static on x86 hardware too

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26-6avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26-5avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26-4avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.26-3avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 2.4.26-2sls
- PreReq: rpm (for update-alternatives)

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 2.4.26-1sls
- 2.4.26
- remove Requires on update-alternatives since it's included in rpm
- require chkconfig package rather than file
- sync with cooker 2.4.26-xmdk:
  - P103: agpgart alias like agpgart 2.6 (nplanel)
  - configure is of 2.5 style, use correct percent-configure macro (gc)

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 2.4.25-4sls
- minor spec cleanups
- remove %%prefix

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.4.25-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
