#!/usr/bin/perl -- # -*- Perl -*-w
# $Id$

# Project exists to assist PostgreSQL users with their structural upgrade 
# from 7.2 (or prior) to 7.3 (possibly later).  Must be run against a 7.3
# database system (dump, upgrade daemon, restore, run this script)
#
# - Replace old style Foreign Keys with new style
# - Replace old SERIAL columns with new ones
# - Replace old style Unique Indexes with new style Unique Constraints


# License
# -------
# Copyright (c) 2001, Rod Taylor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1.   Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
# 2.   Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
# 3.   Neither the name of the InQuent Technologies Inc. nor the names
#      of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written
#      permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE FREEBSD
# PROJECT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


use DBI;
use strict;


# Fetch the connection information from the local environment
my $dbuser = $ENV{'PGUSER'};
$dbuser ||= $ENV{'USER'};

my $database = $ENV{'PGDATABASE'};
$database ||= $dbuser;
my $dbisset = 0;

my $dbhost = $ENV{'PGHOST'};
$dbhost ||= "";

my $dbport = $ENV{'PGPORT'};
$dbport ||= "";

my $dbpass = "";

# Yes to all?
my $yes = 0; 

# Whats the name of the binary?
my $basename = $0;
$basename =~ s|.*/([^/]+)$|$1|;

## Process user supplied arguments.
for( my $i=0; $i <= $#ARGV; $i++ ) {
	ARGPARSE: for ( $ARGV[$i] ) {
		/^-d$/			&& do { $database = $ARGV[++$i];
							$dbisset = 1;
							last;
						};

		/^-[uU]$/		&& do { $dbuser = $ARGV[++$i];
							if (! $dbisset) {
								$database = $dbuser;
							}
							last;
						};

		/^-h$/			&& do { $dbhost = $ARGV[++$i]; last; };
		/^-p$/			&& do { $dbport = $ARGV[++$i]; last; };

		/^--password=/	&& do { $dbpass = $ARGV[$i];
							$dbpass =~ s/^--password=//g;
							last;
						};

		/^-Y$/			&& do { $yes = 1; last; };

		/^-\?$/			&& do { usage(); last; };
		/^--help$/		&& do { usage(); last; };
	}
}

# If no arguments were set, then tell them about usage
if ($#ARGV <= 0) {
	print <<MSG

No arguments set.  Use '$basename --help' for help

Connecting to database '$database' as user '$dbuser'

MSG
;
}

my $dsn = "dbi:Pg:dbname=$database";
$dsn .= ";host=$dbhost" if ( "$dbhost" ne "" );
$dsn .= ";port=$dbport" if ( "$dbport" ne "" );

# Database Connection
# -------------------
my $dbh = DBI->connect($dsn, $dbuser, $dbpass);

# We want to control commits
$dbh->{'AutoCommit'} = 0;

END {
	$dbh->disconnect() if $dbh;
}

findUniqueConstraints();
findSerials();
findForeignKeys();

