%define name	postfix
%define version	2.0.13
%define release 8avx
%define epoch	1

# If set to 0 if official version, 1 if snapshot
%define experimental	0
%define releasedate 	20020508

%define	openssl_ver	0.9.7b
%define tlsno 		pfixtls-0.8.15-%version-%openssl_ver

%if ! %{experimental}
%define ver		%{version}
%define ftp_directory	official
%else
%define ver		%{version}-%{releasedate}
%define ftp_directory	experimental
%endif

%define alternatives 	1
%define alternatives_install_cmd update-alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.postfix 30 --slave %{_libdir}/sendmail mta-in_libdir %{_sbindir}/sendmail.postfix --slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.postfix --slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.postfix --slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.postfix --slave %{_mandir}/man1/mailq.1.bz2 mta-mailqman %{_mandir}/man1/mailq.postfix.1.bz2 --slave %{_mandir}/man1/newaliases.1.bz2 mta-newaliasesman %{_mandir}/man1/newaliases.postfix.1.bz2 --slave %{_mandir}/man5/aliases.5.bz2 mta-aliasesman %{_mandir}/man5/aliases.postfix.5.bz2 --slave %{_sysconfdir}/aliases mta-etc_aliases %{_sysconfdir}/postfix/aliases
%define with_LDAP	1  
%define with_MYSQL	0
%define with_PCRE	1
%define with_SASL	1
%define with_TLS	1
%define with_SMTPD_MULTILINE_GREETING 0

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

%define CHROOT		/var/spool/postfix

%define whinge		%_bindir/logger -p mail.info -t postfix/rpm
%define postfix_running %{_lib}/postfix/master -t >/dev/null 2>&1; echo $?
%define copy_cmd copy() { file="`ls --sort=time $1 |head -n 1`"; ln -f "$file" "$2" 2>/dev/null || cp -df "$file" "$2"; }


Summary:	Postfix Mail Transport Agent
Name:		%{name}
Version:	%{ver}
Release:	%{release}
Epoch:		%{epoch}
License:	IBM Public License
Group:		System/Servers
URL:		http://www.postfix.org/
Source0: 	ftp://ftp.porcupine.org/mirrors/postfix-release/%{ftp_directory}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.porcupine.org/mirrors/postfix-release/%{ftp_directory}/%{name}-%{version}.tar.gz.sig
Source3: 	postfix-etc-init.d-postfix
Source5:	postfix-aliases
Source6: 	postfix-chroot-setup.awk
Source8:	ftp://ftp.aet.tu-cottbus.de/pub/postfix_tls/%{tlsno}.tar.gz.sig
Source9: 	ftp://ftp.aet.tu-cottbus.de/pub/postfix_tls/%{tlsno}.tar.gz
Source10:	postfix.chroot_info
Source11:	postfix.run
Source12:	postfix-log.run
Patch0:		postfix-2.0.12-config-mdk.patch.bz2
Patch1:		postfix-alternatives-mdk.patch.bz2
Patch12:	postfix-smtp_sasl_proto.c.patch.bz2
# applied if %with_SMTPD_MULTILINE_GREETING=1
Patch99:	postfix-1.1.12-20021124-multiline-greeting.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	db4-devel, gawk, /usr/bin/perl, sed, ed
BuildConflicts:	BerkeleyDB-devel
%if %{with_LDAP}
BuildRequires:	openldap >= 1.2.9, openldap-devel >= 1.2.9
%endif

%if %{with_PCRE}
Requires:	pcre
BuildRequires:	pcre, pcre-devel
%endif

%if %{with_MYSQL}
Requires:	MySQL, MySQL-client
BuildRequires:	MySQL, MySQL-client, MySQL-devel
%endif

%if %{with_SASL}
Requires:	cyrus-sasl
BuildRequires:	cyrus-sasl, libsasl-devel
%endif

%if %{with_TLS}
Requires:	openssl >= %openssl_ver
BuildRequires:	openssl-devel
%endif

