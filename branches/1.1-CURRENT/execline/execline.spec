#
# spec file for package execline
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name 		execline
%define version		1.06
%define release		1avx

%define _bindir		/bin

Summary:	light non-interactive scripting language
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Shells
URL:		http://www.skarnet.org/software/%{name}/
Source0:	http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  dietlibc-devel >= 0.28
BuildRequires:  skalibs-devel >= 0.40

%description
execline is a very light, non-interactive scripting language, which is 
similar to a shell. Simple shell scripts can be easily rewritten in the 
execline language, improving performance and memory usage. execline was 
designed for use in embedded systems, but works on most Unix flavors.


%prep
%setup -q -n admin


%build
pushd %{name}-%{version}
    echo "diet gcc -O2 -W -Wall -fomit-frame-pointer -pipe" > conf-compile/conf-cc
    echo "diet gcc -Os -static -s" > conf-compile/conf-ld

    echo "linux-:%{_target_cpu}-:" > src/sys/systype

    echo "%{_includedir}/skalibs" > conf-compile/import
    echo "%{_libdir}/skalibs" >> conf-compile/import

    package/compile
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}/bin

pushd %{name}-%{version}
    for i in `cat package/command.exported` ;  do
        install -m 0755 command/$i %{buildroot}/bin/
    done
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
/bin/*


%changelog
* Tue Aug 23 2005 Sean P. Thomas <spt@annvix.org> 1.06-1avx
- initial Annvix build
