%define name	krb5
%define version	1.3
%define release	5sls

%define srcver	1.3
%define LIBMAJ	1
%define libname	%mklibname %name %LIBMAJ
%define libnamedev %{libname}-devel

Summary:	The Kerberos network authentication system.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
URL:		http://web.mit.edu/kerberos/www/
Source0:	%{name}-%{version}.tar.gz
Source1:	kpropd.init.bz2
Source2:	krb524d.init.bz2
Source3:	kadmind.init.bz2
Source4:	krb5kdc.init.bz2
Source5:	krb5.conf.bz2
Source6:	krb5.sh.bz2
Source7:	krb5.csh.bz2
Source8:	kdcrotate.bz2
Source9:	kdc.conf.bz2
Source10:	kadm5.acl.bz2
Source11:	krsh.bz2
Source12:	krlogin.bz2
Source13:	eklogin.xinetd.bz2
Source14:	klogin.xinetd.bz2
Source15:	kshell.xinetd.bz2
Source16:	telnet-krb5.xinetd.bz2
Source17:	ftp-krb5.xinetd.bz2
Source18:	krb5server.init.bz2
Source19:	statglue.c.bz2
Source20:	telnet.16.xpm.bz2
Source21:	telnet.32.xpm.bz2
Source22:	telnet.48.xpm.bz2
Source23:	Mandrake-Kerberos-HOWTO.html.bz2
Source24:	%{name}-%{version}.tar.gz.asc
Source25:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.tar.gz
Source26:	http://web.mit.edu/kerberos/www/advisories/2003-004-krb4_patchkit.sig
Source27:	telnet.run
Source28:	telnet-log.run
Source29:	ftp.run
Source30:	ftp-log.run
Patch0:		krb5-1.1-db.patch.bz2
Patch1:		krb5-1.1.1-tiocgltc.patch.bz2
Patch2:		krb5-1.1.1-libpty.patch.bz2
Patch3:		krb5-1.1.1-fixinfo.patch.bz2
Patch4:		krb5-1.1.1-manpages.patch.bz2
Patch5:		krb5-1.1.1-netkitr.patch.bz2
Patch6:		krb5-1.2-rlogind.patch.bz2
Patch7:		krb5-1.2-ksu.patch.bz2
Patch8:		krb5-1.2-ksu.options.patch.bz2
Patch9:		krb5-1.2-ksu.man.patch.bz2
Patch10:	krb5-1.2-quiet.patch.bz2
Patch11:	krb5-1.1.1-brokenrev.patch.bz2
Patch12:	krb5-1.2-spelling.patch.bz2
Patch13:	krb5-1.2.1-term.patch.bz2
Patch14:	krb5-1.2.1-passive.patch.bz2
Patch15:	krb5-1.2.1-forward.patch.bz2
Patch16:	krb5-1.2.1-heap.patch.bz2
Patch17:	krb5-1.2.2-wragg.patch.bz2
Patch18:	krb5-1.2.2-statglue.patch.bz2
Patch19:	krb5-1.2.2-by-address.patch.bz2
Patch20:	http://lite.mit.edu/krb5-1.2.2-ktany.patch.bz2
Patch21:	krb5-1.2.2-logauth.patch.bz2
Patch22:	krb5-1.2.2-size.patch.bz2
Patch23:	krb5-1.2.5-db2-configure.patch.bz2
Patch24:	krb5-1.2.2-telnetbanner.patch.bz2
Patch25:	krb5-1.2.4-pic.patch.bz2
Patch26:	krb5-1.2.4-tcl-libs.patch.bz2
Patch27:	krb5-1.2.5-biarch-utmp.patch.bz2
Patch28:	krb5-1.2.7-deps.patch.bz2
Patch29:	krb5-1.2.7-namelength.patch
Patch30:	krb5-1.2.7-errno.patch
Patch31:	gssftp-patch
Patch32:	krb5-1.2.7-reject-bad-transited.patch
Patch33:	krb5-1.2.7-krb524d-double-free.patch
Patch34:	krb5-1.2.8-princ_access.patch
Patch35:	krb5-1.2.8-varargs.patch
Patch36:	krb5-1.3-newline.patch.bz2
Patch37:	krb5-1.3-telnet.patch.bz2
# security
Patch50:	http://web.mit.edu/kerberos/www/advisories/MITKRB5-SA-2003-003-xdr.txt
Patch51:	http://web.mit.edu/kerberos/www/advisories/MITKRB5-SA-2003-005-patch.txt

