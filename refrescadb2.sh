export JANGY_PROJECT='/home/Cesarsoriano85/Paiton/Paiton'
export BPYTHON_INIT_SCRIPT='${JANGY_PROJECT}/utils/django_shell_imports.py'
export PYTHONPATH="${JANGY_PROJECT}:${PYTHONPATH}"

alias jangy="python manage.py"
alias bp="cd $JANGY_PROJECT && bpython --interactive $BPYTHON_INIT_SCRIPT"


function jangyfresh () {
    tmpdate=$(date "+%Y%m%d-%H%M%S") &&\
    cd $JANGY_PROJECT &&\
    echo "+ Dumping django project database to fixture DUMP-${tmpdate}.json ..." &&\
    python manage.py dumpdata --format='json' --indent=4 --verbosity=1 > datadumps/DUMP-${tmpdate}.json &&\
    echo '+ Backing up sqlite binary store and taking database offline...' &&\
    mv sqlite/data.db sqlite/data.db.bk &&\
    echo '+ Rebuilding database structure from model defs...' &&\
    python manage.py syncdb &&\
    echo '+ Graceful-restarting Apache...' &&\
    sudo apachectl graceful &&\
    echo '+ Enabling write access on new sqlite file...' &&\
    chmod a+rw sqlite/data.db &&\
    echo "+ Reloading project data from fixture dump DUMP-${tmpdate}.json ..." &&\
    python manage.py loaddata datadumps/DUMP-${tmpdate}.json &&\
    echo '+ Rebuilding project database structure...'
}