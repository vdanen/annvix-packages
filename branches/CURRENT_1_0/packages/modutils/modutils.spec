%define name	modutils
%define version 2.4.26
%define release 2sls

%define url ftp://ftp.kernel.org:/pub/linux/utils/kernel/modutils/v2.4
%define priority 10

%define toalternate insmod lsmod modprobe rmmod depmod modinfo

Summary:	The kernel daemon (kerneld) and kernel module utilities.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		%{url}
Source0:	%{url}/%{name}-%{version}.tar.bz2
Source1:	modules.conf
Source2:	macros
Patch1:		modutils-2.4.13-systemmap.patch.bz2
Patch2:		modutils-2.4.2-prepost.patch.bz2
Patch3:		modutils-2.4.6-silence.patch.bz2
Patch4:		modutils-2.4.12-ppc3264.patch.bz2
Patch100:	modutils-2.4.22-various-aliases.patch.bz2
Patch101:	modutils-2.4.13-no-scsi_hostadapter-off.patch.bz2
Patch102:	modutils-2.4.22-pre_post_and_usbmouse.patch.bz2
Patch103:	modutils-2.4.26-agpgart-26.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	bison flex zlib-devel gperf glibc-static-devel

Prereq:		chkconfig, rpm
ExclusiveOs:	Linux
Obsoletes:	modules
Provides:	modules

%description
The modutils packages includes the kerneld program for automatic
loading and unloading of modules under 2.2 and 2.4 kernels, as well as
other module management programs.  Examples of loaded and unloaded
modules are device drivers and filesystems, as well as some other
things.

%prep
%setup -q
%patch1 -p1 -b .systemmap
%patch2 -p1 -b .prepost
%patch3 -p1 -b .silence
%patch4 -p1 -b .ppc3264

%patch100 -p1 -b .various-aliases
%patch101 -p1 -b .scsi-off
%patch102 -p1 -b .ppost_and_usbmouse
%patch103 -p1 -b .agpgart-26

%build
%serverbuild
%configure2_5x --disable-compat-2-0 --disable-kerneld --enable-insmod-static \
		--exec_prefix=/ --enable-zlib --disable-combined --enable-combined-insmod \
		--enable-combined-rmmod

%make dep all

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/lib/modutils
mkdir -p $RPM_BUILD_ROOT/sbin
%makeinstall sbindir=$RPM_BUILD_ROOT/sbin

pushd $RPM_BUILD_ROOT/sbin && {
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
} && popd

pushd $RPM_BUILD_ROOT/%{_mandir}/man8 && {
for i in %{toalternate};do
	mv -v $i.8 $i-24.8
 	ln -s $i-24.8 $i.old.8
 done
} && popd

FakeAlternatives() {
  for file in ${1+"$@"}; do
    rm -f $file
    touch $file
    chmod 0755 $file
  done
}
for i in %{toalternate};do
	FakeAlternatives $RPM_BUILD_ROOT/sbin/$i
done
for i in %{toalternate};do
	FakeAlternatives $RPM_BUILD_ROOT/%{_mandir}/man8/$i.8
done

# security hole, works poorly anyway
rm -f $RPM_BUILD_ROOT/sbin/request-route
%ifarch %{ix86}
rm -f $RPM_BUILD_ROOT/sbin/*.static
%endif

install -D -m 644 %{SOURCE1} %buildroot/etc/modules.conf
install -D -m 644 %{SOURCE2} %buildroot/lib/modutils/macros

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

# get rid of the old installations on upgrade
if [ -x /etc/rc.d/init.d/kerneld ] ; then
    /sbin/chkconfig --del kerneld
fi

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
%doc COPYING README CREDITS TODO 
%doc ChangeLog NEWS example/kallsyms.c include/kallsyms.h
%config(noreplace) /etc/modules.conf
%dir /lib/modutils
%config(noreplace) /lib/modutils/macros


%ghost /sbin/lsmod
%ghost /sbin/insmod
%ghost /sbin/modprobe
%ghost /sbin/rmmod
%ghost /sbin/depmod
%ghost /sbin/modinfo

%ghost %{_mandir}/man8/depmod.8*
%ghost %{_mandir}/man8/insmod.8*
%ghost %{_mandir}/man8/lsmod.8*
%ghost %{_mandir}/man8/modprobe.8*
%ghost %{_mandir}/man8/rmmod.8*
%ghost %{_mandir}/man8/modinfo.8*

/sbin/insmod_ksymoops_clean
/sbin/genksyms
/sbin/kallsyms
/sbin/kernelversion
/sbin/ksyms
/sbin/*old
/sbin/*24
%ifnarch %{ix86}
/sbin/insmod.static
/sbin/rmmod.static
%endif

%{_mandir}/*/*24*
%{_mandir}/*/*old*
%{_mandir}/man1/*
%{_mandir}/man2/*
%{_mandir}/man5/*
%{_mandir}/man8/genksyms.8*
%{_mandir}/man8/kallsyms.8*
%{_mandir}/man8/ksyms.8*

%changelog
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

* Fri Aug 29 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.25-2mdk
- /lib/modutils dir belongs to this package.

* Wed Jul 30 2003 Juan Quintela <quintela@mandrakesoft.com> 2.4.25-1mdk
- 2.4.25.

* Wed Jul 16 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.22-9mdk
- from Andrey Borzenkov <arvidjaar@mail.ru> :
  o Really use alternates
  o files may be symlinks; fix links in this case
  o %ghost is needed to make update from pre-alternatives possible
  o add modinfo to %ghost
  o remove target before running alternatives. This is needed when updating
    from pre-alternatives version.

* Thu Mar 27 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.22-9mdk
- Alternate modinfo also.

* Wed Mar  5 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.22-8mdk
- Make the above usbmouse hid do it as pre_post usbmouse modprobe hid.
- Add pre_post table to get pre_post static configuration.

* Wed Jan 15 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.4.22-7mdk
- need to retain insmod.static on other arches

* Wed Jan 15 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.22-6mdk
- Regenerate modutils from his own package and stop the mess.


# end of file