Patch52:	kbr5-fix-call-function.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildPrereq:	bison, flex, libtermcap-devel, texinfo, tcl
BuildRequires:	libext2fs-devel

PreReq:		grep, info, coreutils, /sbin/install-info

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.

%package -n %{libnamedev}
Summary:	Development files needed for compiling Kerberos 5 programs.
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	krb-devel krb5-devel
Obsoletes:	krb-devel krb5-devel

%description -n %{libnamedev}
Kerberos is a network authentication system.  The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you'll
need to install this package.

%package -n %{libname}
Summary:	The shared libraries used by Kerberos 5.
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
Summary:	The server programs for Kerberos 5.
Requires:	%{libname} = %{version}, %{name}-workstation = %{version}, words
Prereq:		grep, /sbin/install-info, /bin/sh, coreutils

%description server
Kerberos is a network authentication system.  The krb5-server package
contains the programs that must be installed on a Kerberos 5 server.
If you're installing a Kerberos 5 server, you need to install this
package (in other words, most people should NOT install this
package).

%package workstation
Summary:	Kerberos 5 programs for use on workstations.
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
%if %{build_opensls}
Requires:	ucspi-tcp
%else
Requires:	xinetd
%endif
Obsoletes:	telnet-server
Provides:	telnet-server

%description -n telnet-server-krb5
Telnet is a popular protocol for logging into remote systems over the Internet.
The telnet-server package provides a telnet daemon, which will support remote
logins into the host machine. The telnet daemon is enabled by default. You may
disable the telnet daemon by editing /etc/inetd.conf.

Install the telnet-server package if you want to support remote logins to your
machine.

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

Install the telnet package if you want to telnet to remote machines.

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

If your system is on a network, you should install ftp in order to do
file transfers.

This version supports kerberos authentication.

%package -n ftp-server-krb5
Summary:	A ftp-server with kerberos support
Requires:	%{libname} = %{version}
Group:		Networking/File transfer
Provides:	ftpserver

%description -n ftp-server-krb5
The ftp-server package provides an ftp server.

This version supports kerberos authentication.

%prep
%setup -q -a 25
#%patch0  -p0 -b .db
#%patch1  -p0 -b .tciogltc OK
#%patch2  -p0 -b .libpty	OK
#%patch3  -p0 -b .fixinfo
#%patch4  -p0 -b .manpages
#%patch5  -p0 -b .netkitr
#%patch6  -p1 -b .rlogind
#%patch7  -p1 -b .ksu
#%patch8 -p1 -b .ksu-options
#%patch9 -p1 -b .ksu-man
#%patch10 -p1 -b .quiet
#%patch11 -p1 -b .brokenrev OK
#%patch12 -p1 -b .spelling
#%patch13 -p1 -b .term		OK
#%patch14 -p1 -b .passive 	OK
#%patch15 -p1 -b .forward
#%patch16 -p1 -b .heap
#%patch17 -p1 -b .wragg
#%patch18 -p1 -b .statglue	OK
#%patch19 -p0 -b .by-address
#%patch20 -p1 -b .ktany
#%patch21 -p1 -b .logauth
#%patch22 -p1 -b .size
#%patch23 -p1 -b .db2-configure
%patch24 -p1 -b .banner
#%ifarch ia64 x86_64
#%patch25 -p1 -b .pic OK
#%endif
#%patch26 -p1 -b .tcl-libs
%patch27 -p1 -b .biarch-utmp
#%patch28 -p1 -b .deps
#%patch29 -p1 -b .namelength
#%patch30 -p1 -b .errno
#%patch31 -p1 -b .gssftp-patch
#%patch32 -p1 -b .reject-bad-transited.patch OK
#%patch33 -p1 -b .double-free OK
#%patch34 -p1 -b .princ_access
#%patch35 -p1 -b .varargs
%patch36 -p1 -b .newline
%patch37 -p1 -b .telnet

