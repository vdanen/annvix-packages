%define name	apache-suexec
%define version %{apache_version}
%define release 1sls

%{expand:%%define apache_version %(rpm -q apache-devel|sed 's/apache-devel-\([0-9].*\)-.*$/\1/')}
%{expand:%%define apache_release %(rpm -q apache-devel|sed 's/apache-devel-[0-9].*-\(.*\)$/\1/')}

# the default version of mm required
%define dmm_major	1
%define dmm_minor	3.0

%{expand:%%define mm_major %([ -x /usr/bin/mm-config ] && mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\1/' || echo "%{dmm_major}")}
%{expand:%%define mm_minor %([ -x /usr/bin/mm-config ] && mm-config --version|sed 's/MM \([0-9]\)\.\([0-9.].*\) \(.*\)$/\2/' || echo "%{dmm_minor}")}
%define mm_version %{mm_major}.%{mm_minor}

Summary:	Suexec binary for apache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org/docs/suexec.html
Source0:	apache-suexec.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	ADVX-build >= 1.2 mm-devel
BuildRequires:	apache-devel >= %{apache_version}-%{apache_release} 

Prereq:		apache-common >= %{apache_version}-%{apache_release}
Prereq:		apache-conf >= %{apache_version}
Prereq: 	mm >= %{mm_major}.%{mm_minor}
Requires:	apache
Provides: 	ADVXpackage
Provides:	AP13package

%description
This package adds suexec to Apache. Suexec provides Apache users the ability
to run CGI and SSI programs under user IDs different from the user ID of the
calling web-server. Normally, when a CGI or SSI program executes, it runs as
the same user who is running the web server. 


%prep
%setup -q -n %{name}

APFLAGS=`/usr/sbin/apxs -q CFLAGS`
OPTIONS=$APFLAGS" \
-DHTTPD_USER=\"apache\" \
-DUID_MIN=100 \
-DGID_MIN=100 \
-DUSERDIR_SUFFIX=\"public_html\" \
-DLOG_EXEC=\"/var/log/httpd/suexec_log\" \
-DDOC_ROOT=\"/var/www\" \
-DSAFE_PATH=\"/usr/local/bin:/usr/bin:/bin\" \
-I/usr/include/apache"
echo Configuring with: $OPTIONS
gcc $OPTIONS -o suexec suexec.c

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
install -m 4711 suexec %{buildroot}%{_sbindir}
install suexec.8 %{buildroot}%{_mandir}/man8

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(4710,root,apache) %{_sbindir}/suexec
%{_mandir}/man8/*

%changelog
* Mon May 17 2004 Vincent Danen <vdanen@opensls.org> 1.3.31-1sls
- apache 1.3.31

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 1.3.29-3sls
- fix handling of libmm deps
- some spec cleanups

* Sat Jan 04 2004 Vincent Danen <vdanen@opensls.org> 1.3.29-2sls
- OpenSLS build
- tidy spec

* Sat Nov 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.29-1mdk
- new S0

* Mon Sep 15 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.28-1mdk
- rebuild with new apache

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.3.27-5mdk
- rebuild
- buildrequires

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-4mdk
- new macroized libmm version

* Thu Jan 02 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-3mdk
- rebuilt for new mm version
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Fri Nov  8 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-2mdk
- Rebuild for Cooker

* Mon Oct 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.27-1mdk
- New version

* Wed Aug 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.26-2mdk
- don't specify release number for apache-conf.

* Wed Aug 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.26-1mdk
- rebuild against latest apache.
- fix some var declaration in the spec file (thanks to Oden).

* Mon Apr 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.3.24-1mdk
- Apache 1.3.24.

* Mon Mar 02 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3.23-3mdk
- Moved suexec into its own SRPM so people can recompile it according to
  their settings without recompiling the whole apache.
