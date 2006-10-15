#
# spec file for package tcb
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		tcb
%define version 	1.0
%define release 	%_revrel

%define major		0
%define libname		%mklibname tcb %{major}

Summary:	Libraries and tools implementing the tcb password shadowing scheme
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	BSD or GPL
Group:		System/Libraries
URL: 		http://www.openwall.com/tcb/
Source0:	ftp://ftp.openwall.com/pub/projects/tcb/%{name}-%{version}.tar.gz

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-crypt_blowfish-devel
BuildRequires:	pam-devel

Requires:	%{libname} = %{version}-%{release}
Requires:	pam_tcb = %{version}-%{release}
Requires:	nss_tcb = %{version}-%{release}
Requires(pre):	setup >= 2.5-5873avx

%description
The tcb package consists of three components: pam_tcb, libnss_tcb, and
libtcb.  pam_tcb is a PAM module which supersedes pam_unix and pam_pwdb.
It also implements the tcb password shadowing scheme (see tcb(5) for
details).  The tcb scheme allows many core system utilities (passwd(1)
being the primary example) to operate with little privilege.  libnss_tcb
is the accompanying NSS module.  libtcb contains code shared by the
PAM and NSS modules and is also used by programs from the shadow-utils
package.


%package -n %{libname}
Summary:        Libraries and tools implementing the tcb password shadowing scheme
Group:          System/Libraries
Requires:	glibc-crypt_blowfish
Provides:	libtcb

%description -n %{libname}
libtcb contains code shared by the PAM and NSS modules and is also used
by programs from the shadow-utils package.


%package -n pam_tcb
Summary:	PAM module for TCB
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n pam_tcb
pam_tcb is a PAM module which supersedes pam_unix and pam_pwdb.
It also implements the tcb password shadowing scheme (see tcb(5) for
details).  The tcb scheme allows many core system utilities (passwd(1)
being the primary example) to operate with little privilege.


%package -n nss_tcb
Summary:	NSS library for TCB
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description -n nss_tcb
libnss_tcb is the accompanying NSS module for pam_tcb.


%package -n %{libname}-devel
Summary:	Libraries and header files for building tcb-aware applications
Group:		Development/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	tcb-devel

%description -n %{libname}-devel
This package contains static libraries and header files needed for
building tcb-aware applications.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%serverbuild
CFLAGS="%{optflags} -DENABLE_SETFSUGID" %make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make install-non-root install-pam_unix install-pam_pwdb \
    DESTDIR=%{buildroot} \
    MANDIR=%{_mandir} \
    LIBDIR=%{_libdir} \
    LIBEXECDIR=%{_libdir} \
    SLIBDIR=/%{_lib}


%pre -n %{libname}
# although setup does the same thing, the lib will likely get installed first
# so we need to do this here also or we end up with incorrect ownerships of
# some files
#
# make this optional as it shouldn't be needed on a fresh install
if [ -x /bin/grep ]; then
    grep -q '^chkpwd:' /etc/group || groupadd -g 29 chkpwd
fi


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post -n nss_tcb
/sbin/ldconfig
%_post_srv nscd


%postun -n nss_tcb
/sbin/ldconfig
%_preun_srv nscd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/tcb_convert
/sbin/tcb_unconvert
%{_mandir}/man8/tcb_convert.8*
%{_mandir}/man8/tcb_unconvert.8*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libtcb.so.*
%attr(0710,root,chkpwd) %verify(not mode group) %dir %{_libdir}/chkpwd
%attr(2711,root,shadow) %verify(not mode group) %{_libdir}/chkpwd/tcb_chkpwd
%{_mandir}/man5/tcb.5*

%files -n nss_tcb
%defattr(-,root,root)
/%{_lib}/libnss_tcb.so.2

%files -n pam_tcb
%defattr(-,root,root)
/%{_lib}/security/pam_pwdb.so
/%{_lib}/security/pam_tcb.so
/%{_lib}/security/pam_unix.so
/%{_lib}/security/pam_unix_acct.so
/%{_lib}/security/pam_unix_auth.so
/%{_lib}/security/pam_unix_passwd.so
/%{_lib}/security/pam_unix_session.so
%{_mandir}/man8/pam_pwdb.8*
%{_mandir}/man8/pam_tcb.8*
%{_mandir}/man8/pam_unix.8*

%files -n %{libname}-devel
%defattr(-,root,root)
%_includedir/tcb.h
%{_libdir}/libtcb.a
%{_libdir}/libtcb.so

%files doc
%defattr(-,root,root)
%doc LICENSE


%changelog
* Sun Oct 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- remove the prereqs as this introduces circular dependencies, so only make
  the grep and friends execute if grep actually exists

* Sun Oct 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- fix libtcb's pre-req's (needs grep and shadow-utils for groupadd)

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- add group chkpwd in the lib's %%pre to ensure we get right ownership of files

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- remove the requires on setup for libtcb as it puts us into a dep loop

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- make the lib provide libtcb too

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- fix some requires

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
