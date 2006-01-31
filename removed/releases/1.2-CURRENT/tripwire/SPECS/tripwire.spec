#
# spec file for package tripwire
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: tripwire.spec 5113 2006-01-12 19:01:07Z vdanen $

%define revision	$Rev: 5113 $
%define name		tripwire
%define version		2.3.1.2
%define release		%_revrel

Summary:	A system integrity assessment tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://www.tripwire.org/
Source0:	http://download.sourceforge.net/tripwire/tripwire-2.3.1-2.tar.bz2
Source1:	tripwire.cron
Source2:	tripwire.txt
Source3:	tripwire.gif
Source4:	twcfg.txt.in
Source5:	twinstall.sh.in
Source6:	twpol.txt.in
Source7:	twupdate
Source8:	98_tripwire.afterboot
Patch0:		tripwire-2.3.0-50-rfc822.patch
Patch4:		tripwire-mkstemp.patch
Patch6:		tripwire-2.3.1-format.patch
# from http://www.frenchfries.net/paul/tripwire/
Patch7:		tw-20030919.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
Buildrequires:	gcc-c++, libstdc++, libstdc++-static-devel, glibc-static-devel

Requires:	sed, grep >= 2.3, gzip, tar, gawk, afterboot
# Tripwire is NOT 64bit clean, nor endian clean, and only works properly
# on x86 architecture. The open source code doesn't seem to be maintained,
# so this is probably unlikely to change.  We exclude non x86 arches.
#ExclusiveArch:	%{ix86}

%description
Tripwire is a very valuable security tool for Linux systems, if it is
installed to a clean system.  Tripwire should be installed right after
the OS installation, and before you have connected your system to a
network (i.e., before any possibility exists that someone could alter
files on your system).

When Tripwire is initially set up, it creates a database that records
certain file information.  Then when it is run, it compares a
designated set of files and directories to the information stored in
the database.  Added or deleted files are flagged and reported, as are
any files that have changed from their previously recorded state in
the database.  When Tripwire is run against system files on a regular
basis, any file changes will be spotted when Tripwire is run.
Tripwire will report the changes, which will give system
administrators a clue that they need to enact damage control measures
immediately if certain files have been altered.


%prep
%setup -q -n tripwire-2.3.1-2
cp %{SOURCE2} quickstart.txt
cp %{SOURCE3} quickstart.gif

%patch7 -p1 -b .portable
%patch0 -p1 -b .rfc822
%patch4 -p1 -b .mkstemp
%patch6 -p0 -b .format

chmod 0755 configure


%build
%configure --enable-static
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Install the binaries.
mkdir -p %{buildroot}%{_sbindir}
install -m 0500 bin/siggen   %{buildroot}%{_sbindir}
install -m 0500 bin/tripwire %{buildroot}%{_sbindir}
install -m 0500 bin/twadmin  %{buildroot}%{_sbindir}
install -m 0500 bin/twprint  %{buildroot}%{_sbindir}

