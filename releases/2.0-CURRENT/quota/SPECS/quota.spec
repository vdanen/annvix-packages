#
# spec file for package quota
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		quota
%define version 	3.13
%define release 	%_revrel

Summary:	System administration tools for monitoring users' disk usage
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Configuration
URL:		http://sourceforge.net/projects/linuxquota
Source:		http://prdownloads.sourceforge.net/linuxquota/%{name}-%{version}.tar.bz2
Patch0:		quota-tools-man-pages-path.patch
Patch1:		quota-tools-no-stripping.patch
Patch2:		quota-3.06-warnquota.patch
Patch3:		quota-tools-default-conf.patch
Patch4:		quota-3.06-pie.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libext2fs-devel
BuildRequires:	gettext
BuildRequires:	tcp_wrappers-devel >= 7.6-29avx

Requires:	kernel >= 2.4
Requires:	initscripts >= 6.38

%description
The quota package contains system administration tools for monitoring
and limiting users' and or groups' disk usage, per filesystem.


%prep
%setup -q -n quota-tools
%patch0 -p1 -b .man-pages
%patch1 -p1 -b .no-stripping
%patch2 -p1 -b .warnquota
%patch3 -p1 -b .default-conf
%ifnarch ppc ppc64 x86_64
%patch4 -p1 -b .pie
%endif


%build
%configure \
    --with-ext2direct=no \
    --enable-rootsbin
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{/sbin,%{_sysconfdir},%{_sbindir},%{_bindir},%{_mandir}/{man1,man2,man3,man8}}

make install ROOTDIR=%{buildroot}

install -m 0644 warnquota.conf %{buildroot}%{_sysconfdir}

%kill_lang %{name}
%find_lang %{name}

# can't strip suid files
chmod 0755 %{buildroot}/sbin/*
chmod 0755 %{buildroot}%{_sbindir}/*
chmod 0755 %{buildroot}%{_bindir}/*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/warnquota.conf
%config(noreplace) %{_sysconfdir}/quotagrpadmins
%config(noreplace) %{_sysconfdir}/quotatab
%attr(0755,root,root) /sbin/*
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%{_includedir}/rpcsvc/*
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man2/*
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_mandir}/man8/*


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.13
- use %%kill_lang

* Mon Aug 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.13
- rebuild against new e2fsprogs
- spec cleanups
- remove locale files
- fix buildrequires

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.13
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.13
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.13
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.13
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.13-1avx
- 3.13
- sync patch with Mandriva (who synced with Fedora)
- rebuild against new libext2fs-devel
- BuildRequires: tcp_wrappers-devel >= 7.6-29avx
- don't apply the pie patch on x86_64 as we get a text relocation error

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.09-5avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.09-4avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.09-3avx
- Annvix build

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 3.09-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
