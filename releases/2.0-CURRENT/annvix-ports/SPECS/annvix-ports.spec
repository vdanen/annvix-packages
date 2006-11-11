#
# spec file for package annvix-ports
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		annvix-ports
%define version		1.4
%define release		%_revrel

%define _portsprefix	/usr/local

Summary:	Annvix ports package
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/ports/?root=tools
Group:		System/Configuration
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	rsync
Requires:	curl
Requires:	rpm-build
Requires(pre):	rpm-helper
Requires(post):	sudo
Requires(post):	apt

%description
The filesystem layout and builder scripts for Annvix ports.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_portsprefix}/ports/{ports,packages/{RPMS.ports,SRPMS.ports,base},override}}
install -m 0644 README %{buildroot}%{_portsprefix}/ports/README
install -m 0750 builder %{buildroot}%{_portsprefix}/ports/builder
install -m 0750 worker %{buildroot}%{_portsprefix}/ports/worker
install -m 0750 builder-wrapper %{buildroot}%{_bindir}/builder


%pre
%_pre_useradd builder %{_portsprefix}/ports /bin/sh 403
/usr/sbin/usermod -G ctools builder


%post
if [ "`grep -q 'added by annvix-ports' /etc/sudoers ; echo $?`" == 1 ]; then
    echo "
# added by annvix-ports
%admin  ALL= (builder) /bin/sh /usr/local/ports/builder*
builder ALL = NOPASSWD: /usr/bin/apt-get
" >>/etc/sudoers
else
    if [ "`grep builder /etc/sudoers | grep -q urpmi ; echo $?`" == 0 ]; then
        perl -pi -e 's|/usr/sbin/urpmi.addmedia, /usr/sbin/urpmi.update, /usr/sbin/urpmi|/usr/bin/apt-get|' /etc/sudoers
    fi
fi
if [ "`grep -q 'added by annvix-ports' /etc/apt/sources.list ; echo $?`" == 1 ]; then
    echo "
# added by annvix-ports
rpm file:/usr/local/ports packages ports
" >>/etc/apt/sources.list
fi


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_portsprefix}/ports
%attr(0775,builder,admin) %dir %{_portsprefix}/ports/packages
%attr(0775,builder,admin) %dir %{_portsprefix}/ports/packages/base
%attr(0775,builder,admin) %dir %{_portsprefix}/ports/packages/RPMS.ports
%attr(0775,builder,admin) %dir %{_portsprefix}/ports/packages/SRPMS.ports
%attr(2775,builder,admin) %dir %{_portsprefix}/ports/ports
%attr(1775,builder,admin) %dir %{_portsprefix}/ports/override
%{_portsprefix}/ports/README
%attr(0750,root,builder) %{_portsprefix}/ports/builder
%attr(0750,root,builder) %{_portsprefix}/ports/worker
%attr(0750,root,admin) %{_bindir}/builder


%changelog
* Fri Nov 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4
- refreshed tarball

* Fri Nov 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4
- 1.4 (support for status flags)

* Fri Nov 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3
- 1.3
- make sudoers and apt's sources.list work with new builder (using
  apt, not urpmi)
- call usermod to add builder to the ctools group

* Sat Sep 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- fix URL

* Tue Jul 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- spec cleanups

* Wed Jun 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- only touch /etc/sudoers if we don't already have an entry for ports stuff

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- minor spec cleanups
- updated url
- prereq on rpm-helper

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- if the urpmi media ports doesn't exist when building the first package,
  prompt the user to set it up first

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- Clean rebuild

* Wed Dec 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- fix the sudo invocation for a cleaner environment

* Wed Dec 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- 1.2
- hefty working to handle %%_revrel, sudo controls, and running as user
  builder
- Requires: s/cvs/rsync/
- update the sudoers file

* Mon Oct 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-5avx
- fix some wierdness with the spec that turned README into README.ports

* Sun Oct 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-4avx
- add uid/gid 403 for user builder (in prep of a single-uid
  controlled ports build system)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-3avx
- bootstrap build (new gcc, new glibc)

* Fri Aug 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-2avx
- make builder chmod files after checkout from CVS so they're
  writable by group admin
- make /usr/local/ports/ports g+s so any new files are owned by
  user:admin (but since we don't change the umask, we still need
  to chmod)
- make /usr/local/ports/override to mimic the system /override for
  building rpm packages

* Wed Aug 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-1avx
- 1.1 (aka ports should work now even if it's not 100%)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-4avx
- rebuild

* Mon Mar 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-3avx
- Annvix build

* Thu Jun  3 2004 Vincent Danen <vdanen@opensls.org> 1.0-2sls
- Requires: rpm-build

* Fri May 28 2004 Vincent Danen <vdanen@opensls.org> 1.0-1sls
- first package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
