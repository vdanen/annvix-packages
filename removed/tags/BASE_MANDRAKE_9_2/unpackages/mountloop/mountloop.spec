Summary: Allow users to mount files via loopback
Name: mountloop
Version: 0.10
Release: 1mdk
URL: http://www.mandrakelinux.com/
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: System/Base
Requires: ssh-askpass, drakxtools, perl-MDK-Common, mount >= 2.11r-2mdk
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: XFree86-devel
Prefix: %{_prefix}

%description
Allow users to mount encrypted loopback filesystems.

%prep
%setup

%build
%make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
mkdir -p $RPM_BUILD_ROOT/%_menudir
cat > $RPM_BUILD_ROOT/%_menudir/%name << EOF
?package(%name): needs=x11 section=Applications/Archiving/Other longtitle="Create encrypted folder" title=DrakLoop command=drakloop icon="%name.png"
EOF
mkdir -p $RPM_BUILD_ROOT%_iconsdir $RPM_BUILD_ROOT%_miconsdir $RPM_BUILD_ROOT%_liconsdir
install -m 644 mountloop-20.png $RPM_BUILD_ROOT%_iconsdir/%name.png
install -m 644 mountloop-32.png $RPM_BUILD_ROOT%_miconsdir/%name.png
install -m 644 mountloop-48.png $RPM_BUILD_ROOT%_liconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog AUTHORS
%attr(4755,root,root) %{_bindir}/encsetup
%attr(4755,root,root) %{_bindir}/mountloop
%attr(4755,root,root) %{_bindir}/umountloop
%{_bindir}/drakloop
%config(noreplace) /etc/X11/xinit.d/*
/usr/X11R6/bin/*
%_menudir/*
%_iconsdir/%name.png
%_miconsdir/%name.png
%_liconsdir/%name.png

%post

%update_menus

%postun

%clean_menus

%changelog
* Fri Jun 13 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.10-1mdk
- allow to be run from the command line when not under X.

* Thu Apr 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.1-1mdk
- make it lib64 aware

* Wed Mar  5 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9-1mdk
- make it works (thx to gc)

* Sat Dec 28 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.8-1mdk
- corrected unmount problem

* Tue Aug 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.7-3mdk
- install icons

* Tue Aug 27 2002 David BAUDENS <baudens@mandrakesoft.com> 0.7-2mdk
- Fix icon (menu)

* Mon Jul  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.7-1mdk
- various changed by Pixel
- don't use strtok anymore to allow spaces in names

* Wed Jun 19 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6-1mdk
- encsetup: change owner of the loop device before mkfs

* Thu Jun 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.5-1mdk
- graphically report errors

* Wed Jun 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.4-1mdk
- added a small GUI to create encrypted folders (drakloop)

* Mon Jun 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.3-1mdk
- simplified the mount of non crypted filesystem by using the none
encryption type instead of parsing arguments.

* Sun Jun  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.2-1mdk
- added an X11 wrapper to mount the dirs

* Wed Jun  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.1-1mdk
- first version

# end of file
