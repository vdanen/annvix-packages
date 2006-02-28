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

%define glibc_ver	2.3.5
%define glibc_epoch	6

# FIXME: please check on next build those we really need
#%define _unpackaged_files_terminate_build 0

# to define when building for PRC
#%define build_for_PRC 1

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
# this one is on glibc, however there is the politic issue
# of the naming of Taiwan 
Source5:	zh_TW_2
# locales data
Source10:	sw_XX
Source11:	ku_TR
Source12:	eo_XX
Source13:	ky_KG
Source14:	iu_CA
Source15:	fur_IT
Source16:	km_KH
Source17:	ph_PH
Source18:	nds_DE
Source19:	nds_DE@traditional
Source20:	nds_NL
Source21: 	pap_AN
Source22:	as_IN
Source23:	sc_IT
Source24:	li_NL
Source25:	li_BE
Source26:	tk_TM
Source27:	fy_DE
Source28:	fy_NL
Source29:	ik_CA
# Those exist in glibc >= 2.3.2 but the attached ones
# are more correct/more complete
# reordering still doesn't work in glibc 2.3
Source30:	hy_AM
# various spelling fixes
Source31:	yi_US
# changed date format strings
Source34:	zh_CN
# rewritten to take profit of new glibc reordering possibilities
Source41:	es_ES
Source42:	es@tradicional
# LC_COLLATE has one line wrong
Source43:	bs_BA
# those replace respectively sr_YU@cyrillic and sr_YU from glibc
Source44:	http://srpski.org/locale/sr_CS
Source45:	http://srpski.org/locale/sr_CS@Latn
# corrected LC_COLLATE
Source46:	sq_AL
# LC_COLLATE for vietnamese is incorrect in glibc, and LC_CTIME seems
# wrong too... 
Source47:	vi_VN
# fixes in weekday names
Source50:	wa_BE
# tr_TR from glibc has errors in LC_COLLATE
# also, I added recognition of Yy and Nn in yes/noexpr
Source51:	tr_TR
# changed to use tcomma/scomma instead tcedilla/scedilla
Source52:	ro_RO
# ours has yesexpr using tajik
Source53:	tg_TJ
# corrected month names
Source54:	az_AZ
# ethiopic locales (violate ISO-639! not packaged)
Source55:	ad_ET
Source58:	qo_ET
Source59:	sx_ET
Source60:	sz_ET
# version in glibc 2.3.3 has wrong yexexpr/noexpr and wrong LC_COLLATE
Source61:	ar_SA
# version in glibc 2.3.3 has wrong yexexpr/noexpr
Source62:	ar_TN
Source63:	ar_YE
# charset definitions
Source71:	CP1133
Source72:	MULELAO-1
Source76:	CP154
# todo: width field
Source81:	ISO-8859-9E
Source82:	TATAR-CYR
Source85:	KOI8-K

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glibc-i18ndata = %{glibc_epoch}:%{glibc_ver}

Prereq:		glibc = %{glibc_epoch}:%{glibc_ver}
Requires:	glibc = %{glibc_epoch}:%{glibc_ver}
AutoReqProv:	no

%description
These are the base files for language localization.
You also need to install the specific locales-?? for the
language(s) you want. Then the user need to set the
LANG variable to their preferred language in their
~/.profile configuration file.


%prep


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 0755 %{SOURCE2} %{buildroot}%{loc_add}
install -m 0755 %{SOURCE3} %{buildroot}%{loc_del}

#mv /usr/share/locale /usr/share/locale_bak
mkdir -p %{buildroot}/usr/share/locale
LOCALEDIR=%{buildroot}/usr/share/locale

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
	es@tradicional \
	ro_RO 
do
	cp $RPM_SOURCE_DIR/$DEF_CHARSET .
done

# special handling for PRC
%if %build_for_PRC
	cp $RPM_SOURCE_DIR/zh_TW_2 zh_TW
%endif

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
#
# Not yet build, to add later: lug_UG, pap_AN
# uz_UZ is purposedly excluded, as we default to cyrillic now
#
for i in \
	 af_ZA am_ET an_ES as_IN az_AZ be_BY bg_BG bn_BD bn_IN br_FR bs_BA \
	 byn_ER ca_ES cs_CZ cy_GB da_DK el_GR eo_XX et_EE eu_ES fa_IR fi_FI \
	 fo_FO fur_IT fy_DE fy_NL ga_IE gd_GB gl_ES gu_IN gv_GB he_IL hi_IN \
	 hr_HR hu_HU hy_AM id_ID ik_CA is_IS iu_CA ja_JP \
	 ka_GE kl_GL km_KH kn_IN ko_KR ku_TR kw_GB ky_KG \
	 lo_LA lt_LT        lv_LV mi_NZ mk_MK ml_IN mn_MN mr_IN ms_MY \
	 mt_MT nb_NO ne_NP nn_NO oc_FR om_ET om_KE pa_IN        \
	 ph_PH pl_PL ro_RO sc_IT se_NO sh_YU sid_ET sk_SK sl_SI \
	 sq_AL sr_CS st_ZA ta_IN te_IN tg_TJ th_TH ti_ER ti_ET \
	 tig_ER tk_TM tl_PH tr_TR tt_RU uk_UA ur_PK       vi_VN wa_BE xh_ZA \
	 yi_US zh_CN zh_HK zh_SG zh_TW zu_ZA
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
		el*) DEF_CHARSET="ISO-8859-7" ;;
		tr*) DEF_CHARSET="ISO-8859-9" ;;
		lt*|lv*) DEF_CHARSET="ISO-8859-13" ;;
		br*|ca*|da*|de*|et*|eu*|fi*|fo*|fur*|fr*) DEF_CHARSET="ISO-8859-15";;
		ga*|gl*|is*|it*) DEF_CHARSET="ISO-8859-15";;
		nl*|nn*|no*|nb*|oc*|pt*|sc*|sq*|sv*|wa*) DEF_CHARSET="ISO-8859-15";;
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
	[ "$DEF_LANG" != "${LOCALENAME}" -a ! -r "$LOCALEDIR/$DEF_LANG" ] && \
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/$DEF_LANG  || :
	localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME} || :
	[ "$DEF_CHARSET" != "BIG5" -a "$DEF_CHARSET" != "UTF-8" ] && \
	(localedef -c -f $DEF_CHARSET -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME}.`basename ${DEF_CHARSET}` || : )
	localedef -c -f UTF-8 -i $DEF_LOCALE_FILE $LOCALEDIR/${LOCALENAME}.UTF-8 || :
done

# fix for Arabic yes/no expr
for i in /usr/share/i18n/locales/ar_??
do
	if [ ! -r "$RPM_SOURCE_DIR/`basename $i`" ]; then
		cat $i | \
		sed 's/^\(yesexpr.*\)<U0646>/\1<U0646><U0079><U0059>/' | \
		sed 's/^\(noexpr.*\)<U0644>/\1<U0644><U006E><U004E>/' > \
		./`basename $i`
	fi
done

# languages which have several locales
#
# Not build yet, to add later: aa_??* so_??
#
for i in $RPM_SOURCE_DIR/nds_??* $RPM_SOURCE_DIR/li_?? \
	 $RPM_SOURCE_DIR/fy_??   $RPM_SOURCE_DIR/sw_?? \
	                               /usr/share/i18n/locales/ar_?? \
	 /usr/share/i18n/locales/de_?? \
	 /usr/share/i18n/locales/en_?? /usr/share/i18n/locales/es_?? \
	 /usr/share/i18n/locales/fr_?? /usr/share/i18n/locales/gez_??* \
	 /usr/share/i18n/locales/it_?? /usr/share/i18n/locales/nl_?? \
	 /usr/share/i18n/locales/pt_?? /usr/share/i18n/locales/ru_?? \
	 /usr/share/i18n/locales/sv_?? 
do
	DEF_CHARSET="UTF-8"
	# for those languages we still keep a default charset different of UTF-8
	case "`basename $i`" in
		en_IN) DEF_CHARSET="UTF-8" ;;
		en_IE|es_ES) DEF_CHARSET="ISO-8859-15" ;;
		af*|en*|es*) DEF_CHARSET="ISO-8859-1" ;;
		bs*|cs*|hr*|hu*|pl*|ro*|sk*|sl*|sh*) DEF_CHARSET="ISO-8859-2" ;;
		el*) DEF_CHARSET="ISO-8859-7" ;;
		tr*) DEF_CHARSET="ISO-8859-9" ;;
		lt*|lv*) DEF_CHARSET="ISO-8859-13" ;;
		br*|ca*|da*|de*|et*|eu*|fi*|fo*|fr*|ga*|gl*) DEF_CHARSET="ISO-8859-15";;
		is*|it*|nl*|nn*|no*|nb*|oc*|pt*|sq*|sv*|wa*) DEF_CHARSET="ISO-8859-15";;
		fy*|nds*|li*) DEF_CHARSET="ISO-8859-15";;
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
	 gl_ES is_IS it_IT li_NL nds_DE nl_NL pt_PT wa_BE
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
#localedef -c -f ISO-8859-1  -i $RPM_SOURCE_DIR/nds_DE $LOCALEDIR/nds || :
localedef -c -f ISO-8859-15 -i ./es@tradicional $LOCALEDIR/es@tradicional || :

