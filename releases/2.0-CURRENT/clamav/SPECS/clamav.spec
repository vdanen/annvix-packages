#
# spec file for package clamav
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		clamav
%define version		0.88.4
%define release		%_revrel

%define	major		1
%define libname		%mklibname %{name} %{major}

Summary:	An anti-virus utility for Unix
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://clamav.sourceforge.net/
Source0:	http://www.clamav.net/%{name}-%{version}.tar.gz
Source1:	http://www.clamav.net/%{name}-%{version}.tar.gz.sig
Source4:	clamd.run
Source5:	clamd-log.run
Source6:	freshclam.run
Source7:	freshclam-log.run
Patch0:		clamav-0.87-avx-config.patch
Patch1:		clamav-0.88.1-avx-stderr.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	zlib-devel
BuildRequires:	gmp-devel
BuildRequires:	bzip2-devel

Requires(post):	clamav-db
Requires(preun): clamav-db
Requires(post):	%{libname} = %{version}
Requires(preun): %{libname} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper

%description 
Clam AntiVirus is an anti-virus toolkit for Unix. The main purpose
of this software is the integration with mail seversions (attachment
scanning). The package provides a flexible and scalable
multi-threaded daemon, a commandline scanner, and a tool for
automatic updating via Internet. The programs are based on a
shared library distributed with the Clam AntiVirus package, which
you can use in your own software. 


%package -n clamd
Summary:	The Clam AntiVirus Daemon
Group:		System/Servers
Requires:	%{name} = %{version}
Requires(post):	clamav-db
Requires(preun): clamav-db
Requires(post):	%{libname} = %{version}
Requires(preun): %{libname} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper

%description -n	clamd
The Clam AntiVirus Daemon


%package -n %{name}-db
Summary:	Virus database for %{name}
Group:		Databases
Requires:	%{name} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper


%description -n	%{name}-db
The actual virus database for %{name}


%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:          System/Libraries

%description -n	%{libname}
Shared libraries for %{name}


%package -n %{libname}-devel
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel
Provides:	lib%{name}-devel
Obsoletes:	%{name}-devel
Obsoletes:	lib%{name}-devel

%description -n	%{libname}-devel
This package contains the static %{libname} library and its header
files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}

# clean up
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done
	
%patch0 -p1 -b .avx
%patch1 -p1 -b .stderr


%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force && aclocal-1.7 && autoconf && automake-1.7

#export SENDMAIL="%{_libdir}/sendmail"

%serverbuild

%configure2_5x \
    --disable-%{name} \
    --with-user=%{name} \
    --with-group=%{name} \
    --with-dbdir=%{_localstatedir}/%{name} \
    --enable-id-check \
    --enable-clamuko \
    --enable-bigstack \
    --without-libcurl \
    --with-zlib=%{_prefix} \
    --disable-zlib-vcheck \
    --disable-milter \
    --without-tcpwrappers
#   --enable-debug

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

install -m 0644 etc/clamd.conf %{buildroot}%{_sysconfdir}/clamd.conf
install -m 0644 etc/freshclam.conf %{buildroot}%{_sysconfdir}/freshclam.conf

mkdir -p %{buildroot}%{_srvdir}/{clamd,freshclam}/log
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/clamd/run
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/clamd/log/run
install -m 0740 %{SOURCE6} %{buildroot}%{_srvdir}/freshclam/run
install -m 0740 %{SOURCE7} %{buildroot}%{_srvdir}/freshclam/log/run

# pid file dir
mkdir -p %{buildroot}/var/run/%{name}

# fix TMPDIR
mkdir -p %{buildroot}%{_localstatedir}/%{name}/tmp


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ -d /var/log/supervise/freshclam -a ! -d /var/log/service/freshclam ]; then
    mv /var/log/supervise/freshclam /var/log/service/
fi
%_post_srv freshclam


%preun
%_preun_srv freshclam


%post -n clamd
%_post_srv clamd


%preun -n clamd
%_preun_srv clamd


%pre -n %{name}-db
%_pre_useradd clamav %{_localstatedir}/%{name} /bin/sh 91