# Install the man pages.
mkdir -p %{buildroot}%{_mandir}/{man4,man5,man8}
install -m 0644 man/man4/*.* %{buildroot}%{_mandir}/man4/
install -m 0644 man/man5/*.* %{buildroot}%{_mandir}/man5/
install -m 0644 man/man8/*.* %{buildroot}%{_mandir}/man8/

# Install configuration information.
mkdir -p %{buildroot}%{_sysconfdir}/tripwire
for infile in %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
    cat $infile |\
        sed -e 's|@sbindir@|%{_sbindir}|g' |\
        sed -e 's|@vardir@|%{_var}|g' >\
        %{buildroot}%{_sysconfdir}/tripwire/`basename $infile .in`
done

install -m 0750 %{SOURCE7} %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE8} %{buildroot}%{_datadir}/afterboot/98_tripwire

# Create the reports directory.
install -d -m 0700 %{buildroot}%{_var}/lib/tripwire/report

# Install the cron job.
install -d -m 0755 %{buildroot}%{_sysconfdir}/cron.daily
install -m 0750 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.daily/tripwire-check

# Fix permissions on documentation files.
chmod 0644 README Release_Notes ChangeLog COPYING policy/policyguide.txt TRADEMARK quickstart.gif quickstart.txt


%post
%_mkafterboot

%postun
%_mkafterboot


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README Release_Notes ChangeLog COPYING policy/policyguide.txt TRADEMARK quickstart.gif quickstart.txt
%attr(0700,root,root) %dir %{_sysconfdir}/tripwire
%attr(0700,root,root) %config(noreplace) %{_sysconfdir}/tripwire/twinstall.sh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/tripwire/twcfg.txt
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/tripwire/twpol.txt
%attr(0750,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/tripwire-check
%attr(0700,root,root) %dir /var/lib/tripwire
%attr(0700,root,root) %dir /var/lib/tripwire/report
%attr(0644,root,root) %{_mandir}/*/*
%attr(0500,root,root) %{_sbindir}/*
%{_datadir}/afterboot/98_tripwire


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-19avx
- bootstrap build (new gcc, new glibc)
- P7: make it compile on gcc3.4 and other portable fixes
- drop P1, P2, P3, P5; no longer needed with P7
- drop the x86 exclusive arch; it can compile on x86_64 so maybe it
  will work as well

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-18avx
- rebuild
- re-enable stack protection

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-17avx
- s/bash2/bash3/ in twpol.txt.in

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-16avx
- drop /etc/init.d/random and /var/lock/subsys/random from default policy
  file
- add /dev/erandom and /dev/frandom to default policy file
- build with -fno-stack-protector until we fix building static SSP-enabled apps

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-15avx
- fix some typeos in the default policy
- fix some space issues in the afterboot snippet

* Wed Oct 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-14avx
- add afterboot snippet
- remove README.RPM
- add twupdate script
- fix description (extra-paranoid will run it once a week?!?)
- update policy file to make it more Annvix specific

* Thu Sep 16 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-13avx
- someone was on crack to make this all other-readable; make permission
  fixes across the board to make tripwire as tamper-proof as possible

* Mon Jul 05 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-12avx
- BuildRequires: libstdc++-static-devel, glibc-static-devel

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.1.2-11avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 2.3.1.2-10sls
- fix format string vuln reported by Paul Herman

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.3.1.2-9sls
- minor spec cleanups

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 2.3.1.2-8sls
- OpenSLS build
- tidy spec

* Mon Jul 14 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.3.1.2-7mdk
- fix gcc-3.3 build (P5)

* Tue Apr 29 2003 Daouda LO <daouda@mandrakesoft.com> 2.3.1.2-6mdk
- Buildrequires

* Sat Feb  1 2003 Daouda LO <daouda@mandrakesoft.com> 2.3.1.2-5mdk
- rebuild 
- add patch for gcc3 support (bug # 1182)
- synced with rh patches.
- use mkstemp, not mktemp
- source from cvs.

* Mon Dec  3 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.3.1.2-4mdk
- update alpha patch (patch0) to fix build
- s/Copyright/License/
- fix rpmlint warnings

* Tue Jul 17 2001 Daouda LO <daouda@mandrakesoft.com> 2.3.1.2-3mdk
- set correctly the USE_FHS tag to avoid puzzled conf files (reported by Vincent)

* Wed Jul  4 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.3.1.2-2mdk
- add to config TEMPDIRECTORY=/root/tmp to secure temp files

* Fri May 25 2001  Daouda Lo <daouda@mandrakesoft.com> 2.3.1.2-1mdk
- release 2.3.1-2

* Fri Apr 27 2001 Daouda Lo <daouda@mandrakesoft.com> 2.3.1-1mdk
- release 2.3.1

* Fri Feb  9 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.3.0-2mdk
- Build on Alpha too

* Fri Nov  3 2000 Florin Grad <florin@mandrakesoft.com> 2.3.0-1mdk
- first Mandrake version.

* Wed Aug 23 2000 Than Ngo <than@redhat.com>
- remove copyleft information in specfile (Bug #16765)

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove duplicate source files
- sync up description with specspo

* Fri Aug 4 2000 Than Ngo <than@redhat.de>
- remove Vendor and Distribution from specfile (Bug #15246)

* Fri Aug 4 2000 Than Ngo <than@redhat.de>
- starts tripwire --check if it was configured before. (Bug #15384)

* Fri Aug 4 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix sense of checking for the database's existence in the cron job
- actually include twinstall.sh, twcfg.txt, twpol.txt

* Thu Aug 3 2000 Than Ngo <than@redhat.de>
- permission fix (bug #15246)

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add quickstart docs (Ed)
- tweak description text (Ed)

* Thu Jul 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update .spec file to follow RPM conventions
- add tripwire --check to cron.daily

