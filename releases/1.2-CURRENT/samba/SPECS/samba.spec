#
# spec file for package samba
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		samba
%define version		3.0.20
%define release		%_revrel

%define smbldapver	0.8.8
%define vscanver	0.3.6b
%global vscandir	samba-vscan-%{vscanver}
%global vfsdir		examples.bin/VFS

%define lib_major	0
%define libname		%mklibname smbclient %{lib_major}

Summary:	The Samba SMB server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.samba.org
Source:         ftp://ca.samba.org/pub/samba/samba-%{version}.tar.bz2
Source1:        samba.log
Source2:        ftp://ca.samba.org/pub/samba/samba-%{version}.tar.asc
Source8:        samba-vscan-%{vscanver}.tar.bz2
Source10:       samba-print-pdf.sh
Source11:       swat.run
Source12:       swat-log.run
Source14:       smbd.run
Source15:       smbd-log.run
Source16:       nmbd.run
Source17:       nmbd-log.run
Source18:       winbindd.run
Source19:       winbindd-log.run
Source20:       smb-migrate
Source21:       README.avx.sambamerge
Patch1:         smbw.patch
Patch2:         samba-3.0.11-mdk-smbldap-config.patch
Patch4:         samba-3.0-smbmount-sbin.patch
Patch5:         samba-3.0.5-mdk-lib64.patch
Patch6:         samba-3.0.6-mdk-smbmount-unixext.patch
Patch7:         samba-3.0.6-mdk-revert-libsmbclient-move.patch
Patch8:         samba-3.0.20-avx-annvix-config.patch
Patch11:	samba-3.0.20-mandrake-packaging.patch
Patch12:	samba-3.0.14a-gcc4.diff
Patch14:	samba-3.0.20-fix-doc-paths.patch
# http://www.samba.org/samba/patches/groupname_enumeration_v3.patch
Patch15:	samba-3.0.20-groupname_enumeration_v3.patch
# http://www.samba.org/samba/patches/winbindd_v1.patch
Patch16:	samba-3.0.20-winbindd_v1.patch
# http://www.samba.org/samba/patches/regcreatekey_winxp_v1.patch
Patch17:	samba-3.0.20-regcreatekey_winxp_v1.patch
# http://www.samba.org/samba/patches/usrmgr_groups_v1.patch
Patch18:	samba-3.0.20-usrmgr_groups_v1.patch

BuildRoot:      %{_buildroot}/%{name}-%{version}
BuildRequires:  pam-devel readline-devel libncurses-devel popt-devel
BuildRequires:  libxml2-devel postgresql-devel
BuildRequires:  MySQL-devel
BuildRequires:  libacl-devel
BuildRequires:  libldap-devel krb5-devel

Requires:       pam >= 0.64, samba-common = %{version}, srv >= 0.7
Prereq:         mktemp psmisc
Prereq:         fileutils sed grep

%description
Samba provides an SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients, including various versions of MS Windows, OS/2,
and other Linux machines. Samba also provides some SMB
clients, which complement the built-in SMB filesystem
in Linux. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.

Samba-3.0 features working NT Domain Control capability and
includes the SWAT (Samba Web Administration Tool) that
allows samba's smb.conf file to be remotely managed using your
favourite web browser. For the time being this is being
enabled on TCP port 901 via tcpsvd. SWAT is now included in
it's own subpackage, samba-swat.

Please refer to the WHATSNEW.txt document for fixup information.
This binary release includes encrypted password support.

Please read the smb.conf file and ENCRYPTION.txt in the
docs directory for implementation details.


%package server
Summary:        Samba (SMB) server programs
Group:          System/Servers
URL:            http://www.samba.org
Requires:       %{name}-common = %{version}
Requires:	perl-Crypt-SmbHash, libxml2
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Provides:       samba
Obsoletes:      samba
Provides:       samba3-server
Obsoletes:      samba3-server

%description server
Samba-server provides a SMB server which can be used to provide
network services to SMB (sometimes called "Lan Manager")
clients. Samba uses NetBIOS over TCP/IP (NetBT) protocols
and does NOT need NetBEUI (Microsoft Raw NetBIOS frame)
protocol.


%package client
Summary:        Samba (SMB) client programs
Group:          Networking/Other
URL:            http://www.samba.org
Requires:       %{name}-common = %{version}
Provides:       samba3-client
Obsoletes:      samba3-client
Obsoletes:      smbfs

%description client
Samba-client provides some SMB clients, which complement the built-in
SMB filesystem in Linux. These allow the accessing of SMB shares, and
printing to SMB printers.


%package common
Summary:        Files used by both Samba servers and clients
Group:          System/Servers
URL:            http://www.samba.org
Provides:       samba3-common
Obsoletes:      samba3-common

%description common
Samba-common provides files necessary for both the server and client
packages of Samba. 


%package swat
Summary:        The Samba Web Administration Tool
Group:          System/Servers
URL:            http://www.samba.org
Requires:       %{name}-server = %{version}
Requires:       ipsvd
Provides:       samba3-swat
Obsoletes:      samba3-swat
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description swat  
SWAT (the Samba Web Administration Tool) allows samba's smb.conf file
to be remotely managed using your favourite web browser. For the time
being this is being enabled on TCP port 901 via tcpsvd. Note that
SWAT does not use SSL encryption, nor does it preserve comments in
your smb.conf file. Webmin uses SSL encryption by default, and
preserves comments in configuration files, even if it does not display
them, and is therefore the preferred method for remotely managing
Samba.


%package winbind   
Summary:        Samba-winbind daemon, utilities and documentation
Group:          System/Servers
URL:            http://www.samba.org
Requires:       %{name}-common = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description winbind
Provides the winbind daemon and testing tools to allow authentication
and group/user enumeration from a Windows or Samba domain controller.


%package -n nss_wins
Summary:        Name Service Switch service for WINS
Group:          System/Servers
URL:            http://www.samba.org
Requires:       %{name}-common = %{version}
Requires(post):	glibc

%description -n nss_wins
Provides the libnss_wins shared library which resolves NetBIOS names to
IP addresses.


%package -n %{libname}
Summary:        SMB Client Library
Group:          System/Libraries
URL:            http://www.samba.org
Provides:       libsmbclient

%description -n %{libname}
This package contains the SMB client library, part of the samba
suite of networking software, allowing other software to access
SMB shares.


%package -n %{libname}-devel
Summary:        SMB Client Library Development files
Group:          Development/C
URL:            http://www.samba.org
Provides:       libsmbclient-devel
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}-devel
This package contains the development files for the SMB client
library, part of the samba suite of networking software, allowing
the development of other software to access SMB shares.


%package -n %{libname}-static-devel
Summary:        SMB Client Static Library Development files
Group:          System/Libraries
URL:            http://www.samba.org
Provides:       libsmbclient-static-devel = %{version}-%{release}
Requires:       %{libname}-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package contains the static development files for the SMB
client library, part of the samba suite of networking software,
allowing the development of other software to access SMB shares.


%package vscan-clamav
Summary:        On-access virus scanning for samba using Clam Antivirus
Group:          System/Servers
Requires:       %{name}-server = %{version}
Provides:       %{name}-vscan
Requires:       clamd

%description vscan-clamav
A vfs-module for samba to implement on-access scanning using the
Clam antivirus scanner daemon.


%package vscan-icap
Summary:        On-access virus scanning for samba using ICAP
Group:          System/Servers
Requires:       %{name}-server = %{version}
Provides:       %{name}-icap

%description vscan-icap
A vfs-module for samba to implement on-access scanning using
ICAP-capable antivirus software.


%prep
%setup -q -a 8
%patch1 -p1 -b .smbw
pushd examples/LDAP/smbldap-tools-%{smbldapver}
%patch2 -p4
popd
%patch4 -p1 -b .sbin
%patch6 -p1 -b .unixext
%patch7 -p1 -b .libsmbdir
%patch11 -p1 -b .mdk
%patch8 -p1 -b .avx
%patch14 -p1 -b .fixdocs
# patches from cvs/samba team
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1	



# Make a copy of examples so that we have a clean one for doc:
cp -a examples examples.bin

