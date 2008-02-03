/*
 * Try to be a little smarter about which kernel are we currently running
 */

#ifndef __rh_config_h__
#define __rh_config_h__

/*
 * First, get the version string for the running kernel from
 * /boot/kernel.h - initscripts should create it for us
 */

#include "/boot/kernel.h"

#if defined(__BOOT_KERNEL_SMP) && (__BOOT_KERNEL_SMP == 1)
#define __module__smp
#endif

#if defined(__BOOT_KERNEL_BOOT) && (__BOOT_KERNEL_BOOT == 1)
#define __module__BOOT
#endif

#if defined(__BOOT_KERNEL_SECURE) && (__BOOT_KERNEL_SECURE == 1)
#define __module__secure
#endif

#if defined(__BOOT_KERNEL_ENTERPRISE) && (__BOOT_KERNEL_ENTERPRISE == 1)
#define __module__enterprise
#endif

#if defined(__BOOT_KERNEL_I586_UP_1GB) && (__BOOT_KERNEL_I586_UP_1GB == 1)
#define __module__i586_up_1GB
#endif

#if defined(__BOOT_KERNEL_I686_UP_4GB) && (__BOOT_KERNEL_I686_UP_4GB == 1)
#define __module__i686_up_4GB
#endif

#if defined(__BOOT_KERNEL_I686_UP_64GB) && (__BOOT_KERNEL_I686_UP_64GB == 1)
#define __module__i686_up_64GB
#endif

#if !defined(__module__smp) && !defined(__module__secure) && !defined(__module__BOOT) && !defined(__module__enterprise) && !defined(__module__i586_up_1GB) && !defined(__module__i686_up_4GB) && !defined(__module__i686_up_64GB) && !defined(__module__i686_smp_64GB)
#define __module__up
#endif /* default (BOOT_KERNEL_UP) */

#ifdef __i386__
# ifdef __MODULE_KERNEL_i586
#  define __module__i586
#  ifdef __module__up
#   define __module__i586_up
#  endif
#  ifdef __module__smp
#   define __module__i586_smp
#  endif
#  ifdef __module__secure
#   define __module__i586_secure
#  endif
#  ifdef __module__BOOT
#   define __module__i586_BOOT
#  endif
#  ifdef __module__enterprise
#   define __module__i586_enterprise
#  endif
#  ifdef __module__i586_up_1GB
#    define __module__i586_i586_up_1GB
#  endif
#  ifdef __module__i686_up_4GB
#    define __module__i586_i686_up_4GB
#  endif
#  ifdef __module__i686_up_64GB
#    define __module__i586_i686_up_64GB
#  endif
# elif defined(__MODULE_KERNEL_i686)
#  define __module__i686
#  ifdef __module__up
#   define __module__i686_up
#  endif
#  ifdef __module__smp
#   define __module__i686_smp
#  endif
#  ifdef __module__secure
#   define __module__i686_secure
#  endif
#  ifdef __module__BOOT
#   define __module__i686_BOOT
#  endif
#  ifdef __module__enterprise
#   define __module__i686_enterprise
#  endif
#  ifdef __module__i586_up_1GB
#    define __module__i686_i586_up_1GB
#  endif
#  ifdef __module__i686_up_4GB
#    define __module__i686_i686_up_4GB
#  endif
#  ifdef __module__i686_up_64GB
#    define __module__i686_i686_up_64GB
#  endif
# else
#  define __module__i386
#  ifdef __module__up
#   define __module__i386_up
#  endif
#  ifdef __module__smp
#   define __module__i386_smp
#  endif
#  ifdef __module__secure
#   define __module__i386_secure
#  endif
#  ifdef __module__BOOT
#   define __module__i386_BOOT
#  endif
#  ifdef __module__enterprise
#   define __module__i386_enterprise
#  endif
#  ifdef __module__i586_up_1GB
#    define __module__i386_i586_up_1GB
#  endif
#  ifdef __module__i686_up_4GB
#    define __module__i386_i686_up_4GB
#  endif
#  ifdef __module__i686_up_64GB
#    define __module__i386_i686_up_64GB
#  endif
# endif
#endif

#ifdef __alpha__
# define __module__alpha
# ifdef __module__up
#  define __module__alpha_up
# endif
# ifdef __module__smp
#  define __module__alpha_smp
# endif
#endif

#ifdef __ia64__
# define __module__ia64
# ifdef __module__up
#  define __module__ia64_up
# endif
# ifdef __module__smp
#  define __module__ia64_smp
# endif
# ifdef __module__BOOT
#  define __module__ia64_BOOT
# endif
#endif

#ifdef __x86_64__
# define __module__x86_64
# ifdef __module__up
#  define __module__x86_64_up
# endif
# ifdef __module__smp
#  define __module__x86_64_smp
# endif
# ifdef __module__BOOT
#  define __module__x86_64_BOOT
# endif
#endif

#ifdef __ppc__
# define __module__ppc
# ifdef __module__up
#  define __module__ppc_up
# endif
# ifdef __module__smp
#  define __module__ppc_smp
# endif
# ifdef __module__BOOT
#  define __module__ppc_BOOT
# endif
#endif

#if defined(__module__smp) || defined(__module__enterprise) || defined(__module__secure) || defined(__module__p3_smp_64GB)
#define _ver_str(x) smp_ ## x
#else
#define _ver_str(x) x
#endif

#endif /* __rh_config_h__ */