#=========================================================
#
# special non-UTF-8 locales for compatibility
#

# Azeri -- for old compatibility
localedef -c -f ISO-8859-9E -i az_AZ $LOCALEDIR/az_AZ.ISO-8859-9E || :

# Bielorussian
localedef -c -f CP1251     -i be_BY $LOCALEDIR/be || :
localedef -c -f CP1251     -i be_BY $LOCALEDIR/be_BY || :
localedef -c -f ISO-8859-5 -i be_BY $LOCALEDIR/be_BY.ISO-8859-5 || :

# Esperanto
localedef -c -f ISO-8859-3 -i eo_XX $LOCALEDIR/eo_XX.ISO-8859-3 || :

# estonian can use iso-8859-15 and iso-8859-4
localedef -c -f ISO-8859-15 -i et_EE $LOCALEDIR/et || :
localedef -c -f ISO-8859-15 -i et_EE $LOCALEDIR/et_EE || :
localedef -c -f ISO-8859-4  -i et_EE $LOCALEDIR/et_EE.ISO-8859-4 || :
localedef -c -f ISO-8859-13 -i et_EE $LOCALEDIR/et_EE.ISO-8859-13 || :

# Finnish default must be iso8859-15
localedef -c -f ISO-8859-1  -i fi_FI $LOCALEDIR/fi_FI.ISO-8859-1 || :

# Hebrew -- for old compatibility and for use with Wine
localedef -c -f ISO-8859-8 -i he_IL $LOCALEDIR/he_IL.ISO-8859-8 || :
localedef -c -f CP1255     -i he_IL $LOCALEDIR/he_IL.CP1255 || :

# Armenian -- for old compatibility
localedef -c -f ARMSCII-8 -i hy_AM $LOCALEDIR/hy_AM.ARMSCII-8 || :

# georgian -- for old compatibility
localedef -c -f GEORGIAN-ACADEMY -i ka_GE $LOCALEDIR/ka_GE.GEORGIAN-ACADEMY || :
localedef -c -f GEORGIAN-PS      -i ka_GE $LOCALEDIR/ka_GE.GEORGIAN-PS || :

# Kurdish 
localedef -c -f ISO-8859-9 -i ku_TR $LOCALEDIR/ku_TR.ISO-8859-9 || :

# Luganda (Ganda)
# "lug" in glibc locale; but it has an iso 639 two letter code: lg
localedef -c -f UTF-8 -i lug_UG $LOCALEDIR/lg || :
localedef -c -f UTF-8 -i lug_UG $LOCALEDIR/lg_UG || :
localedef -c -f UTF-8 -i lug_UG $LOCALEDIR/lg_UG.UTF-8 || :

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

# Maltese -- for old compatibility
localedef -c -f ISO-8859-3 -i mt_MT $LOCALEDIR/mt_MT.ISO-8859-3 || :

# Norwegian bokmål -- for old compatibility
localedef -c -f ISO-8859-15 -i nb_NO $LOCALEDIR/no || :
localedef -c -f ISO-8859-15 -i nb_NO $LOCALEDIR/no_NO || :
localedef -c -f ISO-8859-1  -i nb_NO $LOCALEDIR/no_NO.ISO-8859-1 || :
localedef -c -f ISO-8859-15 -i nb_NO $LOCALEDIR/no_NO.ISO-8859-15 || :
localedef -c -f UTF-8       -i nb_NO $LOCALEDIR/no_NO.UTF-8 || : 

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

# Albanian
localedef -c -f ISO-8859-1 -i sq_AL $LOCALEDIR/sq_AL.ISO-8859-1 || :
localedef -c -f ISO-8859-2 -i sq_AL $LOCALEDIR/sq_AL.ISO-8859-2 || :

# Serbian
localedef -c -f ISO-8859-5  -i sr_CS $LOCALEDIR/sr_CS.ISO-8859-5 || :
localedef -c -f CP1252      -i sr_CS $LOCALEDIR/sr_CS.CP1251 || :
cp $RPM_SOURCE_DIR/sr_CS@Latn .
if [ -r "sr_CS@Latn" ]; then
localedef -c -f UTF-8 -i ./sr_CS@Latn $LOCALEDIR/sr@Latn || :
localedef -c -f UTF-8 -i ./sr_CS@Latn $LOCALEDIR/sr_CS@Latn || :
localedef -c -f UTF-8 -i ./sr_CS@Latn $LOCALEDIR/sr_CS.UTF-8@Latn || :
localedef -c -f ISO-8859-2 -i ./sr_CS@Latn $LOCALEDIR/sr_CS.ISO-8859-2@Latn || :
fi
# for old compatibility
if [ -r "sr_CS" ]; then
localedef -c -f UTF-8      -i ./sr_CS $LOCALEDIR/sr_YU || :
localedef -c -f ISO-8859-5 -i ./sr_CS $LOCALEDIR/sr_YU.ISO-8859-5 || :
localedef -c -f CP1251     -i ./sr_CS $LOCALEDIR/sr_YU.CP1251 || :
localedef -c -f UTF-8      -i ./sr_CS $LOCALEDIR/sr_YU.UTF-8 || :
fi
if [ -r "sr_CS@Latn" ]; then
localedef -c -f UTF-8      -i ./sr_CS@Latn $LOCALEDIR/sr_YU@Latn || :
localedef -c -f ISO-8859-2 -i ./sr_CS@Latn $LOCALEDIR/sr_YU.ISO-8859-2@Latn ||
localedef -c -f UTF-8      -i ./sr_CS@Latn $LOCALEDIR/sr_YU.UTF-8@Latn || :
fi

# Turkmen
localedef -c -f ISO-8859-2 -i tk_TM $LOCALEDIR/tk_TM.ISO-8859-2 || :

# Provide cp1251 for Ukrainian too...
localedef -c -f CP1251     -i uk_UA $LOCALEDIR/uk_UA.CP1251 || :

# Uzbek
[ -r /usr/share/i18n/locales/uz_UZ ] && \
	cp /usr/share/i18n/locales/uz_UZ uz_UZ@Latn
[ -r /usr/share/i18n/locales/uz_UZ@Latn ] && \
	cp -f /usr/share/i18n/locales/uz_UZ@Latn uz_UZ@Latn
if [ -r "uz_UZ@Latn" ]; then
localedef -c -f ISO-8859-1  -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ.ISO-8859-1 || :
localedef -c -f ISO-8859-9  -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ.ISO-8859-9 || :
localedef -c -f UTF-8       -i ./uz_UZ@Latn $LOCALEDIR/uz@Latn || :
localedef -c -f UTF-8       -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ@Latn || :
localedef -c -f UTF-8       -i ./uz_UZ@Latn $LOCALEDIR/uz_UZ.UTF-8@Latn || :
fi
[ -r /usr/share/i18n/locales/uz_UZ@cyrillic ] && \
	cp /usr/share/i18n/locales/uz_UZ@cyrillic uz_UZ@Cyrl
[ -r /usr/share/i18n/locales/uz_UZ@Cyrl ] && \
	cp /usr/share/i18n/locales/uz_UZ@Cyrl uz_UZ@Cyrl
if [ -r "uz_UZ@Cyrl" ]; then
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ.UTF-8 || :
# for compatibility
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz@Cyrl || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ@Cyrl || :
localedef -c -f UTF-8 -i ./uz_UZ@Cyrl $LOCALEDIR/uz_UZ.UTF-8@Cyrl || :
fi

# Vietnamese -- for old compatibility
localedef -c -f VISCII     -i vi_VN $LOCALEDIR/vi_VN.VISCII || :
localedef -c -f TCVN5712-1 -i vi_VN $LOCALEDIR/vi_VN.TCVN || :
localedef -c -f TCVN5712-1 -i vi_VN $LOCALEDIR/vi_VN.TCVN-5712 || :


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
(
 cd %{buildroot}/usr/share/locale ;
 for i in \
	af am ar as az be bg bn br bs ca cs cy da de el en eo es et eu \
	fa fi fo fr fy ga gd gl gu gv he hi hr hu hy id ik is it iu ja \
	ka kl kn ko ku kw ky lg li lo lt lv mi mk ml mn mr ms mt \
	nb nds ne nl no oc pa pap ph pl pt ro ru se sk sl sq sr st sv \
	ta te tg th ti tk tr tt tig uk ur uz vi wa xh yi zh zu \
	tl sp gez 
 do
	LC_ALL=C %{_builddir}/locales-%{version}/softlink.pl $i
 done
)

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


