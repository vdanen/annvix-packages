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
%define version		1.5.1
%define release		%_revrel

%define major		3
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d
%define odevname	%mklibname %{name} 3 -d

Summary:	The Kerberos network authentication system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://web.mit.edu/kerberos/www/
# from http://web.mit.edu/kerberos/dist/krb5/1.4/krb5-%{version}-signed.tar
Source0:	%{name}-%{version}.tar.gz
Source1:	krb5.conf
Source2:	kdcrotate
Source3:	kdc.conf
Source4:	kadm5.acl
Source5:	krsh
Source6:	krlogin
Source7:	statglue.c
Source8:	Mandrake-Kerberos-HOWTO.html
Source9:	%{name}-%{version}.tar.gz.asc
Source10:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.tar.gz
Source11:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.sig
Source12:	ktelnet.run
Source13:	ktelnet-log.run
Source14:	kftp.run
Source15:	kftp-log.run
Source16:	kadmind.run
Source17:	kadmind-log.run
Source18:	kpropd.run
Source19:	kpropd-log.run
Source20:	krb5kdc.run
Source21:	krb5kdc-log.run
Source22:	08_kftp.afterboot
Source23:	08_ktelnet.afterboot
Patch0:		krb5-1.2.2-telnetbanner.patch
Patch1:		krb5-1.2.5-biarch-utmp.patch
Patch3:		krb5-1.3-mdk-no-rpath.patch
Patch5:		krb5-1.3-fdr-large-file.patch
Patch6:		krb5-1.5.1-mdv-ksu-path.patch
Patch7:		krb5-1.3-fdr-ksu-access.patch
Patch8:		krb5-1.3-fdr-pass-by-address.patch

Patch9:		krb5-1.3-fdr-ftp-glob.patch
Patch11:	krb5-1.3.3-fdr-rcp-sendlarge.patch
# (gb) preserve file names when generating files from *.et (multiarch fixes)
Patch17:	krb5-1.3.6-et-preserve-file-names.patch
# http://qa.mandriva.com/show_bug.cgi?id=9410
Patch18:	krb5-1.4.1-ftplfs.patch
Patch19:	2006-002-patch.txt
Patch20:	2006-003-patch.txt
Patch21:        http://web.mit.edu/kerberos/advisories/2007-001-patch.txt
Patch22:        http://web.mit.edu/kerberos/advisories/2007-002-patch.txt
Patch23:        http://web.mit.edu/kerberos/advisories/2007-003-patch.txt
Patch24:	krb5-1.5-MITKRB5-SA-2007-004.patch
Patch25:	krb5-1.5-MITKRB5-SA-2007-005.patch
Patch26:	krb5-1.5.2-CVE-2007-3999_4000.patch
Patch27:	krb5-1.5.2-CVE-2007-4743.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	termcap-devel
BuildRequires:	texinfo
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	chrpath
BuildRequires:	multiarch-utils >= 1.0.3

Requires(pre):	info-install

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.


%package -n %{devname}
Summary:	Development files needed for compiling Kerberos 5 programs
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{odevname}

%description -n %{devname}
Kerberos is a network authentication system.  The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you'll
need to install this package.


%package -n %{libname}
Summary:	The shared libraries used by Kerberos 5
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
Kerberos is a network authentication system.  The krb5-libs package
contains the shared libraries needed by Kerberos 5.  If you're using
Kerberos, you'll need to install this package.


%package server
Group:		System/Servers
Summary:	The server programs for Kerberos 5
Requires:	%{libname} = %{version}
Requires:	%{name}-workstation = %{version}
Requires:	words
Requires(pre):	install-info

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
Requires(pre):	install-info

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
Requires(pre):	afterboot
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires(preun): rpm-helper
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
Group:		Networking/Remote Access
Requires:	%{libname} = %{version}
Obsoletes:	telnet
Provides:	telnet
 
%description -n telnet-client-krb5
Telnet is a popular protocol for logging into remote systems over the Internet.
The telnet package provides a command line telnet client.

This version supports kerberos authentication.


%package -n ftp-client-krb5
Summary:	A ftp-client with kerberos support
Group:		Networking/File Transfer
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
Group:		System/Servers
Requires:	ipsvd
Requires(pre):	afterboot
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires(preun): rpm-helper
Provides:	ftpserver

%description -n ftp-server-krb5
The ftp-server package provides an ftp server.

