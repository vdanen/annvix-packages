%define name	cups
%define version	1.1.19
%define release	13sls

%define major	2
%define libname	%mklibname cups %{major}
%define real_version %{version}

%{!?build_opensls:%global build_opensls 0}

Summary:	Common Unix Printing System - Server package
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.cups.org
Source:		ftp://ftp.easysw.com/pub/cups/%{real_version}/%{name}-%{real_version}-source.tar.bz2
#Source:	ftp://ftp.easysw.com/pub/cups/%{real_version}/cups-cvs20030226.tar.bz2
# Small C program to get list of all installed PPD files
Source1:	poll_ppd_base.c.bz2
# Small C program to list the printer-specific options of a particular printer
Source2:	lphelp.c.bz2
# Icon for the Mandrake menu
Source3:	cups.png.bz2
# Complete replacement for startup script to have it the
# Mandrake way
Source5:	cups.startup.bz2
# Script for cleaning up the PPD files
Source6:	cleanppd.pl.bz2
# Perl script for automatic configuration of CUPS, especially access
# restrictions and broadcasting
Source7:	correctcupsconfig.bz2
# Downdated pstops filter due to problems with multiple page documents
#Source9:	pstops-1.1.6-3.c.bz2
# Backend filter for HPOJ from Mark Horn (mark@hornclan.com)
#Source10:	http://www.hornclan.com/~mark/cups/ptal.2002011801.bz2
# Backend filter for nprint (Novell client) from Mark Horn
# (mark@hornclan.com)
Source11:	http://www.hornclan.com/~mark/cups/nprint.2002011801.bz2
# AppleTalk/netatalk backend for CUPS
Source12:	http://www.oeh.uni-linz.ac.at/~rupi/pap/pap-backend.tar.bz2
Source13:	http://www.oeh.uni-linz.ac.at/~rupi/pap/pap-docu.pdf.bz2
Source14:	http://www.linuxprinting.org/download/printing/photo_print.bz2
Source15:	http://printing.kde.org/downloads/pdfdistiller.bz2
Source16:	cjktexttops.bz2
Source20:	cups.run
Source21:	cups-log.run
Patch1:		cups-1.1.15-cupsdconf.patch.bz2
Patch2:		cups-1.1.9-nopassword.patch.bz2
#Patch4:	cups-1.1.3-mimetypes.patch.bz2
#Patch5:	cups-1.1.3-mdktestpage.patch.bz2
Patch6:		cups-1.1.16-pamconfig.patch.bz2
#Patch6:	cups-1.1.3-pamconfig.patch.bz2
Patch7:		cups-1.1.5-documentationhtml.patch.bz2
Patch8:		cups-1.1.5-ENCRYPTIONtxt.patch.bz2
Patch9:		cups-1.1.6-lp-lpr.patch.bz2
#Patch10:	cups-1.1.6-3-cgi-bin.patch.bz2
#Patch11:	cups-1.1.6-pstoraster-gcc-2.96.patch.bz2
#Patch12:	cups-1.1.9-ownerships.patch.bz2
#Patch13:	cups-1.1.9-ipph-ippmaxattrvalues.patch.bz2
#Patch14:	cups-1.1.13-ipp-security.patch.bz2
#Patch15:	cups-1.1.15-lib64.patch.bz2
#Patch16:	cups-1.1.15-background.patch.bz2
#Patch17:	cups-1.1.15-a2ps-landscape-fix.patch.bz2
#Patch18:	cups-1.1.17-idefense.patch.bz2
#Patch19:	cups-1.1.18-usb-serialnumber.patch.bz2
#Patch20:	cups-1.1.18-hstrerror.patch.bz2
#Patch21:	cups-1.1.19-ipp.c.patch.bz2
Patch22:	cups-1.1.19-dont-broadcast-localhost.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	autoconf2.5, openssl-devel, pam-devel, libopenslp-devel

Requires:	%{libname} >= %{version}-%{release} cups-common >= %{version}-%{release} openssl net-tools
Requires:	printer-testpages
# To satisfy LSB/FHS
Provides:	lpddaemon

%description
The Common Unix Printing System provides a portable printing layer for 
UNIX(TM) operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces.
This is the main package needed for CUPS servers (machines where a
printer is connected to or which host a queue for a network
printer). It can also be used on CUPS clients so that they simply pick
up broadcasted printer information from other CUPS servers and do not
need to be assigned to a specific CUPS server by an
/etc/cups/client.conf file.

%package common
Summary:	Common Unix Printing System - Common stuff
License:	GPL
Group:		System/Servers
Requires:	%{libname} >= %{version}-%{release} rpm >= 3.0.4-6mdk /usr/sbin/update-alternatives openssl net-tools

%description common
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. It contains the command line utilities for
printing and administration (lpr, lpq, lprm, lpadmin, lpc, ...), man
pages, locales, and a sample configuration file for daemon-less CUPS
clients (/etc/cups/client.conf).

This package you need for both CUPS clients and servers. 

%package -n %{libname}
Summary:	Common Unix Printing System - CUPS library
License:	LGPL
Group:		System/Servers
Requires:	openssl net-tools
Obsoletes:	libcups1
Provides:	libcups1 = %{version}

%description -n %{libname}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).

This package you need for both CUPS clients and servers. It is also
needed by Samba.

%package -n %{libname}-devel
Summary:	Common Unix Printing System - Development environment "libcups"
License:	LGPL
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release} openssl openssl-devel
Provides:	libcups-devel = %{version}-%{release}
Obsoletes:	cups-devel, libcups1-devel
Provides:	cups-devel, libcups1-devel

%description -n %{libname}-devel
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This is the development package for
creating additional printer drivers, printing software, and other CUPS
services using the main CUPS library "libcups".

%package serial
Summary:	Common Unix Printing System - Backend for serial port printers
License:	GPL
Group:		System/Servers
Requires:	cups >= %{version}-%{release}

%description serial
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the backend filter
for printers on the serial ports. The auto-detection on the serial
ports takes several seconds (and so the startup time of the CUPS
daemon with this backend present) and therefore it is not recommended
to install this package when one has no serial port printer.


%prep

# Released version
rm -rf $RPM_BUILD_DIR/%{name}-%{real_version}
%setup -q -n %{name}-%{real_version}

#CVS version
rm -rf $RPM_BUILD_DIR/%{name}
#setup -q -n %{name}

# Downdated pstops filter due to problems with multiple page documents
#bzcat %{SOURCE9} > $RPM_BUILD_DIR/%{name}-%{real_version}/filter/pstops.c

# Do NEVER use cups.suse (this package is for Mandrake)
#cp -f data/cups.pam data/cups.suse

