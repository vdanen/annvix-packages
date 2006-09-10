#
# spec file for package chkconfig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		chkconfig
%define version		1.3.25
%define release		%_revrel

Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		ftp://ftp.redhat.com/pub/redhat/code/chkconfig/
Source:		ftp://ftp.redhat.com/pub/redhat/code/chkconfig/chkconfig-%{version}.tar.bz2
Patch1:		ntsysv-mdkconf.patch
Patch3:		chkconfig-runleveldir.patch
Patch4:		ntsysv-tvman.patch
Patch5:		chkconfig-fix.patch
Patch7:		chkconfig-1.3.4-list.patch
Patch8:		chkconfig-1.3.4-skip-files-with-dot.patch
Patch10:	chkconfig-1.3.11-fix-errno-xinetddotd.patch
Patch11:	chkconfig-1.3.25-lsb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	newt-devel
BuildRequires:	popt-devel
BuildRequires:	slang

Requires(pre):	setup
Conflicts:	rpm-helper < 0.6

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc*.d, to relieve system administrators of some 
of the drudgery of manually editing the symbolic links.


%package -n ntsysv
Summary:	A system tool for maintaining the /etc/rc*.d hierarchy
Group:		System/Configuration
Requires:	chkconfig

%description -n ntsysv
ntsysv updates and queries runlevel information for system services.
ntsysv relieves system administrators of having to directly manipulate
the numerous symbolic links in /etc/rc*.d.


%prep
%setup -q
%patch1 -p0 -b .mdkconf
%patch3 -p1 -b .runleveldir
%patch4 -p0 -b .tvman
%patch5 -p0 -b .fix
%patch7 -p1 -b .list
%patch8 -p1 -b .skip-files-with-dot
%patch10 -p1 -b .fix-errno-xinetddotd
%patch11 -p1 -b .lsb


%build
%ifarch sparc
LIBMHACK=-lm
%endif

%make RPM_OPT_FLAGS="%{optflags}" LIBMHACK=$LIBMHACK


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make instroot=%{buildroot} MANDIR=%{_mandir} install

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc${n}.d
done

pushd %{buildroot}%{_sysconfdir}/
    ln -s rc.d/init.d init.d
popd

# we use our own alternative system
rm -f %{buildroot}%{_sbindir}/{alternatives,update-alternatives} %{buildroot}%{_mandir}/man8/alternatives.8*

# remove invalid locales
rm -rf %{buildroot}%{_datadir}/locale/{bn_IN,si}

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%attr(0750,root,admin) /sbin/chkconfig
%{_mandir}/man8/chkconfig.8*
%attr(0750,root,admin) %dir %{_sysconfdir}/rc.d
%attr(0750,root,admin) %dir %{_sysconfdir}/rc.d/init.d
%attr(0750,root,admin) %dir %{_sysconfdir}/rc.d/rc*
%{_sysconfdir}/init.d

%files -n ntsysv
%defattr(-,root,root)
%{_sbindir}/ntsysv
%{_mandir}/man8/ntsysv.8*


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- remove locales

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- require setup before install to get group admin
- spec cleanups

* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- remove the pre-req on initscripts as it really isn't needed
  (initscripts has a pre-req on this pkg), and it puts rpm into a loop
  that causes all kinds of stupidness

* Tue Jul 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.25
- 1.3.25
- updated P11 from Mandriva:
  - drop hybrid LSB support, mostly merged upstream
  - simplify requirements check on delete
  - check for requirements when on add
- drop P6; we don't use xinetd
- own and set perms for /etc/rc.d (750/root:admin)
- chkconfig doesn't need to be run by normal users so fix it's perms too
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.20-1avx
- 1.3.20
- drop P9; fixed upstream
- rediff P12; now handles hybrid scripts like shorewall (sbenedict)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.13-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.13-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.3.13-1avx
- 1.3.13
- fix LSB logic (flepied)
- drop the zh po file (S1) and special accomodations

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.3.8-6avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.3.8-5sls
- minor spec cleanups

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.3.8-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
