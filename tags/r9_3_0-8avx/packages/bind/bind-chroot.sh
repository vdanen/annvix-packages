#!/bin/sh
# copyright Florin Grad <florin@mandrakesoft.com>
# GPL License

# Source function library.
. /etc/rc.d/init.d/functions

[ -f /etc/sysconfig/syslog ] && . /etc/sysconfig/syslog

[ -f /etc/sysconfig/named ] && . /etc/sysconfig/named


# chroot
if [ "$1" == "-s" -o "$1" == "--status" ]; then

	if [ -n "${ROOTDIR}" ]; then
		gprintf "\n"
		gprintf "ROOTDIR is defined in your /etc/sysconfig/named file.\n" 
		gprintf "You already appear to have a chroot BIND setup.\n"
		gprintf "ROOTDIR=${ROOTDIR}\n" 
		exit
	else
		gprintf "Your BIND server is not chrooted.\n"
	fi
		
elif [ "$1" == "-c" -o "$1" == "--chroot" -o "$1" == "-i" -o "$1" == "--interactive" ]; then

	if [ -n "${ROOTDIR}" ]; then
		gprintf "\n"
		gprintf "In your /etc/sysconfig/named file: ROOTDIR=${ROOTDIR} exists\n" 
		gprintf "You already appear to have a chroot BIND setup.\n"
		exit

	#interactive
	elif [ "$1" == "-i" -o "$1" == "--interactive" ]; then
		gprintf "\n"
		gprintf "Please enter the  ROOTDIR path (ex: /var/lib/named-chroot):\n"
		# can't use ctrl-c, we trap all signal.
		read answer;
		export ROOTDIR="$answer"
	#non interactive
	elif [ "$1" == "-c" -a -n "$2" -o "$1" == "--chroot" -a -n "$2" ]; then
		export ROOTDIR="$2"
	else 
		gprintf "\n"
		gprintf "Missing path for chroot.\n"
	fi

	# create directories and set permissions
	mkdir -p ${ROOTDIR}
	chmod 700 ${ROOTDIR}
	cd ${ROOTDIR}
	mkdir -p dev etc var/run
	[ -e dev/null ] || mknod dev/null c 1 3
	[ -e dev/random ] || mknod dev/random c 1 8
	cp /etc/localtime etc/
	[ -f /etc/named.conf ] && mv -f /etc/named.conf etc/
	[ -f /etc/rndc.conf ] && mv -f /etc/rndc.conf etc/
	[ -f /etc/rndc.key ] && mv -f /etc/rndc.key etc/
	[ -e /var/named ] && mv -f /var/named var
	[ -e /var/run/named/named.pid ] && mv -f /var/run/named var/run
	chown -R named.named  ${ROOTDIR}

	# update /etc/sysconfig/syslog
	if ! grep -q "${ROOTDIR}/dev/log" /etc/sysconfig/syslog; then
		if ! grep -q ^SYSLOGD_OPTIONS= /etc/sysconfig/syslog; then 
			gprintf "\n"
			gprintf "\nAdding SYSLOGD_OPTIONS in the /etc/sysconfig/syslog file.\n"
			echo "SYSLOGD_OPTIONS=\"-a ${ROOTDIR}/dev/log\"" >> /etc/sysconfig/syslog
		elif sed 's!^\(SYSLOGD_OPTIONS=".*\)"$!\1 -a '${ROOTDIR}'/dev/log"!' < /etc/sysconfig/syslog > /etc/sysconfig/syslog.new; then
			gprintf "\n"
			gprintf "\nUpdating SYSLOGD_OPTIONS in the /etc/sysconfig/syslog file.\n"
			mv -f /etc/sysconfig/syslog.new /etc/sysconfig/syslog
		else
			gprintf "\n"
			gprintf "\nWarning:  Updating /etc/sysconfig/syslog failed! Continuing.\n"
		fi
	fi

	#update the OPTIONS in /etc/sysconfig/named
	if grep -q ^OPTIONS= /etc/sysconfig/named; then
		if sed 's!^\(OPTIONS=".*\)"$!\1 -c /etc/named.conf"!' < /etc/sysconfig/named > /etc/sysconfig/named.new; then
			mv -f /etc/sysconfig/named.new /etc/sysconfig/named
		fi
	else
		gprintf "\nUpdating OPTIONS in /etc/sysconfig/named\n"
		gprintf "OPTIONS=\"-c /etc/named.conf\"\n" >> /etc/sysconfig/named
	fi

	#update the ROOTDIR in /etc/sysconfig/named
	gprintf "\nUpdating ROOTDIR in /etc/sysconfig/named\n"
	gprintf "ROOTDIR=\"${ROOTDIR}\"\n" >> /etc/sysconfig/named

	gprintf "\n"
	gprintf "\nChroot configuration for BIND is complete.\n"
	gprintf "\nYou should review your ${ROOTDIR}/etc/named.conf\n"
	gprintf "\nand make any necessary changes.\n"
	gprintf "\n"
	gprintf "\nRun \"/sbin/service named restart\" when you are done.\n"
	gprintf "\n"

