use Apache2 ();

use lib qw(/var/www/perl);

# If the mod_perl-common package is present, enable 
# mod_perl 1.0 compatibility mode. Otherwise, we add
# /var/www/perl/.modperl2 to the list of searched directories
# for libraries, so we can, for example, put a dummy Apache::Status
# since it's not present in mod_perl 2.0.
use Config;
if ( -e "$Config{'vendorarch'}/Apache.pm" ) {
   require Apache::compat
} else {
   import lib qw(/var/www/perl/.modperl2); 
}

use ModPerl::Util (); #for CORE::GLOBAL::exit

use Apache::RequestRec ();
use Apache::RequestIO ();
use Apache::RequestUtil ();

use Apache::Server ();
use Apache::ServerUtil ();
use Apache::Connection ();
use Apache::Log ();

use APR::Table ();

use ModPerl::Registry ();

use Apache::Const -compile => ':common';
use APR::Const -compile => ':common';

1;