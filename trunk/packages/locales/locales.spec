#
#
#
%define glibc_ver 2.3.2
%define version   %{glibc_ver}
%define release   5mdk
# FIXME: please check on next build those we really need
#%define _unpackaged_files_terminate_build 0

# to define when building for PRC
#%define build_for_PRC 1

Summary: Base files for localization
Name: locales
Version: %{version}
Release: %{release}
License: GPL
Group: System/Internationalization

# this file is used to circumvent limitations of glib in LC_COLLATE
# re-definition after copy "..." statement 
# glibc 2.2.4 solved a lot of problems; but there are still some ones
#
Source1: iso14651_hack

# this one is on glibc, however there is the politic issue
# of the naming of Taiwan 
Source10: zh_TW_2

# locales data
Source11: ku_TR
Source12: eo_XX
Source13: kn_IN
Source14: iu_CA
Source16: kh_KH
Source17: ph_PH
Source18: pd_CA
Source19: pd_US
Source20: pd_DE
Source21: pp_AN
Source22: as_IN

# Those exist in glibc >= 2.3.2 but the attached ones
# are more correct/more complete

# reordering still doesn't work in glibc 2.3
Source30: hy_AM
# various spelling fixes
Source31: yi_US
# int_curr_symbol missing
Source33: bn_BD
# changed date format strings
Source34: zh_CN

# rewritten to take profit of new glibc reordering possibilities
Source41: es_ES
Source42: es@tradicional
# LC_COLLATE has one line wrong
Source43: bs_BA
# glibc has sr_YU for latin, sr_YU@cyrillic for cyrillic;
# we use (following Gnome Serbian translators) sr_YU for cyrillic
# and sr_YU@Latn (and sh_YU) for latin
Source44: sr_YU
Source45: sh_YU
# corrected LC_COLLATE
Source46: sq_AL
# LC_COLLATE for vietnamese is incorrect in glibc, and LC_CTIME seems
# wrong too... 
Source47: vi_VN
# fixes in month names
Source48: uz_UZ
# cyrillic version
Source49: uz_UZ@Cyrl
# fixes in weekday names
Source50: wa_BE
# tr_TR from glibc has errors in LC_COLLATE
# also, I added recognition of Yy and Nn in yes/noexpr
Source51: tr_TR
# changed to use tcomma/scomma instead tcedilla/scedilla
Source52: ro_RO
# ours has yesexpr/noexpr
Source53: tg_TJ
Source54: az_AZ
# ethiopic locales
Source55: ad_ET
Source56: gez_ER
Source57: gez_ET
Source58: qo_ET
Source59: sx_ET
Source60: sz_ET
Source61: tig_ER
# those ones are in glib but glibc 2.3.2 fails to compile its LC_COLLATE;
Source62: am_ET
Source63: collate_et

# charset definitions
Source71: CP1133
Source72: MULELAO-1
Source76: CP154
# todo: width field
Source81: ISO-8859-9E
Source82: TATAR-CYR
Source85: KOI8-K

# it is arch dependen in fact
#BuildArchitectures: noarch
# to build this package glibc = %{glibc_ver} is needed (for locales definitions)
Prereq: glibc = 6:%{glibc_ver}
# no need to check for dependencies when building, there is no executables here
AutoReqProv: no
BuildRoot: %{_tmppath}/locales-root
Icon: bulle-blank.xpm
# locales are very dependent on glibc version
Requires: glibc = 6:%{glibc_ver}
# glibc >= 2.2.5-6mdk now comes with glibc-i18ndata package
BuildRequires: glibc-i18ndata = %{glibc_ver}

%description
These are the base files for language localization.
You also need to install the specific locales-?? for the
language(s) you want. Then the user need to set the
LANG variable to their preferred language in their
~/.profile configuration file.

%prep

%build
rm -rf $RPM_BUILD_ROOT

#mv /usr/share/locale /usr/share/locale_bak
mkdir -p $RPM_BUILD_ROOT/usr/share/locale
LOCALEDIR=$RPM_BUILD_ROOT/usr/share/locale

rm -rf locales-%{version}
mkdir -p locales-%{version} ; cd locales-%{version}

cp $RPM_SOURCE_DIR/iso14651_hack .
for i in `grep '^#LIST_LOCALES=' iso14651_hack | cut -d= -f2 | tr ':' ' '`
do
	cat iso14651_hack | sed "s/#hack-$i#//" > iso14651_$i
done
		
# copy various unhabitual charsets and other stuff
for DEF_CHARSET in \
	KOI8-K TATAR-CYR \
	ro_RO collate_et es@tradicional
do
	cp $RPM_SOURCE_DIR/$DEF_CHARSET .
done

# special handling for PRC
%if %build_for_PRC
	cp $RPM_SOURCE_DIR/zh_TW_2 zh_TW
%endif


# special handling for ethiopic locales (to circumvent glibc 2.2.4 problem)
# 
cp $RPM_SOURCE_DIR/??_ET $RPM_SOURCE_DIR/??_ER . || :
cp $RPM_SOURCE_DIR/???_ET $RPM_SOURCE_DIR/???_ER . || :
# this to avoid including the one from glibc
cp am_ET am_ET_hack
for i in ??_E[TR] ???_E[TR]
do
	cp $i A
	cat A | sed 's/copy "am_ET"/copy "am_ET_hack"/' > $i
done

# making default charset pseudo-locales
for DEF_CHARSET in UTF-8 ISO-8859-1 ISO-8859-2 ISO-8859-3 ISO-8859-4 \
	 ISO-8859-5 ISO-8859-7 ISO-8859-9 \
	 ISO-8859-10 ISO-8859-13 ISO-8859-14 ISO-8859-15 KOI8-R KOI8-U CP1251 
do
	# find the charset definition
    if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET ]; then
    	if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET.gz ]; then
			cp $RPM_SOURCE_DIR/$DEF_CHARSET .
			DEF_CHARSET=$RPM_SOURCE_DIR/$DEF_CHARSET
		fi
	fi
	# don't use en_DK because of LC_NUMERIC
	localedef -c -f $DEF_CHARSET -i en_US $LOCALEDIR/`basename $DEF_CHARSET` || :
done


# languages which have only one locale; use the language name as locale
# name for them; that makes the localization far easier
# kh_KH to add later
#
for i in \
	 ad_ET af_ZA am_ET as_IN az_AZ be_BY bg_BG bn_BD bn_IN br_FR bs_BA \
	 ca_ES cs_CZ cy_GB da_DK el_GR eo_XX et_EE eu_ES fa_IR fi_FI \
	 fo_FO ga_IE gd_GB gl_ES gv_GB gez_ER gez_ET he_IL hi_IN hr_HR \
	 hu_HU hy_AM id_ID is_IS iu_CA ja_JP ka_GE kl_GL kn_IN ko_KR ku_TR \
	 kw_GB lo_LA lt_LT lv_LV mi_NZ mk_MK ml_IN mn_MN mr_IN ms_MY mt_MT \
	 nn_NO no_NO \
	 oc_FR ph_PH pl_PL pp_AN qo_ET ro_RO se_NO sk_SK sl_SI sh_YU sq_AL \
	 sr_YU st_ZA sx_ET sz_ET ta_IN te_IN tg_TJ th_TH ti_ER ti_ET tl_PH \
	 tr_TR tt_RU tig_ER uk_UA ur_PK uz_UZ vi_VN wa_BE xh_ZA yi_US zh_CN \
	 zh_HK zh_SG zh_TW zu_ZA
do
	LOCALENAME=$i
	if [ -r ./$i ]; then
		DEF_LOCALE_FILE="./$i"
	elif [ -r $RPM_SOURCE_DIR/$i ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/$i"
		cp $RPM_SOURCE_DIR/$i .
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/$i"
	fi
	DEF_CHARSET="UTF-8"
	# for those languages we still keep a default charset different of UTF-8
	case "$i" in
		af*|en*|es*) DEF_CHARSET="ISO-8859-1" ;;
		bs*|cs*|hr*|hu*|pl*|ro*|sk*|sl*|sh*) DEF_CHARSET="ISO-8859-2" ;;
		sr*) DEF_CHARSET="ISO-8859-5" ;;
		el*) DEF_CHARSET="ISO-8859-7" ;;
		tr*) DEF_CHARSET="ISO-8859-9" ;;
		lt*|lv*) DEF_CHARSET="ISO-8859-13" ;;
		br*|ca*|da*|de*|et*|eu*|fi*|fo*|fr*|ga*|gl*) DEF_CHARSET="ISO-8859-15";;
		is*|it*|nl*|nn*|no*|nb*|oc*|pt*|sq*|sv*|wa*) DEF_CHARSET="ISO-8859-15";;
		be*|bg*) DEF_CHARSET="CP1251" ;;
		ru*) DEF_CHARSET="KOI8-R" ;;
		uk*) DEF_CHARSET="KOI8-U" ;;
		ja*) DEF_CHARSET="EUC-JP" ;;
		ko*) DEF_CHARSET="EUC-KR" ;;
		th*) DEF_CHARSET="TIS-620" ;;
		zh_CN|zh_SG) DEF_CHARSET="GB2312" ;;
		zh_TW|zh_TW) DEF_CHARSET="BIG5" ;;
	esac
	DEF_LOCALE=`basename $i`
	DEF_LANG=`echo $DEF_LOCALE | cut -d'_' -f1`
	# find the charset definition
    if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET ]; then
    	if [ ! -r /usr/share/i18n/charmaps/$DEF_CHARSET.gz ]; then
			cp $RPM_SOURCE_DIR/$DEF_CHARSET .
			DEF_CHARSET=$RPM_SOURCE_DIR/$DEF_CHARSET
		fi
	fi
	# if some locale returns a non 0 return code it isn't important
	[ "$DEF_LANG" != "${LOCALENAME}" ] && \
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LANG  || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME} || :
	[ "$DEF_CHARSET" != "BIG5" -a "$DEF_CHARSET" != "UTF-8" ] && \
	(localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME}.`basename ${DEF_CHARSET}` || : )
	localedef -c -f UTF-8 -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME}.UTF-8 || :
done

# fix for Arabic yes/no expr
for i in /usr/share/i18n/locales/ar_??
do
	if [ ! -r ./`basename $i` ]; then
		cat $i | \
		sed 's/^\(yesexpr.*\)<U0646>/\1<U0646><U0079><U0059>/' | \
		sed 's/^\(noexpr.*\)<U0644>/\1<U0644><U006E><U004E>/' > \
		./`basename $i`
	fi
done

# languages which have several locales
#for i in $RPM_SOURCE_DIR/pd_?? 
for i in \
	 /usr/share/i18n/locales/ar_?? /usr/share/i18n/locales/de_?? \
	 /usr/share/i18n/locales/en_?? /usr/share/i18n/locales/es_?? \
	 /usr/share/i18n/locales/fr_?? /usr/share/i18n/locales/it_?? \
	 /usr/share/i18n/locales/nl_?? /usr/share/i18n/locales/pt_?? \
	 /usr/share/i18n/locales/ru_?? /usr/share/i18n/locales/sv_?? 
