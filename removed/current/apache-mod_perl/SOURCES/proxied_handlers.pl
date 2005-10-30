# $Id: proxied_handlers.pl,v 1.1 2000/03/22 14:14:30 mhz Exp $
#
# This Perl script contains auxiliary handler definitions
# for mod_perl-enhanced Apache server, proxied by other server.
# It is engaged in Apache's config files like this:
# PerlRequire conf/proxied_handlers.pl
#

package Apache::Proxied;

use Apache::Constants qw(OK);

use strict;
use vars qw($PERL_LOC);

# Set this variable to the URL path prefix that is stripped from requests when
# they get proxied.
#
$PERL_LOC = '/perl';

# This handler tries to recover some request parameters as they were in
# the original request for scripts that want to construct local redirects and
# URLs seamlessly from Apache->request->uri or $ENV{SCRIPT_NAME}. Don't use
# REQUEST_URI environment variable though, because it gets overwritten
# deep inside Apache::Registry with the actual request URI, which is, of course,
# specific for the proxied server.
# The Apache::Status handler needs this mechanic too.
# To use this handler, add the following line to your server configuration:
# PerlFixupHandler Apache::Proxied::fixup_handler
#
sub fixup_handler {
    my $r = shift;
    my $uri = $PERL_LOC . $r->uri;
    $r->uri($uri);
    return OK;
}

# This handler helps to restore remote host information to log it properly.
# It retrieves the remote IP address from 'X-Forwarded-For' request header,
# if that exists (such header is usually added by Squid).
# To use this handler, add the following line to your server configuration:
# PerlLogHandler Apache::Proxied::log_handler
#
sub log_handler {
    my $r = shift;
    my $xff = $r->header_in('X-Forwarded-For');
    if ($xff && (my $ip = ($xff =~ /([^,\s]+)$/))) {
        $r->connection->remote_ip($ip);
    }
    return OK;
}

1;