This version supports kerberos authentication.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 10
%patch0 -p1 -b .banner
%patch1 -p1 -b .biarch-utmp
%patch3 -p1 -b .no-rpath
%patch5 -p1 -b .large-file
%patch6 -p1 -b .ksu-path
%patch7 -p1 -b .ksu-access
%patch8 -p1 -b .pass-by-address
%patch9 -p1 -b .ftp-glob
%patch11 -p1 -b .rcp-sendlarge
%patch17 -p1 -b .et-preserve-file-names
%patch18 -p1 -b .lfs
%patch19 -p0 -b .cve-2006-6143
%patch20 -p0 -b .cve-2006-6144
%patch21 -p0 -b .cve-2007-0956
%patch22 -p0 -b .cve-2007-0957
%patch23 -p0 -b .cve-2007-1216
%patch24 -p0 -b .cve-2007-2442_2443
%patch25 -p0 -b .cve-2007-2798
%patch26 -p1 -b .cve-2007-3999_4000
%patch27 -p1 -b .cve-2007-4743

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
    --disable-static  

# some rpath cleanups
find . -name Makefile | xargs perl -p -i -e 's@-Wl,-rpath -Wl,\$\(PROG_RPATH\)+@@';
find . -name Makefile | xargs perl -p -i -e 's@PROG_RPATH\=\$\(KRB5_LIBDIR\)+@PROG_RPATH\=@';
find . -name Makefile | xargs perl -p -i -e 's/TCL_RPATH\s+\=\s+\@TCL_RPATH\@+/TCL_RPATH\=/';
find . -name Makefile | xargs perl -p -i -e 's/PROG_RPATH\s+\=\s+\$\(TCL_RPATH\)+/TCL_RPATH\=/';
find . -name Makefile | xargs perl -p -i -e 's/\@SHLIB_RPATH_DIRS\@+//';
%make RPATH_FLAG= PROG_RPATH= LDCOMBINE='%{__cc} -shared -Wl,-soname=lib$(LIB)$(SHLIBSEXT) $(CFLAGS)'

# Run the test suite.  Won't run in the build system because /dev/pts is
# not available for telnet tests and so on.
# make check TMPDIR=%{_buildroot}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# Our shell scripts.
mkdir -p %{buildroot}%{_bindir}
cp %{_sourcedir}/krsh %{buildroot}%{_bindir}/krsh
cp %{_sourcedir}/krlogin %{buildroot}%{_bindir}/krlogin

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
cp %{_sourcedir}/kdc.conf %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kdc.conf
cp %{_sourcedir}/kadm5.acl %{buildroot}%{_sysconfdir}/kerberos/krb5kdc/kadm5.acl

# Client config files and scripts.
mkdir -p %{buildroot}%{_sysconfdir}
cp %{_sourcedir}/krb5.conf %{buildroot}/%{_sysconfdir}/krb5.conf

# KDC init script.
mkdir -p %{buildroot}%{_sbindir}
cp %{_sourcedir}/kdcrotate %{buildroot}%{_sbindir}/kdcrotate

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
install -m 0740 %{_sourcedir}/ktelnet.run %{buildroot}%{_srvdir}/ktelnet/run
install -m 0740 %{_sourcedir}/ktelnet-log.run %{buildroot}%{_srvdir}/ktelnet/log/run
install -m 0740 %{_sourcedir}/kftp.run %{buildroot}%{_srvdir}/kftp/run
install -m 0740 %{_sourcedir}/kftp-log.run %{buildroot}%{_srvdir}/kftp/log/run
install -m 0740 %{_sourcedir}/kadmind.run %{buildroot}%{_srvdir}/kadmind/run
install -m 0740 %{_sourcedir}/kadmind-log.run %{buildroot}%{_srvdir}/kadmind/log/run
install -m 0740 %{_sourcedir}/kpropd.run %{buildroot}%{_srvdir}/kpropd/run
install -m 0740 %{_sourcedir}/kpropd-log.run %{buildroot}%{_srvdir}/kpropd/log/run
install -m 0740 %{_sourcedir}/krb5kdc.run %{buildroot}%{_srvdir}/krb5kdc/run
install -m 0740 %{_sourcedir}/krb5kdc-log.run %{buildroot}%{_srvdir}/krb5kdc/log/run

mkdir -p %{buildroot}%{_srvdir}/{ktelnet,kftp}/{peers,env}
touch %{buildroot}%{_srvdir}/{ktelnet,kftp}/peers/0
chmod 0644 %{buildroot}%{_srvdir}/{ktelnet,kftp}/peers/0
echo "21" >%{buildroot}%{_srvdir}/kftp/env/PORT
echo "23" >%{buildroot}%{_srvdir}/ktelnet/env/PORT

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/08_kftp.afterboot %{buildroot}%{_datadir}/afterboot/08_kftp
install -m 0644 %{_sourcedir}/08_ktelnet.afterboot %{buildroot}%{_datadir}/afterboot/08_ktelnet

cp %{_sourcedir}/Mandrake-Kerberos-HOWTO.html %{_builddir}/%{name}-%{version}/doc/Mandrake-Kerberos-HOWTO.html