do
	DEF_CHARSET="UTF-8"
	# for those languages we still keep a default charset different of UTF-8
	case "`basename $i`" in
		en_IN) DEF_CHARSET="UTF-8" ;;
		en_IE|es_ES) DEF_CHARSET="ISO-8859-15" ;;
		af*|en*|es*) DEF_CHARSET="ISO-8859-1" ;;
		bs*|cs*|hr*|hu*|pl*|ro*|sk*|sl*|sh*) DEF_CHARSET="ISO-8859-2" ;;
		sr*) DEF_CHARSET="ISO-8859-5" ;;
		el*) DEF_CHARSET="ISO-8859-7" ;;
		tr*) DEF_CHARSET="ISO-8859-9" ;;
		lt*|lv*) DEF_CHARSET="ISO-8859-13" ;;
		br*|ca*|da*|de*|et*|eu*|fi*|fo*|fr*|ga*|gl*) DEF_CHARSET="ISO-8859-15";;
		is*|it*|nl*|nn*|no*|nb*|oc*|pt*|sq*|sv*|wa*) DEF_CHARSET="ISO-8859-15";;
		be*|bg*) DEF_CHARSET="CP1251" ;;
		ru*) DEF_CHARSET="KOI8-R" ;;
		uk*) DEF_CHARSET="KOI8-U" ;;
		ja*) DEF_CHARSET="EUC-JP" ;;
		ko*) DEF_CHARSET="EUC-KR" ;;
		ta*) DEF_CHARSET="TSCII" ;;
		th*) DEF_CHARSET="TIS-620" ;;
		zh_CN|zh_SG) DEF_CHARSET="GB2312" ;;
		zh_TW|zh_TW) DEF_CHARSET="BIG5" ;;
	esac
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
	elif [ -r $RPM_SOURCE_DIR/`basename $i` ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/`basename $i`"
		cp $RPM_SOURCE_DIR/`basename $i` .
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/`basename $i`"
		cp /usr/share/i18n/locales/`basename $i` .
	fi
	DEF_LOCALE=`basename $i`
	DEF_LANG=`echo $DEF_LOCALE | cut -d'_' -f1`
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
for i in de_AT de_BE de_LU en_IE fi_FI fr_BE fr_LU nl_BE sv_FI
do
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
    elif [ -r $RPM_SOURCE_DIR/`basename $i` ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/`basename $i`"
		cp $RPM_SOURCE_DIR/`basename $i` .
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

# locales using iso-8859-15 which are the default ones for their respective
# languages
for i in br_FR ca_ES da_DK de_DE es_ES eu_ES fi_FI fr_FR ga_IE \
	 gl_ES is_IS it_IT nl_NL pt_PT wa_BE
do
	if [ -r ./`basename $i` ]; then
		DEF_LOCALE_FILE="./`basename $i`"
    elif [ -r $RPM_SOURCE_DIR/`basename $i` ]; then
		DEF_LOCALE_FILE="$RPM_SOURCE_DIR/`basename $i`"
		cp $RPM_SOURCE_DIR/`basename $i` .
	else
		DEF_LOCALE_FILE="/usr/share/i18n/locales/`basename $i`"
	fi
	DEF_LANG=`basename $i | cut -d'_' -f1 `
	DEF_LOCALE=`basename $i`
	DEF_CHARSET=ISO-8859-15
		
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LANG || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE || :
	# for compatibility 
	localedef -c -f ISO-8859-1   -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-1 || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LOCALE.ISO-8859-15 || :
done

# create the default locales for languages whith multiple locales
localedef -c -f UTF-8       -i ./ar_EG $LOCALEDIR/ar || :
localedef -c -f ISO-8859-1  -i en_US $LOCALEDIR/en
localedef -c -f KOI8-R      -i ru_RU $LOCALEDIR/ru
localedef -c -f ISO-8859-15 -i sv_SE $LOCALEDIR/sv
#localedef -c -f ISO-8859-1  -i $RPM_SOURCE_DIR/pd_US $LOCALEDIR/pd || :
localedef -c -f ISO-8859-15 -i ./es@tradicional $LOCALEDIR/es@tradicional || :

# special case for romanian
localedef -c -f ISO-8859-2  -i ./ro_RO $LOCALEDIR/ro_RO.ISO-8859-2
localedef -c -f ISO-8859-16 -i ./ro_RO $LOCALEDIR/ro_RO.ISO-8859-16
localedef -c -f UTF-8 -i       ./ro_RO $LOCALEDIR/ro_RO.UTF-8
# default, using latin2 for compatibility
localedef -c -f ISO-8859-2 -i  ./ro_RO $LOCALEDIR/ro_RO
localedef -c -f ISO-8859-2 -i  ./ro_RO $LOCALEDIR/ro

# Russian uses koi8-r by default, iso-8859-5 is a second choice
# "ru_RU" locale set to ISO-8859-5 for compatibility reasons
localedef -c -f KOI8-R     -i ru_RU $LOCALEDIR/ru_RU || :
localedef -c -f KOI8-R     -i ru_RU $LOCALEDIR/ru_RU.KOI8-R || :
localedef -c -f ISO-8859-5 -i ru_RU $LOCALEDIR/ru_RU.ISO-8859-5 || :
localedef -c -f CP1251     -i ru_RU $LOCALEDIR/ru_RU.CP1251 || :
# Russian in Ukrainia can use koi8-u
localedef -c -f KOI8-R     -i ru_UA $LOCALEDIR/ru_UA.KOI8-R || :
localedef -c -f KOI8-U     -i ru_UA $LOCALEDIR/ru_UA.KOI8-U || :
localedef -c -f ISO-8859-5 -i ru_UA $LOCALEDIR/ru_UA.ISO-8859-5 || :
localedef -c -f CP1251     -i ru_UA $LOCALEDIR/ru_UA.CP1251 || :
# Provide cp1251 for Ukrainian too...
localedef -c -f CP1251     -i uk_UA $LOCALEDIR/uk_UA.CP1251 || :
# Bielorussian
localedef -c -f CP1251     -i be_BY $LOCALEDIR/be || :
localedef -c -f CP1251     -i be_BY $LOCALEDIR/be_BY || :
localedef -c -f ISO-8859-5 -i be_BY $LOCALEDIR/be_BY.ISO-8859-5 || :

# estonian can use iso-8859-15 and iso-8859-4
localedef -c -f ISO-8859-15 -i et_EE $LOCALEDIR/et || :
localedef -c -f ISO-8859-15 -i et_EE $LOCALEDIR/et_EE || :
localedef -c -f ISO-8859-4  -i et_EE $LOCALEDIR/et_EE.ISO-8859-4 || :
localedef -c -f ISO-8859-13 -i et_EE $LOCALEDIR/et_EE.ISO-8859-13 || :

# Lithuanian
localedef -c -f ISO-8859-13 -i lt_LT $LOCALEDIR/lt || :
localedef -c -f ISO-8859-13 -i lt_LT $LOCALEDIR/lt_LT || :
localedef -c -f ISO-8859-4  -i lt_LT $LOCALEDIR/lt_LT.ISO-8859-4 || :
localedef -c -f ISO-8859-4  -i lt_LT $LOCALEDIR/lt_LT.ISO-8859-13 || :

# Latvian
localedef -c -f ISO-8859-13 -i lv_LV $LOCALEDIR/lv || :
localedef -c -f ISO-8859-13 -i lv_LV $LOCALEDIR/lv_LV || :
localedef -c -f ISO-8859-4  -i lv_LV $LOCALEDIR/lv_LV.ISO-8859-4 || :
localedef -c -f ISO-8859-13 -i lv_LV $LOCALEDIR/lv_LV.ISO-8859-13 || :

# Vietnamese -- for old compatibility
localedef -c -f VISCII     -i vi_VN $LOCALEDIR/vi_VN.VISCII || :
localedef -c -f TCVN5712-1 -i vi_VN $LOCALEDIR/vi_VN.TCVN || :
localedef -c -f TCVN5712-1 -i vi_VN $LOCALEDIR/vi_VN.TCVN-5712 || :

# georgian -- for old compatibility
localedef -c -f GEORGIAN-ACADEMY -i ka_GE $LOCALEDIR/ka_GE.GEORGIAN-ACADEMY || :
localedef -c -f GEORGIAN-PS      -i ka_GE $LOCALEDIR/ka_GE.GEORGIAN-PS || :

# Uzbek
localedef -c -f ISO-8859-1  -i uz_UZ $LOCALEDIR/uz_UZ.ISO-8859-1 || :
localedef -c -f ISO-8859-9  -i uz_UZ $LOCALEDIR/uz_UZ.ISO-8859-9 || :
cp $RPM_SOURCE_DIR/uz_UZ@Cyrl .
if [ -r "uz_UZ@Cyrl" ]; then
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz@Cyrl || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ@Cyrl || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ.UTF-8@Cyrl || :
fi

# Azeri -- for old compatibility
localedef -c -f ISO-8859-9E -i az_AZ $LOCALEDIR/az_AZ.ISO-8859-9E || :

# Kurdish 
localedef -c -f ISO-8859-9 -i ku_TR $LOCALEDIR/ku_TR.ISO-8859-9 || :

# Armenian -- for old compatibility
localedef -c -f ARMSCII-8 -i hy_AM $LOCALEDIR/hy_AM.ARMSCII-8 || :

# Esperanto
localedef -c -f ISO-8859-3 -i eo_XX $LOCALEDIR/eo_XX.ISO-8859-3 || :

# Maltese -- for old compatibility
localedef -c -f ISO-8859-3 -i mt_MT $LOCALEDIR/mt_MT.ISO-8859-3 || :

# Hebrew -- for old compatibility and for use with Wine
localedef -c -f ISO-8859-8 -i he_IL $LOCALEDIR/he_IL.ISO-8859-8 || :
localedef -c -f CP1255     -i he_IL $LOCALEDIR/he_IL.CP1255 || :

# for old compatibility
if [ -r "sr_YU" ]; then
localedef -c -f ISO-8859-5 -i ./sr_YU $LOCALEDIR/sp || :
localedef -c -f ISO-8859-5 -i ./sr_YU $LOCALEDIR/sp_YU || :
localedef -c -f ISO-8859-5 -i ./sr_YU $LOCALEDIR/sp_YU.ISO-8859-5 || :
localedef -c -f UTF-8      -i ./sr_YU $LOCALEDIR/sp_YU.UTF-8 || :
fi
if [ -r "sh_YU" ]; then
localedef -c -f ISO-8859-2 -i ./sh_YU $LOCALEDIR/sr@Latn || :
localedef -c -f ISO-8859-2 -i ./sh_YU $LOCALEDIR/sr_YU@Latn || :
localedef -c -f ISO-8859-2 -i ./sh_YU $LOCALEDIR/sr_YU.ISO-8859-2@Latn || :
localedef -c -f UTF-8      -i ./sh_YU $LOCALEDIR/sr_YU.UTF-8@Latn || :
fi

# en_BE is required for conformance to LI18NUX2000
for i in $LOCALEDIR/en_IE* ; do
	mkdir $LOCALEDIR/en_BE`basename $i | cut -b6- `
	cp -var $i/* $LOCALEDIR/en_BE`basename $i | cut -b6- `
	for j in LC_MONETARY LC_TELEPHONE LC_ADDRESS
	do
		cp -var $LOCALEDIR/nl_BE`basename $i | cut -b6- `/$j \
			$LOCALEDIR/en_BE`basename $i | cut -b6- `
	done
done

# Finnish default must be iso8859-15
localedef -c -f ISO-8859-1  -i fi_FI $LOCALEDIR/fi_FI.ISO-8859-1 || :

# celtic languages may want to use iso-8859-14
localedef -c -f ISO-8859-14 -i br_FR $LOCALEDIR/br_FR.ISO-8859-14 || :
localedef -c -f ISO-8859-14 -i cy_GB $LOCALEDIR/cy_GB.ISO-8859-14 || :
localedef -c -f ISO-8859-14 -i ga_IE $LOCALEDIR/ga_IE.ISO-8859-14 || :
localedef -c -f ISO-8859-1  -i gd_GB $LOCALEDIR/gd_GB.ISO-8859-1  || :
localedef -c -f ISO-8859-14 -i gd_GB $LOCALEDIR/gd_GB.ISO-8859-14 || :
localedef -c -f ISO-8859-1  -i gv_GB $LOCALEDIR/gv_GB.ISO-8859-1  || :
localedef -c -f ISO-8859-14 -i gv_GB $LOCALEDIR/gv_GB.ISO-8859-14 || :
localedef -c -f ISO-8859-1  -i kw_GB $LOCALEDIR/kw_GB.ISO-8859-1  || :
localedef -c -f ISO-8859-14 -i kw_GB $LOCALEDIR/kw_GB.ISO-8859-14 || :

# Albanian
localedef -c -f ISO-8859-1 -i sq_AL $LOCALEDIR/sq_AL.ISO-8859-1 || :
localedef -c -f ISO-8859-2 -i sq_AL $LOCALEDIR/sq_AL.ISO-8859-2 || :

# Chinese
localedef -c -f GB2312    -i zh_CN $LOCALEDIR/zh || :
localedef -c -f GB2312    -i zh_CN $LOCALEDIR/zh_CN || :
localedef -c -f GB2312    -i zh_CN $LOCALEDIR/zh_CN.GB2312 || :
localedef -c -f GBK       -i zh_CN $LOCALEDIR/zh_CN.GBK || :
localedef -c -f GB18030   -i zh_CN $LOCALEDIR/zh_CN.GB18030 || :
localedef -c -f BIG5HKSCS -i zh_HK $LOCALEDIR/zh_HK || :
localedef -c -f GB18030   -i zh_HK $LOCALEDIR/zh_HK.GB18030 || :
localedef -c -f BIG5      -i ./zh_TW $LOCALEDIR/zh_TW || :
localedef -c -f BIG5      -i ./zh_TW $LOCALEDIR/zh_TW.Big5 || :

# Tamil
#cp $RPM_SOURCE_DIR/*TSCII* .
localedef -c -f TSCII -i ta_IN $LOCALEDIR/ta_IN.TSCII || :
localedef -c -f TSCII -i ta_IN $LOCALEDIR/ta_IN.TSCII-0 || :

# special files needed for Gtk and tscii
mkdir -p $RPM_BUILD_ROOT/etc/gtk
cat << EOF > $RPM_BUILD_ROOT/etc/gtk/gtkrc.ta_IN
# Tamil in TSCII
#
# It requires tamil fonts to be installed; and fakes pseudo-iso-8859-1
style "gtk-default-ta" {
       font = "-*-TSC_Avarangal-medium-r-normal--*-120-100-100-p-*-tscii-0"
       fontset = "-*-helvetica-medium-r-normal--*-120-*-*-p-*-iso8859-1,\
       -*-TSC_Avarangal-medium-r-normal--*-120-100-100-p-*-tscii-0,\
       -altsys-TSC_Paranar-medium-r-normal--*-120-100-100-p-*-tscii-0,*-r-*"
}
class "GtkWidget" style "gtk-default-ta"
EOF
mkdir -p $RPM_BUILD_ROOT/etc/gtk-2.0
cat << EOF > $RPM_BUILD_ROOT/etc/gtk-2.0/gtkrc.ta_IN
# Tamil in TSCII
#
# This is no longuer *required*, and it hurts a bit, as it makes it
# impossible for the user to select a different default font/size
# through the GUI tools; but as there may still be several *.po
# files claiming to be latin1, it is better to keep it for smooth transition
style "gtk-default-ta" {
       font_name = "TSCu_Paranar 14"
	   }
class "GtkWidget" style "gtk-default-ta"
EOF

# aliases
for i in ja vi ; do
	case "$i" in
		ja) list="ja_JP.ujis" ;;
		*) list="" ;;
	esac

	for j in `echo $list` ;  do
		mkdir -p $LOCALEDIR/$j
		ln $LOCALEDIR/$i/LC_* $LOCALEDIR/$j || :
		mkdir $LOCALEDIR/$j/LC_MESSAGES
		ln $LOCALEDIR/$i/LC_MESSAGES/* $LOCALEDIR/$j/LC_MESSAGES || :
	done
done

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
./hardlink.pl $RPM_BUILD_ROOT/usr/share/locale

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
(
 cd $RPM_BUILD_ROOT/usr/share/locale ;
 # not built: pd
 for i in \
       af am ar az be bg bn br bs ca cs cy da de el en eo es et eu \
	fa fi fo fr ga gd gl gv    he hi hr hu hy id is it iu ja ka kl \
	ko kw lo lt lv mi mk mr ms mt nb nl nn no oc    ph pl pp pt    \
	ro ru sk sl    sq sr sv       ta te tg th ti    tr tt tig uk ur \
	uz vi wa yi zh \
	tl sp ad gez qo sx sz
 do
	LC_ALL=C $RPM_BUILD_DIR/locales-%{version}/softlink.pl $i
 done
)

cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir /usr/share/locale
/usr/share/locale/ISO*
/usr/share/locale/CP*
/usr/share/locale/UTF*
/usr/share/locale/KOI*

%pre
# avoid symlink problems when updating
rm /usr/share/locale/*@euro > /dev/null 2> /dev/null || :


####################################################################
# The various localization packages.
#
# add one for each new language that is included in the future
# TODO: someone to translate the Summary and descriptions ?
#       for the following languages: be, fo,
#	    kl, lo, sk, th, yi
# TODO: correct/complete languages lo
####################################################################

### af
# translation by Schalk Cronje <schalkc@ntaba.co.za>
%package -n locales-af
Summary: Base files for localization (Afrikaans)
Summary(af): Hierdie is die basislêers vir Afrikaanse lokalisasie
Group: System/Internationalization
Icon: bulle-af.xpm
URL: http://www.af.org.za/aflaai/linux-i18n/
Requires: locales = %{version}-%{release}

%description -n locales-af
These are the base files for Afrikaans language localization; you need
it to correctly display 8bits Afrikaans characters, and for proper
alfabetical sorting and representation of dates and numbers according
to Afrikaans language conventions.

%description -n locales-af -l af
Hierdie is die basislêers vir Afrikaanse lokalisasie. U benodig dit om die
Afrikaanse 8-bis karakters korrek te vertoon, vir korrekte alfabetiese
sorterting en ook om datums en getalle in die Afrikaanse standaardvorm te
vertoon.

%files -n locales-af
%defattr(-,root,root)
/usr/share/locale/af*

### am
# translation by Daniel Yacob <Yacob@EthiopiaOnline.Net>
%package -n locales-am
Summary: Base files for localization (Amharic)
Summary(am): ለlocalization (አማርኛ) መሰረት ፋይሎች
Group: System/Internationalization
Icon: bulle-am.xpm
URL: http://www.ethiopic.org/
Requires: locales = %{version}-%{release}
Provides: locales-ti, locales-gez, locales-tig
Provides: locales-ad, locales-qo, locales-sx, locales-sz

%description -n locales-am
These are the base files for Amharic language localization; you need
it to correctly display 8bits Amharic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Amharic language conventions.

%description -n locales-am -l am
እነዚህ ያማርኛ ቋንቋ localization  መሰረት ፋይሎች ናቸው።
ያማርኛ ፊደላትንለማየት፣ የፊደላት ቅደም ተከተልን ለመጠበቅ፣
ቀኖችንና ቍጥሮችንበቋንቋው ስርዓት ለማስቀመጥ ያስፈልጋሉ።

%files -n locales-am
%defattr(-,root,root)
/usr/share/locale/am*
# tigrinya
/usr/share/locale/ti
/usr/share/locale/ti_*
# ge'ez
/usr/share/locale/gez*
# tigre
/usr/share/locale/tig*
#
/usr/share/locale/ad*
/usr/share/locale/qo*
/usr/share/locale/sx*
/usr/share/locale/sz*

### ar
# translation by Wajdi Al-Jedaibi <wajdi@acm.org>
%package -n locales-ar
Summary: Base files for localization (Arabic)
Summary(ar): هذه هي الملفات اللازمة لإعتماد اللغة العربية في نظام لينكس.
Group: System/Internationalization
Icon: bulle-ar.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ar
These are the base files for Arabic language localization; you need
it to correctly display 8bits arabic characters, and for proper
alfabetical sorting and representation of dates and numbers according
to arabic language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%description -n locales-ar -l ar
هذه هي الملفات اللازمة لإعتماد اللغة العربية في نظام لينكس.
لاحظ أن هذا البرنامجلايقوم بعملية تحويل اتجاه الكتابة من اليمن إلى
اليسار والعكس, ولكن يوفر الاساسيات الضرورية لعرض وتصنيف وترتيب الاحرف
العربية, بما في ذلك إظهار التاريخ و غيره.

%files -n locales-ar
%defattr(-,root,root)
/usr/share/locale/ar*

### as
%package -n locales-as
Summary: Base files for localization (Assamese)
Group: System/Internationalization
Icon: bulle-as.xpm
Requires: locales = %{version}-%{release}

%description -n locales-as
These are the base files for Assamese language localization; you need
it to correctly display 8bits Assamese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Assamese language conventions.

%files -n locales-as
%defattr(-,root,root)
/usr/share/locale/as*

### az
%package -n locales-az
Summary: Base files for localization (Azeri)
Group: System/Internationalization
Icon: bulle-az.xpm
Requires: locales = %{version}-%{release}

%description -n locales-az
These are the base files for Azeri language localization; you need
it to correctly display 8bits Azeri characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Azeri language conventions.

%files -n locales-az
%defattr(-,root,root)
/usr/share/locale/az*

### be
%package -n locales-be
Summary: Base files for localization (Belarussian)
Group: System/Internationalization
Icon: bulle-be.xpm
Requires: locales = %{version}-%{release}

%description -n locales-be
These are the base files for Belarussian language localization; you need
it to correctly display 8bits Belarussian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Belarussian language conventions.

%files -n locales-be
%defattr(-,root,root)
/usr/share/locale/be*

### bg
# translation: Mariana Kokosharova <kokosharova@dir.bg>
%package -n locales-bg
Summary: Base files for localization (Bulgarian)
Summary(bg): съдържат основните регионални характеристики на българския език
Group: System/Internationalization
Icon: bulle-bg.xpm
Requires: locales = %{version}-%{release}

%description -n locales-bg
These are the base files for Bulgarian language localization; you need
it to correctly display 8bits Bulgarian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bulgarian language conventions.

%description -n locales-bg -l bg
Тези файлове съдържат основните регионални характеристики на българския език;
теса необходими за правилното представяне на 8 - битовите букви на кирилицата
на екрана, за правилната азбучна подредба и за представяне на датата и числата
в съответствие на правилата на българския език.

%files -n locales-bg
%defattr(-,root,root)
/usr/share/locale/bg*

### bn
%package -n locales-bn
Summary: Base files for localization (Bengali)
Group: System/Internationalization
Icon: bulle-bn.xpm
Requires: locales = %{version}-%{release}

%description -n locales-bn
These are the base files for Bengali language localization; you need
it to correctly display 8bits Bengali characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bengali language conventions.

%files -n locales-bn
%defattr(-,root,root)
/usr/share/locale/bn*

### br
# Translation by Jañ-Mai Drapier (jan-mai-drapier@mail.dotcom.fr)
%package -n locales-br
Summary: Base files for localization (Breton)
Group: System/Internationalization
Icon: bulle-br.xpm
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation en langue brétonne.
Summary(br): Kement-mañ a zo restroù diazez evit broelañ diouzh ar brezhoneg.

%description -n locales-br
These are the base files for Breton language localization; you need
it to correctly display 8bits Breton characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Breton language conventions.

%description -n locales-br -l fr
Ce paquet contient les définitions de locales en langue brétonne.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates et des nombres.

%description -n locales-br -l br
Kement-mañ a zo restroù diazez evit broelañ diouzh ar Vrezhoneg; ret eo
evit diskwel ent reizh arouezennoù breizhat 8bit, rummañ dre al
lizherenneg, taolennañ an deizadoù hag an niveroù hervez kendivizadoù ar
brezhoneg.

%files -n locales-br
%defattr(-,root,root)
/usr/share/locale/br*

### bs
%package -n locales-bs
Summary: Base files for localization (Bosnian)
Group: System/Internationalization
Icon: bulle-bs.xpm
Requires: locales = %{version}-%{release}

%description -n locales-bs
These are the base files for Bosnian language localization; you need
it to correctly display 8bits Bosnian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bosnian language conventions.

%files -n locales-bs
%defattr(-,root,root)
/usr/share/locale/bs*

### ca
%package -n locales-ca
Summary: Base files for localization (Catalan)
Group: System/Internationalization
Icon: bulle-ca.xpm
Requires: locales = %{version}-%{release}
Summary(ca): Arxius bàsics per a l'adaptació al català
Summary(es): Archivos de base para la localización en idioma catalán
Summary(fr): Fichiers de base pour la localisation en langue catalane

%description -n locales-ca
These are the base files for Catalan language localization; you need
it to correctly display 8bits Catalan characters, and for proper
representation of dates, numbers and alphabetical order according to
Catalan language conventions

%description -n locales-ca -l ca
Aquests són els arxius bàsics per a l'adaptació del sistema a les
peculiaritats de la llengua catalana; són necessaris perquè les
vocals accentuades, la ce trencada, etc. apareguin correctament, i
perquè les dates, els nombres i l'ordre alfabètic s'adaptin a les
convencions de la dita llengua.

%description -n locales-ca -l es
Este paquete incluye las definiciones de locales para el catalán.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del catalán, para el orden alfabético
y para la representación correcta de los números y fechas según
las convenciones del catalán.

%description -n locales-ca -l fr
Ce paquet contient les définitions de locales en langue catalane.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

%files -n locales-ca
%defattr(-,root,root)
/usr/share/locale/ca*

### cs
# translation by <pavel@SnowWhite.inet.cz>
%package -n locales-cs
Summary: Base files for localization (Czech)
Group: System/Internationalization
Icon: bulle-cs.xpm
Requires: locales = %{version}-%{release}
Summary(cs): Základní soubory pro lokalizaci (čeština)

%description -n locales-cs
These are the base files for Czech language localization; you need
it to correctly display 8bits Czech characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Czech language conventions.

%description -n locales-cs -l cs
Zde jsou soubory nutné pro správnou českou lokalizaci; potřebujete je
pro správné zobrazování českých 8bitových znaků a pro správné české
třídění a rprezentaci data a čísel podle českých konvencí.

%files -n locales-cs
%defattr(-,root,root)
/usr/share/locale/cs*

### cy
%package -n locales-cy
Summary: Base files for localization (Welsh)
Summary(cy): Dyma'r ffeiliau sylfaenol i'r lleoliaeth Cymraeg
Group: System/Internationalization
Icon: bulle-cy.xpm
Requires: locales = %{version}-%{release}

%description -n locales-cy
These are the base files for Welsh language localization; you need
it to correctly display 8bits Welsh characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Welsh language conventions.

%description -n locales-cy -l cy
Dyma'r ffeiliau sylfaenol i'r lleoliaeth Cymraeg; mae angen rhain er mwyn
dangos yn iawn y cymeriadau Cymraeg 8-bit, a threfniant y wyddor,
dyddiadau a rhifau yn ôl yr arfer Cymraeg.

%files -n locales-cy
%defattr(-,root,root)
/usr/share/locale/cy*

### da
# danish translation by Erik Martino <martino@daimi.au.dk>
%package -n locales-da
Summary: Base files for localization (Danish)
Summary(da): Her er de basale filer for dansk sprog tilpasning
Group: System/Internationalization
Icon: bulle-da.xpm
Requires: locales = %{version}-%{release}

%description -n locales-da
These are the base files for Danish language localization; you need
it to correctly display 8bits Danish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Danish language conventions.

%description -n locales-da -l da
Her er de basale filer for dansk sprog tilpasning. De er nødvendige for
at vise de danske 8bit tegn, sortere alfabetisk og repræsentere datoer
og tal korrekt ifølge dansk retskrivning.


%files -n locales-da
%defattr(-,root,root)
/usr/share/locale/da*

### de
%package -n locales-de
Summary: Base files for localization (German)
Group: System/Internationalization
Icon: bulle-de.xpm
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation en langue allemande
Summary(de): Basisdateien für die Lokalisierung (deutsch)

%description -n locales-de
These are the base files for German language localization; you need
it to correctly display 8bits German characters, and for proper
alphabetical sorting and representation of dates and numbers according
to German language conventions.

%description -n locales-de -l fr
Ce paquet contient les définitions de locales en langue allemande.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

%description -n locales-de -l de
Dies sind die Basisdateien für die deutsche Sprachanpassung; sie
werden für die korrekte Darstellung deutscher 8-Bit-Zeichen,
die deutsche Sortierreihenfolge sowie Datums- und Zahlendarstellung
benötigt.

%files -n locales-de
%defattr(-,root,root)
/usr/share/locale/de*

### el
# translations from "Theodore J. Soldatos" <theodore@eexi.gr>
%package -n locales-el
Summary: Base files for localization (Greek)
Group: System/Internationalization
Icon: bulle-el.xpm
Requires: locales = %{version}-%{release}
Obsoletes: locales-gr
Provides: locales-gr
Summary(el): Βασικά αρχεία τοπικών ρυθμίσεων (Ελληνικά)

%description -n locales-el
These are the base files for Greek language localization; you need
it to correctly display 8bits Greek characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Greek language conventions.

%description -n locales-el -l el
Αυτά είναι τα βασικά αρχεία για υποστήριξη ελληνικής γλώσσας. Τα χρειάζεστε
για τη σωστή απεικόνιση 8bit ελληνικών χαρακτήρων, καθώς και για την σωστή
ταξινόμηση και απεικόνιση ημερομηνιών και αριθμών σύμφωνα με τις συμβάσεις
της ελληνικής γλώσσας.

%files -n locales-el
%defattr(-,root,root)
/usr/share/locale/el*

### en
%package -n locales-en
Summary: Base files for localization (English)
Group: System/Internationalization
Icon: bulle-en.xpm
Requires: locales = %{version}-%{release}

%description -n locales-en
These are the base files for English language localization.
Contains: en_CA en_DK en_GB en_IE en_US

%files -n locales-en
%defattr(-,root,root)
/usr/share/locale/en*

### eo
# translation by diestel@rzaix340.rz.uni-leipzig.de (Wolfram Diestel)
%package -n locales-eo
Summary: Base files for localization (Esperanto)
Group: System/Internationalization
Icon: bulle-eo.xpm
Requires: locales = %{version}-%{release}
Summary(eo): Bazaj dosieroj por lokaĵo (Esperanto)

%description -n locales-eo
These are the base files for Esperanto language localization; you need
it to correctly display 8bits esperanto characters, and for proper
alphabetical sorting and representation of dates and numbers according
to esperanto language conventions.

%description -n locales-eo -l eo
Tiuj ĉi estas la bazaj dosieroj por la esperantlingva lokaĵo; vi bezonas
ilin por ĝuste vidi 8-bitajn Esperanto-signojn kaj por ĝusta
alfabeta ordo, datindikoj kaj nombroj konvene al la konvencioj
en esperanta medio.

%files -n locales-eo
%defattr(-,root,root)
/usr/share/locale/eo*

### es
%package -n locales-es
Summary: Base files for localization (Spanish)
Group: System/Internationalization
Icon: bulle-es.xpm
Requires: locales = %{version}-%{release}
Summary(es): Ficheros de base para la localización (castellano)

%description -n locales-es
These are the base files for Spanish language localization; you need
it to correctly display 8bits spanish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to spanish language conventions.

%description -n locales-es -l es
Este paquete incluye las definiciones de locales para el castellano.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del idioma español, para el orden alfabético 
y para la representación correcta de los números y fechas según 
las convenciones del castellano.

%files -n locales-es
%defattr(-,root,root)
/usr/share/locale/es*

### et
# translation from: Ekke Einberg <ekke@data.ee>
%package -n locales-et
Summary: Base files for localization (Estonian)
Summary(et): Siin on vajalikud failid Linuxi eestindamiseks.
Group: System/Internationalization
Icon: bulle-et.xpm
Requires: locales = %{version}-%{release}

%description -n locales-et
These are the base files for Estonian language localization; you need
it to correctly display 8bits Estonian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Estonian language conventions.

%description -n locales-et -l et
Siin on vajalikud failid Linuxi eestindamiseks. Need on vajalikud
8-bitiliste eesti sümbolite
korrektseks esitamiseks ning õige tähestikulise järjestuse jaoks. Samuti
numbrite ja kuupäevade
eesti keele reeglitele vastavaks esituseks.

%files -n locales-et
%defattr(-,root,root)
/usr/share/locale/et*

### eu
%package -n locales-eu
Summary: Base files for localization (Basque)
Group: System/Internationalization
Icon: bulle-eu.xpm
Requires: locales = %{version}-%{release}
Summary(eu): Euskarazko egokitzapenerako oinarrizko artxiboak
Summary(es): Archivos de base para la localización en euskara
Summary(fr): Fichiers de base pour la localisation en euskara (langue basque)

%description -n locales-eu
Linux-ek euskaraz badaki !
These are the base files for Basque language localization; you need
it to correctly display 8bits Basque characters, and for proper
representation of dates and numbers according to Basque language
conventions.

%description -n locales-eu -l eu
Linux-ek euskaraz badaki !
Hauek dira euskarazko egokitzapenerako oinarrizko artxiboak; euskarazko
8 biteko karaktereak zuzen ikusi ahal izateko zein zenbakiak
eta datak euskararen arauen arabera era egokian agertarazteko behar dira.

%description -n locales-eu -l es
Linux-ek euskaraz badaki !
Este paquete incluye las definiciones de locales para el euskara.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del euskara, para el orden alfabético
y para la representación correcta de los números y fechas según
las convenciones del euskara.

%description -n locales-eu -l fr
Ce paquet contient les définitions de locales en euskara batua.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

%files -n locales-eu
%defattr(-,root,root)
/usr/share/locale/eu*

### fa
%package -n locales-fa
Summary: Base files for localization (Farsi)
Summary(fa): پرونده‌های اساسی محلی‌سازی (فارسی)
Group: System/Internationalization
Icon: bulle-fa.xpm
Requires: locales = %{version}-%{release}

%description -n locales-fa
These are the base files for Farsi language localization; you need
it to correctly display 8bits Farsi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Farsi language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%description -n locales-fa -l fa
اینها پرونده‌های اساسی زبان فارسی می‌باشند؛ شما برای نمایش درست ۸ بیت حروف فارسی، ترتیب مناسب الفبا، معرفی تاریخ و اعداد بر اساس قواعد زبان فارسی به آنها احتیاج دارید. توجه داشته باشید که این پاکت تعویض نگارش از راست به چپ و از چپ به راست را عهده‌دار نمی‌باشد و نه حتی ترکیب نهایی حروف را؛ این عمل را پایانه‌ی اکس، برنامه یا کارگزار کنسول مجازی انجام می‌دهند.

%files -n locales-fa
%defattr(-,root,root)
/usr/share/locale/fa*

### fi
# translations by Jarkko Vaaraniemi <jvaarani@ees2.oulu.fi>
%package -n locales-fi
Summary: Base files for localization (Finnish)
Summary(fi): Tässä on perustiedot Linuxin suomentamiseen.
Group: System/Internationalization
Icon: bulle-fi.xpm
Requires: locales = %{version}-%{release}

%description -n locales-fi
These are the base files for Finnish language localization; you need
it to correctly display 8bits Finnish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Finnish language conventions.

%description -n locales-fi -l fi
Tässä on perustiedot Linuxin suomentamiseen. Tarvitset sitä suomalaisten
8-bittisten merkkien oikeaan esittämiseen, ja oikeaan aakkostamiseen ja
päivien ja numeroiden esitykseen suomenkielen käytännön mukaan.

%files -n locales-fi
%defattr(-,root,root)
/usr/share/locale/fi*

### fo
%package -n locales-fo
Summary: Base files for localization (Faroese)
Summary(fo): Hetta eru fílurnar tær tørvar til eina tillaging til føroyskt mál
Group: System/Internationalization
Icon: bulle-fo.xpm
Requires: locales = %{version}-%{release}

%description -n locales-fo
These are the base files for Faroese language localization; you need
it to correctly display 8bits Faroese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Faroese language conventions.

%description -n locales-fo -l fo
Hetta eru fílurnar tær tørvar til eina tillaging til føroyskt mál. Tær eru
neyðugar fyri at vísa føroyskar 8-bit stavir, fyri at fáa rætt stavrað og
vísa dagfestingar og tøl sambært føroyska siðvenju.

%files -n locales-fo
%defattr(-,root,root)
/usr/share/locale/fo*

### fr
%package -n locales-fr
Summary: Base files for localization (French)
Group: System/Internationalization
Icon: bulle-fr.xpm
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation (français)
Summary(de): Basisdateien für die Lokalisierung (Französisch)

%description -n locales-fr
These are the base files for French language localization; you need
it to correctly display 8bits french characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to french language conventions.

%description -n locales-fr -l fr
Ce paquet contient les définitions de locales en langue française.
Il permet aux applications de savoir quels caractères sont affichables
et donc afficher correctemment les caractères accentués et l'ordre
alphabetique; il contient aussi les definitions des representations
des dates des nombres et des symboles monétaires en Belgique, Canada,
Suisse, France et Luxembourg.

%description -n locales-fr -l de
Dies sind die Basisdateien für die französische Sprachanpassung; sie
werden für die korrekte Darstellung deutscher 8-Bit-Zeichen,
die französische Sortierreihenfolge sowie Datums- und Zahlendarstellung
benötigt.

%files -n locales-fr
%defattr(-,root,root)
/usr/share/locale/fr*

### ga
%package -n locales-ga
Summary: Base files for localization (Irish)
Summary(ga): Bunchomaid do leagan áitiúil (Gaeilge)
Group: System/Internationalization
Icon: bulle-ga.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ga
These are the base files for Irish Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%description -n locales-ga -l ga
Seo iad na bunchomhaid do leagan áitiúil na Gaeilge; ní mór duit
iad a fháil chun tacar carachtar 8ngiotán a thaispeáint i gceart,
agus sórtáil in ord aibitre agus dátaí agus uimhreacha a chur i
láthair de réir coinbhinsiúnaigh na Gaeilge.

%files -n locales-ga
%defattr(-,root,root)
/usr/share/locale/ga*

### gd
# translation by Caoimhin O Donnaile [caoimhin@SMO.UHI.AC.UK]
# and Cecil Ward [cecil.ward@FREE4ALL.CO.UK]
%package -n locales-gd
Summary: Base files for localization (Scottish Gaelic)
Summary(gd): Faidhlichean bunaiteach airson localization (Gaidhlig na h-Alba)
Group: System/Internationalization
Icon: bulle-gd.xpm
Requires: locales = %{version}-%{release}

%description -n locales-gd
These are the base files for Scottish Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%description -n locales-gd -l gd
Seo na faidhlichean bunaiteach air son "locale" na Gàidhlig.
Tha feum orra gus caractairean 8-bit fhaicinn, gus faclan a
chur ann an òrd na h-aibidile, agus gus àireamhan is cinn-latha
a riochdachadh a-réir nòs na Gàidhlig.

%files -n locales-gd
%defattr(-,root,root)
/usr/share/locale/gd*

### gl
# translation from Emilio <nigrann@sandra.ctv.es>
%package -n locales-gl
Summary: Base files for localization (Galician)
Group: System/Internationalization
Icon: bulle-gl.xpm
Requires: locales = %{version}-%{release}
Summary(gl): Arquivos da base para definición de locais para o galego.
Summary(es): Archivos de base para la localización en idioma gallego

%description -n locales-gl
These are the base files for Galician language localization; you need
it to correctly display 8bits Galician characters, and for proper
representation of dates and numbers according to Galician language
conventions.

%description -n locales-gl -l gl
Este paquete inclúe as definicións de locais para o galego. Este paquete
contén o preciso para a representacion correcta dos caracteres de 8 bits
da fala galega, dos números e datas segundo as convencións do galego.

%description -n locales-gl -l es
Este paquete incluye las definiciones de locales para el gallego.
Este paquete contiene lo necesario para la visualisación correcta de
los caracteres 8bits del gallego, para el orden alfabético
y para la representación correcta de los números y fechas según
las convenciones del gallego.

%files -n locales-gl
%defattr(-,root,root)
/usr/share/locale/gl*

### gv
# translation by Brian Stowell <bstowell@MAILSERVICE.MCB.NET>
%package -n locales-gv
Summary: Base files for localization (Manx Gaelic)
Summary(gv): Coadanyn undinagh son ynnydaghey (Gaelg)
Group: System/Internationalization
Icon: bulle-gv.xpm
Requires: locales = %{version}-%{release}

%description -n locales-gv
These are the base files for Manx Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%description -n locales-gv -l gv
T'ad shoh ny coadanyn undinagh ry-hoi ynnydaghey chengaghyn Gaelagh; ta
feme ayd orroo dy haishbyney karracteyryn Gaelagh 8-bit dy kiart, as son
reaghey-abbyrlit cooie as taishbyney-daaytyn as earrooyn coardail rish
reillyn-chengey Gaelagh.

%files -n locales-gv
%defattr(-,root,root)
/usr/share/locale/gv*


### he (formerly iw)
%package -n locales-he
Summary: Base files for localization (Hebrew)
Summary(he): המקום מכיל עמדות ללופויזציה בעברית 
Group: System/Internationalization
Icon: bulle-he.xpm
Requires: locales = %{version}-%{release}
Obsoletes: locales-iw
Provides: locales-iw

%description -n locales-he
These are the base files for Hebrew language localization; you need
it to correctly display 8bits Hebrew characters, and for proper
alfabetical sorting, and representation of dates and numbers 
according to Hebrew language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying; it is to the xterm, application or virtual
console driver to do that.

%description -n locales-he -l he
אלו הקבצים הבסיסיים לשימוש בעברית, אתה צריך את
החבילה הזאת בכדי להציג עברית של 8 ביטים,
לסידור לפי האלף בית, ולהצגה נכונה של מספרים
ותאריכים בהתאם ולקובל בשפה העברית. שים לב
שהחבילה הזאת אינה מטפטל בהמרה מימין לשמאל 
או משמאל לימין, על הישום או המסוף, בין אם של
X11 או המסוף וירטואלי, לעשות כן.

%files -n locales-he
%defattr(-,root,root)
/usr/share/locale/he*

### hi
%package -n locales-hi
Summary: Base files for localization (Hindi)
Group: System/Internationalization
Icon: bulle-hi.xpm
Requires: locales = %{version}-%{release}

%description -n locales-hi
These are the base files for Hindi language localization; you need
it to correctly display 8bits Hindi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Hindi language conventions.

%files -n locales-hi
%defattr(-,root,root)
/usr/share/locale/hi*

### hr
# translations by Vedran Rodic <vrodic@udig.hr>
%package -n locales-hr
Summary: Base files for localization (Croatian)
Group: System/Internationalization
Icon: bulle-hr.xpm
Requires: locales = %{version}-%{release}
Summary(hr): Osnovne datoteke za lokalizaciju (Hrvatski)

%description -n locales-hr
These are the base files for Croatian language localization; you need
it to correctly display 8bits Croatian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Croatian language conventions.

%description -n locales-hr -l hr
Ovo su osnovne datoteke za lokalizaciju na Hrvatski jezik; potrebne su
da bi se pravilno prikazali 8 bitni Hrvatski znakovi, za pravilno
sortiranje po abecedi i prikaz datuma i brojeva po pravilima
Hrvatskog jezika.

%files -n locales-hr
%defattr(-,root,root)
/usr/share/locale/hr*

### hu
%package -n locales-hu
Summary: Base files for localization (Hungarian)
Group: System/Internationalization
Icon: bulle-hu.xpm
Requires: locales = %{version}-%{release}
Summary(hu): Szükséges fájlok a magyarításhoz

%description -n locales-hu
These are the base files for Hungarian language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according 
to Hungarian language conventions.

%description -n locales-hu -l hu
Ezek a szükséges fájlok a magyarításhoz. Szükség van rá a
magyar helyesírás szabályainak megfelelő sorbarendezéshez,
számok és dátumok megjelenítéséhez.

%files -n locales-hu
%defattr(-,root,root)
/usr/share/locale/hu*

### hy
# translations by Eugene Sevinian <sevinian@crdlx2.yerphi.am>
%package -n locales-hy
Summary: Base files for localization (Armenian)
Group: System/Internationalization
Icon: bulle-hy.xpm
Requires: locales = %{version}-%{release}
Summary(hy): Ամփոփում. Հայացման հիմնական փաթեթները (ֆայլերը)

%description -n locales-hy
These are the base files for Armenian language localization.
You need it to correctly display 8bit Armenian chars, 
for sorting order and proper representation of dates and
numbers according to Armenian language conventions.

%description -n locales-hy -l hy
Այստեղ ներկայացված են հայացման հիմնական փաթեթները (ֆայլերը)։
Դրանք անհրաժեշտ են տվյալների ճշգրիտ խմբավորման եւ ամսաթվերի ու
թվային արժեքների պատշաճ ներկայցման համար համաձայն հայոց լեզվի
կանոնների։

%files -n locales-hy
%defattr(-,root,root)
/usr/share/locale/hy*

### id (formerly in)
# translations by Mohammad DAMT <mdamt@cakraweb.com>
%package -n locales-id
Summary: Base files for localization (Indonesian)
Group: System/Internationalization
Icon: bulle-id.xpm
Requires: locales = %{version}-%{release}
Summary(id): File Utama untuk lokalisasi (dalam Bahasa Indonesia)
Obsoletes: locales-in
Provides: locales-in

%description -n locales-id
These are the base files for Indonesian language localization.
You need it to correctly display sort, for proper representation
of dates and numbers according to Indonesian language conventions.

%description -n locales-id -l id
Ini adalah file untuk lokalisasi sistem ke dalam Bahasa Indonesia.
File ini dibutuhkan bila Anda ingin menampilkan tanggal dan penomoran
yang sesuai dengan kaidah Bahasa Indonesia.

%files -n locales-id
%defattr(-,root,root)
/usr/share/locale/id*

### is
# Gudmundur Erlingsson <gudmuner@lexis.hi.is>
%package -n locales-is
Summary: Base files for localization (Icelandic)
Group: System/Internationalization
Icon: bulle-is.xpm
Requires: locales = %{version}-%{release}
Summary(is): Hér eru grunnskrár fyrir íslenska staðfærslu.

%description -n locales-is
These are the base files for Icelandic language localization; you need
it to correctly display 8bits Icelandic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Icelandic language conventions.

%description -n locales-is -l is
Hér eru grunnskrár fyrir íslenska staðfærslu. Þú þarft á þessum skrám að
halda ef 8 bita séríslenskir stafir eiga að birtast réttir, til að fá
rétta stafrófsröð og til að dagsetningar og tölur birtist eins og
venja er í íslensku.

%files -n locales-is
%defattr(-,root,root)
# I can't use /usr/share/locale/is* because of /usr/share/locale/iso_8859_1
/usr/share/locale/is
/usr/share/locale/is_*

### it
%package -n locales-it
Summary: Base files for localization (Italian)
Summary(it): I files di base per l'adattamento della lingua italiana
Group: System/Internationalization
Icon: bulle-it.xpm
Requires: locales = %{version}-%{release}

%description -n locales-it
These are the base files for Italian language localization; you need
it to correctly display 8bits Italian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Italian language conventions.

%description -n locales-it -l it
Questi sono i files di base per l'adattamento della lingua italiana. Vi
servono per visualizzare correttamente i caratteri a 8bit in italiano,
per l'ordinamento alfabetico corretto e per la rappresentazione delle
date e dei numeri in forma italiana.

%files -n locales-it
%defattr(-,root,root)
/usr/share/locale/it*

### iu
%package -n locales-iu
Summary: Base files for localization (Inuktitut)
Group: System/Internationalization
Icon: bulle-iu.xpm
Requires: locales = %{version}-%{release}

%description -n locales-iu
These are the base files for Inuktitut language localization; you need
it to correctly display 8bits Inuktitut characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Inuktitut language conventions.

%files -n locales-iu
%defattr(-,root,root)
/usr/share/locale/iu*

### ja
# translation by "Evan D.A. Geisinger" <evan.geisinger@etak.com>
%package -n locales-ja
Summary: Base files for localization (Japanese)
Summary(ja): これは日本語ロカライゼーション用基礎ファイル集です。
Group: System/Internationalization
Icon: bulle-ja.xpm
Requires: locales = %{version}-%{release}
Obsoletes: libwcsmbs

%description -n locales-ja
These are the base files for Japanese language localization; you need
it to correctly display 8bits and 7bits japanese codes, and for proper
representation of dates and numbers according to japanese language conventions.

%description -n locales-ja -l ja
これは日本語ロカライゼーション用基礎ファイル集です。これがないと，
７・８ビット文字コードの表示もできず、日本式日付き表現・数値表現ができない。
ただし、要注意点として：１６ビット文字コードが使えなかったので、
このロカール（地域特有設定データ集）が完璧・正式に「正確」とはいいきれない。
（多少「誤魔化し」を利かせて作ったからです）。

%files -n locales-ja
%defattr(-,root,root)
/usr/share/locale/ja*

### ka
%package -n locales-ka
Summary: Base files for localization (Georgian)
Group: System/Internationalization
Icon: bulle-ka.xpm
Requires: locales = %{version}-%{release}
Summary(ka): საბაზო ფაილები ქართულის ლოკალიზებისათვის.

%description -n locales-ka
These are the base files for Georgian language localization; you need
it to correctly display 8bits Georgian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Georgian language conventions.

%description -n locales-ka -l ka
საბაზო ფაილები ქართულის ლოკალიზებისათვის.
საჭიროა 8 ბიტიანი ფონტებით ქართული ანბანის სწორი ჩვენებისა
და სორტირებისათვის. აგრეთვე - თარიღის, ფულის ნიშნებისა და
რიცხვითი მნიშვნელობების მართებული წარმოდგენისათვის.

%files -n locales-ka
%defattr(-,root,root)
/usr/share/locale/ka*

### kh
%package -n locales-kh
Summary: Base files for localization (Khmer)
Group: System/Internationalization
Icon: bulle-kh.xpm
Requires: locales = %{version}-%{release}

%description -n locales-kh
These are the base files for Khmer language localization; you need
it to correctly display 8bits Khmer characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Khmer language conventions.

#%files -n locales-kh
#%defattr(-,root,root)
#/usr/share/locale/kh*

### kl
%package -n locales-kl
Summary: Base files for localization (Greenlandic)
Group: System/Internationalization
Icon: bulle-kl.xpm
Requires: locales = %{version}-%{release}

%description -n locales-kl
These are the base files for Greenlandic language localization; you need
it to correctly display 8bits Greenlandic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Grenlandic language conventions.

%files -n locales-kl
%defattr(-,root,root)
/usr/share/locale/kl*

### kn
%package -n locales-kn
Summary: Base files for localization (Kannada)
Group: System/Internationalization
Icon: bulle-kn.xpm
Requires: locales = %{version}-%{release}

%description -n locales-kn
These are the base files for Kannada language localization; you need
it to correctly display 8bits Kannada characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kannada language conventions.

%files -n locales-kn
%defattr(-,root,root)
/usr/share/locale/kn*

### ko
# translation by Soo-Jin Lee <NothingSpecial@rocketmail.com>
%package -n locales-ko
Summary: Base files for localization (Korean)
Summary(ko): 이것들은 한국어에만 국한된 기초화일들이다
Group: System/Internationalization
Icon: bulle-ko.xpm
Requires: locales = %{version}-%{release}
Obsoletes: libwcsmbs

%description -n locales-ko
These are the base files for Korean language localization; you need
it to correctly display 8bits and 7bits japanese codes, and for proper
representation of dates and numbers according to korean language conventions.

%description -n locales-ko -l ko
이것들은 한국어에만 국한된 기초화일들이다 당신은 한국어규정에
의한 적절한 날짜와 숫자들의 표시를 8바이트와 7바이트의 한국어
코드로 정확히 배열하는데 그것이 필요하다.

%files -n locales-ko
%defattr(-,root,root)
/usr/share/locale/ko*

### ku
%package -n locales-ku
Summary: Base files for localization (Kurdish)
Summary(ku): Rûpel-tâmar ji bo naskirinâ cîh (Kurdi)
Group: System/Internationalization
Icon: bulle-ku.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ku
These are the base files for Kurdish language localization; you need
it to correctly display 8bits Kurdish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kurdish language conventions.

%description -n locales-ku -l ku
Vâhan rûpelen-tâmarê ji bo cîhnaskirînâ zîmanê kurdi, ji bo qû herfên
kurd â 8bits ân vêrin ditin, vâ rûpel-tamar bî vê gêrege ji bo alfabêya
kurdi, dîrok, seat, hêjmar û edetê malbatâ zîmanê kurdin vêre naskirin
bi haliyê systême

%files -n locales-ku
%defattr(-,root,root)
/usr/share/locale/ku*

### kw
# translations by Andrew Climo-Thompson <andrew@clas.demon.co.uk>
# Laurie Climo <lj.climo@ukonline.co.uk> & Marion Gunn <mgunn@ucd.ie>
%package -n locales-kw
Summary: Base files for localization (Cornish)
Summary(kw): Fylennow sel dhe gernewekhe
Group: System/Internationalization
Icon: bulle-kw.xpm
Requires: locales = %{version}-%{release}

%description -n locales-kw
These are the base files for Cornish language localization; you need
it to correctly display 8bits cornish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Cornish language conventions.

%description -n locales-kw -l kw
Otomma'n fylennow sel dhe Gernewekhe an system; 'ma ethom anodho
dhe dhysplegya lythrennow Kernewek 8-ryf dhe wyr, ha sortya yn ordyr
abecedery gwyw ha dysquesdhes dedhyow ha nyverow herwyth rewlys
a'n tavas Kernewek.

%files -n locales-kw
%defattr(-,root,root)
/usr/share/locale/kw*

### lo
%package -n locales-lo
Summary: Base files for localization (Laotian) [INCOMPLETE]
Group: System/Internationalization
Icon: bulle-lo.xpm
Requires: locales = %{version}-%{release}

%description -n locales-lo
These are the base files for Laotian language localization; you need
it to correctly display 8bits lao characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Laotian language conventions.
[THIS IS REALLY INCOMPLETE; OTHER THAN LC_CTYPE THE REST IS STILL
TO BE WRITTEN; ANYONE WANTING TO HELP ?
-- PABLO (srtxg@chanae.alphanet.ch)]

%files -n locales-lo
%defattr(-,root,root)
# not just lo* because of locale.alias
/usr/share/locale/lo
/usr/share/locale/lo_*

### lt
%package -n locales-lt
Summary: Base files for localization (Lithuanian)
Summary(lt): Failai skirti lokalės lituanizacijai
Group: System/Internationalization
Icon: bulle-lt.xpm
Requires: locales = %{version}-%{release}

%description -n locales-lt
These are the base files for Lithuanian language localization; you need
it to correctly display 8bits Lithuanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Lithuanian language conventions.

%description -n locales-lt -l lt
Baziniai failai skirti lokalės lituanizacijai; reikalingi korektiš
kam lietuviškų, 8 bitų simbolių atvaizdavimui, alfabetiniam rūšiavimui
bei datos ir skaičių atvaizdavimui.

%files -n locales-lt
%defattr(-,root,root)
/usr/share/locale/lt*

### lv
# translation done by Vitauts Stochka <vit@dpu.lv>
%package -n locales-lv
Summary: Base files for localization (Latvian)
Summary(lv): Lokalizācijas pamatfaili (Latviešu)
Group: System/Internationalization
Icon: bulle-lv.xpm
Requires: locales = %{version}-%{release}

%description -n locales-lv
These are the base files for Latvian language localization; you need
it to correctly display 8bits Latvian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Latvian language conventions.


%description -n locales-lv -l lv
Šie ir latviešu valodas lokalizācijas pamatfaili; tie jums ir
nepieciešami, lai pareizi attēlotu 8bitu latviešu burtus, veiktu
pareizu kārtošanu pēc alfabēta, kā arī attēlotu datumus un skaitļus
saskaņā ar latviešu valodā pieņemtajām normām.


%files -n locales-lv
%defattr(-,root,root)
/usr/share/locale/lv*

### mi
# Maori translation provided by Gasson <gasson@clear.net.nz>
%package -n locales-mi
Summary: Base files for localization (Maori)
Summary(mi): Ko ngā kōnae papa mō te whakaā-rohe (Māori)
Group: System/Internationalization
Icon: bulle-mi.xpm
Requires: locales = %{version}-%{release}

%description -n locales-mi
These are the base files for Maori language localization; you need it for
it to correctly display 8bits Maori characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Maori language conventions.

%description -n locales-mi -l mi
Ko ēnei ngā kōnae papa mō te whakaā-rohe reo Maori; he mea kē tēnei kei
whakaatuhia i ngā pū Māori mati kaupapa-ā-rua e waru kia tika ai, ā, mō te
whakatakotoranga hoki o ngā wā me ngā nama kia tika ai anō e ai ki ngā aro
whānui reo Māori.

%files -n locales-mi
%defattr(-,root,root)
/usr/share/locale/mi*

### mk
%package -n locales-mk
Summary: Base files for localization (Macedonian)
Group: System/Internationalization
Icon: bulle-mk.xpm
Requires: locales = %{version}-%{release}

%description -n locales-mk
These are the base files for Macedonian language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Macedonian language conventions.

%files -n locales-mk
%defattr(-,root,root)
/usr/share/locale/mk*

### ml
%package -n locales-ml
Summary: Base files for localization (Malayalam)
Group: System/Internationalization
Icon: bulle-ml.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ml
These are the base files for Malayalam language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Malayalam language conventions.

%files -n locales-ml
%defattr(-,root,root)
/usr/share/locale/ml*

### mn
%package -n locales-mn
Summary: Base files for localization (Mongolian)
Group: System/Internationalization
Icon: bulle-mn.xpm
Requires: locales = %{version}-%{release}

%description -n locales-mn
These are the base files for Mongolian language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Mongolian language conventions.

%files -n locales-mn
%defattr(-,root,root)
/usr/share/locale/mn*

### mr
%package -n locales-mr
Summary: Base files for localization (Marathi)
Group: System/Internationalization
Icon: bulle-mr.xpm
Requires: locales = %{version}-%{release}

%description -n locales-mr
These are the base files for Marathi language localization; you need
it to correctly display 8bits Marathi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Marathi language conventions.

%files -n locales-mr
%defattr(-,root,root)
/usr/share/locale/mr*

### ms
%package -n locales-ms
Summary: Base files for localization (Malay)
Group: System/Internationalization
Icon: bulle-ms.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ms
These are the base files for Malay language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Malay language conventions.

%files -n locales-ms
%defattr(-,root,root)
/usr/share/locale/ms*

### mt
# translation by Ramon Casha <rcasha@waldonet.net.mt>
%package -n locales-mt
Summary: Base files for localization (Maltese)
Summary(mt): Files ewlenin għat-traduzzjoni (Maltin)
Group: System/Internationalization
Icon: bulle-mt.xpm
Requires: locales = %{version}-%{release}

%description -n locales-mt
These are the base files for Maltese language localization; you need
it to correctly display 8bits Maltese characters, and for proper
alphabetical sorting and representation of dates and numbers according\
to Maltese language conventions.

%description -n locales-mt -l mt
Dawn huma l-files ewlenin għat-traduzzjoni għal-lingwa Maltija;
għandek bżonnhom biex turi l-ittri 8-bit Maltin sew, biex tissortja
alfabetikament, u biex turi dati u numri skond il-konvenzjonijiet
tal-lingwa Maltija.

%files -n locales-mt
%defattr(-,root,root)
/usr/share/locale/mt*

### nl
%package -n locales-nl
Summary: Base files for localization (Dutch)
Group: System/Internationalization
Icon: bulle-nl.xpm
Requires: locales = %{version}-%{release}
Summary(fr): Fichiers de base pour la localisation en langue néerlandaise
Summary(nl): Dit zijn de basisbestanden nodig voor de Nederlandse taal

%description -n locales-nl
These are the base files for Dutch language localization; you need
it to correctly display 8bits Dutch characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Dutch language conventions.

%description -n locales-nl -l fr
Ce paquet contient les définitions de locales en langue néerlandaise.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates des nombres.

description -n locales-nl -l nl
Dit zijn de basisbestanden nodig voor de Nederlandse taalmodule; ze zijn
noodzakelijk om de 8bits Nederlandse karakters correct weer te geven en
voor een juiste alfabetische sortering en weergave van data en nummers
volgens de Nederlandse Taalconventies

%files -n locales-nl
%defattr(-,root,root)
/usr/share/locale/nl*

### no
# translations by peter@datadok.no
%package -n locales-no
Summary: Base files for localization (Norwegian)
Summary(no): Dette er basisfilene for lokalisering til norsk språk
Group: System/Internationalization
Icon: bulle-no.xpm
Requires: locales = %{version}-%{release}
Provides: locales-nn, locales-nb

%description -n locales-no
These are the base files for Norwegian language localization; you need
it to correctly display 8bits Norwegian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Norwegian language conventions.

%description -n locales-no -l no
Dette er basisfilene for lokalisering til norsk språk. Du trenger dette
for å vise norske 8-bitstegn på riktig måte og for å få riktig sortering
etter alfabetet og visning av datoer og tall i samsvar med norske
konvensjoner.

%files -n locales-no
%defattr(-,root,root)
/usr/share/locale/no*
#/usr/share/locale/nb*
/usr/share/locale/nn*

### oc
%package -n locales-oc
Summary: Base files for localization (Occitan)
Group: System/Internationalization
Icon: bulle-oc.xpm
Requires: locales = %{version}-%{release}
Summary(oc): fichièrs de basa per localisar (occitan)

%description -n locales-oc
These are the base files for Occitan language localization; you need
it to correctly display 8bits Occitan characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Occitan language conventions.

%description -n locales-oc -l oc
Aicí avem empaquetat los fichièrs de basa per la lengua occitana : los
programas n'an de besonh per afichar corrèctament los caractèrs dins lo
fenestron, classar l'òrdre alfabetic e atanben comptar los jorns 
e los meses en occitan.

%files -n locales-oc
%defattr(-,root,root)
/usr/share/locale/oc*

### ph
%package -n locales-ph
Summary: Base files for localization (Pilipino)
Group: System/Internationalization
Icon: bulle-ph.xpm
Requires: locales = %{version}-%{release}
Provides: locales-tl

%description -n locales-ph
These are the base files for Pilipino (official language of the Philipines)
localization; you need it to correctly display 8bits characters,
and for proper alphabetical sorting and representation of dates and numbers
according to Pilipino language conventions.

%files -n locales-ph
%defattr(-,root,root)
/usr/share/locale/ph*
/usr/share/locale/tl*

# ### pd
# %package -n locales-pd
# Summary: Base files for localization (Plautdietsch)
# Summary(de): Basisdateien für die Lokalisierung (Plautdietsch)
# Summary(pd): Grundspikjaloden fe' Sproaktoopaussinj (Plautdietsch)
# Group: System/Internationalization
# Icon: bulle-pd.xpm
# Requires: locales = %{version}
# 
# %description -n locales-pd
# These are the base files for Plautdietsch (Mennonite LowGerman) language
# localization; you need it to correctly display 8bits Plaudietsch characters,
# and for proper alphabetical sorting and representation of dates and numbers
# according to Plautdietsch language conventions.
# 
# %description -n locales-pd -l pd
# Dit send de Grundspikjaloden fe' de plautdietsche Sproaktoopaussinj.
# Dee woaren jebrukt om de 8-bit'sche plautdietsche Teakjens noh Droat
# ut to drekjen, aules jescheit noh'm Aulfabeet to sortieren, un uk de Dotums
# un Nummasch soo auntojäwen soo's daut jeweehnlich em Plautdietschen jeiht.
# 
# %description -n locales-pd -l de
# Dies sind die Basisdateien für die plautdietsche Sprachanpassung; sie
# werden für die korrekte Darstellung plautdietscher 8-Bit-Zeichen,
# die plautdietsche Sortierreihenfolge sowie Datums- und Zahlendarstellung
# benötigt.
# 
# %files -n locales-pd
# %defattr(-,root,root)
# /usr/share/locale/pd*

### pl
# translation from piotr pogorzelski <pp@pietrek.priv.pl>
%package -n locales-pl
Summary: Base files for localization (Polish)
Group: System/Internationalization
Icon: bulle-pl.xpm
Requires: locales = %{version}-%{release}
Summary(pl): Podstawowe pliki dla polskiej lokalizacji

%description -n locales-pl
These are the base files for Polish language localization; you need
it to correctly display 8bits Polish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Polish language conventions.

%description -n locales-pl -l pl
Pliki do lokalizacji systemu dla języka polskiego. Niezbędne do poprawnego
wyświetlania 8-mio bitowych polskich znaków diakrytycznych, sortowania,
prezentowania dat i liczb zgodnie z regułami języka polskiego.

%files -n locales-pl
%defattr(-,root,root)
/usr/share/locale/pl*

### pp 
%package -n locales-pp
Summary: Base files for localization (Papiamento)
Group: System/Internationalization
Icon: bulle-pp.xpm
Requires: locales = %{version}-%{release}

%description -n locales-pp
These are the base files for Papiamento language localization; you need
it to correctly display 8bits Papiamento characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Papiamento language conventions.

%files -n locales-pp
%defattr(-,root,root)
/usr/share/locale/pp*

### pt
%package -n locales-pt
Summary: Base files for localization (Portuguese)
Summary(pt): Estes são os arquivos básicos para a localização (Português)
Group: System/Internationalization
Icon: bulle-pt.xpm
Requires: locales = %{version}-%{release}

%description -n locales-pt
These are the base files for Portuguese language localization; you need
it to correctly display 8bits Portuguese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Portuguese language conventions.

%description -n locales-pt -l pt
Estes são os arquivos básicos para a localização lingüística em português;
eles são necessários para que o sistema mostre corretamente caracteres
portugueses de 8 bits, e para que tenha as apropriadas ordenações
alfabéticas e representação de datas e números de acordo com as convenções
da língua portuguesa.

%files -n locales-pt
%defattr(-,root,root)
/usr/share/locale/pt*

### ro
# translation from "Mihai" <mihai@ambra.ro>
%package -n locales-ro
Summary: Base files for localization (Romanian)
Summary(ro): Acestea sînt fisierele pentru române localizarea
Group: System/Internationalization
Icon: bulle-ro.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ro
These are the base files for Romanian language localization; you need
it to correctly display 8bits Romanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Romanian language conventions.

%description -n locales-ro -l ro
Acestea sînt fisierele de baza pentru localizarea în limba româna; sînt
necesare pentru afisarea corecta a caracterelor românesti pe 8 biti precum
si pentru sortarea alfabetica si reprezentarea datelor si numerelor conform
cu conventiile din limba româna.

%files -n locales-ro
%defattr(-,root,root)
/usr/share/locale/ro*

### ru
%package -n locales-ru
Summary: Base files for localization (Russian)
Group: System/Internationalization
Icon: bulle-ru.xpm
Requires: locales = %{version}-%{release}
Summary(ru): Основные файлы региональных установок (для России)

%description -n locales-ru
These are the base files for Russian language localization; you need
it to correctly display 8bits cyrillic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Russian language conventions.

%description -n locales-ru -l ru
Эти файлы содержат основные региональные установки
для русского языка; они необходимы для правильного
представления 8-битных букв кириллицы на экране,
для правильной алфавитной сортировки и для
представления дат и чисел в соответствии с правилами
русского языка.

%files -n locales-ru
%defattr(-,root,root)
/usr/share/locale/ru*

### se
%package -n locales-se
Summary: Base files for localization (Saami)
Group: System/Internationalization
#Icon: bulle-se.xpm
Requires: locales = %{version}-%{release}

%description -n locales-se
These are the base files for Saami language localization; you need
it to correctly display 8bits Saami characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Saami language conventions.

%files -n locales-se
%defattr(-,root,root)
/usr/share/locale/se*

### sk
%package -n locales-sk
Summary: Base files for localization (Slovak)
Summary(sk): Toto su zakladne súbory pre slovenskú lokalizaciu
Group: System/Internationalization
Icon: bulle-sk.xpm
Requires: locales = %{version}-%{release}

%description -n locales-sk
These are the base files for Slovak language localization; you need
it to correctly display 8bits Slovak characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Slovak language conventions.

%description -n locales-sk -l sk
Tu sú súbory potrebné pre správnu slovenskú lokalizáciu; potrebujete ich pre
korektné zobrazovanie slovenských 8bitových znakov a pre správne triedenie a
reprezentáciu dátumu a čísel podľa konvencií slovenského jazyka.

%files -n locales-sk
%defattr(-,root,root)
/usr/share/locale/sk*

### sl
# Translations from Roman Maurer <roman.maurer@fmf.uni-lj.si>
%package -n locales-sl
Summary: Base files for localization (Slovenian)
Summary(sl): Osnovne datoteke za lokalizacijo (slovenščina)
Group: System/Internationalization
Icon: bulle-sl.xpm
Requires: locales = %{version}-%{release}

%description -n locales-sl
These are the base files for Slovenian language localization; you need
it to correctly display 8bits Slovenian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Slovenian language conventions.

%description -n locales-sl -l sl
To so osnovne datoteke za lokalizacijo Linuxa na slovenski
jezik; potrebujete jih za pravilni prikaz 8-bitnih
slovenskih znakov in za pravilno urejanje po abecedi ter
predstavitev datumov in številk glede na pravila
slovenskega jezika.

%files -n locales-sl
%defattr(-,root,root)
/usr/share/locale/sl*

### sq
%package -n locales-sq
Summary: Base files for localization (Albanian)
Group: System/Internationalization
Icon: bulle-sq.xpm
Requires: locales = %{version}-%{release}

%description -n locales-sq
These are the base files for Albanian language localization; you need
it to correctly display 8bits Albanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Albanian language conventions.

%files -n locales-sq
%defattr(-,root,root)
/usr/share/locale/sq*

### sr
%package -n locales-sr
Summary: Base files for localization (Serbian)
Group: System/Internationalization
Icon: bulle-sr.xpm
Requires: locales = %{version}-%{release}
Provides: locales-sh
Provides: locales-sp
Summary(sr): Основне датотеке за локализацију (Српски) 
Summary(sr@Latn): Osnovne datoteke za lokalizaciju (Srpski)
Summary(sh): Osnovne datoteke za lokalizaciju (Srpski)

%description -n locales-sr
These are the base files for Serbian language localization; you need
it to correctly display 8bits cyrillic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Serbian language conventions.

%description -n locales-sr -l sr
Ово су основне датотеке за
локализацију на Српски језик; потребне
су да се правилно приказали 8 битни
Српски знакови, за правилно
сортирање по абецеди и приказ датума
и бројева по правилима Српског језика.

%description -n locales-sr -l sr@Latn
Ovo su osnovne datoteke za
lokalizaciju na Srpski jezik; potrebne
su da se pravilno prikazali 8 bitni
Srpski znakovi, za pravilno
sortiranje po abecedi i prikaz datuma
i brojeva po pravilima Srpskog jezika.

%description -n locales-sr -l sh
Ovo su osnovne datoteke za
lokalizaciju na Srpski jezik; potrebne
su da se pravilno prikazali 8 bitni
Srpski znakovi, za pravilno
sortiranje po abecedi i prikaz datuma
i brojeva po pravilima Srpskog jezika.

%files -n locales-sr
%defattr(-,root,root)
/usr/share/locale/sh*
/usr/share/locale/sr*
/usr/share/locale/sp*

### st
%package -n locales-st
Summary: Base files for localization (Sotho)
Group: System/Internationalization
Icon: bulle-st.xpm
Requires: locales = %{version}-%{release}

%description -n locales-st
These are the base files for Sotho language localization; you need
it to correctly display 8bits Sotho characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Sotho language conventions.

%files -n locales-st
%defattr(-,root,root)
/usr/share/locale/st*

### sv
# translation by Erik Almqvist <erik.almqvist@vrg.se>
%package -n locales-sv
Summary: Base files for localization (Swedish)
Summary(sv): Detta är huvudfilerna för svenskt språkstöd
Group: System/Internationalization
Icon: bulle-sv.xpm
Requires: locales = %{version}-%{release}

%description -n locales-sv
These are the base files for Swedish language localization; you need
it to correctly display 8bits Swedish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Swedish language conventions.

%description -n locales-sv -l sv
Detta är huvudfilerna för svenskt språkstöd. De behövs för att korrekt visa
svenska 8 bitars tecken och för korrekt alfabetisk sortering. De gör även
att datum och nummerformat visas på svenskt vis.

%files -n locales-sv
%defattr(-,root,root)
/usr/share/locale/sv*

### ta
%package -n locales-ta
Summary: Base files for localization (Tamil)
Group: System/Internationalization
Icon: bulle-ta.xpm
Requires: locales = %{version}-%{release}
URL: http://www.tamil.net/tscii/

%description -n locales-ta
These are the base files for Tamil language localization; you need
it to correctly display 8bits Tamil characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tamil language conventions.

%files -n locales-ta
%defattr(-,root,root)
/usr/share/locale/ta*
# special files needed while Linux doesn't know about tscii
/etc/gtk/gtkrc.ta_IN
/etc/gtk-2.0/gtkrc.ta_IN

### te
%package -n locales-te
Summary: Base files for localization (Telugu)
Group: System/Internationalization
Icon: bulle-te.xpm
Requires: locales = %{version}-%{release}

%description -n locales-te
These are the base files for Telugu language localization; you need
it to correctly display 8bits Telugu characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Telugu language conventions.

%files -n locales-te
%defattr(-,root,root)
/usr/share/locale/te*

### tg
%package -n locales-tg
Summary: Base files for localization (Tajik)
Group: System/Internationalization
Icon: bulle-tg.xpm
Requires: locales = %{version}-%{release}

%description -n locales-tg
These are the base files for Tajik language localization; you need
it to correctly display 8bits Tajik characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tajik language conventions.

%files -n locales-tg
%defattr(-,root,root)
/usr/share/locale/tg*

### th
%package -n locales-th
Summary: Base files for localization (Thai)
Group: System/Internationalization
Icon: bulle-th.xpm
Requires: locales = %{version}-%{release}
URL: http://www.links.nectec.or.th/~thep/th-locale/

%description -n locales-th
These are the base files for Thai language localization; you need
it to correctly display 8bits Thai characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Thai language conventions.

%files -n locales-th
%defattr(-,root,root)
/usr/share/locale/th*

### tr
# translation from Gorkem Cetin <e077245@narwhal.cc.metu.edu.tr>
%package -n locales-tr
Summary: Base files for localization (Turkish)
Group: System/Internationalization
Icon: bulle-tr.xpm
Requires: locales = %{version}-%{release}
Summary(tr): Yerelleştirme için temel dosyalar (Türkçe)

%description -n locales-tr
These are the base files for Turkish language localization; you need
it to correctly display 8bits Turkish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Turkish language conventions.

%description -n locales-tr -l tr
Bu dosyalar, Türkçe yerelleştirmesi için gerekli temel bileşenleri içerir.
8bit türkçe karakterleri görmek, Türk diline uygun olarak alfabe, tarih ve
sayı gösterimlerini ve sıralamalarını yapabilmek için bu dosyalara
ihtiyacınız vardır.

%files -n locales-tr
%defattr(-,root,root)
/usr/share/locale/tr*

### tt
%package -n locales-tt
Summary: Base files for localization (Tatar)
Group: System/Internationalization
Icon: bulle-tt.xpm
Requires: locales = %{version}-%{release}

%description -n locales-tt
These are the base files for Tatar language localization; you need
it to correctly display 8bits Tatar characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tatar language conventions.

%files -n locales-tt
%defattr(-,root,root)
/usr/share/locale/tt*

### uk
%package -n locales-uk
Summary: Base files for localization (Ukrainian)
Group: System/Internationalization
Icon: bulle-uk.xpm
Requires: locales = %{version}-%{release}
Summary(ru): Базовые файлы для Украинской локализации
Summary(uk): Базові файли для української локалізації

%description -n locales-uk
These are the base files for Ukrainian language localization; you need
it to correctly display 8bits Ukrainian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Ukrainian language conventions.

%description -n locales-uk -l ru
Базовые файлы для Украинской локализации; нужны для корректного
представления 8-ми битных Украинских символов, а также для правильной
сортировки и представления даты и чисел в соответствии со стандартами
Украинского языка.

%description -n locales-uk -l uk
Базові файли для української локалізації; необхідні для правильного
відображення 8-ми бітних символів українського алфавіту і також для
правильного сортування і подання дати і чисел у відповідності до
стандартів української мови.

%files -n locales-uk
%defattr(-,root,root)
/usr/share/locale/uk*

### ur
%package -n locales-ur
Summary: Base files for localization (Urdu)
Group: System/Internationalization
Icon: bulle-ur.xpm
Requires: locales = %{version}-%{release}

%description -n locales-ur
These are the base files for Urdu language localization; you need
it to correctly display 8bits Urdu characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Urdu language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%files -n locales-ur
%defattr(-,root,root)
/usr/share/locale/ur*

### uz
%package -n locales-uz
Summary: Base files for localization (Uzbek)
Summary(uz): Lokallashtirishning asosiy fayllari (o'zbekcha)
Group: System/Internationalization
Icon: bulle-uz.xpm
Requires: locales = %{version}-%{release}

%description -n locales-uz
These are the base files for Uzbek language localization; you need
it to correctly display 8bits Uzbek characters, and for proper
alphabetical sorting and representation of dates and numbers
according to Uzbek language conventions.

%description -n locales-uz -l uz
Ushbu asos fayllar Linuxni o'zbekchaga locallashtirish
uchun qo'llaniladi; siz bularni 8 bit o'zbek
harflarini to'g'ri ko'rish va tartiblashda qollanasiz.
O'zbekistonda joriy bo'lgan vaqt, son va valytani
belgilash qoidalari ham shu fayllarda joylashgan.

%files -n locales-uz
%defattr(-,root,root)
/usr/share/locale/uz*

### vi
# translations by <DaiQuy.nguyen@ulg.ac.be>
%package -n locales-vi
Summary: Base files for localization (Vietnamese)
Group: System/Internationalization
Icon: bulle-vi.xpm
Requires: locales = %{version}-%{release}
Summary(vi): Các file cơ sở cho định vị tiếng Việt 

%description -n locales-vi
These are the base files for Vietnamese language localization; you need
it to correctly display 8bits Vietnamese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Vietnamese language conventions.

%description -n locales-vi -l vi
Đây là các file cơ sở cho tiếng Việt.
Bạn cần những file này để có thể
biểu diễn chính xác các kí tự tiếng Việt 8 bits,
để sắp xếp và trình bày ngày tháng và số
một cách chính xác theo đúng qui ước ngôn ngữ tiếng Việt.

%files -n locales-vi
%defattr(-,root,root)
/usr/share/locale/vi*

### wa
# translations from Lorint Hendschel <LorintHendschel@skynet.be>
%package -n locales-wa
Summary: Base files for localization (Walloon)
Group: System/Internationalization
Icon: bulle-wa.xpm
Requires: locales = %{version}-%{release}
Summary(wa): Maisses fitchîs pol lingaedje walon
Summary(fr): Fichiers de base pour la localisation en langue wallonne

%description -n locales-wa
These are the base files for Walloon language localization; you need
it to correctly display 8bits Walloon characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Walloon language conventions.

%description -n locales-wa -l wa
Vochal les maisses fitchîs pol lingaedje walon. Vos nd avoz dandjî po
hågner les caracteres walons ecôdés so ût bits, po l' arindjmint
alfabetike eyèt po rprezinter les dates eyèt les nombes è walon.

%description -n locales-wa -l fr
Ce paquet contient les définitions de locales en langue walone.
Il permet aux applications de savoir quels caractères sont affichables et
donc afficher correctemment les caractères accentués et l'ordre alphabetique;
il contient aussi les definitions des representations des dates et des nombres.

%files -n locales-wa
%defattr(-,root,root)
/usr/share/locale/wa*

### xh
%package -n locales-xh
Summary: Base files for localization (Xhosa)
Group: System/Internationalization
Icon: bulle-xh.xpm
Requires: locales = %{version}-%{release}

%description -n locales-xh
These are the base files for Xhosa language localization; you need
it to correctly display 8bits Xhosa characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Xhosa language conventions.

%files -n locales-xh
%defattr(-,root,root)
/usr/share/locale/xh*

### yi
%package -n locales-yi
Summary: Base files for localization (Yiddish)
Group: System/Internationalization
Icon: bulle-yi.xpm
Requires: locales = %{version}-%{release}
URL: http://www.uyip.org/

%description -n locales-yi
These are the base files for Yiddish language localization; you need
it to correctly display 8bits Yiddish characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Yiddish language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying; it is to the xterm, application or virtual
console driver to do that.

%files -n locales-yi
%defattr(-,root,root)
/usr/share/locale/yi*

### zh
# translation (zh_TW) from <informer@linux1.cgu.edu.tw>
# zh_CN converted from zh_TW.Big5 with b5togb; corrections welcome.
%package -n locales-zh
Summary: Base files for localization (Chinese)
Group: System/Internationalization
Icon: bulle-zh.xpm
Requires: locales = %{version}-%{release}
Obsoletes: libwcsmbs wcsmbs-locale
Summary(zh_CN): 中文地方化的基本档案
Summary(zh_TW): 中文地方化的基本檔案

%description -n locales-zh
These are the base files for Chinese language localization; you need
it to correctly display 8bits and 7bits chinese codes, and for proper
representation of dates and numbers according to chinese language conventions.
Set the LANG variable to "zh_CN" to use simplified chinese (GuoBiao encoding)
or to "zh_TW.Big5" to use traditional characters (Big5 encoding)

%description -n locales-zh -l zh_CN
本档包含了中文地方化(localization)的基本档案; 你需要这些档案才能正确的
显示中文的日期。将环境变数 "LANG" 设定为 "zh_CN" 可以显示简体中文(国标
码),设定为 "zh_TW" 则可显示繁体中文(大五码)。 
%description -n locales-zh -l zh_TW
本檔包含了中文地方化(localization)的基本檔案; 你需要這些檔案才能正確的
顯示中文的日期。將環境變數 "LANG" 設定為 "zh_CN" 可以顯示簡體中文(國標
碼),設定為 "zh_TW" 則可顯示繁體中文(大五碼)。 

%files -n locales-zh
%defattr(-,root,root)
/usr/share/locale/zh*

### zu
%package -n locales-zu
Summary: Base files for localization (Zulu)
Group: System/Internationalization
Icon: bulle-zu.xpm
Requires: locales = %{version}-%{release}

%description -n locales-zu
These are the base files for Zulu language localization; you need
it to correctly display 8bits Zulu characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Xhosa language conventions.

%files -n locales-zu
%defattr(-,root,root)
/usr/share/locale/zu*

%changelog
* Tue Sep 02 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.2-5mdk
- fixed yes/no expr for arabic locales
- fixed Yiddish locale 

* Tue Aug 05 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.2-4mdk
- provide 8bit locales for 'he'
- added Kurdish locale
- changes to date format of Chinese locale
- fixed problems with Serbian locale (circular references)

* Fri Jun 27 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.2-3mdk
- updated uz_UZ
- added xh_ZA, zu_ZA, st_ZA, kn_IN, as_IN
- build with zh_HK.gb18030
- fixed mn_MN;

* Mon May 12 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-2mdk
- Rebuild for new glibc and rpm

* Thu Apr  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.2-1mdk
- Rebuild against glibc 2.3.2

* Thu Feb 27 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.4-6mdk
- changed default encoding of 'ta_IN' to UTF-8 (otherwise DrakX is not
  able to display it)

* Wed Feb 26 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.4-5mdk
- corrected charset of 'ru_RU' locale (it used to be iso-8859-5, but
  since we now use 'ru_RU' instead of 'ru' it should be changed to koi8-r).

* Mon Feb 24 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.4-4mdk
- changes in Vietnamese locale as told by the VietLUG
- fixes in Uzbek locale
- changed default font for Tamil in gtk2

* Wed Jan 29 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.4-3mdk
- put back the gtk-2.0 gtkrc file for Tamil, it is no longuer required
  as glibc 2.3 has real tscii support; but there still are several *.po
  files claiming to be latin1; for compatibility and smooth transition
  the file will be kept some more time
- changed some more locales to default to utf-8

* Mon Dec 30 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.4-2mdk
- completed/improved various definition files

* Tue Dec 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1.4-1mdk
- Rebuild against glibc 2.3.1

* Fri Aug 23 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.3-7mdk
- added Malayalam locale
- removed some locales using unused and obsolete encodings
- changed default Tamil font in gtkrc files

* Fri Aug 16 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.3-6mdk
- added Mongolian locale
- corrected use of program without pathname in %%post
- added a gtkrc files for Gtk1 and Gtk2 and tscii

* Thu Aug 08 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.3-5mdk
- come back of the Tamil TSCII support thanks to Thuraiappah Vaseeharan;
  it is still an ugly hack, but now it works ok for Gtk1, Gtk2 and Qt.

* Wed Jul 24 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.3-4mdk
- forced UTF-8 as default for various languages
- put back default for bg to CP1251
- make locales-xx depend on version and release of "locales", so an
  updated of any locales-xx or locales package will update all the others
  even for releases

* Fri Jul 19 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.3-3mdk
- rebuild the locales to ensure defautl charsets are in sync with XFree86

* Thu Jun 04 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.3-2mdk
- made various locales default to utf-8

* Fri Mar 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.3.1.3-1mdk
- Rebuild for new glibc 2.2.5 and corrected some small problems

* Fri Feb 15 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-8mdk
- rebuild to include xx_YY names for all locales, even those uses in only
  one countr (LIN18NUX requires it)

* Mon Feb 11 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-7mdk
- rebuild with corrected Hungarian and Basque data

* Wed Jan 02 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-6mdk
- corrected Hungarian sorting order
- added Bengali (bn_BD) locale
- corrected Albanian sorting order
- non-euro locales for euro-zone countries are obsolete

* Sun Sep 30 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-5mdk
- "it" locale was missing due to a typo...

* Wed Aug 22 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-4mdk
- included a modified ro_RO in src.rpm

* Thu Aug 21 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-3mdk
- xx_YY.ISO-8859-1 where not build correctly for some locales

* Thu Aug 21 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-2mdk
- updated to new glibc & corrected some small problems

* Mon Aug 20 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.2-1mdk
- updated to new glibc

* Wed May 23 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1.1-1mdk
- rebuild for new glibc

* Wed May 23 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-9mdk
- added Inuktitut locale
- fixed LC_CTYPE of Azeri locale (copy "tr_TR")

* Tue Apr 24 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-8mdk
- added GBK and GB18030 chinese locales
- removed no longuer needed netscape_* pseudo-locales
- fixed ru_RU.KOI8-R locale

* Wed Mar 07 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-7mdk
- Added Tamil locale

* Thu Feb 08 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-6mdk
- added new encoding koi8-t
- added locales required for level1 conformance with LI18NUX2000

* Mon Jan 29 2001 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-5mdk
- added Uzbek locale
- fixed LC_COLLATE for Vietnamese
- improved general handling of LC_COLLATE by circumventing a glibc problem
- added Amharic locale

* Thu Dec 07 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-4mdk
- converted descriptions to UTF-8
- included charset encodings pseudo-locales in "locales" package
  and make as many symlinks as possible to them. 
- added special netscape_xx pseudo-locales names for handling
  Netscape problem with displaying in CJK

* Thu Dec 07 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-3mdk
- make it dependent on glibc version
- removed the conversion scripts; now glibc does it for us
- removed KOI8-C encoding file, replaced with CP154 (aka
  CYRILLIC-ASIAN) which is actually used

* Wed Nov 29 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.3.1-2mdk
- added /usr/bin/* to locales package.

* Fri Nov 17 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3.1-1mdk
- converted to new format used by glibc 2.2

* Mon Oct 30 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-11mdk
- corrected LC_COLLATE for Vietnamese
- updated Tatar locale
- switched default charset for Georgian

* Mon Oct 09 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-10mdk
- improved Vietnamese automatic conversion of translations
- added bs locale
- added a %%pre section for locales-gl

* Thu Aug 31 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-9mdk
- corrected charset encoding for Tatar

* Mon Aug 28 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-8mdk
- more aggressive use of hard links
- new Urdu locale
- fixed Swedish LC_COLLATE and added a 'sv@ny' and 'sv@traditional'
- small fixes for Farsi locale
- Added Maori locale
- Added Tamil locale
- Added Hindi locale 
- Added Albanian locale
- Fixed bug with the @euro locales
- Added Azeri locales (both latin & cyrillic)
- Added Tajik locale
- Added Tatar locale

* Mon Jul 03 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-7mdk
- Finnish language default is iso-8859-15
- added mdk_convert_translations script
- make several aliases for Cyrllic locales
- improved Korean locale
- make ASMO-449+ the default for Arabic
- Added Pilipino and Tagalog locales

* Wed Jun 14 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-6mdk
- The armscii-8 standard has been revised; rebuilt Armenian locale to
  reflect it.

* Thu May 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.3-5mdk
- Update bogus-zh.GB2312-english-locale from pablo to compile on alpha.

* Mon May 22 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-4mdk
- Added Belarussian locale
- added cp1251 versions for Russian and Ukrainian locales

* Wed May 03 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-3mdk
- increased release number, to be sure the files will be taken

* Tue Apr 18 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-2mdk
- removed symlinks of chinese locale, they may cause problems
- added Yiddish locale (date format in LC_TIME still needs checking)
- updated several icons (Thanks Helene)

* Fri Mar 17 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 2.3-1mdk
- added Plautdietsch language locale
- corrections to gl_ES
- added Papiamento language (still to be improved)
- rebuild for glibc 2.1.3

* Fri Jan 28 2000 Francis Galiegue <francis@mandrakesoft.com> 2.2-2mdk
- Added %defattr()s

* Fri Jan 03 2000  Pablo Saratxaga <pablo@mandrakesoft.com>
- added Farsi (Iranian) locale.
- little fix to Esperanto locale (monetary & dates)
- corrected Latvian charset
- added first version of Malay locale
- added various languaes descriptions

* Fri Dec 03 1999  Pablo Saratxaga <pablo@mandrakesoft.com>
- fixed cy_GB locale
- added japanese description of locales-ja
- added new af_ZA locale

* Tue Nov 09 1999  Pablo Saratxaga <pablo@mandrakesoft.com>
- fixed the yes/no ukrainian localization

* Sat Nov 06 1999  Pablo Saratxaga <pablo@mandrakesoft.com>
- removed conflicting conflitcs :)

* Fri Oct 29 1999  Pablo Saratxaga <pablo@mandrakesoft.com>
- fixed hebrew descriptions
- fixed XFree86 dependencies (replaced them with conflict with lower versions)

* Fri Oct 08 1999  Pablo Saratxaga <pablo@mandrakesoft.com>
- corrected cy_GB locale
- added locales using iso-8859-14 for celtic languages
- added Bulgarian locale
- another little correction of tcvn-5712

* Fri Sep 17 1999  Pablo Saratxaga <pablo@mandrakesoft.com>
- corrected Lithuanian and Estonian locales to use proper charset
  (iso-8859-13 and iso-8859-15 respectively)
- corrected ru_RU to use koi8-r
- changed directory naming as to be the same than what glibc now uses
- id_ID locale updated from Mohammad DAMT <mdamt@cakraweb.com>

* Thu Aug 26 1999  Pablo Saratxaga <pablo@mandrakesoft.com>
- corrected a little bug
- it seems that localedef doesn't work anymore for eras in LC_CTIME :-(
  I include the precompiled japanese files from previous version

