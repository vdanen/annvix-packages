#!/bin/bash

# this script is to be called when a locale is removed from the sistem;
# so translations in the language(s) of the locale are no longer installed

# source the default locale info
. /etc/sysconfig/i18n

# the list of languages that rpm installs their translations
RPM_INSTALL_LANG="`grep '^%_install_langs' /etc/rpm/macros | cut -d' ' -f2-`"
[ -z "$RPM_INSTALL_LANG" ] && RPM_INSTALL_LANG=C
OLD_RPM_INSTALL_LANG="$RPM_INSTALL_LANG"

for i in "$@"
do
  # remove the locale from the list known to rpm (so translations in that
  # language are no more installed), and from the menu system
  if [ "$RPM_INSTALL_LANG" != "all" -a "$i" != "UTF-8" ]
  then
	  RPM_INSTALL_LANG=`perl -e 'print join(":",grep { $_ ne "$ARGV[1]" } sort(split(/:/,$ARGV[0])))' "$RPM_INSTALL_LANG" "$i"`
  fi
done

if [ "$OLD_RPM_INSTALL_LANG" != "$RPM_INSTALL_LANG" ]
then
  # update /etc/menu-methods/lang.h file
  perl -pe "s/^function languages\(\)=.*/function languages()=\"${RPM_INSTALL_LANG}\"/" \
	-i /etc/menu-methods/lang.h
  # update /etc/rpm/macros file
  perl -pe "s/^%_install_langs .*/%_install_langs ${RPM_INSTALL_LANG}/" \
	-i /etc/rpm/macros
fi