# Configure CUPS to allow broadcasting and access to the local printers
# from/to all machines in the local network, but no PPP-connected machines
# (as internet access)
%patch1 -p0
# Do changes that it is possible to use the CUPS WWW interface and
# KUPS also when root has no password (makes CUPS more convenient for
# home users without network
%patch2 -p0
# Apply a bugfix of HPGL recognition in /etc/cups/mime.types
#patch4 -p0
# "Mandrakize" test page
#patch5 -p0
# Adapt PAM configuration to Linux Mandrake
%patch6 -p1
# Link to the instructions for setting up encrypted connections on the
# documentation page of the web interface
%patch7 -p0
# Add some additional info to the instructions for setting up encrypted
# connections
%patch8 -p0
# Replace the job title "(stdin)" by "STDIM" when one prints out of 
# standard input with "lp" or "lpr". This caused problems when printing
# to a printer on a Windows server via Samba.
%patch9 -p0
# Fix bug of cgi-bin directory going into /etc/cups instead of into
# /usr/lib/cups
#patch10 -p0
# Insert missing "#include" directives in the code of "pstoraster". They are
# needed by gcc 2.96
#patch11 -p0
# "make install" tries to change ownerships with the "install" command.
# Removed these requests to allow the generation of an RPM as non-root.
#patch12 -p0
# On an IPP request any attribute of the request was limited to have not
# more than 100 values. On asking for the data for a particular printer
# one attribute contains all possible values for the "-o media" option of
# the CUPS lpr command, which are all possible paper sizes, sources, and
# types together. The Epson Stylus Photo 1290 (A3/11x17, Roll feeder) and 
# probably also the Epson Stylus Pro series (bigger than A3/11x17) with the
# GIMP-Print GhostScript driver provide already too many values. ->
# Raised the number of allowed values to 500. 
#patch13 -p0
#Security fix: Fix potential buffer overflow bug when the IPP backend
#reads the names of attributes.
#cd cups
#patch14 -p0
#cd ..
# Fix libdir for 64-bit architectures
#patch15 -p1 -b .lib64
mv config-scripts/cups-directories.m4 config-scripts/cups-directories.m4.orig
cat << EOF > config-scripts/cups-directories.m4
libdir=%{_libdir}
EOF
cat config-scripts/cups-directories.m4.orig >> \
	config-scripts/cups-directories.m4
# Need to regenerate configure script
WANT_AUTOCONF_2_5=1 autoconf
# Let the starter process of cupsd only exit when cupsd is ready to listen
# for requests.
cd scheduler
#patch16 
cd ..
# Fix bug of some applications (as a2ps) do not print correctly in Landscape
# orientation.
#patch17
# Security fixes based on a report from iDEFENSE.
#patch18
# Fix of determination of the printer's serial number in
# /proc/bus/usb/devices
#patch19 -p1
# Fix error reporting when gethostbyname fails
#patch20 -p0
# Fix daemon crash when one configures a printer with the web interface or
# adds a queue with the KDE Printing Manager
#patch21 -p1
# Make the CUPS daemon not sending broadcast packages with the host name
# "localhost". In this case the IP address of the appropriate interface
# is used.
%patch22 -p0

# Let the Makefile not trying to set file ownerships
perl -p -i -e "s/ -o \\$.CUPS_USER.//" scheduler/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" scheduler/Makefile
perl -p -i -e "s/ -o \\$.CUPS_USER.//" systemv/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" systemv/Makefile

# Fix a bug in swapping out parts of big images
#perl -p -i -e 's/cupsTempFd/cupsTempFile/' filter/image.c 
#perl -p -i -e 's/fdopen\(fd, "wb\+"\)/fopen\(img->cachename, "wb\+"\)/' filter/image.c

# Fix Makefiles for german and french translations
perl -p -i -e 's:images/:../images/:' doc/de/Makefile doc/fr/Makefile

# Accept readily filtered print jobs (e. g. from Windows clients)
perl -p -i -e 's:\#application/octet-stream:application/octet-stream:' conf/mime.*

# Load additional tools
bzcat %{SOURCE1} > poll_ppd_base.c
bzcat %{SOURCE2} > lphelp.c
# Load menu icon
bzcat %{SOURCE3} > cups.png
# Load Mandrake startup script
bzcat %{SOURCE5} > cups.startup
# Load HPOJ backend
#bzcat %{SOURCE10} > ptal
# Load nprint backend
bzcat %{SOURCE11} > nprint
# Load AppleTalk "pap" backend
%setup -q -T -D -a 12 -n %{name}-%{real_version}
#setup -q -T -D -a 12 -n %{name}
# Load the "pap" documentation
bzcat %{SOURCE13} > pap-docu.pdf
# Load the "photo_print" utility
bzcat %{SOURCE14} > photo_print
# Load the "pdfdistiller" utility
bzcat %{SOURCE15} > pdf
# Load the "cjktexttops" filter
bzcat %{SOURCE16} > cjktexttops

##### BUILD #####

%build
%serverbuild

# For 'configure' the macro is not used, because otherwise one does not get the
# /etc and /var directories correctly hardcoded into the executables (they
# would get /usr/etc and /usr/var. In addition, the "--with-docdir" option
# has to be given because the default setting is broken. "aclocal" and 
# "autoconf" are needed if we have a CVS snapshot.
aclocal
WANT_AUTOCONF_2_5=1 autoconf
./configure --libdir=%{_libdir} --enable-ssl --with-docdir=%{_defaultdocdir}/cups
%ifarch ia64 x86_64
export REAL_CFLAGS="$CFLAGS -fPIC"
%else
export REAL_CFLAGS="$CFLAGS"
%endif
%make LOGDIR=$RPM_BUILD_ROOT%{_var}/log/cups \
             REQUESTS=$RPM_BUILD_ROOT%{_var}/spool/cups \
             SERVERROOT=$RPM_BUILD_ROOT%{_sysconfdir}/cups \
             MANDIR=$RPM_BUILD_ROOT%{_mandir} \
             PAMDIR=$RPM_BUILD_ROOT%{_sysconfdir}/pam.d \
             BINDIR=$RPM_BUILD_ROOT%{_bindir} \
             SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
             INITDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
             DOCDIR=$RPM_BUILD_ROOT%{_defaultdocdir}/cups \
             CHOWN=/bin/echo OPTIM="$REAL_CFLAGS"

# Compile additional tools
gcc -opoll_ppd_base -I. -I./cups -L./cups -lcups poll_ppd_base.c
gcc -olphelp -I. -I./cups -L./cups -lcups lphelp.c


##### INSTALL #####

%install
rm -rf $RPM_BUILD_ROOT
%if !%{build_opensls}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
%endif

