%define name	chrpath
%define version	0.10
%define release	5sls

Summary: 	Dynamic library load path (rpath) alterer
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Other
URL:		http://www.tux.org/pub/X-Windows/ftp.hungry.com/chrpath/
Source:		%Url/%name-%version.tar.bz2
Patch0:		chrpath-0.10-elf64.patch.bz2

BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot

%description
Chrpath allows you to modify the dynamic library load path (rpath) of
compiled programs.  Currently, only removing and modifying the rpath
is supported.


%prep
%setup -q
%patch0 -p1 -b .elf64

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall 
rm -fr $RPM_BUILD_ROOT/usr/doc

%clean
rm -rf $RPM_BUILD_ROOT;

%files 
%defattr (-, root, root,755)
%doc AUTHORS ChangeLog COPYING NEWS README
%_bindir/chrpath
%_mandir/man1/chrpath.1*

%changelog
* Mon Dec 13 2003 Vincent Danen <vdanen@opensls.org> 0.10-5sls
- OpenSLS build
- tidy spec

* Thu Sep  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.10-4mdk
- Patch0: ELF64 support from Debian though it's still preferable to
  teach faulty packages adequately.

* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.10-3mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.10-2mdk
- build release

* Wed Dec 04 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.10-1mdk
- new release

* Fri Nov 15 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9-2mdk
- fix build for new rpm

* Wed Oct 30 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9-1mdk
- new release

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.8-2mdk
- fix description (Yura Gusev)

* Thu Oct 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.8-1mdk
- new release

* Fri Jul 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.6-1mdk
- new release (add man page)

* Thu Mar 21 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5-1mdk
- initial release