# security
#pushd src/lib/rpc
#%patch50 -p0 -b .2003-003
#popd
#pushd src
#patch -sp0 -b -z .2003-004-krb4 < ../2003-004-krb4_patchkit/patch.1.2.7
#%patch51 -p0 -b .2003-005
#popd

#%patch52 -p1 -b .fix.call.function

#bzcat %{SOURCE19} > src/util/profile/statglue.c
find . -type f -name "*.fixinfo" -exec rm -fv "{}" ";"
gzip doc/*.ps

%build
export CFLAGS=-I/usr/include/et 
find . -name "*.[ch]"|xargs grep -r -l "^extern int errno;" * | xargs perl -p -i -e "s|^extern int errno;|#include <errno.h>|"
find . -name "*.[ch]"|xargs grep -r -l "extern int errno;" * | xargs perl -p -i -e "s|^extern int errno;||"

cd src
#libtoolize --copy --force
#cp config.{guess,sub} config/
%{?__cputoolize: %{__cputoolize} -c config}

# Can't use %%configure because we don't use the default mandir.
#--with-ccopts="$RPM_OPT_FLAGS $ARCH_OPT_FLAGS -fPIC" \
LDCOMBINE_TAIL="-lc"; export LDCOMBINE_TAIL
DEFINES="-D_FILE_OFFSET_BITS=64" ; export DEFINES
# res_search is #define's as __res_search thus failing the name lookup
# in libresolv. Should make a clean patch to *.m4 so that <resolv.h>
# is #include'd prior to checking for that symbol
  #CFLAGS=="$RPM_OPT_FLAGS $ARCH_OPT_FLAGS $DEFINES -fPIC" \
env ac_cv_lib_resolv_res_search=yes ./configure \
	CC=%{__cc} \
	--prefix=%_prefix \
	--infodir=%{_infodir} \
	--mandir=$RPM_BUILD_ROOT%{_mandir} \
	--localstatedir=/etc/kerberos \
	--with-krb4 \
	--enable-dns \
	--with-tcl=%_prefix \
	--with-system-et \
	--with-system-ss \
	--libexecdir=%{_libdir} \
	--libdir=%{_libdir} \
	--enable-shared   \
	--disable-static  

#some rpath cleanups
find . -name Makefile | xargs perl -p -i -e 's@-Wl,-rpath -Wl,\$\(PROG_RPATH\)+@@';
find . -name Makefile | xargs perl -p -i -e 's@PROG_RPATH\=\$\(KRB5_LIBDIR\)+@PROG_RPATH\=@';
find . -name Makefile | xargs perl -p -i -e 's/TCL_RPATH\s+\=\s+\@TCL_RPATH\@+/TCL_RPATH\=/';
find . -name Makefile | xargs perl -p -i -e 's/PROG_RPATH\s+\=\s+\$\(TCL_RPATH\)+/TCL_RPATH\=/';
find . -name Makefile | xargs perl -p -i -e 's/\@SHLIB_RPATH_DIRS\@+//';
find . -name Makefile | xargs perl -p -i -e "s@ %{_libdir}@ $RPM_BUILD_ROOT%{_libdir}@";
%make LDCOMBINE='%{__cc} -shared -Wl,-soname=lib$(LIB)$(SHLIBSEXT) $(CFLAGS)'

# Run the test suite.  Won't run in the build system because /dev/pts is
# not available for telnet tests and so on.
# make check TMPDIR=%{_tmppath}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Our shell scripts.
mkdir -p $RPM_BUILD_ROOT%{_bindir}
bzcat %{SOURCE11} > $RPM_BUILD_ROOT/%{_bindir}/krsh
bzcat %{SOURCE12} > $RPM_BUILD_ROOT/%{_bindir}/krlogin

# Extra headers.
mkdir -p $RPM_BUILD_ROOT%_prefix/include
(cd src/include
 find kadm5 krb5 gssrpc gssapi -name "*.h" | \
 cpio -pdm  $RPM_BUILD_ROOT/%_prefix/include )
sed 's^k5-int^krb5/kdb^g' < $RPM_BUILD_ROOT/%_prefix/include/kadm5/admin.h \
			  > $RPM_BUILD_ROOT/%_prefix/include/kadm5/admin.h2 &&\
mv $RPM_BUILD_ROOT/%_prefix/include/kadm5/admin.h2 \
   $RPM_BUILD_ROOT/%_prefix/include/kadm5/admin.h
find $RPM_BUILD_ROOT/%_prefix/include -type d | xargs chmod 755
find $RPM_BUILD_ROOT/%_prefix/include -type f | xargs chmod 644

#logdir
mkdir -p $RPM_BUILD_ROOT/var/log/kerberos

# Info docs.
mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -m 644 doc/*.info* $RPM_BUILD_ROOT%{_infodir}/

# KDC config files.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/kerberos/krb5kdc
bzcat %{SOURCE9} > $RPM_BUILD_ROOT%{_sysconfdir}/kerberos/krb5kdc/kdc.conf
bzcat %{SOURCE10} > $RPM_BUILD_ROOT%{_sysconfdir}/kerberos/krb5kdc/kadm5.acl

# Client config files and scripts.
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
bzcat %{SOURCE5} > $RPM_BUILD_ROOT/%{_sysconfdir}/krb5.conf
bzcat %{SOURCE6} > $RPM_BUILD_ROOT/etc/profile.d/krb5.sh
bzcat %{SOURCE7} > $RPM_BUILD_ROOT/etc/profile.d/krb5.csh

# KDC init script.
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}

bzcat %{SOURCE4} > $RPM_BUILD_ROOT/%{_initrddir}/krb5kdc
bzcat %{SOURCE3} > $RPM_BUILD_ROOT/%{_initrddir}/kadmin
bzcat %{SOURCE1} > $RPM_BUILD_ROOT/%{_initrddir}/kprop
bzcat %{SOURCE2} > $RPM_BUILD_ROOT/%{_initrddir}/krb524
bzcat %{SOURCE8} > $RPM_BUILD_ROOT/%{_sbindir}/kdcrotate
bzcat %{SOURCE18} > $RPM_BUILD_ROOT/%{_initrddir}/krb5server

# The rest of the binaries and libraries and docs.
cd src
find . -name Makefile | xargs perl -p -i -e "s@ %{_libdir}@ $RPM_BUILD_ROOT%{_libdir}@";
make prefix=$RPM_BUILD_ROOT%_prefix \
	localstatedir=$RPM_BUILD_ROOT/etc/kerberos \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
 	libdir=$RPM_BUILD_ROOT%{_libdir}/ install

# Fixup strange shared library permissions.
chmod 755 $RPM_BUILD_ROOT%{_libdir}/*.so*

%if %{build_opensls}
mkdir -p %{buildroot}/var/service/{telnet,ftp}/log
mkdir -p %{buildroot}/var/log/supervise/{telnet,ftp}
install -m 0755 %{SOURCE27} %{buildroot}/var/service/telnet/run
install -m 0755 %{SOURCE28} %{buildroot}/var/service/telnet/log/run
install -m 0755 %{SOURCE29} %{buildroot}/var/service/ftp/run
install -m 0755 %{SOURCE30} %{buildroot}/var/service/ftp/log/run
%else
# Xinetd configuration files.
mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d/
bzcat %{SOURCE16} > $RPM_BUILD_ROOT/etc/xinetd.d/telnet
bzcat %{SOURCE17} > $RPM_BUILD_ROOT/etc/xinetd.d/ftp

#telnet menu entries
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF >$RPM_BUILD_ROOT%{_menudir}/telnet
?package(telnet): command="%{_bindir}/telnet" needs="text" \
icon="telnet.xpm" section="Networking/Remote access" \
title="Telnet" longtitle="Telnet client"
EOF

# icons for telnet client
mkdir -p $RPM_BUILD_ROOT/%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_liconsdir}
bzcat %{SOURCE20} > $RPM_BUILD_ROOT/%{_miconsdir}/telnet.xpm
bzcat %{SOURCE21} > $RPM_BUILD_ROOT/%{_iconsdir}/telnet.xpm
bzcat %{SOURCE22} > $RPM_BUILD_ROOT/%{_liconsdir}/telnet.xpm
%endif

bzcat %{SOURCE23} > $RPM_BUILD_DIR/%{name}-%{version}/doc/Mandrake-Kerberos-HOWTO.html

strip $RPM_BUILD_ROOT/%{_bindir}/v4rcp
strip $RPM_BUILD_ROOT/%{_bindir}/ksu

find $RPM_BUILD_ROOT -name "*\.h" | xargs perl -p -i -e "s|\<com_err|\<et/com_err|";
find $RPM_BUILD_ROOT -name "*\.h" | xargs perl -p -i -e "s|\"com_err|\"et/com_err|";

find %{_builddir}/%{name}-%{version} -name "*\.h" | xargs perl -p -i -e "s|\<com_err|\<et/com_err|";
find %{_builddir}/%{name}-%{version} -name "*\.h" | xargs perl -p -i -e "s|\"com_err|\"et/com_err|";

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post server
# Remove the init script for older servers.
[ -x /etc/rc.d/init.d/krb5server ] && /sbin/chkconfig --del krb5server
# Install the new ones.
/sbin/chkconfig --add krb5kdc
/sbin/chkconfig --add kadmin
/sbin/chkconfig --add krb524
/sbin/chkconfig --add kprop
# Install info pages.
/sbin/install-info %{_infodir}/krb425.info.bz2 %{_infodir}/dir
/sbin/install-info %{_infodir}/krb5-admin.info.bz2 %{_infodir}/dir
/sbin/install-info %{_infodir}/krb5-install.info.bz2 %{_infodir}/dir

%preun server
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del krb5kdc
	/sbin/chkconfig --del kadmin
	/sbin/chkconfig --del krb524
	/sbin/chkconfig --del kprop
	/sbin/service krb5kdc stop > /dev/null 2>&1 || :
	/sbin/service kadmin stop > /dev/null 2>&1 || :
	/sbin/service krb524 stop > /dev/null 2>&1 || :
	/sbin/service kprop stop > /dev/null 2>&1 || :
#	/sbin/install-info --delete %{_infodir}/krb425.info.gz %{_infodir}/dir
#	/sbin/install-info --delete %{_infodir}/krb5-admin.info.gz %{_infodir}/dir
#	/sbin/install-info --delete %{_infodir}/krb5-install.info.gz %{_infodir}/dir
fi

%postun server
if [ "$1" -ge 1 ] ; then
	/sbin/service krb5kdc condrestart > /dev/null 2>&1 || :
	/sbin/service kadmin condrestart > /dev/null 2>&1 || :
	/sbin/service krb524 condrestart > /dev/null 2>&1 || :
	/sbin/service kprop condrestart > /dev/null 2>&1 || :
fi

%post workstation
/sbin/install-info %{_infodir}/krb5-user.info %{_infodir}/dir
%if !%{build_opensls}
/sbin/service xinetd reload > /dev/null 2>&1 || :
%endif

%preun workstation
if [ "$1" = "0" ] ; then
	/sbin/install-info --delete %{_infodir}/krb5-user.info %{_infodir}/dir
fi

%if !%{build_opensls}
%postun workstation
/sbin/service xinetd reload > /dev/null 2>&1 || :
%endif

%if !%{build_opensls}
%post -n telnet-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :
ln -sf /bin/login /usr/sbin/login.krb5
file="/etc/xinetd.d/telnet"
if [ ! -f $file ] ; then
	echo "Can't find xinetd file for telnet."
	exit 1
fi
perl -pi -e "s|/usr/sbin/in\.telnetd|/usr/sbin/telnetd|g" $file
# We already have the required flags (-a <some_auth_mode>)
cat $file|egrep -q "server_args.*=.*-a[[:space:]]+.*$" && exit 0
# Don't have -a <some_auth_mode>, check if we have server_args or not
cat $file|egrep -q "server_args.*=.*$" && \
	perl -pi -e "s|(server_args.*=.*$)|\1\ -a\ none|" $file && exit 0
# Say, no server_args in xinetd file.
perl -pi -e "s|(server.*=.*/usr/sbin/telnetd.*$)|\1\n\tserver_args\t=\ -a\ none|" $file && exit 0
%endif

