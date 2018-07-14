#!/usr/bin/env bash
ndir="*/"
narr=($ndir)
darr=()
for d in ${narr[*]}
do
    [[ $d =~ (static|sailing_dinosaurs) ]] && darr+=($d)
done
for n in ${narr[*]}
do
    makePath=$n"migrations/"
    mkdir $makePath
    initPath=$makePath"__init__.py"
    touch $initPath
done
python3 manage.py makemigrations
for d in ${darr[*]}
do
    deletePath=$d"migrations/"
    rm -R $deletePath
done
python3 manage.py migrate
