%define name	freeswan
%define version	2.05
%define release	2sls

%define x509_patch_version 1.5.3

Summary:	A Free IPSEC implemetation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		https://www.freeswan.org/
Source0:	ftp://ftp.xs4all.nl:/pub/crypto/%{name}/%{name}-%{version}.tar.gz
# (fg) 20010314 FIXME - HACK - this is a modified version of the initscript for
# ipsec, but it's far from being fully converted!
Source1:	freeswan.init
Source2:	ftp://ftp.xs4all.nl:/pub/crypto/%{name}/%{SOURCE0}.sig
Source3:	http://www.strongsec.com/freeswan/x509-%{x509_patch_version}-%{name}-%{version}.tar.gz
Source4:	http://www.strongsec.com/freeswan/x509-%{x509_patch_version}-%{name}-%{version}.tar.gz.sig

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gmp-devel
BuildRequires:	openldap-devel

Prefix:		%{_prefix}
Prereq:		/sbin/chkconfig rpm-helper

%description
The basic idea of IPSEC is to provide security functions
(authentication and encryption) at the IP (Internet Protocol)
level. It will be required in IP version 6 (better known as IPng,
the next generation) and is optional for the current IP, version 4.

FreeS/WAN is a freely-distributable implementation of IPSEC protocol.

This package has the x509 patch applied (www.strongsec.com)

%prep
%setup -q

tar xzf %{SOURCE3}
cp x509-%{x509_patch_version}-%name-%version/%name.diff .
cp x509-%{x509_patch_version}-%name-%version/README ./README.x509patch
cp x509-%{x509_patch_version}-%name-%version/CHANGES ./CHANGES.x509patch
install -m 0644 x509-%{x509_patch_version}-%name-%version/ipsec.secrets.template ./ipsec.secrets.template.x509patch
mv README README.main

patch -p1 < %name.diff

# enable LDAP v3 support
perl -pi -e "s,#LDAP_VERSION=3,LDAP_VERSION=3,g" %{_builddir}/%{name}-%{version}/programs/pluto/Makefile
# enable smartcard support
#perl -pi -e "s,#SMARTCARD=1,SMARTCARD=1,g" %{_builddir}/%{name}-%{version}/programs/pluto/Makefile

# change some default settings
find . -type f | xargs perl -pi -e "s,/usr/local/man,%{_mandir},g"
find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"
find . -type f | xargs perl -pi -e "s,/libexec/ipsec,/lib/ipsec,g"
find . -type f | xargs perl -pi -e "s,/etc/ipsec.conf,/etc/freeswan/ipsec.conf,g"
find . -type f | xargs perl -pi -e "s,/etc/ipsec.secrets,/etc/freeswan/ipsec.secrets,g"
find . -type f | xargs perl -pi -e "s,/etc/ipsec.d,/etc/freeswan/ipsec.d,g"


%build
%serverbuild

perl -p -i -e "s|INC_USRLOCAL=/usr/local|INC_USRLOCAL=/usr|" Makefile.inc
perl -p -i -e "s|INC_USRLOCAL=/libexec/ipsec/|INC_USRLOCAL=/lib/ipsec/|" Makefile.inc
%make OPT_FLAGS="$RPM_OPT_FLAGS" CONFDIR=/etc/freeswan/ FINALCONFDIR=/etc/freeswan FINALCONFFILE=/etc/ipsec.conf INC_USRLOCAL=/usr INC_MANDIR=share/man programs 

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ipsec.d/{cacerts,crls,private,certs,acerts}
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/pluto}

make install \
	INC_USRLOCAL=/usr \
	INC_MANDIR=share/man \
	CONFDIR="%buildroot"/etc/freeswan \
	DESTDIR="%buildroot"

# (fg) File is copied over here
cp -f %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/ipsec

mv %buildroot/etc/ipsec.d/policies %buildroot/%_sysconfdir/%name/ipsec.d
mv %buildroot/%_docdir/%name/ipsec.conf-sample %_builddir/%name-%version

find . -name ".cvsignore" | xargs rm -rf
rm -rf %{buildroot}%{_sysconfdir}/rc.d/rc*.d

%post
is=%{_sysconfdir}/freeswan/ipsec.secrets; if [ ! -f $is ]; then ipsec newhostkey --output $is && chmod 400 $is; else ipsec newhostkey --output $is.rpmnew && chmod 400 $is.rpmnew; fi

%_post_service ipsec 

%preun
%_preun_service ipsec

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc README* COPYING CHANGES* CREDITS BUGS ipsec* doc/*
%attr(700,root,root) %dir %{_sysconfdir}/%name
%attr(700,root,root) %dir %{_sysconfdir}/%name/ipsec.d/
%attr(700,root,root) %dir %{_sysconfdir}/%name/ipsec.d/acerts
%attr(700,root,root) %dir %{_sysconfdir}/%name/ipsec.d/certs
%attr(700,root,root) %dir %{_sysconfdir}/%name/ipsec.d/cacerts
%attr(700,root,root) %dir %{_sysconfdir}/%name/ipsec.d/crls
%attr(700,root,root) %dir %{_sysconfdir}/%name/ipsec.d/private
%attr(700,root,root) %dir %{_sysconfdir}/%name/ipsec.d/policies/
%config(noreplace) %{_sysconfdir}/%name/ipsec.d/policies/*
%config(noreplace) %{_sysconfdir}/%name/ipsec.conf
%config(noreplace) %{_initrddir}/ipsec
%dir %{_prefix}/lib/ipsec
%{_prefix}/lib/ipsec/*
%{_sbindir}/*
%{_mandir}/*/*

