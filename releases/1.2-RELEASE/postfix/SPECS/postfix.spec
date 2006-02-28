#
# spec file for package postfix
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		postfix
%define version		2.2.5
%define release 	%_revrel
%define epoch		1

%define	openssl_ver	0.9.7d
%define tlsno 		pfixtls-0.8.18-2.1.3-%{openssl_ver}

%define with_LDAP	1  
%define with_MYSQL	0
%define with_PCRE	1
%define with_SASL	1
%define with_TLS	1

%{?_without_ldap:  %{expand: %%define with_LDAP 0}}
%{?_without_mysql: %{expand: %%define with_MYSQL 0}}
%{?_without_pcre:  %{expand: %%define with_PCRE 0}}
%{?_without_sasl:  %{expand: %%define with_SASL 0}}
%{?_without_tls:   %{expand: %%define with_TLS 0}}

%{?_with_ldap:  %{expand: %%define with_LDAP 1}}
%{?_with_mysql: %{expand: %%define with_MYSQL 1}}
%{?_with_pcre:  %{expand: %%define with_PCRE 1}}
%{?_with_sasl:  %{expand: %%define with_SASL 1}}
%{?_with_tls:   %{expand: %%define with_TLS 1}}

# Postfix requires one exlusive uid/gid and a 2nd exclusive gid for its own use.
%define postfix_uid	78
%define postfix_gid	78
%define maildrop_group	postdrop
%define maildrop_gid	79
%define queue_directory	%{_var}/spool/postfix

%define post_install_parameters	daemon_directory=%{_libdir}/postfix command_directory=%{_sbindir} queue_directory=%{queue_directory} sendmail_path=%{_sbindir}/sendmail newaliases_path=%{_bindir}/newaliases mailq_path=%{_bindir}/mailq mail_owner=postfix setgid_group=%{maildrop_group} manpage_directory=%{_mandir} readme_directory=%{_docdir}/%name-%version/README_FILES html_directory=%{_docdir}/%name-%version/html

Summary:	Postfix Mail Transport Agent
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	IBM Public License
Group:		System/Servers
URL:		http://www.postfix.org/
Source0: 	ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz.sig
Source2:	postfix-main.cf
Source3:	postfix-aliases
Source4: 	ftp://ftp.aet.tu-cottbus.de/pub/postfix_tls/%{tlsno}.tar.gz
Source5:	ftp://ftp.aet.tu-cottbus.de/pub/postfix_tls/%{tlsno}.tar.gz.sig
Source6:	postfix.run
Source7:	postfix-etc-pam.d-smtp
Source10:	http://jimsun.LinxNet.com/misc/postfix-anti-UCE.txt
Source11:	http://jimsun.LinxNet.com/misc/header_checks.txt
Source12:	http://jimsun.LinxNet.com/misc/body_checks.txt
Source15:	postfix-smtpd.conf

Patch0:		postfix-2.2.5-avx-config.patch
Patch1:		postfix-alternatives-mdk.patch
Patch3: 	postfix-2.0.18-fdr-hostname-fqdn.patch
Patch4:		postfix-2.1.1-fdr-pie.patch
Patch5:		postfix-2.1.1-fdr-obsolete.patch
Patch6:		postfix-2.2.4-mdk-saslpath.patch
Patch8:		postfix-2.2.5-avx-warnsetsid.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	db4-devel, gawk, perl, sed, ed
BuildConflicts:	BerkeleyDB-devel

%if %{with_LDAP}
BuildRequires:	libldap-devel >= 2.1
%endif
%if %{with_PCRE}
BuildRequires:	pcre-devel
%endif
%if %{with_MYSQL}
BuildRequires:	MySQL-devel
%endif
%if %{with_SASL}
BuildRequires:	libsasl-devel >= 2.0
%endif
%if %{with_TLS}
BuildRequires:	openssl-devel >= %{openssl_ver}
%endif

Provides:	smtpdaemon, MailTransportAgent
# we need the postdrop group (gid 36)
Requires:	setup >= 2.2.0-26mdk
PreReq: 	coreutils, fileutils
Requires(post):	rpm-helper >= 0.3
Requires(postun): rpm-helper >= 0.3
Requires(pre):	rpm-helper >= 0.3
Requires(preun): rpm-helper >= 0.3
Obsoletes:	sendmail exim qmail


%description
Postfix is a Mail Transport Agent (MTA), supporting LDAP, SMTP AUTH (SASL),
TLS and running in a chroot environment.

