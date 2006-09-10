#
# spec file for package subversion
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		subversion
%define svn_version	1.3.2
%define release		%_revrel

%define apache_version	2.0.54
%define mod_version 	%{apache_version}_%{svn_version}
%define mod_dav_name	mod_dav_svn
%define mod_dav_conf	46_%{mod_dav_name}.conf
%define mod_dav_so	%{mod_dav_name}.so
%define mod_authz_name	mod_authz_svn
%define mod_authz_conf	47_%{mod_authz_name}.conf
%define mod_authz_so	%{mod_authz_name}.so

%define build_test 0
%{?_with_test: %{expand: %%global build_test 1}}

Summary:	A Concurrent Versioning system similar to but better than CVS
Name:		%{name}
Version:	%{svn_version}
Release:	%{release}
License:	BSD
Group:		Development/Other
URL:		http://subversion.tigris.org
Source0:	http://subversion.tigris.org/tarballs/%{name}-%{svn_version}.tar.bz2
Source1:	http://subversion.tigris.org/tarballs/%{name}-%{svn_version}.tar.bz2.asc
Source2:	%{mod_dav_conf}
Source3:	%{mod_authz_conf}
Source4:	svn.run
Source5:	svn-log.run
Patch0:		subversion-1.3.0-rc4-fix-svn-config-multiarch.patch
Patch1:		subversion-1.3.1-use_apr1.patch

BuildRoot:	%{_buildroot}/%{name}-%{svn_version}

BuildRequires:	autoconf2.5 >= 2.54
BuildRequires:	libtool >= 1.4.2
BuildRequires:	chrpath
BuildRequires:	python >= 2.2
BuildRequires:	python-devel
BuildRequires:	perl-devel
BuildRequires:	db4-devel
BuildRequires:	neon-devel = 0.24.7
BuildRequires:	httpd-devel >=  %{apache_version}
BuildRequires:	swig-devel >= 1.3.19 
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	libapr >= 1.2.7
BuildRequires:	apr-util >= 1.2.7
BuildConflicts:	libapr = 0.9.7
BuildConflicts:	apr-util = 0.9.7

%description
Subversion is a concurrent version control system which enables one or more
users to collaborate in developing and maintaining a hierarchy of files and
directories while keeping a history of all changes.  Subversion only stores the
differences between versions, instead of every complete file.  Subversion also
keeps a log of who, when, and why changes occured.

This package contains the client, if you're looking for the server end
of things you want %{name}-repos.


%package server
Summary:	Subversion Server
Group:		System/Servers
Requires:	%{name} = %{svn_version}-%{release}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires:	ipsvd

%description server
This package contains a myriad of server for subversion server
and repository admins:
  * hot-backup makes a backup of a svn repo without stopping
  * mirror_dir_through_svn.cgi 
  * various hook scripts
  * xslt example 


%package tools
Summary:	Subversion Repo/Server Tools
Group:		Development/Other
Requires:	%{name}-server =  %{svn_version}-%{release}

%description tools
This package contains a myriad of tools for subversion server
and repository admins:
  * hot-backup makes a backup of a svn repo without stopping
  * mirror_dir_through_svn.cgi 
  * various hook scripts
  * xslt example 


%package -n python-svn
Summary:	Python bindings for Subversion
Group:		Development/Other
Requires:	%{name} = %{svn_version}-%{release}
Provides:	python-subversion = %{svn_version}-%{release}

%description -n python-svn
This package contains the files necessary to use the subversion
library functions within python scripts.


%package -n perl-SVN
Summary:	Perl bindings for Subversion
Group:		Development/Perl
Requires:	%{name} = %{svn_version}-%{release}
Obsoletes:	perl-svn
Provides:	perl-svn = %{version}-%{release}

%description -n	perl-SVN
This package contains the files necessary to use the subversion
library functions within perl scripts.


