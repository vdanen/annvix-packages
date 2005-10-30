#!/usr/bin/perl -w

###########################################################################
# Author List
##############
# Jaeyeon Jung - MIT CSAIL
# Stuart Schechter - Harvard University DEAS
# Will Stockwell - MIT CSAIL
#
# Copyright (c) 2004 Jaeyeon Jung, Stuart Schechter, Will Stockwell
#                    Cambridge, MA, All rights reserved
#
#######################################################################
# Documentation
################
#
# This script converts each user's known host file from plaintext host
# format to hashed host format (see README.hashed_hosts for details).
# It should be run (as root) once (and only once) after installing the
# hashed hosts patch to OpenSSH.
#
#
# perl convert_known_hosts.pl <options>
#   Standard options:
#   -h           Display this usage message
#   -a           Convert the known_hosts files of all users of this host
#                (as obtained from the password file via getpwent()) as
#                well as known_hosts files /etc/ssh/ (if it exists).
#   -pf <file>   Specify an alternate path to your system passwd file.
#                Default is '/etc/passwd'. This is useful if your
#                system uses NIS or LDAP which can sometimes cause problems
#                for the script on large systems. Tools to generate passwd
#                file style data from NIS and LDAP can avoid these problems.
#                (see README for more information)
#   -x <user>    Exclude <user> from conversion procedures
#                as may be identified using '-a', '-pf', or '-m'.  Multiple
#                '-x' options may be specified.
#
#   Alternate options to find user home directories (instead of -a or -pf):
#   -u <path>    Convert the known_hosts files in the .ssh subdirectory
#                beneath this user home directory path, specified
#                via the <path> value.
#                (e.g. -u /home/johndoe converts /home/johndoe/.ssh/)
#   -m <path>    Like -u, but the <path> specifies a master subdirectory
#                under which there are user subdirectories for which the
#                <path>/<user>/.ssh/ directory contains the known_hosts
#                files to be converted.
#                (e.g. -m /home converts files in /home/*/.ssh/)
#   -r <path>    Location of superuser home directory. Default is '/root'.
#                This is only necessary if you specify '-u' or '-m' options
#                and have located your superuser home directory somewhere
#                unusual
#
#   Observing data conversion:
#   -verbose     Show all data converted as it is converted
#                <default unless -s set to http or mail>
#                (-v is equivalent)
#   -quiet       Convert data silently
#                <default if -s set to http or mail>
#                (-q is equivalent)
#
#   Power-user options:
#   -debug       Turn on debug mode which prevents any files from
#                being modified while allowing the user to see what
#                directories will be traversed and what questions
#                will need to be answered with regard to files
#                other than known_hosts that may contain plaintext
#                hostnames.
#   -d <path>    The exact path of a directory in which known_hosts
#                should be converted.
#   -n <name>    Files of this name are to be treated as known_hosts
#                files and converted to hashed hosts along with files
#                with names matching the defaults:
#                   known_hosts, known_hosts2, (usually found in ~user/.ssh/)
#                   ssh_known_hosts, ssh_knownhosts2, (found in /etc/ssh/)
#                   known_hosts~,known_hosts2~,ssh_known_hosts~, and
#                   ssh_known_hosts2~ (emacs backups of above files) 
#   -pw <passwd> <Warning! - passwd will be visible via ps command> 
#                The password with which to encrypt backups of the
#                old plaintext knownhosts files, the originals of which
#                will be replaced with new known_hosts files with 
#                hashed host entries.  The openssl bf (blowfish)
#                command is used for encryption
#                For maximum security, let the script prompt for the
#                password instead so that it does not appear in ps.
#   -s <dirname> The subdirectory under each user directory in which
#                known_hosts files are stored (default is .ssh/)
#
# NOTES:  Multiple user and/or master home directories may be
#         specified using multiple -u and/or -m options.
#         At least one directory must be specified via -a, -u, or -m.
#
#
# Make sure to use a pass phrase that is not stored or used anywhere
# else on the host.
#
# Should a user wish to recover the plaintext copy of his/her known_hosts
# file as it existed before the script was executed, use the following
# command to decrypt it:
#    openssl bf -d -in  ~<username>/.ssh/known_hosts.backup.bf \
#                  -out ~<username>/.ssh/recovered_plaintext_known_hosts
#
#######################
# Terms and conditions
#######################
# This script is to be integrated into the OpenSSL package and licensed
# under the same terms specified for the rest of the OpenSSH package,
# as copied below.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###########################################################################

