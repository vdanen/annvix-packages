%define name	lsb
%define version	1.3
%define release	8sls

%{!?build_opensls:%global build_opensls 0}

Summary:	The skeleton package defining packages needed for LSB compliance.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://www.linuxbase.org
Source1:	lsb-init-functions

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildArch:	noarch

PreReq:		rpm-helper
Provides:	lsb = %{version}
Requires:	pax lsb-release make smtpdaemon ed glibc_lsb
Requires:	XFree86-devel expect lpddaemon perl-DBI glibc-i18ndata
Requires:	vim-enhanced diffutils file gettext chkconfig
Requires:	mtools csh
%if !%{build_opensls}
Requires:	/etc/sgml
%endif

%description
The skeleton package defining packages needed for LSB compliance.
Also contains some directories LSB tests look for that aren't 
owned by other OpenSLS packages, and scripts to re-create the old
/sbin/fasthalt and /sbin/fastboot.
 
Currently, to be able to run the LSB binary test suit successfully, you 
need to boot with devfs=nomount, as well as insure that the partitions 
containing /tmp and /home are mounted with the option 'atime', rather 
than 'noatime'.

You should also note that using the fstab option 'acl' for Posix ACLs 
will generate 1 test failure.  This is not enabled by default on OpenSLS.

 
%install
install -d $RPM_BUILD_ROOT/usr/share/nls
install -d $RPM_BUILD_ROOT/usr/share/tmac
install -d $RPM_BUILD_ROOT/var/cache/fonts
install -d $RPM_BUILD_ROOT/var/games
install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT/lib/%{name}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/lib/%{name}/init-functions

ln -snf /sbin/chkconfig $RPM_BUILD_ROOT%{_libdir}/lsb/install_initd
ln -snf /sbin/chkconfig $RPM_BUILD_ROOT%{_libdir}/lsb/remove_initd

cat << EOF > $RPM_BUILD_ROOT/sbin/fasthalt
#!/bin/sh
#start fasthalt
/sbin/halt -f
#end fasthalt
EOF

cat << EOF > $RPM_BUILD_ROOT/sbin/fastboot
#!/bin/sh
#start fastboot
/sbin/reboot -f
#end fastboot
EOF

cat << EOF > $RPM_BUILD_ROOT/etc/hosts.equiv
# Sample hosts.equiv file for LSB compliance
# see man hosts.equiv for usage.
EOF

cat << EOF > $RPM_BUILD_ROOT/etc/hosts.lpd
#
# hosts.lpd     This file describes the names of the hosts which are
#               allowed to use the remote printer services of this
#               host.  This file is used by the LPD subsystem.
#		Added to Mandrake Linux for LSB compiance.
EOF

cat << EOF > $RPM_BUILD_ROOT/etc/networks
# Sample networks file for LSB compliance. Database of network 
# names and addresses, used by programs such as route.
# format: networkname networkaddress
EOF

cat << EOF > $RPM_BUILD_ROOT/etc/gateways
# sample gateways file for LSB compliance. Database of gateways
# used by routed. Sample format shown below.
# [ net | host ] name1 gateway name2 metric value [ passive | active | external ]
EOF

chmod 0755 $RPM_BUILD_ROOT/sbin/fastboot
chmod 0755 $RPM_BUILD_ROOT/sbin/fasthalt
chmod 0644 $RPM_BUILD_ROOT/etc/hosts.equiv
chmod 0644 $RPM_BUILD_ROOT/etc/hosts.lpd
chmod 0644 $RPM_BUILD_ROOT/etc/networks
chmod 0644 $RPM_BUILD_ROOT/etc/gateways

# (sb) concession for lsb-apache to run
%pre
%_pre_groupadd nobody

%post

echo "To run the LSB binary test suite, download the latest version from"
echo "ftp://ftp.freestandards.org/pub/lsb/test_suites/released/binary/runtime/"
echo "and install the rpm. You need to create a password for user vsx0."  
echo "Log in as user vsx0 and use the command 'run_tests'."
echo ""
echo "Note: Currently you must boot with devfs=nomount to be able to"
echo "      successfully run the LSB binary test suite."
echo ""
echo "Note2: Additionally, if you have partitions containing /tmp or /home"
echo "       that are mounted with 'noatime', this option should be changed"
echo "       to 'atime' or you will see additional test failures."
echo ""
echo "Note3: You should also note that using the fstab option 'acl' for"
echo "       Posix ACLs will generate 1 test failure.  This is not enabled"
echo "       by default on Mandrake Linux."

%postun
%_postun_groupdel nobody

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/usr/share/nls
/usr/share/tmac
/var/cache/fonts
/var/games
/sbin/fasthalt
/sbin/fastboot
%dir /lib/%{name}
/lib/%{name}/init-functions
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%config(noreplace) /etc/hosts.equiv
%config(noreplace) /etc/hosts.lpd
%config(noreplace) /etc/networks
%config(noreplace) /etc/gateways

%changelog
* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.3-8sls
- OpenSLS build
- tidy spec
- remove req on /etc/sgml as that would mean many many MB of junk to fill a
  directory requirement

* Mon Jul 28 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.3-7mdk
- remove rwho requires

* Fri May 23 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.3-6mdk
- requires gettext, add /lib/%{name}/init-functions
- install_initd, remove_initd, use groupadd/del macros

* Tue Feb 18 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.3-5mdk
- keep glibc_lsb, symlinking done there

* Wed Feb 12 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.3-4mdk
- conflicts glibc_lsb, use symlinks to system ld-linux.so.2
- arch specific again now

* Fri Jan 17 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.3-3mdk
- remove getty_ps requirement - removed from distribution

* Thu Jan 10 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.3-2mdk
- requires file

* Mon Dec 9 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.3-1mdk
- Move to LSB v1.3, Provides lsb-1.3, Requires csh

* Sat Nov 16 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-11mdk
- Requires s/diff/diffutils/

* Sat Nov 16 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-10mdk
- update Requires in preparation for upcoming LI18NUX/LSB v1.3

* Tue Sep 10 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-9mdk
- warning on Posix ACLs

* Sat Aug 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-8mdk
- requires mtools

* Wed Aug  7 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-7mdk
- remove conflicts and /etc/ftpusers

* Tue Aug  6 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-6mdk
- Conflicts: wu-ftpd

* Fri Jul 26 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-5mdk
- make pkg noarch, provide our own /etc/ftpusers

* Wed Jul 24 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-4mdk
- add glibc-i18ndata requires

* Tue Jul 23 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-3mdk
- add perl-DBI requires for tjreport results

* Wed Jul 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.2-2mdk
- lsb version 1.2

* Wed Jul 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-8mdk
- bump version to supercede 8.2 update

* Tue Jun 11 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-7mdk
- add creation/removal of group nobody for lsb-apache tests

* Wed May 29 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-6mdk
- add /etc/gateways, fix typo

* Tue May 28 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-5mdk
- add /sbin/fasthalt, /sbin/fastboot scripts
- add dummy /etc/hosts.equiv, /etc/hosts.lpd, /etc/networks files
- add additional note about "noatime" in /etc/fstab
- change requires from sgml-common, rwho, wu-ftpd to specific files

* Tue May 21 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-4mdk
- create some directories LSB tests look for that aren't owned by any
- current Mandrake package, add sgml-common, rwho, wu-ftpd to Requires
- inform installer how to retrieve/run LSB tests about devfs=nomount

* Tue Feb 12 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-3mdk
- change summary too - thx Pixel

* Mon Feb 11 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-2mdk
- change description

* Sat Feb  9 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.1-1mdk
- first release
