%define name	ADVX-build
%define version	10
%define release	1avx

Summary:	ADVX-build contains tools and macros to build ADVX
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.advx.org/devel/policy.php
Source0:	ADVX-build.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch

%description
ADVX-build contains a set of tools and macros to build ADVX
components, including Apache 2.

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/ADVX
bzcat %{SOURCE0} > %{buildroot}%{_datadir}/ADVX/ADVX-build

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
echo "See http://www.advx.org/devel.policy.php for more info" > \
        %{buildroot}%{_docdir}/%{name}-%{version}/README

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ "./%{name}" != "/" ] && rm -rf ./%{name}

%files 
%defattr(-,root,root)
%doc %{_docdir}/%{name}-%{version}/README
%dir %{_docdir}/%{name}-%{version}
%dir %{_datadir}/ADVX
%attr(0644,root,root) %{_datadir}/ADVX/*

%changelog
* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 10-1avx
- 10
- remove redundant provides

* Fri Jun 18 2004 Vincent Danen <vdanen@annvix.org> 9.2-5avx
- Annvix build

* Mon Feb 09 2004 Vincent Danen <vdanen@opensls.org> 9.2-4sls
- spec cleanups
- own %%{_datadir}/ADVX

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 9.2-3sls
- OpenSLS build
- tidy spec

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 9.2-2mdk
- Rebuild to fix bad signature

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 9.2-1mdk
- 9.2 (to reflect next distro version)
- remove versioned dirs to ease upgrades
- added a macro to install into libexecdir

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.2-1mdk
- Add AP13pre macro to check the presence and sanity of config files when
  installing 1.3 modules.

* Mon Jan 06 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.1-2mdk
- Change ADVXdir to %{_datadir} to compli with the FHS/LSB.
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we ca easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Mon Jan 06 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.1-1mdk
- Change apxs to apxs2 and /usr/include/apache to /usr/include/apache2
  to be able to work on Apache 1.3 and 2.0 at the same time.

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0-3mdk
- don't strip files on install

* Fri Sep 6 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.0-2mdk
- noarch
- clean after build

* Wed Sep 4 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.0-1mdk
- New package
