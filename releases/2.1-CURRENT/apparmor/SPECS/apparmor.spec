#
# spec file for package apparmor
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apparmor
%define version		2.1
%define release		%_revrel

%define svnrel		961

%define major		1
%define libname		%mklibname apparmor %{major}
%define devname		%mklibname apparmor -d

%define aa_profilesdir	%{_sysconfdir}/apparmor/profiles

Summary:	AppArmor security framework
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-%{svnrel}.tar.gz
Source1:	01_mod_apparmor.conf
Source2:	apparmor-avx.init
Patch0:		apparmor-2.1-961-mdv-ldflags.patch
Patch1:		apparmor-parser-2.0.2-avx-fixes.patch
Patch2:		apparmor-2.1-961-avx-socklog.patch
Patch3:		apparmor-utils-2.0-avx-nofork.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	flex >= 2.5.33
#BuildRequires:	latex2html
BuildRequires:	bison
BuildRequires:	perl-devel
BuildRequires:	pam-devel
BuildRequires:	httpd-devel
BuildRequires:	swig
BuildRequires:	audit-devel
BuildRequires:	pkgconfig
BuildRequires:	libpcap-devel

# the main package is a virtual requires to pull in all the components
Requires:	apparmor-parser
Requires:	apparmor-utils
Requires:	apparmor-profiles
Requires:	%{libname}

%description
AppArmor is a security framework that proactively protects the operating system
and applications from external or internal threats, even zero-day attacks, by
enforcing good program behavior and preventing even unknown software flaws from
being exploited. AppArmor security profiles completely define what system
resources individual programs can access, and with what privileges.


%package -n %{libname}
Summary:	Main libraries for %{name}
Group:		System/Libraries
License:        LGPL
Provides:	lib%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the AppArmor library.


%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname apparmor 1 -d}

%description -n %{devname}
This package contains development files for %{name}.


%package -n perl-libapparmor
Summary:        AppArmor module for perl
Group:          Development/Perl
Requires:       %{libname} = %{version}

%description -n perl-libapparmor
This package contains the AppArmor module for perl.


%package profiles
Summary:        Base AppArmors profiles
License:        GPL
Group:          System/Base
Requires:       apparmor-parser
Requires(post): apparmor-parser

%description profiles
Base AppArmor profiles (aka security policy).


%package parser
Summary:        AppArmor userlevel parser utility
License:        GPL
Group:          System/Base
Requires(preun): rpm-helper
Requires(post): rpm-helper

%description parser
AppArmor Parser is a userlevel program that is used to load in program
profiles to the AppArmor Security kernel module.


%package -n pam_apparmor
Summary:        PAM module for AppArmor
License:        GPL
Group:          System/Libraries

%description -n pam_apparmor
The pam_apparmor module provides the means for any pam applications that call
pam_open_session() to automatically perform an AppArmor change_hat operation in
order to switch to a user-specific security policy.


%package utils
Summary:        AppArmor userlevel utilities
License:        GPL
Group:          System/Base
Requires:	perl-libapparmor
Requires:	perl(RPC::XML)
Requires:	perl(Term::ReadKey)

%description utils
This package contains programs to help create and manage AppArmor profiles.


%package -n httpd-mod_apparmor
Summary:        Fine-grained AppArmor confinement for apache
License:        LGPL
Group:          System/Servers

%description -n httpd-mod_apparmor
apache-mod_apparmor adds support to apache to provide AppArmor confinement
to individual cgi scripts handled by apache modules like mod_php and mod_perl.
This package is part of a suite of tools that used to be named SubDomain.


%prep
%setup -q -n %{name}-%{version}-%{svnrel}
pushd changehat/pam_apparmor
%patch0 -p0 -b .ldflags
popd
pushd parser
%patch1 -p0 -b .avx
popd
pushd utils
%patch2 -p0 -b .avx-socklog
%patch3 -p0 -b .avx-nofork
popd


%build
%serverbuild

# library
pushd changehat/libapparmor
    ./autogen.sh
    %configure --with-perl
    %make CFLAGS="%{optflags}" TESTBUILDDIR=$(pwd)
    cd src
    # so including <sys/apparmor.h> in the next builds works
    ln -s . sys
    # same for <aalogparse/aalogparse.h>
    ln -s . aalogparse
popd