Postfix is Wietse Venema's mailer that started life as an alternative 
to the widely-used Sendmail program.
Postfix attempts to be fast, easy to administer, and secure, while at 
the same time being sendmail compatible enough to not upset existing 
users. Thus, the outside has a sendmail-ish flavor, but the inside is 
completely different.
This software was formerly known as VMailer. It was released by the end
of 1998 as the IBM Secure Mailer. From then on it has lived on as Postfix. 

This rpm supports LDAP, SMTP AUTH (trough cyrus-sasl) and TLS.
If you also need MySQL support, rebuild the srpm --with mysql.


%prep
%setup -q -a 4

%patch0 -p1 -b .avx
mkdir -p conf/dist
mv conf/main.cf conf/dist
cp %{SOURCE2} conf/main.cf
# hack for 64bit
if [ "%{_lib}" != "lib" ]; then
    ed conf/main.cf <<-EOF || exit 1
    ,s/\/lib\//\/%{_lib}\//g
    w
    q
EOF
fi

%patch3 -p1 -b .postfix-hostname-fqdn
%patch4 -p1 -b .pie
%patch5 -p1 -b .obsolete
%patch6 -p1 -b .saslpath
%patch8 -p1 -b .warnsetsid

mkdir UCE
install -m 0644 %{SOURCE10} UCE
install -m 0644 %{SOURCE11} UCE
install -m 0644 %{SOURCE12} UCE


%build
%serverbuild
%ifarch x86_64
    CCARGS="-fPIC"
%else
    CCARGS=
%endif
AUXLIBS=

%ifarch s390 s390x ppc
CCARGS="${CCARGS} -fsigned-char"
%endif

%if %{with_LDAP}
    CCARGS="${CCARGS} -DHAS_LDAP"
    AUXLIBS="${AUXLIBS} -L%{_libdir} -lldap -llber"
%endif
%if %{with_PCRE}
    CCARGS="${CCARGS} -DHAS_PCRE"
    AUXLIBS="${AUXLIBS} -lpcre"
%endif
%if %{with_MYSQL}
    CCARGS="${CCARGS} -DHAS_MYSQL -I/usr/include/mysql"
    AUXLIBS="${AUXLIBS} -L%{_libdir}/mysql -lmysqlclient -lm"
%endif
%if %{with_SASL}
    CCARGS="${CCARGS} -DUSE_SASL_AUTH -I/usr/include/sasl"
    AUXLIBS="${AUXLIBS} -lsasl2"
%endif
%if %{with_TLS}
    LIBS=
    CCARGS="${CCARGS} -DUSE_TLS -I/usr/include/openssl"
    AUXLIBS="${AUXLIBS} -lssl -lcrypto"
%endif

export CCARGS AUXLIBS
make -f Makefile.init makefiles

unset CCARGS AUXLIBS
make DEBUG="" OPT="%{optflags}"
#make manpages

# add correct parameters to main.cf.dist
LD_LIBRARY_PATH=$PWD/lib${LD_LIBRARY_PATH:+:}${LD_LIBRARY_PATH} \
    ./src/postconf/postconf -c ./conf/dist -e \
    %post_install_parameters
mv conf/dist/main.cf conf/main.cf.dist


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# install postfix into the build root
LD_LIBRARY_PATH=$PWD/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} \
sh postfix-install -non-interactive \
    install_root=%{buildroot} \
    config_directory=%{_sysconfdir}/postfix \
    %post_install_parameters \
    || exit 1

# for sasl configuration
mkdir -p %{buildroot}%{_sysconfdir}/postfix/sasl
cp %{SOURCE15} %{buildroot}%{_sysconfdir}/postfix/sasl/smtpd.conf

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
install -c %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/smtp

# Change alias_maps and alias_database default directory to %{_sysconfdir}/postfix
bin/postconf -c %{buildroot}%{_sysconfdir}/postfix -e \
    "alias_maps = hash:%{_sysconfdir}/postfix/aliases" \
    "alias_database = hash:%{_sysconfdir}/postfix/aliases" \
    || exit 1

install -c auxiliary/rmail/rmail %{buildroot}%{_bindir}/rmail

# copy new aliases files and generate a ghost aliases.db file
cp -f %{SOURCE3} %{buildroot}%{_sysconfdir}/postfix/aliases
chmod 0644 %{buildroot}%{_sysconfdir}/postfix/aliases

