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
%define version		3.0.25a
%define release		%_revrel

%define smbldapver	0.9.2
%define vscanver	0.3.6c-beta4
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
Source0:        http://us1.samba.org/samba/ftp/stable/samba-%{version}.tar.gz
Source1:        http://us1.samba.org/samba/ftp/stable/samba-%{version}.tar.asc
Source2:        samba.log
Source3:        samba-vscan-%{vscanver}.tar.bz2
Source4:        samba-print-pdf.sh
Source5:        swat.run
Source6:        swat-log.run
Source7:        smbd.run
Source8:        smbd-log.run
Source9:        nmbd.run
Source10:       nmbd-log.run
Source11:       winbindd.run
Source12:       winbindd-log.run
Source13:       smb-migrate
Source14:       README.avx.sambamerge
Source15:	smbusers
Source16:	smbprint
Source17:	findsmb
Source18:	smb.init
Source19:	winbind.init
Source20:	wrepld.init
Source21:	samba.pamd
Source22:	system-auth-winbind.pamd
Source23:	smb.conf
Source24:	smb.conf_full
Patch2:         smbldap-tools-0.9.1-mdkconfig.patch
Patch4:         samba-3.0-smbmount-sbin.patch
Patch6:         samba-3.0.6-mdk-smbmount-unixext.patch
Patch7:         samba-3.0.23-mdv-revert-libsmbclient-move.patch
Patch8:         samba-3.0.20-avx-annvix-config.patch
Patch11:	samba-3.0-mandriva-packaging.patch
Patch13:	http://samba.org/~metze/samba3-default-quota-ignore-error-01.diff
Patch14:	samba-3.0.25-CVE-2007-4138.patch
Patch15:	samba-3.0.25b-CVE-2007-4572.patch
Patch16:	samba-CVE-2007-5398.patch
Patch17:	samba-cvs-bug5087.patch
Patch18:	samba-3.0.27a-git-regression-fix.patch
Patch19:	samba3-deb-regression-fix.patch
Patch20:	samba-CVE-2007-6015.patch

BuildRoot:      %{_buildroot}/%{name}-%{version}
BuildRequires:  pam-devel
BuildRequires:	readline-devel
BuildRequires:	libncurses-devel
BuildRequires:	popt-devel
BuildRequires:  libxml2-devel
BuildRequires:  libacl-devel
BuildRequires:  libldap-devel
BuildRequires:	krb5-devel

Requires:       pam >= 0.64
Requires:	samba-common = %{version}
Requires:	srv >= 0.7
Requires(pre):	mktemp
Requires(pre):	psmisc
Requires(pre):	fileutils
Requires(pre):	sed
Requires(pre):	grep

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
Requires:       %{name}-common = %{version}
Requires:	perl-Crypt-SmbHash
Requires:	libxml2
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
Provides:       samba3-common
Obsoletes:      samba3-common

%description common
Samba-common provides files necessary for both the server and client
packages of Samba. 


%package swat
Summary:        The Samba Web Administration Tool
Group:          System/Servers
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
Requires:       %{name}-common = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description winbind
Provides the winbind daemon and testing tools to allow authentication
and group/user enumeration from a Windows or Samba domain controller.


%package -n nss_wins
Summary:        Name Service Switch service for WINS
Group:          System/Servers
Requires:       %{name}-common = %{version}
Requires(post):	glibc

%description -n nss_wins
Provides the libnss_wins shared library which resolves NetBIOS names to
IP addresses.


%package -n %{libname}
Summary:        SMB Client Library
Group:          System/Libraries
Provides:       libsmbclient

%description -n %{libname}
This package contains the SMB client library, part of the samba
suite of networking software, allowing other software to access
SMB shares.


%package -n %{libname}-devel
Summary:        SMB Client Library Development files
Group:          Development/C
Provides:       libsmbclient-devel
Requires:       %{libname} = %{version}-%{release}

%description -n %{libname}-devel
This package contains the development files for the SMB client
library, part of the samba suite of networking software, allowing
the development of other software to access SMB shares.


%package -n %{libname}-static-devel
Summary:        SMB Client Static Library Development files
Group:          System/Libraries
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
%setup -q -a 3
pushd examples/LDAP/smbldap-tools-%{smbldapver}
%patch2 -p1
popd
%patch4 -p1 -b .sbin
%patch6 -p1 -b .unixext
%patch7 -p1 -b .libsmbdir
%patch11 -p1 -b .mdk
%patch8 -p1 -b .avx
pushd source
%patch13
popd
%patch14 -p1 -b .cve-2007-4138
%patch15 -p1 -b .cve-2007-4572
%patch16 -p1 -b .cve-2007-5398
%patch17 -p0 -b .bug5087
%patch18 -p1 -b .regression-git
%patch19 -p1 -b .regression-deb
%patch20 -p1 -b .cve-2007-6015

