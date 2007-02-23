#
# spec file for package spamassassin
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		spamassassin
%define version		3.1.8
%define release		%_revrel

%define fname		Mail-SpamAssassin
%define instdir		vendor

Summary:	A spam filter for email which can be invoked from mail delivery agents
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Artistic
Group:		Networking/Mail
URL:		http://spamassassin.apache.org/
Source0:	http://www.apache.org/dist/spamassassin/source/%{fname}-%{version}.tar.bz2
Source1:	http://www.apache.org/dist/spamassassin/source/%{fname}-%{version}.tar.bz2.asc
Source2:	spamd.run
Source3:	spamd-log.run
Source4:	spamassassin-default.rc
Source5:	spamassassin-spamc.rc
# (fc) 2.60-5mdk don't use version dependent perl call in #!
Patch1:		spamassassin-3.1.0-avx-fixbang.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	openssl-devel
BuildRequires:	perl(Time::HiRes)
BuildRequires:	perl(HTML::Parser)
BuildRequires:	perl(Digest::SHA1)
BuildRequires:  perl(DB_File)
BuildRequires:	perl(Net::DNS)
BuildRequires:	perl(Mail::SPF::Query)
BuildRequires:	perl(IP::Country)
BuildRequires:	perl(IO::Socket::SSL)
BuildRequires:	perl(Archive::Tar)
BuildRequires:	perl(IO::Zlib)
BuildRequires:	perl(Net::Ident)

Requires:  	perl-Mail-SpamAssassin = %{version}-%{release}
Requires:  	perl(DB_File)
Requires:	perl(Net::DNS)
# these aren't 100% required, but are very useful
Requires:	perl(Sys::Hostname::Long)
Requires:	perl(Mail::SPF::Query)
Requires:	perl(IP::Country)
Requires:	perl(IO::Socket::SSL)
Requires:	perl(Archive::Tar)
Requires:	perl(IO::Zlib)
Requires:	perl(Net::Ident)
Requires:	perl-libwww-perl
Requires:	gnupg
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
SpamAssassin provides you with a way to reduce if not completely eliminate
Unsolicited Commercial Email (SPAM) from your incoming email.  It can
be invoked by a MDA such as sendmail or postfix, or can be called from
a procmail script, .forward file, etc.  It uses a genetic-algorithm
evolved scoring system to identify messages which look spammy, then
adds headers to the message so they can be filtered by the user's mail
reading software.  This distribution includes the spamd/spamc components
which create a server that considerably speeds processing of mail.

SpamAssassin also includes support for reporting spam messages
automatically, and/or manually, to collaborative filtering databases such
as Vipul's Razor, DCC or pyzor. 
Install perl-Razor-Agent package to get Vipul's Razor support. 
Install dcc package to get Distributed Checksum Clearinghouse (DCC) support.
Install pyzor package to get Pyzor support.


%package spamd
Summary:	Daemonized version of SpamAssassin
Group:		System/Servers
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	spamassassin = %{version}

%description spamd
The purpose of this program is to provide a daemonized version of the
spamassassin executable. The goal is improving throughput performance
for automated mail checking.

This package includes "spamc", a fast, low-overhead C client program.


%package -n perl-%{fname}
Summary:	Mail::SpamAssassin -- SpamAssassin e-mail filter Perl modules
Group:		Development/Perl

%description -n perl-%{fname}
Mail::SpamAssassin is a module to identify spam using text analysis and
several internet-based realtime blacklists. Using its rule base, it uses a
wide range of heuristic tests on mail headers and body text to identify
``spam'', also known as unsolicited commercial email. Once identified, the
mail can then be optionally tagged as spam for later filtering using the
user's own mail user-agent application.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Obsoletes:	spamassassin-tools

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{fname}-%{version}
%patch1 -p1 -b .fixbang


