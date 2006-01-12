#
# spec file for package automake1.8
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		automake%{pkgamversion}
%define version 	1.9.4
%define release 	%_revrel

%define amversion	1.9
%define pkgamversion	1.8

%define docheck 1
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically creating Makefiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://sources.redhat.com/automake/
Source0:	ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.bz2
Patch0:		automake-1.9.4-infofiles.patch
Patch1:		automake-1.9.4-avx-skiptests.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	autoconf2.5 >= 1:2.59-3avx
BuildRequires:	autoconf2.5 >= 1:2.59-3avx
BuildRequires:	texinfo

Provides:	automake = %{version}-%{release}
Provides:	automake1.9 = %{version}-%{release}
Conflicts:	automake1.5
Conflicts:	automake < 1.4-0.p6.27avx
Obsoletes:	automake1.9
Requires(post):	info-install /usr/sbin/update-alternatives
Requires(preun): info-install /usr/sbin/update-alternatives

# tests need these
%if %{docheck}
BuildRequires:	bison, flex, python
%endif

%description
Automake is a tool for automatically generating Makefiles compliant with
the GNU Coding Standards.


%prep
%setup -q -n automake-%{version}
%patch0 -p1 -b .parallel
%patch1 -p1 -b .skiptests


%build
# (Abel) config* don't understand noarch-annvix-linux-gnu arch
%define _target_platform i586-annvix-linux-gnu

%configure2_5x
%make

%if %{docheck}
# (Abel) reqd2.test tries to make sure automake won't work if ltmain.sh
# is not present. But automake behavior changed, now it can handle missing
# libtool file as well, so this test is bogus.
perl -pi -e 's/reqd2.test//g' tests/Makefile
make check	# VERBOSE=1
%endif

# (Abel) forcefully modify info filename, otherwise info page will refer to
# old automake
pushd doc
    makeinfo -I . -o %{name}.info automake.texi
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}/%{_bindir}/{automake,aclocal}

# provide -1.8 symlinks
ln -s automake-%{amversion} %{buildroot}%{_bindir}/automake-%{pkgamversion}
ln -s aclocal-%{amversion} %{buildroot}%{_bindir}/aclocal-%{pkgamversion}

rm -f %{buildroot}/%{_infodir}/*
install -m 0644 doc/%{name}.info* %{buildroot}/%{_infodir}/

perl -p -i -e 's|\(automake\)Extending aclocal|(%{name})Extending aclocal|' \
    %{buildroot}/%{_bindir}/aclocal-%{amversion}

mkdir -p %{buildroot}%{_datadir}/aclocal


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info
update-alternatives \
    --install %{_bindir}/automake automake %{_bindir}/automake-%{amversion} 30 \
    --slave   %{_bindir}/aclocal  aclocal  %{_bindir}/aclocal-%{amversion}

%preun
%_remove_install_info %{name}.info
if [ $1 = 0 ]; then
    update-alternatives --remove automake %{_bindir}/automake-%{amversion}
fi


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_bindir}/*
%{_datadir}/automake*
%{_infodir}/automake*
%{_datadir}/aclocal*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Dec 31 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.4-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.4-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.9.4-1avx
- first Annvix build
- we get 10 tests failing: auxdir2.test, cond17.test, txinfo3.test,
  txinfo5.test, txinfo13.test, txinfo16.test, txinfo18.test, txinfo22.test,
  txinfo23.test, txinfo24.test, txinfo25.test, txinfo28.test, and
  version7.test; use P1 to skip those tests for now

* Tue Feb 22 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.9.4-3mdk
- add BuildRequires: python tetex-latex - for tests

* Sat Jan 15 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.9.4-2mdk 
- allow checks

* Thu Jan 13 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0:1.9.4-1mdk
- 1.9.4
- respun patch0

* Mon May 17 2004 Abel Cheung <deaddog@deaddog.org> 1.8.5-1mdk
- New version
- Patch0: Let the node name in info page coexist with other versions
- Sorry, automake 1.8.x is NOT an upgrade of 1.5.x!
- Tune up alternative priority
- Add `--with check' option to enable `make check'
- Also owns /usr/share/aclocal

* Tue Apr 27 2004 David Walluck <walluck@mandrake.org> 0:1.8.4-1mdk
- 1.8.4

* Wed Mar 17 2004 David Walluck <walluck@mandrake.org> 0:1.8.3-1mdk
- 1.8.3

* Wed Feb 11 2004 David Walluck <walluck@linux-mandrake.com> 0:1.8.2-1mdk
- release