Provides:	smtpdaemon, MailTransportAgent
Requires:	procmail
# we need the postdrop group (gid 36)
Requires:	setup >= 2.2.0-26mdk
PreReq: 	coreutils
PreReq: 	rpm-helper >= 0.3
%if %alternatives
PreReq:		/usr/sbin/update-alternatives
%else
Obsoletes:	sendmail exim qmail
%endif


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
If you need MySQL too, rebuild the srpm --with mysql.

%prep
%setup -q -a 9
# Apply the TLS patch, must be at first, because the changes of master.cf
%if %{with_TLS}
patch -p1 <%{tlsno}/pfixtls.diff
%endif

%patch0 -p0 -b .mdkconfig

%patch12 -p1 -b .auth

%if %alternatives
%patch1 -p1 -b .alternatives
%endif

# Apply my SMTPD Multiline greeting patch
%if %{with_SMTPD_MULTILINE_GREETING}
%patch99 -p1 -b .multiline
%endif

# Move around the TLS docs
%if %{with_TLS}
mkdir TLS
mv %{tlsno}/doc/* TLS
for i in ACKNOWLEDGEMENTS CHANGES INSTALL README TODO; do
  mv %{tlsno}/$i $i.TLS
done
%endif

# setup master.cf to be chrooted
mv conf/master.cf conf/master.cf-nochroot
awk -f %{SOURCE6} < conf/master.cf-nochroot > conf/master.cf

install -m644 %{SOURCE10} CHROOT_INFO.README.MANDRAKE

%build
%serverbuild
CCARGS=
AUXLIBS=

%ifarch s390 s390x ppc
CCARGS="${CCARGS} -fsigned-char"
%endif

%if %{with_LDAP}
  CCARGS="${CCARGS} -DHAS_LDAP"
  AUXLIBS="${AUXLIBS} -lldap -llber"
%endif
%if %{with_PCRE}
  # -I option required for pcre 3.4 (and later?) - yves ??? use /usr/bin/pcre-config
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
  CCARGS="${CCARGS} -DHAS_SSL -I/usr/include/openssl"
  AUXLIBS="${AUXLIBS} -lssl -lcrypto"
%endif

export CCARGS AUXLIBS
make -f Makefile.init makefiles

unset CCARGS AUXLIBS
make DEBUG="" OPT="$RPM_OPT_FLAGS"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# install postfix into the build root
sh postfix-install -non-interactive \
       install_root=%buildroot \
       config_directory=%{_sysconfdir}/postfix \
       daemon_directory=%{_libdir}/postfix \
       command_directory=%{_sbindir} \
       queue_directory=%{_var}/spool/postfix \
       sendmail_path=%{_sbindir}/sendmail.postfix \
       newaliases_path=%{_bindir}/newaliases.postfix \
       mailq_path=%{_bindir}/mailq.postfix \
       mail_owner=postfix \
       setgid_group=%{maildrop_group} \
       manpage_directory=%{_mandir} \
       sample_directory=%{_docdir}/%name-%version/samples \
       readme_directory=%{_docdir}/%name-%version/README_FILES || exit 1

# rpm %%doc macro wants to take his files in buildroot
rm -fr ./samples
mv %buildroot/%{_docdir}/%name-%version/samples .

# Change alias_maps and alias_database default directory to %{_sysconfdir}/postfix
bin/postconf -c %buildroot/%{_sysconfdir}/postfix -e \
        "alias_maps = hash:%{_sysconfdir}/postfix/aliases" \
        "alias_database = hash:%{_sysconfdir}/postfix/aliases" \
|| exit 1

# These set up the chroot directory structure
mkdir -p %buildroot/%CHROOT/etc
mkdir -p %buildroot/%CHROOT/%{_lib}
mkdir -p %buildroot/%CHROOT/%{_libdir}
mkdir -p %buildroot/%CHROOT/%{_datadir}/zoneinfo

install -c auxiliary/rmail/rmail %buildroot/%{_bindir}/rmail

# copy new aliases files and generate a ghost aliases.db file
cp -f %{SOURCE5} %buildroot/%{_sysconfdir}/postfix/aliases
chmod 644 %buildroot/%{_sysconfdir}/postfix/aliases

touch %buildroot/%{_sysconfdir}/postfix/aliases.db

for i in active bounce corrupt defer deferred flush incoming private saved maildrop public pid; do
    mkdir -p %buildroot/%CHROOT/$i
done

# install smtp-sink/smtp-source by hand
for i in smtp-sink smtp-source; do
  install -c -m 755 bin/$i %buildroot/%{_sbindir}/
done

# Move stuff around so we don't conflict with sendmail
mv %buildroot/%{_bindir}/rmail %buildroot/%{_bindir}/rmail.postfix
mv %buildroot/%{_mandir}/man1/mailq.1 %buildroot/%{_mandir}/man1/mailq.postfix.1
mv %buildroot/%{_mandir}/man1/newaliases.1 %buildroot/%{_mandir}/man1/newaliases.postfix.1
mv %buildroot/%{_mandir}/man5/aliases.5 %buildroot/%{_mandir}/man5/aliases.postfix.5

# RPM compresses man pages automatically.
# - Edit postfix-files to reflect this, so post-install won't get confused
#   when called during package installation.
ed %buildroot/%{_sysconfdir}/postfix/postfix-files <<EOF || exit 1
%s/\(\/man[158]\/.*\.[158]\):/\1.bz2:/
w
q
EOF

mkdir -p %{buildroot}%{_srvdir}/postfix/log
mkdir -p %{buildroot}%{_srvlogdir}/postfix
install -m 0750 %{SOURCE11} %{buildroot}%{_srvdir}/postfix/run
install -m 0750 %{SOURCE12} %{buildroot}%{_srvdir}/postfix/log/run


%pre
%_pre_useradd postfix /var/spool/postfix /bin/false %{postfix_uid}
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
	sample_directory=%{_docdir}/%name-%version/samples \
	readme_directory=%{_docdir}/%name-%version/README_FILES \
	upgrade-package

%_post_srv postfix

# setup chroot config
mkdir -p %{CHROOT}/%_sysconfdir
[ -e %_sysconfdir/localtime ] && cp %_sysconfdir/localtime %{CHROOT}/%_sysconfdir
# yves 1.1.10-1mdk -- ??
[ -e %_sysconfdir/resolv.conf ] && cp %_sysconfdir/resolv.conf %{CHROOT}/%_sysconfdir
[ -e %_sysconfdir/hosts ] && cp %_sysconfdir/hosts %{CHROOT}/%_sysconfdir

%if %alternatives
%{alternatives_install_cmd}
%endif

# (gc) necessary when we upgrade from a non alternativized package, because it's executed after the old files are removed
%triggerpostun -- postfix
%if %alternatives
[ -e %{_sbindir}/sendmail.postfix ] && %{alternatives_install_cmd} || :
%endif

# Generate chroot jails on the fly when needed things are installed/upgraded
%triggerin -- glibc
%{copy_cmd}
# Kill off old versions
rm -rf %{CHROOT}/%{_lib}/libnss* %{CHROOT}/%{_lib}/libresolv*
# Copy the relevant parts in
LIBCVER=`ls -l /%{_lib}/libc.so.6* | sed "s/.*libc-\(.*\).so$/\1/g"`
for i in compat dns files hesiod nis nisplus winbind wins; do
	[ -e /%{_lib}/libnss_$i-${LIBCVER}.so ] && copy /%{_lib}/libnss_$i-${LIBCVER}.so %{CHROOT}/%{_lib}/
	[ -e /%{_lib}/libnss_$i.so ] && copy /%{_lib}/libnss_$i.so %{CHROOT}/%{_lib}/
done
copy /%{_lib}/libresolv-${LIBCVER}.so %{CHROOT}/%{_lib}/
ldconfig -n %{CHROOT}/%{_lib}

%if %{with_LDAP}
%triggerin -- libldap2
rm -rf %{CHROOT}%{_libdir}/liblber* %{CHROOT}%{_libdir}/libldap*
%{copy_cmd}
# yves 1.1.10-1mdk -- i like chrooting things..
# cp -L instead of copy_cmd
cp -L %{_libdir}/liblber.so.2 %{CHROOT}%{_libdir}/
cp -L %{_libdir}/libldap_r.so.2 %{CHROOT}%{_libdir}/
cp -L %{_libdir}/libldap.so.2 %{CHROOT}%{_libdir}/
#ldconfig -n %{CHROOT}%{_libdir}
%endif

%triggerin -- setup
rm -f %{CHROOT}/etc/{services,host.conf}
%{copy_cmd}
copy /etc/services %{CHROOT}/etc
# yves 1.1.10-1mdk -- ??
copy /etc/host.conf %{CHROOT}/etc

# put db4 in the chroot jail
%triggerin -- libdb4.1
%{copy_cmd} 
copy %{_libdir}/libdb-4.1.so %{CHROOT}/%{_libdir}	

%preun

# selectively remove the rest of the queue directory structure
# first remove the "queues" (and assume the hash depth is still 2)
queue_directory_remove () {
    for dir in active bounce defer deferred flush incoming; do
        for a in 0 1 2 3 4 5 6 7 8 9 A B C D E F; do
   	    test -d $dir/$a && {
	        for b in 0 1 2 3 4 5 6 7 8 9 A B C D E F; do
		    test -d $dir/$a/$b && (
		        /bin/rm -f $dir/$a/$b/*
		        /bin/rmdir $dir/$a/$b
		    )
		done
		/bin/rmdir $dir/$a || echo "WARNING: preun - unable to remove directory %{_var}/spool/postfix/$dir/$a"
	    }
        done
	/bin/rmdir $dir || echo "WARNING: preun - unable to remove directory %{_var}/spool/postfix/$dir"
    done

    # now remove the other directories
    for dir in corrupt maildrop pid private public saved; do
        test -d $dir && {
            /bin/rm -f $dir/*
            /bin/rmdir $dir || echo "WARNING: preun - unable to remove directory %{_var}/spool/postfix/$dir"
        }
    done
}

%_preun_srv postfix

if [ $1 = 0 ]; then
	%if %alternatives
    		update-alternatives --remove mta %{_sbindir}/sendmail.postfix
	%endif

	cd %CHROOT && {
		# Clean up chroot environment
		rm -rf %{CHROOT}/%{_lib} %{CHROOT}/usr %{CHROOT}/etc
        	queue_directory_remove
	}
	true # to ensure we exit safely
fi

# Remove unneeded symbolic links
for i in samples README_FILES; do
  test -L %{_sysconfdir}/postfix/$i && rm %{_sysconfdir}/postfix/$i || true
done


%postun

%_postun_userdel postfix
%_postun_groupdel %{maildrop_group}

[ $1 = 0 ] && exit 0
/usr/sbin/srv restart postfix 2>&1 > /dev/null || :

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-, root, root)
%verify(not md5 size mtime) %config %dir %{_sysconfdir}/postfix
%attr(0644, root, root)         %{_sysconfdir}/postfix/LICENSE
%attr(0755, root, root) %config	%{_sysconfdir}/postfix/postfix-script
%attr(0755, root, root) %config	%{_sysconfdir}/postfix/post-install
%attr(0644, root, root)                                                %{_sysconfdir}/postfix/postfix-files
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/main.cf
%attr(0644, root, root)                                                %{_sysconfdir}/postfix/main.cf.default
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/master.cf
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/access
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/aliases
%attr(0644, root, root) %verify(not md5 size mtime) %ghost             %{_sysconfdir}/postfix/aliases.db
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/canonical
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/pcre_table
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/regexp_table
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/relocated
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/transport
%attr(0644, root, root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/postfix/virtual

#%dir %attr(-, root, root) %{_sysconfdir}/postfix/README_FILES
#%attr(0644,   root, root) %{_sysconfdir}/postfix/README_FILES/*

%dir %{_srvdir}/postfix
%dir %{_srvdir}/postfix/log
%{_srvdir}/postfix/run
%{_srvdir}/postfix/log/run
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/postfix

%dir                      %verify(not md5 size mtime) %{_var}/spool/postfix
%dir %attr(-, root, root) %verify(not md5 size mtime) %{_var}/spool/postfix/etc
%dir %attr(-, root, root) %verify(not md5 size mtime) %{_var}/spool/postfix/%{_lib}
%attr(-, root, root)      %verify(not md5 size mtime) %{_var}/spool/postfix/usr

# For correct directory permissions check postfix-install script
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/active
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/bounce
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/corrupt
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/defer
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/deferred
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/flush
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/incoming
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/private
%dir %attr(0700, postfix, root)     %verify(not md5 size mtime) %{_var}/spool/postfix/saved

%dir %attr(0730, postfix, %{maildrop_group}) %verify(not md5 size mtime) %{_var}/spool/postfix/maildrop
%dir %attr(0710, postfix, %{maildrop_group}) %verify(not md5 size mtime) %{_var}/spool/postfix/public

%dir %attr(0755, root, root)        %verify(not md5 size mtime) %{_var}/spool/postfix/pid

%doc 0README COMPATIBILITY HISTORY INSTALL LICENSE PORTING RELEASE_NOTES
%if %{with_TLS}
%doc ACKNOWLEDGEMENTS.TLS CHANGES.TLS README.TLS TODO.TLS TLS
%endif
%doc html
%doc samples
%doc README_FILES
%doc CHROOT_INFO.README.MANDRAKE

%dir %attr(0755, root, root) %verify(not md5 size mtime) %{_libdir}/postfix
%{_libdir}/postfix/bounce
%{_libdir}/postfix/cleanup
%{_libdir}/postfix/error
%{_libdir}/postfix/flush
%{_libdir}/postfix/lmtp
%{_libdir}/postfix/local
%{_libdir}/postfix/master
%{_libdir}/postfix/nqmgr
%{_libdir}/postfix/pickup
%{_libdir}/postfix/pipe
%{_libdir}/postfix/proxymap
%{_libdir}/postfix/qmgr
%{_libdir}/postfix/qmqpd
%{_libdir}/postfix/showq
%{_libdir}/postfix/smtp
%{_libdir}/postfix/smtpd
%{_libdir}/postfix/spawn
%{_libdir}/postfix/trivial-rewrite
%{_libdir}/postfix/virtual

%if %{with_TLS}
%{_libdir}/postfix/tlsmgr
%endif

%{_sbindir}/postalias
%{_sbindir}/postcat
%{_sbindir}/postconf
%attr(2755,root,%{maildrop_group}) %{_sbindir}/postdrop
%attr(2755,root,%{maildrop_group}) %{_sbindir}/postqueue
%{_sbindir}/postfix
%{_sbindir}/postkick
%{_sbindir}/postlock
%{_sbindir}/postlog
%{_sbindir}/postmap
%{_sbindir}/postsuper

%{_sbindir}/smtp-sink
%{_sbindir}/smtp-source

%{_sbindir}/sendmail.postfix
%{_bindir}/mailq.postfix
%{_bindir}/newaliases.postfix
%attr(0755, root, root) %{_bindir}/rmail.postfix

%{_mandir}/*/*


%changelog
* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.org> 2.0.13-8avx
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
- use %%_docdir instead of %%_datadir/doc.
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
- added %_libdir/sendmail link for backward compatibility

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
