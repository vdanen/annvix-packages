%define name	spamassassin
%define version	2.64
%define release	2avx

%define fname	Mail-SpamAssassin
%define instdir	vendor

Summary:	A spam filter for email which can be invoked from mail delivery agents
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Artistic
Group:		Networking/Mail
URL:		http://spamassassin.org/
Source:		http://spamassassin.org/devel/%{fname}-%{version}.tar.bz2
Source1:	spamd.run
Source2:	spamd-log.run
# (fc) 2.60-5mdk don't use version dependent perl call in #!
Patch1:		spamassassin-2.60-fixbang.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	perl-devel
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-HTML-Parser

Prereq:		rpm-helper
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}
Requires:  	perl-DB_File

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

%package tools
Summary:	Miscleanous tools for SpamAssassin
Group:		Networking/Mail
Requires:	perl-Mail-SpamAssassin = %{version}-%{release}

%description tools
Miscleanous tools from various authors, distributed with SpamAssassin.
See /usr/share/doc/spamassassin-tools-*/.

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


%prep

%setup -q -n %{fname}-%{version}
%patch1 -p1 -b .fixbang

%build

%{__perl} \
    Makefile.PL \
    INSTALLDIRS=%{instdir} \
    DESTDIR="%{buildroot}/%{_prefix}" \
    SYSCONFDIR=%{_sysconfdir} < /dev/null

%make OPTIMIZE="%{optflags}" CFLAGS="%{optflags}"

# got root?
# make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}/{%{_initrddir},var/spool/spamassassin}
mkdir -p %{buildroot}/%{_sysconfdir}/mail/%{name}

cat << EOF >> %{buildroot}/%{_sysconfdir}/mail/%{name}/local.cf 
    auto_whitelist_path        /var/spool/spamassassin/auto-whitelist
    auto_whitelist_file_mode   0666
EOF

mkdir -p %{buildroot}%{_srvdir}/spamd/log
mkdir -p %{buildroot}%{_srvlogdir}/spamd
install -m 0750 %{SOURCE1} %{buildroot}%{_srvdir}/spamd/run
install -m 0750 %{SOURCE2} %{buildroot}%{_srvdir}/spamd/log/run

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
[ -f %{_sysconfdir}/spamassassin.cf ] && /bin/mv %{_sysconfdir}/spamassassin.cf %{_sysconfdir}/mail/spamassassin/migrated.cf || true
[ -f %{_sysconfdir}/mail/spamassassin.cf ] && /bin/mv %{_sysconfdir}/mail/spamassassin.cf %{_sysconfdir}/mail/spamassassin/migrated.cf || true
touch /var/spool/spamassassin/auto-whitelist.db
chmod 666 /var/spool/spamassassin/auto-whitelist.db
%_post_srv spamd

%preun
%_preun_srv spamd


%files
%defattr(-,root,root)
%doc README Changes sample-*.txt spamd/README.spamd procmailrc.example INSTALL COPYRIGHT CONTRIB_CERT TRADEMARK USAGE 
%dir %{_sysconfdir}/mail/%{name}
%config(noreplace) %{_sysconfdir}/mail/%{name}/*
%dir %attr(0777,root,root) /var/spool/spamassassin
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/spamassassin
%dir %{_srvdir}/spamd
%dir %{_srvdir}/spamd/log
%{_srvdir}/spamd/run
%{_srvdir}/spamd/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/spamd

%files tools
%defattr(-,root,root)
%doc sql tools masses contrib qmail

%files -n perl-%{fname}
%defattr(644,root,root,755)
%dir %{perl_vendorlib}/Mail
%{perl_vendorlib}/Mail/SpamAssassin*
%{_mandir}/man3*/*

%changelog
* Mon Sep 20 2004 Vincent Danen <vdanen@annvix.org> 2.64-2avx
- update run scripts

* Sat Sep 04 2004 Vincent Danen <vdanen@annvix.org> 2.64-1avx
- 2.64 (security fixes)

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 2.63-7avx
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

* Mon Jan 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.62-1mdk
- Release 2.62
- Fix build on 8.2 (milter@free.fr)

* Tue Dec 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.61-1mdk
- 2.61

