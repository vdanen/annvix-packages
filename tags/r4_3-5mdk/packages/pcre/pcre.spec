%define buildfor $(awk '{print $4}' /etc/mandrake-release)
%{expand:%%define buildfor7_2 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 7.2 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor8_0 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 8.0 ]; then echo 1; else echo 0; fi)}
%{expand:%%define buildfor8_1 %(A=$(awk '{print $4}' /etc/mandrake-release); if [ "$A" = 8.1 ]; then echo 1; else echo 0; fi)}

%define name pcre
%define major 0
%define libname_orig	%mklibname pcre
%define libname	%{libname_orig}%{major}

# define to update aclocal.m4 with new libtool.m4
%define regenerate_configure 0
%ifarch x86_64 mips
%define regenerate_configure 1
%endif

Summary: 	PCRE is a Perl-compatible regular expression library
Name:	 	%name
Version:	4.3
Release:	5mdk
License: 	BSD-Style
Group: 		File tools
Source:		%name-%version.tar.bz2
Patch0:		%{name}-4.3-avoid-link-path.patch.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
URL: 		http://www.pcre.org/
Requires: 	%{libname} = %{version}

%description
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. 
This package contains a grep variant based on the PCRE library.

%package	-n %{libname}
Group:		System/Libraries
Summary:	PCRE is a Perl-compatible regular expression library
Provides:	%{libname_orig} = %{version}-%{release}

%description	-n %{libname}
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h. The official POSIX name is
regex.h, but I didn't want to risk possible problems with existing files of
that name by distributing it that way. To use it with an existing program that
uses the POSIX API, it will have to be renamed or pointed at by a link.


%package	-n %{libname}-devel
Group:		Development/C
Summary:	Headers and static lib for pcre development
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description	-n %{libname}-devel
Install this package if you want do compile applications using the pcre
library.

%prep
%setup -q
%patch0 -p1 -b .linkpath
%if %{regenerate_configure}
aclocal && autoconf
%endif

%build
%if %buildfor7_2 || %buildfor8_0 || %buildfor8_1
CFLAGS="%optflags" ./configure --prefix=%_prefix --libdir=%_libdir --mandir=%_datadir/man
%else
%configure2_5x --enable-utf8
%endif
%make

# Tests, patch out actual pcre_study_size in expected results
echo 'int main() { printf("%d", sizeof(pcre_study_data)); return 0; }' | \
%{__cc} -xc - -include "internal.h" -o study_size
STUDY_SIZE=`./study_size`
perl -pi -e "s,(Study size\s+=\s+)\d+,\${1}$STUDY_SIZE," testdata/testoutput*
make check

%install
rm -rf $RPM_BUILD_ROOT
%if %buildfor7_2 || %buildfor8_0 || %buildfor8_1
make DESTDIR=$RPM_BUILD_ROOT install
%else
%makeinstall_std
%endif


mkdir -p $RPM_BUILD_ROOT/%_lib
mv $RPM_BUILD_ROOT/%_libdir/lib%{name}.so.%{major}.* $RPM_BUILD_ROOT/%_lib
cd $RPM_BUILD_ROOT/%_libdir
ln -s ../../%_lib/lib%{name}.so.%{major}.* .

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
 
%files
%defattr(-,root,root)
#%doc doc/pcregrep.txt doc/pcregrep.html 

%_mandir/man1/pcregrep.1*
%_mandir/man1/pcretest.1*
%_bindir/pcregrep  
%_bindir/pcretest


#
%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README NON-UNIX-USE 
#%doc doc/pcre.txt doc/pcre.html

/%_lib/lib*.so.*
%_libdir/lib*.so.*


#
%files -n %{libname}-devel
%defattr(-,root,root)
#%doc doc/pcreposix.txt doc/pcreposix.html
#%doc doc/perltest.txt doc/pcretest.txt doc/Tech.Notes

%_libdir/lib*.a
%_libdir/lib*.la
%_libdir/lib*.so
%_includedir/*.h

%_bindir/pcre-config

%_mandir/man3/*.3*

%changelog
* Thu Sep  4 2003 Abel Cheung <deaddog@deaddog.org> 4.3-5mdk
- Patch0: Avoid adding buildroot absolute dir to library linking path
- Remove duplicate manpage in lib package
- Fix provides
- Convert this spec to UTF-8

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.3-4mdk
- Enable UTF-8 support, mklibname, make check

* Tue Jul 08 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 4.3-3mdk
- Rebuild

* Tue Jun 10 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 4.3-2mdk
- Fix #3804

* Wed May 28 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 4.3-1mdk
- 4.3

* Mon May 26 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 3.9-6mdk
- Rebuild

* Wed Jul 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.9-5mdk
- Regenerate configure script with updated libtool.m4 where necessary
- Rpmlint fixes: configure-without-libdir-spec, hardcoded-library-path

* Wed Mar 27 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 3.9-4mdk
- Fix compile on 8.0 8.1

* Fri Feb 15 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 3.9-3mdk
- use %%configure2_5x (not for 7.2 or 8.0, just current)
- use %%makeinstall_std (it was already using 'make install DESTDIR=...')
- fix source permissions (rpmlint)

* Thu Jan 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.9-2mdk
- libpcre needs to go to /lib since /bin/grep uses it

* Sat Jan 12 2002 Laurent MONTEL <lmontel@mandrakesoft.com> 3.9-1mdk
- Update code (3.9)

* Fri Nov 23 2001 Laurent MONTEL <lmontel@mandrakesoft.com> 3.7-1mdk
- Update code (3.7)

* Thu Nov 15 2001 David BAUDENS <baudens@mandrakesoft.com> 3.5-2mdk
- Fix build on 7.2 and 8.0

* Fri Aug 17 2001 Laurent MONTEL <lmontel@mandrakesoft.com> 3.5-1mdk
- Update code

* Sat Apr 14 2001 Laurent MONTEL <lmontel@mandrakesoft.com> 3.4-3mdk
- Clean spec file

* Thu Dec 21 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.4-2mdk
- used srpm from Götz Waschk <waschk@linux-mandrake.com> :
	- new library naming scheme

* Fri Nov 24 2000 Lenny Cartier <lenny@mandrakesoft.com> 3.4-1mdk
- used srpm from Götz Waschk <waschk@linux-mandrake.com> :
	- initial Mandrake package

