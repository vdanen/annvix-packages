 if ! { (echo "${PATH}" | grep -q /usr/bin) } then
 	setenv PATH "/usr/bin:${PATH}"
 endif
 
 if ! { (echo "${PATH}" | grep -q /usr/sbin) } then
 	if ( `id -u` == 0 )  then
 		setenv PATH "/usr/sbin:${PATH}"
 	endif
 endif