* Tue Dec 02 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.60-6mdk
- Fix build for Mdk 9.1 (Derek Simkowiak)

* Mon Nov 17 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.60-5mdk
- Patch1: don't use version dependent perl in #!

* Mon Nov 17 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.60-4mdk
- rebuilt for perl-5.8.2

* Mon Nov 03 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.60-3mdk
- Requires perl-DB-file to get working baysian filters
- Fix build for old distro (Nicolas Chipaux)

* Sun Oct 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.60-2mdk
- make it build and install (!)

* Wed Sep 24 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.60-1mdk
- 2.60
- reorder patches
- fix P0
- drop the osirus patch, it's included
- use macros
- misc spec file fixes

* Mon Sep 15 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.55-2mdk
- Patch5: drop Osirus support (their service is discontinued)

* Mon Jun  2 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.55-1mdk
- Release 2.55

* Tue May 13 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.54-1mdk
- Release 2.54

* Fri Apr  4 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.53-1mdk
- Release 2.53
- spamd is now enabled by default

* Wed Apr  2 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.52-1mdk
- Release 2.52

* Thu Feb  6 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.44-1mdk
- Release 2.44
- Remove patch0 (merged upstream)

* Mon Feb  3 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.43-4mdk
- Patch0: fix buffer overflow in spamd (Timo Sirainen)

* Wed Nov 13 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.43-3mdk
- from  Chris Weber <chris@solution.de> :
  - build cleanly on mdk82, defines for perl_sitelib, perl_man1dir and
    perl_man3dir should be realy in rpm's macrodefs.
* Wed Oct 30 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.43-2mdk
- ISTEAM powered =  add support for Mdk 8.0

* Tue Oct 29 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.43-1mdk
- Back to stable release : 2.43
- now requires perl-HTML-Parser

* Wed Oct 02 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.50-0.1mdk
- 2.50 (devel release)
- Readd my changelog for 2.30-2mdk (fcrozat ??!!)
- remove Patch0,1,2: obsoletes
- Add flags for 8.2 release
- remove conflict with itself
- Add reload entry in initscript

* Wed Sep 25 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.41-2mdk
- Patch0 (CVS): fix escaped dollar sign in INVALID_MSGID
- Patch1 (CVS): -r was not warning if no reporting systems were installed (bug 899)
- Patch2 (CVS): rounding errors where hits=5.000 (bug 893)

* Mon Sep 23 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.41-1mdk
- Release 2.41 
- WARNING : command line syntax has changed, check your procmail rules
- Merge with spamassassin official specfile (split in 3 packages)
- Remove patches 0 (no longer needed), 2 & 3 (merged upstream)
- Patch4: fix name of lock file + fix razor2 support for spamd

* Sun Aug 04 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.31-2mdk
- add BuildRequires db2-devel

* Wed Jul 17 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.31-1mdk
- Release 2.31
- Remove patch2 (merged upstream)
- Fix BuildRequires (Stephane Lentz)

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 2.30-4mdk
- rebuild for perl 5.8.0

* Thu Jun 27 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.30-3mdk
- Fix dependencies

* Tue Jun 18 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.30-2mdk
- Patch2 (CVS): fix --help command
- Patch3 (CVS): add support for Razor v2

* Tue Jun 18 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.30-1mdk
- New spamassassin. Seems to be ok, but it cannot pass its own sample-nospam
  test mail 8).

* Wed Jun  5 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-4mdk
- No longer Require/BuildRequires razor (but users should really install it..)

* Mon May  6 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-3mdk
- BuildConflicts with older version of spamassasin (Thanks to Charles)

* Fri May  3 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-2mdk
- Fix patch1 to really put subsys lock file

* Tue Apr 23 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.20-1mdk
- Release 2.20
- Remove patch1 (merged upstream)
- Patch1: add missing lock in initscript

* Tue Apr  9 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.11-4mdk
- Create whitelist database with writable permission in %post
- Fix whitelist database path
- Oops, fix seach of perl modules

* Tue Apr  9 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.11-3mdk
- Add support for Vipul's Razor
- Patch1: fix to work with Razor 1.20
- Add SQL, spamproxy and qmail documentation

* Tue Apr  9 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.11-2mdk
- Fix %post script

* Mon Apr 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11-1mdk
- initial package
