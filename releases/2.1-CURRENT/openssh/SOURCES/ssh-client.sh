# fix hanging ssh clients on exit
if [ -n "$BASH_VERSION" ]; then
    shopt -s huponexit
elif [ -n "$ZSH_VERSION" ]; then
    setopt hup
fi
