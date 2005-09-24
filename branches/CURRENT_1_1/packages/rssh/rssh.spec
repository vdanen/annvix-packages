#
# spec file for package rssh
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		rssh
%define version		2.2.3
%define release		1avx

Summary:	Restricted shell for scp or sftp
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Networking/Remote access
URL:		http://www.pizzashack.org/rssh/
Source:		http://prdownloads.sourceforge.net/rssh/%{name}-%{version}.tar.gz

BuildRoot:	%_tmppath/%{name}-%{version}
BuildRequires:	openssh-clients openssh-server

Requires:	openssh

%description
rssh is a restricted shell for use with ssh, which allows the system
administrator to restrict a user's access to a system via scp or sftp, or
both.


%prep
%setup -q


%build
%configure2_5x \
    --with-sftp-server=%_libdir/ssh/sftp-server
%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
install -m 0755 -D conf_convert.sh %buildroot%_datadir/%name/conf_convert.sh


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog CHROOT COPYING README SECURITY TODO
%config(noreplace) %{_sysconfdir}/rssh.conf
%attr(755,root,root) %{_bindir}/rssh
%attr(4755,root,root) %{_libexecdir}/rssh_chroot_helper
%dir %_datadir/%name
%_datadir/%name/conf_convert.sh
%{_mandir}/man*/*


%changelog
* Sat Sep 24 2005 Vincent Danen <vdanen@annvix.org> 2.2.3-1avx
- first Annvix package

* Sat Apr 09 2005 Olivier Thauvin <nanardon@zarb.org> 2.2.3-2mdk
- help him to sftp-server for lib64 arch

* Sat Jan 15 2005 Goetz Waschk <waschk@linux-mandrake.com> 2.2.3-1mdk
- New release 2.2.3

* Sat Oct 23 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.2.2-1mdk
- New release 2.2.2

* Sat Jun 19 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.2.1-1mdk
- New release 2.2.1

* Tue May 11 2004 Götz Waschk <waschk@linux-mandrake.com> 2.2.0-1mdk
- add %_datadir/%name/conf_convert.sh to migrate from 2.1.1
- New release 2.2.0

* Tue May 11 2004 Götz Waschk <waschk@linux-mandrake.com> 2.1.1-1mdk
- initial mdk package