touch %{buildroot}%{_sysconfdir}/postfix/aliases.db

for i in active bounce corrupt defer deferred flush incoming private saved maildrop public pid trace; do
    mkdir -p %{buildroot}%{queue_directory}/$i
done

# install performance benchmark tools by hand
for i in smtp-sink smtp-source; do
    install -c -m 0755 bin/$i %{buildroot}%{_sbindir}/
    install -c -m 0644 man/man1/$i.1 %{buildroot}%{_mandir}/man1/
done

# RPM compresses man pages automatically.
# - Edit postfix-files to reflect this, so post-install won't get confused
#   when called during package installation.
ed %{buildroot}%{_sysconfdir}/postfix/postfix-files <<EOF || exit 1
    %s/\(\/man[158]\/.*\.[158]\):/\1.bz2:/
    w
    q
EOF

# install qshape
install -c -m 0755 auxiliary/qshape/qshape.pl %{buildroot}%{_sbindir}/qshape
cp man/man1/qshape.1 %{buildroot}%{_mandir}/man1/qshape.1

# remove sample_directory from main.cf (#15297)
# the default is /etc/postfix
sed -i "/^sample_directory/d" %{buildroot}%{_sysconfdir}/postfix/main.cf

mkdir -p %{buildroot}/usr/lib
pushd %{buildroot}/usr/lib
    ln -sf ../sbin/sendmail sendmail
popd

mkdir -p %{buildroot}%{_srvdir}/postfix
install -m 0740 %{SOURCE6} %{buildroot}%{_srvdir}/postfix/run


rm -f %{buildroot}%{_sysconfdir}/postfix/LICENSE


%pre
%_pre_useradd postfix %{queue_directory} /bin/false %{postfix_uid}
%_pre_groupadd %{maildrop_group} %{maildrop_gid} postfix


%post
# upgrade configuration files if necessary
sh %{_sysconfdir}/postfix/post-install \
    config_directory=%{_sysconfdir}/postfix \
    daemon_directory=%{_libdir}/postfix \
    command_directory=%{_sbindir} \
    mail_owner=postfix \
    setgid_group=%{maildrop_group} \
    manpage_directory=%{_mandir} \
    sample_directory=%{_docdir}/%{name}-%{version}/samples \
    readme_directory=%{_docdir}/%{name}-%{version}/README_FILES \
    html_directory=%{_docdir}/%{name}-%{version}/html \
    upgrade-package

%_post_srv postfix

# move previous sasl configuration files to new location if applicable
# have to go through many loops to prevent damaging user configuration
saslpath="`postconf -h smtpd_sasl_path | cut -d: -f 1`"
if [ -n "${saslpath}" -a "${saslpath%/}" != "%{_libdir}/sasl2" -a -e %{_libdir}/sasl2/smtpd.conf ]; then
    if ! grep -qsve '^\(#.*\|[[:space:]]*\)$' ${saslpath}/smtpd.conf; then
        # ${saslpath}/smtpd.conf missing or just comments
        if [ -s ${saslpath}/smtpd.conf ] && [ ! -e ${saslpath}/smtpd.conf.rpmnew -o ${saslpath}/smtpd.conf -nt ${saslpath}/smtpd.conf.rpmnew ];then
            mv ${saslpath}/smtpd.conf ${saslpath}/smtpd.conf.rpmnew
        fi
        mv %{_libdir}/sasl2/smtpd.conf ${saslpath}/smtpd.conf
    fi
fi


%preun
%_preun_srv postfix

%postun
%_postun_userdel postfix
%_postun_groupdel %{maildrop_group}

[ $1 = 0 ] && exit 0
/usr/sbin/srv --restart postfix 2>&1 > /dev/null || :


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-, root, root)
%doc AAAREADME US_PATENT_6321267 COMPATIBILITY COPYRIGHT HISTORY LICENSE PORTING RELEASE_NOTES*
%doc examples/smtpd-policy
%doc html UCE
%doc README_FILES