# Find old style Foreign Keys based on:
#
# - Group of 3 triggers of the appropriate types
# - 
sub findForeignKeys
{
	my $sql = qq{
	    SELECT tgargs
	         , tgnargs
	      FROM pg_trigger
	     WHERE NOT EXISTS (SELECT *
	                         FROM pg_depend
	                         JOIN pg_constraint as c ON (refobjid = c.oid)
	                        WHERE objid = pg_trigger.oid
	                          AND deptype = 'i'
	                          AND contype = 'f'
	                      )
	  GROUP BY tgargs
	         , tgnargs
	    HAVING count(*) = 3;
	};
	my $sth = $dbh->prepare($sql);
	$sth->execute() || triggerError($!);

	while (my $row = $sth->fetchrow_hashref)
	{
		# Fetch vars
		my $fkeynargs = $row->{'tgnargs'};
		my $fkeyargs = $row->{'tgargs'};
		my $matchtype = "MATCH SIMPLE";
		my $updatetype = "";
		my $deletetype = "";

		if ($fkeynargs % 2 == 0 && $fkeynargs >= 6) {
			my ( $keyname
			   , $table
			   , $ftable
			   , $unspecified
			   , $lcolumn_name
			   , $fcolumn_name
			   , @junk
			   ) = split(/\000/, $fkeyargs);

			# Account for old versions which don't seem to handle NULL
			# but instead return a string.  Newer DBI::Pg drivers 
			# don't have this problem
			if (!defined($ftable)) {
				( $keyname
				, $table
				, $ftable
				, $unspecified
				, $lcolumn_name
				, $fcolumn_name
				, @junk
				) = split(/\\000/, $fkeyargs);
			}
			else
			{
				# Clean up the string for further manipulation.  DBD doesn't deal well with
				# strings with NULLs in them
				$fkeyargs =~ s|\000|\\000|g;
			}

			# Catch and record MATCH FULL
			if ($unspecified eq "FULL")
			{
				$matchtype = "MATCH FULL";
			}

			# Start off our column lists
			my $key_cols = "$lcolumn_name";
			my $ref_cols = "$fcolumn_name";

			# Perhaps there is more than a single column
			while ($lcolumn_name = shift(@junk) and $fcolumn_name = shift(@junk)) {
				$key_cols .= ", $lcolumn_name";
				$ref_cols .= ", $fcolumn_name";
			}

			my $trigsql = qq{
			  SELECT tgname
			       , relname
			       , proname
			    FROM pg_trigger
			    JOIN pg_proc ON (pg_proc.oid = tgfoid)
			    JOIN pg_class ON (pg_class.oid = tgrelid)
			   WHERE tgargs = ?;
			};

			my $tgsth = $dbh->prepare($trigsql);
			$tgsth->execute($fkeyargs) || triggerError($!);
			my $triglist = "";
			while (my $tgrow = $tgsth->fetchrow_hashref)
			{
				my $trigname = $tgrow->{'tgname'};
				my $tablename = $tgrow->{'relname'};
				my $fname = $tgrow->{'proname'};

				for ($fname)
				{
				/^RI_FKey_cascade_del$/		&& do {$deletetype = "ON DELETE CASCADE"; last;};
				/^RI_FKey_cascade_upd$/		&& do {$updatetype = "ON UPDATE CASCADE"; last;};
				/^RI_FKey_restrict_del$/	&& do {$deletetype = "ON DELETE RESTRICT"; last;};
				/^RI_FKey_restrict_upd$/	&& do {$updatetype = "ON UPDATE RESTRICT"; last;};
				/^RI_FKey_setnull_del$/		&& do {$deletetype = "ON DELETE SET NULL"; last;};
				/^RI_FKey_setnull_upd$/		&& do {$updatetype = "ON UPDATE SET NULL"; last;};
				/^RI_FKey_setdefault_del$/	&& do {$deletetype = "ON DELETE SET DEFAULT"; last;};
				/^RI_FKey_setdefault_upd$/	&& do {$updatetype = "ON UPDATE SET DEFAULT"; last;};
				/^RI_FKey_noaction_del$/	&& do {$deletetype = "ON DELETE NO ACTION"; last;};
				/^RI_FKey_noaction_upd$/	&& do {$updatetype = "ON UPDATE NO ACTION"; last;};
				}

				$triglist .= "	DROP TRIGGER \"$trigname\" ON $tablename;\n";
			}


			my $constraint = "";
			if ($keyname ne "<unnamed>") 
			{
				$constraint = "CONSTRAINT \"$keyname\"";
			}

			my $fkey = qq{
$triglist
	ALTER TABLE $table ADD $constraint FOREIGN KEY ($key_cols)
		 REFERENCES $ftable($ref_cols) $matchtype $updatetype $deletetype;
			};

			# Does the user want to upgrade this sequence?
			print <<MSG
The below commands will upgrade the foreign key style.  Shall I execute them?
$fkey
MSG
;
			if (userConfirm())
			{
				my $sthfkey = $dbh->prepare($fkey);
				$sthfkey->execute() || $dbh->rollback();
				$dbh->commit() || $dbh->rollback();
			}
		}
	}

}