# patches from cvs/samba team

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
    CFLAGS="`echo "%{optflags}"|sed -e 's/-g//g'` -DLDAP_DEPRECATED"

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
        --with-shared-modules=idmap_rid,idmap_ad
#	--with-expsam=xml \

    #Fix the make file so we don't create debug information
    perl -pi -e 's/-g //g' Makefile

    perl -pi -e 's|-Wl,-rpath,%{_libdir}||g;s|-Wl,-rpath -Wl,%{_libdir}||g' Makefile

    make proto_exists
    %make all libsmbclient smbfilter wins modules bin/smbget
#client/mount.cifs client/umount.cifs
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
        PAMMODULESDIR=/%{_lib}/security \
        ROOTSBINDIR=/bin \
        install installclientlib installmodules
popd

#install -m 0755 source/bin/smbget %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_datadir}/swat/using_samba

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

install -m 0755 source/bin/lib*.a %{buildroot}%{_libdir}/
pushd $RPM_BUILD_ROOT/%{_libdir}                                                                                                                                                   
    [ -f libsmbclient.so ] && mv -f libsmbclient.so libsmbclient.so.%{lib_major}                                                                                                     
    ln -sf libsmbclient.so.%{lib_major} libsmbclient.so                                                                                                                              
popd

# smbsh forgotten
#install -m 0755 source/bin/smbsh %{buildroot}%{_bindir}/

%makeinstall_std -C %{vfsdir}/%{vscandir}
install -m 0644 %{vfsdir}/%{vscandir}/*/vscan-*.conf %{buildroot}%{_sysconfdir}/%{name}

# libnss_* still not handled by make:
# Install the nsswitch library extension file
for i in wins winbind; do
    install -m 0755 source/nsswitch/libnss_${i}.so %{buildroot}/%{_lib}/libnss_${i}.so
done
# Make link for wins and winbind resolvers
( cd %{buildroot}/%{_lib}; ln -s libnss_wins.so libnss_wins.so.2; ln -s libnss_winbind.so libnss_winbind.so.2)

# Install other stuff
install -m 0644 %{_sourcedir}/smbusers %{buildroot}%{_sysconfdir}/%{name}/smbusers
install -m 0755 %{_sourcedir}/smbprint %{buildroot}%{_bindir}
install -m 0755 %{_sourcedir}/findsmb %{buildroot}%{_bindir}
install -m 0755 %{_sourcedir}/smb.init %{buildroot}%{_sbindir}/%{name}
install -m 0755 %{_sourcedir}/winbind.init %{buildroot}%{_sbindir}/winbind
install -m 0644 %{_sourcedir}/samba.pamd %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 0644 %{_sourcedir}/system-auth-winbind.pamd %{buildroot}%{_sysconfdir}/pam.d/system-auth-winbind
install -m 0644 %{_sourcedir}/samba.log %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# install pam_winbind.conf sample file
mkdir -p %{buildroot}%{_sysconfdir}/security
install -m 0644 examples/pam_winbind/pam_winbind.conf %{buildroot}%{_sysconfdir}/security/pam_winbind.conf

# make a conf file for winbind from the default one:
cat %{_sourcedir}/smb.conf_full|sed -e  's/^;  winbind/  winbind/g;s/^;  obey pam/  obey pam/g;s/   printer admin = @adm/#  printer admin = @adm/g; s/^#   printer admin = @"D/   printer admin = @"D/g;s/^;   password server = \*/   password server = \*/g;s/^;  template/  template/g; s/^   security = user/   security = domain/g' > smb-winbind.conf
install -m 0644 smb-winbind.conf %{buildroot}%{_sysconfdir}/%{name}/smb-winbind.conf
install -m 0644 %{_sourcedir}/smb.conf_full %{buildroot}%{_sysconfdir}/%{name}/smb.conf_full

# install mount.cifs
for i in mount.cifs umount.cifs
do
    install -m 0755 source/bin/$i %{buildroot}/bin/$i
    ln -s ../bin/$i %{buildroot}/sbin/$i
done

echo 127.0.0.1 localhost > %{buildroot}%{_sysconfdir}/%{name}/lmhosts

# Link smbspool to CUPS (does not require installed CUPS)

mkdir -p %{buildroot}%{_prefix}/lib/cups/backend
ln -s %{_bindir}/smbspool %{buildroot}%{_prefix}/lib/cups/backend/smb

