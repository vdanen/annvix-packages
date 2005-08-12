#
# spec file for package ipsvd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define	name		ipsvd
%define	version		0.10.1
%define	release		4avx

Summary:	Internet protocol service daemons
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Servers
URL:		http://smarden.org/ipsvd/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		ipsvd-0.10.1-mdk-system_matrixssl.diff.bz2
Patch1:		ipsvd-0.10.1-avx-matrixarch.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.27-2avx
BuildRequires:	matrixssl-devel >= 1.2.2-3avx

%description
ipsvd is a set of internet protocol service daemons for Unix. It 
currently includes a TCP/IP service daemon, and a UDP/IP service 
daemon. 

An internet protocol service (ipsv) daemon waits for incoming 
connections on a local socket; for new connections, it conditionally 
runs an arbitrary program with standard input reading from the 
socket, and standard output writing to the socket (if connected), 
to handle the connection. Standard error is used for logging. 

ipsv daemons can be told to read and follow pre-defined instructions 
on how to handle incoming connections; based on the client's IP 
address or hostname, they can run different programs, set a different 
environment, deny a connection, or set a per host concurrency limit. 

On Linux the network connection optionally can be encrypted using 
SSLv3. 

Normally the ipsv daemons are run by a supervisor process, such as 
runsv from the runit package, or supervise from the daemontools 
package. 

ipsvd can be used to run services normally run by inetd, xinetd, or 
tcpserver. 


%prep
%setup -q -n net
%patch0 -p0
%patch1 -p0
perl -pi -e s"|{ARCH}|${MYARCH}|g" Makefile


%build
pushd %{name}-%{version}/src
    MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6][lb]/arm/'`
    perl -pi -e "s|{ARCH}|${MYARCH}|g" Makefile
    echo "diet gcc -Os -pipe -nostdinc" > conf-cc
    echo "diet gcc -Os -static -s -nostdinc" > conf-ld
    make
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/sbin/
install -d %{buildroot}%{_mandir}/man{5,7,8}

pushd %{name}-%{version}
    for i in ipsvd-cdb sslio tcpsvd udpsvd; do
	install -m 0755 src/$i %{buildroot}/sbin/
    done
popd

install -m 0644 %{name}-%{version}/man/*.5 %{buildroot}%{_mandir}/man5/
install -m 0644 %{name}-%{version}/man/*.7 %{buildroot}%{_mandir}/man7/
install -m 0644 %{name}-%{version}/man/*.8 %{buildroot}%{_mandir}/man8/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
%attr(0755,root,root) /sbin/ipsvd-cdb
%attr(0755,root,root) /sbin/sslio
%attr(0755,root,root) /sbin/tcpsvd
%attr(0755,root,root) /sbin/udpsvd
%attr(0644,root,root) %{_mandir}/man5/ipsvd-instruct.5*
%attr(0644,root,root) %{_mandir}/man7/ipsvd.7*
%attr(0644,root,root) %{_mandir}/man8/sslio.8*
%attr(0644,root,root) %{_mandir}/man8/udpsvd.8*
%attr(0644,root,root) %{_mandir}/man8/ipsvd-cdb.8*
%attr(0644,root,root) %{_mandir}/man8/tcpsvd.8*


%changelog
* Fri Aug 12 2005 Vincent Danen <vdanen@annvix.org> 0.10.1-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 0.10.1-3avx
- rebuild

* Fri Feb 04 2005 Vincent Danen <vdanen@annvix.org> 0.10.1-2avx
- rebuild against new dietlibc

* Thu Jan 20 2005 Vincent Danen <vdanen@annvix.org> 0.10.1-1avx
- 0.10.0
- take an updated P0 from mdk but fix it
- require a newer matrixssl and dietlibc


* Wed Oct 13 2004 Vincent Danen <vdanen@annvix.org> 0.9.6-2avx
- build against newer matrixssl (1.2.2)

* Sat Sep 11 2004 Vincent Danen <vdanen@annvix.org> 0.9.6-1avx
- first Annvix build; to eventually replace ucspi-tcp

* Wed Aug 04 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.6-1mdk
- initial mandrake package
