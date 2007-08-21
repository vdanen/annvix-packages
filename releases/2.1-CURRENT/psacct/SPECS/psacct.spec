#
# spec file for package psacct
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		psacct
%define version		6.4
%define release		%_revrel

Summary:	Utilities for monitoring process activities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://savannah.gnu.org/projects/acct/
Source:		http://www.physik3.uni-rostock.de/tim/kernel/utils/acct/acct-%{version}-pre1.tar.gz
Source1:	psacct.logrotate
Source2:	psacct-avx.init
Patch0:		psacct-6.3.2-mdv-info.patch
Patch1:		psacct-6.3.2-mdv-biarch-utmp.patch

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

# lesspipe.sh requires file
Requires(post):	info-install
Requires(post):	rpm-helper
Requires(preun): info-install
Requires(preun): rpm-helper

%description
The psacct package contains several utilities for monitoring process
activities, including ac, lastcomm, accton and sa.  The ac command
displays statistics about how long users have been logged on.  The
lastcomm command displays information about previous executed commands.
The accton command turns process accounting on or off.  The sa command
summarizes information about previously executed commmands.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n acct-%{version}-pre1
%patch0 -p1 -b .infoentry
%patch1 -p1 -b .biarch-utmp


%build
%serverbuild

%configure2_5x

perl -p -i -e "s@/var/account@/var/log@g" files.h configure

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{sbin,var/log}

%makeinstall

mv %{buildroot}%{_sbindir}/accton %{buildroot}/sbin/accton
ln -s ../../sbin/accton %{buildroot}%{_sbindir}/accton

# psacct's last conflicts with last from SysVinit
rm -f %{buildroot}%{_bindir}/last
rm -f %{buildroot}%{_mandir}/man1/last.1

touch %{buildroot}/var/log/pacct %{buildroot}/var/log/usracct %{buildroot}/var/log/savacct

install -D -m 0640 %{_sourcedir}/psacct.logrotate %{buildroot}/etc/logrotate.d/psacct
install -D -m 0750 %{_sourcedir}/psacct-avx.init %{buildroot}/%{_initrddir}/psacct


%post
# Create initial log files so that logrotate doesn't complain
if [ $1 = 1 ]; then
    %create_ghostfile /var/log/usracct root admin 640
    %create_ghostfile /var/log/savacct root admin 640
    %create_ghostfile /var/log/pacct root admin 640
fi

%_install_info accounting.info
%_post_service %{name}


%preun
%_remove_install_info accounting.info
%_preun_service %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/accton
%{_sbindir}/accton
%{_sbindir}/dump-acct
%{_sbindir}/dump-utmp
%{_sbindir}/sa
%{_bindir}/ac
%{_bindir}/lastcomm
%{_mandir}/man1/ac.1*
%{_mandir}/man1/lastcomm.1*
%{_mandir}/man8/accton.8*
%{_mandir}/man8/sa.8*
%{_infodir}/accounting.info*
%config(noreplace) %{_sysconfdir}/logrotate.d/psacct
%{_initrddir}/psacct
%ghost /var/log/pacct
%ghost /var/log/usracct
%ghost /var/log/savacct


%files doc
%defattr(-,root,root)
%doc README NEWS INSTALL AUTHORS ChangeLog COPYING


%changelog
* Mon Aug 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.4-pre1
- first Annvix build
- this is really 6.4-pre1 but since pre1 is already over 7mos old, for the
  sake of simplicty we'll just call it 6.4
- drop the last command from this package as a) it has a buffer overflow so dumps
  core anyways and b) last from SysVinit is sufficient

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
