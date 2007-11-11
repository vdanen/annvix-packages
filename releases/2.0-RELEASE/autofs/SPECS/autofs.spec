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
Patch23:	autofs-5.0.2-ldap-schema-discovery-config-update.aptch
Patch24:	autofs-5.0.2-ldap-search-basedn-list.patch
Patch25:	autofs-5.0.2-set-default-browse-mode.patch
Patch26:	autofs-5.0.2-separate-config-files.patch
Patch27:	autofs-5.0.2-rename-configuration-file.patch
Patch28:	autofs-5.0.1-rc3-comment-default-master-map.patch
Patch29:	automount-5.0.2-avx-stderr.patch

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openldap-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	libsasl-devel
BuildRequires:	krb5-devel

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


%build
autoconf
%serverbuild
%configure2_5x \
    --with-mapdir=%{_sysconfdir}/%{name} \
    --with-confdir=%{_sysconfdir}/%{name} \
    --with-sasl=yes

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
install -m 0740 %{_sourcedir}/autofs-log.run %{buildroot}%{_srvdir}/autofs/log/run
>%{buildroot}%{_srvdir}/autofs/env/OPTIONS


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
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
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/autofs/log/run
%attr(0640,root,admin) %{_srvdir}/autofs/env/OPTIONS


%files doc
%defattr(-,root,root)
%doc INSTALL CHANGELOG CREDITS README* examples


%changelog
* Sat Nov 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- backport to 2.0-RELEASE (from 2.1-CURRENT)
- fix build dependencies for 2.0-RELEASE

* Sat Nov 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.0.2
- first Annvix package (taken from Mandriva cooker)
- P29: log to stderr and uncomment -f in --help

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