make install BUILDROOT=$RPM_BUILD_ROOT
	     LOGDIR=$RPM_BUILD_ROOT%{_var}/log/cups \
             REQUESTS=$RPM_BUILD_ROOT%{_var}/spool/cups \
             SERVERROOT=$RPM_BUILD_ROOT%{_sysconfdir}/cups \
             AMANDIR=$RPM_BUILD_ROOT%{_mandir} \
             PMANDIR=$RPM_BUILD_ROOT%{_mandir} \
             MANDIR=$RPM_BUILD_ROOT%{_mandir} \
             PAMDIR=$RPM_BUILD_ROOT%{_sysconfdir}/pam.d \
             BINDIR=$RPM_BUILD_ROOT%{_bindir} \
             SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
             INITDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
             DOCDIR=$RPM_BUILD_ROOT%{_defaultdocdir}/cups \
             CHOWN=/bin/echo

# Remove SUID bit from "lppasswd"
chmod 755 $RPM_BUILD_ROOT%{_bindir}/lppasswd

# Install the README files of the source tarball in the doc directory
chmod a+r *.txt
cp *.txt $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}

# Make a directory for the SSL files
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cups/ssl

# Install additional tools
install -m 755 poll_ppd_base $RPM_BUILD_ROOT%{_bindir}
install -m 755 lphelp $RPM_BUILD_ROOT%{_bindir}

# Install HPOJ backend
#install -m 755 ptal $RPM_BUILD_ROOT%{_libdir}/cups/backend/

# Install nprint backend
install -m 755 nprint $RPM_BUILD_ROOT%{_libdir}/cups/backend/

# Install AppleTalk backend
install -m 755 pap-backend/pap $RPM_BUILD_ROOT%{_libdir}/cups/backend/
install -m 644 pap-docu.pdf $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}

# Install "photo_print"
install -m 755 photo_print $RPM_BUILD_ROOT%{_bindir}

# Install "pdfdistiller"
install -m 755 pdf $RPM_BUILD_ROOT%{_libdir}/cups/backend/

# Install "cjktexttops"
install -m 755 cjktexttops $RPM_BUILD_ROOT%{_libdir}/cups/filter/

# Set link to test page in /usr/share/printer-testpages
rm -f $RPM_BUILD_ROOT%{_datadir}/cups/data/testprint.ps
ln -s %{_datadir}/printer-testpages/testprint.ps $RPM_BUILD_ROOT%{_datadir}/cups/data/testprint.ps

%if !%{build_opensls}
# install menu icon
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/locolor/16x16/apps/
install -m 644 cups.png $RPM_BUILD_ROOT%{_iconsdir}/locolor/16x16/apps/
%endif