# ipsvd support
mkdir -p %{buildroot}%{_srvdir}/swat/{log,env,peers}
install -m 0740 %{_sourcedir}/swat.run %{buildroot}%{_srvdir}/swat/run
install -m 0740 %{_sourcedir}/swat-log.run %{buildroot}%{_srvdir}/swat/log/run
touch %{buildroot}%{_srvdir}/swat/peers/0
chmod 0640 %{buildroot}%{_srvdir}/swat/peers/0


echo "901" >%{buildroot}%{_srvdir}/swat/env/PORT

cp %{_sourcedir}/samba-print-pdf.sh %{buildroot}%{_datadir}/%{name}/scripts/print-pdf
cp %{_sourcedir}/smb-migrate %{buildroot}%{_datadir}/%{name}/scripts/smb-migrate

rm -f %{buildroot}%{_sbindir}/mount.smbfs
# Link smbmount to /sbin/mount.smb and /sbin/mount.smbfs
# I don't think it's possible for make to do this ...
pushd %{buildroot}/sbin
    ln -s ..%{_bindir}/smbmount mount.smb
    ln -s ..%{_bindir}/smbmount mount.smbfs
popd

mkdir -p %{buildroot}%{_srvdir}/{smbd,nmbd,winbindd}/log
install -m 0740 %{_sourcedir}/smbd.run %{buildroot}%{_srvdir}/smbd/run
install -m 0740 %{_sourcedir}/smbd-log.run %{buildroot}%{_srvdir}/smbd/log/run
install -m 0740 %{_sourcedir}/nmbd.run %{buildroot}%{_srvdir}/nmbd/run
install -m 0740 %{_sourcedir}/nmbd-log.run %{buildroot}%{_srvdir}/nmbd/log/run
install -m 0740 %{_sourcedir}/winbindd.run %{buildroot}%{_srvdir}/winbindd/run
install -m 0740 %{_sourcedir}/winbindd-log.run %{buildroot}%{_srvdir}/winbindd/log/run

install -m 0640 %{_sourcedir}/smb.conf %{buildroot}%{_sysconfdir}/samba/smb.conf

# Clean up unpackaged files:
#for i in %{_bindir}/pam_smbpass.so %{_bindir}/smbwrapper.so %{_mandir}/man1/editreg*;do
for i in %{_mandir}/man1/editreg*;do
    rm -f %{buildroot}/$i
done
rm -f %{buildroot}%{_sysconfdir}/%{name}/vscan-{symantec,fprotd,fsav,kavp,mcdaemon,mks32,oav,sophos,trend,antivir}.conf

# install html man pages for swat
mkdir -p %{buildroot}/%{_datadir}/swat/help/manpages

# the binary gets removed ... but not the man page ...
rm -f %{buildroot}%{_mandir}/man1/testprns*


# (sb) make a smb.conf.clean we can use for the merge, since an existing
# smb.conf won't get overwritten
cp %{buildroot}%{_sysconfdir}/%{name}/smb.conf %{buildroot}%{_datadir}/%{name}/smb.conf.clean

# (sb) leave a README.avx.conf to explain what has been done
cp %{_sourcedir}/README.avx.sambamerge %{buildroot}%{_datadir}/%{name}/README.avx.conf