find %{buildroot} -name "*\.h" | xargs perl -p -i -e "s|\<com_err|\<et/com_err|";
find %{buildroot} -name "*\.h" | xargs perl -p -i -e "s|\"com_err|\"et/com_err|";

find %{_builddir}/%{name}-%{version} -name "*\.h" | xargs perl -p -i -e "s|\<com_err|\<et/com_err|";
find %{_builddir}/%{name}-%{version} -name "*\.h" | xargs perl -p -i -e "s|\"com_err|\"et/com_err|";

# strip rpath
chrpath -d %{buildroot}%{_libdir}/*so*
strip %{buildroot}%{_bindir}/ksu

# dump un-FHS examples location (files included in doc list now)
rm -Rf %{buildroot}/%{_datadir}/examples

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/krb5-config
%multiarch_includes %{buildroot}%{_includedir}/gssapi/gssapi.h
# (gb) this one could be fixed differently and properly using <stdint.h>
%multiarch_includes %{buildroot}%{_includedir}/gssrpc/types.h
# multiarch_includes %{buildroot}%{_includedir}/krb5/k5-config.h
# multiarch_includes %{buildroot}%{_includedir}/krb5/autoconf.h
# multiarch_includes %{buildroot}%{_includedir}/krb5/osconf.h
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
%_post_srv kadmind
%_post_srv kpropd
%_post_srv krb5kdc
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
%dir %{_libdir}/krb5/plugins/kdb
%{_libdir}/krb5/plugins/kdb/db2.so


%files -n %{libname}
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/krb5.conf
%{_libdir}/lib*.so.*
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins


%files -n %{devname}
%defattr(-,root,root)
%{_bindir}/krb5-config
%{_bindir}/sclient
%{_sbindir}/sserver
%multiarch %{multiarch_bindir}/krb5-config
%multiarch %{multiarch_includedir}/gssapi/gssapi.h
%multiarch %{multiarch_includedir}/gssrpc/types.h
# multiarch %{multiarch_includedir}/krb5/k5-config.h
# multiarch %{multiarch_includedir}/krb5/autoconf.h
# multiarch %{multiarch_includedir}/krb5/osconf.h
%multiarch %{multiarch_includedir}/krb5.h
%{_includedir}/*
%{_libdir}/lib*.so
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


%files doc
%defattr(-,root,root)
%doc README
%doc doc/*.html doc/user*.ps.gz src/config-files/services.append src/config-files/krb5.conf
%attr(0755,root,root) %doc src/config-files/convert-config-files
%doc src/config-files/kdc.conf
%doc doc/api doc/implement doc/kadm5 doc/kadmin doc/krb5-protocol doc/rpc


%changelog
* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- rebuild against new e2fsprogs
- update the buildreqs

* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- P26: security fix for CVE-2007-3999 and CVE-2007-4000
- P27: security fix for CVE-2007-4743 (the other half of CVE-2007-3999)
- v4rcp is no longer built, so it no longer needs to be stripped

* Fri Jul 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- P24: security fix for CVE-2007-2442 and CVE-2007-2443
- P25: security fix for CVE-2007-2798
- implement devel naming policy
- implement library provides policy
- clean up some provides/obsoletes

* Sat Apr 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- fix the tools looking for libs in the buildroot

* Thu Apr 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- fix typo in requires that prevents some installations
- by default, only allow valid (kerberized) authenticated logins and don't
  allow unencrypted logins (can be changed by modifying ktelnet's runscript)
- do the same for kftp as well (user cannot send password unencrypted and must
  have the credentials to use the resource; this also can be changed in kftp's
  runscript -- the rationale here is that for other FTP services, there are
  better alternatives so make this purely kerberos)

* Mon Apr 09 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- P21: security fix for CVE-2007-0956
- P22: security fix for CVE-2007-0957
- P23: security fix for CVE-2007-1216

* Wed Jan 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- P19: security fix for CVE-2006-6143
- P20: security fix for CVE-2006-6144

* Sat Dec 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- the library major is 3, not 1

* Sat Dec 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- revert the previous change or else libkrb51 will end up pulling in some
  other -devel packages

* Sat Dec 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- put libgssapi_krb5.so in the lib package, not the lib -devel package or
  else rpc.gssd won't run (and it's not acceptable to have to install the
  -devel package for a daemon to run)

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5.1
- 1.5.1
- drop P2, P4, P10, P12, P13, P14, P15, P16, P19, P20; merged
  upstream or no longer needed
- grabbed updated P1, P6, P18 from Mandriva
- rebuild against new tcl and adjust buildrequires
- fix some groups

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.3
- 1.4.3
- spec cleanups
- renumber patches and source files
- rebuild against new e2fsprogs
- P19: rebuild properly when pthread_mutexattr_setrobust_np() is defined but not
  declared, such as with recent glibc when _GNU_SOURCE isn't being used
- P20: patch to fix CVE-2006-3083

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.2
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