%build
perl \
    Makefile.PL \
    INSTALLDIRS=vendor \
    SYSCONFDIR=%{_sysconfdir} \
    DATADIR=%{_datadir}/spamassassin \
    ENABLE_SSL=yes \
    RUN_NET_TESTS=no< /dev/null

%make OPTIMIZE="%{optflags}"


%check
export LANG=C
export LC_ALL=C
export LANGUAGE=C
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/var/spool/spamassassin
mkdir -p %{buildroot}%{_sysconfdir}/mail/spamassassin/sa-update-keys
mkdir -p %{buildroot}%{_localstatedir}/spamassassin

cat << EOF >> %{buildroot}/%{_sysconfdir}/mail/spamassassin/local.cf 
required_hits			5
rewrite_header			Subject [**SPAM**]
report_safe			0
EOF

install -m 0644 %{_sourcedir}/spamassassin-default.rc %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m 0644 %{_sourcedir}/spamassassin-spamc.rc %{buildroot}%{_sysconfdir}/mail/spamassassin/

mkdir -p %{buildroot}%{_srvdir}/spamd/{log,env}
install -m 0740 %{_sourcedir}/spamd.run %{buildroot}%{_srvdir}/spamd/run
install -m 0740 %{_sourcedir}/spamd-log.run %{buildroot}%{_srvdir}/spamd/log/run
echo "-c -m5 -H" >%{buildroot}%{_srvdir}/spamd/env/OPTIONS


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
[ -f %{_sysconfdir}/spamassassin.cf ] && /bin/mv %{_sysconfdir}/spamassassin.cf %{_sysconfdir}/mail/spamassassin/migrated.cf || true
[ -f %{_sysconfdir}/mail/spamassassin.cf ] && /bin/mv %{_sysconfdir}/mail/spamassassin.cf %{_sysconfdir}/mail/spamassassin/migrated.cf || true


%post spamd
%_post_srv spamd


%preun spamd
%_preun_srv spamd


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/mail/spamassassin
%dir %{_sysconfdir}/mail/spamassassin/sa-update-keys
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/spamassassin/*.cf
%config(noreplace) %{_sysconfdir}/mail/spamassassin/*.pre
%config(noreplace) %{_sysconfdir}/mail/spamassassin/spamassassin-default.rc
%dir %attr(0700,mail,mail) /var/spool/spamassassin
%dir %{_localstatedir}/spamassassin
%attr(0755,root,root) %{_bindir}/sa-learn
%attr(0755,root,root) %{_bindir}/sa-update
%attr(0755,root,root) %{_bindir}/spamassassin
%{_mandir}/man1/sa-learn.1*
%{_mandir}/man1/sa-update.1*
%{_mandir}/man1/spamassassin.1*
%{_datadir}/spamassassin

%files spamd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/mail/spamassassin/spamassassin-spamc.rc
%attr(0755,root,root) %{_bindir}/spamc
%attr(0755,root,root) %{_bindir}/spamd
%{_mandir}/man1/spamc.1*
%{_mandir}/man1/spamd.1*
%dir %attr(0750,root,admin) %{_srvdir}/spamd
%dir %attr(0750,root,admin) %{_srvdir}/spamd/log
%dir %attr(0750,root,admin) %{_srvdir}/spamd/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/spamd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/spamd/log/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/spamd/env/OPTIONS

%files -n perl-%{fname}
%defattr(644,root,root,755)
%dir %{perl_vendorlib}/Mail
%{perl_vendorlib}/Mail/SpamAssassin*
%{perl_vendorlib}/spamassassin-run.pod
%{_mandir}/man1/spamassassin-run.1*
%{_mandir}/man3*/*

%files doc
%defattr(-,root,root)
%doc README Changes sample-*.txt procmailrc.example INSTALL TRADEMARK USAGE
%doc spamd/README* spamd/PROTOCOL
%doc sql tools masses contrib


