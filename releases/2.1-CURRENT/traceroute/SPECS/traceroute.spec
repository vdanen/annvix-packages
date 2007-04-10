#
# spec file for package traceroute
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		traceroute
%define version		1.4a12
%define release		%_revrel

Summary:	Traces the route taken by packets over a TCP/IP network
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Monitoring
URL:		http://www.chiark.greenend.org.uk/ucgi/~richard/cvsweb/debfix/packages/traceroute/
Source:		ftp://ftp.ee.lbl.gov/traceroute-%{version}.tar.bz2
Patch1:		traceroute-1.4a5-secfix.patch
Patch3:		traceroute-1.4a5-autoroute.patch
Patch4:		traceroute-1.4a5-autoroute2.patch
Patch5:		traceroute-1.4a5-unaligned.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  Traceroute displays
the IP number and host name (if possible) of the machines along the
route taken by the packets.  Traceroute is used as a network debugging
tool.  If you're having network connectivity problems, traceroute will
show you where the trouble is coming from along the route.


%prep
%setup -q
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0


%build
export RPM_OPT_FLAGS="%{optflags} -DHAVE_IFF_LOOPBACK -DUSE_KERNEL_ROUTING_TABLE"
%configure
make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sbindir},%{_mandir}/man8}

install traceroute %{buildroot}%{_sbindir}
cp traceroute.8 %{buildroot}%{_mandir}/man8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0755,root,bin) %{_sbindir}/traceroute
%{_mandir}/man8/traceroute.8*


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12-9avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12-8avx
- rebuild

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12-7avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.4a12-6sls
- minor spec cleanups
- remove %%prefix

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.4a12-5sls
- OpenSLS build
- tidy spec
- remove suid bit

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
