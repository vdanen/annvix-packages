#
# spec file for package krb5
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		krb5
%define version		1.4.2
%define release		%_revrel

%define major		1
%define libname		%mklibname %{name} %{major}

Summary:	The Kerberos network authentication system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://web.mit.edu/kerberos/www/
# from http://web.mit.edu/kerberos/dist/krb5/1.4/krb5-%{version}-signed.tar
Source0:	%{name}-%{version}.tar.gz
Source5:	krb5.conf
Source8:	kdcrotate
Source9:	kdc.conf
Source10:	kadm5.acl
Source11:	krsh
Source12:	krlogin
Source19:	statglue.c
Source23:	Mandrake-Kerberos-HOWTO.html
Source24:	%{name}-%{version}.tar.gz.asc
Source25:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.tar.gz
Source26:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.sig
Source27:	ktelnet.run
Source28:	ktelnet-log.run
Source29:	kftp.run
Source30:	kftp-log.run
Source31:	kadmind.run
Source32:	kadmind-log.run
Source33:	kpropd.run
Source34:	kpropd-log.run
Source35:	krb5kdc.run
Source36:	krb5kdc-log.run
Source39:	08_kftp.afterboot
Source40:	08_ktelnet.afterboot
Patch0:		krb5-1.2.2-telnetbanner.patch
Patch1:		krb5-1.2.5-biarch-utmp.patch
Patch3:		krb5-1.3-telnet.patch
Patch4:		krb5-1.3-mdk-no-rpath.patch
Patch5:		krb5-1.3-fdr-info-dir.patch
Patch6:		krb5-1.3-fdr-large-file.patch
Patch7:		krb5-1.3-fdr-ksu-path.patch
Patch8:		krb5-1.3-fdr-ksu-access.patch
Patch9:		krb5-1.3-fdr-pass-by-address.patch
Patch12:	krb5-1.3-fdr-ftp-glob.patch
Patch16:	krb5-1.3.2-fdr-efence.patch
Patch17:	krb5-1.3.3-fdr-rcp-sendlarge.patch
Patch21:	krb5-1.3.3-rcp-markus.patch
Patch22:	krb5-1.4.1-api.patch
Patch23:	krb5-1.4.1-fclose.patch
Patch24:	krb5-1.3.6-telnet-environ.patch
Patch25:	krb5-1.3.5-gethostbyname_r.patch
# (gb) preserve file names when generating files from *.et (multiarch fixes)
Patch26:	krb5-1.3.6-et-preserve-file-names.patch
# http://qa.mandriva.com/show_bug.cgi?id=9410
Patch27:	krb5-1.4.1-ftplfs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison, flex, libtermcap-devel, texinfo, tcl
BuildRequires:	libext2fs-devel, chrpath, multiarch-utils >= 1.0.3

PreReq:		grep, info, coreutils, info-install

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.


%package -n %{libname}-devel
Summary:	Development files needed for compiling Kerberos 5 programs
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	krb-devel krb5-devel libkrb-devel libkrb5-devel
Obsoletes:	krb-devel krb5-devel

%description -n %{libname}-devel
Kerberos is a network authentication system.  The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you'll
need to install this package.


%package -n %{libname}
Summary:	The shared libraries used by Kerberos 5
Group:		System/Libraries
Prereq:		grep, /sbin/ldconfig, coreutils
Provides:	krb5-libs
Obsoletes:	krb5-libs

%description -n %{libname}
Kerberos is a network authentication system.  The krb5-libs package
contains the shared libraries needed by Kerberos 5.  If you're using
Kerberos, you'll need to install this package.


%package server
Group:		System/Servers
Summary:	The server programs for Kerberos 5
Requires:	%{libname} = %{version}, %{name}-workstation = %{version}, words
Prereq:		grep, /sbin/install-info, /bin/sh, coreutils

%description server
Kerberos is a network authentication system.  The krb5-server package
contains the programs that must be installed on a Kerberos 5 server.
If you're installing a Kerberos 5 server, you need to install this
package (in other words, most people should NOT install this
package).


%package workstation
Summary:	Kerberos 5 programs for use on workstations
Group:		System/Base
Requires:	%{libname} = %{version}
Prereq:		grep, /sbin/install-info, /bin/sh, coreutils

%description workstation
Kerberos is a network authentication system.  The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd) as well as kerberized versions of Telnet and FTP.  If your
network uses Kerberos, this package should be installed on every
workstation.


%package -n telnet-server-krb5
Summary:	A telnet-server with kerberos support
Group:		System/Servers
Requires:	%{libname} = %{version}
Requires:	ipsvd
Requires:	krb5-workstation
PreReq:		afterboot
Obsoletes:	telnet-server
Provides:	telnet-server

%description -n telnet-server-krb5
Telnet is a popular protocol for logging into remote systems over the Internet.
The telnet-server package provides a telnet daemon, which will support remote
logins into the host machine. The telnet daemon is enabled by default. You may
disable the telnet daemon by editing /etc/inetd.conf.

This version supports kerberos authentication.


%package -n telnet-client-krb5
Summary:	A telnet-client with kerberos support
Group:		System/Servers
Requires:	%{libname} = %{version}
Obsoletes:	telnet
Provides:	telnet
 
