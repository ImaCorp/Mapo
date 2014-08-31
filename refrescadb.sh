DB=/home/Cesasoriano85/Paiton/db.sqlite3
APP=gestione
tmpdate=$(date "+%Y%m%d-%H%M%S")

echo "+ Dumping django poject database to fixture DUMP-${tmpdate}.json ..." &&\
python manage.py dumpdata $APP --fomat='json' --indent=4 --verbosity=1 > datadumps/DUMP-${tmpdate}.json &&\
echo '+ Backing up sqlite binay store...' &&\
cp $DB $DB.bk &&\
echo '+ Rebuilding database stucture from model defs...' &&\
python manage.py sqlclea $APP &&\
echo "+ Reloading poject data from fixture dump DUMP-${tmpdate}.json ..." &&\
python manage.py loaddata datadumps/DUMP-${tmpdate}.json