# install script to call the web interface from the menu
install -d $RPM_BUILD_ROOT%{_libdir}/cups/scripts/
cat <<EOF > $RPM_BUILD_ROOT%{_libdir}/cups/scripts/cupsWebAdmin
#!/bin/sh
url='http://localhost:631/'
if ! [ -z "\$BROWSER" ] && ( which \$BROWSER ); then
  browser=\`which \$BROWSER\`
elif [ -x /usr/bin/netscape ]; then
  browser=/usr/bin/netscape
elif [ -x /usr/bin/konqueror ]; then
  browser=/usr/bin/konqueror
elif [ -x /usr/bin/lynx ]; then
  browser='xterm -bg black -fg white -e lynx'
elif [ -x /usr/bin/links ]; then
  browser='xterm -bg black -fg white -e links'
else
  xmessage "No web browser found, install one or set the BROWSER environment variable!"
  exit 1
fi
\$browser \$url
EOF
chmod a+rx $RPM_BUILD_ROOT%{_libdir}/cups/scripts/cupsWebAdmin

%if %{build_opensls}
mkdir -p %{buildroot}/var/service/cups/log
mkdir -p %{buildroot}/var/log/supervise/cups
install -m 0755 %{SOURCE20} %{buildroot}/var/service/cups/run
install -m 0755 %{SOURCE21} %{buildroot}/var/service/cups/log/run
%else
# entry for xinetd (disabled by default)
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/cups-lpd
# default: off
# description: The cups-lpd mini daemon enable cups accepting jobs from a \
#       remote LPD client (for example a machine with an older distribution \
#       than Linux Mandrake 7.2 or with a commercial Unix).
service printer
{
	socket_type	= stream
	protocol	= tcp
	wait		= no
	user		= lp
	server		= %{_libdir}/cups/daemon/cups-lpd
	server_args	= -o document-format=application/octet-stream
	disable		= yes
}                                                                               
EOF

# install menu entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}

cat <<EOF > $RPM_BUILD_ROOT%{_menudir}/cups
?package(cups): needs=X11 \
section=Configuration/Printing \
title="CUPS WWW admin tool" \
longtitle="Web-based administration tool for CUPS, works with every browser. Set the $BROWSER environment variable to choose your preferred browser." \
command="%{_libdir}/cups/scripts/cupsWebAdmin 1>/dev/null 2>/dev/null" \
icon="%{_iconsdir}/locolor/16x16/apps/cups.png"
EOF
%endif

%if %{build_opensls}
rm -rf $RPM_BUILD_ROOT%{_initrddir}
%else
# Install startup script
install -m 755 cups.startup $RPM_BUILD_ROOT%{_initrddir}/cups
%endif

# Install script for automatic CUPS configuration
bzcat %{SOURCE7} > $RPM_BUILD_ROOT%{_sbindir}/correctcupsconfig
chmod a+rx $RPM_BUILD_ROOT%{_sbindir}/correctcupsconfig

# Install PPDs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cups/model
install -m 755 ppd/*.ppd $RPM_BUILD_ROOT%{_datadir}/cups/model

# Uncompress Perl script for cleaning up manufacturer entries in PPD files
bzcat %{SOURCE6} > ./cleanppd.pl
chmod a+rx ./cleanppd.pl
# Do the clean-up
find $RPM_BUILD_ROOT%{_datadir}/cups/model -name "*.ppd" -exec ./cleanppd.pl '{}' \;

# Needed by CUPS driver development kit of GIMP-Print
#ln -s libcupsimage.so.2 $RPM_BUILD_ROOT%{_libdir}/libcupsimage.so

# prepare the commands conflicting with LPD for the update-alternatives
# treatment
( cd $RPM_BUILD_ROOT%{_bindir}
  mv lpr lpr-cups
  mv lpq lpq-cups
  mv lprm lprm-cups
  mv lp lp-cups
  mv cancel cancel-cups
  mv lpstat lpstat-cups
)
( cd $RPM_BUILD_ROOT%{_sbindir}
  mv lpc lpc-cups
)
( cd $RPM_BUILD_ROOT%{_mandir}/man1
  rm -f cancel.1
  ln -s lp-cups.1 cancel.1
  mv lpr.1 lpr-cups.1
  mv lpq.1 lpq-cups.1
  mv lprm.1 lprm-cups.1
  mv lp.1 lp-cups.1
  mv cancel.1 cancel-cups.1
  mv lpstat.1 lpstat-cups.1
)
( cd $RPM_BUILD_ROOT%{_mandir}/man8
  mv lpc.8 lpc-cups.8
)

# Remove links to the startup script, we make our own ones with chkconfig
rm -rf $RPM_BUILD_ROOT/etc/rc.d/rc?.d/[SK]*
# Remove superflouus man page stuff
rm -rf $RPM_BUILD_ROOT%{_mandir}/cat
rm -rf $RPM_BUILD_ROOT%{_mandir}/cat?
rm -rf $RPM_BUILD_ROOT%{_mandir}/*/cat
rm -rf $RPM_BUILD_ROOT%{_mandir}/*/cat?

# Install missing headers (Thanks to Oden Eriksson)
install -m644 cups/debug.h  $RPM_BUILD_ROOT%{_includedir}/cups/
install -m644 cups/string.h $RPM_BUILD_ROOT%{_includedir}/cups/
install -m644 config.h $RPM_BUILD_ROOT%{_includedir}/cups/

# Suppress automatic replacement of "echo" by "gprintf" in the CUPS
# startup script by RPM. This automatic replacement is broken.
#export DONT_GPRINTIFY=1


##### PRE/POST INSTALL SCRIPTS #####

%post
/sbin/ldconfig
# Let CUPS daemon be automatically started at boot time
%_post_service cups

%if !%{build_opensls}
##menu
%{update_menus}
%endif

%post common
# Set permissions/ownerships for lppasswd
chown lp.root %{_bindir}/lppasswd
chmod 4755 %{_bindir}/lppasswd
# Set up update-alternatives entries
%{_sbindir}/update-alternatives --install %{_bindir}/lpr lpr %{_bindir}/lpr-cups 10 --slave %{_mandir}/man1/lpr.1.bz2 lpr.1.bz2 %{_mandir}/man1/lpr-cups.1.bz2
%{_sbindir}/update-alternatives --install %{_bindir}/lpq lpq %{_bindir}/lpq-cups 10 --slave %{_mandir}/man1/lpq.1.bz2 lpq.1.bz2 %{_mandir}/man1/lpq-cups.1.bz2
%{_sbindir}/update-alternatives --install %{_bindir}/lprm lprm %{_bindir}/lprm-cups 10 --slave %{_mandir}/man1/lprm.1.bz2 lprm.1.bz2 %{_mandir}/man1/lprm-cups.1.bz2
%{_sbindir}/update-alternatives --install %{_bindir}/lp lp %{_bindir}/lp-cups 10 --slave %{_mandir}/man1/lp.1.bz2 lp.1.bz2 %{_mandir}/man1/lp-cups.1.bz2
%{_sbindir}/update-alternatives --install %{_bindir}/cancel cancel %{_bindir}/cancel-cups 10 --slave %{_mandir}/man1/cancel.1.bz2 cancel.1.bz2 %{_mandir}/man1/cancel-cups.1.bz2
%{_sbindir}/update-alternatives --install %{_bindir}/lpstat lpstat %{_bindir}/lpstat-cups 10 --slave %{_mandir}/man1/lpstat.1.bz2 lpstat.1.bz2 %{_mandir}/man1/lpstat-cups.1.bz2
%{_sbindir}/update-alternatives --install %{_sbindir}/lpc lpc %{_sbindir}/lpc-cups 10 --slave %{_mandir}/man8/lpc.8.bz2 lpc.1.bz2 %{_mandir}/man8/lpc-cups.8.bz2

%post -n %{libname}
/sbin/ldconfig

%preun
# Let CUPS daemon not be automatically started at boot time any more
%_preun_service cups

%preun common
if [ "$1" = 0 ]; then
  # Remove update-alternatives entries
  %{_sbindir}/update-alternatives --remove lpr %{_bindir}/lpr-cups
  %{_sbindir}/update-alternatives --remove lpq %{_bindir}/lpq-cups
  %{_sbindir}/update-alternatives --remove lprm %{_bindir}/lprm-cups
  %{_sbindir}/update-alternatives --remove lp %{_bindir}/lp-cups
  %{_sbindir}/update-alternatives --remove cancel %{_bindir}/cancel-cups
  %{_sbindir}/update-alternatives --remove lpstat %{_bindir}/lpstat-cups
  %{_sbindir}/update-alternatives --remove lpc %{_sbindir}/lpc-cups
fi

%preun -n %{libname}
/sbin/ldconfig

%if !%{build_opensls}
%postun
## menu
%{update_menus}
%endif

%postun -n %{libname}
/sbin/ldconfig

##### CLEAN UP #####

%clean
rm -rf $RPM_BUILD_ROOT


##### FILE LISTS FOR ALL BINARY PACKAGES #####

#####cups
%files
%defattr(-,root,root)
%doc %{_defaultdocdir}/%{name}
%config(noreplace) %attr(711,lp,root) %{_sysconfdir}/cups/certs
%config(noreplace) %{_sysconfdir}/cups/classes.conf
%config(noreplace) %{_sysconfdir}/cups/cupsd.conf
%config(noreplace) %{_sysconfdir}/cups/interfaces
%config(noreplace) %{_sysconfdir}/cups/mime.convs
%config(noreplace) %{_sysconfdir}/cups/mime.types
%config(noreplace) %{_sysconfdir}/cups/ppd
%config(noreplace) %{_sysconfdir}/cups/printers.conf
%config(noreplace) %{_sysconfdir}/cups/ssl
%if !%{build_opensls}
%config(noreplace) %{_initrddir}/cups
%endif
%config(noreplace) %{_sysconfdir}/pam.d/cups
%if %{build_opensls}
%dir /var/service/cups
%dir /var/service/cups/log
/var/service/cups/run
/var/service/cups/log/run
%dir %attr(0750,nobody,nogroup) /var/log/supervise/cups
%else
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/xinetd.d/cups-lpd
%endif
%dir %{_libdir}/cups
%{_libdir}/cups/cgi-bin
%{_libdir}/cups/daemon
%{_libdir}/cups/filter
%{_libdir}/cups/scripts
%dir %{_libdir}/cups/backend
%{_libdir}/cups/backend/http
%{_libdir}/cups/backend/ipp
%{_libdir}/cups/backend/lpd
%{_libdir}/cups/backend/nprint
%{_libdir}/cups/backend/pap
%{_libdir}/cups/backend/parallel
#{_libdir}/cups/backend/ptal
%{_libdir}/cups/backend/scsi
%{_libdir}/cups/backend/socket
%{_libdir}/cups/backend/usb
%{_libdir}/cups/backend/pdf
%{_datadir}/cups
%{_var}/log/cups
# This library is used by the CUPS filters and they make only sense on a
# machine running the CUPS daemon. Therefore it is not in a seperate 
# package.
#{_libdir}/libcupsimage.so.*
# Set ownerships of spool directory which is normally done by 'make install'
# Because RPM does 'make install' as normal user, this has to be done here
%dir %attr(0700,lp,root) %{_var}/spool/cups
%dir %attr(01700,lp,root) %{_var}/spool/cups/tmp
%if !%{build_opensls}
# menu entry
%{_iconsdir}/locolor/16x16/apps/*
%{_menudir}/*
%endif

#####cups-common
%files common
%defattr(-,root,root)
%dir %config(noreplace) %{_sysconfdir}/cups
%config(noreplace) %{_sysconfdir}/cups/client.conf
%{_sbindir}/*
%{_bindir}/*cups
%{_bindir}/lphelp
%{_bindir}/lpoptions
%{_bindir}/lppasswd
%{_bindir}/*able
%{_bindir}/photo_print
%{_bindir}/poll_ppd_base
%{_bindir}/cupstestppd
%{_datadir}/locale/*/*
%{_mandir}/*/*
#{_mandir}/*/*/*

#####%{libname}
%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcups.so.*
%{_libdir}/libcupsimage.so.*

#####%{libname}-devel
%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/cups/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_bindir}/cups-config

%files serial
%defattr(-,root,root)
%{_libdir}/cups/backend/serial


##### CHANGELOG #####

%changelog
* Sat Jan 10 2004 Vincent Danen <vdanen@opensls.org> 1.1.19-13sls
- don't install initscript

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 1.1.19-12sls
- don't install menu or xinetd stuff
- supervise files

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 1.1.19-11sls
- OpenSLS build
- tidy spec (but still needs a lot more cleaning)
- remove support for older mdk versions

* Wed Sep 17 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-10mdk
- Fixed bug 5615 by means of the following two changes:
  o Make the CUPS daemon not sending broadcast packages with the host name
    "localhost". In this case the IP address of the appropriate interface
    is used (patch 22).
  o Do not insert "ServerName" directives in /etc/cups/cupsd.conf any more
    during the startup of CUPS (with the /usr/sbin/correctcupsconfig
    script).

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.19-9mdk
- Remove wrongly inherited deps on all subpackages

* Fri Aug  8 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-8mdk
- Added a version number to the "Provides: libcups1" to avoid a conflict
  with libpng3.

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.19-7mdk
- mklibname, fix major in package name

* Sun Jul 27 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-6mdk
- Install missing headers (Thanks to Oden Eriksson)

* Thu Jul 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.19-5mdk
- Rebuild

* Thu Jun 26 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-4mdk
- Re-introduced SLP support.

* Thu Jun 05 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.19-3mdk
- Use --disable-slp

* Thu Jun 05 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.19-2mdk
- Don't link with libslp

* Tue May 27 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-1mdk
- Updated to finally released CUPS 1.1.19 (SECURITY FIX: Denial of service 
  attack vulnerability, see http://www.cups.org/str.php?L75 and other bug 
  fixes and updates).
- Moved libcups.so to "-devel" package to avoide dependency of "libcups1"
  on other "-devel" packages.
- Rebuild to get a "-debug" package.

* Tue May 13 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.9mdk
- Updated to released CUPS 1.1.19rc5.

* Sat May 10 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.8mdk
- Updated to released CUPS 1.1.19rc4.

* Mon Apr 28 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.7mdk
- Updated to released CUPS 1.1.19rc3.

* Sun Apr 20 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.6mdk
- Updated to released CUPS 1.1.19rc2.
 
* Tue Mar 11 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.5mdk
- Fixed japanese text printing with "cjktexttops": The margins were too
  narrow and too long lines were cut off and not wrapped. No no information 
  of the printed text gets lost any more.

* Mon Mar 10 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.4mdk
- Add "cjktexttops" filter (derived from Red Hat's filter) for
  printing japanese plain text files with "mpage".

* Thu Mar  6 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.3mdk
- Let CUPS daemon accept raw files (e. g. already filtered by Windows
  driver).
- Added "pdf" backend.

* Wed Feb 26 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.2mdk
- Updated to the CVS of Feb. 26, 2003 (Bug fixes).

* Sat Feb 15 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.19-0.1mdk
- Updated to the CVS of Feb. 15, 2003 (Several bug fixes).

* Fri Jan 31 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.18-5mdk
- Removed most operations from "cleanppd.pl". They are taken care of
  by this spec file or by "printerdrake".

* Fri Jan 31 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.18-4mdk
- Removed all data manipulations from "poll_ppd_base", they will be done
  by "printerdrake" now.

* Thu Jan 23 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.18-3mdk
- Removed determination of the printer's serial number in 
  /proc/bus/usb/devices, it was broken.
- Fixed error reporting when gethostbyname fails.

* Wed Jan 15 2003 Till Kamppeter <till@mandrakesoft.com> 1.1.18-2mdk
- Rebuilt for new OpenSSL version.

* Thu Dec 19 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.18-1mdk
- Updated to released CUPS 1.1.18 (Security fixes based on a report from 
  iDEFENSE, new cupstestppd utility for validating PPD files).

* Fri Nov 23 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.17-1mdk
- Updated to released CUPS 1.1.17.
- Removed "cat" subdirectories from man page directory.

* Fri Nov 22 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.17-0.2mdk
- Updated to the CVS of Nov. 22, 2002 (CUPS daemon didn't pass command
  line options of "lpr" to the filters).

* Thu Nov 21 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.17-0.1mdk
- Updated to the CVS of Nov. 21, 2002 (Fixes printer configuration via web 
  interface, has Mac OS character sets to print jobs from Mac OS X clients 
  correctly, fixed possible crash of CUPS daemon when it gets a job from
  CUPS' Windows client PostScript driver).
- Moved "/usr/bin/cups-config" from the "cups-common" to the
  "libcups1-devel" package.

* Wed Oct 30 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.16-3mdk
- Updated to the CVS of Oct. 30, 2002 (Web server fixes).

* Wed Oct 30 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.16-2mdk
- Updated to the CVS of Oct. 28, 2002 (Fixes the problem of queues
  generated with "lpadmin" ignoring the PPD file and printing raw
  PostScript code until the CUPS daemon is restarted.
- Replaced Patch 15 (libdir for 64-bit architecture) by code manipulation
  directly in the spec file.

* Wed Oct 17 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.16-1mdk
- Updated to the CVS of Oct. 17, 2002 (Fixes web interface problem,
  landscape bug, and several others. ommited CUPS 1.1.16 final due
  to persisting web interface bug).
- Let "service cups reload" only send a SIGHUP to the CUPS daemon instead
  of killing and restarting it.

* Tue Sep 10 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.16-0.4mdk
- Downdated to the CVS of Aug. 16, 2002 (In the CVS from Aug. 31 it is not
  possible to add print queues with the web interface due to changes in
  the PAM infrastructure of CUPS).

* Sat Aug 31 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.16-0.3mdk
- Fixed "/usr/sbin/correctcupsconfig" script so that it generates a
  correct "/etc/cups/cupsd.conf" when this file is missing.

* Fri Aug 16 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.16-0.2mdk
- Updated to the CVS of Aug. 16, 2002 (Option conflicts fix in web
  interface).
- Fixed startup script so that the "gprintf"ication works again. 

* Wed Aug 14 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.16-0.1mdk
- Updated to the CVS of Aug. 14, 2002 (release candidate for CUPS 1.1.16).
- Changed cups-lpd configuration so that the CUPS server filters the
  incoming LPD jobs, so the LPD client does not need a driver.

* Fri Aug  9 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.15-9mdk
- Fix bug of some applications (as a2ps) do not print correctly in Landscape
  orientation.

* Sun Aug 04 2002 Stefan van der Eijk <stefan@eijk.nu> 1.1.15-8mdk
- BuildRequires

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.15-7mdk
- Automated rebuild with gcc3.2

* Mon Jul 22 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.15-6mdk
- Let the starter process of cupsd only exit when cupsd is ready to listen
  for requests.

* Wed Jul 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.15-5mdk
- Menu dir is %%_menudir
- rpmlint fixes: strange-permission, configure-without-libdir-spec,
  hardcoded-library-path

* Fri Jun 28 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.15-4mdk
- If /usr/sbin/correctcupsconfig inserts the "Printcap" line in
  /etc/cups/cupsd.conf when one installs LPRng/LPD, it also removes
  the old CUPS-generated /etc/printcap. This old /etc/printcap causes
  ugly warnings in LPRng.

* Wed Jun 19 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.15-3mdk
- Apply the patch for /etc/cups/cupsd.conf.

* Wed Jun 19 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.15-2mdk
- Replaced automatic CUPS configuration by usage of the new CUPS
  placeholder "@LOCAL" for all local, non-PPP networks.
- Instead of the autoconfig script "setcupsconfig" now a script only
  doing slight corrections in some case "correctcupsconfig" is called
  at every CUPS startup. Now no change is done on /etc/cups/cupsd.conf
  when there is no warning.

* Tue Jun 18 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.15-1mdk
- Updated to version 1.1.15.
- Removed "ptal" backend, this is now provided by HPOJ.
- Added "pap" backend, to access printers via AppleTalk.
- Added "photo_print", a script to print series of photos, several photos
  per sheet.

* Thu Apr 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.14-4mdk
- remove system wide directories ownership

* Tue Mar 26 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.14-3mdk
- Auto-config program /usr/sbin/setcupsconfig supports having two or
  more network cards with the same IP address.

* Sat Feb 16 2002 Stefan van der Eijk <stefan@eijk.nu> 1.1.14-2mdk
- BuildRequires

* Wed Feb 13 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.14-1mdk
- Updated to version 1.1.14 (Release because of the IPP security bugfix).

* Wed Feb 13 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.13-5mdk
- Security fix for the IPP backend was not complete. Applied new,
  complete patch.
- Made a symbolic link to the test page in "printer-testpages", so only
  one test page has to be maintained and kept on the distro CDs.

* Sun Feb 10 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.13-4mdk
- Security fix: Fixed potential buffer overflow bug when the IPP backend
  reads the names of attributes.
- Added "lpddaemon" to the "Provides" of CUPS, to satisfy FHS/LSB tests.
- Moved "Obsoletes: cups-devel" and "Provides: cups-devel" from "cups"
  to "libcups1-devel".

* Mon Feb  4 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.13-3mdk
- Added backend filter for nprint (Novell client) from Mark Horn 
  (mark@hornclan.com),
- Updated HPOJ/ptal backend filter to the version of 18/01/2002.
- Added check for "ptal:/..." URIs when the startup script checks
  the /etc/cups/printers.conf whether HPOJ needs to be started.

* Sat Feb  2 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.13-2mdk
- Added backend filter for HPOJ from Mark Horn (mark@hornclan.com),

* Fri Feb  1 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.13-1mdk
- Updated to version 1.1.13.

* Sat Jan 19 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.12-3mdk
- Let "setcupsconfig" use "Listen" directives instead of "Port" directives
  in /etc/cups/cupsd.conf to restrict CUPS listening only to local networks.
  This was suggested by David Walser (luigiwalser at yahoo dot com).

* Sat Jan 12 2002 Till Kamppeter <till@mandrakesoft.com> 1.1.12-2mdk
- Used "route -n" instead of "route" in startup script, the simple
  "route" does often not show the loopback device correctly.

* Mon Dec 17 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.12-1mdk
- Updated to version 1.1.12.

* Mon Dec 17 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-14mdk
- Suppressed automatic replacement of "echo" by "gprintf" in the startup
  script, the automatic replacement is broken.

* Tue Dec  4 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-13mdk
- Modified startup script to do not do any changes on /etc/hosts any more.

* Wed Oct 12 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-12mdk
- Fixed auto-correction of /etc/hosts. Nicknames for localhost are conserved
  now.

* Wed Oct 10 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-11mdk
- Corrected text on the test page.

* Wed Oct 10 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-10mdk
- Inserted new Mandrake logo into the test page.
- Rebuilt for libpng3.

* Wed Sep 19 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-9mdk
- Separated out the serial port backend of CUPS into an extra package, it
  was the reason for the CUPS daemon needing several seconds to start.

* Wed Sep 19 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-8mdk
- Fixed setcupsconfig so that CUPS also starts on systems without
  /etc/sysconfig/network-scripts/draknet_conf.

* Sat Sep 15 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-7mdk
- fixed link from lp.1 to cancel.1 to work in the update-alternatives
  structure so that "man cancel" shows the correct man page.

* Sat Sep 15 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-6mdk
- Automatic CUPS configuration defines the directory for temporary
  files now, so environment variable settings cannot break things
  (Bug 4568)

* Fri Sep 14 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-5mdk
- Made automatic CUPS configuration also working on non-english
  systems.
- CUPS requires net-tools.

* Fri Sep 14 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-4mdk
- Check /etc/hosts on startup so assure that it has a correct
  "localhost" line.
- Do not change hostname to "localhost" if there is no local network.

* Sat Sep  1 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-3mdk
- Turn off the cups-lpd mini daemon when LPD/LPRng is running (in the
  startup script).

* Sat Sep  1 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-2mdk
- Expanded auto-configuration script for more different network
  configurations, especially ADSL and cable modem through an ethernet
  card.
- Added checks for system environment to the CUPS startup script,
  missing kernel modules and a missing loopback device are started
  automatically now.

* Tue Aug 21 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.10-1mdk
- Updated to CUPS 1.1.10 (several bugfixes) 

* Wed Aug 15 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.9-6mdk
- Raised limit of values per attribute of an IPP request from 100 to 500
  (Broke Epson Stylus Photo 1290 with the GIMP-Print GhostScript driver)

* Sat Jul 28 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.9-5mdk
- lphelp takes PPD files from standard input now

* Mon Jul 23 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.1.9-4mdk
- Don't BuildRequires: egcs when it's not needed (as for 1.1.6-12mdk)

* Sat Jul 21 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.9-3mdk
- Updated to CUPS 1.1.9-1 (several bugfixes)

* Wed Jul 18 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.9-2mdk
- Extended the update-alternatives stuff so that CUPS can also co-exist
  with LPRng

* Tue Jul 10 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.9-1mdk
- Updated to CUPS 1.1.9 (several bugfixes)

* Fri Jun  8 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.8-1mdk
- Updated to CUPS 1.1.8 (several bugfixes)

* Fri May  4 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.7-1mdk
- SECURITY FIXES: Updated to CUPS 1.1.7

* Thu May  3 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-22mdk
- Downdated pstops filter to the version of CUPS 1.1.6-3 due to problems 
  with multiple page documents

* Thu Apr 12 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-21mdk
- Cleaned up output of "poll_ppd_base" to give a nicer and more user-
  friendly printer list in "printerdrake".

* Fri Apr  6 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-20mdk
- Additional fixes in "poll_ppd_base": Manufacturer names are made
  all-uppercase and "-" in the beginning of a model name is removed.

* Fri Apr  6 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-19mdk
- Removed the manufacturer's names from the model field in the output
  of "poll_ppd_base", they were sometimes written all-uppercase and 
  sometimes not and this messed up the printer listing in "printerdrake".

* Sat Mar 31 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-18mdk
- Use new macros for server packages only when building for Linux Mandrake 
  8.x to not blow up a build for 7.x.

* Sat Mar 31 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-17mdk
- Updated CUPS from CVS (Lots of bugfixes).
- Cleaned up PostScript code of the test page.

* Thu Mar 29 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-16mdk
- Used new macros for server packages ("-fno-omit-frame-pointer" and
  upgrade fixes).
- Inserted missing "#include" directives in the code of "pstoraster". They
  are needed by gcc 2.96.

* Sat Mar 17 2001 David BAUDENS <baudens@mandrakesoft.com> 1.1.6-15mdk
- Don't BuildRequires: egcs on PPC

* Thu Mar 15 2001 Francis Galiegue <fg@mandrakesoft.com> 1.1.6-14mdk
- Add -fPIC to CFLAGS for ia64

* Sun Mar 11 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-13mdk
- In case of building a package for Mandrake 7.2, the "cups" package
  provides "cups-common" and "libcups1" now, the "cups-devel" package 
  provides "libcups1-devel".

* Thu Mar  8 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-12mdk
- Fixed a bug in swapping out parts of big images (lead to images sometimes
  not printed or printed totally in black). 

* Mon Mar  5 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-11mdk
- Modified "lphelp" so that it is able to read out the numerical options
  of the new XML-Foomatic which will appear in the near future

* Thu Feb 22 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-10mdk
- Fixed bug of cgi-bin directory going into /etc/cups instead of into
  /usr/lib/cups

* Wed Feb 21 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-9mdk
- SECURITY FIX: Source release 1.1.6-3 (Many security fixes done by SuSE).

* Fri Feb 16 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-8mdk
- Removed "cups-common" package for Mandrake-7.2 builds to make package
  structure exactly as in Mandrake 7.2.

* Thu Feb 15 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-7mdk
- Fixed bug in creation of temporary files, now test page printing, printer 
  configuration and printer creation with KUPS should work again.

* Wed Feb 14 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-6mdk
- Fixed bug which prevented CUPS from connecting to Windows 2000 servers.

* Thu Feb  8 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-5mdk
- SECURITY FIX: Source release 1.1.6-2 used (replacement of lppasswd by new,
  more secure version, many other security fixes, most contributed by SuSE).

* Tue Feb  7 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-4mdk
- SECURITY FIX: SUID bit from "lppasswd" removed, program has several
  security problems.
- Patch on /etc/cups/mime.types for better recognizing of files with
  PJL commands inside.

* Tue Feb  6 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-3mdk
- SECURITY FIX: Changed automatic configuration script so that CUPS
  only accepts broadcasted printer information which comes from the local
  network. Broadcast signals out of the internet are ignored (security
  recommendation of Michael Sweet, author of CUPS).

* Sat Feb  3 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.1.6-3mdk
- backported for 7.2, with conditional macro for building (use 
  %define buildfor72 0 for cooker).
- more macros.
- added xinetd entry cups-lpd.

* Thu Feb  1 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.1.6-2.1mdk
- security update for 7.2 (buffer overflows)

* Tue Jan 30 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-2mdk
- Replaced the job title "(stdin)" by "STDIM" when one prints out of 
  standard input with "lp" or "lpr". This caused problems when printing
  to a printer on a Windows server via Samba.

* Fri Jan 26 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.6-1mdk
- Updated to CUPS 1.1.6.

* Mon Jan  8 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.5-3mdk
- Fixed buffer overflow problem of CUPS' WWW server (QA Bug 687).

* Thu Jan  4 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.5-2mdk

- Bugfix release of CUPS 1.1.5.
- Enhancements in the documentation for setting up encrypted connections.
- Reactivate usage of implicit classes by default.
- Fixed segfault of "lppasswd -a name".

* Wed Jan  3 2001 Till Kamppeter <till@mandrakesoft.com> 1.1.5-1mdk

- Updated to CUPS 1.1.5 (encryption support enabled).
- Added README files of the source tarball to the doc directory.

* Tue Dec 19 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-9mdk
- Rearranged package to seperate libraries, client, server, and so on.
- Fixed several bugs in CUPS-LPD mini-daemon.
- Fixed authorization bug of lpmove.

* Mon Nov 27 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-8mdk
- Fixed RPM problem of /etc/cups/cupsd.conf.rpmnew sometimes not created.

* Thu Nov 23 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-7mdk
- Fixed bug of jobs sent to implicit classes not printing.

* Sat Nov 18 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-6mdk
- Fixed bug in the autodetection of the printer devices.

* Wed Nov 15 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-5mdk
- Security fix: Automatic configuration of broadcasting and printer access 
  restricted to the local network(s) (eth?), printers were accessible from
  all over the internet before, and broadcasting to all networks
  (255.255.255.255) kept dial-on-demand connections permanently up.

* Tue Nov 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.1.4-4mdk
- Fix gcc2.96 compilation.

* Sat Oct 21 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-3mdk
- Security fix: lpstat and web interface displayed the SMB password before

* Tue Oct 17 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-2mdk
- Set default Filterlimit to 999999 in /etc/cups/cupsd.conf, the default
  value zero limited to one process instead of allowing unlimited processes.
- Fixed a bug in scaling of HPGL files.

* Sat Oct 14 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.4-1mdk
- New release with all previous bugfixes included and important fixes for
  the GIMP-Print drivers.

* Mon Oct  2 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-13mdk
- Applied patch by Michael Sweet for the test file bug in the IPP backend.

* Sun Oct  1 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-12mdk
- Fixed a bug of the IPP backend which prevented text with accented characters
  being transferred correctly to the printing server.

* Sun Oct  1 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-11mdk
- Cleaned up manufacturer entry in the CUPS PPD files
- Fixed a bug in handling lines with leading spaces in ~/.lpoptions

* Thu Sep 28 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-10mdk
- Menu call for the web interface not fixed to Netscape any more.

* Thu Sep 28 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-9mdk
- New bugfix patch of Michael Sweet for admin.cgi

* Wed Sep 27 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-8mdk
- Fixed bug in admin.cgi by a patch of Michael Sweet, no downdate to 1.1.2
  any more
- Fixed bug with duplex printing in HP LaserJet driver

* Tue Sep 26 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-7mdk
- Fixed bug in IPP backend which prevented options from
  being transferred correctly to a remote printer

* Tue Sep 26 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-6mdk
- Applied new PAM configuration

* Mon Sep 25 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-5mdk
- Program "lphelp" expanded to show also numerical options of CUPS-O-MATIC
  PPD files.

* Sat Sep 23 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-4mdk
- Mandrakized the test page
- Login/password request for command line tools

* Fri Sep 22 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-3mdk
- Revised support of accounts without password. Now XPP, KUPS and QTCUPS
  do not ask for the login/password again and again when one clicks
  "Cancel" in the login dialog.

* Wed Sep 20 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-2mdk
- Fixed bug of adding a printer with the web interface being impossible
- Make CUPS WWW interface and KUPS usable when root has no 
  password

* Tue Sep 19 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.3-1mdk
- Corrected "preun" script, so that update-alternatives links do not
  get lost on update of the package.
- Updated to CUPS 1.1.3 which includes all the previous bug fix
  patches and some additional bugfixes.

* Sat Sep 16 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-22mdk
- changed default configuration to generate an /etc/printcap
  file. So non-natively CUPS supporting programs (as KDE)
  find the printers.

* Thu Sep 14 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.1.2-21mdk
- corrected incoherent-subsys, till sucks
- added reload

* Wed Sep 13 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-20mdk
- Replaced startup script completely to fit to the Mandrake
  standard
- Applied another development snapshot patch of Michael Sweet to fix
  bugs in pstoimage and pstoraster, and the information propafation
  between the CUPS daemons on different machines.

* Sat Sep  9 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-19mdk
- Applied another development snapshot patch of Michael Sweet to fix
  several bugs.

* Fri Sep  8 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-18mdk
- {_datadir}/locale was forgotten in files section, added

* Fri Sep  8 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-17mdk
- Added /usr/sbin/update-alternatives to "Requires:" line
  to surround a bug of version number comparing in RPM

* Thu Sep  7 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-16mdk
- Turned off feature of "Implicit classes", it is broken.
- Introduced "Requires:" line to make sure that "update-
  alternatives" is available.
- Added patch of Michael Sweet to support instances in lpq
  and lprm.

* Thu Sep  7 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-15mdk
- Applied development snapshot patch of Michael Sweet to fix
  several bugs.
- Added automatic daemon restart on update.

* Wed Sep  5 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-14mdk
- Fixed segfaults in poll_ppd_base
- Better description in cups.sh (help text for startup 
  services config programs)

* Fri Sep  1 2000 Till Kamppeter <till@mandrakesoft.com> 1.1.2-13mdk
- Fixed bugs in the "files" list of specfile (definition of doc dir)

* Tue Aug 29 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-12mdk
- Added patch adjusting the USB printer autodetection to the current state

* Fri Aug 25 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-11mdk
- Menu entry for CUPS WWW Admin tool added
- Removed compatibility link /etc/init.d/cups to /etc/rc.d/init.d/cups, init
  script simply in %{_initrddir} now.

* Fri Aug 25 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-10mdk
- Fixed compiler options for the additional tools

* Thu Aug 24 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-9mdk
- Made the cups package ready for co-existing with the old lpr printing
  system.

* Mon Aug 21 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-8mdk
- Moved "/usr/lib/libcups*.so" links from devel package to main package
  because the function overloading in XPP and QTCUPS would not work without
  these links.

* Thu Aug 17 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-7mdk
- Added program "lphelp" which lists the printer-specific options defined
  in the PPD file, so that one can make use of it in "lp", "lpr", and
  "lpoptions" commands at the command line.
- Got a bugfix from Michael Sweet to fix an htmltops problem, applied it
- Applied bugfix for HPGL recognition in /etc/cups/mime.types

* Thu Aug 17 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-6mdk
- Added program "poll_ppd_base" to get a list of all PPD files installed with
  manufacturer and model names of the printers (useful for installation/
  configuration scripts)

* Mon Aug 14 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-5mdk
- Added link libcupsimage.so --> libcupsimage.so.2 so thet drivers based
  on the CUPS driver development kit of GIMP Print compile
- Moved links "*.so" --> "*.so.2" to the development package (rpmlint
  recommends this)

* Wed Aug  9 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-4mdk
- Replaced "chown" in "%post" by "%attr" in file list
- Now GhostScript 5.50 is not more required by this package but by cups-drivers
- Compatibility link /etc/rc.d/init.d/cups, if /etc/rc.d/init.d/ exists

* Tue Aug  8 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-3mdk
- Let the PPDs delivered with CUPS be installed, too

* Tue Aug  8 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-2mdk
- Moved init script to from /etc/rc.d/init.d/ to /etc/init.d
- Now GhostScript 5.50 is required
- Patched chkconfig entry in /etc/init.d/cups to 2345 60 60 (as lpd)

* Tue Aug  8 2000 Till Kamppeter <tkamppeter@mandrakesoft.com> 1.1.2-1mdk
- Excluded static CUPS library to allow overloading of CUPS functions
- Patched CUPS daemon config to use Web interface for administration
- pstoraster not removed to have the flexibility to also use CUPS drivers
- Updated to version 1.1.2 with bugfix patch for the Makefile

* Tue Jul  4 2000 François Pons <fpons@mandrakesoft.com> 1.1-0.b5.1mdk
- removed pstoraster from installation as drivers are in cups-drivers.
- initial release.
