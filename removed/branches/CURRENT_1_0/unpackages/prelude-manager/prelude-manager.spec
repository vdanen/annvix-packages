%define name	prelude-manager
%define version	0.8.7
%define release	3sls

%define _localstatedir /var

Summary:	Prelude Hybrid Intrusion Detection System Manager
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.prelude-ids.org/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.init.bz2
Patch0:		%{name}-0.8.7-single_slash_fix.diff.bz2
Patch1:		%{name}-0.8.7-CVS_fix.diff.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libprelude-devel
BuildRequires:	MySQL-devel
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-libs-devel
BuildRequires:	libxml2-devel

PreReq:		rpm-helper
Requires:	libprelude >= 0.8.4
Provides:	prelude
Obsoletes:	prelude >= 0.4.2 prelude-doc

%description
Prelude Manager is the main program of the Prelude Hybrid IDS
suite. It is a multithreaded server which handles connections from
the Prelude sensors. It is able to register local or remote
sensors, let the operator configure them remotely, receive alerts,
and store alerts in a database or any format supported by
reporting plugins, thus providing centralized logging and
analysis. It also provides relaying capabilities for failover and
replication. The IDMEF standard is used for alert representation.
Support for filtering plugins allows you to hook in different
places in the Manager to define custom criteria for alert relaying
and logging. 

%package mysql-plugin
Summary:	MySQL report plugin for Prelude IDS Manager
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	MySQL-shared-libs

%description mysql-plugin
This plugin adds MySQL logging capabilities to the Prelude IDS
Manager.

%package pgsql-plugin
Summary:	PostgreSQL report plugin for Prelude IDS Manager
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	postgresql-libs

%description pgsql-plugin
This plugin adds PostgreSQL logging capabilities to the Prelude IDS
Manager.

%package xml-plugin
Summary:	XML report plugin for Prelude IDS Manager
Group:		System/Servers
Requires:	%{name} = %{version}

%description xml-plugin
This plugin adds XML logging capabilities to the Prelude IDS
Manager.

%package devel
Summary:	Libraries, includes, etc. to develop Prelude IDS Manager plugins
Group:		Development/C
Requires:	%{name} = %{version}
BuildRequires:	libprelude-devel
Requires:	libprelude

%description devel
Prelude Manager is the main program of the Prelude Hybrid IDS
suite. It is a multithreaded server which handles connections from
the Prelude sensors. It is able to register local or remote
sensors, let the operator configure them remotely, receive alerts,
and store alerts in a database or any format supported by
reporting plugins, thus providing centralized logging and
analysis. It also provides relaying capabilities for failover and
replication. The IDMEF standard is used for alert representation.
Support for filtering plugins allows you to hook in different
places in the Manager to define custom criteria for alert relaying
and logging.

Install this package if you want to build Prelude IDS Manager
Plugins.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

# logdir hack
perl -pi -e "s|/var/log/|/var/log/%{name}/|g" %{name}.conf*

bzcat %{SOURCE1} > %{name}.init

%build

export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal; autoconf; automake

%configure2_5x \
    --localstatedir=%{_localstatedir} \
    --enable-static \
    --enable-shared \
    --enable-openssl \
    --enable-mysql \
    --enable-pgsql

#    --enable-gtk-doc \
#    --with-html-dir=%{_datadir}/doc/%{name}-devel-%{version}

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# install init script
install -d %{buildroot}%{_initrddir}
install -m0755 %{name}.init %{buildroot}%{_initrddir}/%{name}

# fix logrotate stuff
install -d %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} << EOF
/var/log/%{name}/prelude.log {
    missingok
    postrotate
        [ -f /var/lock/subsys/%{name} ] && %{_initrddir}/%{name} restart
    endscript
}
EOF

# make the logdir
install -d %{buildroot}/var/log/%{name}
touch %{buildroot}/var/log/%{name}/prelude.log

%post
%_post_service %{name}
touch /var/log/prelude-manager/prelude.log

%preun
%_preun_service %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/%{name}
%{_bindir}/manager-adduser
%{_libdir}/%{name}/decodes/prelude-nids.so
%{_libdir}/%{name}/decodes/prelude-nids.la
%{_libdir}/%{name}/reports/textmod.so
%{_libdir}/%{name}/reports/textmod.la
%{_libdir}/%{name}/reports/debug.so
%{_libdir}/%{name}/reports/debug.la
%dir /var/spool/%{name}
%dir /var/log/%{name}
%ghost %attr(0664,root,root) /var/log/%{name}/prelude.log

%files mysql-plugin
%defattr(-,root,root)
%doc plugins/db/mysql/mysql.sql
%{_bindir}/%{name}-db-create.sh
%{_libdir}/%{name}/db/mysql.so
%{_libdir}/%{name}/db/mysql.la
%{_datadir}/%{name}/mysql/mysql.sql

%files pgsql-plugin
%defattr(-,root,root)
%doc plugins/db/pgsql/postgres.sql
%{_libdir}/%{name}/db/pgsql.so
%{_libdir}/%{name}/db/pgsql.la
%{_datadir}/%{name}/pgsql/postgres.sql

%files xml-plugin
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_libdir}/%{name}/reports/xmlmod.so
%{_libdir}/%{name}/reports/xmlmod.la
%{_datadir}/%{name}/xmlmod/idmef-message.dtd

%files devel
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_libdir}/%{name}/db/mysql.a
%{_libdir}/%{name}/db/pgsql.a
%{_libdir}/%{name}/decodes/prelude-nids.a
%{_libdir}/%{name}/reports/debug.a
%{_libdir}/%{name}/reports/textmod.a
%{_libdir}/%{name}/reports/xmlmod.a
%{_includedir}/%{name}

%changelog
* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.8.7-3sls
- OpenSLS build
- tidy spec
- short descriptions for plugins

* Tue Sep 09 2003 Florin Grad <florin@mandrakesoft.com> 0.8.7-2mdk
- use the modified libprelude

* Mon Sep 08 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.7-1mdk
- initial cooker contrib, used parts from the spec file by Sylvain GIL 
- added new S1
- added P0 and P1

* Sun Jun 16 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4.2-7mdk
- Work around pcap build on the Alpha.
- BuildRequires: libpcre-devel.

* Wed Sep 19 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.4.2-6mdk

- require Prelude Report in order to not confuse the user.
- Doesn't require libpcap anymore

* Sun Sep 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.4.2-5mdk
- Fix some (French-like?) English. ;p
- Quiet untar of source so we don't get an ugly output on the screen.
- Don't list prelude.conf twice.
- Tag /etc/prelude as a directory.
- Don't use /var/tmp as the BuildRoot.

* Sun Sep 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.4.2-4mdk
- make the startup script more robust

* Wed Sep 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.4.2-3mdk
- added logrotate file
- all config => noreplace
- fixed initscript wrt to draknet
- prelude-report depends on prelude
- corrected the log dir location.

* Thu Sep 06 2001 Stefan van der Eijk <stefan@eijk.nu> 0.4.2-2mdk
- BuildRequires:	byacc flex libpcap-devel
- Copyright --> License
- replace RPM_SOURCE_DIR/prelude.init with SOURCE1 (rpmlint)

* Mon Aug 27 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.4.2-1mdk

- Update to 0.4.2

* Thu Mar 29 2001 Yoann Vandoorselaere <yoann@mandrakesoft.com> 0.3-1mdk
- first packaging attempt.

