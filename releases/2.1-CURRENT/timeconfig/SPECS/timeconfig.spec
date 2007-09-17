#
# spec file for package timeconfig
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		timeconfig
%define version		3.2
%define release		%_revrel

Summary:	Text mode tools for setting system time parameters
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
Source0:	timeconfig-%{version}.tar.bz2
Patch0:		timeconfig-gmt.patch
Patch1:		timeconfig-mdkconf.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	newt-devel
BuildRequires:	popt-devel
BuildRequires:	slang-devel

Requires:	initscripts >= 2.81
Requires(post):	fileutils
Requires(post):	gawk

%description
The timeconfig package contains two utilities: timeconfig and
setclock.  Timeconfig provides a simple text mode tool for configuring
the time parameters in /etc/sysconfig/clock and /etc/localtime. The
setclock tool sets the hardware clock on the system to the current
time stored in the system clock.


%prep
%setup -q
%patch0 -p0 -b .gmt
%patch1 -p0 -b .mdkconf


%build
make RPM_OPT_FLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make PREFIX=%{buildroot}%{_prefix} install
rm -f %{buildroot}%{_libdir}/zoneinfo

# fix indonesian locale, its language code is 'id' not 'in'.
mkdir -p %{buildroot}%{_datadir}/locale/id/LC_MESSAGES

# remove unpackaged files
rm -rf %{buildroot}%{_mandir}/pt_BR/
rm -rf %{buildroot}%{_datadir}/locale/{eu_ES,zh}

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ -L %{_sysconfdir}/localtime ]; then
    _FNAME=`ls -ld %{_sysconfdir}/localtime | awk '{ print $11}' | sed 's/lib/share/'`
    rm %{_sysconfdir}/localtime
    cp -f $_FNAME %{_sysconfdir}/localtime
    if [ -f %{_sysconfdir}/sysconfig/clock ]; then
	grep -q "^ZONE=" %{_sysconfdir}/sysconfig/clock && \
	echo "ZONE=\"$_FNAME\"" | sed -e "s|.*/zoneinfo/||" >> %{_sysconfdir}/sysconfig/clock
    else
	echo "ZONE=\"$_FNAME\"" | sed -e "s|.*/zoneinfo/||" >> %{_sysconfdir}/sysconfig/clock
    fi
fi


%files -f %{name}.lang
%defattr(-,root,root)
%{_sbindir}/*
%{_mandir}/man*/*


%changelog
* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- rebuild against new slang, new newt

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- spec cleanups
- remove locales

* Fri Jun 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- rebuild with gcc4
- remove invalid locale directories

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq
- drop unused sources

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2-15avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2-14avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.2-13avx
- rebuild against new newt/slang

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.2-12avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.2-11sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 3.2-10sls
- remove the console-helper stuff using %%build_opensls

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 3.2-9sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