%package devel
Summary:	Subversion headers/libraries for development
Group:		Development/Other
Provides:	libsvn-devel = %{svn_version}-%{release}

%description devel
This package contains the header files and linker scripts for
subversion libraries.


%package -n httpd-mod_dav_svn
Summary:	Subversion server DSO module for apache
Version:	%{mod_version}	
Group:		System/Servers
Requires:	%{name}-server = %{svn_version}-%{release}
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	httpd-conf >= %{apache_version}
Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-mod_dav >= %{apache_version}
Provides:	apache2-%{mod_dav_name} = %{mod_version}
Obsoletes:	apache2-mod_dav_svn
Obsoletes:	apache-mod_authz_svn

%description -n httpd-mod_dav_svn
Subversion is a concurrent version control system which enables
one or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes. Subversion only stores the differences between versions,
instead of every complete file. Subversion also keeps a log of
who, when, and why changes occured.

This package contains the apache server extension DSO for running
a subversion server.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .fix_svn-config_multiarch
%patch1 -p1 -b .use_apr1

rm -rf neon apr apr-util db4

# fix shebang lines, #111498
perl -pi -e 's|/usr/bin/env perl -w|/usr/bin/perl -w|' tools/hook-scripts/*.pl.in

# fix perms
find . -type f -a -perm 0640 -exec chmod 0644 {} \; 
find . -type f -a -perm 0750 -exec chmod 0755 {} \; 


%build
./autogen.sh

export CFLAGS="-fPIC"
export CXXFLAGS="-fPIC"

./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --libdir=%{_libdir} \
    --localstatedir=%{_localstatedir} \
    --mandir=%{_mandir} \
    --with-apxs=%{_sbindir}/apxs \
    --disable-mod-activation \
    --with-swig=%{_prefix} \
    --disable-static \
    --enable-shared \
    --enable-dso

# put the apache modules in the correct place
perl -pi -e "s|%{_libdir}/httpd|%{_libdir}/httpd-extramodules|g" Makefile subversion/mod_authz_svn/*la subversion/mod_dav_svn/*la

%make all
%make swig-py swig_pydir=%{py_sitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
%make swig-pl


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %{build_test}
echo "###########################################################################"
echo "This can take quite some time to finish, so please be patient..."
echo "Don't be too surprised it the tests takes 30 minutes on a dual xeon machine..."
make LD_LIBRARY_PATH="`pwd`/subversion/bindings/swig/perl/libsvn_swig_perl/.libs:`pwd`/subversion/bindings/swig/python/libsvn_swig_py/.libs:\
`pwd`/subversion/bindings/swig/python/.libs:`pwd`/subversion/libsvn_ra_local/.libs:`pwd`/subversion/svnadmin/.libs:\
`pwd`/subversion/tests/libsvn_ra_local/.libs:`pwd`/subversion/tests/libsvn_fs/.libs:`pwd`/subversion/tests/libsvn_wc/.libs:\
`pwd`/subversion/tests/libsvn_fs_base/.libs:`pwd`/subversion/tests/libsvn_diff/.libs:`pwd`/subversion/tests/libsvn_subr/.libs:\
`pwd`/subversion/tests/libsvn_delta/.libs:`pwd`/subversion/tests/libsvn_repos/.libs:`pwd`/subversion/tests/.libs:\
`pwd`/subversion/svnserve/.libs:`pwd`/subversion/libsvn_fs/.libs:`pwd`/subversion/libsvn_ra/.libs:`pwd`/subversion/libsvn_wc/.libs:\
`pwd`/subversion/mod_dav_svn/.libs:`pwd`/subversion/mod_authz_svn/.libs:`pwd`/subversion/svnlook/.libs:`pwd`/subversion/svndumpfilter/.libs:\
`pwd`/subversion/libsvn_client/.libs:`pwd`/subversion/libsvn_fs_base/bdb/.libs:`pwd`/subversion/libsvn_fs_base/util/.libs:\
`pwd`/subversion/libsvn_fs_base/.libs:`pwd`/subversion/libsvn_diff/.libs:`pwd`/subversion/libsvn_subr/.libs:`pwd`/subversion/svnversion/.libs:\
`pwd`/subversion/libsvn_ra_dav/.libs:`pwd`/subversion/libsvn_ra_svn/.libs:`pwd`/subversion/libsvn_delta/.libs:`pwd`/subversion/libsvn_fs_fs/.libs:\
`pwd`/subversion/libsvn_repos/.libs:`pwd`/subversion/clients/cmdline/.libs:$LD_LIBRARY_PATH" check
%endif

%makeinstall_std

%makeinstall_std install-swig-py swig_pydir=%{py_sitedir}/libsvn swig_pydir_extra=%{py_sitedir}/svn
%makeinstall_std install-swig-pl-lib

# perl bindings
make DESTDIR=%{buildroot} pure_vendor_install -C subversion/bindings/swig/perl/native 

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
cp %{_sourcedir}/%{mod_dav_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_dav_conf}
cp %{_sourcedir}/%{mod_authz_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_authz_conf}

######################
###  client-tools  ###
######################

# various commands
install -m 0755 contrib/client-side/search-svnlog.pl %{buildroot}%{_bindir}
(cd  %{buildroot}/%{_bindir}; ln -s search-svnlog.pl search-svnlog)
install -m 0755 contrib/client-side/svn_all_diffs.pl %{buildroot}%{_bindir}
(cd  %{buildroot}/%{_bindir}; ln -s svn_all_diffs.pl svn_all_diffs)
install -m 0755 contrib/client-side/svn_load_dirs.pl %{buildroot}%{_bindir}
(cd  %{buildroot}/%{_bindir}; ln -s svn_load_dirs.pl svn_load_dirs)
install -m 0755 contrib/client-side/svn-log.pl %{buildroot}%{_bindir}
(cd  %{buildroot}/%{_bindir}; ln -s svn-log.pl svn-log)
install -m 0755 tools/client-side/server-vsn.py %{buildroot}%{_bindir}
(cd  %{buildroot}/%{_bindir}; ln -s server-vsn.py server-vsn)
install -m 0755 tools/client-side/showchange.pl %{buildroot}%{_bindir}
(cd  %{buildroot}/%{_bindir}; ln -s showchange.pl showchange)


####################
###  repo-tools  ###
####################

# hotbackup tool
install -m 0755 tools/backup/hot-backup.py %{buildroot}%{_bindir}
(cd %{buildroot}%{_bindir}; ln -s hot-backup.py hot-backup)

# hook-scripts
install -d -m 0755 %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0644 tools/hook-scripts/commit-access-control.cfg.example %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0755 tools/hook-scripts/commit-access-control.pl %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0755 tools/hook-scripts/commit-email.pl %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0755 tools/hook-scripts/propchange-email.pl %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0644 tools/hook-scripts/svnperms.conf.example %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0755 tools/hook-scripts/svnperms.py %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0755 tools/hook-scripts/mailer/mailer.py %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0644 tools/hook-scripts/mailer/mailer.conf.example %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts
install -m 0644 tools/hook-scripts/README %{buildroot}/%{_datadir}/%{name}-%{svn_version}/repo-tools/hook-scripts

#xslt
install -d -m 0755 %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/xslt
install -m 0644 tools/xslt/svnindex.css %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/xslt
install -m 0644 tools/xslt/svnindex.xsl %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/xslt

#cgi
install -d -m 0755 %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/cgi
install -m 0755 contrib/cgi/mirror_dir_through_svn.cgi %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/cgi
install -m 0644 contrib/cgi/mirror_dir_through_svn.README %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/cgi
install -m 0755 contrib/cgi/tweak-log.cgi %{buildroot}%{_datadir}/%{name}-%{svn_version}/repo-tools/cgi

# install a nice icon for web usage
install -d %{buildroot}/var/www/icons
install -m 0644 notes/logo/256-colour/subversion_logo_hor-237x32.png %{buildroot}/var/www/icons/subversion.png

# fix a missing file...
ln -snf libsvn_diff-1.so.0.0.0 %{buildroot}%{_libdir}/libsvn_diff.so

# install svn-config
perl -pi -e "s|\@SVN_DB_LIBS\@|-ldb|g" svn-config
perl -pi -e "s|\@SVN_DB_INCLUDES\@|-I%{_includedir}/db4|g" svn-config
install -m 0755 svn-config %{buildroot}%{_bindir}

# fix the stupid rpath stuff...
find %{buildroot}%{perl_vendorarch} -type f -name "*.so" | xargs chrpath -d

%kill_lang %{name}
%find_lang %{name}

%multiarch_binaries %{buildroot}%{_bindir}/svn-config

# nuke *.pyc files
find %{buildroot} -name "*.pyc" | xargs rm -f

# cleanup
find %{buildroot} -name "perllocal.pod" | xargs rm -f

# get rid of the devel files for python and perl
rm -f %{buildroot}%{py_sitedir}/libsvn/*.la
rm -f %{buildroot}%{_libdir}/libsvn_swig_py*.so
rm -f %{buildroot}%{_libdir}/libsvn_swig_perl*.so

mkdir -p %{buildroot}%{_localstatedir}/svn/repositories
# service support
mkdir -p %{buildroot}%{_srvdir}/svn/{log,peers,env}
install -m 0740 %{_sourcedir}/svn.run %{buildroot}%{_srvdir}/svn/run
install -m 0740 %{_sourcedir}/svn-log.run %{buildroot}%{_srvdir}/svn/log/run
touch %{buildroot}%{_srvdir}/svn/peers/0
chmod 0640 %{buildroot}%{_srvdir}/svn/peers/0

echo "3690" >%{buildroot}%{_srvdir}/svn/env/PORT
echo "%{_localstatedir}/svn/repositories" >%{buildroot}%{_srvdir}/svn/env/REPOSITORIES

# move some docs
mv subversion/bindings/swig/INSTALL INSTALL.swig
mv subversion/bindings/swig/NOTES NOTES.swig
mv subversion/%{mod_authz_name}/INSTALL INSTALL.%{mod_authz_name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n python-svn -p /sbin/ldconfig
%postun -n python-svn -p /sbin/ldconfig


%post -n perl-SVN -p /sbin/ldconfig
%postun -n perl-SVN -p /sbin/ldconfig


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%pre server
%_pre_useradd svn %{_localstatedir}/svn /bin/false 92


%post server
# Libraries for REPOS ( Repository ) and FS ( filesystem backends ) are in
# server now, so we need a ldconfig
/sbin/ldconfig
%_post_srv svn
pushd %{_srvdir}/svn >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd >/dev/null 2>&1


%preun server
%_preun_srv svn


%postun server -p /sbin/ldconfig


%files 
%defattr(-,root,root)
%{_bindir}/svn
%{_bindir}/svnversion
%{_bindir}/server-vsn*
%{_bindir}/showchange*
%{_bindir}/search-svnlog*
%{_bindir}/svn_all_diffs*
%{_bindir}/svn_load_dirs*
%{_bindir}/svn-log*
%{_bindir}/svnlook
%{_libdir}/libsvn_ra-1.so.*
%{_libdir}/libsvn_ra_dav-1.so.*
%{_libdir}/libsvn_ra_local-1.so.*
%{_libdir}/libsvn_ra_svn-1.so.*
%{_libdir}/libsvn_client*so.*
%{_libdir}/libsvn_wc-*so.*
%{_libdir}/libsvn_delta-*so.*
%{_libdir}/libsvn_subr-*so.*
%{_libdir}/libsvn_diff-*so.*
%{_mandir}/man1/svn*


%files server
%defattr(-,root,root)
%{_bindir}/svnadmin
%{_bindir}/svnserve
%{_bindir}/svndumpfilter
%attr(0770,svn,svn) %dir %{_localstatedir}/svn
%attr(0770,svn,svn) %dir %{_localstatedir}/svn/repositories
%{_libdir}/libsvn_fs*.so.*
%{_libdir}/libsvn_repos-*.so.*
%{_mandir}/man1/svnadmin.1*
%{_mandir}/man8/svnserve.8*
%{_mandir}/man5/svnserve.conf.5*
%{_mandir}/man1/svndumpfilter.1*
%dir %attr(0750,root,admin) %{_srvdir}/svn
%dir %attr(0750,root,admin) %{_srvdir}/svn/log
%dir %attr(0750,root,admin) %{_srvdir}/svn/peers
%dir %attr(0750,root,admin) %{_srvdir}/svn/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/svn/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/svn/log/run
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/svn/peers/0
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/svn/env/PORT
%config(noreplace) %attr(0640,root,admin) %{_srvdir}/svn/env/REPOSITORIES


%files tools
%defattr(-,root,root)
%{_bindir}/hot-backup*
%dir %{_datadir}/%{name}-%{svn_version}/repo-tools
%{_datadir}/%{name}-%{svn_version}/repo-tools/*


%files -n python-svn
%defattr(-,root,root)
%{_libdir}/libsvn_swig_py*.so.*
%dir %{py_sitedir}/svn
%{py_sitedir}/svn/*.py*
%dir %{py_sitedir}/libsvn
%{py_sitedir}/libsvn/*.py*
%{py_sitedir}/libsvn/*.so


%files -n perl-SVN
%defattr(-,root,root)
%{_libdir}/libsvn_swig_perl*.so.*
%{perl_vendorarch}/SVN
%{perl_vendorarch}/auto/SVN
%{_mandir}/man3/SVN::*.3*


%files devel
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/svn-config
%{_bindir}/svn-config
%{_libdir}/libsvn*.la
%{_includedir}/subversion*/*
%{_libdir}/libsvn_*.so


