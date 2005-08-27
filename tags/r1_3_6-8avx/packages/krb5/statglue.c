/* glibc 2.2.2 fixes the "weak symbol pulled into shared library" problem,
 * but we need to maintain that behavior to keep from breaking third-party
 * apps.  Glue code from Jakub. */
#include <sys/stat.h>
#undef lstat
#undef __lstat
#undef fstat
#undef __fstat
#undef stat
#undef __stat
int __lstat (const char *file, struct stat *buf) { return __lxstat (_STAT_VER, file, buf); }
extern int lstat (const char *file, struct stat *buf) __attribute__((weak, alias ("__lstat")));
int __fstat (int fd, struct stat *buf) { return __fxstat (_STAT_VER, fd, buf); }
extern int fstat (int fd, struct stat *buf) __attribute__((weak, alias ("__fstat")));
int __stat (const char *file, struct stat *buf) { return __xstat (_STAT_VER, file, buf); }
extern int stat (const char *file, struct stat *buf) __attribute__((weak, alias ("__stat")));
