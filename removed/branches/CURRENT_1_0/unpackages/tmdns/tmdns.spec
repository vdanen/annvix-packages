%define name	tmdns
%define version	0.1
%define release	13sls

%define _prefix	/

Summary:	A Multicast DNS Responder for Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://zeroconf.sourceforge.net/
Group:		System/Servers
Source0:	%{name}-%{version}.tar.bz2
Source1:	tmdns.services
Source2:	tmdns.init
Source3:	update-resolvrdv
Patch1:		tmdns-0.1-paths.patch.bz2
patch2:		tmdns-0.1-local.patch.bz2
Patch3:		tmdns-0.1-libresolv.patch.bz2
Patch4:		tmdns-0.1-64bit-fixes.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	autoconf2.5, automake1.7

Prefix:		%{_prefix}
PreReq:		rpm-helper
Conflicts:	bind

%description
Tmdns is tiny/trivial Multicast DNS Responder for Linux. It should
allow you to take part in a zeroconf environment.

%prep
%setup -q
%patch1 -p1 -b .paths
#%patch2 -p1 -b .local
%patch3 -p1 -b .libresolv
%patch4 -p1 -b .64bit-fixes

%build
%serverbuild
autoconf
%configure2_5x --disable-debug
# [gb] disable SMP build for now, troubles when regenerating configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT/etc/
./server/tmdns -P > $RPM_BUILD_ROOT/etc/tmdns.conf 2>/dev/null
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/etc/$(basename %{SOURCE1})
install -D -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/tmdns
install -D -m755 %{SOURCE3} $RPM_BUILD_ROOT/sbin/$(basename %{SOURCE3})

%post
%_post_service %{name}

%preun
%_preun_service  %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS TODO docs/draft-cheshire-dnsext-multicastdns.txt
%config(noreplace) %attr(755,root,root) %{_initrddir}/%{name}
%config(noreplace) /etc/tmdns.conf
%config(noreplace) /etc/tmdns.services
/sbin/*

%changelog
* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 0.1-13sls
- OpenSLS build
- tidy spec

* Tue Aug 19 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1-12mdk
- Patch3: Fix detection of libresolv on AMD64
- Patch4: Some 64-bit fixes through code inspection

* Fri Mar 14 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-11mdk
- probe == false in init.d/ script (thanks: dirk.egert).

* Wed Feb 26 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-10mdk
- Conflicts: bind.

* Sat Feb  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1-9mdk
- implement update-resolvrdv -r
- call update-resolvrdv in init script
- don't require zcip as it can work without a zeroconf address

* Fri Jan 31 2003 Stefan van der Eijk <stefan@eijk.nu> 0.1-8mdk
- BuildRequires

* Thu Jan 30 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1-7mdk
- allow non local addresses

* Tue Jan 21 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-6mdk
- chmod(0644) /etc/resolv.conf after rewriting it.

* Mon Jan 20 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-5mdk
- Another fix of update-resolvrdv.

* Mon Jan 20 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-4mdk
- Requires: zcip.
- update-resolvrdv: Check that tmdns is launched before doing stuff.

* Mon Jan 20 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-3mdk
- Add update-resolvrdv script.

* Fri Jan 17 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.1-2mdk
- only register local addresses

* Fri Jan 17 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.1-1mdk
- Firs packaging.

# end of file
