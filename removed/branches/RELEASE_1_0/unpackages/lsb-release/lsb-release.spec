%define name	lsb-release
%define version	1.4
%define release	6sls

#
#	Copyright 1999, International Business Machines, Inc.
#	George Kraft IV (gk4@us.ibm.com)
#       Christopher Yeoh (cyeoh@linuxcare.com)
#
#	Red Hat Package Manager (RPM) file for lsb-release
#
# Note that in order to create a package which is LSB compliant
# the value of the _defaultdocdir macro should be /usr/share/doc
# and _mandir should be /usr/share/man
#

Summary:	Linux Standard Base tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://www.linuxbase.org/
Source:		lsb-release-1.4.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root

%description
LSB version query program

This program forms part of the required functionality of
the LSB (Linux Standard Base) specification.

The program queries the installed state of the distribution
to display certain properties such as the version of the
LSB against which the distribution claims compliance as 
well. It can also attempt to display the name and release
of the distribution along with an identifier of who produces
the distribution.

%prep

%setup

%build
make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make prefix=%buildroot mandir=%buildroot/%{_mandir} install 
mkdir -p %buildroot/etc
cat > %buildroot/etc/lsb-release << EOF
LSB_VERSION=1.3
DISTRIB_ID=OpenSLS
DISTRIB_RELEASE=1.0-CURRENT
DISTRIB_CODENAME=Loki
DISTRIB_DESCRIPTION="OpenSLS"
EOF

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
/bin/lsb_release
%{_mandir}/man1/lsb_release.1*
%config(noreplace) /etc/lsb-release

%changelog
* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.4-6sls
- minor spec cleanups
- remove %%prefix

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.4-5sls
- OpenSLS build
- tidy spec

* Mon Jul 28 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.4-4mdk
- Mandrake 9.2, codename TBA

* Mon Mar 31 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.4-3mdk
- LSB1.3, Mandrake 9.1 (bamboo)

* Thu Sep 19 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.4-2mdk
- update for LSB1.2, Mandrake 9.0
- s/Copyright/License/, bzip2 source

* Fri Aug 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.4-1mdk
- first Mandrake Linux version

* Tue Jan  2 2001 Christopher Yeoh <cyeoh@linuxcare.com>
- Update description of package

* Mon Nov  6 2000 Christopher Yeoh <cyeoh@linuxcare.com>
- Repackage for version 1.4
- Add comments about creating an LSB compliant package.

* Thu Nov  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- add %defattr to fix build as non root.
- fix %file for non rh distribution.
- macros.

* Mon Oct 30 2000 Christopher Yeoh <cyeoh@linuxcare.com>
- Repackage so lsb_release goes in /bin

* Sat Oct 21 2000 Christopher Yeoh <cyeoh@linuxcare.com>
- Changes for 1.2 release of lsb_release

* Thu Sep 28 2000 Christopher Yeoh <cyeoh@linuxcare.com>
- Changes for 1.1 release of lsb_release

* Tue Sep 26 2000 Christopher Yeoh <cyeoh@linuxcare.com>
- Clean up script not to trample over currently installed package
- Changes to use new makefile bundled with lsb_release tarball
- Fixes bugs in post commands and adds post uninstall commands