%dir %{_sysconfdir}/postfix
%dir %{_sysconfdir}/postfix/sasl
%config(noreplace) %{_sysconfdir}/postfix/sasl/smtpd.conf
%attr(0755,root,root) %{_sysconfdir}/postfix/postfix-script
%attr(0755,root,root) %{_sysconfdir}/postfix/post-install
%attr(0755,root,root) %{_sysconfdir}/postfix/postfix-files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/smtp
%config(noreplace) %{_sysconfdir}/postfix/postfix-files
%config(noreplace) %{_sysconfdir}/postfix/main.cf
%{_sysconfdir}/postfix/main.cf.dist
%{_sysconfdir}/postfix/main.cf.default
%config(noreplace) %{_sysconfdir}/postfix/master.cf
%config(noreplace) %{_sysconfdir}/postfix/access
%config(noreplace) %{_sysconfdir}/postfix/aliases
%ghost %{_sysconfdir}/postfix/aliases.db
%config(noreplace) %{_sysconfdir}/postfix/canonical
%config(noreplace) %{_sysconfdir}/postfix/generic
%config(noreplace) %{_sysconfdir}/postfix/header_checks
%config(noreplace) %{_sysconfdir}/postfix/relocated
%config(noreplace) %{_sysconfdir}/postfix/transport
%config(noreplace) %{_sysconfdir}/postfix/virtual
%{_sysconfdir}/postfix/makedefs.out

%dir %attr(0750,root,admin) %{_srvdir}/postfix
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/postfix/run

# For correct directory permissions check postfix-install script
%dir %{queue_directory}
%dir %attr(0700,postfix,root) %{queue_directory}/active
%dir %attr(0700,postfix,root) %{queue_directory}/bounce
%dir %attr(0700,postfix,root) %{queue_directory}/corrupt
%dir %attr(0700,postfix,root) %{queue_directory}/defer
%dir %attr(0700,postfix,root) %{queue_directory}/deferred
%dir %attr(0700,postfix,root) %{queue_directory}/flush
%dir %attr(0700,postfix,root) %{queue_directory}/hold
%dir %attr(0700,postfix,root) %{queue_directory}/incoming
%dir %attr(0700,postfix,root) %{queue_directory}/private
%dir %attr(0700,postfix,root) %{queue_directory}/saved
%dir %attr(0700,postfix,root) %{queue_directory}/trace
%dir %attr(0730,postfix,%{maildrop_group}) %{queue_directory}/maildrop
%dir %attr(0710,postfix,%{maildrop_group}) %{queue_directory}/public
%dir %attr(0755,root,root) %{queue_directory}/pid

%dir %attr(0755,root,root) %{_libdir}/postfix
%attr(0755,root,root) %{_libdir}/postfix/bounce
%attr(0755,root,root) %{_libdir}/postfix/cleanup
%attr(0755,root,root) %{_libdir}/postfix/discard
%attr(0755,root,root) %{_libdir}/postfix/error
%attr(0755,root,root) %{_libdir}/postfix/flush
%attr(0755,root,root) %{_libdir}/postfix/lmtp
%attr(0755,root,root) %{_libdir}/postfix/local
%attr(0755,root,root) %{_libdir}/postfix/master
%attr(0755,root,root) %{_libdir}/postfix/nqmgr
%attr(0755,root,root) %{_libdir}/postfix/oqmgr
%attr(0755,root,root) %{_libdir}/postfix/pickup
%attr(0755,root,root) %{_libdir}/postfix/pipe
%attr(0755,root,root) %{_libdir}/postfix/proxymap
%attr(0755,root,root) %{_libdir}/postfix/qmgr
%attr(0755,root,root) %{_libdir}/postfix/qmqpd
%attr(0755,root,root) %{_libdir}/postfix/scache
%attr(0755,root,root) %{_libdir}/postfix/showq
%attr(0755,root,root) %{_libdir}/postfix/smtp
%attr(0755,root,root) %{_libdir}/postfix/smtpd
%attr(0755,root,root) %{_libdir}/postfix/spawn
%attr(0755,root,root) %{_libdir}/postfix/trivial-rewrite
%attr(0755,root,root) %{_libdir}/postfix/virtual
%attr(0755,root,root) %{_libdir}/postfix/verify
%attr(0755,root,root) %{_libdir}/postfix/anvil

%attr(0755,root,root) %{_libdir}/postfix/tlsmgr

%attr(0755,root,root) %{_sbindir}/postalias
%attr(0755,root,root) %{_sbindir}/postcat
%attr(0755,root,root) %{_sbindir}/postconf
%attr(2755,root,%{maildrop_group}) %{_sbindir}/postdrop
%attr(2755,root,%{maildrop_group}) %{_sbindir}/postqueue
%attr(0755,root,root) %{_sbindir}/postfix
%attr(0755,root,root) %{_sbindir}/postkick
%attr(0755,root,root) %{_sbindir}/postlock
%attr(0755,root,root) %{_sbindir}/postlog
%attr(0755,root,root) %{_sbindir}/postmap
%attr(0755,root,root) %{_sbindir}/postsuper

