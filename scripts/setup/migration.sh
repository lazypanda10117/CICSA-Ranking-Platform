# DEPRECATED MIGRATION SCRIPT

#!/usr/bin/env bash
ndir="*/"
narr=($ndir)
darr=()

echo "Setting up Ignored-Directories Vector"

for d in ${narr[*]}
do
    [[ $d =~ (static|misc|init|template|api|scripts) ]] && darr+=($d)
done

echo "Building Migration Directories"

for n in ${darr[*]}
do
    makePath=$n"migrations/"
    rm -R $makePath 2>/dev/null
    mkdir $makePath 2>/dev/null
    initPath=$makePath"__init__.py"
    touch $initPath 2>/dev/null
done

echo "Making Migrations through Django Migration Manager"

python3 manage.py makemigrations

echo "Deleting Migration Directories after Use"

for d in ${darr[*]}
do
    deletePath=$d"migrations/"
    rm -R $deletePath 2>/dev/null
done