mkdir -p %{buildroot}%{_srvdir}/smbd/depends
%_mkdepends smbd nmbd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post server
%_post_srv nmbd
%_post_srv smbd

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
%_preun_srv nmbd
%_preun_srv smbd


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
%{_libdir}/%{name}/auth
%{_libdir}/%{name}/fi.msg
%dir %{_libdir}/%{name}/nss_info
%{_libdir}/%{name}/nss_info/rfc2307.so
%{_libdir}/%{name}/nss_info/sfu.so
%{_libdir}/%{name}/*.so

%{_mandir}/man1/profiles.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man7/samba.7*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/idmap_ad.8*
%{_mandir}/man8/idmap_ldap.8*
%{_mandir}/man8/idmap_nss.8*
%{_mandir}/man8/idmap_rid.8*
%{_mandir}/man8/idmap_tdb.8*
%{_mandir}/man8/vfs_audit.8*
%{_mandir}/man8/vfs_cacheprime.8*
%{_mandir}/man8/vfs_cap.8*
%{_mandir}/man8/vfs_catia.8*
%{_mandir}/man8/vfs_commit.8*
%{_mandir}/man8/vfs_default_quota.8*
%{_mandir}/man8/vfs_extd_audit.8*
%{_mandir}/man8/vfs_fake_perms.8*
%{_mandir}/man8/vfs_full_audit.8*
%{_mandir}/man8/vfs_gpfs.8*
%{_mandir}/man8/vfs_netatalk.8*
%{_mandir}/man8/vfs_notify_fam.8*
%{_mandir}/man8/vfs_prealloc.8*
%{_mandir}/man8/vfs_readahead.8*
%{_mandir}/man8/vfs_readonly.8*
%{_mandir}/man8/vfs_recycle.8*
%{_mandir}/man8/vfs_shadow_copy.8*
%attr(775,root,adm) %dir %{_localstatedir}/%{name}/netlogon
%attr(755,root,root) %dir %{_localstatedir}/%{name}/profiles
%attr(755,root,root) %dir %{_localstatedir}/%{name}/printers
%attr(2775,root,adm) %dir %{_localstatedir}/%{name}/printers/*
%attr(1777,root,root) %dir /var/spool/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%attr(0755,root,root) %{_datadir}/%{name}/scripts/print-pdf

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
%{_bindir}/eventlogadm
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
%{_mandir}/man8/eventlogadm.8*
# Link of smbspool to CUPS
%{_prefix}/lib/cups/backend/smb

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
%{_mandir}/man8/tdbtool.8*
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
%{_mandir}/man7/pam_winbind*.7*
%{_mandir}/man8/winbindd*.8*
%{_mandir}/man1/wbinfo*.1*
%dir %attr(0750,root,admin) %{_srvdir}/winbindd
%dir %attr(0750,root,admin) %{_srvdir}/winbindd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/winbindd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/winbindd/log/run
%config(noreplace) %{_sysconfdir}/security/pam_winbind.conf

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
%{_mandir}/man7/libsmbclient.7*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%files vscan-clamav
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-clamav.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-clamav.conf

%files vscan-icap
%defattr(-,root,root)
%{_libdir}/%{name}/vfs/vscan-icap.so
%config(noreplace) %{_sysconfdir}/%{name}/vscan-icap.conf


%changelog
* Thu Dec 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.25a
- P20: security fix for CVE-2007-6015

* Tue Nov 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.25a
- P18: another regression fix from the samba team
- P19: another regression fix from Debian

* Wed Nov 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.25a
- P17: patch to fix samba bug #5087 (regression in fix for CVE-2007-4572)

* Sat Nov 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.25a
- P15: security fix for CVE-2007-4572
- P16: security fix for CVE-2007-5398

* Sun Sep 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.25a
- P14: security fix for CVE-2007-4138

* Tue Jun 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.25a
- 3.0.25a (security fixes for CVE-2007-2444, CVE-2007-2446, CVE-2007-2447)
- drop the socket options in smb.conf (Mandriva bug #28459)
- drop P1; the target isn't available anymore
- vscan 0.3.6c-beta4 (this one builds with this version of samba)
- updated P13 from Mandriva

* Tue Feb 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.24
- 3.0.24 (security fix for CVE-2007-0452, CVE-2007-0454)

* Sat Jan 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23d
- restart nmbd first, then smbd because smbd depends on nmbd

* Sat Jan 27 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23d
- remove "guest" from the default passdb entry in smb.conf and smb.conf_full
  as per http://lists.samba.org/archive/samba/2006-August/123755.html --
  otherwise smbd will dump core when running (very bad behaviour but at
  least this fixes it)

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23d
- build against new libxml2

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23d
- rebuild against new pam

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23d
- rebuild against new krb5

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23d
- 3.0.23d
- samba installs the lib as .so and .so.0 as the symlink when we want it the
  other way around
- split out the files in the packaging patch as their own source files
- drop P12; no longer relevant (old quota patch)
- drop P14; no longer required

* Sun Aug 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23a
- rebuild against new openldap 
- spec cleanups

* Mon Jul 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.23a
- 3.0.23a (fixes CVE-2006-3403)
- drop pdb_xml
- updated P7, P11 from Mandriva
- fix installation/build of {mount,umount}.cifs

* Sat Jun 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.22
- rebuild against new pam
- P14: update config for new pam

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0.22
- 3.0.22
- smbldap 0.91
- don't build against mysql or postgresql anymore
- fix pre-reqp
- update P2, P7 from Mandriva
- remove P5, P12, P14, P15, P16, P17, P18
- add new P12, P13
- move the cups backend directory to be /usr/lib/cups on both x86 and
  x86_64
- fix source urls and use the same .gz source the samba team does
- rebuild with gcc4

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
  also log to %%m.log rather than log.%%m so logs actually get rotated
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
