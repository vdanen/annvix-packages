#
# spec file for package php
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php
%define version		5.2.4
%define release		%_revrel
%define epoch		2

%define libversion	5
%define libname		%mklibname php_common %{libversion}

%define suhosin_ver	5.2.4-0.9.6.2

%define _requires_exceptions BEGIN\\|mkinstalldirs\\|pear(\\|/usr/bin/tclsh

Summary:	The PHP5 scripting language
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Source0:	http://static.php.net/www.php.net/distributions/php-%{version}.tar.bz2
Source1:	php-exif.ini
Source2:	php-gd.ini
Source3:	php-mcrypt.ini
Source4:	php-mysql.ini
Source5:	php-mysqli.ini
Source6:	php-odbc.ini
Source7:	php-sqlite.ini
Source8:	php-pgsql.ini
Source9:	php-soap.ini
Source10:	php-sockets.ini
Source11:	php-mime_magic.ini
#
# Mandriva/Annvix patches
#
Patch0:		php-5.2.3-mdv-init.patch
Patch1:		php-5.2.4-mdv-shared.patch
Patch3:		php-5.2.3-mdv-64bit.patch
Patch5:		php-5.2.3-mdv-libtool.patch
Patch6:		php-5.2.4-mdv-no_egg.patch
Patch7:		php-5.2.4-mdv-phpize.patch
Patch8:		php-5.2.3-mdv-remove_bogus_iconv_deps.patch
Patch9:		php-5.2.3-mdv-phpbuilddir.patch
# http://www.outoforder.cc/projects/apache/mod_transform/patches/php5-apache2-filters.patch
Patch10:	php5-apache2-filters.patch
# P11 fixes the way we package the extensions to not check if the dep are installed or compiled in
Patch11:	php-5.2.3-mdv-extension_dep_macro_revert.patch
Patch12:	php-5.2.3-mdv-no_libedit.patch
Patch13:	php-5.2.1-mdv-extraimapcheck.patch
#
# from PLD (20-29)
#
Patch20:	php-5.2.4-mdv-pld-mail.patch
Patch21:	php-4.3.3RC3-pld-sybase-fix.patch
Patch25:	php-5.2.3-pld-dba-link.patch
Patch27:	php-4.4.1-pld-zlib-for-getimagesize.patch
Patch28:	php-5.0.0b3-pld-zlib.patch
#
# From Debian (30-39)
#
Patch30:	php-5.2.3-mdv-deb-exif_nesting_level.patch
#
# from Fedora (50-60)
#
Patch50:	php-5.2.3-mdv-fdr-cxx.patch
Patch51:	php-5.2.3-mdv-fdr-install.patch
Patch53:	php-5.2.1-fdr-umask.patch
#
# General fixes (70+)
#
Patch71:	php-5.2.3-mdv-shutdown.patch
# Functional changes
Patch72:	php-5.2.3-mdv-dlopen.patch
# Fixes for tests
Patch73:	php-5.1.0RC4-mdk-tests-dashn.patch
Patch74:	php-5.2.3-mdv-tests-wddx.patch
# http://bugs.php.net/bug.php?id=29119
Patch76:	php-5.2.3-mdv-bug29119.patch
Patch77:	php-5.1.0RC6-CVE-2005-3388.diff
Patch78:	php-5.2.3-mdv-libc-client-php.patch
Patch80:	php-5.2.0-CVE-2006-6383.patch
# http://www.hardened-php.net/
Patch100:	suhosin-patch-%{suhosin_ver}.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	httpd-devel >= 2.0.54
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	libtool-devel
BuildRequires:	libxml2-devel >= 2.6
BuildRequires:	libxslt-devel >= 1.1.0
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	openssl >= 0.9.7
BuildRequires:	pcre-devel >= 6.6
BuildRequires:	pam-devel
BuildRequires:	multiarch-utils >= 1.0.3

%description
PHP5 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.


%package cli
Summary:	Command-line interface to PHP
Epoch:		%{epoch}
Group:		Development/PHP
URL:		http://www.php.net
Requires(pre):	php-ini
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	php-suhosin >= 0.9.20
Requires:	php-filter >= 0.11.0
Requires:	php-json >= 1.2.1
Provides:	php = %{version}
Provides:	php5 = %{version}
Provides:	php%{libversion} = %{version}
Obsoletes:	php

%description cli
PHP5 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

This package contains a command-line (CLI) version of php. You must also
install libphp_common. 

If you need apache module support, you also need to install the mod_php
package.


%package cgi
Summary:	CGI interface to PHP
Epoch:		%{epoch}
Group:		Development/PHP
URL:		http://www.php.net
Requires(pre):	php-ini
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	php-suhosin >= 0.9.20
Requires:	php-filter >= 0.11.0
Requires:	php-json >= 1.2.1
Provides:	php = %{version}
Provides:	php5 = %{version}
Provides:	php%{libversion} = %{version}
Obsoletes:	php

%description cgi
PHP5 is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

This package contains a standalone (CGI) version of php. You must also
install libphp_common. 

If you need apache module support, you also need to install the mod_php
package.


%package fcgi
Summary:	FastCGI interface to PHP
Epoch:		%{epoch}
Group:		Development/PHP
URL:		http://www.php.net
Requires(pre):	php-ini
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	php-suhosin >= 0.9.20
Requires:	php-filter >= 0.11.0
Requires:	php-json >= 1.2.1
Provides:	php = %{version}
Provides:	php5 = %{version}
Provides:	php%{libversion} = %{version}
Obsoletes:	php

%description fcgi
PHP5 is an HTML-embeddable scripting language. PHP5 offers built-in
database integration for several commercial and non-commercial
database management systems, so writing a database-enabled script
with PHP5 is fairly simple.  The most common use of PHP5 coding is
probably as a replacement for CGI scripts.

This package contains a standalone (CGI) version of php with FastCGI
support. You must also install libphp5_common. If you need apache
module support, you also need to install the apache-mod_php
package.


%package -n %{libname}
Summary:	Shared library for php
Epoch:		%{epoch}
Group:		Development/PHP
URL:		http://www.php.net
Provides:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	libphp_common = %{version}
Provides:	php-common = %{version}
Provides:	php-pcre = %{version}
Provides:	php-xml = %{version}
Provides:	php-gettext = %{version}
Provides:	php-posix = %{version}
Provides:	php-ctype = %{version}
Provides:	php-session = %{version}
Provides:	php-sysvsem = %{version}
Provides:	php-sysvshm = %{version}
Provides:	php-tokenizer = %{version}
Provides:	php-simplexml = %{version}
Provides:	php-hash = %{version}
Provides:	php-ftp = %{version}
Obsoletes:	php-pcre
Obsoletes:	php-xml
Obsoletes:	php-gettext
Obsoletes:	php-posix
Obsoletes:	php-ctype
Obsoletes:	php-session
Obsoletes:	php-sysvsem
Obsoletes:	php-sysvshm
Obsoletes:	php-tokenizer
Obsoletes:	php-simplexml
Obsoletes:	php-hash
Obsoletes:	php-ftp

%description -n	%{libname}
This package provides the common files to run with different
implementations of PHP. You need this package if you install the php
standalone package or a webserver with php support (ie: mod_php).

%package devel
Summary:	Development package for PHP5
Epoch:		%{epoch}
Group:		Development/C
URL:		http://www.php.net
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires:	autoconf2.5
Requires:	automake1.7
Requires:	bison
Requires:	byacc
Requires:	flex
Requires:	libtool
Requires:	libxml2-devel >= 2.6
Requires:	libxslt-devel >= 1.1.0
Requires:	openssl >= 0.9.7
Requires:	openssl-devel >= 0.9.7
Requires:	pcre-devel >= 6.6
Requires:	pam-devel
Requires:	chrpath
Requires(post):	%{libname} >= %{epoch}:%{version}
Requires(preun): %{libname} >= %{epoch}:%{version}
Provides:	libphp_common-devel = %{version}

%description devel
The php-devel package lets you compile dynamic extensions to PHP5. Included
here is the source for the php extensions. Instead of recompiling the whole
php binary to add support for, say, oracle, install this package and use the
new self-contained extensions support. For more information, read the file
SELF-CONTAINED-EXTENSIONS.


%package pear
Summary:	The PHP PEAR files
Epoch:		%{epoch}
Group:		Development/Other
Requires:	php-cli

%description pear
PEAR is short for "PHP Extension and Application Repository" and is
pronounced just like the fruit. The purpose of PEAR is to provide:

    * A structured library of open-sourced code for PHP users
    * A system for code distribution and package maintenance
    * A standard style for code written in PHP, specified here
    * The PHP Foundation Classes (PFC), see more below
    * The PHP Extension Code Library (PECL), see more below
    * A web site, mailing lists and download mirrors to support the
      PHP/PEAR community


%package bcmath
Summary:	The bcmath module for PHP
Epoch:		0
Group:		Development/PHP

%description bcmath
This is a dynamic shared object (DSO) for PHP that will add bc style precision
math functions support.

For arbitrary precision mathematics PHP offers the Binary Calculator which
supports numbers of any size and precision, represented as strings.


%package bz2
Summary:	The bzip2 module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	bzip2-devel

%description bz2
This is a dynamic shared object (DSO) for PHP that will add bzip2 compression
support to PHP.

The bzip2 functions are used to transparently read and write bzip2 (.bz2)
compressed files.


%package calendar
Summary:	Calendar extension module for PHP
Epoch:		0
Group:		Development/PHP

%description calendar
This is a dynamic shared object (DSO) for PHP that will add calendar support.

The calendar extension presents a series of functions to simplify converting
between different calendar formats. The intermediary or standard it is based on
is the Julian Day Count. The Julian Day Count is a count of days starting from
January 1st, 4713 B.C. To convert between calendar systems, you must first
convert to Julian Day Count, then to the calendar system of your choice. Julian
Day Count is very different from the Julian Calendar! For more information on
Julian Day Count, visit http://www.hermetic.ch/cal_stud/jdn.htm. For more
information on calendar systems visit
http://www.boogle.com/info/cal-overview.html. Excerpts from this page are
included in these instructions, and are in quotes.


%package curl
Summary:	Curl extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	curl-devel >= 7.9.8

%description curl
This is a dynamic shared object (DSO) for PHP that will add curl support.

PHP supports libcurl, a library created by Daniel Stenberg, that allows you to
connect and communicate to many different types of servers with many different
types of protocols. libcurl currently supports the http, https, ftp, gopher,
telnet, dict, file, and ldap protocols. libcurl also supports HTTPS
certificates, HTTP POST, HTTP PUT, FTP uploading (this can also be done with
PHP's ftp extension), HTTP form based upload, proxies, cookies, and
user+password authentication.


%package dba
Summary:	DBA extension module for PHP
Epoch:		0
Group:		Development/PHP
Obsoletes:	php-dba_bundle
Provides:	php-dba_bundle
BuildRequires:	gdbm-devel
BuildRequires:	db4-devel

%description dba
This is a dynamic shared object (DSO) for PHP that will add flat-file databases
(DBA) support.

These functions build the foundation for accessing Berkeley DB style databases.

This is a general abstraction layer for several file-based databases. As such,
functionality is limited to a common subset of features supported by modern
databases such as Sleepycat Software's DB2. (This is not to be confused with
IBM's DB2 software, which is supported through the ODBC functions.)


%package dbase
Epoch:		0
Summary:	DBase extension module for PHP
Group:		Development/PHP

%description dbase
This is a dynamic shared object (DSO) for PHP that will add DBase support.

These functions allow you to access records stored in dBase-format (dbf)
databases.

dBase files are simple sequential files of fixed length records. Records are
appended to the end of the file and delete records are kept until you call
dbase_pack().


%package dom
Summary:	Dom extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	libxml2-devel

%description dom
This is a dynamic shared object (DSO) for PHP that will add dom support.

The DOM extension is the replacement for the DOM XML extension from PHP 4. The
extension still contains many old functions, but they should no longer be used.
In particular, functions that are not object-oriented should be avoided.

The extension allows you to operate on an XML document with the DOM API.


%package exif
Summary:	EXIF extension module for PHP
Epoch:		0
Group:		Development/PHP

%description exif
This is a dynamic shared object (DSO) for PHP that will add EXIF tags support
in image files.

With the exif extension you are able to work with image meta data. For example,
you may use exif functions to read meta data of pictures taken from digital
cameras by working with information stored in the headers of the JPEG and TIFF
images.


%package gd
Summary:	GD extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	gd-devel >= 2.0.33
BuildRequires:	freetype2-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	xpm-devel
BuildRequires:	x11-devel

%description gd
This is a dynamic shared object (DSO) for PHP that will add GD support,
allowing you to create and manipulate images with PHP using the gd library.

PHP is not limited to creating just HTML output. It can also be used to create
and manipulate image files in a variety of different image formats, including
gif, png, jpg, wbmp, and xpm. Even more convenient, PHP can output image
streams directly to a browser. You will need to compile PHP with the GD library
of image functions for this to work. GD and PHP may also require other
libraries, depending on which image formats you want to work with.

You can use the image functions in PHP to get the size of JPEG, GIF, PNG, SWF,
TIFF and JPEG2000 images.

%package gmp
Summary:	Gmp extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	gmp-devel

%description gmp
This is a dynamic shared object (DSO) for PHP that will add arbitrary length
number support using the GNU MP library.


%package iconv
Summary:	Iconv extension module for PHP
Epoch:		0
Group:		Development/PHP

%description iconv
This is a dynamic shared object (DSO) for PHP that will add iconv support.

This module contains an interface to iconv character set conversion facility.
With this module, you can turn a string represented by a local character set
into the one represented by another character set, which may be the Unicode
character set. Supported character sets depend on the iconv implementation of
your system. Note that the iconv function on some systems may not work as you
expect. In such case, it'd be a good idea to install the GNU libiconv library.
It will most likely end up with more consistent results.


%package json
Summary:	JavaScript Object Notation
Group:		Development/PHP

%description json
Support for JSON (JavaScript Object Notation) serialization.


%package ldap
Summary:	LDAP extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	openldap-devel
BuildRequires:	libsasl-devel

%description ldap
This is a dynamic shared object (DSO) for PHP that will add LDAP support.

LDAP is the Lightweight Directory Access Protocol, and is a protocol used to
access "Directory Servers". The Directory is a special kind of database that
holds information in a tree structure.

The concept is similar to your hard disk directory structure, except that in
this context, the root directory is "The world" and the first level
subdirectories are "countries". Lower levels of the directory structure contain
entries for companies, organisations or places, while yet lower still we find
directory entries for people, and perhaps equipment or documents.


%package mbstring
Summary:	MBstring extension module for PHP
Epoch:		0
Group:		Development/PHP

%description mbstring
This is a dynamic shared object (DSO) for PHP that will add multibyte string
support.

mbstring provides multibyte specific string functions that help you deal with
multibyte encodings in PHP. In addition to that, mbstring handles character
encoding conversion between the possible encoding pairs. mbstring is designed
to handle Unicode-based encodings such as UTF-8 and UCS-2 and many single-byte
encodings for convenience.


%package mcrypt
Summary:	Mcrypt extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	libmcrypt-devel
BuildRequires:	libtool-devel

%description mcrypt
This is a dynamic shared object (DSO) for PHP that will add mcrypt support.

This is an interface to the mcrypt library, which supports a wide variety of
block algorithms such as DES, TripleDES, Blowfish (default), 3-WAY, SAFER-SK64,
SAFER-SK128, TWOFISH, TEA, RC2 and GOST in CBC, OFB, CFB and ECB cipher modes.
Additionally, it supports RC6 and IDEA which are considered "non-free".


%package mhash
Summary:	Mhash extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	mhash-devel

%description mhash
This is a dynamic shared object (DSO) for PHP that will add mhash support.

These functions are intended to work with mhash. Mhash can be used to create
checksums, message digests, message authentication codes, and more.

This is an interface to the mhash library. mhash supports a wide variety of
hash algorithms such as MD5, SHA1, GOST, and many others. For a complete list
of supported hashes, refer to the documentation of mhash. The general rule is
that you can access the hash algorithm from PHP with MHASH_HASHNAME. For
example, to access TIGER you use the PHP constant MHASH_TIGER.


%package mime_magic
Summary:	The MIME Magic module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	httpd-conf

%description mime_magic
This is a dynamic shared object (DSO) that adds MIME Magic support to PHP.

The functions in this module try to guess the content type and encoding of a
file by looking for certain magic byte sequences at specific positions within
the file. While this is not a bullet proof approach the heuristics used do a
very good job.

This extension is derived from Apache mod_mime_magic, which is itself based on
the file command maintained by Ian F. Darwin. See the source code for further
historic and copyright information.


%package	mysql
Summary:	MySQL database module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	mysql-devel >= 4.0.10

%description mysql
This is a dynamic shared object (DSO) for PHP that will add MySQL database
support.

These functions allow you to access MySQL database servers. More information
about MySQL can be found at http://www.mysql.com/.

Documentation for MySQL can be found at http://dev.mysql.com/doc/.


%package mysqli
Summary:	MySQL database module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	mysql-devel >= 4.1.7

%description mysqli
This is a dynamic shared object (DSO) for PHP that will add MySQL database
support.

The mysqli extension allows you to access the functionality provided by MySQL
4.1 and above. More information about the MySQL Database server can be found at
http://www.mysql.com/

Documentation for MySQL can be found at http://dev.mysql.com/doc/.


%package ncurses
Summary:	Ncurses module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	ncurses-devel

%description ncurses
This PHP module adds support for ncurses functions (only for cli and cgi
SAPIs).


%package odbc
Summary:	ODBC extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	unixODBC-devel >= 2.2.1

%description odbc
This is a dynamic shared object (DSO) for PHP that will add ODBC support.

In addition to normal ODBC support, the Unified ODBC functions in PHP allow you
to access several databases that have borrowed the semantics of the ODBC API to
implement their own API. Instead of maintaining multiple database drivers that
were all nearly identical, these drivers have been unified into a single set of
ODBC functions.


%package pcntl
Summary:	Process Control extension module for PHP
Epoch:		0
Group:		Development/PHP

%description pcntl
This is a dynamic shared object (DSO) for PHP that will add process spawning
and control support. It supports functions like fork(), waitpid(), signal()
etc.

Process Control support in PHP implements the Unix style of process creation,
program execution, signal handling and process termination. Process Control
should not be enabled within a webserver environment and unexpected results may
happen if any Process Control functions are used within a webserver
environment.


%package pdo
Summary:	PHP Data Objects Interface
Epoch:		0
Group:		Development/PHP

%description pdo
PDO provides a uniform data access interface, sporting advanced features such
as prepared statements and bound parameters. PDO drivers are dynamically
loadable and may be developed independently from the core, but still accessed
using the same API.

Read the documentation at http://www.php.net/pdo for more information.


%package pdo_mysql
Summary:	MySQL Interface driver for PDO
Epoch:		0
Group:		Development/PHP
Requires:	php-pdo >= 0:%{version}

%description pdo_mysql
PDO_MYSQL is a driver that implements the PHP Data Objects (PDO) interface to
enable access from PHP to MySQL 3.x and 4.x databases.

PDO_MYSQL will take advantage of native prepared statement support present in
MySQL 4.1 and higher. If you're using an older version of the mysql client
libraries, PDO will emulate them for you.


%package pdo_odbc
Summary:	ODBC v3 Interface driver for PDO
Epoch:		0
Group:		Development/PHP
BuildRequires:	unixODBC-devel
Requires:	php-pdo >= 0:%{version}

%description pdo_odbc
PDO_ODBC is a driver that implements the PHP Data Objects (PDO) interface to
enable access from PHP to databases through ODBC drivers or through the IBM DB2
Call Level Interface (DB2 CLI) library. PDO_ODBC currently supports three
different "flavours" of database drivers:
 
 o ibm-db2  - Supports access to IBM DB2 Universal Database, Cloudscape, and
              Apache Derby servers through the free DB2 client. ibm-db2 is not
	      supported in Mandriva.

 o unixODBC - Supports access to database servers through the unixODBC driver
              manager and the database's own ODBC drivers. 

 o generic  - Offers a compile option for ODBC driver managers that are not
              explicitly supported by PDO_ODBC. 


%package pdo_pgsql
Summary:	PostgreSQL interface driver for PDO
Epoch:		0
Group:		Development/PHP
BuildRequires:	postgresql-devel
Requires:	php-pdo >= 0:%{version}

%description pdo_pgsql
PDO_PGSQL is a driver that implements the PHP Data Objects (PDO) interface to
enable access from PHP to PostgreSQL databases.


%package pdo_sqlite
Summary:	SQLite v3 Interface driver for PDO
Epoch:		0
Group:		Development/PHP
BuildRequires:	sqlite3-devel
Requires:	php-pdo >= 0:%{version}

%description pdo_sqlite
PDO_SQLITE is a driver that implements the PHP Data Objects (PDO) interface to
enable access to SQLite 3 databases.

This extension provides an SQLite v3 driver for PDO. SQLite V3 is NOT
compatible with the bundled SQLite 2 in PHP 5, but is a significant step
forwards, featuring complete utf-8 support, native support for blobs, native
support for prepared statements with bound parameters and improved concurrency.

%package pgsql
Summary:	PostgreSQL database module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	postgresql-devel
BuildRequires:	openssl-devel

%description pgsql
This is a dynamic shared object (DSO) for PHP that will add PostgreSQL database
support.

PostgreSQL database is Open Source product and available without cost.
Postgres, developed originally in the UC Berkeley Computer Science Department,
pioneered many of the object-relational concepts now becoming available in some
commercial databases. It provides SQL92/SQL99 language support, transactions,
referential integrity, stored procedures and type extensibility. PostgreSQL is
an open source descendant of this original Berkeley code.


%package readline
Summary:	Readline extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel

%description readline
This PHP module adds support for readline functions (only for cli and cgi
SAPIs).

The readline() functions implement an interface to the GNU Readline library.
These are functions that provide editable command lines. An example being the
way Bash allows you to use the arrow keys to insert characters or scroll
through command history. Because of the interactive nature of this library, it
will be of little use for writing Web applications, but may be useful when
writing scripts used from a command line.


%package shmop
Epoch:		0
Summary:	Shared Memory Operations extension module for PHP
Group:		Development/PHP

%description shmop
This is a dynamic shared object (DSO) for PHP that will add Shared Memory
Operations support.

Shmop is an easy to use set of functions that allows PHP to read, write, create
and delete Unix shared memory segments.


%package snmp
Summary:	NET-SNMP extension module for PHP
Epoch:		0
Group:		Development/PHP
Requires:	net-snmp-mibs
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	elfutils-devel

%description snmp
This is a dynamic shared object (DSO) for PHP that will add SNMP support using
the NET-SNMP libraries.

In order to use the SNMP functions you need to install the NET-SNMP package.


%package soap
Summary:	Soap extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	libxml2-devel

%description soap
This is a dynamic shared object (DSO) for PHP that will add soap support.

The SOAP extension can be used to write SOAP Servers and Clients. It supports
subsets of SOAP 1.1, SOAP 1.2 and WSDL 1.1 specifications.


%package sockets
Summary:	Sockets extension module for PHP
Epoch:		0
Group:		Development/PHP

%description sockets
This is a dynamic shared object (DSO) for PHP that will add sockets support.

The socket extension implements a low-level interface to the socket
communication functions based on the popular BSD sockets, providing the
possibility to act as a socket server as well as a client.


%package sqlite
Summary:	SQLite database bindings for PHP
Epoch:		0
Group:		Development/PHP
Requires:	php-pdo >= 0:%{version}
#BuildRequires:	sqlite-devel

%description sqlite
This is an extension for the SQLite Embeddable SQL Database Engine. SQLite is a
C library that implements an embeddable SQL database engine. Programs that link
with the SQLite library can have SQL database access without running a separate
RDBMS process.

SQLite is not a client library used to connect to a big database server. SQLite
is the server. The SQLite library reads and writes directly to and from the
database files on disk.


%package sysvmsg
Summary:	SysV msg extension module for PHP
Epoch:		0
Group:		Development/PHP

%description sysvmsg
This is a dynamic shared object (DSO) for PHP that will add SysV message queues
support.


%package wddx
Summary:	WDDX serialization functions
Epoch:		0
Group:		Development/PHP
BuildRequires:  expat-devel

%description wddx
This is a dynamic shared object (DSO) that adds wddx support to PHP. 

These functions are intended for work with WDDX (http://www.openwddx.org/)


%package xmlreader
Summary:	Xmlreader extension module for PHP
Epoch:		0
Group:		Development/PHP
Requires:	php-dom
BuildRequires:	libxml2-devel

%description xmlreader
XMLReader represents a reader that provides non-cached, forward-only access to
XML data. It is based upon the xmlTextReader api from libxml


%package xmlrpc
Summary:	Xmlrpc extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	expat-devel
BuildRequires:	libxmlrpc-devel

%description xmlrpc
This is a dynamic shared object (DSO) for PHP that will add XMLRPC support.

These functions can be used to write XML-RPC servers and clients. You can find
more information about XML-RPC at http://www.xmlrpc.com/, and more
documentation on this extension and its functions at
http://xmlrpc-epi.sourceforge.net/.


%package xmlwriter
Summary:	Provides fast, non-cached, forward-only means to write XML data
Epoch:		0
Group:		Development/PHP
BuildRequires:	libxml2-devel

%description xmlwriter
This extension wraps the libxml xmlWriter API. Represents a writer that
provides a non-cached, forward-only means of generating streams or files
containing XML data.


%package xsl
Summary:	Xsl extension module for PHP
Epoch:		0
Group:		Development/PHP
BuildRequires:	libxslt-devel
BuildRequires:	libxml2-devel

%description xsl
This is a dynamic shared object (DSO) for PHP that will add xsl support.

The XSL extension implements the XSL standard, performing XSLT transformations
using the libxslt library


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.



%prep
%setup -q -n php-%{version}
# use .avx suffix to delete patch backups so they don't end up in php-devel
%patch0 -p0 -b .init.avx
%patch1 -p1 -b .shared.avx
%patch3 -p1 -b .64bit.avx
%patch5 -p0 -b .libtool.avx
%patch6 -p1 -b .no_egg.avx
%patch7 -p1 -b .phpize.avx
%patch8 -p0 -b .remove_bogus_iconv_deps.avx
%patch9 -p1 -b .phpbuilddir.avx
%patch10 -p0 -b .apache2-filters.avx
%patch11 -p1 -b .extension_dep_macro_revert.avx
%patch12 -p0 -b .no_libedit.avx
%patch13 -p0 -b .extraimapcheck.avx
# from PLD
%patch20 -p0 -b .mail.avx
%patch21 -p1 -b .sybase-fix.avx
%patch25 -p0 -b .dba-link.avx
%patch27 -p1 -b .zlib-for-getimagesize.avx
%patch28 -p1 -b .zlib.avx
# from Fedora
%patch50 -p0 -b .cxx.avx
%patch51 -p0 -b .install.avx
%patch53 -p0 -b .umask.avx
#
%patch71 -p1 -b .shutdown.avx
%patch72 -p0 -b .dlopen.avx
#
#%patch73 -p1 -b .tests-dashn.avx
%patch74 -p1 -b .tests-wddx.avx

# make the tests worky
%patch76 -p0 -b .bug29119.avx
%patch77 -p0 -b .cve-2005-3388.avx
%patch78 -p0 -b .libc-client-php.avx
%patch80 -p1 -b .cve-2006-6383.avx

%patch100 -p1 -b .suhosin.avx

# remove bogus checks
rm -f ext/recode/config9.m4

# Change perms otherwise rpm would get fooled while finding requires
find -name "*.inc" | xargs chmod 0644
find -name "*.php*" | xargs chmod 0644
find -name "*README*" | xargs chmod 0644

mkdir -p php-devel/extensions
mkdir -p php-devel/sapi

# cleanup php-devel
cp -a tests php-devel/

cp -dpR ext/* php-devel/extensions/
rm -f php-devel/extensions/informix/stub.c
rm -f php-devel/extensions/standard/.deps
rm -f php-devel/extensions/skeleton/EXPERIMENTAL
rm -f php-devel/extensions/ncurses/EXPERIMENTAL

# windows sources are not wanted
rm -rf php-devel/extensions/com_dotnet

cp -dpR sapi/* php-devel/sapi/ 
rm -f php-devel/sapi/thttpd/stub.c
rm -f php-devel/sapi/cgi/php.sym
rm -f php-devel/sapi/fastcgi/php.sym
rm -f php-devel/sapi/pi3web/php.sym

# remove other unwanted files
find php-devel -name "*.dsp" | xargs rm -f
find php-devel -name "*.mak" | xargs rm -f
find php-devel -name "*.w32" | xargs rm
find php-devel -name "*.avx" | xargs rm -f

# make sure we use the system libs
rm -rf ext/pcre/pcrelib
rm -rf ext/xmlrpc/libxmlrpc


%build
%serverbuild

cat > php-devel/buildext <<EOF
#!/bin/bash
gcc -Wall -fPIC -shared %{optflags} \\
    -I. \`%{_bindir}/php-config --includes\` \\
    -I%{_includedir}/libxml2 \\
    -I%{_includedir}/freetype \\
    -I%{_includedir}/openssl \\
    -I%{_usrsrc}/php-devel/ext \\
    -I%{_includedir}/\$1 \\
    \$4 \$2 -o \$1.so \$3 -lc
EOF

chmod 0755 php-devel/buildext

# this _has_ to be executed!
#export WANT_AUTOCONF_2_5=1

rm -f configure; aclocal-1.7 && autoconf --force && autoheader
#./buildconf --force

perl -pi -e "s|'\\\$install_libdir'|'%{_libdir}'|" ltmain.sh

export oldstyleextdir=yes
export EXTENSION_DIR="%{_libdir}/php/extensions"
export PROG_SENDMAIL="%{_sbindir}/sendmail"
export CFLAGS="%{optflags} -fPIC -L%{_libdir}"
export GD_SHARED_LIBADD="$GD_SHARED_LIBADD -lm"

# never use "--disable-rpath", it does the opposite
# Configure php
for i in cgi cli fcgi apxs; do
    ./configure \
        `[ $i = apxs ] && echo --with-apxs2=%{_sbindir}/apxs` \
        `[ $i = fcgi ] && echo --enable-fastcgi --with-fastcgi=%{_prefix} --disable-cli --enable-force-cgi-redirect` \
        `[ $i = cgi ] && echo --enable-discard-path --disable-cli --enable-force-cgi-redirect` \
        `[ $i = cli ] && echo --disable-cgi --enable-cli` \
        --cache-file=config.cache \
        --build=%{_build} \
        --prefix=%{_prefix} \
        --exec-prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --enable-shared=yes \
        --enable-static=no \
        --with-libdir=%{_lib} \
        --with-config-file-path=%{_sysconfdir} \
        --with-config-file-scan-dir=%{_sysconfdir}/php.d \
        --disable-debug \
        --enable-pic \
        --enable-inline-optimization \
        --with-exec-dir=%{_bindir} \
        --with-pcre=%{_prefix} \
        --with-pcre-dir=%{_prefix} \
        --with-pcre-regex=%{_prefix} \
        --with-ttf=%{_prefix} \
        --with-freetype-dir=%{_prefix} \
        --with-png-dir=%{_prefix} \
        --with-jpeg-dir=%{_prefix} \
        --with-xpm-dir=%{_prefix} \
        --with-regex=php \
        --enable-magic-quotes \
        --enable-safe-mode \
        --with-zlib=%{_prefix} \
        --with-zlib-dir=%{_prefix} \
        --with-openssl=%{_prefix} \
        --with-openssl-dir=%{_prefix} \
        --enable-libxml=%{_prefix} \
        --with-libxml-dir=%{_prefix} \
        --enable-spl=%{_prefix} \
        --enable-track-vars \
        --enable-trans-sid \
        --enable-memory-limit \
        --with-versioning \
        --enable-mod_charset \
        --with-pear=%{_datadir}/pear \
        --enable-xml \
        --enable-bcmath=shared,%{_prefix} \
        --with-bz2=shared,%{_prefix} \
        --enable-calendar=shared \
        --enable-ctype \
        --with-curl=shared,%{_prefix} --without-curlwrappers \
        --enable-dba=shared --with-gdbm --with-db4 --with-cdb --with-flatfile --with-inifile \
        --enable-dbase=shared \
        --enable-dom=shared,%{_prefix} \
        --enable-exif=shared \
        --disable-filter \
        --enable-json=shared \
        --enable-ftp \
        --with-gd=shared --enable-gd-native-ttf \
        --with-gettext=%{_prefix} \
        --with-gmp=shared,%{_prefix} \
        --enable-hash=%{_prefix} \
        --with-iconv=shared \
        --without-imap \
        --with-ldap=shared,%{_prefix} --with-ldap-sasl=%{_prefix} \
        --enable-mbstring=shared,%{_prefix} --enable-mbregex \
        --with-mcrypt=shared,%{_prefix} \
        --with-mhash=shared,%{_prefix} \
        --with-mime-magic=shared,%{_sysconfdir}/httpd/conf/magic \
        --with-mysql=shared,%{_prefix} --with-mysql-sock=%{_localstatedir}/mysql/mysql.sock \
        --with-mysqli=shared,%{_bindir}/mysql_config \
        --with-ncurses=shared,%{_prefix} \
        --with-unixODBC=shared,%{_prefix} \
        --enable-pcntl=shared \
        --enable-pdo=shared,%{_prefix} \
            --with-pdo-mysql=shared,%{_prefix} --with-pdo-odbc=shared,unixODBC,%{_prefix} \
            --with-pdo-pgsql=shared,%{_prefix} --with-pdo-sqlite=shared,%{_prefix} --without-pdo-dblib \
        --with-pgsql=shared,%{_prefix} \
        --enable-posix \
        --with-readline=shared,%{_prefix} \
        --enable-session=%{_prefix} \
        --enable-shmop=shared,%{_prefix} \
        --enable-simplexml=%{_prefix} \
        --with-snmp=shared,%{_prefix} --enable-ucd-snmp-hack \
        --enable-soap=shared,%{_prefix} \
        --enable-sockets=shared,%{_prefix} \
        --with-sqlite=shared \
        --enable-sysvmsg=shared,%{_prefix} \
        --enable-sysvsem=%{_prefix} \
        --enable-sysvshm=%{_prefix} \
        --enable-tokenizer=%{_prefix} \
        --enable-wddx=shared \
        --with-xmlrpc=shared,%{_prefix} --with-expat-dir=shared,%{_prefix} \
        --enable-xmlreader=shared,%{_prefix} \
        --enable-xmlwriter=shared,%{_prefix} \
        --with-xsl=shared,%{_prefix} \
        --enable-reflection=shared

    cp -f Makefile Makefile.$i
    cp -f main/php_config.h php_config.h.$i

    perl -pi -e 's|-prefer-non-pic -static||g' Makefile.$i
done

# remove all confusion...
perl -pi -e "s|^#define CONFIGURE_COMMAND .*|#define CONFIGURE_COMMAND \"This is irrelevant, look inside the %{_docdir}/libphp_common%{libversion}-%{version}/configure_command file.  Use apt-get to install any extensions not shown below.\"|g" main/build-defs.h
cp config.nice configure_command; chmod 0644 configure_command

%make

cp -af sapi/cgi sapi/cgi.org
# make php-fcgi
cp -af php_config.h.fcgi main/php_config.h
%make -f Makefile.fcgi sapi/cgi/php-cgi
mv sapi/cgi sapi/fcgi
mv sapi/cgi.org sapi/cgi
perl -pi -e "s|sapi/cgi|sapi/fcgi|g" sapi/fcgi/php

# make php-cgi
cp -af php_config.h.cgi main/php_config.h
%make -f Makefile.cgi sapi/cgi/php-cgi

cp -af php_config.h.apxs main/php_config.h


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/php/extensions
mkdir -p %{buildroot}%{_usrsrc}/php-devel
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/php.d

make -f Makefile.apxs install \
    INSTALL_ROOT=%{buildroot} \
    INSTALL_IT="\$(LIBTOOL) --mode=install install libphp5_common.la %{buildroot}%{_libdir}/" \
    INSTALL_CLI="\$(LIBTOOL) --silent --mode=install install sapi/cli/php %{buildroot}%{_bindir}/php"

./libtool --silent --mode=install install sapi/fcgi/php-cgi %{buildroot}%{_bindir}/php-fcgi
./libtool --silent --mode=install install sapi/cgi/php-cgi %{buildroot}%{_bindir}/php-cgi

cp -dpR php-devel/* %{buildroot}%{_usrsrc}/php-devel/
install -m 0644 run-tests*.php %{buildroot}%{_usrsrc}/php-devel/
install -m 0644 main/internal_functions.c %{buildroot}%{_usrsrc}/php-devel/
install -m 0755 scripts/phpize %{buildroot}%{_bindir}/
install -m 0755 scripts/php-config %{buildroot}%{_bindir}/

install -m 0644 sapi/cli/php.1 %{buildroot}%{_mandir}/man1/
install -m 0644 scripts/man1/phpize.1 %{buildroot}%{_mandir}/man1/
install -m 0644 scripts/man1/php-config.1 %{buildroot}%{_mandir}/man1/

ln -snf extensions %{buildroot}%{_usrsrc}/php-devel/ext

# extensions
echo "extension = bz2.so"	> %{buildroot}%{_sysconfdir}/php.d/10_bz2.ini
echo "extension = bcmath.so"	> %{buildroot}%{_sysconfdir}/php.d/66_bcmath.ini
echo "extension = calendar.so"	> %{buildroot}%{_sysconfdir}/php.d/11_calendar.ini
echo "extension = curl.so"	> %{buildroot}%{_sysconfdir}/php.d/13_curl.ini
echo "extension = dba.so"	> %{buildroot}%{_sysconfdir}/php.d/14_dba.ini
echo "extension = dbase.so"	> %{buildroot}%{_sysconfdir}/php.d/15_dbase.ini
echo "extension = dom.so"	> %{buildroot}%{_sysconfdir}/php.d/18_dom.ini
cp %{_sourcedir}/php-exif.ini %{buildroot}%{_sysconfdir}/php.d/19_exif.ini
cp %{_sourcedir}/php-gd.ini %{buildroot}%{_sysconfdir}/php.d/23_gd.ini
echo "extension = gmp.so"	> %{buildroot}%{_sysconfdir}/php.d/25_gmp.ini
echo "extension = iconv.so"	> %{buildroot}%{_sysconfdir}/php.d/26_iconv.ini
echo "extension = ldap.so"	> %{buildroot}%{_sysconfdir}/php.d/27_ldap.ini
echo "extension = mbstring.so"	> %{buildroot}%{_sysconfdir}/php.d/29_mbstring.ini
cp %{_sourcedir}/php-mcrypt.ini %{buildroot}%{_sysconfdir}/php.d/29_mcrypt.ini
echo "extension = mhash.so"	> %{buildroot}%{_sysconfdir}/php.d/30_mhash.ini
cp %{_sourcedir}/php-mime_magic.ini %{buildroot}%{_sysconfdir}/php.d/31_mime_magic.ini
cp %{_sourcedir}/php-mysql.ini %{buildroot}%{_sysconfdir}/php.d/34_mysql.ini
cp %{_sourcedir}/php-mysqli.ini %{buildroot}%{_sysconfdir}/php.d/37_mysqli.ini
echo "extension = ncurses.so"		> %{buildroot}%{_sysconfdir}/php.d/38_ncurses.ini
cp %{_sourcedir}/php-odbc.ini %{buildroot}%{_sysconfdir}/php.d/39_odbc.ini
echo "extension = pcntl.so"		> %{buildroot}%{_sysconfdir}/php.d/40_pcntl.ini
echo "extension = pdo.so"		> %{buildroot}%{_sysconfdir}/php.d/70_pdo.ini
echo "extension = pdo_mysql.so"		> %{buildroot}%{_sysconfdir}/php.d/73_pdo_mysql.ini
echo "extension = pdo_odbc.so"		> %{buildroot}%{_sysconfdir}/php.d/75_pdo_odbc.ini
echo "extension = pdo_pgsql.so"		> %{buildroot}%{_sysconfdir}/php.d/76_pdo_pgsql.ini
echo "extension = pdo_sqlite.so"	> %{buildroot}%{_sysconfdir}/php.d/77_pdo_sqlite.ini
cp %{_sourcedir}/php-pgsql.ini %{buildroot}%{_sysconfdir}/php.d/39_pgsql.ini
echo "extension = pgsql.so"		> %{buildroot}%{_sysconfdir}/php.d/39_pgsql.ini
echo "extension = readline.so"		> %{buildroot}%{_sysconfdir}/php.d/41_readline.ini
echo "extension = shmop.so"		> %{buildroot}%{_sysconfdir}/php.d/48_shmop.ini
echo "extension = snmp.so"		> %{buildroot}%{_sysconfdir}/php.d/50_snmp.ini
cp %{_sourcedir}/php-soap.ini %{buildroot}%{_sysconfdir}/php.d/51_soap.ini
cp %{_sourcedir}/php-sockets.ini %{buildroot}%{_sysconfdir}/php.d/52_sockets.ini
cp %{_sourcedir}/php-sqlite.ini %{buildroot}%{_sysconfdir}/php.d/78_sqlite.ini
echo "extension = sysvmsg.so"		> %{buildroot}%{_sysconfdir}/php.d/56_sysvmsg.ini
echo "extension = xmlrpc.so"		> %{buildroot}%{_sysconfdir}/php.d/62_xmlrpc.ini
echo "extension = xmlreader.so"		> %{buildroot}%{_sysconfdir}/php.d/63_xmlreader.ini
echo "extension = xmlwriter.so"		> %{buildroot}%{_sysconfdir}/php.d/64_xmlwriter.ini
echo "extension = xsl.so"		> %{buildroot}%{_sysconfdir}/php.d/63_xsl.ini
echo "extension = wddx.so"		> %{buildroot}%{_sysconfdir}/php.d/63_wddx.ini
echo "extension = json.so"		> %{buildroot}%{_sysconfdir}/php.d/82_json.ini

# fix docs
cp Zend/LICENSE Zend/ZEND_LICENSE
cp README.SELF-CONTAINED-EXTENSIONS SELF-CONTAINED-EXTENSIONS
pushd ext
    for i in `ls -1`
    do
        if [ -f "$i/CREDITS" ]; then
            cp $i/CREDITS ../CREDITS.$i
        fi
        if [ -f "$i/README" ]; then
            cp $i/README ../README.$i
        fi
    done
popd

# cgi docs
cp sapi/cgi/CREDITS CREDITS.cgi

# fcgi docs
cp sapi/cgi/README.FastCGI README.fcgi
cp sapi/cgi/CREDITS CREDITS.fcg

# cli docs
cp sapi/cli/CREDITS CREDITS.cli
cp sapi/cli/README README.cli
cp sapi/cli/TODO TODO.cli

# other docs
cp -a ext/dom/examples php-dom-examples
mkdir php-exif-examples && cp -a ext/exif/{example.php,test.php,test.txt} php-exif-examples/
cp -a ext/simplexml/examples php-simplexml-examples

# house cleaning
rm -f %{buildroot}%{_libdir}/*.a

# fix one strange weirdo
perl -pi -e "s|^libdir=.*|libdir='%{_libdir}'|g" %{buildroot}%{_libdir}/*.la

%multiarch_includes %{buildroot}%{_includedir}/php/main/build-defs.h
%multiarch_includes %{buildroot}%{_includedir}/php/main/config.w32.h
%multiarch_includes %{buildroot}%{_includedir}/php/main/php_config.h

# fix PEAR
rm -rf %{buildroot}/.{channels,depdb,depdblock,filemap,lock}
rm -rf %{buildroot}/%{_datadir}/pear/.{depdb,depdblock,lock}
rm -f %{buildroot}%{_sysconfdir}/pear.conf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%pre cgi
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-fcgi
update-alternatives --remove php %{_bindir}/php-cli


%pre fcgi
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-fcgi
update-alternatives --remove php %{_bindir}/php-cli


%pre cli
update-alternatives --remove php %{_bindir}/php-cgi
update-alternatives --remove php %{_bindir}/php-fcgi
update-alternatives --remove php %{_bindir}/php-cli


%post pear
if [ ! -f /etc/pear.conf ]; then
    echo "Creating initial /etc/pear.conf"
    %{_bindir}/pear config-create /usr/share /etc/pear.conf >/dev/null
    %{_bindir}/pear config-set bin_dir %{_bindir} >/dev/null
    %{_bindir}/pear config-set ext_dir %{_libdir}/php/extensions >/dev/null
    %{_bindir}/pear config-set php_dir %{_datadir}/pear >/dev/null
    # unfortunately, pear's config-set modifies the user's .pearrc instead of the system-wide one
    mv -f $HOME/.pearrc /etc/pear.conf
fi


%files cgi
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php-cgi

%files fcgi
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php-fcgi

%files cli
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php
%attr(0644,root,root) %{_mandir}/man1/php.1*

%files -n %{libname}
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/libphp5_common.so.*

%files devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/php-config
%attr(0755,root,root) %{_bindir}/phpize
%attr(0755,root,root) %{_libdir}/libphp5_common.so
%attr(0755,root,root) %{_libdir}/libphp5_common.la
%dir %{_libdir}/php/build
%{_libdir}/php/build/*
%{_usrsrc}/php-devel
%multiarch %{multiarch_includedir}/php/main/build-defs.h
%multiarch %{multiarch_includedir}/php/main/config.w32.h
%multiarch %{multiarch_includedir}/php/main/php_config.h
%{_includedir}/php
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/phpize.1*

%files pear
%defattr(-,root,root)
%dir %{_datadir}/pear
%{_datadir}/pear/*
%{_datadir}/pear/.filemap
%{_datadir}/pear/.registry
%{_datadir}/pear/.channels
%{_bindir}/pear
%{_bindir}/peardev
%{_bindir}/pecl

%files bcmath 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_bcmath.ini
%attr(0755,root,root) %{_libdir}/php/extensions/bcmath.so

%files bz2 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_bz2.ini
%attr(0755,root,root) %{_libdir}/php/extensions/bz2.so

%files calendar 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_calendar.ini
%attr(0755,root,root) %{_libdir}/php/extensions/calendar.so

%files curl 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_curl.ini
%attr(0755,root,root) %{_libdir}/php/extensions/curl.so

%files dba 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_dba.ini
%attr(0755,root,root) %{_libdir}/php/extensions/dba.so

%files dbase 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_dbase.ini
%attr(0755,root,root) %{_libdir}/php/extensions/dbase.so

%files dom 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_dom.ini
%attr(0755,root,root) %{_libdir}/php/extensions/dom.so

%files exif 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_exif.ini
%attr(0755,root,root) %{_libdir}/php/extensions/exif.so

%files gd 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_gd.ini
%attr(0755,root,root) %{_libdir}/php/extensions/gd.so

%files gmp 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_gmp.ini
%attr(0755,root,root) %{_libdir}/php/extensions/gmp.so

%files iconv 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_iconv.ini
%attr(0755,root,root) %{_libdir}/php/extensions/iconv.so

%files json
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_json.ini
%attr(0755,root,root) %{_libdir}/php/extensions/json.so

%files ldap 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_ldap.ini
%attr(0755,root,root) %{_libdir}/php/extensions/ldap.so

%files mbstring 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_mbstring.ini
%attr(0755,root,root) %{_libdir}/php/extensions/mbstring.so

%files mcrypt 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_mcrypt.ini
%attr(0755,root,root) %{_libdir}/php/extensions/mcrypt.so

%files mhash 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_mhash.ini
%attr(0755,root,root) %{_libdir}/php/extensions/mhash.so

%files mime_magic 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_mime_magic.ini
%attr(0755,root,root) %{_libdir}/php/extensions/mime_magic.so

%files mysql 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_mysql.ini
%attr(0755,root,root) %{_libdir}/php/extensions/mysql.so

%files mysqli 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_mysqli.ini
%attr(0755,root,root) %{_libdir}/php/extensions/mysqli.so

%files ncurses 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_ncurses.ini
%attr(0755,root,root) %{_libdir}/php/extensions/ncurses.so

%files odbc 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_odbc.ini
%attr(0755,root,root) %{_libdir}/php/extensions/odbc.so

%files pcntl 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_pcntl.ini
%attr(0755,root,root) %{_libdir}/php/extensions/pcntl.so

%files pdo
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_pdo.ini
%attr(0755,root,root) %{_libdir}/php/extensions/pdo.so

%files pdo_mysql
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/*_pdo_mysql.ini
%attr(0755,root,root) %{_libdir}/php/extensions/pdo_mysql.so

%files pdo_odbc
%defattr(-,root,root)
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/*_pdo_odbc.ini
%attr(0755,root,root) %{_libdir}/php/extensions/pdo_odbc.so

%files pdo_pgsql
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_pdo_pgsql.ini
%attr(0755,root,root) %{_libdir}/php/extensions/pdo_pgsql.so

%files pdo_sqlite
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_pdo_sqlite.ini
%attr(0755,root,root) %{_libdir}/php/extensions/pdo_sqlite.so

%files pgsql 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_pgsql.ini
%attr(0755,root,root) %{_libdir}/php/extensions/pgsql.so

%files readline 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_readline.ini
%attr(0755,root,root) %{_libdir}/php/extensions/readline.so

%files shmop 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_shmop.ini
%attr(0755,root,root) %{_libdir}/php/extensions/shmop.so

%files snmp 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_snmp.ini
%attr(0755,root,root) %{_libdir}/php/extensions/snmp.so

%files soap 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_soap.ini
%attr(0755,root,root) %{_libdir}/php/extensions/soap.so

%files sockets 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_sockets.ini
%attr(0755,root,root) %{_libdir}/php/extensions/sockets.so

%files sqlite 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_sqlite.ini
%attr(0755,root,root) %{_libdir}/php/extensions/sqlite.so

%files sysvmsg 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_sysvmsg.ini
%attr(0755,root,root) %{_libdir}/php/extensions/sysvmsg.so

%files wddx
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_wddx.ini
%attr(0755,root,root) %{_libdir}/php/extensions/wddx.so

%files xmlreader 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_xmlreader.ini
%attr(0755,root,root) %{_libdir}/php/extensions/xmlreader.so

%files xmlrpc
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_xmlrpc.ini
%attr(0755,root,root) %{_libdir}/php/extensions/xmlrpc.so

%files xmlwriter 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_xmlwriter.ini
%attr(0755,root,root) %{_libdir}/php/extensions/xmlwriter.so

%files xsl 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/*_xsl.ini
%attr(0755,root,root) %{_libdir}/php/extensions/xsl.so

%files doc
%defattr(-,root,root)
%doc CREDITS* README* TODO* Zend/ZEND_*
%doc INSTALL LICENSE NEWS php.ini-dist php.ini-recommended configure_command
%doc SELF-CONTAINED-EXTENSIONS CODING_STANDARDS TODO EXTENSIONS
%doc php-dom-examples
%doc php-exif-examples
%doc php-simplexml-examples


%changelog
* Wed Sep 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.4
- drop P14, merged upstream
- updated P20 from Mandriva
- require the latest suhosin
- use %%serverbuild
- use the bundled json instead of the pecl one

* Wed Sep 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.4
- 5.2.4 (fixes for CVE-2007-2872, CVE-2007-3378, CVE-2007-3997, CVE-2007-3998,
  CVE-2007-4652, CVE-2007-4657, CVE-2007-4658, CVE-2007-4659, CVE-2007-4661,
  CVE-2007-4662, CVE-2007-4663, CVE-2007-4670)
- suhosin patch for 5.2.4
- updated P1, P6, P7 from Mandriva
- dropped old/obsolete patches: P4, P52, P70

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.3
- rebuild with SSP

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.3
- merge all modules we can into this package except filter, json, suhosin, xdebug,
  and imap (all are or have external sources)
- build the following (previously separate) modules directly into php:
  gettext, posix, ctype, session, sysvsem, sysvshm, tokenizer, simplexml,
  hash, ftp (all are needed by -{cli,cgi,fcgi} anyways, so might as well keep
  them constant)
- new php modules: bcmath, dom, dbase, mime_magic, ncurses, pcntl, snmp, sqlite,
  xmlreader, xmlwriter
- php-dba replaces php-dba_bundle
- phpinfo() talks about apt-get rather than urpmi
- dropped P2
- refreshed a bunch of patches from Mandriva (5.2.3-8mdv)
- enable reflection support
- build with the bundled gd library
- don't build php-filter here; the pecl package we were using is newer

* Mon Jun 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.3
- fix the php-fcgi build

* Sun Jun 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.3
- 5.2.3 (fixes for CVE-2007-1887, CVE-2007-1900, CVE-2007-2756, CVE-2007-2872)
- suhosin patch for 5.2.3
- updated P25

* Mon May 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- add php-fcgi

* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- versioned provides
- drop some (useless and inacurrate) provides/obsoletes for php3/php4
- provide/obsolete php-xml; it's been built here for a while now and is
  useful enough to build right into the core

* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- php 5.2.2 (fixes for CVE-2007-1001, CVE-2007-1718, CVE-2007-1717,
  CVE-2007-1649, CVE-2007-1583, CVE-2007-1484, CVE-2007-1521, CVE-2007-1460,
  CVE-2007-1461, CVE-2007-1375, CVE-2007-1285, CVE-2007-1396, CVE-2007-1864)
- updated suhosin (5.2.2-rc2-0.9.6.2)
- drop upstream patches P75, P81
- fix dependency exceptions

* Thu May 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- drop the php-xml and php-xmlrpc requires on php-pear as they don't seem necessary

* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- php 5.2.1
- updated suhosin (5.2.1-0.9.6.2)
- updated P53
- drop P79 - merged upstream
- P13: extra safe_mode/open_basedir checks for imap support from Mandriva

* Wed Feb 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- P80: security fix for CVE-2006-6383
- P81: security fix for CVE-2007-0455
 
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- apache 2.2.4

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- build against new libxml2 and libxslt

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- rebuild against new pam

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- don't install our pear.conf but run the pear command to create the
  config on intial install

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- 5.2.0
- suhosin patch 0.9.6.2
- P78: to make the imap build cleaner
- updated P1, P6 from Mandriva
- drop P22, P24, P26
- drop the buildconflicts on php
- require php-filter and php-json (from pecl) to mimic a default php build
- don't make test
- P79: add support for curl 7.16.0
- produce php-pear here rather than in a separate package

* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- remove the version requirements on php-suhosin since it's using it's
  own version, not php's

* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- P100: use the suhosin patch instead of the hardened patch
- requires php-suhosin

* Thu Sep 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- 5.1.6 (multiple security fixes)
- updated hardening patch

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new openssl
- spec cleanups
- hardening patch 0.4.14
- disable one test that the new hardening patch seems to have broken

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- hardening patch 0.4.12: fixes CVE-2006-2563, CVE-2006-2660, CVE-2006-1990,
  CVE-2006-3011
- spec cleanups

* Sun Jun 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new pam

* Sat Jun 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- rebuild against new libxml2
- really add -doc subpackage
- put all the docs for the various extensions here too

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- 5.1.4
- rediff P1, P6, P11
- updated P4 (no more ext/msession)
- drop P7; merged upstream
- hardened php 5.1.4-0.4.11
- disable tests/basic/021.phpt as it fails even on a vanilla (unpatched)
  5.1.4 so although it claims it's fixed (bug #37276) that doesn't seem to
  be the case
- add -doc subpackage
- rebuild with gcc4

* Mon Apr 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- add some sane default requires for php-cgi and php-cli
- put back the BuildConflicts on php otherwise all the tests fail

* Thu Mar 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- remove .avx files, not .droplet files
- disable the sunfuncts test as it's not 100% precise on x86_64 but it's
  so close the difference is really minor so don't let php fail on this
- find the .avx files after we copy in from sapi/ or we end up missing
  what we patched in there

* Wed Mar 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- 5.1.2
- remove debug conditional build
- add "pear(" to _requires_exceptions
- change group to Development/PHP
- drop S4 (php-test)
- sync most patches with Mandriva's 5.1.2-5mdk
- update various requires and buildrequires
- use php-devel rather than php[ver]-devel
- drop the phpdir, peardir, and phpsrcdir defines

* Wed Jan 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- 4.4.2
- hardening patch 0.4.8 for php 4.4.2
- rediffed P5
- dropped P6; doesn't look like it's needed any longer
- dropped P12; fixed upstream
- add a --without harden option to build without the hardening patch;
  the default is to build with it

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Tue Dec 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-2avx
- P12: fix php bug #35067; should fix a squirrelmail issue
- don't bzip patches or unnecessary source files anymore

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- 4.4.1; fixes several security issues (see http://www.php.net/release_4_4_1.php)
- hardening patch 4.4.1-0.4.5

* Fri Sep 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-2avx
- hardening patch 4.4.0-0.4.3

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-1avx
- 4.4.0
- P100: re-introduce the hardened php stuff (4.4.0-0.4.1)
- rediffed P5, P10, P11 from Mandriva

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-1avx
- 4.3.11: security fixes for CAN-2005-0524, CAN-2005-0525, CAN-2005-1042,
  and CAN-2005-1043
- rediffed patches P5, P7, P9, P10, P23, P24 from Mandriva

* Sat Mar 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-5avx
- rebuild against new libxml2 and libxslt
- enable multiarch stuff

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-4avx
- drop P3 and P8
- drop the hardened-php patch; for one it breaks compatibility with external
  3rd party products (like Zend) and for another including it in the build is
  against the php license
- enable building with -fstack-protector

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-3avx
- rebuild against latest openssl

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-2avx
- include the hardened-php patch (4.3.10-0.2.4)
- drop P55
- drop S5 as it's redundant
- rename S4
- use the lib64 patch from mandrake (P5)
- rediff P21

* Thu Dec 16 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- 4.3.10
- rediff P5, P55, P56
- drop P26

* Wed Sep 29 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- 4.3.9
- rediff P5, P9, P10
- drop P57, P58, P72 (applied upstream)

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-2avx
- P72: fix anthill #965; patch from CVS

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
- 4.3.8; security fix for CAN-2004-0594 and CAN-2004-0595
- remove %%build_propolice macro
- enforce new patch-naming policy
- sync with 4.3.7-5mdk:
  - remove the ADVXpackage provides (oden)
  - sync with fedora (P57, P58) (4.3.7-3) (oden)
  - fix deps
  - add P11 (fixes one minor annoyance while running the tests) (oden)
  - add P56 (fedora) (oden)
  - nuke some patch -b backups as they pollute the -devel package (oden)
  - rediffed P5, P21, P22 (oden)
  - added P23-P29 from PLD, slightly adjusted (oden)
  - added P21-P25 from fedora (oden)
  - use the %%configure2_5x macro (oden)
  - added P10 to make phpize work (oden)
  - move scandir to /etc/php.d (oden)
  - rediffed P1 and P20 (oden)
  - drop P40, it's included (oden)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- 4.3.7

* Tue Apr 13 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- 4.3.6
- more epoch fixes
- don't build with %%debug by default
- fix bug22414.phpbt (jmd)
- rediff P1, P20 (oden)
- spec cleanups/macros/etc. (oden)
- libversion is 4, not 432
- remove some unneeded BuildConflicts, Obsoletes, and Provides

* Tue Apr 13 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-5sls
- fix epoch in requires

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-4sls
- minor spec cleanups

* Fri Jan 09 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-3sls
- rediff P5; fix lib64 build (aka php-dba_bundle wasn't compiling)

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec
- use %%build_propolice to add -fno-stack-protector until we can sort out
  the build problems with __guard/etc. symbols

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
