#
# spec file for package annvix-release
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		annvix-release
%define version		2.0
%define release		%_revrel

%define distrib		Artemis
%define realversion 	2.0-CURRENT
%define macrofile	%build_sysmacrospath

Summary:	Annvix release file
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://annvix.org/
Group:		System/Configuration
Source0:	CREDITS

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Annvix release and rpm macros files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
rm -rf %{_builddir}/%{name}-%{version} && mkdir %{_builddir}/%{name}-%{version}
cp -av %{_sourcedir}/CREDITS %{_builddir}/%{name}-%{version}/


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
echo "Annvix release %{realversion} (%{distrib}) for %{_target_cpu}" > %{buildroot}%{_sysconfdir}/annvix-release
ln -sf annvix-release %{buildroot}%{_sysconfdir}/release

# create a rpm macros file
mkdir -p %{buildroot}%{_sys_macros_dir}
cat > %{buildroot}%{macrofile} <<EOF
%%annvix_release		%{realversion}
%%annvix_version		%{realversion}
%%annvix_codename	%{distrib}
%%annvix_arch		%{_target_cpu}
%%annvix_os		%{_target_os}
%%_revrel		%%(echo %%{revision}|cut -d ' ' -f 2)avx
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sysconfdir}/annvix-release
%{_sysconfdir}/release
%{macrofile}

%files doc
%defattr(-,root,root)
%doc %{name}-%{version}/CREDITS


%changelog
* Tue Jul 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- spec cleanups

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- add -doc subpackage

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- 2.0-CURRENT (Artemis)

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- fix group

* Wed Feb 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- 1.2-RELEASE (Cerberus)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- Clean rebuild

* Fri Dec 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- obfuscate email addresses

* Fri Dec 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- 1.2-CURRENT (Ares)
- add %%_revrel macro to dynamically set the release based on the subversion
  revision number
- use CREDITS as the source file rather than a tarball

* Fri Oct 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-5avx
- 1.1-RELEASE rather

* Fri Oct 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-4avx
- 1.0-RELEASE: Bachus

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-3avx
- add a rpm macro file

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-2avx
- drop the redhat-release and mandrake-release files; we're pretty much
  incompatible with them now
- s/Mandrake/Mandriva/ in the CREDITS file
- updates to CREDITS file

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-1avx
- long overdue tagging of 1.1-CURRENT (actually got lost somewhere)
- make /etc/release a symlink too

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0-2avx
- 1.0-RELEASE

* Thu Jun 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0-1avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.0-0.2sls
- remove icon
- macros

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 1.0-0.1sls
- 1.0-CURRENT
- for lack of a better icon, we'll leave mandrake-small.gif for the time
  being
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