%changelog
* Fri Feb 23 2007 Vincent Danen <vdanen-at-annvix.org> 3.1.8
- 3.1.8: security fix for CVE-2007-0451

* Thu Dec 28 2006 Vincent Danen <vdanen-at-annvix.org> 3.1.7
- set LANG/LC_ALL/LANGUAGE variables for make test
- add directories for sa-update and requires on gnupg

* Sun Nov 12 2006 Ying-Hung Chen <ying-at-annvix.org> 3.1.7
- Spamassassin version 3.1.7
- Add requires: perl-libwww-perl for sa-update commend

* Thu Nov 02 2006 Ying-Hung Chen <ying-at-annvix.org> 3.1.3
- Update the Requires Mail-SpamAssassin section to fix the dependency problem

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.3
- rebuild against new openssl
- spec cleanups

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.3
- 3.1.3 (fixes CVE-2006-2447)

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1
- make -doc obsolete -tools

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.1
- 3.1.1
- rebuild against perl 5.8.8
- perl policy
- drop the -tools subpackage, it only contained docs
- create -doc subpackage
- get rid of the with_TEST stuff, use %%check instead

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- drop requires on perl-Geography-Countries; it's not required (IP-Country already
  requires it and SA doesn't explicitly need it itself)
- BuildRequires: perl-IP-Country
- add missing requires on perl-IO-Socket-SSL
- BuildRequires/Requires: perl-Archive-Tar, perl-IO-Zlib, and perl-Net-Ident for
  all the extra goodies
- don't automatically ship the auto-whitelist or enable it

* Sun Mar 12 2006 Ying-Hung Chen <ying-at-annvix.org> 3.1.0
- Requires perl-IP-Country, perl-Geography-Countries

* Mon Mar 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- make spamd use ./env/OPTIONS rather than the sysconfig file which
  didn't properly set $OPTIONS anyways (used $SPAMOPTIONS)
- drop S6 as a result

* Sat Mar 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- Requires: perl-Mail-SPF-Query, perl-Sys-Hostname-Long (provide SPF support)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Dec 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-3avx
- uncompressed patches
- fix bug #14 and make /var/spool/spamassassin read/write by mail only
- remove dcc_home from the default local.cf
- add perl-Net-DNS and perl-DB_File as BuildReqs
- add a conditional to make test

* Sun Oct 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-2avx
- both spamd/log/run and /etc/sysconfig/spamd were marked as SOURCE3 so the
  run script was actually the bzipped sysconfig file
- fix spamd runscript; read sysconfig/spamd rather than sysconfig/spamassassin
  and remove obsolete option -a
- fix sysconfig/spamd to remove the -d (daemonize) option
- Requires: perl-Net-DNS

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.1.0-1avx
- 3.1.0
- put spamd and spamc into -spamc package
- fix URL
- rediff P1

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-10avx
- rebuild against new perl

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-9avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-8avx
- use execlineb for run scripts
- move logdir to /var/log/service/spamd
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-7avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-5avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-4avx
- use logger for logging

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.64-3avx
- rebuild against new perl

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.64-2avx
- update run scripts

* Sat Sep 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.64-1avx
- 2.64 (security fixes)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.63-7avx
- Annvix build

* Thu Jun  3 2004 Vincent Danen <vdanen@opensls.org> 2.63-6sls
- %%post_srv and %%preun_srv

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.63-5sls
- build against perl 5.8.4

* Mon Mar 22 2004 Vincent Danen <vdanen@opensls.org> 2.63-4sls
- fix syntax error in run script

* Mon Mar 22 2004 Vincent Danen <vdanen@opensls.org> 2.63-3sls
- fix supervise scripts; spamd should not run in daemon mode

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.63-2sls
- minor spec cleanups

* Wed Jan 21 2004 Vincent Danen <vdanen@opensls.org> 2.63-1sls
- OpenSLS build
- tidy spec
- 2.63
- supervise scripts
- remove P0 and the initscript

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
