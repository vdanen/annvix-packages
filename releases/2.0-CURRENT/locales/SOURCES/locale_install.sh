#!/bin/bash

# this script is to be called when a locale is installed for first time;
# it gets the locale name(s) as parameter, and does the needed steps
# so that the new locale can be used by the system

# source the default locale info
if [ -r /etc/sysconfig/i18n ]; then
. /etc/sysconfig/i18n
fi

# what is the default system locale?
unset BOOT_LOCALE
SHORT_BOOT_LOCALE="`echo ${LANGUAGE} | cut -d: -f1 | cut -d'@' -f1`"
[ -z "$BOOT_LOCALE" ] && BOOT_LOCALE="${GP_LANG}"
[ -z "$BOOT_LOCALE" ] && BOOT_LOCALE="${LC_ALL}"
[ -z "$BOOT_LOCALE" ] && BOOT_LOCALE="${LC_MESSAGES}"
[ -z "$BOOT_LOCALE" ] && BOOT_LOCALE="`echo ${LANGUAGE} | cut -d: -f1`"
[ -z "$BOOT_LOCALE" ] && BOOT_LOCALE="${LANG}"
[ -z "$BOOT_LOCALE" ] && BOOT_LOCALE="UTF-8"
[ -z "$SHORT_BOOT_LOCALE" ] && SHORT_BOOT_LOCALE="en"

# we only keep "language_country" for some special cases;
# for everything else we keep only language
case "$SHORT_BOOT_LOCALE" in
	pt_BR) ;;
	zh_CN|zh_SG) SHORT_BOOT_LOCALE="zh_CN" ;;
	zh_TW|zh_HK) SHORT_BOOT_LOCALE="zh_TW" ;;
	az_IR|ku_IQ) ;;
	*) SHORT_BOOT_LOCALE="`echo $SHORT_BOOT_LOCALE | cut -d'_' -f1`" ;;	
esac

# the list of languages that rpm installs their translations
if [ -r /etc/rpm/macros ]; then
RPM_INSTALL_LANG="`grep '^%_install_langs' /etc/rpm/macros | cut -d' ' -f2-`"
fi
[ -z "$RPM_INSTALL_LANG" ] && RPM_INSTALL_LANG=C
OLD_RPM_INSTALL_LANG="$RPM_INSTALL_LANG"

for i in "$@"
do
  if [ "$i" = "$SHORT_BOOT_LOCALE" ]
  then	
    # copy the LC_* of the defautl system locale to /etc/locale, so
    # erverything is ok on boot time, even if /usr is not mounted
    if [ -r "/usr/share/locale/$BOOT_LOCALE/LC_CTYPE" ]
    then
	    mkdir -p "/etc/locale/$BOOT_LOCALE/LC_MESSAGES"
	    for j in \
		LC_ADDRESS  LC_IDENTIFICATION  LC_MONETARY  LC_PAPER \
		LC_COLLATE  LC_MEASUREMENT     LC_NAME      LC_TELEPHONE \
		LC_CTYPE    LC_NUMERIC         LC_TIME \
		LC_MESSAGES/SYS_LC_MESSAGES
	    do
		    cp -fp "/usr/share/locale/$BOOT_LOCALE/$j" \
		    	"/etc/locale/$BOOT_LOCALE/$j"
	    done
    fi
  fi

  # make the installed locale known to rpm (so translations in that
  # language are installed), and the menu system
  if [ "$RPM_INSTALL_LANG" != "all" -a "$i" != "UTF-8" ]
  then
	  RPM_INSTALL_LANG=`perl -e 'print join(":",grep { ! $seen{$_} ++ } sort(split(/:/,$ARGV[0])))' "$i:$RPM_INSTALL_LANG"`
  fi
done

if [ "$OLD_RPM_INSTALL_LANG" != "$RPM_INSTALL_LANG" ]
then
  # update /etc/menu-methods/lang.h file
  if [ -w /etc/menu-methods/lang.h ]; then
  perl -pe "s/^function languages\(\)=.*/function languages()=\"${RPM_INSTALL_LANG}\"/" \
	-i /etc/menu-methods/lang.h
  fi
  # update /etc/rpm/macros file
  if [ -w /etc/rpm/macros ]; then
  perl -pe "s/^%_install_langs .*/%_install_langs ${RPM_INSTALL_LANG}/" \
	-i /etc/rpm/macros
  fi
fi