%if !%{build_opensls}
%postun -n telnet-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :
%endif

%if !%{build_opensls}
%post -n telnet-client-krb5
%{update_menus}
%endif

%if !%{build_opensls}
%postun -n telnet-client-krb5
%{clean_menus}
%endif

%if !%{build_opensls}
%post -n ftp-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :
ln -sf /bin/login /usr/sbin/login.krb5
file="/etc/xinetd.d/ftp"
if [ ! -f $file ] ; then
	echo "Can't find xinetd file for ftp."
	exit 1
fi
%endif

%if !%{build_opensls}
%postun -n ftp-server-krb5
/sbin/service xinetd reload > /dev/null 2>&1 || :
%endif

%files workstation
%defattr(-,root,root)

%config(noreplace) /etc/profile.d/krb5.sh
%config(noreplace) /etc/profile.d/krb5.csh

%doc doc/*.html doc/user*.ps.gz src/config-files/services.append
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
%{_bindir}/krb524init
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
%attr(0755,root,root) %{_bindir}/v4rcp
%{_mandir}/man1/v4rcp.1*
%{_bindir}/v5passwd
%{_mandir}/man1/v5passwd.1*
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

%attr(0755,root,root) %config(noreplace) %{_initrddir}/krb5kdc
%attr(0755,root,root) %config(noreplace) %{_initrddir}/kadmin
%attr(0755,root,root) %config(noreplace) %{_initrddir}/krb524
%attr(0755,root,root) %config(noreplace) %{_initrddir}/kprop
%attr(0755,root,root) %config(noreplace) %{_initrddir}/krb5server

%doc doc/admin*.ps.gz doc/*html
%doc doc/krb425*.ps.gz 
%doc doc/install*.ps.gz

%{_infodir}/krb5-admin.info*
%{_infodir}/krb5-install.info*
%{_infodir}/krb425.info*

%dir /var/log/kerberos
%dir %{_sysconfdir}/kerberos/krb5kdc 
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kdc.conf
%config(noreplace) %{_sysconfdir}/kerberos/krb5kdc/kadm5.acl

%{_mandir}/man5/kdc.conf.5*
%{_sbindir}/kadmin.local
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kadmind4
%{_sbindir}/kdb5_util
%{_mandir}/man8/kdb5_util.8*
%{_sbindir}/kprop
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_mandir}/man8/kpropd.8*
%{_sbindir}/krb524d
%{_sbindir}/krb5kdc
%{_mandir}/man8/k5srvutil.8*
%{_sbindir}/k5srvutil
%{_mandir}/man8/krb5kdc.8*
%{_sbindir}/sim_server
%{_sbindir}/v5passwdd
# This is here for people who want to test their server, and also 
# included in devel package for similar reasons.
%{_bindir}/sclient
%{_bindir}/krb5-config
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

%files -n %{libnamedev}
%defattr(-,root,root)
%doc doc/api
%doc doc/implement
%doc doc/kadm5
%doc doc/kadmin
%doc doc/krb5-protocol
%doc doc/rpc
%{_includedir}/*

%{_libdir}/lib*.so

%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*

%files -n telnet-server-krb5
%defattr(-,root,root)
%{_sbindir}/telnetd
%{_mandir}/man8/telnetd.8*
%if %{build_opensls}
%dir /var/service/telnet
%dir /var/service/telnet/log
%dir %attr(0750,nobody,nogroup) /var/log/supervise/telnet
/var/service/telnet/run
/var/service/telnet/log/run
%else
%config(noreplace) /etc/xinetd.d/telnet
%endif

%files -n telnet-client-krb5
%defattr(-,root,root)
%{_bindir}/telnet
%{_mandir}/man1/telnet.1*
%if !%{build_opensls}
%{_menudir}/telnet
%{_miconsdir}/telnet.xpm
%{_iconsdir}/telnet.xpm
%{_liconsdir}/telnet.xpm
%endif

%files -n ftp-client-krb5
%defattr(-,root,root)
%{_bindir}/ftp
%{_mandir}/man1/ftp.1*

%files -n ftp-server-krb5
%defattr(-,root,root)
%{_sbindir}/ftpd
%{_mandir}/man8/ftpd.8*
%if %{build_opensls}
%dir /var/service/ftp
%dir /var/service/ftp/log
%dir %attr(0750,nobody,nogroup) /var/log/supervise/ftp
/var/service/ftp/run
/var/service/ftp/log/run
%else
%config(noreplace) /etc/xinetd.d/ftp
%endif

%changelog
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