use strict;
use File::Glob qw(:globally :nocase);

# The first argument is the directory in which all user home directories
# reside and the second argument is the passphrase to use when encrypting
# backup files.

# A set of root home directories in which home directories are stored
# and that we should traverse for conversion of known_hosts files.
my %MASTER_HOME_PATHS = ();

# A set of the user home directories that we should traverse
# to convert known_hosts files.  Each should have a child directory
# named ".ssh" or such.  Keys are user home directories.  Values are
# references to arrays [ $uid, $username ].  Will be filled with all
# subdirectories of the members of %MASTER_HOME_PATHS.
my %USER_HOME_PATHS = ();

# A set of directories that contain known_hosts files, such as
# ~user/.ssh and /etc/ssh
my %SSH_DIR_PATHS = ();

# A list of file paths that we suspect might contain plaintext hostnames
# but that are not known_host files.
my @SUSPECTS = ();

# Command line option flags
my $CONVERT_ALL_USERS = 0;
my $ROOT_HOME_DIR = "/root/";
my $PASSWD_FILE = "";
my $SAVE_FILE = "";
my @ARG_USER_HOME_PATHS;

my @IGNORE_USERS;
my $VERBOSE = 1;

# When set, debug mode prevents the script from changing the file system
my $DEBUG_MODE = 0;

# The pass_phrase for encryption
my $PASS_PHRASE;

# Set of names known to be used for known_hosts files.
my %IS_KNOWN_HOSTS_FILE_NAME = ("known_hosts" => 1,
				"known_hosts2" => 1,
				"ssh_known_hosts" => 1,
				"ssh_known_hosts2" => 1,
				"known_hosts~" => 1,
				"known_hosts2~" => 1,
				"ssh_known_hosts~" => 1,
				"ssh_known_hosts2~" => 1);

my $USER_SSH_SUBDIR_NAME = ".ssh/";

my $GLOBAL_SSH_CONFIG_DIR = "/etc/ssh/";


##########################################################################
# Subroutine: Convert_File($known_host_file_name)
###
#
# Converts a known_host file, backing up the original to encrypted format
# and moving aside any backups that would be overwritten to filenames
# with dates appended.
#
##########################################################################
sub Convert_File($)
{
    my ($known_hosts_file_name) = (@_);
    my $known_hosts_backup_name = $known_hosts_file_name . ".backup.bf";
    my $known_hosts_temp_file_name = $known_hosts_file_name . ".tmp";
    my $known_hosts_old_file_name = $known_hosts_file_name . ".old";

    if (-e $known_hosts_backup_name) {
	# Copy existing backup file aside to one with a dated name.
	my ($sec,$min,$hour,$day,$mon,$year) = 
	    localtime((stat($known_hosts_backup_name))[9]);
	my $backup_dated = 
	    $known_hosts_file_name .  
	    sprintf(".backup.%04d%02d%02d-%02d%02d%02d.bf",
		    $year + 1900, $mon,$day,$hour,$min,$sec);
	
	rename($known_hosts_backup_name,$backup_dated) unless $DEBUG_MODE;

	print "    old backup file:  $known_hosts_backup_name\n" if $VERBOSE;
	print "    has been renamed: $backup_dated\n" if $VERBOSE;
    }
   
    return if $DEBUG_MODE;

    # Create an encrypted backup copy of the original known_hosts file
    EncryptBF($known_hosts_file_name, $known_hosts_backup_name, $PASS_PHRASE);

    my ($uid, $gid) = (stat $known_hosts_file_name)[4,5];

    # Hash known_hosts entries
    system "ssh-keygen -H -f $known_hosts_file_name";

    # Overwrite data in .old file before unlink'ing
    my $bytes = (stat($known_hosts_old_file_name))[7];
    open (OKH, ">$known_hosts_old_file_name") ||
        die "Unable to open file $known_hosts_old_file_name: $!";
    print OKH "0" x $bytes;
    close (OKH);

    # Remove the unencrypted backup file
    unlink $known_hosts_old_file_name;

    # Ensure correct permissions and ownership are set for the known_hosts file
    chmod (0600, $known_hosts_file_name);
    chown $uid, $gid, ($known_hosts_file_name, $known_hosts_backup_name);
}