# parser
pushd parser
    cp %{_sourcedir}/apparmor-avx.init rc.apparmor.annvix
    %make CFLAGS="%{optflags}" TESTBUILDDIR=$(pwd)
popd

# pam
pushd changehat/pam_apparmor
    %make \
        LDFLAGS="-L../libapparmor/src/.libs" \
        TESTBUILDDIR=$(pwd) \
        CFLAGS="%{optflags} -I../libapparmor/src"
popd

# utils
pushd utils
    %make TESTBUILDDIR=$(pwd) CFLAGS="%{optflags}"
popd

# mod_apparmor
pushd changehat/mod_apparmor
    %make \
        LIBAPPARMOR_FLAGS="-L../libapparmor/src/.libs -lapparmor -I../libapparmor/src" \
        TESTBUILDDIR=$(pwd)
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# lib
pushd changehat/libapparmor
    %makeinstall_std LIB=%{_lib} LIBDIR=%{_libdir}
    mkdir -p %{buildroot}%{perl_vendorarch}
    # XXX - for some reason, on i586 builds this file is not copied
    install -m 0644 swig/perl/LibAppArmor.pm %{buildroot}%{perl_vendorarch}
    # fix some perms
    find %{buildroot} -type f -exec chmod 0644 {} \;
popd

# parser
pushd parser
    %makeinstall_std DISTRO=annvix APPARMOR_BIN_PREFIX=%{buildroot}%{_initrddir}  TESTBUILDDIR=$(pwd)
    mv %{buildroot}%{_initrddir}/rc.apparmor.functions %{buildroot}%{_initrddir}/apparmor.functions
popd

# profiles
pushd profiles
    %makeinstall_std EXTRASDIR=%{buildroot}%{aa_profilesdir}/extras
popd

# pam
pushd changehat/pam_apparmor
    %makeinstall_std SECDIR=%{buildroot}/%{_lib}/security
popd

# utils
pushd utils
    %makeinstall_std PERLDIR=%{buildroot}%{perl_vendorlib}/Immunix
popd

# mod_apparmor
pushd changehat/mod_apparmor
    %makeinstall_std APXS_INSTALL_DIR=%{_libdir}/httpd-extramodules
    mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
    install -m 0644 %{_sourcedir}/01_mod_apparmor.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/
popd

# remove profiles shipped elsewhere
rm -f %{buildroot}%{_profiledir}/{bin,sbin,usr.sbin,usr.bin}.*

%kill_lang %{name}-parser
%find_lang %{name}-parser


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post parser
%_post_service apparmor
#%_post_service aaeventd


%preun parser
%_preun_service apparmor
#%_preun_service aaeventd


%posttrans profiles
%_aa_reload


%files
%defattr(-,root,root)

