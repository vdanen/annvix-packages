#############################################################################
# Project         : Mandrake Linux
# Module          : rpm-helper
# File            : rpm-helper.spec
# Version         : $Id: rpm-helper.spec,v 1.13 2003/09/17 13:52:51 flepied Exp $
# Author          : Frederic Lepied
# Created On      : Tue Jul  9 08:21:29 2002
# Purpose         : rpm build rules
#############################################################################

Summary: Helper scripts for rpm scriptlets
Name: rpm-helper
Version: 0.9.1
Release: 1mdk
Source0: %name-%version.tar.bz2
License: GPL
Group: System/Configuration/Packaging
URL: http://www.mandrakelinux.com/
BuildArchitectures: noarch
BuildRoot: %_tmppath/%name-buildroot
Conflicts: chkconfig < 1.3.4-10mdk
Requires: chkconfig, grep, shadow-utils, chkconfig, coreutils

%description
Helper scripts for rpm scriptlets to help create/remove :
- groups
- services
- shells
- users

%prep
%setup

%build

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std LIBDIR=%_datadir/%name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README* ChangeLog AUTHORS
%_datadir/%name

%changelog
* Wed Sep 17 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9.1-1mdk
- don't depend on initscripts anymore

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9-1mdk
- added the right requires

* Sun Dec 22 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.8-1mdk
- corrected add-shell to not add the shell multiple times
- corrected add-service when SECURE_LEVEL isn't set
- corrected add-group not to delete supplementary groups already added

* Tue Nov  5 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.7.1-1mdk
- add verify-shell

* Tue Nov  5 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.7-1mdk
- add add-shell and del-shell to update /etc/shells

* Fri Sep  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6-1mdk
- add add-shell and del-shell to update /etc/shells
- add-service: do the security stuff here instead of doing it in chkconfig
to be more flexible.

* Thu Aug  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.5-1mdk
- add-service: on upgrade, restart services that depend of portmap.

* Wed Jul 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.4.1-1mdk
- correct add-group when no user is added to the group

* Mon Jul 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.4-1mdk
- added del-group and add-group

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.3-1mdk
- extend add-user to support extended groups

* Wed Jul 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.2-1mdk
- added create-file

* Tue Jul  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.1-1mdk
- Initial version

# end of file
