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
%define version		2.3.7
%define release 	%_revrel
%define epoch		1

%define tlsno 		pfixtls-0.8.18-2.1.3-0.9.7d

%define with_LDAP	1  
%define with_MYSQL	1
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

Patch0:		postfix-2.3.4-avx-config.patch
Patch1:		postfix-alternatives-mdk.patch
Patch3: 	postfix-2.0.18-fdr-hostname-fqdn.patch
Patch4:		postfix-2.1.1-fdr-pie.patch
Patch5:		postfix-2.1.1-fdr-obsolete.patch
Patch8:		postfix-2.3.4-avx-warnsetsid.patch
Patch9:		postfix-2.3.7-vda-64.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	db4-devel
BuildRequires:	gawk
BuildRequires:	perl
BuildRequires:	sed
BuildRequires:	ed
%if %{with_LDAP}
BuildRequires:	openldap-devel >= 2.1
%endif
%if %{with_PCRE}
BuildRequires:	pcre-devel
%endif
%if %{with_MYSQL}
BuildRequires:	mysql-devel
%endif
%if %{with_SASL}
BuildRequires:	libsasl-devel >= 2.0
%endif
%if %{with_TLS}
BuildRequires:	openssl-devel >= 0.9.7
%endif
BuildConflicts:	BerkeleyDB-devel

Provides:	smtpdaemon
Provides:	MailTransportAgent
# we need the postdrop group (gid 36)
Requires:	setup >= 2.2.0-26mdk
Requires(post):	coreutils
Requires(post):	fileutils
Requires(post):	rpm-helper >= 0.3
Requires(postun): rpm-helper >= 0.3
Requires(pre):	rpm-helper >= 0.3
Requires(preun): rpm-helper >= 0.3
Conflicts:	sendmail
Conflicts:	exim
Conflicts:	qmail


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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 4

%patch0 -p1 -b .config
mkdir -p conf/dist
mv conf/main.cf conf/dist
cp %{_sourcedir}/postfix-main.cf conf/main.cf
perl -pi -e 's|@docdir@|%{_docdir}/%{name}-%{version}|g' conf/main.cf
# hack for 64bit
if [ "%{_lib}" != "lib" ]; then
    perl -pi -e 's|/lib/|/%{_lib}/|g' conf/main.cf
fi

%patch3 -p1 -b .postfix-hostname-fqdn
%patch4 -p1 -b .pie
%patch5 -p1 -b .obsolete
%patch8 -p1 -b .warnsetsid
%patch9 -p1 -b .vda

mkdir UCE
install -m 0644 %{_sourcedir}/postfix-anti-UCE.txt UCE
install -m 0644 %{_sourcedir}/header_checks.txt UCE
install -m 0644 %{_sourcedir}/body_checks.txt UCE


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
    CCARGS="${CCARGS} -DUSE_SASL_AUTH -DUSE_CYRUS_SASL -I/usr/include/sasl"
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
mkdir -p %{buildroot}%{_sysconfdir}/sasl2
cp %{_sourcedir}/postfix-smtpd.conf %{buildroot}%{_sysconfdir}/sasl2/smtpd.conf

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
install -c %{_sourcedir}/postfix-etc-pam.d-smtp %{buildroot}%{_sysconfdir}/pam.d/smtp

# Change alias_maps and alias_database default directory to %{_sysconfdir}/postfix
bin/postconf -c %{buildroot}%{_sysconfdir}/postfix -e \
    "alias_maps = hash:%{_sysconfdir}/postfix/aliases" \
    "alias_database = hash:%{_sysconfdir}/postfix/aliases" \
    || exit 1

install -c auxiliary/rmail/rmail %{buildroot}%{_bindir}/rmail

# copy new aliases files and generate a ghost aliases.db file
cp -f %{_sourcedir}/postfix-aliases %{buildroot}%{_sysconfdir}/postfix/aliases
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
install -m 0740 %{_sourcedir}/postfix.run %{buildroot}%{_srvdir}/postfix/run


rm -f %{buildroot}%{_sysconfdir}/postfix/LICENSE

# fix docs
mv %{buildroot}%{_docdir}/%{name}-%{version} %{buildroot}%{_docdir}/%{name}-doc-%{version}


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
    sample_directory=no \
    readme_directory=no \
    html_directory=no \
    upgrade-package

newaliases

%_post_srv postfix

# move previous sasl configuration files to new location if applicable
# have to go through many loops to prevent damaging user configuration
saslpath="`postconf -h smtpd_sasl_path`"
if [ -n "${saslpath}" -a "${saslpath##*:}" -o "${saslpath}" != "${saslpath##*/usr/lib}" ]; then
    postconf -e smtpd_sasl_path=smtpd
