%define name	php-%{subname}
%define version	%{phpversion}
%define release	1avx

%define phpsource	%{_prefix}/src/php-devel
%{expand:%(cat /usr/src/php-devel/PHP_BUILD||(echo -e "error: failed build dependencies:\n        php-devel >= 430 (4.3.0) is needed by this package." >/dev/stderr;kill -2 $PPID))}

%define subname		pear
%define php_ver_rel	%{phpversion}-%{phprelease}
%define pear_date	20040506

Summary:	The PHP PEAR files
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/Other
URL:		http://www.php.net
Source0:	php-pear-%{pear_date}.tar.bz2
Source1:	fixregistry.php

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	php%{libversion}-devel php-xml perl php-cli
BuildArch:	noarch

Requires:	php-cli
Requires:	php-xml
Requires:	php-xmlrpc
Provides:	php-pear-Log
Provides:	php-pear-Mail
Provides:	php-pear-Mail_Mime
Provides:	php-pear-Net_Socket
Provides:	php-pear-Archive_Tar
Provides:	php-pear-Console_Getopt
Provides:	php-pear-DB
Provides:	php-pear-Net_SMTP
Provides:	php-pear-XML_Parser
Provides:	php-pear-XML_RPC
Provides:	php-pear-phpUnit

%description
PEAR is short for "PHP Extension and Application Repository" and is
pronounced just like the fruit. The purpose of PEAR is to provide:

    * A structured library of open-sourced code for PHP users
    * A system for code distribution and package maintenance
    * A standard style for code written in PHP, specified here
    * The PHP Foundation Classes (PFC), see more below
    * The PHP Extension Code Library (PECL), see more below
    * A web site, mailing lists and download mirrors to support the
      PHP/PEAR community 

%prep
%setup -q -n %{name}


%build
# Make sure that there are no < /dev/tty statements in go-pear
perl -pi -e "s|/dev/tty|php://stdin|;" go-pear
perl -pi -e 's|detect_install_dirs\(\)|detect_install_dirs("%{buildroot}/usr")|;' go-pear
perl -pi -e "s|'XML_Parser',|'XML_Parser',\n    'Log',\n    'Mail_Mime',\n    |;" go-pear

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# Pass default values to go-pear.  This will fetch, build and install PEAR
install -d %{buildroot}{%{peardir},%{_bindir}}
yes ""|php -q go-pear

echo "Get all the info on http://pear.php.net" > README

# Remove CVS files
find %{buildroot}%{peardir} -name ".cvsignore" |\
	xargs rm -f

# Remove buildroot
for f in %{buildroot}/%{peardir}/.registry/*.reg
do
  php %{SOURCE1} $f %{buildroot}
done

# Turn generated conf into a global setting
mkdir -p %{buildroot}%{_sysconfdir}
grep -v '#' ~/.pearrc >%{buildroot}%{_sysconfdir}/pear.conf
php %{SOURCE1} %{buildroot}%{_sysconfdir}/pear.conf %{buildroot}

find %{buildroot} -type f|xargs perl -pi -e "s|%{buildroot}||g;"

# Remove empty files
rm -f %{buildroot}/%{peardir}/.lock

# Remove unwanted file
rm -f %{buildroot}/%{_prefix}/php.ini-gopear

# Create the directory that will contain .xml of additional packages
mkdir %{buildroot}%{peardir}/packages

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README
%dir %{peardir}
%{peardir}/*
%{peardir}/.filemap
%{peardir}/.registry
%{_bindir}/pear
%config(noreplace) %{_sysconfdir}/pear.conf

%changelog
* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- point pear config to actual install paths (#6661) (pterjan)
- provide all included pear packages (pterjan)
- fix registry (pterjan)
- use a tarball instead of downloading at build time (pterjan)
- create %%{peardir}/packages to contain .xml of additional packages
  (pterjan)
- Requires: php-cli (pterjan)

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- php 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- php 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec
- NOTE: this package needs to be re-done in such a way that it does not
  require an active internet connection

* Sat Nov 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for php 4.3.4

* Mon Oct 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- 4.3.3

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-3mdk
- built for 4.3.3

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Tue Jun 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2
- misc spec file fixes

* Tue May 06 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild
- misc spec file fixes

* Sun Feb 16 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-3mdk
- add Mail_Mime and Net_Socket that are required for horde.

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-2mdk
- rebuild

* Mon Jan  6 2003 Jean-Michel Dault <jmdalt@mandrakesoft.com> 4.3.0-1mdk
- Completely remade SPEC file
- Added Log package
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Tue Mar 19 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 4.1.2-20020403.1mdk
- First release of the php-pear package

