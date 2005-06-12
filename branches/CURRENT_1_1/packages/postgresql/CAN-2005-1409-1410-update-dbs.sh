#!/bin/sh

db_security_update_CAN_2005_1409_1410() {
    for db in $(su -c '/usr/bin/psql -lt | cut -d\| -f1' postgres); do
        if [ "$db" = template0 ]; then
            continue
        fi

        echo "Applying security update in database $db..."
        su -c "/usr/bin/psql $db" postgres >/dev/null 2>/dev/null <<EOF 
        UPDATE pg_proc
          SET proacl = '{=}'
          WHERE pronamespace = 11 and pronargs = 5 and proargtypes[2] = 'cstring'::regtype;

        UPDATE pg_proc 
          SET proargtypes[0] = 'internal'::regtype
          WHERE oid in (
            'dex_init(text)'::regprocedure,
            'snb_en_init(text)'::regprocedure,
            'snb_ru_init(text)'::regprocedure,
            'spell_init(text)'::regprocedure,
            'syn_init(text)'::regprocedure
          );
EOF
    done

    echo "Applying security update in database template0..."
    su -c "/usr/bin/psql template1" postgres >/dev/null 2>/dev/null <<EOF 
    UPDATE pg_database SET datallowconn = true WHERE datname = 'template0';
    \connect template0;
    UPDATE pg_proc SET proacl = '{=}'
    WHERE pronamespace = 11 AND pronargs = 5
        AND proargtypes[2] = 'cstring'::regtype;
    VACUUM FREEZE;
    \connect template1;
    UPDATE pg_database SET datallowconn = false WHERE datname = 'template0';
EOF
}

db_security_update_CAN_2005_1409_1410
exit 0
