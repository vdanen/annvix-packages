%define name ucspi-tcp
%define version 0.88
%define release 7rph

Name:		%{name}
Summary:	tcpserver and tcpclient for building TCP client-server apps
Version:	%{version}
Release:	%{release}
Copyright:	D. J. Bernstein
Group:		System/Servers
URL:		http://cr.yp.to/ucspi-tcp.html
Source:		%{name}-%{version}.tar.bz2
Source1:	%{name}-%{version}-man.tar.bz2
Patch0:		ucspi-tcp-0.88-errno.patch.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}
Packager:	Vincent Danen <vdanen@mandrakesoft.com>

%description
tcpserver and tcpclient are easy-to-use command-line tools for building TCP
client-server applications.

tcpserver waits for incoming connections and, for each connection, runs a
program of your choice.  Your program receives environment variables showing
the local and remote host names, IP addresses, and port numbers.

tcpserver offers a concurrency limit to protect you from running out of
processes and memory.  When you are handling 40 (by default) simultaneous
connections, tcpserver smoothly defers acceptance of new connections.

tcpserver also provides TCP access control features, similar to
tcp-wrappers/tcpd's hosts.allow but much faster.  It's access control rules
are compiled into a hashed format with cdb, so it can easily deal with
thousands of different hosts.

This package includes a recordio tool that monitors all the input and output
of a server.

tcpclient makes a TCP connection and runs a program of your choice.  It sets
up the same environment variables as tcpserver.

This package includes several sample clients built on top of tcpclient:
who@, date@, finger@, http@, tcpcat, and mconnect.

tcpserver and tcpclient conform to UCSPI, the UNIX Client-Server Program
Interface, using the TCP protocol.  UCSPI tools are available for several
different networks.

%prep
%setup -q
%patch0 -p1 -b .errno
echo "gcc %{optflags}" >conf-cc
echo "gcc -s %{optflags}" >conf-ld
echo "/usr" >conf-home


%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT

%make


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/{man5,man8}
install -s -m 755 addcr argv0 date@ delcr finger@ fixcrio http@ mconnect \
  mconnect-io rblsmtpd recordio tcpcat tcpclient tcprules tcprulescheck \
  tcpserver who@ %{buildroot}%{_bindir}
cd $RPM_BUILD_DIR
tar xvyf %{SOURCE1}
cd %{name}-%{version}-man
install -m 644 *.5 %{buildroot}%{_mandir}/man5
install -m 644 *.8 %{buildroot}%{_mandir}/man8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}-man


%files
%defattr (-,root,root)
%doc CHANGES README TODO VERSION
%{_bindir}/addcr
%{_bindir}/argv0 
%{_bindir}/date@ 
%{_bindir}/delcr 
%{_bindir}/finger@ 
%{_bindir}/fixcrio 
%{_bindir}/http@ 
%{_bindir}/mconnect
%{_bindir}/mconnect-io 
%{_bindir}/rblsmtpd 
%{_bindir}/recordio 
%{_bindir}/tcpcat 
%{_bindir}/tcpclient 
%{_bindir}/tcprules 
%{_bindir}/tcprulescheck
%{_bindir}/tcpserver 
%{_bindir}/who@
%{_mandir}/man5/tcp-qualify.5*
%{_mandir}/man8/addcr.8*
%{_mandir}/man8/argv0.8*
%{_mandir}/man8/date@.8*
%{_mandir}/man8/delcr.8*
%{_mandir}/man8/finger@.8*
%{_mandir}/man8/fixcrio.8*
%{_mandir}/man8/http@.8*
%{_mandir}/man8/mconnect.8*
%{_mandir}/man8/rblsmtpd.8*
%{_mandir}/man8/recordio.8*
%{_mandir}/man8/tcpcat.8*
%{_mandir}/man8/tcpclient.8*
%{_mandir}/man8/tcprules.8*
%{_mandir}/man8/tcprulescheck.8*
%{_mandir}/man8/tcpserver.8*
%{_mandir}/man8/who@.8*



%changelog
* Sat Feb  1 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.88-7rph
- build for 9.1
- P0: errno.h handling

* Fri Aug  9 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.88-6rph
- build for 9.0

* Wed May 29 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.88-5rph
- set conf-home to /usr so that who@ and others know where tcpserver and co.
  are located

* Mon Apr 15 2002 Vincent Danen <vdanen@mandrakesoft.com> 0.88-4rph
- rebuild with rph extension

* Wed Jul 19 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.88-3mdk
- macroization

* Thu Jun 29 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.88-2mdk
- include manpages compiled by me from the website

* Wed Jun 28 2000 Vincent Danen <vdanen@linux-mandrake.com> 0.88-1mdk
- first build for mandrake