%description -n telnet-client-krb5
Telnet is a popular protocol for logging into remote systems over the Internet.
The telnet package provides a command line telnet client.

This version supports kerberos authentication.


%package -n ftp-client-krb5
Summary:	A ftp-client with kerberos support
Group:		Networking/File transfer
Requires:	%{libname} = %{version}
Obsoletes:	ftp
Provides:	ftp

%description -n ftp-client-krb5
The ftp package provides the standard UNIX command-line FTP client.
FTP is the file transfer protocol, which is a widely used Internet
protocol for transferring files and for archiving files.

This version supports kerberos authentication.


%package -n ftp-server-krb5
Summary:	A ftp-server with kerberos support
Requires:	%{libname} = %{version}
Group:		Networking/File transfer
Requires:	ipsvd
PreReq:		afterboot
Provides:	ftpserver

%description -n ftp-server-krb5
The ftp-server package provides an ftp server.

This version supports kerberos authentication.


%prep
%setup -q -a 25
%patch0 -p1 -b .banner
%patch1 -p1 -b .biarch-utmp
#%patch2 -p1 -b .newline
%patch3 -p1 -b .telnet
%patch4 -p1 -b .no-rpath
%patch5 -p1 -b .info-dir
%patch6 -p1 -b .large-file
%patch7 -p1 -b .ksu-path
%patch8 -p1 -b .ksu-access
%patch9 -p1 -b .pass-by-address
#%patch10 -p1 -b .rlogind-environ
#%patch11 -p1 -b .ktany
%patch12 -p1 -b .ftp-glob
#%patch13 -p1 -b .varargs
#%patch14 -p1 -b .server-sort
#%patch15 -p1 -b .null
%patch16 -p1 -b .efence
%patch17 -p1 -b .rcp-sendlarge
%patch21 -p1 -b .can-2004-0175
%patch22 -p1 -b .api_crash
%patch23 -p1 -b .double_close
%patch24 -p1 -b .can-2005-0488
%patch25 -p1 -b .gethostbyname_r
%patch26 -p1 -b .et-preserve-file-names
%patch27 -p1 -b .lfs