#########################################################################
# Subroutine: Remove_Backspaces($line)
###
#
# Process backspaces in user input data so that backspaces actually
# eliminate characters rather than showing up as characters themselves.
#
#########################################################################
sub Remove_Backspaces($)
{
    my ($line) = (@_);
    my $prev;
    do  {
	# Iterate to remove cases of multiple backspaces
	$prev = $line;
	
	# removes a single instance of a backspace and the
	# character that preceeds it.
	$line =~ s/(.|^)[\b]//;

	# repeat until there were no backspaces left to process
    } while ($line ne $prev);

    return $line;
}

#########################################################################
# Subroutine: Get_PassPhrase()
###
#
# Read a line from stdin without echo
# (for reading passwords/passphrases)
#
# No input parameters.
# Returns a string read from stdin with the EOL chopped off.
#########################################################################
sub Get_PassPhrase()
{
    my $phrase;
    # turn character echo at terminal off
    system "stty -echo";
    # remove linefeed
    chop($phrase = <STDIN>);
    # turn character echo at termianl back on
    system "stty echo";
    # since echo was off when return was pressed, echo the line feed now
    print STDERR "\n";

    # process backspaces
    $phrase = Remove_Backspaces($phrase);

    return $phrase;
}

#########################################################################
# Subroutine: EncryptBF($source_path, $dest_path, $pass_phrase)
###
#
# Uses blowfish cipher to encrypt file at $source_path with the key
# string $pass_phrase and writes the results into $dest_path
#########################################################################
sub EncryptBF($$$)
{
    my ($source, $dest, $pass_phrase) = @_;
    open OPENSSL_COMMAND, "| openssl bf -e -in $source -out $dest -pass stdin";
    print OPENSSL_COMMAND $pass_phrase;
    close OPENSSL_COMMAND;
}


#########################################################################
# Subroutine: Ignore_User($user)
###
#
# Returns 1 if user is to be ignored (i.e. included in @IGNORE_USERS list.
# Returns 0 otherwise.
#########################################################################
sub Ignore_User($)
{
    my ($user) = @_;
    foreach (@IGNORE_USERS) {
        return 1 if ($user eq $_);
    }
    
    return 0;
}


