%define libdaemonver 0.2

Summary: Detect and perform actions when an ethernet cable is (un)plugged.
Name: ifplugd
Version: 0.15
Release: 4mdk
Source0: http://www.stud.uni-hamburg.de/~lennart/projects/ifplugd/%{name}-%{version}.tar.bz2
Source1: http://www.stud.uni-hamburg.de/~lennart/projects/libdaemon/libdaemon-%{libdaemonver}.tar.bz2
Patch0: ifplugd-0.14-exit-status.patch.bz2
Patch1: ifplugd-0.15-force-up-on-error.patch.bz2
Patch2: ifplugd-0.15-startup.patch.bz2
License: GPL
Group: System/Configuration/Networking
URL: http://www.stud.uni-hamburg.de/users/lennart/projects/ifplugd/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires:	doxygen lynx

%description
ifplugd is a Linux daemon which will automatically configure your
ethernet device when a cable is plugged in and automatically
unconfigure it if the cable is pulled. This is useful on laptops with
onboard network adapters, since it will only configure the interface
when a cable is really connected.

%prep
%setup -q -a1
%patch0 -p1 -b .exit-status
%patch1 -p1 -b .force-up-on-error
%patch2 -p1 -b .startup

perl -p -i -e 's@/usr/local@@' man/*.[58]

%build
cd libdaemon-%{libdaemonver}
%configure2_5x
%make
rm -f src/.libs/*.so*
cd ..
ln -s $PWD/libdaemon-%{libdaemonver}/src libdaemon
export CPPFLAGS=-I.
export LDFLAGS=-L$PWD/libdaemon-%{libdaemonver}/src/.libs
%configure2_5x	--sbindir=/sbin
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/ifplugd
#mv $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/README doc/NEWS doc/README.html doc/style.css LICENSE
/sbin/ifplugd
/sbin/ifstatus
%{_mandir}/man?/ifplugd*
%{_mandir}/man?/ifstatus*
%dir %{_sysconfdir}/ifplugd
%config(noreplace) %{_sysconfdir}/ifplugd/ifplugd.conf
%config(noreplace) %{_sysconfdir}/ifplugd/ifplugd.action

%changelog
* Wed Aug 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.15-4mdk
- corrected startup sequence to prevent a bug when called from hotplug
- corrected patch1

* Wed Jul 16 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.15-3mdk
- yet another buildrequires darn it

* Wed Jul 16 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.15-2mdk
- drop Prefix tag
- buildrequires
- macroize
- pass sbindir to configure so we don't have to move it after install
- own %%{_sysconfdir}/ifplugd

* Mon Jul  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.15-1mdk
- 0.15

* Mon Mar  3 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.13-3mdk
- corrected handling of error case.

* Mon Feb 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.13-2mdk
- corrected exit status to conform to Un*x standard

* Sat Feb  1 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.13-1mdk
- 0.13
- removed patch2 (integrated upstream)

* Sat Feb  1 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.12-4mdk
- corrected patch2 with author's feedback

* Fri Jan 24 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.12-3mdk
- corrected log management

* Thu Jan 16 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.12-2mdk
- on unsupported cards, force ifup

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.12-1mdk
- initial Mandrake Linux packaging

# end of file
