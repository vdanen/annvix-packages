Summary: Images used in the Red Hat Linux installer
Name: anaconda-images
Version: 9.2.90
Release: 1.1
Source0: %{name}-%{version}.tar.bz2
License: Copyright © 2004 Red Hat, Inc.  All rights reserved.
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Requires: anaconda-runtime

%description
The anaconda-images package (the "Package") contain image files which
incorporate the Fedora trademark and the RPM logo (the "Marks").  The
Marks are trademarks or registered trademarks of Red Hat, Inc. in the
United States and other countries and are used by permission.

Please see the included COPYING file for information on copying
and redistribution.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING
%dir %{_datadir}/anaconda
%{_datadir}/anaconda/pixmaps
%{_prefix}/lib/anaconda-runtime/boot/syslinux-splash.png


%changelog
* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jan 25 2004 Jeremy Katz <katzj@redhat.com>
- back to test release stuff

* Wed Jan 15 2003 Matt Wilson <msw@redhat.com>
- use %%{_prefix}/lib for syslinux-splash, otherwise this package
  doens't rebuild on lib64 systems

* Tue Oct  1 2002 Jeremy Katz <katzj@redhat.com>
- tweak directory ownership (#74044)

* Thu Sep  5 2002 Jeremy Katz <katzj@redhat.com>
- add COPYING

* Thu Sep  5 2002 Jeremy Katz <katzj@redhat.com>
- syslinux splash is here now

* Wed Sep  4 2002 Jeremy Katz <katzj@redhat.com>
- more rnotes

* Wed Jun 26 2002 Michael Fulbright <msf@redhat.com>
- added new images

* Mon Apr 15 2002 Jeremy Katz <katzj@redhat.com>
- rnotes back to lang subdirectory

* Mon Apr 15 2002 Matt Wilson <msw@redhat.com>
- Added Copyright statement like redhat-logo's (MF #63508)

* Thu Apr 11 2002 Jeremy Katz <katzj@redhat.com>
- update to final splash and rnotes

* Wed Feb 20 2002 Jeremy Katz <katzj@redhat.com>
- make the package noarch

* Mon Dec 17 2001 Jeremy Katz <katzj@redhat.com>
- split out of anaconda package



