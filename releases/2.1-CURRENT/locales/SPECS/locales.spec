#
# spec file for package locales
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		locales
%define version		%{glibc_ver}
%define release		%_revrel

%define glibc_ver	2.5
%define glibc_epoch	6

# FIXME: please check on next build those we really need
#%define _unpackaged_files_terminate_build 0

# shorthands for the post scripts
%define loc_add		/usr/bin/locale_install.sh
%define loc_del		/usr/bin/locale_uninstall.sh

Summary:	Base files for localization
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Internationalization

# this file is used to circumvent limitations of glib in LC_COLLATE
# re-definition after copy "..." statement 
# glibc 2.2.4 solved a lot of problems; but there are still some ones
#
Source1:	iso14651_hack
# scripts to install/uninstall a locale
Source2:	locale_install.sh
Source3:	locale_uninstall.sh

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-i18ndata = %{glibc_epoch}:%{glibc_ver}

Requires:	glibc = %{glibc_epoch}:%{glibc_ver}
Requires:	basesystem
AutoReqProv:	no

%description
These are the base files for language localization.  You also need to
install the specific locales-?? for the language(s) you want.  Then the user
 need to set the LANG variable to their preferred language in their
~/.profile configuration file.


%package -n locales-en
Summary:	Base files for localization (English)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-en
These are the base files for English language localization.
Contains: en_CA en_DK en_GB en_IE en_US


%prep


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{_sourcedir}/locale_install.sh %{buildroot}%{loc_add}
install -m 0755 %{_sourcedir}/locale_uninstall.sh %{buildroot}%{loc_del}

#mv /usr/share/locale /usr/share/locale_bak
mkdir -p %{buildroot}/usr/share/locale
LOCALEDIR=%{buildroot}/usr/share/locale

rm -rf locales-%{version}
mkdir -p locales-%{version} ; cd locales-%{version}

cp %{_sourcedir}/iso14651_hack .
for i in `grep '^#LIST_LOCALES=' iso14651_hack | cut -d= -f2 | tr ':' ' '`
do
    cat iso14651_hack | sed "s/#hack-$i#//" > iso14651_$i
done
		
# making default charset pseudo-locales
for DEF_CHARSET in UTF-8 ISO-8859-1 ISO-8859-2 ISO-8859-3 ISO-8859-4 \
	 ISO-8859-5 ISO-8859-7 ISO-8859-9 \
	 ISO-8859-10 ISO-8859-13 ISO-8859-14 ISO-8859-15 KOI8-R KOI8-U CP1251 
do
	# find the charset definition
    if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET ]; then
    	if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET.gz ]; then
			cp %{_sourcedir}/$DEF_CHARSET .
			DEF_CHARSET=%{_sourcedir}/$DEF_CHARSET
		fi
	fi
	# don't use en_DK because of LC_NUMERIC
	localedef -c -f $DEF_CHARSET -i en_US $LOCALEDIR/`basename $DEF_CHARSET` || :
done


# languages which have several locales
#
for i in /usr/share/i18n/locales/en_??
do
	DEF_CHARSET="UTF-8"
	# for those languages we still keep a default charset different of UTF-8
	case "`basename $i`" in
		en_IN) DEF_CHARSET="UTF-8" ;;
		en_IE) DEF_CHARSET="ISO-8859-15" ;;
		en*) DEF_CHARSET="ISO-8859-1" ;;
	esac
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
	elif [ -r %{_sourcedir}/`basename $i` ]; then
		DEF_LOCALE_FILE="%{_sourcedir}/`basename $i`"
		cp %{_sourcedir}/`basename $i` .
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/`basename $i`"
		cp /usr/share/i18n/locales/`basename $i` .
	fi
	DEF_LOCALE=`basename $i`
	# if some locale returns a non 0 return code it isn't important
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE || :
	# for compatibility 
	[ "$DEF_CHARSET" = "ISO-8859-15" ] && \
	(localedef -c -f ISO-8859-1 -i $DEF_LOCALE_FILE $LOCALEDIR/${DEF_LOCALE}.ISO-8859-1 || : )
	[ "$DEF_CHARSET" != "UTF-8" ] && \
	(localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${DEF_LOCALE}.`basename ${DEF_CHARSET}` || : )
	localedef -c -f UTF-8 -i $DEF_LOCALE_FILE $LOCALEDIR/${DEF_LOCALE}.UTF-8 || :
done

# locales using ISO-8859-15 that are not for the default locale of their
# respectives languages
for i in en_IE
do
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
    elif [ -r %{_sourcedir}/`basename $i` ]; then
		DEF_LOCALE_FILE="%{_sourcedir}/`basename $i`"
		cp %{_sourcedir}/`basename $i` .
    else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/`basename $i`"
    fi
	DEF_LANG=`basename $i | cut -d'_' -f1 `
	DEF_LOCALE=`basename $i`
	DEF_CHARSET=ISO-8859-15
	
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE || :
	# for compatibility 
	localedef -c -f ISO-8859-1 -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-1 || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-15 || :