%attr(0755,root,root) %{_sbindir}/smtp-sink
%attr(0755,root,root) %{_sbindir}/smtp-source
%attr(0755,root,root) %{_sbindir}/qshape

%attr(0755,root,root) %{_sbindir}/sendmail
/usr/lib/sendmail
%attr(0755,root,root) %{_bindir}/mailq
%attr(0755,root,root) %{_bindir}/newaliases
%attr(0755,root,root) %{_bindir}/rmail

%{_mandir}/*/*


%changelog
* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5
- remove prereq on sysklogd

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5-5avx
- fix call to srv

* Wed Sep 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5-4avx
- don't change the manpage names in /etc/postfix/postfix-files since
  they're not being alternativized (ha!) anymore (ie. mailq.1 rather
  than mailq.postfix.1)

* Wed Sep 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5-3avx
- rebuild against fixed rpm-helper

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5-2avx
- rebuild against new pcre

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.2.5-1avx
- 2.2.5
- run scripts are now considered config files and are not replaceable
- shorten some alternatives; we'll use alternatives to provide the sendmail symlink
  but that's about it; make exim and postfix conflict
- updated saslpath patch (andreas)
- reduce the number of %%config files that aren't really config files
- get rid of alternatives
- drop P2; merged upstream
- rediff P8
- don't apply the TLS patch

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-6avx
- fix perms on run scripts

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-5avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-4avx
- rebuild

* Fri Jan 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-3avx
- don't refresh aliases at install time (bluca)
- provide a default /etc/pam.d/smtp for saslauthd users (bluca)
- don't move sasl conf if not necessary (bluca)
- make main.cf.dist a working config file (bluca)
- include manpage for qshape (bluca)

* Wed Jan 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-2avx
- rebuild against new openssl

* Sat Oct 16 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-1avx
- 2.1.5
- remove support for experimental versions; we'll never ship an
  experimental version
- remove chroot support
- remove the queue_directory_remove() function; it's not used and it's
  too dangerous to every use (big bad assumption)
- add the qshape tool
- lots of spec cleanups
- add missing sendmail.postfix manpage
- add missing TLS docs
- add P3, P4, and P5 from Fedora
- add P6 and P7 from Mandrake
- use a non-commented main.cf and put the full main.cf as main.cf.dist
- merge the Mandrake config patch with our own removing a few options like
  the delay warning and the changed ESMTP banner (we don't need to advertise
  the version or OS)
- if /usr/lib/sasl2/smtpd.conf exists, move it to /etc/postfix/sasl
- remove P99 (smtpd multiline patch)
- add Jim Seymour's text on UCE (S10-S12)
- remove Requires: procmail
- PreReq: fileutils, sysklogd
- fix BuildRequires
- P8: make master warn on setsid() failure rather than abort
  which lets us run the master process supervised
- update run script; remove the log service (not necessary,
  postfix never logs to stdout)
- alternatives points the libdir sendmail to %%{_libdir} but this isn't right on
  lib64 because programs will look for /usr/lib/sendmail not /usr/lib64/sendmail; fixed

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-10avx
- update run scripts

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-9avx
- rebuild against latest openssl

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-8avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.0.13-7sls
- minor spec cleanups

* Tue Feb 04 2004 Vincent Danen <vdanen@opensls.org> 2.0.13-6sls
- supervise scripts
- remove initscript
- postfix has static uid/gid 78, postdrop is static gid 79
- no more PreReq: chkconfig and service

* Fri Jan 02 2004 Vincent Danen <vdanen@opensls.org> 2.0.13-5sls
- requires pcre-devel, not libpcre-devel (for amd64)

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 2.0.13-4sls
- OpenSLS build
- tidy spec

* Mon Aug 18 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.13-3mdk
- add CHROOT_INFO.README.MANDRAKE in doc section, in particular to
  explain how to sync system and chroot files

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.13-2mdk
- BuildRequires: db4-devel, libsasl-devel to match other deps

* Wed Aug  6 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.13-1mdk
- 2.0.13

* Fri Jun 27 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.12-3mdk
- fix default cyrus transport location thx to Buchan Milne
- build against db4.1

* Fri Jun 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.12-2mdk
- use sasl2

* Thu Jun 12 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.12-1mdk
- new version

* Mon May 26 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.10-1mdk
- new version

* Thu May 22 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.9-4mdk
- update multiline greeting patch

* Wed May 07 2003 Yves Duret <yves@zarb.org> 2.0.9-3mdk
- opensslpower.

* Mon May 05 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0.9-2mdk
- workaround to fix requires openssl (yves sucks)

* Sat May 03 2003 Yves Duret <yves@zarb.org> 2.0.9-1mdk
- 2.0.9

* Thu Mar  6 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.6-1mdk
- 2.0.6 is a minor security fix
- build against openssl-0.9.7a
- build against libdb4.0 instead of libdb3.3

* Tue Jan 21 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.1-2mdk
- fix proxymap to not be launched chroot'ed thx to <mr at uue dot org>
  (Michael Reinsch)
- needs sasl1 to build, not any (not sasl2 that is)

* Mon Jan 20 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.1-1mdk
- new version (plank the children (c) dams)
- drop the domain.name -> example.com patch: we've had a similar patch on
  1.1.x since Wed May 29 2002, but postfix mainstream authors still haven't
  changed accordingly in postfix mainstream sources; therefore I assume
  they don't agree with such a patch, and there is no point bothering on
  our side to maintain such a patch

* Tue Dec 17 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.12-2mdk
- have initscript 'start' update the db's, thx to Todd Lyons <tlyons@mandrakesoft.com>

* Mon Dec 09 2002 Yves Duret <yves@zarb.org> 1.1.12-1mdk
- new upstream version.
- updated postfix tls to according postfix version.

* Mon Nov 11 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.11-6mdk
- Make it lib64 aware

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.11-5mdk
- fix gc vs c-r
- prereq : s/(sh-|text|file)utils/coreutils/

* Tue Sep 17 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.11-3mdk
- don't use "rmail.postfix" but "rmail" in master.cf, fix uucp,
  thx Buchan Milne <bgmilne@cae.co.za>

* Fri Aug 30 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.11-3mdk
- fix upgrades from Mandrake 8.2 (call update-alternatives in triggerpostun
  so that old files removal is already done)

* Tue Jul 30 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.1.11-2mdk
- use %%_pre_groupadd and %%_postun_groupdel %{maildrop_group}

* Wed Jul 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.11-1mdk
- new version
- updated postfix_lfs source to 0.8.11a-1.1.11-0.9.6d

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.1.10-3mdk
- add postfix user

* Wed May 29 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.10-2mdk
- specfile: added --with --without build conditions to override included defines.
- MySQL: adjust requires and buildrequires.
- main.cf: fix a typo.
- added P100 to perform domain.name-to-example.com everywhere 
  as requested by the .name TLD maintainer Andreas Aardal Hanssen <ahanssen@gnr.com>.

* Sun May 19 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.10-1mdk
- version 1.1.10.
- updated source9 (postfix_tls) to pfixtls-0.8.10-1.1.10-0.9.6d for postfix 1.1.10.
- requires openssl with version according to pfixtls need (0.9.6d here).
- fix sample_directory pointed to /sample in main.cf (tvignaud).
- fix /etc/aliases symlink (alternatives).
- chroot: added etc/{resolv.conf,hosts,host.conf} to the chroot-jail.
- chroot: fix db3 trigger (on libdb3.3)
- chroot: fix ldap trigger (on libldap2 instead of generic openldap package).
- chroot: renamed ROOT by CHROOT.
- do not ship two times the TLS doc (in TLS). 
- use %%{_docdir} instead of %%_datadir/doc.
- rpmlint: use %%SOURCE6 instead of %%sourcedir.
- spec: replace official condif by reverse experimental condif (so my vim macro works again).
- description: add a space before begining with a new sentence.

* Tue May 14 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.9-1mdk
- version 1.1.9
- updated source9 (postfix_tls) to pfixtls-0.8.9-1.1.9-0.9.6d for postfix 1.1.9
- source in gzip format instead of bzip2
- include .sig file for postfix src and pfixtls
- fix %%postun script (exit if $0=0 instead of restart postfix)
  pointed by Guillaume Cottenceau
  
* Mon May 13 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.8-3mdk
- fix chroot pbs in upgrade too. thx Pascal Terjean. i really sux.
- add db3 in chroot jail.

* Mon May 13 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.8-2mdk
- finally fix uppgrade. i sux.

* Fri May 10 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.8-1mdk
- version 1.1.8-20020508 (bug fixes)
- updated source9 (postfix_tls) to pfixtls-0.8.8-1.1.8-0.9.6d for postfix 1.1.8

* Wed Apr 24 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.7-3mdk
- fix alternative pb (symlink not created)

* Wed Apr 17 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.7-2mdk
- added %{_libdir}/sendmail link for backward compatibility

* Sun Apr 14 2002 Yves Duret <yduret@mandrakesoft.com> 1.1.7-1mdk
- the long awaiting postfix update (added Epoch tag).
- complete spec file rewrite (using the RedHat one).

* Tue Jan 29 2002 Geoffrey Lee <snailtalk@mandarkesoft.com> 20010228-20mdk
- A much needed upgrade to pl08.
- pfixtls 0.7.13 for pl08.
- Remove the postfix useradd and groupadd.
- Requires latest setup package.

* Mon Nov 26 2001 Vincent Danen <vdanen@mandrakesoft.com> 20010228-19mdk
- apply security fix from Venema that fixes potential DoS

* Wed Nov 14 2001 Philippe Libat <philippe@mandrakesoft.com> 20010228-18mdk
- add pam.d/smtp, sasl/smtpd.conf for sasl configuration

* Wed Nov 14 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 20010228-17mdk
- remove empty include statement that was preventing USE_SASL_AUTH to be
  defined. Thanks to James Farrell <jfarrell@candyraver.com> for reporting and
  fixing this problem.

* Tue Oct 23 2001 Florin <florin@mandrakesoft.com> 20010228-16mdk
- rebuild for db3

* Tue Sep  4 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 20010228-15mdk
- subst `Linux-Mandrake' with `Mandrake Linux' in SMTP Greeting Banner

* Mon Sep 03 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 20010228-14mdk
- Hand modified the config file patch, to fix bug #4048

* Mon Sep 03 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 20010228-13mdk
- Provides: MailTransportAgent

* Sat Jul 07 2001 Stefan van der Eijk <stefan@eijk.nu> 20010228-12mdk
- BuildRequires:	libsasl-devel

* Fri Jul 06 2001 Philippe Libat <philippe@mandrakesoft.com> 20010228-11mdk
- new db3

* Mon Jun 25 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 20010228-10mdk
- Patch dnsverify.pl, to have /usr/bin/perl not /users2/local/bin/perl
  on first line, as the interpreter to be run.

* Thu Jun 19 2001 Philippe Libat <philippe@mandrakesoft.com> 20010228-9mdk
- version pl3
- TLS, LDAP

* Wed Jun 13 2001 Philippe Libat <philippe@mandrakesoft.com> 20010228-8mdk
- SASL Support

* Tue Jun 12 2001 Philippe Libat <philippe@mandrakesoft.com> 20010228-7mdk
- Added config samples

* Tue Apr 17 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 20010228-6mdk
- Do not stop postfix before installing, it will prevent us from restarting it.

* Tue Apr 17 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 20010228-5mdk
- Revert latest change, cause the DB are already re-generated in postfix.init
  at each startup.

* Thu Apr 05 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 20010228-4mdk
- When upgrading, always regenerate all .db file (except aliases)
  This fix bug #2260 (upgrade postfix need to recreate /etc/postfix/*.db
  files). This avoid problem when the DB file version change.
  
  thanks to Steffen Ullrich <coyote.frank@gmx.de> for reporting and helping
  fixing this bug.

* Wed Apr 04 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 20010228-3mdk
- Fix bug #1810 (postfix invokes procmail with options that cause a `>From '
  line in the headers) by adding the -o options to the procmail call.

* Thu Mar 29 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 20010228-2mdk
- use post/preun service macros
- user serverbuild for safer flags

* Tue Mar  6 2001 Vincent Danen <vdanen@mandrakesoft.com> 20010228-1mdk
- 20010228 release
- macros
- added conflicts: qmail
- added buildrequires: db3-devel
- added buildconflicts: BerkeleyDB-devel

* Wed Jan 17 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231_pl13-2mdk
- install rmail script.

* Wed Jan 17 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231_pl13-1mdk
- Upgrade to patch level 13.
- add delay_warning_time option to main.cf (fix bug #1390).

* Thu Nov 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 19991231_pl08-6mdk
- Explicit compile with db1.

* Tue Aug 29 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231_pl08-5mdk
- change license to IBM Public License

* Tue Aug 29 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231_pl08-4mdk
- use noreplace
- use %{_initrddir}

* Tue Aug 29 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231_pl08-3mdk
- correct 2 shell syntax error in %postun

* Wed Aug  2 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 19991231_pl08-2mdk
- %config(noreplace)

* Fri Jul 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231_pl08-1mdk
- updated to postfix release 19991231-pl8.
- small specfile cleanup.

* Mon Jul 10 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 19991231-8mdk
- let spechelper compress man-pages and strip binaries (hey guyes, we do this
  for a _long_ time)
- use new macros

* Sat Jul 08 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 19991231-7mdk
- modified find statement to only find files (not directories)
- moved BuildRoot to /var/tmp

* Fri May 05 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231-6mdk
- Fix an aliases.db problem...

* Tue Mar 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 19991231-5mdk
- Fix group.

* Wed Mar  8 2000 Pixel <pixel@mandrakesoft.com> 19991231-4mdk
- add prereq wc

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 19991231
- added postfix group
- corrected aliases.db bug

* Mon Dec 27 1999 Jerome Dumonteil <jd@mandrakesoft.com>
- Add postfix check in post to create sub dirs in spool

* Mon Dec 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add -a $DOMAIN -d $LOGNAME to procmail (philippe).
- New banner.

* Wed Nov 10 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- fix if conflicts with sendmail.

* Sat Jun  5 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- install bins from libexec/

* Sat Jun  5 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 19990601
- .spec cleanup for easier updates

* Wed May 26 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- created link from /usr/sbin/sendmail to %{_libdir}/sendmail
  so it doesn't bug out when i rpm -e sendmail
- Now removes /var/lock/subsys/postfix like a good little prog
  upon rpm -e

* Fri Apr 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Mandrake adptations.

* Tue Apr 13 1999 Arne Coucheron <arneco@online.no>
  [19990317-pl04-1]

* Tue Mar 30 1999 Arne Coucheron <arneco@online.no>
  [19990317-pl03-2]
- Castro, Castro, pay attention my friend. You're making it very hard
  maintaining the package if you don't follow the flow of the releases

* Thu Mar 25 1999 Arne Coucheron <arneco@online.no>
  [19990317-pl02-1]

* Tue Mar 23 1999 Arne Coucheron <arneco@online.no>
  [19990317-3]
- added bugfix patch01

* Sat Mar 20 1999 Arne Coucheron <arneco@online.no>
  [19990317-2]
- removed the mynetworks line in main.cf, let postfix figure it out
- striping of the files in /usr/sbin
- alias database moved to /etc/postfix and made a symlink to it in /etc
- enabled procmail support in main.cf and added it to Requires:
- check status on master instead of postfix in the init script
- obsoletes postfix-beta
- had to move some of my latest changelog entries up here since Edgard Castro
  didn't follow my releases

* Thu Mar 18 1999 Edgard Castro <castro@usmatrix.net>
  [19990317]

* Tue Mar 16 1999 Edgard Castro <castro@usmatrix.net>
  [alpha-19990315]

* Tue Mar  9 1999 Edgard Castro <castro@usmatrix.net>
  [19990122-pl01-2]
- shell and gecho information changed to complie with Red Hat stardand
- changed the name of the rpm package to postfix, instead of postfix-beta

* Tue Feb 16 1999 Edgard Castro <castro@usmatrix.net>
  [19990122-pl01-1]

* Sun Jan 24 1999 Arne Coucheron <arneco@online.no>
  [19990122-1]
- shell for postfix user changed to /bin/true to avoid logins to the account
- files in /usr/libexec/postfix moved to %{_libdir}/postfix since this complies
  more with the Red Hat standard

* Wed Jan 06 1999 Arne Coucheron <arneco@online.no>
  [19981230-2]
- added URL for the source
- added a cron job for daily check of errors
- sample config files moved from /etc/postfix/sample to the docdir 
- dropped making of symlinks in /usr/sbin and instead installing the real
  files there
- because of the previous they're not needed anymore in /usr/libexec/postfix,
  so they are removed from that place

* Fri Jan 01 1999 Arne Coucheron <arneco@online.no>
  [19981230-1]

* Tue Dec 29 1998 Arne Coucheron <arneco@online.no>
  [19981222-1]
- first build of rpm version
