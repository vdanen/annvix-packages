%define prefix /usr

Summary:        Prelude Hybrid Intrusion Detection System - Network Sensor
Name:           prelude-nids
Version:        0.8.1
Release:        1mdk
License:        GPL
Group:          Networking/Other
URL:            http://www.prelude-ids.org/
Source:		http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
Buildroot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  libprelude-devel flex bison
Requires:	libprelude >= 0.8.4

%description
Prelude NIDS is the network-based sensor program part of the Prelude Hybrid IDS
suite. It provides network monitoring with fast pattern matching (Boyer-Moore)
to detect attacks against a network. It includes advanced mechanisms such as a
generic signature engine which is able to understand any ruleset as long as
there is a dedicated parser, protocol and detection analysis plugins featuring
Telnet, RPC, HTTP, and FTP decoding and preprocessors for cross-platform
polymorphic shellcodes detection, ARP misuse detection, and scanning detection.
It supports IP fragmentation and TCP segmentation to track connections and
detect stateful events. 

%package        devel
Summary:        Libraries, includes, etc. to develop Prelude NIDS 
Group:          Development/C
Requires:       %{name} = %{version}
BuildRequires:  libprelude-devel
Requires:       libprelude

%description devel
Prelude NIDS is the network-based sensor program part of the Prelude Hybrid IDS
suite. It provides network monitoring with fast pattern matching (Boyer-Moore)
to detect attacks against a network. It includes advanced mechanisms such as a
generic signature engine which is able to understand any ruleset as long as
there is a dedicated parser, protocol and detection analysis plugins featuring
Telnet, RPC, HTTP, and FTP decoding and preprocessors for cross-platform
polymorphic shellcodes detection, ARP misuse detection, and scanning detection.
It supports IP fragmentation and TCP segmentation to track connections and
detect stateful events. 
This package contains the headers for developing

%prep
%setup -q -n %{name}-%{version}

tar xvf libpcap.tar
cp libpcap/pcap.h .
# include hack...
for i in `find src -type f -name "Makefile.am"`; do
    perl -pi -e "s|libpcap/pcap.h|pcap.h|g" $i
    perl -pi -e "s|nodist_prelude_nids_SOURCES|#nodist_prelude_nids_SOURCES|g" $i
done


%build
#export WANT_AUTOCONF_2_5=1
#libtoolize --copy --force; aclocal; autoconf; automake

%configure 
%make 

%install
%makeinstall_std 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_bindir}/prelude-nids
%{_libdir}/prelude-nids/detects/*
%{_libdir}/prelude-nids/protocols/*
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/prelude-nids/*

%files devel
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_includedir}/prelude-nids/*.h

%changelog
* Tue Sep 09 2003 Florin Grad <florin@mandrakesoft.com> 0.8.1-1mdk
- first mandrake release
- add the manpage

* Wed Sep 03 2002 Sylvain GIL <prelude-packaging@tootella.org> 0.8.1-2
- Increased libprelude dependency version
* Mon Sep 01 2002 Sylvain GIL <prelude-packaging@tootella.org> 0.8.1-1
-  Initial Packaging.

