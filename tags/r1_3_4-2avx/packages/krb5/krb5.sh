if ! echo ${PATH} | grep -q /usr/bin ; then
	PATH=/usr/bin:${PATH}
fi
if ! echo ${PATH} | grep -q /usr/sbin ; then
	if [ `id -u` = 0 ] ; then
		PATH=/usr/sbin:${PATH}
	fi
fi
