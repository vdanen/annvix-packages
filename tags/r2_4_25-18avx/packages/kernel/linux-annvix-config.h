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

#if defined(__BOOT_KERNEL_BUILD) && (__BOOT_KERNEL_BUILD == 1)
#define __module__build
#endif

#if !defined(__module__smp) && !defined(__module__BOOT) && !defined(__module__BUILD)
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
#  ifdef __module__BOOT
#   define __module__i586_BOOT
#  endif
#  ifdef __module__build
#   define __module__i586_build
#  endif
# else
#  define __module__i386
#  ifdef __module__up
#   define __module__i386_up
#  endif
#  ifdef __module__smp
#   define __module__i386_smp
#  endif
#  ifdef __module__BOOT
#   define __module__i386_BOOT
#  endif
#  ifdef __module__build
#   define __module__i386_build
#  endif
# endif
#endif

#if defined(__module__smp)
#define _ver_str(x) smp_ ## x
#else
#define _ver_str(x) x
#endif

#endif /* __rh_config_h__ */
