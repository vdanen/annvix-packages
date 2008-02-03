[[ -n "$TARGET" ]] || TARGET="%{_target_cpu}"

case "$TARGET" in
  sparc64)
    ASM64="asm-sparc64"
    ASM="asm-sparc"
    DEF64="__arch64__"
    STUB="__SPARC_ASM_STUB__"
    NAME64="SPARC64"
    NAME32="SPARC32"
    ;;
  ppc64)
    ASM64="asm-ppc64"
    ASM="asm-ppc"
    DEF64="__powerpc64__"
    STUB="__PPC_ASM_STUB__"
    NAME64="PPC64"
    NAME32="PPC32"
    ;;
  x86_64|amd64)
    ASM64="asm-x86_64"
    ASM="asm-i386"
    DEF64="__x86_64__"
    STUB="__X86_64_ASM_STUB__"
    NAME64="X86-64"
    NAME32="x86"
    ;;
  s390x)
    ASM64="asm-s390x"
    ASM="asm-s390"
    DEF64="__s390x__"
    STUB="__S390_ASM_STUB__"
    NAME64="S390x"
    NAME32="S390"
    ;;
  i*86|athlon)
    ASM="asm-i386"
    ;;
  ppc)
    ASM="asm-ppc"
    ;;
  *)
    ASM="asm-$TARGET"
esac

function CreateBiarchHeader() {
  I="$1"
  J=`echo $I | tr a-z.- A-Z__`
  if [ -f $ASM/$I -a -f $ASM64/$I ]; then
    INC64="#include <$ASM64/$I>"
    INC32="#include <$ASM/$I>"
  elif [ -f $ASM/$I ]; then
    INC64="#error $I is not supported on $NAME64"
    INC32="#include <$ASM/$I>"
  else
    INC64="#include <$ASM64/$I>"
    INC32="#error $I is not supported on $NAME32"
  fi
  [ -d asm ] || mkdir asm
  cat > asm/$I << EOF
#ifndef ${STUB}${J}__
#define ${STUB}${J}__
#ifdef $DEF64
$INC64
#else
$INC32
#endif
#endif
EOF
}

# Prepare PowerPC tree (2.6.16+)
case $TARGET in (ppc*)
[[ -d asm-powerpc ]] && {
    for f in asm-powerpc/*.h; do
	[[ -f asm-ppc/${f##*/} ]] || cp -av $f asm-ppc/
    done
    if [[ -z "$ASM64" ]]; then
	mv asm-powerpc $ASM
    else
	mv asm-powerpc $ASM64
    fi
} ;;
esac

# Create bi-arch headers
[[ -z "$DEF64" ]] && mv $ASM asm || {
  for I in `( ls $ASM; ls $ASM64 ) | grep '\.h$' | sort -u`; do
    CreateBiarchHeader $I
  done
}

# Clean-ups 
find . -maxdepth 1 -type d -name "asm-*" ! -name "$ASM" ! -name "$ASM64" ! -name "asm-generic" | xargs rm -rf
find . -type d -name CVS | xargs rm -rf