%files -n httpd-mod_dav_svn
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_dav_conf}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_authz_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_dav_so}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_authz_so}
%attr(0644,root,root) %{_var}/www/icons/subversion.png


%files doc
%defattr(-,root,root)
%doc BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README
%doc notes/repos_upgrade_HOWTO
%doc INSTALL.%{mod_authz_name} INSTALL.swig NOTES.swig
%doc tools/examples/*.py


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.2
- spec cleanups
- remove locales

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.2
- spec cleanups

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.2
- rebuild against new db4
- rebuild with old db4.1 removed as it picks up the .so deps

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.2
- 1.3.2
- rebuild against new python

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1
- rebuild against new apr/apr-util/httpd
- add libapr/apr-util buildreq and force it to 1.2.7 so we don't get
  libapr0 and friends picked up
- P1: fix build with apr1
- fix perms before building; most everything is either 0640 or 0750
- make the default repository 0770 so only group svn can access it
- call ldconfig in %%postun server, and also for perl-SVN and python-svn

* Tue May 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.3.1
- 1.3.1
- rebuild against perl 5.8.8
- rebuild against swig 1.3.27
- rename perl-svn to perl-SVN
- P0: fix multiarch support
- spec cleanups
- add -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Oct 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3-1avx
- use the (totally weird) mandriva spec as a base
- rip out java support
- rip out ruby support
- complete overhaul of the spec
- drop doc package
- drop the python/perl devel packages (amusing: the description says that
  it's likely no one will ever need them, but they're packaged anyways)
- don't restart apache when adding the modules, just like the other apache
  modules
- always build the perl and python bindings
- get rid of the xinetd script and use ipsvd to run svnserve

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