cp -a %{vscandir} %{vfsdir}/
#fix stupid directory names:
#mv %{vfsdir}/%{vscandir}/openantivirus %{vfsdir}/%{vscandir}/oav
# Inline replacement of config dir
for av in clamav icap; do
    [ -e %{vfsdir}/%{vscandir}/*/vscan-$av.h ] && perl -pi -e \
        's,^#define PARAMCONF "/etc/samba,#define PARAMCONF "/etc/%{name},' \
        %{vfsdir}/%{vscandir}/*/vscan-$av.h
done
#Inline edit vscan header:
perl -pi -e 's/^# define SAMBA_VERSION_MAJOR 2/# define SAMBA_VERSION_MAJOR 3/g;s/# define SAMBA_VERSION_MINOR_2/# define SAMBA_VERSION_MINOR 0/g' %{vfsdir}/%{vscandir}/include/vscan-global.h
# dunno why samba-vscan keeps copmatability with ancient versions
# of samba but breaks  on samba versions with alpha chars in the name ...
perl -pi -e 's/SAMBA_VERSION_MAJOR==2 && SAMBA_VERSION_RELEASE>=4/SAMBA_VERSION_MAJOR==2/g' %{vfsdir}/%{vscandir}/*/vscan-*.c

find docs examples -name '.cvsignore' -exec rm -f {} \;

%build
pushd source
    CFLAGS=`echo "%{optflags}"|sed -e 's/-g//g'`

    ## fix optimization with gcc 3.3.1 (can remove when we move to 3.4)
    #CFLAGS=`echo "$CFLAGS"|sed -e 's/-O2/-Os/g'`

    ./autogen.sh
    # Don't use --with-fhs now, since it overrides libdir, it sets configdir, 
    # lockdir,piddir logfilebase,privatedir and swatdir
    %configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir}/%{name} \
        --localstatedir=/var \
        --with-libdir=%{_libdir}/%{name} \
        --with-privatedir=%{_sysconfdir}/%{name} \
	--with-lockdir=/var/cache/%{name} \
	--with-piddir=/var/run \
        --with-swatdir=%{_datadir}/swat \
        --with-configdir=%{_sysconfdir}/%{name} \
	--with-logfilebase=/var/log/%{name} \
        --with-automount \
        --with-smbmount \
        --with-pam \
        --with-pam_smbpass \
	--with-ldapsam \
	--with-tdbsam \
        --without-syslog \
        --with-quotas \
        --with-utmp \
	--with-manpages-langs=en \
	--with-acl-support      \
	--disable-mysqltest \
	--with-expsam=mysql,xml,pgsql \
        --with-shared-modules=idmap_rid,idmap_ad

    #Fix the make file so we don't create debug information
    perl -pi -e 's/-g //g' Makefile

    perl -pi -e 's|-Wl,-rpath,%{_libdir}||g;s|-Wl,-rpath -Wl,%{_libdir}||g' Makefile

    make proto_exists
    %make all libsmbclient smbfilter wins modules bin/smbget client/mount.cifs client/umount.cifs
popd

pushd %{vfsdir}/%{vscandir}  
    %configure
    #sed -i -e 's,openantivirus,oav,g' Makefile
    sed -i -e 's,^\(.*clamd socket name.*=\).*,\1 /var/lib/clamav/clamd.socket,g' clamav/vscan-clamav.conf
    make clamav icap
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}

#Ensure all docs are readable
chmod a+r docs -R

# Any entries here mean samba makefile is *really* broken:
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_datadir}
mkdir -p %{buildroot}%{_libdir}/%{name}/vfs

pushd source
    make DESTDIR=%{buildroot} \
        LIBDIR=%{_libdir}/%{name} \
        MANDIR=%{_mandir} \
        install installclientlib installmodules
popd

install -m 0755 source/bin/smbget %{buildroot}%{_bindir}

#need to stay 
mkdir -p %{buildroot}/{sbin,bin}
mkdir -p %{buildroot}%{_sysconfdir}/{logrotate.d,pam.d}
mkdir -p %{buildroot}/var/cache/%{name}
mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}/var/run/%{name}
mkdir -p %{buildroot}/var/spool/%{name}
mkdir -p %{buildroot}%{_localstatedir}/%{name}/{netlogon,profiles,printers}
mkdir -p %{buildroot}%{_localstatedir}/%{name}/printers/{W32X86,WIN40,W32ALPHA,W32MIPS,W32PPC}
mkdir -p %{buildroot}%{_localstatedir}/%{name}/codepages/src
mkdir -p %{buildroot}/%{_lib}/security
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/%{name}/vfs
mkdir -p %{buildroot}%{_datadir}/%{name}/scripts

#smbwrapper and pam_winbind not handled by make, pam_smbpass.so doesn't build
#install -m 0755 source/bin/smbwrapper.so %{buildroot}%{_libdir}/smbwrapper.so
install -m 0755 source/bin/pam_smbpass.so %{buildroot}/%{_lib}/security/pam_smbpass.so
install -m 0755 source/nsswitch/pam_winbind.so %{buildroot}/%{_lib}/security/pam_winbind.so

install -m 0755 source/bin/libsmbclient.a %{buildroot}%{_libdir}/libsmbclient.a

# winbind idmap_rid:
#install -d %{buildroot}%{_libdir}/%{name}/idmap
#install source/bin/idmap_rid.so %{buildroot}%{_libdir}/%{name}/idmap

# smbsh forgotten
#install -m 0755 source/bin/smbsh %{buildroot}%{_bindir}/

%makeinstall_std -C %{vfsdir}/%{vscandir}
install -m 0644 %{vfsdir}/%{vscandir}/*/vscan-*.conf %{buildroot}%{_sysconfdir}/%{name}

#libnss_* not handled by make:
# Install the nsswitch library extension file
for i in wins winbind; do
    install -m 0755 source/nsswitch/libnss_${i}.so %{buildroot}/%{_lib}/libnss_${i}.so
done
# Make link for wins and winbind resolvers
( cd %{buildroot}/%{_lib}; ln -s libnss_wins.so libnss_wins.so.2; ln -s libnss_winbind.so libnss_winbind.so.2)

# Install other stuff

install -m 0644 packaging/Mandrake/smbusers %{buildroot}%{_sysconfdir}/%{name}/smbusers
install -m 0755 packaging/Mandrake/smbprint %{buildroot}%{_bindir}
install -m 0755 packaging/Mandrake/findsmb %{buildroot}%{_bindir}
install -m 0755 packaging/Mandrake/smb.init %{buildroot}%{_sbindir}/%{name}
install -m 0755 packaging/Mandrake/winbind.init %{buildroot}%{_sbindir}/winbind
install -m 0644 packaging/Mandrake/samba.pamd %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 0644 packaging/Mandrake/system-auth-winbind.pamd %{buildroot}%{_sysconfdir}/pam.d/system-auth-winbind
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# make a conf file for winbind from the default one:
cat packaging/Mandrake/smb.conf|sed -e  's/^;  winbind/  winbind/g;s/^;  obey pam/  obey pam/g;s/   printer admin = @adm/#  printer admin = @adm/g; s/^#   printer admin = @"D/   printer admin = @"D/g;s/^;   password server = \*/   password server = \*/g;s/^;  template/  template/g; s/^   security = user/   security = domain/g' > packaging/Mandrake/smb-winbind.conf
install -m 0644 packaging/Mandrake/smb-winbind.conf %{buildroot}%{_sysconfdir}/%{name}/smb-winbind.conf

# Some inline fixes for smb.conf for non-winbind use
install -m 0644 packaging/Mandrake/smb.conf %{buildroot}%{_sysconfdir}/%{name}/smb.conf
cat packaging/Mandrake/smb.conf | \
    sed -e 's/^;   printer admin = @adm/   printer admin = @adm/g' >%{buildroot}%{_sysconfdir}/%{name}/smb.conf

# install mount.cifs
for i in mount.cifs umount.cifs
do
    install -m 0755 source/client/$i %{buildroot}/bin/$i
    ln -s ../bin/$i %{buildroot}/sbin/$i
done

echo 127.0.0.1 localhost > %{buildroot}%{_sysconfdir}/%{name}/lmhosts

# Link smbspool to CUPS (does not require installed CUPS)

mkdir -p %{buildroot}%{_libdir}/cups/backend
ln -s %{_bindir}/smbspool %{buildroot}%{_libdir}/cups/backend/smb

# ipsvd support
mkdir -p %{buildroot}%{_srvdir}/swat/{log,env,peers}
install -m 0740 %{SOURCE11} %{buildroot}%{_srvdir}/swat/run
install -m 0740 %{SOURCE12} %{buildroot}%{_srvdir}/swat/log/run
touch %{buildroot}%{_srvdir}/swat/peers/0
chmod 0640 %{buildroot}%{_srvdir}/swat/peers/0


echo "901" >%{buildroot}%{_srvdir}/swat/env/PORT

cat %{SOURCE10}> %{buildroot}%{_datadir}/%{name}/scripts/print-pdf
cat %{SOURCE20}> %{buildroot}%{_datadir}/%{name}/scripts/smb-migrate

rm -f %{buildroot}/sbin/mount.smbfs
# Link smbmount to /sbin/mount.smb and /sbin/mount.smbfs
# I don't think it's possible for make to do this ...
pushd %{buildroot}/sbin
    ln -s ..%{_bindir}/smbmount mount.smb
    ln -s ..%{_bindir}/smbmount mount.smbfs
popd

mkdir -p %{buildroot}%{_srvdir}/{smbd,nmbd,winbindd}/log
install -m 0740 %{SOURCE14} %{buildroot}%{_srvdir}/smbd/run
install -m 0740 %{SOURCE15} %{buildroot}%{_srvdir}/smbd/log/run
install -m 0740 %{SOURCE16} %{buildroot}%{_srvdir}/nmbd/run
install -m 0740 %{SOURCE17} %{buildroot}%{_srvdir}/nmbd/log/run
install -m 0740 %{SOURCE18} %{buildroot}%{_srvdir}/winbindd/run
install -m 0740 %{SOURCE19} %{buildroot}%{_srvdir}/winbindd/log/run

mv %{buildroot}%{_sysconfdir}/samba/smb.conf %{buildroot}%{_sysconfdir}/samba/smb.conf_full
install -m 0640 packaging/Mandrake/smb.conf.secure %{buildroot}%{_sysconfdir}/samba/smb.conf

# Clean up unpackaged files:
for i in %{_bindir}/pam_smbpass.so %{_bindir}/smbwrapper.so %{_mandir}/man1/editreg*;do
    rm -f %{buildroot}/$i
done
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-{symantec,fprotd,fsav,kavp,mcdaemon,mks32,oav,sophos,trend,antivir}.conf

# install html man pages for swat
mkdir -p %{buildroot}/%{_datadir}/swat/help/manpages
install -m 0644 docs/htmldocs/manpages-3/* %{buildroot}/%{_datadir}/swat/help/manpages

# the binary gets removed ... but not the man page ...
rm -f %{buildroot}%{_mandir}/man1/testprns*


# (sb) make a smb.conf.clean we can use for the merge, since an existing
# smb.conf won't get overwritten
cp %{buildroot}%{_sysconfdir}/%{name}/smb.conf %{buildroot}%{_datadir}/%{name}/smb.conf.clean

# (sb) leave a README.avx.conf to explain what has been done
cat %{SOURCE21} >%{buildroot}%{_datadir}/%{name}/README.avx.conf

mkdir -p %{buildroot}%{_srvdir}/smbd/depends
%_mkdepends smbd nmbd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post server
for i in smbd nmbd
do
    if [ -d /var/log/supervise/$i -a ! -d /var/log/service/$i ]; then
        mv /var/log/supervise/$i /var/log/service/
    fi
done
%_post_srv smbd
%_post_srv nmbd

# Add a unix group for samba machine accounts
groupadd -frg 101 machines

# Migrate tdb's from /var/lock/samba (taken from official samba spec file):
for i in /var/lock/samba/*.tdb
do
    if [ -f $i ]; then
        newname=`echo $i | sed -e's|var\/lock\/samba|var\/cache\/samba|'`
        echo "Moving $i to $newname"
        mv $i $newname
    fi
done


%post common
# Basic migration script for pre-2.2.1 users,
# since smb config moved from /etc to %{_sysconfdir}/samba

# Let's create a proper %{_sysconfdir}/samba/smbpasswd file
[ -f %{_sysconfdir}/%{name}/smbpasswd ] || {
    echo "Creating password file for samba..."
    touch %{_sysconfdir}/%{name}/smbpasswd
}

# And this too, in case we don't have smbd to create it for us
[ -f /var/cache/%{name}/unexpected.tdb ] || {
    touch /var/cache/%{name}/unexpected.tdb
}

# Let's define the proper paths for config files
perl -pi -e 's/(\/etc\/)(smb)/\1%{name}\/\2/' %{_sysconfdir}/%{name}/smb.conf

# Fix the logrotate.d file from smb and nmb to smbd and nmbd
if [ -f %{_sysconfdir}/logrotate.d/samba ]; then
    perl -pi -e 's/smb /smbd /' %{_sysconfdir}/logrotate.d/samba
    perl -pi -e 's/nmb /nmbd /' %{_sysconfdir}/logrotate.d/samba
fi

# And not loose our machine account SID
[ -f %{_sysconfdir}/MACHINE.SID ] && mv -f %{_sysconfdir}/MACHINE.SID %{_sysconfdir}/%{name}/ ||:

%triggerpostun common -- samba-common < 3.0.1-7avx
# (sb) merge any existing smb.conf with new syntax file
if [ "$1" = "2" ]; then
    # (sb) save existing smb.conf for merge
    echo "Upgrade: copying smb.conf to smb.conf.tomerge for merging..."
    cp -f %{_sysconfdir}/%{name}/smb.conf %{_sysconfdir}/%{name}/smb.conf.tomerge
    echo "Upgrade: merging previous smb.conf..."
    if [ -f %{_datadir}/%{name}/smb.conf.clean ]; then
	cp %{_datadir}/%{name}/smb.conf.clean %{_sysconfdir}/%{name}/smb.conf
	cp %{_datadir}/%{name}/README.avx.conf %{_sysconfdir}/%{name}/
	%{_datadir}/%{name}/smb-migrate commit
    fi
fi

%postun common
if [ -f %{_sysconfdir}/%{name}/README.avx.conf ]; then rm -f %{_sysconfdir}/%{name}/README.avx.conf; fi

%post winbind
if [ $1 = 1 ]; then
#    /sbin/chkconfig winbind on
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmsave
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmtemp
    for i in passwd group;do
        grep ^$i %{_sysconfdir}/nsswitch.conf |grep -v 'winbind' >/dev/null
        if [ $? = 0 ];then
            echo "Adding a winbind entry to the $i section of %{_sysconfdir}/nsswitch.conf"
            awk '/^'$i'/ {print $0 " winbind"};!/^'$i'/ {print}' %{_sysconfdir}/nsswitch.conf.rpmtemp >%{_sysconfdir}/nsswitch.conf;
	    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmtemp
        else
            echo "$i entry found in %{_sysconfdir}/nsswitch.conf"
        fi
    done
    if [ -f %{_sysconfdir}/nsswitch.conf.rpmtemp ];then rm -f %{_sysconfdir}/nsswitch.conf.rpmtemp;fi
fi
if [ -d /var/log/supervise/winbindd -a ! -d /var/log/service/winbindd ]; then
    mv /var/log/supervise/winbindd /var/log/service/
fi
%_post_srv winbindd

%preun winbind
if [ $1 = 0 ]; then
    echo "Removing winbind entries from %{_sysconfdir}/nsswitch.conf"
    perl -pi -e 's/ winbind//' %{_sysconfdir}/nsswitch.conf
fi
%_preun_srv winbindd

%post -n nss_wins
if [ $1 = 1 ]; then
    cp -af %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/nsswitch.conf.rpmsave
    grep '^hosts' %{_sysconfdir}/nsswitch.conf |grep -v 'wins' >/dev/null
    if [ $? = 0 ];then
        echo "Adding a wins entry to the hosts section of %{_sysconfdir}/nsswitch.conf"
        awk '/^hosts/ {print $0 " wins"};!/^hosts/ {print}' %{_sysconfdir}/nsswitch.conf.rpmsave >%{_sysconfdir}/nsswitch.conf;
    else
        echo "wins entry found in %{_sysconfdir}/nsswitch.conf"
    fi
fi

%preun -n nss_wins
if [ $1 = 0 ]; then
    echo "Removing wins entry from %{_sysconfdir}/nsswitch.conf"
    perl -pi -e 's/ wins//' %{_sysconfdir}/nsswitch.conf
fi

%preun server
%_preun_srv smbd
%_preun_srv nmbd


%post swat
%_post_srv swat
pushd %{_srvdir}/swat >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd >/dev/null 2>&1


%preun swat
%_preun_srv swat


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files server
%defattr(-,root,root)
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smbusers
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_sbindir}/nmbd
%{_sbindir}/samba
%{_sbindir}/smbd
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/smbcontrol
%{_bindir}/smbstatus
%{_bindir}/tdbbackup
%attr(755,root,root) /%{_lib}/security/pam_smbpass*
%dir %{_libdir}/%{name}/vfs
%{_libdir}/%{name}/vfs/*.so
%exclude %{_libdir}/%{name}/vfs/vscan*.so
%dir %{_libdir}/%{name}/pdb
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/tdbbackup.8*
%attr(775,root,adm) %dir %{_localstatedir}/%{name}/netlogon
%attr(755,root,root) %dir %{_localstatedir}/%{name}/profiles
%attr(755,root,root) %dir %{_localstatedir}/%{name}/printers
%attr(2775,root,adm) %dir %{_localstatedir}/%{name}/printers/*
%attr(1777,root,root) %dir /var/spool/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%attr(0755,root,root) %{_datadir}/%{name}/scripts/print-pdf
# passdb
%{_libdir}/%{name}/pdb/*mysql.so
%{_libdir}/%{name}/pdb/*pgsql.so
%{_libdir}/%{name}/pdb/*xml.so

%dir %attr(0750,root,admin) %{_srvdir}/smbd
%dir %attr(0750,root,admin) %{_srvdir}/smbd/log
%dir %attr(0750,root,admin) %{_srvdir}/smbd/depends
%dir %attr(0750,root,admin) %{_srvdir}/nmbd
%dir %attr(0750,root,admin) %{_srvdir}/nmbd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/smbd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/smbd/log/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/smbd/depends/nmbd
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nmbd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/nmbd/log/run

%files swat
%defattr(-,root,root)
%dir %attr(0750,root,admin) %{_srvdir}/swat
%dir %attr(0750,root,admin) %{_srvdir}/swat/log
%dir %attr(0750,root,admin) %{_srvdir}/swat/env
%dir %attr(0750,root,admin) %{_srvdir}/swat/peers
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/swat/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/swat/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/swat/peers/0
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/swat/env/PORT
%{_sbindir}/swat
%attr(-,root,root) %{_datadir}/swat/help/
%attr(-,root,root) %{_datadir}/swat/images/
%attr(-,root,root) %{_datadir}/swat/include/
%attr(-,root,root) %{_datadir}/swat/help/
%lang(ja) %{_datadir}/swat/lang/ja
%lang(tr) %{_datadir}/swat/lang/tr
%{_mandir}/man8/swat*.8*
%lang(de) %{_libdir}/%{name}/de.msg
%lang(en) %{_libdir}/%{name}/en.msg
%lang(fr) %{_libdir}/%{name}/fr.msg
%lang(it) %{_libdir}/%{name}/it.msg
%lang(ja) %{_libdir}/%{name}/ja.msg
%lang(nl) %{_libdir}/%{name}/nl.msg
%lang(pl) %{_libdir}/%{name}/pl.msg
%lang(tr) %{_libdir}/%{name}/tr.msg

%files client
%defattr(-,root,root)
%{_bindir}/findsmb
%{_bindir}/nmblookup
%{_bindir}/smbclient
%attr(4755,root,root) %{_bindir}/smbmnt
%attr(755,root,root) %{_bindir}/smbmount
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbtar
%attr(4755,root,root) %{_bindir}/smbumount
%{_bindir}/smbget
/sbin/mount.smb
/sbin/mount.smbfs
/sbin/mount.cifs
/sbin/umount.cifs
%attr(4755,root,root) /bin/mount.cifs
%attr(4755,root,root) /bin/umount.cifs
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbget.1*
%{_mandir}/man5/smbgetrc.5*
%{_mandir}/man8/mount.cifs*.8*
%{_mandir}/man8/umount.cifs*.8*
%{_mandir}/man8/smbmnt.8*
%{_mandir}/man8/smbmount.8*
%{_mandir}/man8/smbspool.8*
%{_mandir}/man8/smbumount.8*
# Link of smbspool to CUPS
/%{_libdir}/cups/backend/smb

%files common
%defattr(-,root,root)
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb.conf_full
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/smb-winbind.conf
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/%{name}/lmhosts
%dir /var/cache/%{name}
%dir /var/log/%{name}
%dir /var/run/%{name}
%{_bindir}/net
%{_bindir}/ntlm_auth
%{_bindir}/rpcclient
%{_bindir}/smbcacls
%{_bindir}/smbcquotas
%{_bindir}/smbpasswd
%{_bindir}/smbtree
%{_bindir}/testparm
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man5/smb.conf*.5*
%{_mandir}/man5/smbpasswd*.5*
%{_mandir}/man5/lmhosts*.5*
%{_mandir}/man8/net.8*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man8/tdbdump.8*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/charset
%dir %{_sysconfdir}/%{name}
%dir %{_localstatedir}/%{name}
%attr(-,root,root) %{_localstatedir}/%{name}/codepages
%dir %{_datadir}/swat
%attr(0750,root,adm) %{_datadir}/%{name}/scripts/smb-migrate
%{_datadir}/%{name}/smb.conf.clean
%{_datadir}/%{name}/README.avx.conf

%files winbind
%defattr(-,root,root)
%attr(-,root,root) %config(noreplace) %{_sysconfdir}/pam.d/system-auth-winbind*
%{_sbindir}/winbindd
%{_sbindir}/winbind
%{_bindir}/wbinfo
%attr(755,root,root) /%{_lib}/security/pam_winbind*
%attr(755,root,root) /%{_lib}/libnss_winbind*
%{_libdir}/%{name}/idmap
%{_mandir}/man8/pam_winbind*.8*
%{_mandir}/man8/winbindd*.8*
%{_mandir}/man1/wbinfo*.1*
%dir %attr(0750,root,admin) %{_srvdir}/winbindd
%dir %attr(0750,root,admin) %{_srvdir}/winbindd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/winbindd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/winbindd/log/run

%files -n nss_wins
%defattr(-,root,root)
%attr(755,root,root) /%{_lib}/libnss_wins.so*

%exclude %{_mandir}/man1/vfstest*.1*
%exclude %{_mandir}/man1/log2pcap*.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libsmbclient.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libsmbclient.so
%{_mandir}/man8/libsmbclient.8*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/libsmbclient.a

%files vscan-clamav
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-clamav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-clamav.conf
%doc %{vfsdir}/%{vscandir}/INSTALL

%files vscan-icap
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-icap.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-icap.conf
%doc %{vfsdir}/%{vscandir}/INSTALL

%exclude %{_mandir}/man1/smbsh*.1*


%changelog
* Tue Feb 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20
- correct the perms on swat's peers/PORT file

* Mon Feb 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20
- correct the perms on swat's peers/0 file

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20
- remove tdbdump and it's manpage from samba-server because it's already
  in samba-common which samba-server requires anyways (thanks Ying for
  spotting this)

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20
- build against new postgresql

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix (some) prereqs

* Fri Sep 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20-6avx
- cleanups to swat runfile

* Thu Sep 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20-5avx
- fix the nmbd runscript to remove svwaitup since it doesn't have
  any dependencies

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20-4avx
- add %%post and %%preun for swat
- execline run scripts
- simplify the winbindd script; admins need to know their stuff before
  they go adding daemons so don't baby them (aka get rid of the uid/gid
  checks)
- build peers.cdb in swat %%post
- env dirs
- make smbd require nmbd; for now don't add a reverse require because it
  makes the new srv have fits

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20-3avx
- really apply P16
- P17 and P18: more post-3.0.20 fixes
- rediff P8 against the updated mandrake smb.conf

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20-2avx
- rebuild against new readline and libxml2

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.20-1avx
- 3.0.20
- use execlineb for run scripts
- move logdir to /var/log/service/{smbd,nmbd,swat,winbindd}
- run scripts are now considered config files and are not replaceable
- update group enumeration patch, add winbind patch from
  http://www.samba.org/samba/patches/
- add new idmap_ad plugin
- rediff P8
- update the run scripts to use -F instead of both -D and -F
- source /usr/share/srv/functions in windbindd's run script

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11-6avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11-5avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11-4avx
- rebuild

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11-3avx
- rebuild against new libxml2

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11-2avx
- use logger for logging
- add the idmap_rid module (bgmilne)
- put smbldap-tools as it's own package (bgmilne)
- drop the unnecessary cache file backup (bgmilne)

* Tue Feb 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0.11-1avx
- 3.0.11
- fix nmbd/log/run script
- drop editreg (bgmilne)
- new smbldap-tools (redo P2, etc.) (bgmilne)
- remove all xinetd-related stuff
- some spec cleanups
- update swat runscript to use tcpsvd
- samba-swat requires ipsvd, not ucspi-tcp
- GUT the spec.. alternatives, strange mojo.. this was an awful spec... it's much
  cleaner now thank you very much
- server requires perl-Crypt-SmbHash, libxml2
- update smb.conf to use smbpasswd by default for the backend
- update smbd/nmbd runscripts
- rediff P3; make sure the passdb backend is specified as it defaults to ldap;
  also log to %m.log rather than log.%m so logs actually get rotated
- compile without-syslog as on active servers, it files messages and daemons up
  pretty quick; let samba handle it's own logging

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.10-1avx
- 3.0.10 - security update for CAN-2004-1154
- add a symlink for mount.cifs in /sbin, so mount -t cifs works (bgmilne)
- drop P3; merged
- fix build when not system (tdbtool must be suffixed also), mdk bug
  #12417 (bgmilne)
- rediff P8
- include pam_windbind.8 manpage

* Wed Nov 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.8-1avx
- 3.0.8 - security update for CAN-2004-0930
- add tdbtool to common (bgmilne)
- fix the doc permissions that were broken in the tarball (bgmilne)
- s/Anthill/Bugzilla/

* Mon Sep 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.7-1avx
- 3.0.7 - security update for CAN-2004-0807 and CAN-2004-0808
- P8: move old smb.conf to smb.conf_full and use a new secure (small!)
  smb.conf
- updated runscripts
- don't apply P5 (broken)
- P6: from Urban Widmark via Robert Sim (anthill bug 1086) to be able
  to disable unix extensions in smbmount (and via 'unix extensions' in
  smb.conf) (bgmilne)
- update P3 from mandrake
- sync smb.conf with drakwizard (which also fixes quoting of macros which
  can have spaces) (bgmilne)
- add example admin share (bgmilne)
- P7: keep libsmbclient.so where it belongs (bgmilne)
- remove cups support, but keep the smbspool link to cups in case someone
  installs cups on their own
- NOTE: this spec still needs a major overhaul

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.5-3avx
- rebuild against new openssl

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.5-2avx
- don't need libsmbclient move hack for x86_64 anymore
- fix pid file location (#10666) (bgmilne)
- merge amd64 fixes (P7) (bgmilne)
- make pdf printer work again, and other misc fixes to default
  config (bgmilne)

* Tue Jul 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.5-1avx
- 3.0.5 (fixes CAN-2004-0600, CAN-2004-0686)
- include gpg signature
- update run scripts for as-close-to-proper daemonization as
  possible (but samba still forks which forces us to take drastic
  measures)
- Requires: srv >= 0.7

* Wed Jul 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.5pre1-1avx
- 3.0.5pre1
- remove symantec antvirus completely as it's the only one we need
  external libs for
- merge from Mandrake 3.x-xmdk:
  - add migrate script to merge existing smb.conf (sbenedict); use
    trigger to only upgrade from <3.0.1-7avx
  - re-enable relaxed CFLAGS to fix broken smbmount, smbclient (sbenedict)
  - P2: fix default smbldap config (bgmilne)
  - fix samba-vscan (0.3.5), add clamav and icap (bgmilne)
  - P3: fix default vscan-clamav config and add sample config for homes
    share (bgmilne)
  - add PostgreSQL passdb backend (bgmilne)
  - re-work scanner support (bgmilne)
  - add support for NAI McAfee and F-Secure (bgmilne)
  - fix building without scanners (bgmilne)


* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.0.1-7avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.0.1-6sls
- minor spec cleanups

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 3.0.1-5sls
- srv macros
- strip all support for mdk releases
- remove %%build_opensls macros
- remove initscripts
- add winbindd under supervise
- machines has static gid 101 not 421
- remove calls to chkconfig for winbind (should the mods to nsswitch.conf be
  done using chkauth or something similar in the future, rather than in the
  spec?)

* Fri Jan 09 2004 Vincent Danen <vdanen@opensls.org> 3.0.1-4sls
- libsmbclient.so is installed into /usr/lib not /usr/lib64 so if building for
  amd64, move it

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 3.0.1-3sls
- OpenSLS build
- tidy spec
- use %%build_opensls to disable req for xinetd and put req on ucspi-tcp
  instead
- build the swat.cdb in %%post; default rules allow 127. and nothing else
- include supervise run files for smbd and nmbd

* Fri Dec 19 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-2mdk
- 3.0.1 final

* Thu Dec 11 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.rc2.2mdk
- 3.0.1rc2

* Sat Dec 06 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.rc1.2mdk
- rc1
- samba-vscan-0.3.4

* Fri Dec 05 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.pre3.5mdk
- Allow winbind to start if old winbind ranges are used (ease upgrades)

* Tue Nov 18 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.pre3.4mdk
- Fix build as system on 8.2 (and probably earlier)

* Sun Nov 16 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.pre3.3mdk
- Ensure printer drivers keep permissions by default (setgid and inherit perms)

* Fri Nov 14 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.pre3.2mdk
- 3.0.1pre3
- Add support for Mandrake 10.0 (as system samba)
- Fix alternatives triggers
- Fix obsoletes

* Mon Nov 10 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.pre2.2mdk
- 3.0.1pre2
- misc spec files (pointed out by Luca Olivetti)
- Fix path to smbldap-passwd.pl
- Only allow one copy of winbind and nss_wins
- Add trigger for alternatives

* Sun Oct 12 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.1-0.pre1.2mdk
- 3.0.1pre1
- remove buildroot patch (p3), fixed upstream

* Thu Sep 25 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-2mdk
- 3.0.0 final

* Sat Sep 13 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.rc4.2mdk
- rc4
- Don't update alternatives in pre/post scripts when not using alternatives
- Fix case of --with-system without alternatives
- Final fixes to smbldap-tools for non-system case
- Remove duplicate docs (really - 1 character typo ...)
- Update configs (fix winbind init script, add example scripts in smb.conf)

* Tue Sep 09 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.rc3.2mdk
- rc3
- Fix mount.smb{,fs} alternatives (spotted by Laurent Culioli)

* Thu Sep 04 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.rc2.3mdk
- Fix alternatives
- Fix libname (can I blame guillomovitch's evil line-wrapping spec mode?)
- Fix smbldap-tools package/use names when not system samba
- Don't conflict samba3-client with samba-client for now so we can install it

* Fri Aug 29 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.rc2.2mdk
- rc2
- Remove patches 100-102 (upstream)
- Fix libname
- Alternatavise client
- Better solution to avoid rpath

* Fri Aug 22 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.rc1.3mdk
- Fix build with test package (p100), but not by default (too big)
- Fix (p101) for SID resolution when member of samba-2.2.x domain
- Fix libsmbclient packages (thanks Gotz)
- version mount.cifs, patch from CVS (p102), and setuid it
- Clean up docs (guillomovitch spam ;-)

* Sat Aug 16 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.rc1.2mdk
- rc1
- disable test subpackage since it's broken again

* Mon Jul 28 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.beta3.3mdk
- Rebuild for kerberos-1.3 on cooker
- Put printer directories back
- Add mount.cifs
- Go back to standard optimisations

* Thu Jul 17 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.beta3.2mdk
- beta3
- remove -g from cflags to avoid large static libraries
- drop optimisation from O2 to O1 for gcc 3.3.1
- own some directories for distriblint's benefit
- use chrpath on distro's that have it to drastically reduce rpmlint score

* Mon Jul 14 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.beta2.3mdk
- place non-conditional excludes at the end of files list, to prevent causing
  rpm in Mandrake <=8.2 from segfaulting when processing files.
- Update default config  

* Wed Jul 02 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.beta2.2mdk
- 3.0.0beta2
- manually build editreg
- Add some new man pages

* Tue Jun 10 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.beta1.3mdk
- add provision for passdb-ldap subpackage (it doesn't build like that yet)
- avoid debugging info on cooker/9.2 for the moment
- We probably don't need to autoconf (and can thus build on 8.1)
- We can probably build without kerberos support (and thus on 8.0)
- Don't require mysql-devel on alpha's (maybe we want to be able to disable
  mysql support for other arches?)
- We shouldn't need to specifically add openssl to include path, since ssl
  support is deprecated.
- png icons, change menu title to not conflict with ksambaplugin  
- update to samba-vscan-0.3.3beta1, but it still does not build the vscan
  modules.
- add -static-devel package
- Add buildrequires for lib packages that are picked up if installed
  (ncurses, popt) in an attempt to get slbd to build samba3
- Fix default config (P100)

* Sun Jun 08 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0.0-0.beta1.2mdk
- Get packages into cooker (klama doesn't want to build this package ..)
- samba-vscan-0.3.2b

* Fri Jun 06 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha24.2mdk
- Rename debug package to test and other fixes for rpm-4.2
- prepare for beta1

* Wed Apr 30 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha24.1mdk
- Remove some files removed upstream
- In builds from source, don't terminate on missing docs or unpackaged files
  (if only we could do it for other missing files ...)

* Mon Apr 28 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha24.0mdk
- Reenable debug package by (--without debug to not build it), fixed post-a23
- Add bugzilla note for builds from source (also intended for packages made
  available on samba FTP site) at samba team request
- Fix build from CVS (run autogen.sh, pass options to all rpm commands)
- Appease distriblint, but not much to be done about /usr/share/swat3/ since
  samba-doc owns some subdirs, and samba-swat others, and they can be installed
  independantly.
- Apply kaspersky vscan build fix from samba2  
- Final for alpha24

* Wed Apr 23 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha23.3mdk
- Small fixes in preparation for testing as system samba
- Make debug package optional (--with debug) since it's often broken
- Add support for 9.2 (including in-line smbd quota patch for glibc2.3)
- Add --with options option, which will just show you the available options and exit

* Sun Apr 06 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha23.2mdk
- Alpha23
- buildrequire autconf2.5
- samba-vscan 0.3.2a
- Remove patch 102 (upstreamed)

* Thu Mar 06 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha22.2mdk
- Alpha22
- Add profiles binary to server and ntlm_auth to common
- smbwrapper and torture target broken (only in 9.0?)
- remove unused source 2

* Tue Mar 04 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha21.4mdk
- Don't provide samba-{server,client,common} when not system samba (bug #2617)
- Don't build libsmbclient packages when not system samba
- Fix conflict between samba-server and samba3-server (pam_smbpass)
- Fix smbwrapper (from 2.2.7a-5mdk for bug #2356)
- Fix codepage/charset example (bug #1574)

* Thu Jan 23 2003 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha21.3mdk
- samba-vscan 0.3.1 (and make it build again), including required inline edits
- Make all vscan packages provide samba(3)-vscan
- Build all vscan except kav (requires kaspersky lib) with --with-scanners
- Add vscan-(scanner).conf files
- Explicitly add ldapsam for 2.2 compatability when building --with ldap,
  default build now uses new ldap passdb backend (ie you always get ldap)
- Enable (experimental) tdb passdb backend
- Fix file ownership conflicts between server and common
- Cleanup configure, to match order of --help
- Fix libdir location, was being overridden by --with-fhs
- Split off a libsmbclient and -devel package
- Add wins replication init script (patch 102)
- Workaround passdb/pdb_xml.c not compiling
- Workaround missing install targets for smbsh/smbwrapper.so in cvs
- Inline patch smbd/quotas.c for Mandrake >9.0

* Wed Nov 27 2002 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha21.2mdk
- Remove patch 20,21,22,23,25,26 (upstream)
- New destdir patch from cvs (18)
- package installed but non-packaged files
- new debug subpackage for vfstest and related files (it was that or nuke the 
  manpage ;-))
- use _libdir for libdir instead of _sysconfdir
- Update samba-vscan (untested)

* Mon Oct 28 2002 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha20.3mdk
- Fix mount.smbfs3 pointing to smbmount not in package
- Remove unnecessary lines from install (now done by make)
- Build with ldap and ads on all releases by default
- Put av-stuff back

* Mon Oct 21 2002 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha20.2mdk
- When not building as system samba, avoid conflicting with system samba
- Macro-ize as much as possible for above (aka finish cleanups)
- Fix paths in init scripts and logrotate and xinetd
- Fix provides and obsoletes so as to provide samba, but not obsolete
  current stable until we have a stable release (when it's the system samba).
- Add warnings to descriptions when not system samba.
- This is now parallel installable with the normal samba release, for easy
  testing. It shouldn't touch existing installations. Of course, only
  one samba at a time on the same interface!

* Sat Sep 28 2002 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-0.alpha20.1mdk
- Merge with 2.2.6pre2.2mdk
- Detect alpha- and beta-, along with pre-releases

* Tue Feb 05 2002 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha14-0.1mdk
- Sync with 2.2.3-2mdk (new --without options, detect when 
  building for a different distribution.

* Mon Feb 04 2002 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha14-0.0mdk
- Sync with 2.2.2-10mdk, which added build-time options --with ldap,
  winbind, acl, wins, mdk72, mdk80, mdk81, mdk82, cooker. Added
  warning in description if built with these options.

* Wed Jan 23 2002 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha13-0.2mdk
- Added if's for build_ads, which hopefully will add Active Directory
  Support (by request).

* Thu Jan 17 2002 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha13-0.1mdk
- More syncing with 2.2 rpm (post and postun scripts)
- Testing without ldap

* Thu Jan 17 2002 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha13-0.0mdk
- 3.0-alpha13
- Fixed installman.sh patch.

* Wed Jan 09 2002 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha12-0.1mdk
- Fixed %post and %preun for nss_wins, added %post and %preun for
  samba-winbind (chkconfig and winbind entries in nsswitch.conf)

* Sun Dec 23 2001 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha12-0.0mdk
- 3.0-alpha12
- Sync up with changes made in 2.2.2 to support Mandrake 8.0, 7.2
- Added new subpackage for swat
- More if's for ldap.

* Thu Dec 20 2001 Buchan Milne <bgmilne@cae.co.za> 3.0-alpha11-0.0mdk
- 3.0-alpha11

* Wed Dec 19 2001 Buchan Milne <bgmilne@cae.co.za> 3.0alpha10-0.0mdk
- 3.0-alpha10

* Tue Dec 18 2001 Buchan Milne <bgmilne@cae.co.za> 3.0alpha9-0.0mdk
- 3.0-alpha9

* Mon Dec 17 2001 Buchan Milne <bgmilne@cae.co.za> 3.0alpha8-0.1mdk
- Added net command to %files common, pdbedit and smbgroupedit to
  %files, s/%{prefix}\/bin/%{_bindir}/ (the big cleanup).
  Added patch to smb.init from 2.2.2 (got missed with 3.0-alpha1 patches)

* Sun Dec 16 2001 Buchan Milne <bgmilne@cae.co.za> 3.0alpha8-0.0mdk
- Patch for installman.sh to handle lang=en correctly (p24)
- added --with-manpages-langs=en,ja,pl (translated manpages), but there
  aren't any manpages for these languages yet ... so we still
  need %dir and %doc entries for them ...
- patch (p25) to configure.in to support more than 2 languages.
- addtosmbpass seems to have returned for now, but make_* have disappeared!

* Fri Dec 14 2001 Buchan Milne <bgmilne@cae.co.za> 3.0alpha6-0.0mdk
- DESTDIR patch for Makefile.in (p23), remove a lot of %%install scripts
  this forces move of smbcontrol and smbmnt to %{prefix}/bin
  removed --with-pam_smbpass as it doesn't compile.

* Thu Dec 06 2001 Buchan Milne <bgmilne@cae.co.za> 3.0-0.0alpha1mdk
- Samba 3.0alpha1 released (we missed Samba 3.0alpha0!)
- Redid smbmount-sbin patch and smb.conf patch (20), removed xfs quota patch 
  (applied upstream), removed ook-patch (codepage directory totally different).
- Added winbind.init (21) and system-auth-winbind.pamd (22). Patches 20-23 
  should be applied upstream before 3.0 ships ...

* Wed Dec 05 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.2-6mdk
- fixed typo in system-auth-winbind.pamd (--Thanks J. Gluck).
- fixed %post xxx problem (smb not started in chkconfig --Thanks Viet & B. Kenworthy).

* Fri Nov 23 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.2-5mdk
- Had to remove the network recycle bin patch: it seems to mess up 
  file deletion from windows (files appear to be "already in use")

* Tue Nov 13 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.2-4mdk
- added network recycle bin patch:
  <http://www.amherst.edu/~bbstone/howto/samba.html>
- added "recycle bin = .recycled" parameter in smb.conf [homes].
- fixed winbind/nss_wins perms (oh no I don't own that stuff ;o)

* Mon Nov 12 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.2-3mdk
- added %build 8.0 and 7.2, for tweakers to play around.
- changed configure options:
  . removed --with-mmap, --with-netatalk (obsolete).
  . added --with-msdfs, --with-vfs (seems stable, but still need testing).

* Mon Nov 12 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.2-2mdk
- rebuilt with winbind and nss_wins enabled.

* Wed Oct 31 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.2-1mdk
- Rebuilt on cooker.

* Wed Oct 31 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.992mdk
- Patch for smb.conf to fix incorrect lpq command, typo in winbind,
  and add sample linpopup command. Added print driver directories.
- New XFS quota patch (untested!, samba runs, but do quotas work? We
  can't check yet since the kernel doesn't seem to support XFS quotas!)

* Fri Oct 19 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.2-0.99mdk
- New samba.spec, almost ready for winbind operations. OLA for Buchan Milne
  Who did a tremendous integration work on 2.2.2.
  Rebuild on cooker, please test XFS (ACLs and quotas) again...
  
* Mon Oct 15 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.9mdk
- Samba-2.2.2. released! Use %defines to determine which subpackages
  are built and which Mandrake release we are buiding on/for (hint: define 
  build_mdk81 1 for Mandrake 8.1 updates)

* Sun Oct 14 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.20011014mdk
- %post and %postun for nss_wins

* Wed Oct 10 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.20011010mdk
- New CVS snapshot, /etc/pam.d/system-auth-winbind added
  with configuration to allow easy winbind setup.
  
* Sun Oct 7 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.20011007mdk
- Added new package nss_wins and moved smbpasswd to common (required by
  winbind).

* Sat Oct 6 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.20011006mdk
- Added new package winbind.

* Mon Oct 1 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.20011001mdk
- Removed patch to smb init.d file (applied in cvs)

* Sun Sep 30 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.20010930mdk
- Added winbind init script, which still needs to check for running nmbd.

* Thu Sep 27 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.2-0.20010927mdk
- Built from samba-2.2.2-pre cvs, added winbindd, wbinfo, nss_winbind and 
  pam_winbind, moved pam_smbpass from samba-common to samba. We still
  need a start-up script for winbind, or need to modify existing one.
  
* Mon Sep 10 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1a-15mdk
- Enabled acl support (XFS acls now supported by kernel-2.4.8-21mdk thx Chmou)
  Added smbd patch to support XFS quota (Nathan Scott)
  
* Mon Sep 10 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1a-14mdk
- Oops! smbpasswd created in wrong directory...

* Tue Sep 06 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1a-13mdk
- Removed a wrong comment in smb.conf.
  Added creation of smbpasswd during install.

* Mon Aug 27 2001 Pixel <pixel@mandrakesoft.com> 2.2.1a-12mdk
- really less verbose %%post

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.1a-11mdk
- Fix shared libs in /usr/bin silliness.

* Thu Aug 23 2001 Pixel <pixel@mandrakesoft.com> 2.2.1a-10mdk
- less verbose %%post

* Wed Aug 22 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.1a-9mdk
- Added smbcacls (missing in %files), modification to smb.conf: ([printers]
  is still needed, even with point-and-print!, user add script should
  use name and not gid, since we may not get the gid . New script for
  putting manpages in place (still need to be added in %files!). Moved
  smbcontrol to sbin and added it and its man page to %files.

* Wed Aug 22 2001 Pixel <pixel@mandrakesoft.com> 2.2.1a-8mdk
- cleanup /var/lib/samba/codepage/src

* Tue Aug 21 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1a-7mdk
- moved codepage generation to %%install and codepage dir to /var/lib/samba

* Tue Aug 21 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1a-6mdk
- /lib/* was in both samba and samba-common
  Introducing samba-doc: "alas, for the sake of thy modem, shalt thou remember
  when Samba was under the Megabyte..."

* Fri Aug 03 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1a-5mdk
- Added "the gc touch" to smbinit through the use of killall -0 instead of
  grep cupsd | grep -v grep (too many greps :o)

* Wed Jul 18 2001 Stefan van der Eijk <stefan@eijk.nu> 2.2.1a-4mdk
- BuildRequires: libcups-devel
- Removed BuildRequires: openssl-devel

* Fri Jul 13 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1a-3mdk
- replace chkconfig --add/del with --level 35 on/reset.

* Fri Jul 13 2001 Geoffrey Lee <snailtalk@mandrakesoft.cm> 2.2.1a-2mdk
- Replace discription s/inetd/xinetd/, we all love xinetd, blah.

* Thu Jul 12 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.1a-1mdk
- Bugfix release. Fixed add user script, added print$ share and printer admin
  We need to test interaction of new print support with CUPS, but printer
  driver uploads should work.

* Wed Jul 11 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-17mdk
- fixed smb.conf a bit, rebuilt on cooker.

* Tue Jul 10 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.1-16mdk
- Finally, samba 2.2.1 has actually been release. At least we were ready!
  Cleaned up smb.conf, and added some useful entries for domain controlling.
  Migrated changes made in samba's samba2.spec for 2.2.1  to this file.
  Added groupadd command in post to create a group for samba machine accounts.
  (We should still check the postun, samba removes pam, logs and cache)

* Tue Jun 26 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-15mdk
- fixed smbwrapper compile options.

* Tue Jun 26 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-14mdk
- added LFS support.
  added smbwrapper support (smbsh)

* Wed Jun 20 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-13mdk
- /sbin/mount.smb and /sbin/mount.smbfs now point to the correct location
  of smbmount (/usr/bin/smbmount)

* Tue Jun 19 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-12mdk
- smbmount and smbumount are now in /usr/bin and SUID.
  added ||: to triggerpostun son you don't get error 1 anymore when rpm -e
  Checked the .bz2 sources with file *: everything is OK now (I'm so stupid ;o)!

* Tue Jun 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.2.1-11mdk
- s/Copyright/License/;
- Stop Sylvester from pretending .gz source to be .bz2 source via filename
  aka really bzip2 the source.

* Mon Jun 18 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-10mdk
- changed Till's startup script modifications: now samba is being reloaded
  automatically 1 minute after it has started (same reasons as below in 9mdk)
  added _post_ and _preun_ for service smb
  fixed creation of /var/lib/samba/{netlogon,profiles} (%dir was missing)

* Thu Jun 14 2001 Till Kamppeter <till@mandrakesoft.com> 2.2.1-9mdk
- Modified the Samba startup script so that in case of CUPS being used as
  printing system Samba only starts when the CUPS daemon is ready to accept
  requests. Otherwise the CUPS queues would not appear as Samba shares.

* Mon Jun 11 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-8mdk
- patched smbmount.c to have it call smbmnt in sbin (thanks Seb).

* Wed May 30 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-7mdk
- put SWAT menu icons back in place.

* Mon May 28 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-6mdk
- OOPS! fixed smbmount symlinks

* Mon May 28 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-5mdk
- removed inetd postun script, replaced with xinetd.
  updated binary list (smbcacls...)
  cleaned samba.spec

* Mon May 28 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.1-4mdk
- Changed configure options to point to correct log and codepage directories,
  added crude script to fix logrotate file for new log file names, updated
  patches to work with current CVS.

* Thu May 24 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-3mdk
- Cleaned and updated the %files section.

* Sat May 19 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.1-2mdk
- Moved all samba files from /etc to /etc/samba (Thanks DomS!).
  Fixed fixinit patch (/etc/samba/smb.conf)

* Fri May 18 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.1-1mdk
- Now use packaging/Mandrake/smb.conf, removed unused and obsolete
  patches, moved netlogon and profile shares to /var/lib/samba in the
  smb.conf to match the spec file. Added configuration for ntlogon to
  smb.conf. Removed pam-foo, fixinit and makefilepath patches. Removed
  symlink I introduced in 2.2.0-1mdk

* Thu May 3 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.0-5mdk
- Added more configure options. Changed Description field (thx John T).

* Wed Apr 25 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.0-4mdk
- moved netlogon and profiles to /var/lib/samba by popular demand ;o)

* Tue Apr 24 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.0-3mdk
- moved netlogon and profiles back to /home.

* Fri Apr 20 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.2.0-2mdk
- fixed post inetd/xinetd script&

* Thu Apr 19 2001 Buchan Milne <bgmilne@cae.co.za> 2.2.0-1mdk
- Upgrade to 2.2.0. Merged most of 2.0.7-25mdk's patches (beware
  nasty "ln -sf samba-%{ver} ../samba-2.0.7" hack to force some patches
  to take. smbadduser and addtosmbpass seem to have disappeared. Moved
  all Mandrake-specific files to packaging/Mandrake and made patches
  from those shipped with samba. Moved netlogon to /home/samba and added
  /home/samba/profiles. Added winbind,smbfilter and debug2html to make command.

* Thu Apr 12 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0.7-25mdk
- Fix menu entry and provide separate menu entry for GNOME
  (nautilus doesn't support HTTP authentication yet)
- Add icons in package

* Fri Mar 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.0.7-24mdk
- use new server macros

* Wed Mar 21 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-23mdk
- check whether /etc/inetd.conf exists (upgrade) or not (fresh install).

* Thu Mar 15 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-22mdk
- spec cosmetics, added '-r' option to lpr-cups command line so files are
  removed from /var/spool/samba after printing.

* Tue Mar 06 2001 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-21mdk
- merged last rh patches.

* Thu Nov 23 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-20mdk
- removed dependencies on cups and cups-devel so one can install samba without using cups
- added /home/netlogon

* Mon Nov 20 2000 Till Kamppeter <till@mandrakesoft.com> 2.0.7-19mdk
- Changed default print command in /etc/smb.conf, so that the Windows
  driver of the printer has to be used on the client.
- Fixed bug in smbspool which prevented from printing from a
  Linux-Samba-CUPS client to a Windows server through the guest account.

* Mon Oct 16 2000 Till Kamppeter <till@mandrakesoft.com> 2.0.7-18mdk
- Moved "smbspool" (Samba client of CUPS) to the samba-client package

* Sat Oct 7 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.0.7-17mdk
- Added RedHat's "quota" patch to samba-glibc21.patch.bz2, this fixes
  quota related compile problems on the alpha.

* Wed Oct 4 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-16mdk
- Fixed 'guest ok = ok' flag in smb.conf

* Tue Oct 3 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-15mdk
- Allowed guest account to print in smb.conf
- added swat icon in menu

* Tue Oct 3 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-14mdk
- Removed rh ssl patch and --with-ssl flag: not appropriate for 7.2

* Tue Oct 3 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-13mdk
- Changed fixinit patch.
- Changed smb.conf for better CUPS configuration.
- Thanks Fred for doing this ---vvv.

* Tue Oct  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.0.7-12mdk
- menu entry for web configuration tool.
- merge with rh: xinetd + ssl + pam_stack.
- Added smbadduser rh-bugfix w/o relocation of config-files.

* Mon Oct  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.0.7-11mdk
- added build requires on cups-devel and pam-devel.

* Mon Oct  2 2000 Till Kamppeter <till@mandrakesoft.com> 2.0.7-10mdk
- Fixed smb.conf entry for CUPS: "printcap name = lpstat", "lpstats" was
  wrong.

* Mon Sep 25 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-9mdk
- Cosmetic changes to make rpmlint more happy

* Wed Sep 11 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-8mdk
- added linkage to the using_samba book in swat

* Fri Sep 01 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-7mdk
- Added CUPS support to smb.conf
- Added internationalization options to smb.conf [Global]

* Wed Aug 30 2000 Till Kamppeter <till@mandrakesoft.com> 2.0.7-6mdk
- Put "smbspool" to the files to install

* Wed Aug 30 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-5mdk
- Did some cleaning in the patches

* Fri Jul 28 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-4mdk
- relocated man pages from /usr/man to /usr/share/man for compatibility reasons

* Fri Jul 28 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-3mdk
- added make_unicodemap and build of unicode_map.$i in the spec file

* Fri Jul 28 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-2mdk
- renamed /etc/codepage/codepage.$i into /etc/codepage/unicode_map.$i to fix smbmount bug.

* Fri Jul 07 2000 Sylvestre Taburet <staburet@mandrakesoft.com> 2.0.7-1mdk
- 2.0.7

* Wed Apr 05 2000 Francis Galiegue <fg@mandrakesoft.com> 2.0.6-4mdk

- Titi sucks, does not put versions in changelog
- Fixed groups for -common and -client
- /usr/sbin/samba is no config file

* Thu Mar 23 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>
- fix buggy post install script (pixel)

* Fri Mar 17 2000 Francis Galiegue <francis@mandrakesoft.com> 2.0.6-2mdk

- Changed group according to 7.1 specs
- Some spec file changes
- Let spec-helper do its job

* Thu Nov 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.0.6.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh changes.
- Split in 3 packages.

* Fri Aug 13 1999 Pablo Saratxaga <pablo@@mandrakesoft.com>
- corrected a bug with %post (the $1 parameter is "1" in case of
  a first install, not "0". That parameter is the number of packages
  of the same name that will exist after running all the steps if nothing
  is removed; so it is "1" after first isntall, "2" for a second install
  or an upgrade, and "0" for a removal)

* Wed Jul 28 1999 Pablo Saratxaga <pablo@@mandrakesoft.com>
- made smbmnt and smbumount suid root, and only executable by group 'smb'
  add to 'smb' group any user that should be allowed to mount/unmount
  SMB shared directories

* Fri Jul 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.0.5a (bug security fix).

* Wed Jul 21 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 2.0.5
- cs/da/de/fi/fr/it/tr descriptions/summaries

* Sun Jun 13 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 2.0.4b
- recompile on a system that works ;)

* Wed Apr 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.
- Bzip2 man-pages.

* Fri Mar 26 1999 Bill Nottingham <notting@redhat.com>
- add a mount.smb to make smb mounting a little easier.
- smb filesystems apparently do not work on alpha. Oops.

* Thu Mar 25 1999 Bill Nottingham <notting@redhat.com>
- always create codepages

* Tue Mar 23 1999 Bill Nottingham <notting@redhat.com>
- logrotate changes

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- updated init script to use graceful restart (not stop/start)

* Tue Mar  9 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.3

* Thu Feb 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.2

* Mon Feb 15 1999 Bill Nottingham <notting@redhat.com>
- swat swat

* Tue Feb  9 1999 Bill Nottingham <notting@redhat.com>
- fix bash2 breakage in post script

* Fri Feb  5 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.0

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- make sure all binaries are stripped

* Thu Sep 17 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.9.18p10.
- fix %triggerpostun.

* Tue Jul 07 1998 Erik Troan <ewt@redhat.com>
- updated postun triggerscript to check $0
- clear /etc/codepages from %preun instead of %postun

* Mon Jun 08 1998 Erik Troan <ewt@redhat.com>
- made the %postun script a tad less agressive; no reason to remove
  the logs or lock file (after all, if the lock file is still there,
  samba is still running)
- the %postun and %preun should only exectute if this is the final
  removal
- migrated %triggerpostun from Red Hat's samba package to work around
  packaging problems in some Red Hat samba releases

* Sun Apr 26 1998 John H Terpstra <jht@samba.anu.edu.au>
- minor tidy up in preparation for release of 1.9.18p5
- added findsmb utility from SGI package

* Wed Mar 18 1998 John H Terpstra <jht@samba.anu.edu.au>
- Updated version and codepage info.
- Release to test name resolve order

* Sat Jan 24 1998 John H Terpstra <jht@samba.anu.edu.au>
- Many optimisations (some suggested by Manoj Kasichainula <manojk@io.com>
- Use of chkconfig in place of individual symlinks to /etc/rc.d/init/smb
- Compounded make line
- Updated smb.init restart mechanism
- Use compound mkdir -p line instead of individual calls to mkdir
- Fixed smb.conf file path for log files
- Fixed smb.conf file path for incoming smb print spool directory
- Added a number of options to smb.conf file
- Added smbadduser command (missed from all previous RPMs) - Doooh!
- Added smbuser file and smb.conf file updates for username map