# unchroot
elif [ "$1" == "-u" -o "$1" == "--unchroot" ]; then

	if ! grep -q "^ROOTDIR=" /etc/sysconfig/named; then
		gprintf "\n"
		gprintf "Your bind is not currently chrooted\n"
		gprintf "\n"
		exit
	fi
		
	gprintf "\n"
	gprintf "Removing ROOTDIR from /etc/sysconfig/named\n"
	sed -e '/^\(ROOTDIR=".*\)"$/d' < /etc/sysconfig/named > /etc/sysconfig/named.new
	mv -f /etc/sysconfig/named.new /etc/sysconfig/named
	gprintf "Cleaning the OPTIONS in /etc/sysconfig/named\n"
	sed -e 's|-c /etc/named.conf[ \t]*||' < /etc/sysconfig/named > /etc/sysconfig/named.new
	mv -f /etc/sysconfig/named.new /etc/sysconfig/named
	sed -e 's|[ \t][ \t]*"|"|' < /etc/sysconfig/named > /etc/sysconfig/named.new
	mv -f /etc/sysconfig/named.new /etc/sysconfig/named
	gprintf "Cleaning the SYSLOGD_OPTIONS in /etc/sysconfig/syslog\n"
	sed -e 's|-a '${ROOTDIR}'/dev/log[ \t]*||' < /etc/sysconfig/syslog > /etc/sysconfig/syslog.new
	mv -f /etc/sysconfig/syslog.new /etc/sysconfig/syslog
	sed -e 's|[ \t][ \t]*"|"|' < /etc/sysconfig/syslog > /etc/sysconfig/syslog.new
	mv -f /etc/sysconfig/syslog.new /etc/sysconfig/syslog
	gprintf "\n"
	gprintf "Moving the following files to their original location :\n"
	gprintf "/etc/named.conf\n"
	gprintf "/etc/rndc.conf\n"
	gprintf "/etc/rndc.key\n"
	gprintf "/var/named/*\n"
	gprintf "/var/run/named\n"
	gprintf "/etc/named.conf\n"
	[ -f /etc/named.conf ] || mv -f ${ROOTDIR}/etc/named.conf /etc/
	[ -f /etc/rndc.conf ] || mv -f ${ROOTDIR}/etc/rndc.conf /etc/
	[ -f /etc/rndc.key ] || mv -f ${ROOTDIR}/etc/rndc.key /etc/
	[ -e /var/named ] || mv -f ${ROOTDIR}/var/named /var
	[ -e /var/run/named ] || mv -f ${ROOTDIR}/var/run/named /var/run
	[ -f /etc/named.conf ] && chown -R named.named  /etc/named.conf
	[ -f /etc/rndc.conf ] && chown -R named.named  /etc/rndc.conf
	[ -f /etc/rndc.key ] && chown -R named.named  /etc/rndc.key
	[ -e /var/named ] && chown -R named.named  /var/named
	[ -e /var/run/named ] && chown -R named.named  /var/run/named
	touch /var/run/named/named.pid
	[ -f /var/run/named/named.pid ] && chown -R named.named /var/run/named

	gprintf "\n"
	gprintf "Removing the ${ROOTDIR}\n"
	rm -rf ${ROOTDIR}
	gprintf "\nYour bind server is not chrooted anymore."
	gprintf "\n"
	gprintf "\nRun \"/sbin/service named restart\" when you are done.\n"
	gprintf "\n"

#usage 
else 
	gprintf "\nUsage: chroot_bind.sh [arguments]"
	gprintf "\n"
	gprintf "\n\t-s, --status \t\t(current bind configuration type)"
	gprintf "\n"
	gprintf "\narguments:"
	gprintf "\n\t-i, --interactive \t(so you can choose your path)"
	gprintf "\n"
	gprintf "\n\t-c, --chroot \t\t(choose a chroot location. ex: /var/lib/named-chroot/)"
	gprintf "\n"
	gprintf "\n\t-u, --unchroot \t\t(back to the original configuration)"
	gprintf "\n"
fi
