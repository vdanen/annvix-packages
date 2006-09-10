#
# spec file for package urpmi
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		urpmi
%define version		4.8.22
%define release 	%_revrel

%define compat_perl_vendorlib %(perl -MConfig -e 'print "%{?perl_vendorlib:1}" ? "%{perl_vendorlib}" : "$Config{installvendorlib}"')

%define allow_karun	0

Summary:	Command-line software installation tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://search.cpan.org/dist/%{name}/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	bzip2-devel
BuildRequires:	gettext
BuildRequires:	perl
BuildRequires:	perl(File::Slurp)
BuildRequires:	perl(URPM) >= 1.36
BuildRequires:	perl(MDV::Packdrakeng)
BuildRequires:	perl(Locale::gettext) >= 1.01-15avx
BuildRequires:	perl(Net::LDAP)
BuildArch:	noarch

Requires:	webfetch
Requires:	eject
Requires:	gnupg
Requires:	perl(URPM) >= 1.37
Requires(pre):	perl(Locale::gettext) >= 1.01-15avx
Requires(pre):	rpmtools >= 5.0.2
Requires(pre):	perl(URPM) >= 1.37
Conflicts:	curl < 7.13.0

%description
urpmi takes care of dependencies between rpms, using a pool (or pools)
of rpms.

urpmi is Annvix's console-based software installation tool, developed
by Mandriva. urpmi will follow package dependencies -- in other words,
it will install all the other software required by the software you ask
it to install -- and it's capable of obtaining packages from a variety
of media, including installation CD-ROMs, your local hard disk, and
remote sources such as web or FTP sites.


%if %{allow_karun}
%package -n urpmi-parallel-ka-run
Summary:	Parallel extension to urpmi using ka-run
Group:		%{group}
Requires:	urpmi >= %{version}-%{release}
Requires:	parallel-tools

%description -n urpmi-parallel-ka-run
urpmi-parallel-ka-run is an extension module to urpmi for handling
distributed installation using ka-run or Taktuk tools.
%endif


%package -n urpmi-parallel-ssh
Summary:	Parallel extension to urpmi using ssh and scp
Group:		%{group}
Requires:	urpmi >= %{version}-%{release}
Requires:	openssh-clients
Requires:	perl

%description -n urpmi-parallel-ssh
urpmi-parallel-ssh is an extension module to urpmi for handling
distributed installation using ssh and scp tools.


%package -n urpmi-ldap
Summary:	Extension to urpmi to specify media configuration via LDAP
Group:		%{group}
Requires:	urpmi >= %{version}-%{release}
Requires:	openldap-clients

%description -n urpmi-ldap
urpmi-ldap is an extension module to urpmi to allow to specify
urpmi configuration (notably media) in an LDAP directory.


%package -n urpmi-recover
Summary:	A tool to manage rpm repackaging and rollback
Group:		%{group}
Requires:	urpmi >= %{version}-%{release}
Requires:	perl
Requires:	perl-DateManip

%description -n urpmi-recover
urpmi-recover is a tool that enables to set up a policy to keep trace of all
packages that are uninstalled or upgraded on an rpm-based system, and to
perform rollbacks, that is, to revert the system back to a previous state.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
perl Makefile.PL INSTALLDIRS=vendor \
    --install-po
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

# rpm-find-leaves is invoked by this name in rpmdrake
pushd %{buildroot}%{_bindir}
    ln -s -f rpm-find-leaves urpmi_rpm-find-leaves
popd

# Don't install READMEs twice
rm -f %{buildroot}%{compat_perl_vendorlib}/urpm/README*

# For ghost file
mkdir -p %{buildroot}%{_sys_macros_dir}
touch %{buildroot}%{_sys_macros_dir}/urpmi.recover.macros


