#
# spec file for package timezone
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		timezone
%define version		2007j
%define release		%_revrel
%define epoch		6

# RH 2007c-1.fc6

%define tzdata_version	%{version}
%define tzcode_version	%{version}

Summary:	Timezone data
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Base
Source0:	tzdata-base-0.tar.bz2
Source1:	ftp://elsie.nci.nih.gov/pub/tzdata%{tzdata_version}.tar.gz
Source2:	ftp://elsie.nci.nih.gov/pub/tzcode%{tzcode_version}.tar.gz
Source3:	update-localtime.sh
Patch0:		tzdata-mdvconfig.patch
Patch1:		tzdata-extra-tz-links.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gawk

Conflicts:	glibc < 6:2.2.5

%description
This package contains data files with rules for various timezones
around the world.


%prep
%setup -q -n tzdata

mkdir tzdata%{tzdata_version}
tar xzf %{_sourcedir}/tzdata%{tzdata_version}.tar.gz -C tzdata%{tzdata_version}
mkdir tzcode%{tzcode_version}
tar xzf %{_sourcedir}/tzcode%{tzcode_version}.tar.gz -C tzcode%{tzcode_version}

%patch0 -p1 -b .mdvconfig
%patch1 -p1 -b .extra-tz-links

ln -s Makeconfig.in Makeconfig
cat > config.mk << EOF
objpfx = `pwd`/obj/
sbindir = %{_sbindir}
datadir = %{_datadir}
install_root = %{buildroot}
sysdep-CFLAGS = %{optflags}
EOF


%build
%make
grep -v tz-art.htm tzcode%{tzcode_version}/tz-link.htm > tzcode%{tzcode_version}/tz-link.html


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make install

# nuke unpackaged files
rm -f %{buildroot}%{_sysconfdir}/localtime

# install update-localtime script
mkdir -p %{buildroot}%{_sbindir}
install -m 0755 %{_sourcedir}/update-localtime.sh %{buildroot}%{_sbindir}/update-localtime


%check
make check


%post -p %{_sbindir}/update-localtime


# XXX next glibc updates are expected to remove /etc/localtime
%triggerin -- glibc
if [ ! -f %{_sysconfdir}/localtime ]; then
    %{_sbindir}/update-localtime
fi


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/zdump
%{_sbindir}/zic
%{_sbindir}/update-localtime
%dir %{_datadir}/zoneinfo
%{_datadir}/zoneinfo/*


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 2007j
- 2007j
- rediffed P1
- drop P2; no longer required

* Sat Mar 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 2007c
- stand-alone timezone package taken from Mandriva

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
