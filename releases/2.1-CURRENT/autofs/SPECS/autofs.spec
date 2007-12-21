#
# spec file for package autofs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		autofs
%define version		5.0.2
%define release		%_revrel

Summary: 	A tool for automatically mounting and unmounting filesystems
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		ftp://ftp.kernel.org/pub/linux/daemons/autofs
Source0:	ftp://ftp.kernel.org/pub/linux/daemons/autofs/v5/autofs-%{version}.tar.bz2
Source1:	ftp://ftp.kernel.org/pub/linux/daemons/autofs/v5/autofs-%{version}.tar.bz2.sign
Source2:	autofs.run
Source3:	autofs-log.run
Source4:	autofs.finish
Patch0:		autofs-5.0.2-add-krb5-include.patch
Patch1:		autofs-5.0.2-bad-proto-init.patch
Patch2:		autofs-5.0.2-add-missing-multi-support.patch
Patch3:		autofs-5.0.2-add-multi-nsswitch-lookup.patch
Patch4:		autofs-5.0.2-consistent-random-selection-option-name.patch
Patch5:		autofs-5.0.2-fix-offset-dir-create.patch
Patch6:		autofs-5.0.2-quote-exports.patch
Patch7:		autofs-5.0.2-hi-res-time.patch
Patch8:		autofs-5.0.2-quoted-slash-alone.patch
Patch9:		autofs-5.0.2-fix-dnattr-parse.patch
Patch10:	autofs-5.0.2-fix-nfs-version-in-get-supported-ver-and-cost.patch
Patch11:	autofs-5.0.2-instance-stale-mark.patch
Patch12:	autofs-5.0.2-fix-largefile-dumbness.patch
Patch13:	autofs-5.0.2-dont-fail-on-empty-master.patch
Patch14:	autofs-5.0.2-ldap-percent-hack.patch
Patch15:	autofs-5.0.2-fix-mount-nfs-nosymlink.patch
Patch16:	autofs-5.0.2-dont-fail-on-empty-master-fix.patch
Patch17:	autofs-5.0.2-default-nsswitch.patch
Patch18:	autofs-5.0.2-add-ldap-schema-discovery.patch
Patch19:	autofs-5.0.2-random-selection-fix.patch
Patch20:	autofs-5.0.2-timeout-option-parse-fix.patch
Patch21:	autofs-5.0.2-ldap-check-star.patch
Patch22:	autofs-5.0.2-add-ldap-schema-discovery-fix.patch
Patch23:	autofs-5.0.2-ldap-schema-discovery-config-update.patch
Patch24:	autofs-5.0.2-ldap-search-basedn-list.patch
Patch25:	autofs-5.0.2-libxml2-workaround.patch
Patch26:	autofs-5.0.2-reread-config-on-hup.patch
Patch27:	autofs-5.0.2-add-multiple-server-selection-option.patch
Patch28:	autofs-5.0.2-foreground-logging.patch
Patch29:	autofs-5.0.2-cleanup-krb5-comment.patch
Patch30:	autofs-5.0.2-submount-deadlock.patch
Patch31:	autofs-5.0.2-add-ferror-check.patch
Patch32:	autofs-5.0.2-autofs-5-typo.patch
Patch33:	autofs-5.0.2-swallow-null-macro.patch
Patch34:	autofs-5.0.2-remove-unsed-export-validation-code.patch
Patch35:	autofs-5.0.2-dynamic-logging.patch
Patch36:	autofs-5.0.2-fix-recursive-loopback-mounts.patch
Patch37:	autofs-5.0.2-log-map-reload.patch
Patch38:	autofs-5.0.2-basedn-with-spaces.patch
Patch39:	autofs-5.0.2-dynamic-logging-fixes.patch
Patch40:	autofs-5.0.2-basedn-with-spaces-fix.patch
Patch41:	autofs-5.0.2-check-mtab-updated.patch
Patch42:	autofs-5.0.2-basedn-with-spaces-fix-2.patch
Patch43:	autofs-5.0.2-master-check-underscore.patch
Patch44:	autofs-5.0.2-add-ldap-schema-discovery-fix-2.patch
Patch45:	autofs-5.0.2-hosts-nosuid-default.patch
Patch46:	autofs-5.0.2-hosts-nodev-default.patch
Patch100:	autofs-5.0.2-mdv-rename-configuration-file.patch
Patch101:	autofs-5.0.2-mdv-separate-config-files.patch
Patch102:	autofs-5.0.2-avx-config_fixes.patch

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openldap-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	krb5-devel
BuildRequires:	xml-devel
# this is only needed if --with-sasl=yes
#BuildRequires:	cyrus-sasl-devel