#########################################################################
# Subroutine: InvalidUsage
###
#
# Print out the invalid usage message to inform the user that the
# command line parameters provided were invalid.  Then exit to script.
#########################################################################
sub InvalidUsage()
{
    print STDERR <<USAGE;

perl convert_known_hosts.pl <options>
  Standard options:
  -h           Display this usage message
  -a           Convert the known_hosts files of all users of this host
               (as obtained from the password file via getpwent()) as
               well as known_hosts files /etc/ssh/ (if it exists).
  -pf <file>   Specify an alternate path to your system passwd file.
               Default is '/etc/passwd'. This is useful if your
               system uses NIS or LDAP which can sometimes cause problems
               for the script on large systems. Tools to generate passwd
               file style data from NIS and LDAP can avoid these problems.
               (see README for more information)
  -x <user>    Exclude <user> from conversion procedures
               as may be identified using '-a', '-pf', or '-m'.  Multiple
               '-x' options may be specified.

  Alternate options to find user home directories (instead of -a or -pf):
  -u <path>    Convert the known_hosts files in the .ssh subdirectory
               beneath this user home directory path, specified
               via the <path> value.
               (e.g. -u /home/johndoe converts /home/johndoe/.ssh/)
  -m <path>    Like -u, but the <path> specifies a master subdirectory
               under which there are user subdirectories for which the
               <path>/<user>/.ssh/ directory contains the known_hosts
               files to be converted.
               (e.g. -m /home converts files in /home/*/.ssh/)
  -r <path>    Location of superuser home directory. Default is '/root'.
               This is only necessary if you specify '-u' or '-m' options
               and have located your superuser home directory somewhere
               unusual

  Observing data conversion:
  -verbose     Show all data converted as it is converted
               <default unless -s set to http or mail>
               (-v is equivalent)
  -quiet       Convert data silently
               <default if -s set to http or mail>
               (-q is equivalent)

  Power-user options:
  -debug       Turn on debug mode which prevents any files from
               being modified while allowing the user to see what
               directories will be traversed and what questions
               will need to be answered with regard to files
               other than known_hosts that may contain plaintext
               hostnames.
  -d <path>    The exact path of a directory in which known_hosts
               should be converted.
  -n <name>    Files of this name are to be treated as known_hosts
               files and converted to hashed hosts along with files
               with names matching the defaults:
                  known_hosts, known_hosts2, (usually found in ~user/.ssh/)
                  ssh_known_hosts, ssh_knownhosts2, (found in /etc/ssh/)
                  known_hosts~,known_hosts2~,ssh_known_hosts~, and
                  ssh_known_hosts2~ (emacs backups of above files) 
  -pw <passwd> <Warning! - passwd will be visible via ps command> 
               The password with which to encrypt backups of the
               old plaintext knownhosts files, the originals of which
               will be replaced with new known_hosts files with 
               hashed host entries.  The openssl bf (blowfish)
               command is used for encryption
               For maximum security, let the script prompt for the
               password instead so that it does not appear in ps.
  -s <dirname> The subdirectory under each user directory in which
               known_hosts files are stored (default is .ssh/)

NOTES:  Multiple user and/or master home directories may be
        specified using multiple -u and/or -m options.
        At least one directory must be specified via -a, -u, or -m.
USAGE

    exit();
}



##########################################################################
# Main program
###############
#
#                        convert_known_hosts
#
#
##########################################################################

# Parse command line options
while (my $option = shift @ARGV) {
    if ($option eq "-a") {
        if ($PASSWD_FILE ne "") {
            print STDERR "-a and -pf options are mutually exclusive.\n\n";
            InvalidUsage();
        } elsif (scalar(keys %USER_HOME_PATHS) != 0) {
            print STDERR "-a and -u options are mutually exclusive.\n\n";
            InvalidUsage();
        } elsif (scalar(keys %MASTER_HOME_PATHS) != 0) {
            print STDERR "-a and -m options are mutually exclusvie.\n\n";
            InvalidUsage();
        }

	# User has specified to add the home directories of all
	# users available via getpwent() to the list that should
        # be converted

        $CONVERT_ALL_USERS = 1;
    } elsif ($option eq "-d") {
	# User has specified a direct path to a directory containing
	# known_hosts files.
	InvalidUsage() unless my $ssh_dir_path = shift @ARGV;
	$ssh_dir_path .= "/" unless
	    (substr($ssh_dir_path,length($ssh_dir_path)-1,1) eq "/");
	unless (-d $ssh_dir_path) {
	    print STDERR "No such directory: $ssh_dir_path\n\n";
	    exit;
	}
	$SSH_DIR_PATHS{$ssh_dir_path} = 1;
    } elsif ($option eq "-debug") {
	# Run in debug mode, explaining what will be done but not
	# actually doing it.
	$DEBUG_MODE = 1;
    } elsif ($option eq "-h") {
        InvalidUsage();
    } elsif ($option eq "-m") {
        # Avoid argument conflicts
        if ($PASSWD_FILE ne "") {
            print STDERR "-m and -pf options are mutually exclusive.\n\n";
            InvalidUsage();
        } elsif ($CONVERT_ALL_USERS) {
            print STDERR "-m and -a options are mutually exclusive.\n\n";
            InvalidUsage();
        }

	# User has specified a path to a master home directory
	# in which user home directories are located
	InvalidUsage() unless my $master_home_path = shift @ARGV;

        # Grab as many paths as are specified (i.e. looking for next
        # argument or end of the list)
        while (defined $master_home_path) {
            $master_home_path .= "/" unless
                (substr($master_home_path,length($master_home_path)-1,1) eq "/");
            unless (-d $master_home_path) {
                print STDERR "No such directory: $master_home_path\n\n";
                exit;
            }
            $MASTER_HOME_PATHS{$master_home_path} = 1;

            $master_home_path = shift @ARGV;
            if ((! defined($master_home_path)) ||
                $master_home_path =~ /^\-/) { # Next argument
                unshift (@ARGV, $master_home_path); # Put it back in the list
                last;
            }
        } 
    } elsif ($option eq "-n") {
	# Recognize the name specified as a known_hosts file
	InvalidUsage() unless my $known_hosts_file = shift @ARGV;
	$IS_KNOWN_HOSTS_FILE_NAME{$known_hosts_file} = 1;
    } elsif ($option eq "-pf") {
        if ($CONVERT_ALL_USERS) {
            print STDERR "-pf and -a options are mutually exclusive.\n\n";
            InvalidUsage();
        } elsif (scalar(keys %USER_HOME_PATHS) != 0) {
            print STDERR "-pf and -u options are mutually exclusive.\n\n";
            InvalidUsage();
        } elsif (scalar(keys %MASTER_HOME_PATHS) != 0) {
            print STDERR "-pf and -m options are mutually exclusvie.\n\n";
            InvalidUsage();
        }

        # user has specified a passwd file to use instead of getpwent()

        InvalidUsage() unless my $PASSWD_FILE = shift @ARGV;
    } elsif ($option eq "-pw") {
	# User has specified the password to be used to encrypt
	# old known_host files and suspicious files
	InvalidUsage() unless $PASS_PHRASE = shift @ARGV;
    }  elsif ($option eq "-q" || $option eq "-quiet") {
        $VERBOSE = 0;
    } elsif ($option eq "-r") {
        if ($> != 0) {
            print STDERR "Superuser privileges required for $option option\n\n";
            InvalidUsage();
        }

        InvalidUsage() unless $ROOT_HOME_DIR = shift @ARGV;
    } elsif ($option eq "-s") {
	# Use a user subdirectory name other than ".ssh/" to find
	# known_hosts files.
	InvalidUsage() unless $USER_SSH_SUBDIR_NAME = shift @ARGV;
	$USER_SSH_SUBDIR_NAME .= "/" unless
	    (substr($USER_SSH_SUBDIR_NAME,length($USER_SSH_SUBDIR_NAME)-1,1) 
	     eq "/");
    } elsif ($option eq "-u") {
        # Avoid argument conflicts
        if ($PASSWD_FILE ne "") {
            print STDERR "-u and -pf options are mutually exclusive.\n\n";
            InvalidUsage();
        } elsif ($CONVERT_ALL_USERS) {
            print STDERR "-u and -a options are mutually exclusive.\n\n";
            InvalidUsage();
        }

 	# User has specified a path to a user home directory
	InvalidUsage() unless my $user_home_path = shift @ARGV;

        while (defined $user_home_path) {
	    push @ARG_USER_HOME_PATHS, $user_home_path;

            $user_home_path = shift @ARGV;
            if ((! defined($user_home_path)) ||
                $user_home_path =~ /^\-/) { # Next argument
                unshift (@ARGV, $user_home_path); # Put it back in the list
                last;
            }
        }

    } elsif ($option eq "-v" || $option eq "-verbose") {
        $VERBOSE = 1;
    } elsif ($option eq "-x") {
        # Specify that a user is not to have data converted

        InvalidUsage() unless my $exclude_user = shift @ARGV;
        push @IGNORE_USERS, $exclude_user;
        
    } else {
	print STDERR "No such option: $option\n\n";
	InvalidUsage();
    }
}

# Handle the different cases  of how user home directories are found
if ($PASSWD_FILE ne "") {
    open (PW, "$PASSWD_FILE") || die "failed to open password file: $!";
    while(my @pwent = split (":", scalar(<PW>))) {
        my ($user, $user_id, $user_home_path) = @pwent[0, 2, 7];

        next if ignore_user($user);
        $user_home_path .= "/" unless
            (substr($user_home_path,length($user_home_path)-1,1) eq "/");
        $USER_HOME_PATHS{$user_home_path} = [ $user_id, $user ];
    }
    close (PW);

    # Make sure /etc/ssh/ is on list of directories to convert
    $SSH_DIR_PATHS{$GLOBAL_SSH_CONFIG_DIR} = 1;

} elsif (scalar(@ARG_USER_HOME_PATHS) > 0 || 
         scalar(keys %MASTER_HOME_PATHS) > 0) {
    # -m or -u options specified.  Expand -m into user home directories
    # Collection script also requires user IDs and user names so
    # grab them too.  -u options have already been expanded

    my ($user, $user_id, $user_home_path);

    foreach $user_home_path (@ARG_USER_HOME_PATHS) {
	$user_home_path .= "/" unless
	    (substr($user_home_path,length($user_home_path)-1,1) eq "/");
	unless (-d $user_home_path) {
	    print STDERR "No such directory: $user_home_path\n\n";
	    exit;
	}

        $user = (split ("/", $user_home_path))[-1];
	next if Ignore_User($user);
        $user_id = (stat($user_home_path))[4];
	$USER_HOME_PATHS{$user_home_path} = [ $user_id, $user ];
    }

    foreach my $path (keys %MASTER_HOME_PATHS) {
        opendir (DIR, $path) || die "Failed to open directory $path: $!";
        my @subdirs = grep {!/^\./ && -d "$path/$_" } readdir(DIR);
        close (DIR);

        foreach $user (@subdirs) {
            next if Ignore_User($user);
            $user_home_path = "$path/$user";
            $user_id = (stat($user_home_path))[4];
            $USER_HOME_PATHS{$user_home_path} = [ $user_id, $user ];
        }
    }

    # Can't forget to include superuser
    $USER_HOME_PATHS{$ROOT_HOME_DIR} = [ 0, "root" ];
} else {
    while(my @pwent = getpwent()) {
        my ($user, $user_id, $user_home_path) = @pwent[0, 2, 7];

        next if Ignore_User($user);
        $user_home_path .= "/" unless
            (substr($user_home_path,length($user_home_path)-1,1) eq "/");
        $USER_HOME_PATHS{$user_home_path} = [ $user_id, $user ];
    }

    # Make sure /etc/ssh/ is on list of directories to convert
    $SSH_DIR_PATHS{$GLOBAL_SSH_CONFIG_DIR} = 1;

} 


# Make sure at least one directory has been specified
InvalidUsage() unless ( keys %USER_HOME_PATHS );

# Remind user if debug mode is on
if ($DEBUG_MODE) {
    print STDERR "\n******************************DEBUG MODE ON" .
	"****************************\n" .
	"NO FILES OR DIRECTORIES WILL BE MODIFIED DURING THE RUN OF " .
	"THIS SCRIPT.\n\n";

}

# If user hasn't specified a pass_phrase for encryption (-pw option)
# get the password by prompting
unless ($PASS_PHRASE) {
    my $confirm;
    print STDERR "A passphrase is required for encrypting " . 
	    "known_host file backups.\n";

    do {
	print STDERR "Enter pass phrase:  ";
	$PASS_PHRASE = Get_PassPhrase();
	print STDERR  "Confirm pass phrase: ";
	$confirm = Get_PassPhrase();
	print STDERR "Pass phrases did not match.\n"
	    if $PASS_PHRASE ne $confirm;
    } while $PASS_PHRASE ne $confirm;
}


# Add the list of user SSH directories (e.g. ~user/.ssh) to the list
# of general SSH directories to search for known_hosts and the like.
foreach my $user_home_path (sort keys %USER_HOME_PATHS) {
    # Ensure that $user_home_path ends in a '/'
    unless (substr($user_home_path,length($user_home_path)-1,1) eq "/") {
	$user_home_path .= "/";
    }
    # Ensure path exists
    next unless -d $user_home_path;
    # Step into the .ssh directory of that user
    my $user_ssh_path .= $user_home_path . $USER_SSH_SUBDIR_NAME;
    next unless -d $user_ssh_path;
    $SSH_DIR_PATHS{$user_ssh_path} = 1;
}


# Process all directories that may contain known_hosts files,
# converting known_hosts files and backing up the originals
foreach my $ssh_dir_path (sort keys %SSH_DIR_PATHS) {
    # Ensure that $ssh_dir_path ends in a '/'
    unless (substr($ssh_dir_path,length($ssh_dir_path)-1,1) eq "/") {
	$ssh_dir_path .= "/";
    }
    next unless -d $ssh_dir_path;
    next unless opendir(SSH_DIR, $ssh_dir_path);

    print "Inspecting $ssh_dir_path\n" if $VERBOSE;

    my $file;
    while (defined ($file = readdir(SSH_DIR))) {
	# Look at name of each file in the user's ~/.ssh/ directory
	my $filepath = $ssh_dir_path . $file;
	if (-f $filepath && $IS_KNOWN_HOSTS_FILE_NAME{$file}) {
	    # File is a known_host file and must be converted
	    print "  converting $file\n" if $VERBOSE;
	    Convert_File($filepath);
	} elsif (substr($filepath,length($filepath)-3,3) eq ".bf" &&
		 -f $filepath) {
	    # Encrypted back-up file.  No immediate action needed.
	    # (If at risk of being overwritten, it will be backed up
	    #  with date appended in Covert_File subroutine)
	} elsif ($file =~ m/hosts/i || 
		 ($file =~ m/host/i && !($file =~ m/key/i))) {
	    # File looks suspiciously like one that might contains
	    # plaintext host entries in it.  Best to report it
	    # to the administrator running this script.	    
	    push @SUSPECTS, ($filepath);
	}
    }
    closedir(SSH_DIR);
}


# Print out a list of files that look suspiciously like ones that
# might contain plaintext host names (files with "hosts" in their names
# that aren't among the ones we know about.)
if (@SUSPECTS) {
    print "\n\n\n";
    print "    IMPORTANT     IMPORTANT     IMPORTANT     IMPORTANT    \n";
    print "***********************************************************\n";
    print "Please audit the following files to ensure they do not \n";
    print "contain lingering plaintext known_host entries.\n";
    print "***********************************************************\n";
    foreach my $suspect (@SUSPECTS) {
	print "" . $suspect . "\n";
    }

    print "\n\n";
    my $response = "";


    # Step through the list of suspect files again asking the
    # user if they should be encrypted.
    foreach my $suspect (@SUSPECTS) {


	if(-d $suspect) {
	    # Check to see if the suspiciously named directory entry is itself
	    # a directory
	    print STDERR "$suspect is a directory and cannot be directly encrpted.\n";
	    next;
	}
	unless (-f $suspect) {
	    # Make sure that the suspiciously named directory entry is a file
	    print STDERR "$suspect is not a flat file and cannot be directly encrypted.\n";
	    next;
	}
    
	if ($response ne "Y") {
	    # User has yet to specify that they want all (or no) suspect
	    # files encrypted.  Prompt user to ask about this file.
	    print STDERR "Encrypt $suspect?\n";
	    do {
		print STDERR
		"('y' or 'n', capitalize if answer applies to all files):";
		$response = <STDIN>;
		$response = Remove_Backspaces($response);
		$response = substr($response,0,1);
	    } while (uc($response) ne "N" && uc($response) ne "Y");

	    # "N" => stop asking about encrypting suspect files
	    last if $response eq "N";

	    # "n" => don't encrypt this suspect file, but go to next in loop
	    next if $response eq "n";
	}

	next if $DEBUG_MODE;

	# Encrypt the suspicious file to a .bf (blowfish) file
	EncryptBF($suspect, $suspect . ".bf", $PASS_PHRASE);

	# Remove the original suspicious file
	unlink $suspect;
    }

}