# Find possible old style Serial columns based on:
#
# - Process unique constraints. Unique indexes without
#   the corresponding entry in pg_constraint)
sub findUniqueConstraints
{
	my $sql = qq{
	    SELECT ci.relname AS index_name
             , ct.relname AS table_name
             , pg_catalog.pg_get_indexdef(indexrelid) AS constraint_definition
          FROM pg_class AS ci
          JOIN pg_index ON (ci.oid = indexrelid)
          JOIN pg_class AS ct ON (ct.oid = indrelid)
	      JOIN pg_catalog.pg_namespace ON (ct.relnamespace = pg_namespace.oid)
         WHERE indisunique
           AND NOT EXISTS (SELECT TRUE
                             FROM pg_catalog.pg_depend
	                         JOIN pg_catalog.pg_constraint ON (refobjid = pg_constraint.oid)
                            WHERE objid = indexrelid
                              AND objsubid = 0)
	       AND nspname NOT IN ('pg_catalog', 'pg_toast');
	};
	
	my $sth = $dbh->prepare($sql) || triggerError($!);
	$sth->execute();

	while (my $row = $sth->fetchrow_hashref)
	{
		# Fetch vars
		my $constraint_name = $row->{'index_name'};
		my $table = $row->{'table_name'};
		my $columns = $row->{'constraint_definition'};

		# Extract the columns from the index definition
		$columns =~ s|.*\(([^\)]+)\).*|$1|g;
		$columns =~ s|([^\s]+)[^\s]+_ops|$1|g;

		my $upsql = qq{
DROP INDEX $constraint_name RESTRICT;
ALTER TABLE $table ADD CONSTRAINT $constraint_name UNIQUE ($columns);
		};


		# Does the user want to upgrade this sequence?
		print <<MSG


Upgrade the Unique Constraint style via:
$upsql
MSG
;
		if (userConfirm())
		{
			# Drop the old index and create a new constraint by the same name
			# to replace it.
			my $upsth = $dbh->prepare($upsql);
			$upsth->execute() || $dbh->rollback();

			$dbh->commit() || $dbh->rollback();
		}
	}
}