done

# create the default locales for languages whith multiple locales
localedef -c -f ISO-8859-1  -i en_US $LOCALEDIR/en


# replace all identique files with hard links.
# script from Alastair McKinstry, 2000-07-03
cat > hardlink.pl << EOF
#!/usr/bin/perl
@files = \`find \$ARGV[0] -type f -a -not -name "LC_C*" \`;

foreach \$fi (@files) {
    chop (\$fi);
    (\$sum,\$name) = split(/ /,\`md5sum -b  \$fi\`);
    if (  \$orig{\$sum} eq "" ) {
        \$orig{\$sum} =\$fi;
    } else {
        \`ln -f \$orig{\$sum} \$fi\`;
    }
}
EOF

chmod a+x hardlink.pl
./hardlink.pl %{buildroot}/usr/share/locale

# make LC_CTYPE and LC_COLLATE symlinks
cat > softlink.pl << EOF
#!/usr/bin/perl
@files = \`find [A-Z]* \$ARGV[0]* -type f -a -name "LC_C*" \`;

foreach \$fi (@files) {
    chop (\$fi);
    (\$sum,\$name) = split(/ /,\`md5sum -b  \$fi\`);
    if (  \$orig{\$sum} eq "" ) {
        \$orig{\$sum} =\$fi;
    } else {
        \`rm \$fi\`;
	\`ln -s ../\$orig{\$sum} \$fi\`;
    }
}
EOF

chmod a+x softlink.pl
(cd %{buildroot}/usr/share/locale; LC_ALL=C %{_builddir}/locales-%{version}/softlink.pl en)

cd ..


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
# avoid symlink problems when updating
rm /usr/share/locale/*@euro > /dev/null 2> /dev/null || :


%post
if [ "$1" = "1" ]; then
	%{loc_add} "UTF-8"
fi


%preun
if [ "$1" = "0" ]; then
	%{loc_del} "UTF-8"
fi


%post -n locales-en
if [ "$1" = "1" ]; then
	%{loc_add} en en_GB en_IE en_US
fi


%postun -n locales-en
if [ "$1" = "0" ]; then
	%{loc_del} en en_GB en_IE en_US
fi


%files
%defattr(-,root,root)
%dir /usr/share/locale
/usr/share/locale/ISO*
/usr/share/locale/CP*
/usr/share/locale/UTF*
/usr/share/locale/KOI*
/usr/bin/*


%files -n locales-en
%defattr(-,root,root)
/usr/share/locale/en*


%changelog
* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- drop the prereq
- clean the spec

* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5
- 2.5

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- remove all locale files except english
- spec cleanups

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.6
- 2.3.6
- requires: basesystem (for grep, perl, etc.)
- updated locale_install/uninstall scripts from Mandriva

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.5-1avx
- rebuild for glibc 2.3.5
- drop all icons
- drop all non-english summaries and descriptions
- remove the handling of special gtk exceptions
- merge changes from mdk 2.3.5-1mdk:
  - use %%preun instead of %%postun --> otherwise /usr/bin/locale_uninstall.sh 
    has already been removed
  - fix of LC_COLLATE for ar_SA
  - fixed locale_install script so it works when first value of
    LANGUAGE variable is of the form "xx_YY" instead of "xx"
  - fixed vietnamese locale (mainly LC_COLLATE)
  - removed some experimental ethiopic locales that violate ISO-639
  - fixed yesexpr/noexpr for ar_SA, ar_TN and ar_YE locales
  - Added Frisian locales fy_DE, fy_NL
  - Added Inupiaq (ik_CA) locale 
  - added postinstall/postuninstall scripts to add/remove the support
    of the given languages when a new locale is added or removed from
    the system.
  - Added new locales: sc_IT (Sardinian), fur_IT (Furlan),
    tk_TM (Turkmen) 
  - corrected ar_SA, ar_TN and ar_YE locales
  - added ky_KG locale
  - added transliteration to armenian locale
  - added "no_NO" compatibility names for Norwegian Bokmål
  - changed default for Uzbek to cyrillic
  - small improvement in esperanto locale
  - corrected LC_TIME of Azeri locale
  - added limburguish and low saxon locales
  - changed serbian to default to UTF-8
  - big cleaning to match new glibc
  - added Nepali and Punjabi
  - added "nb" locale (copy of "no")
  - Added first Gujarati locale
  - updated Serbian locales

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-9avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.3.2-8avx
- Annvix build
- include epoch in BuildRequires

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 2.3.2-7sls
- minor spec cleanups
- remove icon

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 2.3.2-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