%changelog
* Sat Mar 27 2004 Vincent Danen <vdanen@opensls.org> 2.05-2sls
- major spec tidying (still need to daemonize the service)

* Wed Mar  3 2004 Thomas Backlund <tmb@iki.fi> 2.05-1sls
- OpenSLS build
- freeswan 2.05
- update x509 patch to 1.5.3

* Thu Dec 04 2003 Florin <florin@mandrakesoft.com> 2.04-2mdk
- /etc/freeswan/ipsec.d is the right directory
- add the certs and acerts directories

* Mon Dec 01 2003 Florin <florin@mandrakesoft.com> 2.04-1mdk
- 2.04
- update the x509 patch
- add the link to my web site to have compatible kernels

* Sun Nov 23 2003 Stefan van der Eijk <stefan@eijk.nu> 2.03-2mdk
- BuildRequires

* Mon Nov 10 2003 Florin <florin@mandrakesoft.com> 2.03-1mdk
- 2.0.3
- x509-1.4.8 patch
- do some spec cleaning

* Fri Sep 26 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.01-2mdk
- stick with /usr/lib/ipsec since anyway that's kernel dependent

* Thu Aug 28 2003 Florin <florin@mandrakesoft.com> 2.0.1-1mdk
- 2.0.1
- x509-1.4.4 patch

* Thu May 22 2003 Florin <florin@mandrakesoft.com> 2.00-2mdk
- - x509-1.3.3 patch

* Wed May 14 2003 Florin <florin@mandrakesoft.com> 2.00-1mdk
- 2.00
- x509-1.3.2 patch 
- the secrets file is not present anymore
- the devel files go to the debug package
- add the policies files
- add the libexec files
- add the sample configuration file

* Thu Jan 09 2003 Florin <florin@mandrakesoft.com> 1.99-3mdk
- recompile against the latest glibc/gcc

* Fri Nov 15 2002 Florin <florin@mandrakesoft.com> 1.99-2mdk
- add some missing files
- add the Makefile patch

* Thu Nov 14 2002 Florin <florin@mandrakesoft.com> 1.99-1mdk
- 1.99
- x509patch-0.9.15 patch
- Requires on rpm-helper

* Tue Aug 27 2002 Florin <florin@mandrakesoft.com> 1.98b-1mdk
- 1.98
- x509patch-0.9.14 patch
* Mon Aug 26 2002 Florin <florin@mandrakesoft.com> 1.97-4mdk
- add the ipsec.d/* directories

* Fri Aug 23 2002 Florin <florin@mandrakesoft.com> 1.97-3mdk
- x509patch-0.9.13 patch

* Thu Aug 08 2002 Florin <florin@mandrakesoft.com> 1.97-2mdk
- better usage in the initscript

* Tue Apr 16 2002 Florin <florin@mandrakesoft.com> 1.97-1mdk
- 1.97
- update the sources path
- add the x509 patch (source3)
- add the doc section
- add the /etc/%name/ipsec.d directory

* Fri Apr 12 2002 Florin <florin@mandrakesoft.com> 1.96-1mdk
- 1.96
- create a new %{_sysconfig}/%name/ipsec.secrets.rpmnew if
- ipsec.secrets exists
- use the --output option in post instead of redirection

* Tue Mar 12 2002 Florin <florin@mandrakesoft.com> 1.95-2mdk
- fix the conf files problem

* Wed Feb 27 2002 Florin <florin@mandrakesoft.com> 1.95-1mdk
- 1.95
- leave the sources in gz format
- add the signature file (source2)
- new initscript

* Wed Aug 29 2001 Sylvain de Tilly <sdetilly@mandrakesoft.com> 1.91-3mdk
- change config file in /usr/lib/ipsec/showhostkey :
	/etc/ipsec.secrets to /etc/freeswan/ipsec.secrets
- change "hostname --fqdn" by "hostname" in /usr/lib/ipsec/showhostkey

* Tue Jul 31 2001 Sylvain de Tilly <sdetilly@mandrakesoft.com> 1.91-2mdk
- Add ipsec mini-howto in html and sgml format.

* Wed Jul 18 2001 Sylvain de Tilly <sdetilly@mandrakesofr.com> 1.91-1mdk
- update 1.9 to 1.9.1

* Sun Apr  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.9-2mdk
- use server macros

* Thu Apr  5 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.9-1mdk
- 1.9.

* Wed Mar 14 2001 Francis Galiegue <fg@mandrakesoft.com> 1.8-2mdk
- Modified init.d script to "feel like" Mandrake - HACK - please improve it
- More macros

* Tue Jan 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> VERSION-1mdk
- 


# end of file