%post -n %{name}-db
# try to keep most uptodate database
for i in main daily; do
    if [ -f /var/lib/clamav/$i.cvd.rpmnew ]; then
        if [ /var/lib/clamav/$i.cvd.rpmnew -nt /var/lib/clamav/$i.cvd ]; then
            mv -f /var/lib/clamav/$i.cvd.rpmnew /var/lib/clamav/$i.cvd
        else
            rm -f /var/lib/clamav/$i.cvd.rpmnew
        fi
    fi
done


%postun -n %{name}-db
%_postun_userdel clamav


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/clamd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/freshclam.conf
%{_bindir}/clamscan
%{_bindir}/clamdscan
%{_bindir}/freshclam
%{_bindir}/sigtool
%{_mandir}/man1/sigtool.1*
%{_mandir}/man1/clamdscan.1*
%{_mandir}/man1/clamscan.1*
%{_mandir}/man1/freshclam.1*
%{_mandir}/man5/clamd.conf.5*
%{_mandir}/man5/freshclam.conf.5*
%exclude %{_mandir}/man8/%{name}-milter.8*
%dir %attr(0755,clamav,clamav) /var/run/%{name}
%dir %attr(0755,clamav,clamav) %{_localstatedir}/%{name}
%dir %attr(0750,root,admin) %{_srvdir}/freshclam
%dir %attr(0750,root,admin) %{_srvdir}/freshclam/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/freshclam/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/freshclam/log/run

%files -n clamd
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/clamd.conf
%{_sbindir}/clamd
%{_mandir}/man8/clamd.8*
%dir %attr(0750,root,admin) %{_srvdir}/clamd
%dir %attr(0750,root,admin) %{_srvdir}/clamd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/clamd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/clamd/log/run

%files -n %{name}-db
%defattr(-,root,root)
%dir %attr(0755,clamav,clamav) %{_localstatedir}/%{name}
%attr(0644,clamav,clamav) %config(noreplace) %{_localstatedir}/%{name}/daily.cvd
%attr(0644,clamav,clamav) %config(noreplace) %{_localstatedir}/%{name}/main.cvd
%dir %attr(0755,clamav,clamav) %{_localstatedir}/%{name}/tmp

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/clamav-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/libclamav.pc

%files doc
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog FAQ NEWS README test UPGRADE COPYING
%doc contrib/clamdwatch contrib/clamavmon contrib/clamdmon

      
%changelog
* Tue Aug 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88.4
- 0.88.4 (fixes a heap-based buffer overflow vulnerability)
- clean spec

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88.2
- add -doc subpackage
- rebuild with gcc4
- fixed group

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88.2
- 0.88.2: fixes CVE-2006-1989

* Tue Apr 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88.1
- 0.88.1: fixes CVE-2006-1614, CVE-2006-1615, CVE-2006-1630
- rediff P1

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88
- 0.88 (fixes CVE-2006-0162)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.87.1
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.87.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Mon Nov 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.87.1-1avx
- 0.87.1; security fixes for CVE-2005-3239, CVE-2005-3303, CVE-2005-3500,
  CVE-2005-3501

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.87-2avx
- clamav is static uid/gid 91, not 89 (clashes with dhcpd)
- useradd only in clamav-db, not in clamav or clamd
- execline the runscripts and make both freshclam and clamd run
  as user clamav rather than root
- P1: allow clamav/freshclam to log to stderr (from http://www.gluelogic.com/code/)
- P0: adjust the configs to log to stderr by default
- drop the logrotate files and logfiles

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.87-1avx
- 0.87

* Sat Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-4avx
- don't build against libcurl as apparently that would be in violation
  of the GPL since we build it against OpenSSL; see:
    http://curl.haxx.se/legal/distro-dilemma.html

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-3avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-2avx
- spec tidys

* Fri Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-1avx
- 0.86.2
- use execlineb for run scripts
- move logdir to /var/log/service/{freshclam,clamd}
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.1-3avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.1-2avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.1-1avx
- 0.86.1 (fixes a possible crash in libmspack's Quantum decompressor)
- make the freshclam and clamd logfiles mode 0640 rather than 0644

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.83-3avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.83-2avx
- use logger for logging

* Wed Feb 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.83-1avx
- 0.83
- first Annvix build
- big spec cleanups; get rid of milter support
- remove BuildRequires: bc
- clamav is static uid/gid 89
- supervise scripts
