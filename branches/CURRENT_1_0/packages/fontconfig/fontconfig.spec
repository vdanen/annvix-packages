%define name	fontconfig
%define version	2.2.1
%define release	8sls

%define fontconfig_major	1
%define lib_name		%mklibname %{name} %{fontconfig_major}

%define freetype_version	2.1.4

Summary:	Font configuration library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/XFree86
URL:		http://fontconfig.org/
Source:		http://fontconfig.org/release/fontconfig-%{version}.tar.bz2

# (fc) 2.0-5mdk don't add build date in configuration file 
Patch3:		fontconfig-2.1.94-builddate.patch.bz2
# (fc) 2.1-4mdk Blacklist certain fonts that freetype can't handle (rawhide)
Patch5:		fontconfig-2.1-blacklist.patch.bz2
# (fc) 2.1-4mdk support for slighthint is back (rawhide)
Patch6:		fontconfig-2.1-slighthint.patch.bz2
# (fc) 2.1-4mdk default configuration (rawhide) + (pablo) 2.2-3mdk adds font aliases for various languages
Patch7:		fontconfig-2.2.1-defaultconfig.patch.bz2
# (fc) 2.2.1-6mdk fix crash when HOME is not defined (bug #4518)
Patch8:		fontconfig-2.2.1-home.patch.bz2

BuildRoot:	%{_tmppath}/fontconfig-%{version}-root
BuildRequires:	ed

BuildRequires:	freetype2-devel >= %{freetype_version}
BuildRequires:	expat-devel

PreReq:		%{lib_name}  >= %{version}-%{release}

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package -n %{lib_name}
Summary:	Font configuration and customization library
Group:		System/Libraries
Requires:	%{name} >= %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Provides:	%{name}-libs = %{version}-%{release}

%description -n %{lib_name}
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package -n %{lib_name}-devel
Summary:	Font configuration and customization library
Group:		Development/C
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Requires:	freetype2-devel >= %{freetype_version}
Requires:	expat-devel

%description -n %{lib_name}-devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%prep
%setup -q
%patch3 -p1 -b .builddate
%patch5 -p1 -b .blacklist
%patch6 -p1 -b .slighthint
%patch7 -p1 -b .defaultconfig
%patch8 -p1 -b .home

%build

%configure --with-add-fonts="/usr/X11R6/lib/X11/fonts,/opt/ttfonts,/usr/share/yudit/fonts" --disable-docs
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/fontconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%{_bindir}/fc-cache -f >/dev/null

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README AUTHORS COPYING doc/fontconfig-user.html doc/fontconfig-user.txt
%{_bindir}/fc-cache
%{_bindir}/fc-list
%dir %{_sysconfdir}/fonts
%{_sysconfdir}/fonts/fonts.dtd
%config(noreplace) %{_sysconfdir}/fonts/*.conf
%{_mandir}/man5/*

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc doc/fontconfig-devel doc/fontconfig-devel.txt 
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> - 2.2.1-8sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> - 2.2.1-7sls
- OpenSLS build
- tidy spec

* Wed Aug 20 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.2.1-6mdk
- Patch8 : fix crash when HOME is not defined (bug #4518)

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.2.1-5mdk
- Add Provides: libfontconfig, fontconfig-libs

* Thu Aug  7 2003 Pixel <pixel@mandrakesoft.com> 2.2.1-4mdk
- rebuilding, since pablo forgot to upload libfontconfig :-/

* Wed Aug 06 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.2.1-3mdk
- Changed name of Urdu Nastaliq font

* Wed Jul 23 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.2.1-2mdk
- added some fonts to sans/serif/mono aliases
- put back the special rules to fix display with Raghindi (devanagari) font
  (hinting must be disabled, and antialias disabled at small sizes)

* Wed Jul  9 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.2.1-1mdk
- Release 2.2.1

* Wed May 14 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.2.0-3mdk
- added various indic fonts to sans/serif/mono aliases
- added special rules to fix display with Raghindi (devanagari) font
  (hinting must be disabled, and antialias disabled at small sizes) 

* Mon May 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.2.0-2mdk
- Rebuild to get the new devel dependencies

* Tue Apr 22 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.2.0-1mdk
- Release 2.2.0
- Make sure all X11 fonts are in default configuration.

* Thu Apr 17 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1.94-1mdk
- Release 2.1.94
- Regenerate patches 3, 7
- Remove patches 4, 9, 10, 11, 12, 13, 14 (merged upstream)

* Tue Mar 11 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1-9mdk
- Update patch 4 with FcConfigEnableHome backport

* Wed Mar 05 2003 Pablo Saratxaga <pablo@mandrakesoft.com> - 2.1-8mdk
- Changed default Tamil fonts; added "Code2000" at the end of
  aliases for "Sans".

* Thu Feb 27 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1-7mdk
- Merge patch 8 in patch 7 : patches should not patch patched portion of files...
- Keith Packard is my hero : 
 - Patch14 (CVS): fix matching code (Mdk bug 812)

* Tue Feb 25 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.1-6mdk
- Patch9 (CVS): don't try to run fc-cache in dir without write access (CVS)
- Patch10 (CVS): Dont cache directorys until they've been scanned,avoids 
losing subdir contents, track dirs containing fonts.cache files referenced 
from ~/.fonts.cache file 
- Patch11 (CVS): fix crash in subpixel config load
- Patch12 (CVS): fix UTF-16 conversion
- Patch13 (CVS): speedup FcStrCmpIgnoreCase
- Update patch4 to first use $HOME and fallback using getpwuid

* Wed Jan 15 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.1-5mdk
- improved the default fontset aliases so it matches previous Xft1 setting

* Mon Jan 13 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1-4mdk
- Patch5 (rawhide): blacklist certain fonts freetype can't handle
- Patch6 (rawhide): support for slighthint is back
- Patch7 (rawhide): change order of default fonts 

* Wed Jan  8 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1-3mdk
- Update patch4 to fallback to $HOME if not info is available with getpwuid

* Fri Jan  3 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1-2mdk
- Patch4: don't use HOME variable to get homedir

* Thu Nov 28 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.1-1mdk
- Release 2.1
- Remove patch2 (merged upstream)

* Tue Nov 19 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-5mdk
- Remove patches 0 & 1 (no longer needed with freetype2 2.1.3)
- Patch2: don't add build date in configuration file

* Wed Nov 6 2002 Stefan van der Eijk <stefan@eijk.nu> 2.0-4mdk
- BuildRequires: ed

* Wed Nov  6 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-3mdk
- Ensure main package is required by library package

* Mon Nov  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-2mdk
- Fix dependencies

* Mon Nov  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 2.0-1mdk
- Initial Mdk package (based on rawhide)