%files -n %{libname}
%defattr(-,root,root)
%doc changehat/libapparmor/COPYING.LGPL
%attr(0755,root,root) /%{_libdir}/*.so.*

%files -n perl-libapparmor
%defattr(-,root,root)
%{perl_vendorarch}/auto/LibAppArmor
%{perl_vendorarch}/LibAppArmor.pm

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/aalogparse/
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_includedir}/sys/*.h
%attr(0644,root,root) %{_mandir}/man2/aa_change_hat.2*

%files profiles
%defattr(-,root,root)
%dir %{_sysconfdir}/apparmor.d
%dir %{_sysconfdir}/apparmor.d/abstractions
%dir %{_sysconfdir}/apparmor.d/program-chunks
%dir %{_sysconfdir}/apparmor.d/tunables
%config(noreplace) %{_sysconfdir}/apparmor.d/abstractions/*
%config(noreplace) %{_sysconfdir}/apparmor.d/program-chunks/*
%config(noreplace) %{_sysconfdir}/apparmor.d/tunables/*
%dir %{_sysconfdir}/apparmor
%dir %{aa_profilesdir}
%dir %{aa_profilesdir}/extras
%{aa_profilesdir}/extras/README
%config(noreplace) %{aa_profilesdir}/extras/usr.*
%config(noreplace) %{aa_profilesdir}/extras/etc.*
%config(noreplace) %{aa_profilesdir}/extras/sbin.*
%config(noreplace) %{aa_profilesdir}/extras/bin.*

%files parser -f %{name}-parser.lang
%defattr(-,root,root)
%doc parser/COPYING.GPL parser/README
%dir %{_sysconfdir}/apparmor
%config(noreplace) %{_sysconfdir}/apparmor/subdomain.conf
#%{_initrddir}/aaeventd
%{_initrddir}/apparmor
%{_initrddir}/apparmor.functions
/sbin/*
%{_mandir}/man5/apparmor.d.5*
%{_mandir}/man5/apparmor.vim.5*
%{_mandir}/man5/subdomain.conf.5*
%{_mandir}/man7/apparmor.7*
%{_mandir}/man8/apparmor_parser.8*
%{_var}/lib/apparmor

%files -n pam_apparmor
%defattr(-,root,root)
%doc changehat/pam_apparmor/README changehat/pam_apparmor/COPYING
%attr(0755,root,root) /%{_lib}/security/*.so

%files utils
%defattr(-,root,root)
%dir %{_sysconfdir}/apparmor
%config(noreplace) %{_sysconfdir}/apparmor/logprof.conf
%config(noreplace) %{_sysconfdir}/apparmor/severity.db
%{_datadir}/locale/*/*/apparmor-utils.mo
%{_sbindir}/*
%{perl_vendorlib}/Immunix
%{_var}/log/apparmor
%{_mandir}/man5/logprof.conf.5*
%{_mandir}/man8/aa-autodep.8*
%{_mandir}/man8/aa-complain.8*
%{_mandir}/man8/aa-enforce.8*
%{_mandir}/man8/aa-genprof.8*
%{_mandir}/man8/aa-logprof.8*
%{_mandir}/man8/aa-status.8*
%{_mandir}/man8/aa-unconfined.8*
%{_mandir}/man8/apparmor_status.8*
%{_mandir}/man8/autodep.8*
%{_mandir}/man8/complain.8*
%{_mandir}/man8/enforce.8*
%{_mandir}/man8/genprof.8*
%{_mandir}/man8/logprof.8*
%{_mandir}/man8/unconfined.8*
%{_mandir}/man8/aa-audit.8*
%{_mandir}/man8/audit.8*

%files -n httpd-mod_apparmor
%defattr(-,root,root,-)
%doc changehat/mod_apparmor/COPYING.LGPL
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/01_mod_apparmor.conf
%attr(0755,root,root) %{_libdir}/httpd-extramodules/mod_apparmor.so
%attr(0644,root,root) %{_mandir}/man8/mod_apparmor.8*


%changelog
* Thu Dec 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1
- use %%perl_vendorlib to install the Immunix perl modules otherwise
  they are not found on x86_64

* Wed Dec 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1
- rebuild against new audit

* Fri Oct 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1
- add some requires
- (re-)nuke the profiles that we either won't use or will be shipping
  elsewhere

* Fri Oct 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1
- merge all the apparmor specs into one spec now that it is
  shipped in one tarball (thanks to Mandriva for this)
- drop the old apparmor individual packages

* Tue Jun 26 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- updated initscript to return proper errorlevels and add
  condrestart/condreload (thanks, Andreas)

* Wed Jun 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- buildrequires perl-devel

* Tue Jun 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.2
- 2.0.2-662
- rediff P0
- drop P1; fixes merged upstream
- update our initscript to match the new apparmor_ names (rather than
  subdomain_)

* Fri Nov 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- r150 (October snapshot)
- drop P1-P3: applied upstream
- new P1 to fix a single fdopendir() call that requires glibc 2.4

* Wed Nov 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- add buildrequires of flex and bison

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- updated the initscript and modified the patch to the functions accordingly
- add a virtual rpm so you can just "apt-get install apparmor" and get all
  the required components

* Tue Sep 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- fix the preun script

* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- sync some patches with SUSE to match support in SLE10:
  - P1: fix segv if profiles directory does not exist
  - P2: add support for the new m flag (mmap w/ PROT_EXEC permission)
  - P3: add support for the new Px/Ux modes which indicate to ld.so that
    sensitive environment variables should be filtered on exec()

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- remove locales

* Wed Aug 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- don't include the aaeventd initscript (runscript is in apparmor-utils)
- requires rpm-helper

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- fix permissions
- provide our own initscripts for apparmor and aaeventd (S0, S1)
- drop /subdomain (not required since we use /sys/kernel/security)
- update P0 to fix the apparmor.functions

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- put /lib/apparmor/rc.apparmor.functions in /etc/rc.d/init.d/apparmor.functions

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- P0: fix installation of initscripts (location) for Annvix/Mandriva
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