# Find possible old style Serial columns based on:
#
# - Column is int or bigint
# - Column has a nextval() default
# - The sequence name includes the tablename, column name, and ends in _seq
#   or includes the tablename and is 40 or more characters in length.
sub findSerials
{
	my $sql = qq{
	    SELECT nspname
	         , relname
	         , attname
	         , adsrc
	      FROM pg_catalog.pg_class as c

	      JOIN pg_catalog.pg_attribute as a
	           ON (c.oid = a.attrelid)

	      JOIN pg_catalog.pg_attrdef as ad
	           ON (a.attrelid = ad.adrelid
	           AND a.attnum = ad.adnum)

	      JOIN pg_catalog.pg_type as t
	           ON (t.typname IN ('int4', 'int8')
	           AND t.oid = a.atttypid)

	      JOIN pg_catalog.pg_namespace as n
	           ON (c.relnamespace = n.oid)

	     WHERE n.nspname = 'public'
	       AND adsrc LIKE 'nextval%'
	       AND adsrc LIKE '%'|| relname ||'_'|| attname ||'_seq%'
	       AND NOT EXISTS (SELECT *
	                         FROM pg_catalog.pg_depend as sd
	                         JOIN pg_catalog.pg_class as sc
	                              ON (sc.oid = sd.objid)
	                        WHERE sd.refobjid = a.attrelid
	                          AND sd.refobjsubid = a.attnum
	                          AND sd.objsubid = 0
	                          AND deptype = 'i'
	                          AND sc.relkind = 'S'
	                          AND sc.relname = c.relname ||'_'|| a.attname || '_seq'
	                      );
	};
	
	my $sth = $dbh->prepare($sql) || triggerError($!);
	$sth->execute();

	while (my $row = $sth->fetchrow_hashref)
	{
		# Fetch vars
		my $table = $row->{'relname'};
		my $column = $row->{'attname'};
		my $seq = $row->{'adsrc'};

		# Extract the sequence name from the default
		$seq =~ s|^nextval\(["']+([^'"\)]+)["']+.*\)$|$1|g;

		# Does the user want to upgrade this sequence?
		print <<MSG
Do you wish to upgrade Sequence '$seq' to SERIAL?
Found on column $table.$column
MSG
;
		if (userConfirm())
		{
			# Add the pg_depend entry for the serial column.  Should be enough
			# to fool pg_dump into recreating it properly next time.  The default
			# is still slightly different than a fresh serial, but close enough.
			my $upsql = qq{
			  INSERT INTO pg_catalog.pg_depend
			            ( classid
			            , objid
			            , objsubid
			            , refclassid
			            , refobjid
			            , refobjsubid
			            , deptype
			   ) VALUES ( (SELECT c.oid            -- classid
			                 FROM pg_class as c
			                 JOIN pg_namespace as n
			                      ON (n.oid = c.relnamespace)
			                WHERE n.nspname = 'pg_catalog'
			                  AND c.relname = 'pg_class')

			            , (SELECT c.oid            -- objid
			                 FROM pg_class as c
			                 JOIN pg_namespace as n
			                      ON (n.oid = c.relnamespace)
			                WHERE n.nspname = 'public'
			                  AND c.relname = '$seq')

			            , 0                        -- objsubid

			            , (SELECT c.oid            -- refclassid
			                 FROM pg_class as c
			                 JOIN pg_namespace as n
			                      ON (n.oid = c.relnamespace)
			                WHERE n.nspname = 'pg_catalog'
			                  AND c.relname = 'pg_class')

			            , (SELECT c.oid            -- refobjid
			                 FROM pg_class as c
			                 JOIN pg_namespace as n
			                      ON (n.oid = c.relnamespace)
			                WHERE n.nspname = 'public'
			                  AND c.relname = '$table')

			            , (SELECT a.attnum         -- refobjsubid
			                 FROM pg_class as c
			                 JOIN pg_namespace as n
			                      ON (n.oid = c.relnamespace)
			                 JOIN pg_attribute as a
			                      ON (a.attrelid = c.oid)
			                WHERE n.nspname = 'public'
			                  AND c.relname = '$table'
			                  AND a.attname = '$column')

			            , 'i'                      -- deptype
			            );
			};

			my $upsth = $dbh->prepare($upsql);
			$upsth->execute() || $dbh->rollback();

			$dbh->commit() || $dbh->rollback();
		}
	}
}


#######
# userConfirm
#	Wait for a key press
sub userConfirm
{
	my $ret = 0;
	my $key = "";

	# Sleep for key unless -Y was used
	if ($yes == 1)
	{
		$ret = 1;
		$key = 'Y';
	}

	# Wait for a keypress
	while ($key eq "")
	{
		print "\n << 'Y'es or 'N'o >> : ";
		$key = <STDIN>;

		chomp $key;

		# If it's not a Y or N, then ask again
		$key =~ s/[^YyNn]//g;
	}

	if ($key =~ /[Yy]/)
	{
		$ret = 1;
	}

	return $ret;
}

#######
# triggerError
#	Exit nicely, but print a message as we go about an error
sub triggerError
{
	my $msg = shift;

	# Set a default message if one wasn't supplied
	if (!defined($msg))
	{
		$msg = "Unknown error";
	}

	print $msg;

	exit 1;
}


#######
# usage
#   Script usage
sub usage
{
	print <<USAGE
Usage:
  $basename [options] [dbname [username]]

Options:
  -d <dbname>     Specify database name to connect to (default: $database)
  -h <host>       Specify database server host (default: localhost)
  -p <port>       Specify database server port (default: 5432)
  -u <username>   Specify database username (default: $dbuser)
  --password=<pw> Specify database password (default: blank)

  -Y              The script normally asks whether the user wishes to apply 
                  the conversion for each item found.  This forces YES to all
                  questions.

USAGE
;
	exit 0;
}
