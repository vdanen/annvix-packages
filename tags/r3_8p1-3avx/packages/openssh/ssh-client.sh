# fix hanging ssh clients on exit
if test -n "$ZSH_VERSION"; then
       setopt hup
else
       shopt -s huponexit
fi