%files
%defattr(-,root,root)
%dir /usr/share/locale
/usr/share/locale/ISO*
/usr/share/locale/CP*
/usr/share/locale/UTF*
/usr/share/locale/KOI*
/usr/bin/*



####################################################################
# The various localization packages.
#
# add one for each new language that is included in the future
####################################################################

### aa
%package -n locales-aa
Summary:	Base files for localization (Afar)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-aa
These are the base files for Afar language localization; you need
it to correctly display 8bits Afar characters, and for proper
alfabetical sorting and representation of dates and numbers according
to Afar language conventions.

%post -n locales-aa
if [ "$1" = "1" ]; then
	%{loc_add} aa
fi
%postun -n locales-aa
if [ "$1" = "0" ]; then
	%{loc_del} aa
fi

#%files -n locales-aa
#%defattr(-,root,root)
#/usr/share/locale/aa*

### af
# translation by Schalk Cronje <schalkc@ntaba.co.za>
%package -n locales-af
Summary:	Base files for localization (Afrikaans)
Group:		System/Internationalization
URL:		http://www.af.org.za/aflaai/linux-i18n/
Requires:	locales = %{version}-%{release}

%description -n locales-af
These are the base files for Afrikaans language localization; you need
it to correctly display 8bits Afrikaans characters, and for proper
alfabetical sorting and representation of dates and numbers according
to Afrikaans language conventions.

%post -n locales-af
if [ "$1" = "1" ]; then
	%{loc_add} af
fi
%postun -n locales-af
if [ "$1" = "0" ]; then
	%{loc_del} af
fi

%files -n locales-af
%defattr(-,root,root)
/usr/share/locale/af*

### am
# translation by Daniel Yacob <Yacob@EthiopiaOnline.Net>
%package -n locales-am
Summary:	Base files for localization (Amharic)
Group:		System/Internationalization
URL:		http://www.ethiopic.org/
Requires:	locales = %{version}-%{release}
Provides:	locales-byn, locales-gez, locales-sid, locales-ti, locales-tig, locales-om

%description -n locales-am
These are the base files for Amharic language localization; you need
it to correctly display 8bits Amharic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Amharic language conventions.

%post -n locales-am
if [ "$1" = "1" ]; then
	%{loc_add} am byn ti gez sid tig om
fi
%postun -n locales-am
if [ "$1" = "0" ]; then
	%{loc_del} am byn ti gez sid tig om
fi

%files -n locales-am
%defattr(-,root,root)
/usr/share/locale/am*
# blin
/usr/share/locale/byn
# tigrinya
/usr/share/locale/ti
/usr/share/locale/ti_*
# ge'ez
/usr/share/locale/gez*
# sidama
/usr/share/locale/sid*
# tigre
/usr/share/locale/tig*
# Oromo
/usr/share/locale/om*

### ar
# translation by Wajdi Al-Jedaibi <wajdi@acm.org>
%package -n locales-ar
Summary:	Base files for localization (Arabic)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ar
These are the base files for Arabic language localization; you need
it to correctly display 8bits arabic characters, and for proper
alfabetical sorting and representation of dates and numbers according
to arabic language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%post -n locales-ar
if [ "$1" = "1" ]; then
	%{loc_add} ar
fi
%postun -n locales-ar
if [ "$1" = "0" ]; then
	%{loc_del} ar
fi

%files -n locales-ar
%defattr(-,root,root)
/usr/share/locale/ar*

### as
%package -n locales-as
Summary:	Base files for localization (Assamese)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-as
These are the base files for Assamese language localization; you need
it to correctly display 8bits Assamese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Assamese language conventions.

%post -n locales-as
if [ "$1" = "1" ]; then
	%{loc_add} as
fi
%postun -n locales-as
if [ "$1" = "0" ]; then
	%{loc_del} as
fi

%files -n locales-as
%defattr(-,root,root)
/usr/share/locale/as*

### az
%package -n locales-az
Summary:	Base files for localization (Azeri)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-az
These are the base files for Azeri language localization; you need
it to correctly display 8bits Azeri characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Azeri language conventions.

%post -n locales-az
if [ "$1" = "1" ]; then
	%{loc_add} az
fi
%postun -n locales-az
if [ "$1" = "0" ]; then
	%{loc_del} az
fi

%files -n locales-az
%defattr(-,root,root)
/usr/share/locale/az*

### be
%package -n locales-be
Summary:	Base files for localization (Belarussian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-be
These are the base files for Belarussian language localization; you need
it to correctly display 8bits Belarussian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Belarussian language conventions.

%post -n locales-be
if [ "$1" = "1" ]; then
	%{loc_add} be
fi
%postun -n locales-be
if [ "$1" = "0" ]; then
	%{loc_del} be
fi

%files -n locales-be
%defattr(-,root,root)
# not just be* because of ber
/usr/share/locale/be
/usr/share/locale/be_*

### bg
# translation: Mariana Kokosharova <kokosharova@dir.bg>
%package -n locales-bg
Summary:	Base files for localization (Bulgarian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-bg
These are the base files for Bulgarian language localization; you need
it to correctly display 8bits Bulgarian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bulgarian language conventions.

%post -n locales-bg
if [ "$1" = "1" ]; then
	%{loc_add} bg
fi
%postun -n locales-bg
if [ "$1" = "0" ]; then
	%{loc_del} bg
fi

%files -n locales-bg
%defattr(-,root,root)
/usr/share/locale/bg*

### bn
%package -n locales-bn
Summary:	Base files for localization (Bengali)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-bn
These are the base files for Bengali language localization; you need
it to correctly display 8bits Bengali characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bengali language conventions.

%post -n locales-bn
if [ "$1" = "1" ]; then
	%{loc_add} bn
fi
%postun -n locales-bn
if [ "$1" = "0" ]; then
	%{loc_del} bn
fi

%files -n locales-bn
%defattr(-,root,root)
/usr/share/locale/bn*

### br
# Translation by Jañ-Mai Drapier (jan-mai-drapier@mail.dotcom.fr)
%package -n locales-br
Summary:	Base files for localization (Breton)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-br
These are the base files for Breton language localization; you need
it to correctly display 8bits Breton characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Breton language conventions.

%post -n locales-br
if [ "$1" = "1" ]; then
	%{loc_add} br
fi
%postun -n locales-br
if [ "$1" = "0" ]; then
	%{loc_del} br
fi

%files -n locales-br
%defattr(-,root,root)
/usr/share/locale/br*

### bs
%package -n locales-bs
Summary:	Base files for localization (Bosnian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-bs
These are the base files for Bosnian language localization; you need
it to correctly display 8bits Bosnian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Bosnian language conventions.

%post -n locales-bs
if [ "$1" = "1" ]; then
	%{loc_add} bs
fi
%postun -n locales-bs
if [ "$1" = "0" ]; then
	%{loc_del} bs
fi

%files -n locales-bs
%defattr(-,root,root)
/usr/share/locale/bs*

### ca
%package -n locales-ca
Summary:	Base files for localization (Catalan)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ca
These are the base files for Catalan language localization; you need
it to correctly display 8bits Catalan characters, and for proper
representation of dates, numbers and alphabetical order according to
Catalan language conventions

%post -n locales-ca
if [ "$1" = "1" ]; then
	%{loc_add} ca
fi
%postun -n locales-ca
if [ "$1" = "0" ]; then
	%{loc_del} ca
fi

%files -n locales-ca
%defattr(-,root,root)
/usr/share/locale/ca*

### cs
# translation by <pavel@SnowWhite.inet.cz>
%package -n locales-cs
Summary:	Base files for localization (Czech)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-cs
These are the base files for Czech language localization; you need
it to correctly display 8bits Czech characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Czech language conventions.

%post -n locales-cs
if [ "$1" = "1" ]; then
	%{loc_add} cs
fi
%postun -n locales-cs
if [ "$1" = "0" ]; then
	%{loc_del} cs
fi

%files -n locales-cs
%defattr(-,root,root)
/usr/share/locale/cs*

### cy
%package -n locales-cy
Summary:	Base files for localization (Welsh)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-cy
These are the base files for Welsh language localization; you need
it to correctly display 8bits Welsh characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Welsh language conventions.

%post -n locales-cy
if [ "$1" = "1" ]; then
	%{loc_add} cy
fi
%postun -n locales-cy
if [ "$1" = "0" ]; then
	%{loc_del} cy
fi

%files -n locales-cy
%defattr(-,root,root)
/usr/share/locale/cy*

### da
# danish translation by Erik Martino <martino@daimi.au.dk>
%package -n locales-da
Summary:	Base files for localization (Danish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-da
These are the base files for Danish language localization; you need
it to correctly display 8bits Danish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Danish language conventions.

%post -n locales-da
if [ "$1" = "1" ]; then
	%{loc_add} da
fi
%postun -n locales-da
if [ "$1" = "0" ]; then
	%{loc_del} da
fi

%files -n locales-da
%defattr(-,root,root)
/usr/share/locale/da*

### de
%package -n locales-de
Summary:	Base files for localization (German)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-de
These are the base files for German language localization; you need
it to correctly display 8bits German characters, and for proper
alphabetical sorting and representation of dates and numbers according
to German language conventions.

%post -n locales-de
if [ "$1" = "1" ]; then
	%{loc_add} de
fi
%postun -n locales-de
if [ "$1" = "0" ]; then
	%{loc_del} de
fi

%files -n locales-de
%defattr(-,root,root)
/usr/share/locale/de*

### el
# translations from "Theodore J. Soldatos" <theodore@eexi.gr>
%package -n locales-el
Summary:	Base files for localization (Greek)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Obsoletes:	locales-gr
Provides:	locales-gr

%description -n locales-el
These are the base files for Greek language localization; you need
it to correctly display 8bits Greek characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Greek language conventions.

%post -n locales-el
if [ "$1" = "1" ]; then
	%{loc_add} el
fi
%postun -n locales-el
if [ "$1" = "0" ]; then
	%{loc_del} el
fi

%files -n locales-el
%defattr(-,root,root)
/usr/share/locale/el*

### en
%package -n locales-en
Summary:	Base files for localization (English)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-en
These are the base files for English language localization.
Contains: en_CA en_DK en_GB en_IE en_US

%post -n locales-en
if [ "$1" = "1" ]; then
	%{loc_add} en en_GB en_IE en_US
fi
%postun -n locales-en
if [ "$1" = "0" ]; then
	%{loc_del} en en_GB en_IE en_US
fi

%files -n locales-en
%defattr(-,root,root)
/usr/share/locale/en*

### eo
# translation by diestel@rzaix340.rz.uni-leipzig.de (Wolfram Diestel)
%package -n locales-eo
Summary:	Base files for localization (Esperanto)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-eo
These are the base files for Esperanto language localization; you need
it to correctly display 8bits esperanto characters, and for proper
alphabetical sorting and representation of dates and numbers according
to esperanto language conventions.

%post -n locales-eo
if [ "$1" = "1" ]; then
	%{loc_add} eo
fi
%postun -n locales-eo
if [ "$1" = "0" ]; then
	%{loc_del} eo
fi

%files -n locales-eo
%defattr(-,root,root)
/usr/share/locale/eo*

### es
%package -n locales-es
Summary:	Base files for localization (Spanish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Provides:	locales-an

%description -n locales-es
These are the base files for Spanish language localization; you need
it to correctly display 8bits spanish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to spanish language conventions.

%post -n locales-es
if [ "$1" = "1" ]; then
	%{loc_add} es an
fi
%postun -n locales-es
if [ "$1" = "0" ]; then
	%{loc_del} es an
fi

%files -n locales-es
%defattr(-,root,root)
/usr/share/locale/es*
# Aragonese
/usr/share/locale/an*

### et
# translation from: Ekke Einberg <ekke@data.ee>
%package -n locales-et
Summary:	Base files for localization (Estonian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-et
These are the base files for Estonian language localization; you need
it to correctly display 8bits Estonian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Estonian language conventions.

%post -n locales-et
if [ "$1" = "1" ]; then
	%{loc_add} et
fi
%postun -n locales-et
if [ "$1" = "0" ]; then
	%{loc_del} et
fi

%files -n locales-et
%defattr(-,root,root)
/usr/share/locale/et*

### eu
%package -n locales-eu
Summary:	Base files for localization (Basque)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-eu
Linux-ek euskaraz badaki !
These are the base files for Basque language localization; you need
it to correctly display 8bits Basque characters, and for proper
representation of dates and numbers according to Basque language
conventions.

%post -n locales-eu
if [ "$1" = "1" ]; then
	%{loc_add} eu
fi
%postun -n locales-eu
if [ "$1" = "0" ]; then
	%{loc_del} eu
fi

%files -n locales-eu
%defattr(-,root,root)
/usr/share/locale/eu*

### fa
%package -n locales-fa
Summary:	Base files for localization (Farsi)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-fa
These are the base files for Farsi language localization; you need
it to correctly display 8bits Farsi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Farsi language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%post -n locales-fa
if [ "$1" = "1" ]; then
	%{loc_add} fa
fi
%postun -n locales-fa
if [ "$1" = "0" ]; then
	%{loc_del} fa
fi

%files -n locales-fa
%defattr(-,root,root)
/usr/share/locale/fa*

### fi
# translations by Jarkko Vaaraniemi <jvaarani@ees2.oulu.fi>
%package -n locales-fi
Summary:	Base files for localization (Finnish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-fi
These are the base files for Finnish language localization; you need
it to correctly display 8bits Finnish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Finnish language conventions.

%post -n locales-fi
if [ "$1" = "1" ]; then
	%{loc_add} fi
fi
%postun -n locales-fi
if [ "$1" = "0" ]; then
	%{loc_del} fi
fi

%files -n locales-fi
%defattr(-,root,root)
/usr/share/locale/fi*

### fo
%package -n locales-fo
Summary:	Base files for localization (Faroese)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-fo
These are the base files for Faroese language localization; you need
it to correctly display 8bits Faroese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Faroese language conventions.

%post -n locales-fo
if [ "$1" = "1" ]; then
	%{loc_add} fo
fi
%postun -n locales-fo
if [ "$1" = "0" ]; then
	%{loc_del} fo
fi

%files -n locales-fo
%defattr(-,root,root)
/usr/share/locale/fo*

### fr
%package -n locales-fr
Summary:	Base files for localization (French)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-fr
These are the base files for French language localization; you need
it to correctly display 8bits french characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to french language conventions.

%post -n locales-fr
if [ "$1" = "1" ]; then
	%{loc_add} fr
fi
%postun -n locales-fr
if [ "$1" = "0" ]; then
	%{loc_del} fr
fi

%files -n locales-fr
%defattr(-,root,root)
/usr/share/locale/fr*

### fur
%package -n locales-fur
Summary:	Base files for localization (Friulan)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-fur
These are the base files for Friulan language localization; you need
it to correctly display 8bits friulan characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to friulan language conventions.

%post -n locales-fur
if [ "$1" = "1" ]; then
	%{loc_add} fur
fi
%postun -n locales-fur
if [ "$1" = "0" ]; then
	%{loc_del} fur
fi

%files -n locales-fur
%defattr(-,root,root)
/usr/share/locale/fur*

### fy
%package -n locales-fy
Summary:	Base files for localization (Frisian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-fy
These are the base files for Frisian language localization; you need
it to correctly display 8bits frisian characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to frisian language conventions.

%post -n locales-fy
if [ "$1" = "1" ]; then
	%{loc_add} fy
fi
%postun -n locales-fy
if [ "$1" = "0" ]; then
	%{loc_del} fy
fi

%files -n locales-fy
%defattr(-,root,root)
/usr/share/locale/fy*

### ga
%package -n locales-ga
Summary:	Base files for localization (Irish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ga
These are the base files for Irish Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%post -n locales-ga
if [ "$1" = "1" ]; then
	%{loc_add} ga
fi
%postun -n locales-ga
if [ "$1" = "0" ]; then
	%{loc_del} ga
fi

%files -n locales-ga
%defattr(-,root,root)
/usr/share/locale/ga*

### gd
# translation by Caoimhin O Donnaile [caoimhin@SMO.UHI.AC.UK]
# and Cecil Ward [cecil.ward@FREE4ALL.CO.UK]
%package -n locales-gd
Summary:	Base files for localization (Scottish Gaelic)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-gd
These are the base files for Scottish Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%post -n locales-gd
if [ "$1" = "1" ]; then
	%{loc_add} gd
fi
%postun -n locales-gd
if [ "$1" = "0" ]; then
	%{loc_del} gd
fi

%files -n locales-gd
%defattr(-,root,root)
/usr/share/locale/gd*

### gl
# translation from Emilio <nigrann@sandra.ctv.es>
%package -n locales-gl
Summary:	Base files for localization (Galician)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-gl
These are the base files for Galician language localization; you need
it to correctly display 8bits Galician characters, and for proper
representation of dates and numbers according to Galician language
conventions.

%post -n locales-gl
if [ "$1" = "1" ]; then
	%{loc_add} gl
fi
%postun -n locales-gl
if [ "$1" = "0" ]; then
	%{loc_del} gl
fi

%files -n locales-gl
%defattr(-,root,root)
/usr/share/locale/gl*

### gu
%package -n locales-gu
Summary:	Base files for localization (Gujarati)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-gu
These are the base files for Gujarati language localization; you need
it to correctly display 8bits gujarati characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%post -n locales-gu
if [ "$1" = "1" ]; then
	%{loc_add} gu
fi
%postun -n locales-gu
if [ "$1" = "0" ]; then
	%{loc_del} gu
fi

%files -n locales-gu
%defattr(-,root,root)
/usr/share/locale/gu*

### gv
# translation by Brian Stowell <bstowell@MAILSERVICE.MCB.NET>
%package -n locales-gv
Summary:	Base files for localization (Manx Gaelic)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-gv
These are the base files for Manx Gaelic language localization; you need
it to correctly display 8bits gaelic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to gaelic language conventions.

%post -n locales-gv
if [ "$1" = "1" ]; then
	%{loc_add} gv
fi
%postun -n locales-gv
if [ "$1" = "0" ]; then
	%{loc_del} gv
fi

%files -n locales-gv
%defattr(-,root,root)
/usr/share/locale/gv*

### he (formerly iw)
%package -n locales-he
Summary:	Base files for localization (Hebrew)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-he
These are the base files for Hebrew language localization; you need
it to correctly display 8bits Hebrew characters, and for proper
alfabetical sorting, and representation of dates and numbers 
according to Hebrew language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying; it is to the xterm, application or virtual
console driver to do that.

%post -n locales-he
if [ "$1" = "1" ]; then
	%{loc_add} he
fi
%postun -n locales-he
if [ "$1" = "0" ]; then
	%{loc_del} he
fi

%files -n locales-he
%defattr(-,root,root)
/usr/share/locale/he*

### hi
%package -n locales-hi
Summary:	Base files for localization (Hindi)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-hi
These are the base files for Hindi language localization; you need
it to correctly display 8bits Hindi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Hindi language conventions.

%post -n locales-hi
if [ "$1" = "1" ]; then
	%{loc_add} hi
fi
%postun -n locales-hi
if [ "$1" = "0" ]; then
	%{loc_del} hi
fi

%files -n locales-hi
%defattr(-,root,root)
/usr/share/locale/hi*

### hr
# translations by Vedran Rodic <vrodic@udig.hr>
%package -n locales-hr
Summary:	Base files for localization (Croatian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-hr
These are the base files for Croatian language localization; you need
it to correctly display 8bits Croatian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Croatian language conventions.

%post -n locales-hr
if [ "$1" = "1" ]; then
	%{loc_add} hr
fi
%postun -n locales-hr
if [ "$1" = "0" ]; then
	%{loc_del} hr
fi

%files -n locales-hr
%defattr(-,root,root)
/usr/share/locale/hr*

### hu
%package -n locales-hu
Summary:	Base files for localization (Hungarian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-hu
These are the base files for Hungarian language localization.
You need it to correctly display sort, for sorting order and
proper representation of dates and numbers according 
to Hungarian language conventions.

%post -n locales-hu
if [ "$1" = "1" ]; then
	%{loc_add} hu
fi
%postun -n locales-hu
if [ "$1" = "0" ]; then
	%{loc_del} hu
fi

%files -n locales-hu
%defattr(-,root,root)
/usr/share/locale/hu*

### hy
# translations by Eugene Sevinian <sevinian@crdlx2.yerphi.am>
%package -n locales-hy
Summary:	Base files for localization (Armenian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-hy
These are the base files for Armenian language localization.
You need it to correctly display 8bit Armenian chars, 
for sorting order and proper representation of dates and
numbers according to Armenian language conventions.

%post -n locales-hy
if [ "$1" = "1" ]; then
	%{loc_add} hy
fi
%postun -n locales-hy
if [ "$1" = "0" ]; then
	%{loc_del} hy
fi

%files -n locales-hy
%defattr(-,root,root)
/usr/share/locale/hy*

### id (formerly in)
# translations by Mohammad DAMT <mdamt@cakraweb.com>
%package -n locales-id
Summary:	Base files for localization (Indonesian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-id
These are the base files for Indonesian language localization.
You need it to correctly display sort, for proper representation
of dates and numbers according to Indonesian language conventions.

%post -n locales-id
if [ "$1" = "1" ]; then
	%{loc_add} id
fi
%postun -n locales-id
if [ "$1" = "0" ]; then
	%{loc_del} id
fi

%files -n locales-id
%defattr(-,root,root)
/usr/share/locale/id*

### ik
%package -n locales-ik
Summary:	Base files for localization (Inupiaq)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ik
These are the base files for Inupiaq language localization; you need
it to correctly display 8bits Inupiac characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Inupiaq language conventions.

%post -n locales-ik
if [ "$1" = "1" ]; then
	%{loc_add} ik
fi
%postun -n locales-ik
if [ "$1" = "0" ]; then
	%{loc_del} ik
fi

%files -n locales-ik
%defattr(-,root,root)
/usr/share/locale/ik*

### is
# Gudmundur Erlingsson <gudmuner@lexis.hi.is>
%package -n locales-is
Summary:	Base files for localization (Icelandic)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-is
These are the base files for Icelandic language localization; you need
it to correctly display 8bits Icelandic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Icelandic language conventions.

%post -n locales-is
if [ "$1" = "1" ]; then
	%{loc_add} is
fi
%postun -n locales-is
if [ "$1" = "0" ]; then
	%{loc_del} is
fi

%files -n locales-is
%defattr(-,root,root)
# I can't use /usr/share/locale/is* because of /usr/share/locale/iso_8859_1
/usr/share/locale/is
/usr/share/locale/is_*

### it
%package -n locales-it
Summary:	Base files for localization (Italian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-it
These are the base files for Italian language localization; you need
it to correctly display 8bits Italian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Italian language conventions.

%post -n locales-it
if [ "$1" = "1" ]; then
	%{loc_add} it
fi
%postun -n locales-it
if [ "$1" = "0" ]; then
	%{loc_del} it
fi

%files -n locales-it
%defattr(-,root,root)
/usr/share/locale/it*

### iu
%package -n locales-iu
Summary:	Base files for localization (Inuktitut)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-iu
These are the base files for Inuktitut language localization; you need
it to correctly display 8bits Inuktitut characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Inuktitut language conventions.

%post -n locales-iu
if [ "$1" = "1" ]; then
	%{loc_add} iu
fi
%postun -n locales-iu
if [ "$1" = "0" ]; then
	%{loc_del} iu
fi

%files -n locales-iu
%defattr(-,root,root)
/usr/share/locale/iu*

### ja
# translation by "Evan D.A. Geisinger" <evan.geisinger@etak.com>
%package -n locales-ja
Summary:	Base files for localization (Japanese)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Obsoletes:	libwcsmbs

%description -n locales-ja
These are the base files for Japanese language localization; you need
it to correctly display 8bits and 7bits japanese codes, and for proper
representation of dates and numbers according to japanese language conventions.

%post -n locales-ja
if [ "$1" = "1" ]; then
	%{loc_add} ja
fi
%postun -n locales-ja
if [ "$1" = "0" ]; then
	%{loc_del} ja
fi

%files -n locales-ja
%defattr(-,root,root)
/usr/share/locale/ja*

### ka
%package -n locales-ka
Summary:	Base files for localization (Georgian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ka
These are the base files for Georgian language localization; you need
it to correctly display 8bits Georgian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Georgian language conventions.

%post -n locales-ka
if [ "$1" = "1" ]; then
	%{loc_add} ka
fi
%postun -n locales-ka
if [ "$1" = "0" ]; then
	%{loc_del} ka
fi

%files -n locales-ka
%defattr(-,root,root)
/usr/share/locale/ka*

### kl
%package -n locales-kl
Summary:	Base files for localization (Greenlandic)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-kl
These are the base files for Greenlandic language localization; you need
it to correctly display 8bits Greenlandic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Grenlandic language conventions.

%post -n locales-kl
if [ "$1" = "1" ]; then
	%{loc_add} kl
fi
%postun -n locales-kl
if [ "$1" = "0" ]; then
	%{loc_del} kl
fi

%files -n locales-kl
%defattr(-,root,root)
/usr/share/locale/kl*

### km
%package -n locales-km
Summary:	Base files for localization (Khmer)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-km
These are the base files for Khmer language localization; you need
it to correctly display 8bits Khmer characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Khmer language conventions.

%post -n locales-km
if [ "$1" = "1" ]; then
	%{loc_add} km
fi
%postun -n locales-km
if [ "$1" = "0" ]; then
	%{loc_del} km
fi

%files -n locales-km
%defattr(-,root,root)
/usr/share/locale/km*

### kn
%package -n locales-kn
Summary:	Base files for localization (Kannada)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-kn
These are the base files for Kannada language localization; you need
it to correctly display 8bits Kannada characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kannada language conventions.

%post -n locales-kn
if [ "$1" = "1" ]; then
	%{loc_add} kn
fi
%postun -n locales-kn
if [ "$1" = "0" ]; then
	%{loc_del} kn
fi

%files -n locales-kn
%defattr(-,root,root)
/usr/share/locale/kn*

### ko
# translation by Soo-Jin Lee <NothingSpecial@rocketmail.com>
%package -n locales-ko
Summary:	Base files for localization (Korean)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Obsoletes:	libwcsmbs

%description -n locales-ko
These are the base files for Korean language localization; you need
it to correctly display 8bits and 7bits japanese codes, and for proper
representation of dates and numbers according to korean language conventions.

%post -n locales-ko
if [ "$1" = "1" ]; then
	%{loc_add} ko
fi
%postun -n locales-ko
if [ "$1" = "0" ]; then
	%{loc_del} ko
fi

%files -n locales-ko
%defattr(-,root,root)
/usr/share/locale/ko*

### ku
%package -n locales-ku
Summary:	Base files for localization (Kurdish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ku
These are the base files for Kurdish language localization; you need
it to correctly display 8bits Kurdish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kurdish language conventions.

%post -n locales-ku
if [ "$1" = "1" ]; then
	%{loc_add} ku
fi
%postun -n locales-ku
if [ "$1" = "0" ]; then
	%{loc_del} ku
fi

%files -n locales-ku
%defattr(-,root,root)
/usr/share/locale/ku*

### kw
# translations by Andrew Climo-Thompson <andrew@clas.demon.co.uk>
# Laurie Climo <lj.climo@ukonline.co.uk> & Marion Gunn <mgunn@ucd.ie>
%package -n locales-kw
Summary:	Base files for localization (Cornish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-kw
These are the base files for Cornish language localization; you need
it to correctly display 8bits cornish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Cornish language conventions.

%post -n locales-kw
if [ "$1" = "1" ]; then
	%{loc_add} kw
fi
%postun -n locales-kw
if [ "$1" = "0" ]; then
	%{loc_del} kw
fi

%files -n locales-kw
%defattr(-,root,root)
/usr/share/locale/kw*

### ky
%package -n locales-ky
Summary:	Base files for localization (Kyrgyz)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ky
These are the base files for Kyrgyz language localization; you need
it to correctly display 8bits kyrgyz characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Kyrgyz language conventions.

%post -n locales-ky
if [ "$1" = "1" ]; then
	%{loc_add} ky
fi
%postun -n locales-ky
if [ "$1" = "0" ]; then
	%{loc_del} ky
fi

%files -n locales-ky
%defattr(-,root,root)
/usr/share/locale/ky*

### lg
%package -n locales-lg
Summary:	Base files for localization (Luganda)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Provides:	locales-lug

%description -n locales-lg
These are the base files for Luganda (Ganda) language localization; you need
it to correctly display 8bits Luganda characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Luganda language conventions.

%post -n locales-lg
if [ "$1" = "1" ]; then
	%{loc_add} lg lug
fi
%postun -n locales-lg
if [ "$1" = "0" ]; then
	%{loc_del} lg lug
fi

#%files -n locales-lg
#%defattr(-,root,root)
#/usr/share/locale/lg*
#/usr/share/locale/lug*

### li
%package -n locales-li
Summary:	Base files for localization (Limburguish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-li
These are the base files for Limburguish language localization; you need
it to correctly display 8bits characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Limburguish language conventions.

%post -n locales-li
if [ "$1" = "1" ]; then
	%{loc_add} li
fi
%postun -n locales-li
if [ "$1" = "0" ]; then
	%{loc_del} li
fi

%files -n locales-li
%defattr(-,root,root)
/usr/share/locale/li*

### lo
%package -n locales-lo
Summary:	Base files for localization (Laotian) [INCOMPLETE]
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-lo
These are the base files for Laotian language localization; you need
it to correctly display 8bits lao characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Laotian language conventions.

%post -n locales-lo
if [ "$1" = "1" ]; then
	%{loc_add} lo
fi
%postun -n locales-lo
if [ "$1" = "0" ]; then
	%{loc_del} lo
fi

%files -n locales-lo
%defattr(-,root,root)
# not just lo* because of locale.alias
/usr/share/locale/lo
/usr/share/locale/lo_*

### lt
%package -n locales-lt
Summary:	Base files for localization (Lithuanian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-lt
These are the base files for Lithuanian language localization; you need
it to correctly display 8bits Lithuanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Lithuanian language conventions.

%post -n locales-lt
if [ "$1" = "1" ]; then
	%{loc_add} lt
fi
%postun -n locales-lt
if [ "$1" = "0" ]; then
	%{loc_del} lt
fi

%files -n locales-lt
%defattr(-,root,root)
# not just lt* because of ltg
/usr/share/locale/lt
/usr/share/locale/lt_*

### lv
# translation done by Vitauts Stochka <vit@dpu.lv>
%package -n locales-lv
Summary:	Base files for localization (Latvian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-lv
These are the base files for Latvian language localization; you need
it to correctly display 8bits Latvian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Latvian language conventions.


%post -n locales-lv
if [ "$1" = "1" ]; then
	%{loc_add} lv
fi
%postun -n locales-lv
if [ "$1" = "0" ]; then
	%{loc_del} lv
fi

%files -n locales-lv
%defattr(-,root,root)
/usr/share/locale/lv*

### mi
# Maori translation provided by Gasson <gasson@clear.net.nz>
%package -n locales-mi
Summary:	Base files for localization (Maori)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-mi
These are the base files for Maori language localization; you need it for
it to correctly display 8bits Maori characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Maori language conventions.

%post -n locales-mi
if [ "$1" = "1" ]; then
	%{loc_add} mi
fi
%postun -n locales-mi
if [ "$1" = "0" ]; then
	%{loc_del} mi
fi

%files -n locales-mi
%defattr(-,root,root)
/usr/share/locale/mi*

### mk
%package -n locales-mk
Summary:	Base files for localization (Macedonian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-mk
These are the base files for Macedonian language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Macedonian language conventions.

%post -n locales-mk
if [ "$1" = "1" ]; then
	%{loc_add} mk
fi
%postun -n locales-mk
if [ "$1" = "0" ]; then
	%{loc_del} mk
fi

%files -n locales-mk
%defattr(-,root,root)
/usr/share/locale/mk*

### ml
%package -n locales-ml
Summary:	Base files for localization (Malayalam)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ml
These are the base files for Malayalam language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Malayalam language conventions.

%post -n locales-ml
if [ "$1" = "1" ]; then
	%{loc_add} ml
fi
%postun -n locales-ml
if [ "$1" = "0" ]; then
	%{loc_del} ml
fi

%files -n locales-ml
%defattr(-,root,root)
/usr/share/locale/ml*

### mn
%package -n locales-mn
Summary:	Base files for localization (Mongolian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-mn
These are the base files for Mongolian language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Mongolian language conventions.

%post -n locales-mn
if [ "$1" = "1" ]; then
	%{loc_add} mn
fi
%postun -n locales-mn
if [ "$1" = "0" ]; then
	%{loc_del} mn
fi

%files -n locales-mn
%defattr(-,root,root)
/usr/share/locale/mn*

### mr
%package -n locales-mr
Summary:	Base files for localization (Marathi)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-mr
These are the base files for Marathi language localization; you need
it to correctly display 8bits Marathi characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Marathi language conventions.

%post -n locales-mr
if [ "$1" = "1" ]; then
	%{loc_add} mr
fi
%postun -n locales-mr
if [ "$1" = "0" ]; then
	%{loc_del} mr
fi

%files -n locales-mr
%defattr(-,root,root)
/usr/share/locale/mr*

### ms
%package -n locales-ms
Summary:	Base files for localization (Malay)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ms
These are the base files for Malay language localization; you need it for
proper alphabetical sorting and representation of dates and numbers according
to Malay language conventions.

%post -n locales-ms
if [ "$1" = "1" ]; then
	%{loc_add} ms
fi
%postun -n locales-ms
if [ "$1" = "0" ]; then
	%{loc_del} ms
fi

%files -n locales-ms
%defattr(-,root,root)
/usr/share/locale/ms*

### mt
# translation by Ramon Casha <rcasha@waldonet.net.mt>
%package -n locales-mt
Summary:	Base files for localization (Maltese)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-mt
These are the base files for Maltese language localization; you need
it to correctly display 8bits Maltese characters, and for proper
alphabetical sorting and representation of dates and numbers according\
to Maltese language conventions.

%post -n locales-mt
if [ "$1" = "1" ]; then
	%{loc_add} mt
fi
%postun -n locales-mt
if [ "$1" = "0" ]; then
	%{loc_del} mt
fi

%files -n locales-mt
%defattr(-,root,root)
/usr/share/locale/mt*

### nds
%package -n locales-nds
Summary:	Base files for localization (Lower Saxon)
Group:		System/Internationalization
Requires:	locales = %{version}

%description -n locales-nds
These are the base files for Lower Saxon language
localization; you need it to correctly display 8bits Lower Saxon characters,
and for proper alphabetical sorting and representation of dates and numbers
according to Lower Saxon language conventions.

%post -n locales-nds
if [ "$1" = "1" ]; then
	%{loc_add} nds
fi
%postun -n locales-nds
if [ "$1" = "0" ]; then
	%{loc_del} nds
fi

%files -n locales-nds
%defattr(-,root,root)
/usr/share/locale/nds*

### ne
%package -n locales-ne
Summary:	Base files for localization (Nepali)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ne
These are the base files for Nepali language localization; you need
it to correctly display 8bits Nepali characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Nepali language conventions.

%post -n locales-ne
if [ "$1" = "1" ]; then
	%{loc_add} ne
fi
%postun -n locales-ne
if [ "$1" = "0" ]; then
	%{loc_del} ne
fi

%files -n locales-ne
%defattr(-,root,root)
/usr/share/locale/ne*

### nl
%package -n locales-nl
Summary:	Base files for localization (Dutch)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-nl
These are the base files for Dutch language localization; you need
it to correctly display 8bits Dutch characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Dutch language conventions.

%post -n locales-nl
if [ "$1" = "1" ]; then
	%{loc_add} nl
fi
%postun -n locales-nl
if [ "$1" = "0" ]; then
	%{loc_del} nl
fi

%files -n locales-nl
%defattr(-,root,root)
/usr/share/locale/nl*

### no
# translations by peter@datadok.no
%package -n locales-no
Summary:	Base files for localization (Norwegian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Provides:	locales-nn, locales-nb

%description -n locales-no
These are the base files for Norwegian language localization; you need
it to correctly display 8bits Norwegian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Norwegian language conventions.

%post -n locales-no
if [ "$1" = "1" ]; then
	%{loc_add} no nb nn
fi
%postun -n locales-no
if [ "$1" = "0" ]; then
	%{loc_del} no nb nn
fi

%files -n locales-no
%defattr(-,root,root)
/usr/share/locale/no*
/usr/share/locale/nb*
/usr/share/locale/nn*

### oc
%package -n locales-oc
Summary:	Base files for localization (Occitan)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-oc
These are the base files for Occitan language localization; you need
it to correctly display 8bits Occitan characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Occitan language conventions.

%post -n locales-oc
if [ "$1" = "1" ]; then
	%{loc_add} oc
fi
%postun -n locales-oc
if [ "$1" = "0" ]; then
	%{loc_del} oc
fi

%files -n locales-oc
%defattr(-,root,root)
/usr/share/locale/oc*

### om
%package -n locales-om
Summary:	Base files for localization (Oromo)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-om
These are the base files for Oromo language localization; you need
it to correctly display 8bits Oromo characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Oromo language conventions.

%post -n locales-om
if [ "$1" = "1" ]; then
	%{loc_add} om
fi
%postun -n locales-om
if [ "$1" = "0" ]; then
	%{loc_del} om
fi

#%files -n locales-om
#%defattr(-,root,root)
#/usr/share/locale/om*

### pa
%package -n locales-pa
Summary:	Base files for localization (Punjabi)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-pa
These are the base files for Punjabi localization; you need it to correctly
display 8bits characters, and for proper alphabetical sorting and
representation of dates and numbers according
to Punjabi language conventions.

%post -n locales-pa
if [ "$1" = "1" ]; then
	%{loc_add} pa
fi
%postun -n locales-pa
if [ "$1" = "0" ]; then
	%{loc_del} pa
fi

%files -n locales-pa
%defattr(-,root,root)
# not just pa* because of pap
/usr/share/locale/pa
/usr/share/locale/pa_*

### ph
%package -n locales-ph
Summary:	Base files for localization (Pilipino)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Provides:	locales-tl

%description -n locales-ph
These are the base files for Pilipino (official language of the Philipines)
localization; you need it to correctly display 8bits characters,
and for proper alphabetical sorting and representation of dates and numbers
according to Pilipino language conventions.

%post -n locales-ph
if [ "$1" = "1" ]; then
	%{loc_add} ph tl
fi
%postun -n locales-ph
if [ "$1" = "0" ]; then
	%{loc_del} ph tl
fi

%files -n locales-ph
%defattr(-,root,root)
/usr/share/locale/ph*
/usr/share/locale/tl*

### pl
# translation from piotr pogorzelski <pp@pietrek.priv.pl>
%package -n locales-pl
Summary:	Base files for localization (Polish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-pl
These are the base files for Polish language localization; you need
it to correctly display 8bits Polish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Polish language conventions.

%post -n locales-pl
if [ "$1" = "1" ]; then
	%{loc_add} pl
fi
%postun -n locales-pl
if [ "$1" = "0" ]; then
	%{loc_del} pl
fi

%files -n locales-pl
%defattr(-,root,root)
/usr/share/locale/pl*

### pap
%package -n locales-pap
Summary:	Base files for localization (Papiamento)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Obsoletes:	locales-pp
Provides:	locales-pp

%description -n locales-pap
These are the base files for Papiamento language localization; you need
it to correctly display 8bits Papiamento characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Papiamento language conventions.

%post -n locales-pap
if [ "$1" = "1" ]; then
	%{loc_add} pap
fi
%postun -n locales-pap
if [ "$1" = "0" ]; then
	%{loc_del} pap
fi

#%files -n locales-pap
#%defattr(-,root,root)
#/usr/share/locale/pap*

### pt
%package -n locales-pt
Summary:	Base files for localization (Portuguese)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-pt
These are the base files for Portuguese language localization; you need
it to correctly display 8bits Portuguese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Portuguese language conventions.

%post -n locales-pt
if [ "$1" = "1" ]; then
	%{loc_add} pt pt_BR pt_PT
fi
%postun -n locales-pt
if [ "$1" = "0" ]; then
	%{loc_del} pt pt_BR pt_PT
fi

%files -n locales-pt
%defattr(-,root,root)
/usr/share/locale/pt*

### ro
# translation from "Mihai" <mihai@ambra.ro>
%package -n locales-ro
Summary:	Base files for localization (Romanian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ro
These are the base files for Romanian language localization; you need
it to correctly display 8bits Romanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Romanian language conventions.

%post -n locales-ro
if [ "$1" = "1" ]; then
	%{loc_add} ro
fi
%postun -n locales-ro
if [ "$1" = "0" ]; then
	%{loc_del} ro
fi

%files -n locales-ro
%defattr(-,root,root)
/usr/share/locale/ro*

### ru
%package -n locales-ru
Summary:	Base files for localization (Russian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ru
These are the base files for Russian language localization; you need
it to correctly display 8bits cyrillic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Russian language conventions.

%post -n locales-ru
if [ "$1" = "1" ]; then
	%{loc_add} ru
fi
%postun -n locales-ru
if [ "$1" = "0" ]; then
	%{loc_del} ru
fi

%files -n locales-ru
%defattr(-,root,root)
/usr/share/locale/ru*

### sc
%package -n locales-sc
Summary:	Base files for localization (Sardinian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-sc
These are the base files for Sardinian language localization; you need
it to correctly display 8bits sardinian characters, and for proper
alfabetical sorting and representation of dates and numbers 
according to sardinian language conventions.

%post -n locales-sc
if [ "$1" = "1" ]; then
	%{loc_add} sc
fi
%postun -n locales-sc
if [ "$1" = "0" ]; then
	%{loc_del} sc
fi

%files -n locales-sc
%defattr(-,root,root)
/usr/share/locale/sc*

### se
%package -n locales-se
Summary:	Base files for localization (Saami)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-se
These are the base files for Saami language localization; you need
it to correctly display 8bits Saami characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Saami language conventions.

%post -n locales-se
if [ "$1" = "1" ]; then
	%{loc_add} se
fi
%postun -n locales-se
if [ "$1" = "0" ]; then
	%{loc_del} se
fi

%files -n locales-se
%defattr(-,root,root)
/usr/share/locale/se*

### sk
%package -n locales-sk
Summary:	Base files for localization (Slovak)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-sk
These are the base files for Slovak language localization; you need
it to correctly display 8bits Slovak characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Slovak language conventions.

%post -n locales-sk
if [ "$1" = "1" ]; then
	%{loc_add} sk
fi
%postun -n locales-sk
if [ "$1" = "0" ]; then
	%{loc_del} sk
fi

%files -n locales-sk
%defattr(-,root,root)
/usr/share/locale/sk*

### sl
# Translations from Roman Maurer <roman.maurer@fmf.uni-lj.si>
%package -n locales-sl
Summary:	Base files for localization (Slovenian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-sl
These are the base files for Slovenian language localization; you need
it to correctly display 8bits Slovenian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Slovenian language conventions.

%post -n locales-sl
if [ "$1" = "1" ]; then
	%{loc_add} sl
fi
%postun -n locales-sl
if [ "$1" = "0" ]; then
	%{loc_del} sl
fi

%files -n locales-sl
%defattr(-,root,root)
/usr/share/locale/sl*

### so
%package -n locales-so
Summary:	Base files for localization (Somali)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-so
These are the base files for Somali language localization; you need
it to correctly display 8bits Somali characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Somali language conventions.

%post -n locales-so
if [ "$1" = "1" ]; then
	%{loc_add} so
fi
%postun -n locales-so
if [ "$1" = "0" ]; then
	%{loc_del} so
fi

#%files -n locales-so
#%defattr(-,root,root)
#/usr/share/locale/so*

### sq
%package -n locales-sq
Summary:	Base files for localization (Albanian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-sq
These are the base files for Albanian language localization; you need
it to correctly display 8bits Albanian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Albanian language conventions.

%post -n locales-sq
if [ "$1" = "1" ]; then
	%{loc_add} sq
fi
%postun -n locales-sq
if [ "$1" = "0" ]; then
	%{loc_del} sq
fi

%files -n locales-sq
%defattr(-,root,root)
/usr/share/locale/sq*

### sr
%package -n locales-sr
Summary:	Base files for localization (Serbian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Provides:	locales-sh

%description -n locales-sr
These are the base files for Serbian language localization; you need
it to correctly display 8bits cyrillic characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Serbian language conventions.

%post -n locales-sr
if [ "$1" = "1" ]; then
	%{loc_add} sr sr@Latn sh
fi
%postun -n locales-sr
if [ "$1" = "0" ]; then
	%{loc_del} sr sr@Latn sh
fi

%files -n locales-sr
%defattr(-,root,root)
/usr/share/locale/sh*
/usr/share/locale/sr*

### st
%package -n locales-st
Summary:	Base files for localization (Sotho)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-st
These are the base files for Sotho language localization; you need
it to correctly display 8bits Sotho characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Sotho language conventions.

%post -n locales-st
if [ "$1" = "1" ]; then
	%{loc_add} st
fi
%postun -n locales-st
if [ "$1" = "0" ]; then
	%{loc_del} st
fi

%files -n locales-st
%defattr(-,root,root)
/usr/share/locale/st*

### sv
# translation by Erik Almqvist <erik.almqvist@vrg.se>
%package -n locales-sv
Summary:	Base files for localization (Swedish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-sv
These are the base files for Swedish language localization; you need
it to correctly display 8bits Swedish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Swedish language conventions.

%post -n locales-sv
if [ "$1" = "1" ]; then
	%{loc_add} sv
fi
%postun -n locales-sv
if [ "$1" = "0" ]; then
	%{loc_del} sv
fi

%files -n locales-sv
%defattr(-,root,root)
/usr/share/locale/sv*

### sw
%package -n locales-sw
Summary:	Base files for localization (Swahili)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-sw
These are the base files for Swahili language localization; you need
it to correctly display 8bits Swahili characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Swahili language conventions.

%post -n locales-sw
if [ "$1" = "1" ]; then
	%{loc_add} sw
fi
%postun -n locales-sw
if [ "$1" = "0" ]; then
	%{loc_del} sw
fi

%files -n locales-sw
%defattr(-,root,root)
/usr/share/locale/sw*

### ta
%package -n locales-ta
Summary:	Base files for localization (Tamil)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
URL:		http://www.tamil.net/tscii/

%description -n locales-ta
These are the base files for Tamil language localization; you need
it to correctly display 8bits Tamil characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tamil language conventions.

%post -n locales-ta
if [ "$1" = "1" ]; then
	%{loc_add} ta
fi
%postun -n locales-ta
if [ "$1" = "0" ]; then
	%{loc_del} ta
fi

%files -n locales-ta
%defattr(-,root,root)
/usr/share/locale/ta*

### te
%package -n locales-te
Summary:	Base files for localization (Telugu)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-te
These are the base files for Telugu language localization; you need
it to correctly display 8bits Telugu characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Telugu language conventions.

%post -n locales-te
if [ "$1" = "1" ]; then
	%{loc_add} te
fi
%postun -n locales-te
if [ "$1" = "0" ]; then
	%{loc_del} te
fi

%files -n locales-te
%defattr(-,root,root)
/usr/share/locale/te*

### tg
%package -n locales-tg
Summary:	Base files for localization (Tajik)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-tg
These are the base files for Tajik language localization; you need
it to correctly display 8bits Tajik characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tajik language conventions.

%post -n locales-tg
if [ "$1" = "1" ]; then
	%{loc_add} tg
fi
%postun -n locales-tg
if [ "$1" = "0" ]; then
	%{loc_del} tg
fi

%files -n locales-tg
%defattr(-,root,root)
/usr/share/locale/tg*

### th
%package -n locales-th
Summary:	Base files for localization (Thai)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
URL:		http://www.links.nectec.or.th/~thep/th-locale/

%description -n locales-th
These are the base files for Thai language localization; you need
it to correctly display 8bits Thai characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Thai language conventions.

%post -n locales-th
if [ "$1" = "1" ]; then
	%{loc_add} th
fi
%postun -n locales-th
if [ "$1" = "0" ]; then
	%{loc_del} th
fi

%files -n locales-th
%defattr(-,root,root)
/usr/share/locale/th*

### tk
%package -n locales-tk
Summary:	Base files for localization (Turkmen)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-tk
These are the base files for Turkmen language localization; you need
it to correctly display 8bits Turkmen characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Turkmen language conventions.

%post -n locales-tk
if [ "$1" = "1" ]; then
	%{loc_add} tk
fi
%postun -n locales-tk
if [ "$1" = "0" ]; then
	%{loc_del} tk
fi

%files -n locales-tk
%defattr(-,root,root)
/usr/share/locale/tk*

### tr
# translation from Gorkem Cetin <e077245@narwhal.cc.metu.edu.tr>
%package -n locales-tr
Summary:	Base files for localization (Turkish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-tr
These are the base files for Turkish language localization; you need
it to correctly display 8bits Turkish characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Turkish language conventions.

%post -n locales-tr
if [ "$1" = "1" ]; then
	%{loc_add} tr
fi
%postun -n locales-tr
if [ "$1" = "0" ]; then
	%{loc_del} tr
fi

%files -n locales-tr
%defattr(-,root,root)
/usr/share/locale/tr*

### tt
%package -n locales-tt
Summary:	Base files for localization (Tatar)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-tt
These are the base files for Tatar language localization; you need
it to correctly display 8bits Tatar characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Tatar language conventions.

%post -n locales-tt
if [ "$1" = "1" ]; then
	%{loc_add} tt
fi
%postun -n locales-tt
if [ "$1" = "0" ]; then
	%{loc_del} tt
fi

%files -n locales-tt
%defattr(-,root,root)
/usr/share/locale/tt*

### uk
%package -n locales-uk
Summary:	Base files for localization (Ukrainian)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-uk
These are the base files for Ukrainian language localization; you need
it to correctly display 8bits Ukrainian characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Ukrainian language conventions.

%post -n locales-uk
if [ "$1" = "1" ]; then
	%{loc_add} uk
fi
%postun -n locales-uk
if [ "$1" = "0" ]; then
	%{loc_del} uk
fi

%files -n locales-uk
%defattr(-,root,root)
/usr/share/locale/uk*

### ur
%package -n locales-ur
Summary:	Base files for localization (Urdu)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-ur
These are the base files for Urdu language localization; you need
it to correctly display 8bits Urdu characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Urdu language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying nor the isolate-initial-medial-final shapes
of letters; it is to the xterm, application or virtual console driver
to do that.

%post -n locales-ur
if [ "$1" = "1" ]; then
	%{loc_add} ur
fi
%postun -n locales-ur
if [ "$1" = "0" ]; then
	%{loc_del} ur
fi

%files -n locales-ur
%defattr(-,root,root)
/usr/share/locale/ur*

### uz
%package -n locales-uz
Summary:	Base files for localization (Uzbek)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-uz
These are the base files for Uzbek language localization; you need
it to correctly display 8bits Uzbek characters, and for proper
alphabetical sorting and representation of dates and numbers
according to Uzbek language conventions.

%post -n locales-uz
if [ "$1" = "1" ]; then
	%{loc_add} uz uz@Latn
fi
%postun -n locales-uz
if [ "$1" = "0" ]; then
	%{loc_del} uz uz@Latn
fi

%files -n locales-uz
%defattr(-,root,root)
/usr/share/locale/uz*

### vi
# translations by <DaiQuy.nguyen@ulg.ac.be>
%package -n locales-vi
Summary:	Base files for localization (Vietnamese)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-vi
These are the base files for Vietnamese language localization; you need
it to correctly display 8bits Vietnamese characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Vietnamese language conventions.

%post -n locales-vi
if [ "$1" = "1" ]; then
	%{loc_add} vi
fi
%postun -n locales-vi
if [ "$1" = "0" ]; then
	%{loc_del} vi
fi

%files -n locales-vi
%defattr(-,root,root)
/usr/share/locale/vi*

### wa
# translations from Lorint Hendschel <LorintHendschel@skynet.be>
%package -n locales-wa
Summary:	Base files for localization (Walloon)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-wa
These are the base files for Walloon language localization; you need
it to correctly display 8bits Walloon characters, and for proper
alphabetical sorting and representation of dates and numbers according
to Walloon language conventions.

%post -n locales-wa
if [ "$1" = "1" ]; then
	%{loc_add} wa
fi
%postun -n locales-wa
if [ "$1" = "0" ]; then
	%{loc_del} wa
fi

%files -n locales-wa
%defattr(-,root,root)
/usr/share/locale/wa*

### xh
%package -n locales-xh
Summary:	Base files for localization (Xhosa)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-xh
These are the base files for Xhosa language localization; you need
it to correctly display 8bits Xhosa characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Xhosa language conventions.

%post -n locales-xh
if [ "$1" = "1" ]; then
	%{loc_add} xh
fi
%postun -n locales-xh
if [ "$1" = "0" ]; then
	%{loc_del} xh
fi

%files -n locales-xh
%defattr(-,root,root)
/usr/share/locale/xh*

### yi
%package -n locales-yi
Summary:	Base files for localization (Yiddish)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
URL:		http://www.uyip.org/

%description -n locales-yi
These are the base files for Yiddish language localization; you need
it to correctly display 8bits Yiddish characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Yiddish language conventions.
Note that this package doesn't handle right-to-left and left-to-right
switching when displaying; it is to the xterm, application or virtual
console driver to do that.

%post -n locales-yi
if [ "$1" = "1" ]; then
	%{loc_add} yi
fi
%postun -n locales-yi
if [ "$1" = "0" ]; then
	%{loc_del} yi
fi

%files -n locales-yi
%defattr(-,root,root)
/usr/share/locale/yi*

### zh
# translation (zh_TW) from <informer@linux1.cgu.edu.tw>
# zh_CN converted from zh_TW.Big5 with b5togb; corrections welcome.
%package -n locales-zh
Summary:	Base files for localization (Chinese)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}
Obsoletes:	libwcsmbs wcsmbs-locale

%description -n locales-zh
These are the base files for Chinese language localization; you need
it to correctly display 8bits and 7bits chinese codes, and for proper
representation of dates and numbers according to chinese language conventions.
Set the LANG variable to "zh_CN" to use simplified chinese (GuoBiao encoding)
or to "zh_TW.Big5" to use traditional characters (Big5 encoding)

%post -n locales-zh
if [ "$1" = "1" ]; then
	%{loc_add} zh zh_CN zh_TW
fi
%postun -n locales-zh
if [ "$1" = "0" ]; then
	%{loc_del} zh zh_CN zh_TW
fi

%files -n locales-zh
%defattr(-,root,root)
/usr/share/locale/zh*

### zu
%package -n locales-zu
Summary:	Base files for localization (Zulu)
Group:		System/Internationalization
Requires:	locales = %{version}-%{release}

%description -n locales-zu
These are the base files for Zulu language localization; you need
it to correctly display 8bits Zulu characters, and for proper
alfabetical sorting, and representation of dates and numbers
according to Xhosa language conventions.

%post -n locales-zu
if [ "$1" = "1" ]; then
	%{loc_add} zu
fi
%postun -n locales-zu
if [ "$1" = "0" ]; then
	%{loc_del} zu
fi

%files -n locales-zu
%defattr(-,root,root)
/usr/share/locale/zu*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