fi

for old_smtpd_conf in /etc/postfix/sasl/smtpd.conf %{_libdir}/sasl2/smtpd.conf; do
if [ -e ${old_smtpd_conf} ]; then
    if ! grep -qsve '^\(#.*\|[[:space:]]*\)$' /etc/sasl2/smtpd.conf; then
        # /etc/sasl2/smtpd.conf missing or just comments
        if [ -s /etc/sasl2/smtpd.conf ] && [ ! -e /etc/sasl2/smtpd.conf.rpmnew -o /etc/sasl2/smtpd.conf -nt /etc/sasl2/smtpd.conf.rpmnew ];then                     
                mv /etc/sasl2/smtpd.conf /etc/sasl2/smtpd.conf.rpmnew
        fi
        mv ${old_smtpd_conf} /etc/sasl2/smtpd.conf
    else
        echo "warning: existing ${old_smtpd_conf} will be ignored"
    fi
fi
done


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
%defattr(-,root,root)
%dir %{_sysconfdir}/postfix
%config(noreplace) %{_sysconfdir}/sasl2/smtpd.conf
%attr(0755,root,root) %{_sysconfdir}/postfix/postfix-script
%attr(0755,root,root) %{_sysconfdir}/postfix/post-install
%attr(0755,root,root) %{_sysconfdir}/postfix/postfix-files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/smtp
%config(noreplace) %{_sysconfdir}/postfix/postfix-files
%config(noreplace) %{_sysconfdir}/postfix/main.cf
%{_sysconfdir}/postfix/main.cf.dist
%{_sysconfdir}/postfix/main.cf.default
%{_sysconfdir}/postfix/bounce.cf.default
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


%files doc
%defattr(-,root,root)
%doc AAAREADME US_PATENT_6321267 COMPATIBILITY COPYRIGHT HISTORY LICENSE PORTING RELEASE_NOTES*
%doc examples/smtpd-policy
%doc html UCE
%doc README_FILES


%changelog
* Sat Feb 24 2007 Ying-Hung Chen <ying-at-yingternet.com> 2.3.7
- 2.3.7
- P9: update 2.3.7-vda patch to work with > 2GB quota on 64 bits systems

* Sat Feb 24 2007 Ying-Hung Chen <ying-at-yingternet.com> 2.3.5
- P9: update vda patch to work with > 2GB quota on 64 bits systems

* Sun Dec 24 2006 Vincent Danen <vdanen-at-annvix.org> 2.3.5
- make the buildrequires on openldap-devel, not libldap-devel

* Sun Dec 24 2006 Ying-Hung Chen <ying-at-annvix.org> 2.3.5
- 2.3.5
- P9: update vda patch
- fixed %%post scripting typo
- put back BuildRequires ed since there are still places use ed

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.4
- 2.3.4
- update the body and header checks
- fix the pam.d file
- fix main.cf so it will always point to the right docdir
- use perl to manipulate main.cf instead of ed, and drop the BuildRequires
- don't set delay_warning_time by default (mdv bug #23198)
- adjust default saslpath in the sample config
- fix the location of the sasl configuration file
- drop P6
- rediff P0, P8
- P9: updated

* Tue Nov 14 2006 Ying-Hung Chen <ying-at-annvix.org> 2.2.11
- Fixed annoying install warning message "chown: cannot access 
  `/usr/share/doc/postfix-doc-2.2.11/README_FILES': 
   No such file or directory"
- Added newaliases to generate aliases.db

* Mon Nov 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.11
- rebuild against new pcre

* Tue Sep 26 2006 Ying-Hung Chen <ying-at-annvix.org> 2.2.11
- 2.2.11

* Sun Aug 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.10
- rebuild against new mysql
- rebuild against new openssl
- rebuild against new openldap 
- the run script was accidentally installed as the pam file; fixed
- spec cleanups

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.10
- rebuild against new db4

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.10
- add -doc subpackage
- rebuild with gcc4

* Sat May 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.10
- use Conflicts instead of Obsoletes or it puts apt into an infinite obsoletes
  loop when you have exim installed

* Thu Apr 20 2006 Ying-Hung Chen <ying-at-annvix.org> 2.2.10
- 2.2.10
- updated P9

* Tue Feb 28 2006 Ying-Hung Chen <ying-at-annvix.org> 2.2.5
- Added vda patch for quota support
- build with MySQL support per default

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