%if ! %{allow_karun}
rm -f %{buildroot}%{compat_perl_vendorlib}/urpm/parallel_ka_run.pm
%endif

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%preun
if [ "$1" = "0" ]; then
    cd /var/lib/urpmi
    rm -f compss provides depslist* descriptions.* *.cache hdlist.* synthesis.hdlist.* list.*
    cd /var/cache/urpmi
    rm -rf partial/* headers/* rpms/*
fi
exit 0

%post -p /usr/bin/perl
use urpm;
if (-e "/etc/urpmi/urpmi.cfg") {
    $urpm = new urpm;
    $urpm->read_config;
    $urpm->update_media(nolock => 1, nopubkey => 1);
}


%files -f %{name}.lang
%defattr(-,root,root)
%dir %{_sysconfdir}/urpmi
%dir /var/lib/urpmi
%dir /var/cache/urpmi
%dir /var/cache/urpmi/partial
%dir /var/cache/urpmi/headers
%dir /var/cache/urpmi/rpms
%config(noreplace) %{_sysconfdir}/urpmi/skip.list
%config(noreplace) %{_sysconfdir}/urpmi/inst.list
%{_bindir}/rpm-find-leaves
%{_bindir}/urpmi_rpm-find-leaves
%{_bindir}/urpmf
%{_bindir}/urpmq
%{_sbindir}/urpmi
%{_sbindir}/rurpmi
%{_sbindir}/urpme
%{_sbindir}/rurpme
%{_sbindir}/urpmi.addmedia
%{_sbindir}/urpmi.removemedia
%{_sbindir}/urpmi.update
%{_mandir}/man3/urpm*
%{_mandir}/man5/urpm*
%{_mandir}/man5/proxy*
%{_mandir}/man8/rurpm*
%{_mandir}/man8/urpme*
%{_mandir}/man8/urpmf*
%{_mandir}/man8/urpmq*
%{_mandir}/man8/urpmi.8*
%{_mandir}/man8/urpmi.addmedia*
%{_mandir}/man8/urpmi.removemedia*
%{_mandir}/man8/urpmi.update*
%{compat_perl_vendorlib}/urpm.pm
%dir %{compat_perl_vendorlib}/urpm 
%{compat_perl_vendorlib}/urpm/args.pm
%{compat_perl_vendorlib}/urpm/cfg.pm
%{compat_perl_vendorlib}/urpm/download.pm
%{compat_perl_vendorlib}/urpm/msg.pm
%{compat_perl_vendorlib}/urpm/sys.pm
%{compat_perl_vendorlib}/urpm/util.pm
%{compat_perl_vendorlib}/urpm/prompt.pm

%if %{allow_karun}
%files -n urpmi-parallel-ka-run
%defattr(-,root,root)
%{compat_perl_vendorlib}/urpm/parallel_ka_run.pm
%endif

%files -n urpmi-parallel-ssh
%defattr(-,root,root)
%{compat_perl_vendorlib}/urpm/parallel_ssh.pm

%files -n urpmi-ldap
%{compat_perl_vendorlib}/urpm/ldap.pm

%files -n urpmi-recover
%{_sbindir}/urpmi.recover
%{_mandir}/man8/urpmi.recover*
%config(noreplace) %{_sys_macros_dir}/urpmi.recover.macros
%ghost %{_sys_macros_dir}/urpmi.recover.macros

%files doc
%defattr(-,root,root)
%doc ChangeLog urpmi.schema urpm/README.ssh
%if %{allow_karun}
%doc urpm/README.ka-run
%endif


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8.22
- remove locales

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8.22
- 4.8.22
- remove pre-Annvix changelog

* Tue May 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8.19
- fix requires typeo

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8.19
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Tue May 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8.19
- fix typeo on buildreq

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8.19
- fix group

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.8.19
- 4.8.19
- add the urpmi-recover package
- remove the "fur" locale

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.7.16
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.7.16
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Oct 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.7.16-1avx
- 4.7.16

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.7.15-1avx
- 4.7.15

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.7.14-1avx
- 4.7.14
- new: rurpmi, an experimental restricted version of urpmi (intended to
  be used via sudoers)
- new: ability to use ldap to configure repositories
- new: support for rpm 4.4.1

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.23-5avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.23-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.23-3avx
- bootstrap build

* Mon Mar 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.23-2avx
- sync with 4.6.23-5mdk

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.23-1avx
- 4.6.23

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.20-1avx
- 4.6.20
- requires perl-URPM 1.08
- conflicts curl < 7.13.0

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.6.14-1avx
- 4.6.14
- update description
- PreReq: perl-URPM >= 1.04, rpmtools >= 5.0.2

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.5-1avx
- 4.5
- Requires: perl (on urpmi-parallel-ssh)
- remove gurpmi completely
- remove bash_completion stuff
- kernel stuff doesn't need to be in inst.lst anymore

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.4-50avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.4-49sls
- remove %%build_opensls macro
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 4.4-48sls
- new macro: %%allow_karun which is off for OpenSLS builds
- fix %%allow_gurpmi macro
- don't build gurpmi

* Fri Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.4-47sls
- OpenSLS build
- tidy spec
- do a lot of %%define forces using %%build_opensls macro
- remove Distribution tag
- don't use %%real_release

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
