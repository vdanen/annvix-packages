use Apache2 ();

use lib qw(/var/www/perl);

# If the mod_perl-common package is present, enable 
# mod_perl 1.0 compatibility mode.
use Config;
if ( -e "$Config{'vendorarch'}/Apache.pm" ) {
   require Apache::compat
}

use ModPerl::Util (); #for CORE::GLOBAL::exit

use Apache::RequestRec ();
use Apache::RequestIO ();
use Apache::RequestUtil ();

use Apache::ServerRec ();
use Apache::ServerUtil ();
use Apache::Connection ();
use Apache::Log ();

use APR::Table ();

use ModPerl::Registry ();

use Apache::Const -compile => ':common';
use APR::Const -compile => ':common';

1;