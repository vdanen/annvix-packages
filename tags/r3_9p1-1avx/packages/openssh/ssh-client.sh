# fix hanging ssh clients on exit
if [ "$SHELL" != "/bin/ksh" ]; then
  if [ -n "$ZSH_VERSION" ]; then
       setopt hup
  else
       shopt -s huponexit
  fi
fi