find . -type f -name "*.fixinfo" -exec rm -fv "{}" ";"
gzip doc/*.ps

find -name "*\.h" | xargs perl -pi -e 's|\<com_err|\<et/com_err|';
find -name "*\.h" | xargs perl -pi -e 's|\"com_err|\"et/com_err|';


%build
export CFLAGS=-I/usr/include/et 
find . -name "*.[ch]"|xargs grep -r -l "^extern int errno;" * | xargs perl -p -i -e "s|^extern int errno;|#include <errno.h>|"
find . -name "*.[ch]"|xargs grep -r -l "extern int errno;" * | xargs perl -p -i -e "s|^extern int errno;||"

cd src
%{?__cputoolize: %{__cputoolize} -c config}

# Can't use %%configure because we don't use the default mandir.
#--with-ccopts="$RPM_OPT_FLAGS $ARCH_OPT_FLAGS -fPIC" \
LDCOMBINE_TAIL="-lc"; export LDCOMBINE_TAIL
DEFINES="-D_FILE_OFFSET_BITS=64" ; export DEFINES
# res_search is #define's as __res_search thus failing the name lookup
# in libresolv. Should make a clean patch to *.m4 so that <resolv.h>
# is #include'd prior to checking for that symbol
# CFLAGS=="$RPM_OPT_FLAGS $ARCH_OPT_FLAGS $DEFINES -fPIC" \
env ac_cv_lib_resolv_res_search=yes ./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{buildroot}%{_mandir} \
    --localstatedir=%{_sysconfdir}/kerberos \
    --without-krb4 \
    --enable-dns-for-realm \
    --with-tcl=%{_prefix} \
    --with-system-et \
    --with-system-ss \
    --libexecdir=%{_libdir} \
    --libdir=%{_libdir} \
    --enable-shared   \
    --enable-static  

# some rpath cleanups
find . -name Makefile | xargs perl -p -i -e 's@-Wl,-rpath -Wl,\$\(PROG_RPATH\)+@@';
find . -name Makefile | xargs perl -p -i -e 's@PROG_RPATH\=\$\(KRB5_LIBDIR\)+@PROG_RPATH\=@';
find . -name Makefile | xargs perl -p -i -e 's/TCL_RPATH\s+\=\s+\@TCL_RPATH\@+/TCL_RPATH\=/';
find . -name Makefile | xargs perl -p -i -e 's/PROG_RPATH\s+\=\s+\$\(TCL_RPATH\)+/TCL_RPATH\=/';
find . -name Makefile | xargs perl -p -i -e 's/\@SHLIB_RPATH_DIRS\@+//';
find . -name Makefile | xargs perl -p -i -e "s@ %{_libdir}@ %{buildroot}%{_libdir}@";
%make RPATH_FLAG= PROG_RPATH= LDCOMBINE='%{__cc} -shared -Wl,-soname=lib$(LIB)$(SHLIBSEXT) $(CFLAGS)'

# Run the test suite.  Won't run in the build system because /dev/pts is
# not available for telnet tests and so on.
# make check TMPDIR=%{_buildroot}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Our shell scripts.
mkdir -p %{buildroot}%{_bindir}
cat %{SOURCE11} > %{buildroot}%{_bindir}/krsh
cat %{SOURCE12} > %{buildroot}%{_bindir}/krlogin

# Extra headers.
mkdir -p %{buildroot}%{_includedir}
pushd src/include
    find kadm5 krb5 gssrpc gssapi -name "*.h" | cpio -pdm  %{buildroot}%{_includedir}
popd
perl -pi -e 's#k5-int#krb5/kdb#g' %{buildroot}%{_includedir}/kadm5/admin.h
find %{buildroot}%{_includedir} -type d | xargs chmod 0755
find %{buildroot}%{_includedir} -type f | xargs chmod 0644

# logdir
mkdir -p %{buildroot}/var/log/kerberos

# Info docs.
mkdir -p %{buildroot}%{_infodir}
install -m 644 doc/*.info* %{buildroot}%{_infodir}/
rm -f %{buildroot}%{_infodir}/krb425.info*

# KDC config files.
mkdir -p %{buildroot}%{_sysconfdir}/kerberos/krb5kdc
cat %{SOURCE9} > %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kdc.conf
cat %{SOURCE10} > %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kadm5.acl

# Client config files and scripts.
mkdir -p %{buildroot}%{_sysconfdir}
cat %{SOURCE5} > %{buildroot}/%{_sysconfdir}/krb5.conf

# KDC init script.
mkdir -p %{buildroot}%{_sbindir}
cat %{SOURCE8} > %{buildroot}%{_sbindir}/kdcrotate

# The rest of the binaries and libraries and docs.
pushd src
find . -name Makefile | xargs perl -p -i -e "s@ %{_libdir}@ %{buildroot}%{_libdir}@";
make prefix=%{buildroot}%{_prefix} \
    localstatedir=%{buildroot}%{_sysconfdir}/kerberos \
    infodir=%{buildroot}%{_infodir} \
    libdir=%{buildroot}%{_libdir} install
popd

# Fixup strange shared library permissions.
chmod 0755 %{buildroot}%{_libdir}/*.so*

mkdir -p %{buildroot}%{_srvdir}/{ktelnet,kftp,kadmind,kpropd,krb5kdc}/log
install -m 0740 %{SOURCE27} %{buildroot}%{_srvdir}/ktelnet/run
install -m 0740 %{SOURCE28} %{buildroot}%{_srvdir}/ktelnet/log/run
install -m 0740 %{SOURCE29} %{buildroot}%{_srvdir}/kftp/run
install -m 0740 %{SOURCE30} %{buildroot}%{_srvdir}/kftp/log/run
install -m 0740 %{SOURCE31} %{buildroot}%{_srvdir}/kadmind/run
install -m 0740 %{SOURCE32} %{buildroot}%{_srvdir}/kadmind/log/run
install -m 0740 %{SOURCE33} %{buildroot}%{_srvdir}/kpropd/run
install -m 0740 %{SOURCE34} %{buildroot}%{_srvdir}/kpropd/log/run
install -m 0740 %{SOURCE35} %{buildroot}%{_srvdir}/krb5kdc/run
install -m 0740 %{SOURCE36} %{buildroot}%{_srvdir}/krb5kdc/log/run

mkdir -p %{buildroot}%{_srvdir}/{ktelnet,kftp}/{peers,env}
touch %{buildroot}%{_srvdir}/{ktelnet,kftp}/peers/0
chmod 0644 %{buildroot}%{_srvdir}/{ktelnet,kftp}/peers/0
echo "21" >%{buildroot}%{_srvdir}/kftp/env/PORT
echo "23" >%{buildroot}%{_srvdir}/ktelnet/env/PORT

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE39} %{buildroot}%{_datadir}/afterboot/08_kftp
install -m 0644 %{SOURCE40} %{buildroot}%{_datadir}/afterboot/08_ktelnet

cat %{SOURCE23} > %{_builddir}/%{name}-%{version}/doc/Mandrake-Kerberos-HOWTO.html

find %{buildroot} -name "*\.h" | xargs perl -p -i -e "s|\<com_err|\<et/com_err|";
find %{buildroot} -name "*\.h" | xargs perl -p -i -e "s|\"com_err|\"et/com_err|";

find %{_builddir}/%{name}-%{version} -name "*\.h" | xargs perl -p -i -e "s|\<com_err|\<et/com_err|";
find %{_builddir}/%{name}-%{version} -name "*\.h" | xargs perl -p -i -e "s|\"com_err|\"et/com_err|";

# strip rpath
chrpath -d %{buildroot}%{_libdir}/*so*
strip %{buildroot}%{_bindir}/{ksu,v4rcp}

# dump un-FHS examples location (files included in doc list now)
rm -Rf %{buildroot}/%{_datadir}/examples

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/krb5-config
%multiarch_includes %{buildroot}%{_includedir}/gssapi/gssapi.h
# (gb) this one could be fixed differently and properly using <stdint.h>
%multiarch_includes %{buildroot}%{_includedir}/gssrpc/types.h
# multiarch_includes %{buildroot}%{_includedir}/krb5/k5-config.h
%multiarch_includes %{buildroot}%{_includedir}/krb5/autoconf.h
%multiarch_includes %{buildroot}%{_includedir}/krb5/osconf.h
%multiarch_includes %{buildroot}%{_includedir}/krb5.h

rm -rf %{buildroot}%{_includedir}/kerberosIV

pushd %{buildroot}/var
    ln -s ..%{_sysconfdir}/kerberos .
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post server
for i in kadmind kpropd krb5kdc
do
    if [ -d /var/log/supervise/$i -a ! -d /var/log/service/$i ]; then
        mv /var/log/supervise/$i /var/log/service/
    fi
done
%_post_srv kadmind
%_post_srv kpropd
%_post_srv krb5kdc

# Install info pages.
%_install_info krb5-admin.info
%_install_info krb5-install.info

%preun server
%_preun_srv kadmind
%_preun_srv kpropd
%_preun_srv krb5kdc
%_remove_install_info krb5-admin.info
%_remove_install_info krb5-install.info


%post workstation
%_install_info krb5-user.info

%preun workstation
%_remove_install_info krb5-user.info


%post -n telnet-server-krb5
if [ -d /var/log/supervise/ktelnet -a ! -d /var/log/service/ktelnet ]; then
    mv /var/log/supervise/ktelnet /var/log/service/
fi
%_post_srv ktelnet
%_mkafterboot
pushd %{_srvdir}/ktelnet >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd >/dev/null 2>&1


%preun -n telnet-server-krb5
%_preun_srv ktelnet

%postun -n telnet-server-krb5
%_mkafterboot


%post -n ftp-server-krb5
if [ -d /var/log/supervise/kftp -a ! -d /var/log/service/kftp ]; then
    mv /var/log/supervise/kftp /var/log/service/
fi
%_post_srv kftp
%_mkafterboot
pushd %{_srvdir}/kftp >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd >/dev/null 2>&1

%preun -n ftp-server-krb5
%_preun_srv kftp

%postun -n ftp-server-krb5
%_mkafterboot


%files workstation
%defattr(-,root,root)
%doc doc/*.html doc/user*.ps.gz src/config-files/services.append src/config-files/krb5.conf
%attr(0755,root,root) %doc src/config-files/convert-config-files
%{_infodir}/krb5-user.info*
%{_bindir}/gss-client
%{_bindir}/kdestroy
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kerberos.1*
%{_bindir}/kinit
%{_mandir}/man1/kinit.1*
%{_bindir}/klist
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd
%{_mandir}/man1/kpasswd.1*
%{_sbindir}/kadmin
%{_mandir}/man8/kadmin.8*
%{_sbindir}/ktutil
%{_mandir}/man8/ktutil.8*
%attr(0755,root,root) %{_bindir}/ksu
%{_mandir}/man1/ksu.1*
%{_bindir}/kvno
%{_mandir}/man1/kvno.1*
%{_bindir}/rcp
%{_mandir}/man1/rcp.1*
%attr(0755,root,root) %{_bindir}/krlogin
%{_bindir}/rlogin
%{_mandir}/man1/rlogin.1*
%attr(0755,root,root) %{_bindir}/krsh
%{_bindir}/rsh
%{_mandir}/man1/rsh.1*
%{_mandir}/man1/tmac.doc*
#%{_bindir}/v5passwd
#%{_mandir}/man1/v5passwd.1*
%{_bindir}/sim_client
%{_bindir}/uuclient
%{_sbindir}/login.krb5
%{_mandir}/man8/login.krb5.8*
%{_sbindir}/gss-server
%{_sbindir}/klogind
%{_mandir}/man8/klogind.8*
%{_sbindir}/krb5-send-pr
%{_mandir}/man1/krb5-send-pr.1*
%{_sbindir}/kshd
%{_mandir}/man8/kshd.8*
%{_sbindir}/uuserver
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/krb5.conf.5*


%files server
%defattr(-,root,root)
%doc src/config-files/kdc.conf
/var/kerberos
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kdc.conf
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kadm5.acl
%dir %attr(0750,root,admin) %{_srvdir}/kadmind
%dir %attr(0750,root,admin) %{_srvdir}/kadmind/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/kadmind/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/kadmind/log/run
%dir %attr(0750,root,admin) %{_srvdir}/kpropd
%dir %attr(0750,root,admin) %{_srvdir}/kpropd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/kpropd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/kpropd/log/run
%dir %attr(0750,root,admin) %{_srvdir}/krb5kdc
%dir %attr(0750,root,admin) %{_srvdir}/krb5kdc/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/krb5kdc/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/krb5kdc/log/run
%{_infodir}/krb5-admin.info*
%{_infodir}/krb5-install.info*
%dir /var/log/kerberos
%dir %{_sysconfdir}/kerberos/krb5kdc 
%{_mandir}/man5/kdc.conf.5*
%{_sbindir}/kadmin.local
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kdb5_util
%{_mandir}/man8/kdb5_util.8*
%{_sbindir}/kprop
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_mandir}/man8/kpropd.8*
%{_sbindir}/krb5kdc
%{_mandir}/man8/k5srvutil.8*
%{_sbindir}/k5srvutil
%{_mandir}/man8/krb5kdc.8*
%{_sbindir}/sim_server
#%{_sbindir}/v5passwdd
# This is here for people who want to test their server, and also 
# included in devel package for similar reasons.
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*
%attr(0755,root,root) %{_sbindir}/kdcrotate
%{_datadir}/gnats/mit


%files -n %{libname}
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/krb5.conf
%{_libdir}/lib*.so.*


%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/api
%doc doc/implement
%doc doc/kadm5
%doc doc/kadmin
%doc doc/krb5-protocol
%doc doc/rpc
%{_bindir}/krb5-config
%{_bindir}/sclient
%{_sbindir}/sserver
%multiarch %{multiarch_bindir}/krb5-config
%multiarch %{multiarch_includedir}/gssapi/gssapi.h
%multiarch %{multiarch_includedir}/gssrpc/types.h
# multiarch %{multiarch_includedir}/krb5/k5-config.h
%multiarch %{multiarch_includedir}/krb5/autoconf.h
%multiarch %{multiarch_includedir}/krb5/osconf.h
%multiarch %{multiarch_includedir}/krb5.h
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/*.a
%{_mandir}/man1/krb5-config.1*
%{_mandir}/man1/sclient.1*
%{_mandir}/man8/sserver.8*


%files -n telnet-server-krb5
%defattr(-,root,root)
%{_sbindir}/telnetd
%{_mandir}/man8/telnetd.8*
%dir %attr(0750,root,admin) %{_srvdir}/ktelnet
%dir %attr(0750,root,admin) %{_srvdir}/ktelnet/log
%dir %attr(0750,root,admin) %{_srvdir}/ktelnet/peers
%dir %attr(0750,root,admin) %{_srvdir}/ktelnet/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ktelnet/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ktelnet/log/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/ktelnet/env/PORT
%config(noreplace) %{_srvdir}/ktelnet/peers/0
%{_datadir}/afterboot/08_ktelnet


%files -n telnet-client-krb5
%defattr(-,root,root)
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*


%files -n ftp-client-krb5
%defattr(-,root,root)
%{_bindir}/ftp
%{_mandir}/man1/ftp.1*


%files -n ftp-server-krb5
%defattr(-,root,root)
%{_sbindir}/ftpd
%{_mandir}/man8/ftpd.8*
%dir %attr(0750,root,admin) %{_srvdir}/kftp
%dir %attr(0750,root,admin) %{_srvdir}/kftp/log
%dir %attr(0750,root,admin) %{_srvdir}/kftp/peers
%dir %attr(0750,root,admin) %{_srvdir}/kftp/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/kftp/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/kftp/log/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/kftp/env/PORT
%config(noreplace) %{_srvdir}/kftp/peers/0
%{_datadir}/afterboot/08_kftp


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-3avx
- env dirs and execline runscripts for ktelnet, kftp
- execline runscripts for kpropd and krb5kdc
- fix the chrpath call
- telnet-server-krb5 requires krb5-workstation (for login.krb5)

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-2avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2-1avx
- 1.4.2
- drop support for krb4 compatibility; including krb524 run scripts
- P25: from fedora
- P26: preserve filenames when generating files from *.et (multiarch
  fixes) (gbeauchesne)
- P27: large file support for FTP
- use correct ./configure option to enable dns realm lookup (andreas)
- drop P13, P18, P19, P20: merged upstream
- drop P2, P10, P11: conflicts
- drop P14: some conflicts, some upstream
- drop P15: original source gone
- drop S1, S2, S3, S4, S18: we don't use initscripts
- multiarch support
- use execlineb for run scripts
- move logdir to /var/log/service/k*
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-8avx
- fix perms on run scripts

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-7avx
- bootstrap build (new gcc, new glibc)

* Thu Jul 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-6avx
- P19, P20: security fix for CAN-2005-1174, CAN-2005-1175, CAN-2005-1689
- P21: security fix for CAN-2004-0175 (port of fixes to krb5-aware rcp)
- P22: keep apps which call krb5_principal_compare() or krb5_realm_compare() with
  malformed or NULL principal structures from crashing outright (Thomas Biege)
- P23: fix double-close in keytab handling (Nalin Dahyabhai)
- P24: security fix for CAN-2005-0488 (telnet client environment variable disclosure)
- add symlink of /var/kerberos to /etc/kerberos
- add symlink of /etc/krb5.keytab to /etc/kerberos/krb5kdc/kadm5.keytab since krb5 actually
  uses it by default rather than what we have tucked away
- add empty kadm5.keytab file
- drop S6 and S7; all they did was set the PATH to include /usr/bin and /usr/sbin (if
  root) which doesn't make sense and seems stupid and redundant
- update configs to s/MANDRAKESOFT.COM/ANNVIX.ORG/

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-5avx
- bootstrap build

* Tue Mar 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-4avx
- P18: security fix for MITKRB5-SA-2005-001 (CAN-2005-0469 and
  CAN-2005-0468)

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-3avx
- logger for krb5kdc

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-2avx
- user logger for logging

* Wed Dec 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.6-1avx
- 1.3.6
- drop P18 and P19 (merged upstream)

* Fri Oct 08 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.4-3avx
- switch from tcpserver to tcpsvd
- Requires: ipsvd
- add the /service/{kftp,ktelnet}/peers directories to, by default,
  allow all connections
- add afterboot snippet

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.4-2avx
- update run scripts
- fix kftp/ktelnet log run scripts for log directory location

* Sat Sep 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.4-1avx
- 1.3.4
- move krb5-config to devel package (abel)
- remove P4, fixed upstream
- P4: don't output any rpath-related flags to krb5-config (abel)
- massive spec cleanups  
- enable static devel libs (oden)
- include security fixes for CAN-2004-0642, CAN-2004-0643,
  CAN-2004-0644, CAN-2004-0772
- P5-P17: misc patches from Fedora
- P18, P19: security fixes for CAN-2004-0642, CAN-2004-0643,
  CAN-2004-0644, CAN-2004-0772

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3-9avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 1.3-8sls
- remove all un-applied patches; renumber patches
- P4: fix for MITKRB5-SA-2004-001

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.3-7sls
- minor spec cleanups

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 1.3-6sls
- supervise macros
- remove %%build_opensls macros
- rename supervise files: telnet -> ktelnet, ftp -> kftp
- remove postscript docs
- supervise scripts; remove initscripts

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.3-5sls
- supervise files; no xinetd
- don't include menu entries or icons

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 1.3-4sls
- OpenSLS build
- tidy spec
- remove prereq on rsh; doesn't seem to break anything and we definitely
  don't want rsh installed
- NOTE: need to figure out why we're not building this thing with any
  optflags (also preventing us from using -fstack-protector)

* Tue Sep 02 2003 Florin <florin@mandrakesoft.com> 1.3-3mdk
- replace <com_err.h> with <et/com_err.h> in the headers

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3-2mdk
- cputoolize
- Put back Patch27 (biarch-utmp)
- BuildRequires: libext2fs-devel

* Tue Jul 22 2003 Florin <florin@mandrakesoft.com> 1.3-1mdk
- 1.3
- libification for the krb5-libs package
- use the system err headers
- add telnet newline patch
- drop lost of useless patches
- add the post sections for ftp-server
- TODO: update some patches(if possible)

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.7-5mdk
- Rebuild
- Add patch51 fix compile thanks Gwenole Beauchesne

* Tue Jun  3 2003 Stefan van der Eijk <stefan@eijk.nu> 1.2.7-4mdk
- rebuild for rpm-4.2
- remove redundant BuildRequires

* Mon Apr  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.7-3mdk
- Patch27: Handle biarch struct utmp
- Patch28: Fix deps, I want parallel build

* Tue Apr 1 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.2.7-2mdk
- security fixes:
  - MITKRB5-SA-2003-003 (P50)
  - MITKRB5-SA-2003-005 (P51)
  - MITKRB5-SA-2003-004 (S25 and S26)

* Wed Jan 22 2003 Florin <florin@mandrakesoft.com> 1.2.7-1mdk
- 1.2.7
- remove patch 26 and 27

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.2.5-4mdk
- krb5-devel: provides/obsoletes krb-devel
- remove useless prefix
- requires s/shutils/coreutils/

* Wed Oct 30 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.5-3mdk
- Requires: words on krb5-server (re: stefan@eijk.nu)
- fix typo in kadmin initscript (re: stefan@eijk.nu)

* Tue Oct 29 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.2.5-2mdk
- P28: fix remote root hole in kadm4

* Thu Aug 29 2002 Florin <florin@mandrakesoft.com> 1.2.5-1mdk
- 1.2.5
- add db2-configure and xdr_array patches
- add the krb5-%{version}.tar.gz.asc and main source in gz format

* Tue Jul  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.4-3mdk
- Patch28: Correctly search for tclConfig.sh
- Patch27: Build libdb.a with PIC code on the appropriate arches since
  they turn out to be linked into shared objects
- res_search is #define's as __res_search and then fails to be found
  as is in libresolv. Should make a clean patch to *.m4 so that
  <resolv.h> is #include'd prior to checking for that symbol

* Mon Jun 17 2002 Florin <florin@mandrakesoft.com> 1.2.4-2mdk
- recompile against the matest gcc
- add some error messages in kadmind init script (thx to  V.A. Brennen)

* Mon Apr 08 2002 Florin <florin@mandrakesoft.com> 1.2.4-1mdk
- 1.2.4
- keep only the enable dns option (remove the netlib option)

* Tue Mar 05 2002 Florin <florin@mandrakesoft.com> 1.2.2-17mdk
- do not use authentication as default for the ftpd server

* Fri Jan 11 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.2-16mdk
- Don't print a whole load of system information in telnet.

* Wed Oct 17 2001 Florin <florin@mandrakesoft.com> 1.2.2-15mdk
- don't use LOG_AUTH as an option value when calling openlog() in ksu (#45965)
- add the fix buffer overflow telnetd patch
- better initscripts (use variables and add reload entries)
- fix telnet client (remove the 8 bit telnet patch)
- add patch to support "ANY" keytab type 
(i.e.,"default_keytab_name = ANY:FILE:/etc/krb5.keytab,
SRVTAB:/etc/srvtab" patch from Gerald Britton, #42551)
- build with -D_FILE_OFFSET_BITS=64 to get large file I/O in ftpd (#30697)
- patch ftpd to use long long and %%lld format specifiers to 
support the SIZE command on large files (also #30697)
- clean patches

* Wed Oct 10 2001 Stefan van der Eijk <stefan@eijk.nu> 1.2.2-14mdk
- BuildRequires: cpio

* Sun Sep 30 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.2-13mdk
- Make use of [[:space:]] in scriptlets of telnet-server-krb5.

* Thu Sep 27 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.2.2-12mdk
- In %post of telnet daemon make it so that we start the correct daemon
  and with our default authentication mode if no authentication mode
  is specified whenever we are doing upgrades with a modified 
  /etc/xinetd.d/telnet configuration file (Very obscure bug).
  
* Fri Sep 21 2001 Florin <florin@mandrakesoft.com> 1.2.2-11mdk
- oh, this krb5.csh again (thanks again Konrad Bernloehr)

* Thu Sep 20 2001 Florin <florin@mandrakesoft.com> 1.2.2-10mdk
- fix the /etc/profile.d/krb5.csh

* Wed Sep 12 2001 Florin <florin@mandrakesoft.com> 1.2.2-9mdk
- add krb5-1.2.2-telnet-8bit.patch.bz2 (thx to G.Lee)

* Wed Aug 29 2001 Florin <florin@mandrakesoft.com> 1.2.2-8mdk
- fix the /etc/profile.d/krb5.csh
(thx to Konrad Bernloehr for pointing this out)
- remove the e2fsprogs-devel from BuildPrereq

* Fri Aug 24 2001 Florin <florin@mandrakesoft.com> 1.2.2-7mdk
- s/valid/none for the telnet-server xinetd.d/telnet file
- create /usr/sbin/login.krb5 in post for telnet-server-krb5
- s/-a// for the ftp-server xinetd.d/ftp file
- fix perms for kdcrotate 

* Thu Aug 09 2001 Florin <florin@mandrakesoft.com> 1.2.2-6mdk
- fix the rpmlint rpath error 

* Wed Aug 08 2001 Florin <florin@mandrakesoft.com> 1.2.2-5mdk
- fix the krb5.conf and the kdc.conf sources
- add the Mandrake-Kerberos-HOWTO.html
- move the kdcrotate script to %{_sbindir} in server
- get rid of BUILD_SOURCE_DIR
- bzip all the sources

* Mon Aug 06 2001 Florin <florin@mandrakesoft.com> 1.2.2-4mdk
- add the telnet*xpm sources and {telnet,ftp} xinetd files 
- generate also the {telnet,ftp}-{server,client}-krb5 packages
- fix the krb5.conf entry in the kdcrotate initscript
- fix the kpropd and the krb5server initscript

* Fri Aug 03 2001 Florin <florin@mandrakesoft.com> 1.2.2-3mdk
- modify the krb5server initscript
- add a working configuration: update krb5.conf, krbkdc.conf 
- add the /var/log/kerberos dir

* Tue Jul 31 2001 Florin <florin@mandrakesoft.com> 1.2.2-2mdk
- krb5.conf needs to go under sysconfdir obviously
- add the *.h files in devel (I have forgotten them, oups)

* Tue Jul 3 2001 Florin <florin@mandrakesoft.com> 1.2.2-1mdk
- mandrake adaptions

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- pass some structures by address instead of on the stack in krb5kdc

* Tue May 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Apr 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch from Tom Yu to fix ftpd overflows

* Wed Apr 18 2001 Than Ngo <than@redhat.com>
- disable optimizations on the alpha again

* Fri Mar 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in glue code to make sure that libkrb5 continues to provide a
  weak copy of stat()

* Thu Mar 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- build alpha with -O0 for now

* Thu Mar  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix the kpropd init script

* Mon Mar  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.2, which fixes some bugs relating to empty ETYPE-INFO
- re-enable optimization on Alpha

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- build alpha with -O0 for now
- own %{_var}/kerberos

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- own the directories which are created for each package (#26342)

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize init scripts

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- add some comments to the ksu patches for the curious
- re-enable optimization on alphas

* Mon Jan 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix krb5-send-pr (#18932) and move it from -server to -workstation
- buildprereq libtermcap-devel
- temporariliy disable optimization on alphas
- gettextize init scripts

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- force -fPIC

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add bison as a BuildPrereq (#20091)

* Mon Oct 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- change /usr/dict/words to /usr/share/dict/words in default kdc.conf (#20000)

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply kpasswd bug fixes from David Wragg

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- make krb5-libs obsolete the old krb5-configs package (#18351)
- don't quit from the kpropd init script if there's no principal database so
  that you can propagate the first time without running kpropd manually
- don't complain if /etc/ld.so.conf doesn't exist in the -libs %post

* Tue Sep 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix credential forwarding problem in klogind (goof in KRB5CCNAME handling)
  (#11588)
- fix heap corruption bug in FTP client (#14301)

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix summaries and descriptions
- switched the default transfer protocol from PORT to PASV as proposed on
  bugzilla (#16134), and to match the regular ftp package's behavior

* Wed Jul 19 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Fri Jul 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable servers by default to keep linuxconf from thinking they need to be
  started when they don't

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- change cleanup code in post to not tickle chkconfig
- add grep as a Prereq: for -libs

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- move condrestarts to postun
- make xinetd configs noreplace
- add descriptions to xinetd configs
- add /etc/init.d as a prereq for the -server package
- patch to properly truncate $TERM in krlogind

* Fri Jun 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.1
- back out Tom Yu's patch, which is a big chunk of the 1.2 -> 1.2.1 update
- start using the official source tarball instead of its contents

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Tom Yu's patch to fix compatibility between 1.2 kadmin and 1.1.1 kadmind
- pull out 6.2 options in the spec file (sonames changing in 1.2 means it's not
  compatible with other stuff in 6.2, so no need)

* Wed Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak graceful start/stop logic in post and preun

* Mon Jun 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to the 1.2 release
- ditch a lot of our patches which went upstream
- enable use of DNS to look up things at build-time
- disable use of DNS to look up things at run-time in default krb5.conf
- change ownership of the convert-config-files script to root.root
- compress PS docs
- fix some typos in the kinit man page
- run condrestart in server post, and shut down in preun

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- only remove old krb5server init script links if the init script is there

* Sat Jun 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable kshell and eklogin by default

* Thu Jun 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch mkdir/rmdir problem in ftpcmd.y
- add condrestart option to init script
- split the server init script into three pieces and add one for kpropd

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure workstation servers are all disabled by default
- clean up krb5server init script

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply second set of buffer overflow fixes from Tom Yu
- fix from Dirk Husung for a bug in buffer cleanups in the test suite
- work around possibly broken rev binary in running test suite
- move default realm configs from /var/kerberos to %{_var}/kerberos

* Tue Jun  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- make ksu and v4rcp owned by root

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- use %%{_infodir} to better comply with FHS
- move .so files to -devel subpackage
- tweak xinetd config files (bugs #11833, #11835, #11836, #11840)
- fix package descriptions again

* Wed May 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- change a LINE_MAX to 1024, fix from Ken Raeburn
- add fix for login vulnerability in case anyone rebuilds without krb4 compat
- add tweaks for byte-swapping macros in krb.h, also from Ken
- add xinetd config files
- make rsh and rlogin quieter
- build with debug to fix credential forwarding
- add rsh as a build-time req because the configure scripts look for it to
  determine paths

* Wed May 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix config_subpackage logic

* Tue May 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove setuid bit on v4rcp and ksu in case the checks previously added
  don't close all of the problems in ksu
- apply patches from Jeffrey Schiller to fix overruns Chris Evans found
- reintroduce configs subpackage for use in the errata
- add PreReq: sh-utils

* Mon May 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix double-free in the kdc (patch merged into MIT tree)
- include convert-config-files script as a documentation file

* Wed May 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch ksu man page because the -C option never works
- add access() checks and disable debug mode in ksu
- modify default ksu build arguments to specify more directories in CMD_PATH
  and to use getusershell()

* Wed May 03 2000 Bill Nottingham <notting@redhat.com>
- fix configure stuff for ia64

* Mon Apr 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- add LDCOMBINE=-lc to configure invocation to use libc versioning (bug #10653)
- change Requires: for/in subpackages to include %{version}

* Wed Apr 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- add man pages for kerberos(1), kvno(1), .k5login(5)
- add kvno to -workstation

* Mon Apr 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge krb5-configs back into krb5-libs.  The krb5.conf file is marked as
  a %%config file anyway.
- Make krb5.conf a noreplace config file.

* Thu Mar 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- Make klogind pass a clean environment to children, like NetKit's rlogind does.

* Wed Mar 08 2000 Nalin Dahyabhai <nalin@redhat.com>
- Don't enable the server by default.
- Compress info pages.
- Add defaults for the PAM module to krb5.conf

* Mon Mar 06 2000 Nalin Dahyabhai <nalin@redhat.com>
- Correct copyright: it's exportable now, provided the proper paperwork is
  filed with the government.

* Fri Mar 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply Mike Friedman's patch to fix format string problems
- don't strip off argv[0] when invoking regular rsh/rlogin

* Thu Mar 02 2000 Nalin Dahyabhai <nalin@redhat.com>
- run kadmin.local correctly at startup

* Mon Feb 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- pass absolute path to kadm5.keytab if/when extracting keys at startup

* Sat Feb 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix info page insertions

* Wed Feb  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak server init script to automatically extract kadm5 keys if
  /var/kerberos/krb5kdc/kadm5.keytab doesn't exist yet
- adjust package descriptions

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix for potentially gzipped man pages

* Fri Jan 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix comments in krb5-configs

* Fri Jan  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- move /usr/kerberos/bin to end of PATH

* Tue Dec 28 1999 Nalin Dahyabhai <nalin@redhat.com>
- install kadmin header files

* Tue Dec 21 1999 Nalin Dahyabhai <nalin@redhat.com>
- patch around TIOCGTLC defined on alpha and remove warnings from libpty.h
- add installation of info docs
- remove krb4 compat patch because it doesn't fix workstation-side servers

* Mon Dec 20 1999 Nalin Dahyabhai <nalin@redhat.com>
- remove hesiod dependency at build-time

* Sun Dec 19 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- rebuild on 1.1.1

* Thu Oct  7 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- clean up init script for server, verify that it works [jlkatz]
- clean up rotation script so that rc likes it better
- add clean stanza

* Mon Oct  4 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- backed out ncurses and makeshlib patches
- update for krb5-1.1
- add KDC rotation to rc.boot, based on ideas from Michael's C version

* Mon Sep 26 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- added -lncurses to telnet and telnetd makefiles

* Mon Jul  5 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- added krb5.csh and krb5.sh to /etc/profile.d

* Mon Jun 22 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- broke out configuration files

* Mon Jun 14 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- fixed server package so that it works now

* Sat May 15 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- started changelog
- updated existing 1.0.5 RPM from Eos Linux to krb5 1.0.6
- added --force to makeinfo commands to skip errors during build

