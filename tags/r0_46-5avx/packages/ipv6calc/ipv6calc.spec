%define name	ipv6calc
%define version	0.46
%define release	5avx

Summary:	IPv6 address format change and calculation utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
URL:		http://www.deepspace6.net/projects/ipv6calc.html
Source0:	ftp://ftp.deepspace6.net/pub/ds6/sources/ipv6calc/%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	openssl-devel

%description
ipv6calc is a small utility which formats and calculates IPv6
addresses in different ways.

Install this package, if you want to extend the existing address
detection on IPv6 initscript setup or make life easier in adding
reverse IPv6 zones to DNS or using in DNS queries like nslookup -q=ANY
`ipv6calc -r 3ffe:400:100:f101::1/48` See also here for more details:
http://www.bieringer.de/linux/IPv6/ipv6calc/ .

%prep

%setup -q

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

%build

%configure

%make CFLAGS="%{optflags} -I../getopt/ -I../ -I../lib/"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/bin
install -d %{buildroot}%{_bindir}

install -m0755 ipv6calc/ipv6calc %{buildroot}/bin/
install -m0755 ipv6logconv/ipv6logconv %{buildroot}%{_bindir}/
install -m0755 ipv6logstats/ipv6logstats %{buildroot}%{_bindir}/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README CREDITS TODO
%doc doc/ipv6calc.html ipv6calcweb/ipv6calcweb.cgi
%doc examples/analog/analog-dist.cfg
%doc examples/analog/analog-dist-combined.cfg
%doc examples/analog/analog-ipv6calc-descriptions.txt
%doc examples/analog/ipv6calc.tab
%doc examples/analog/run_analog.sh
%attr(0755,root,root) /bin/ipv6calc
%attr(0755,root,root) %{_bindir}/ipv6logconv
%attr(0755,root,root) %{_bindir}/ipv6logstats

%changelog
* Thu Jan 06 2005 Vincent Danen <vdanen@annvix.org> 0.46-5avx
- rebuild against new openssl

* Tue Aug 17 2004 Vincent Danen <vdanen@annvix.org> 0.46-4avx
- rebuild against new openssl

* Thu Jun 24 2004 Vincent Danen <vdanen@annvix.org> 0.46-3avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.46-2sls
- minor spec cleanups

* Wed Dec 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.46-1sls
- initial OpenSLS package, used bits from PLD
