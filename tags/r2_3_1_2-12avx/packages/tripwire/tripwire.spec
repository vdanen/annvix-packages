%define name	tripwire
%define version	2.3.1.2
%define release	12avx

%define ext	2

Summary:	A system integrity assessment tool.
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
Source7:	README.RPM
Patch0:		tripwire-2.3.0-50-rfc822.patch.bz2
Patch1:		tripwire-2.3.1-2-fhs.patch.bz2
Patch2:		tripwire-2.3.1-gcc3.patch.bz2
Patch3:		tripwire-jbj.patch.bz2
Patch4:		tripwire-mkstemp.patch.bz2
Patch5:		tripwire-2.3.1-2-gcc-3.3.patch.bz2
Patch6:		tripwire-2.3.1-format.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Buildrequires:	gcc-c++, libstdc++, libstdc++-static-devel, glibc-static-devel

Requires:	sed, grep >= 2.3, gzip, tar, gawk
# Tripwire is NOT 64bit clean, nor endian clean, and only works properly
# on x86 architecture. The open source code doesn't seem to be maintained,
# so this is probably unlikely to change.  We exclude non x86 arches.
ExclusiveArch:	%{ix86}

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

Extra-paranoid Tripwire users will set it up to run once a week and
e-mail the results to themselves.  Then if the e-mails stop coming,
you'll know someone has gotten to the Tripwire program...

After installing this package, you should run "/etc/tripwire/twinstall.sh"
to generate cryptographic keys, and "tripwire --init" to initialize the
database.

%prep
%setup -q -n tripwire-2.3.1-2
cp %{SOURCE2} quickstart.txt
cp %{SOURCE3} quickstart.gif

%patch0 -p1 -b .rfc822
%patch1 -p1 -b .fhs
%patch2 -p1 -b .gcc3
%patch3 -p1 -b .jbj
%patch4 -p1 -b .mkstemp
%patch5 -p0 -b .gcc3.3
%patch6 -p0 -b .format

%build
cd src

#make distclean
rm -rf STLport*
touch STLport_r STLport_d

# Do not parallelize this with _smp_flags or -j
make release RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Install the binaries.
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m755 bin/*/siggen   $RPM_BUILD_ROOT%{_sbindir}
install -m755 bin/*/tripwire $RPM_BUILD_ROOT%{_sbindir}
install -m755 bin/*/twadmin  $RPM_BUILD_ROOT%{_sbindir}
install -m755 bin/*/twprint  $RPM_BUILD_ROOT%{_sbindir}

# Install the man pages.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man4,man5,man8}
install -m644 man/man4/*.* $RPM_BUILD_ROOT%{_mandir}/man4/
install -m644 man/man5/*.* $RPM_BUILD_ROOT%{_mandir}/man5/
install -m644 man/man8/*.* $RPM_BUILD_ROOT%{_mandir}/man8/

# Install configuration information.
mkdir -p $RPM_BUILD_ROOT/etc/tripwire
for infile in %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
	cat $infile |\
	sed -e 's|@sbindir@|%{_sbindir}|g' |\
	sed -e 's|@vardir@|%{_var}|g' >\
	$RPM_BUILD_ROOT/etc/tripwire/`basename $infile .in`
done

cp -p %{SOURCE7} .

# Create the reports directory.
install -d -m700 $RPM_BUILD_ROOT%{_var}/lib/tripwire/report

# Install the cron job.
install -d -m755 $RPM_BUILD_ROOT/etc/cron.daily
install -m755 %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/tripwire-check

# Fix permissions on documentation files.
chmod 644 README Release_Notes ChangeLog COPYING policy/policyguide.txt TRADEMARK quickstart.gif quickstart.txt README.RPM

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%attr(-,root,root) %doc README Release_Notes ChangeLog COPYING policy/policyguide.txt TRADEMARK quickstart.gif quickstart.txt README.RPM
%attr(0755,root,root) %dir /etc/tripwire
%attr(0755,root,root) %config(noreplace) /etc/tripwire/twinstall.sh
%attr(0644,root,root) %config(noreplace) /etc/tripwire/twcfg.txt
%attr(0644,root,root) %config(noreplace) /etc/tripwire/twpol.txt
%attr(0755,root,root) %config(noreplace) /etc/cron.daily/tripwire-check
%attr(0755,root,root) %dir /var/lib/tripwire
%attr(0755,root,root) %dir /var/lib/tripwire/report
%attr(0644,root,root) %{_mandir}/*/*
%attr(0755,root,root) %{_sbindir}/*

%changelog
* Mon Jul 05 2004 Vincent Danen <vdanen@annvix.org> 2.3.1.2-12avx
- BuildRequires: libstdc++-static-devel, glibc-static-devel

* Sat Jun 19 2004 Vincent Danen <vdanen@annvix.org> 2.3.1.2-11avx
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