Requires:	nfs-utils-clients
Requires:	portmap
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
autofs is a daemon which automatically mounts filesystems when you use
them, and unmounts them later when you are not using them.  This can
include network filesystems, CD-ROMs, floppies, and so forth.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1

%patch100 -p1
%patch101 -p1
%patch102 -p1

%build
autoconf
%serverbuild
%configure2_5x \
    --with-mapdir=%{_sysconfdir}/%{name} \
    --with-confdir=%{_sysconfdir}/%{name} \
    --with-sasl=no

%make

mkdir examples
cp samples/ldap* examples
cp samples/autofs.schema examples


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
#mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}/autofs
mkdir -p %{buildroot}%{_mandir}/{man5,man8}
mkdir -p %{buildroot}%{_sysconfdir}

%make INSTALLROOT=%{buildroot} install 

rm -f %{buildroot}%{_sysconfdir}/init.d/%{name}
rm -f %{buildroot}%{_mandir}/man8/autofs*

mkdir -p %{buildroot}%{_srvdir}/autofs/{log,peers,env}
install -m 0740 %{_sourcedir}/autofs.run %{buildroot}%{_srvdir}/autofs/run
install -m 0740 %{_sourcedir}/autofs.finish %{buildroot}%{_srvdir}/autofs/finish
install -m 0740 %{_sourcedir}/autofs-log.run %{buildroot}%{_srvdir}/autofs/log/run
>%{buildroot}%{_srvdir}/autofs/env/OPTIONS


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ "`grep -q autofs4 %{_sysconfdir}/modprobe.preload; echo $?`" == "1" ]; then
    echo "autofs4" >>%{_sysconfdir}/modprobe.preload
fi
%_post_srv autofs


%preun
%_preun_srv autofs


%files
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/autofs
%config(noreplace) %{_sysconfdir}/sysconfig/autofs
%{_libdir}/%{name}
%{_sbindir}/automount
%{_mandir}/*/*
%dir %attr(0750,root,admin) %{_srvdir}/autofs
%dir %attr(0750,root,admin) %{_srvdir}/autofs/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/autofs/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/autofs/finish
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/autofs/log/run
%attr(0640,root,admin) %{_srvdir}/autofs/env/OPTIONS


%files doc
%defattr(-,root,root)
%doc INSTALL CHANGELOG CREDITS README* examples


%changelog
* Fri Dec 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- P46: make the hosts mak mount nodev by default too (CVE-2007-6285)

* Mon Dec 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- add autofs4 module to /etc/modprobe.preload if it's not already there
  so that autofs can run "out of the box"

* Sat Dec 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- rebuild against new krb5

* Thu Dec 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- P45: make the hosts map mount nosuid by default (CVE-2007-5964)
- rediff P102

* Sat Nov 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- buildrequires xml-devel
- disable sasl support as it breaks the ldap module and is non-functional anyways
- include all of the upstream patches and apply them in the upstream-
  suggested order
- drop our stderr patch; it got fixed (somewhere) in one of the new patches
- drop some Mandriva patches
- drop the initscript
- add a finish script to killall -9 automount since it seems to be quite stubborn
- P102: patch the config file have it only automount /net

* Sat Nov 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- first Annvix package (taken from Mandriva cooker)
- P29: log to stderr and uncomment -f in --help

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
