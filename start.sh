#!/bin/bash
cd $1
source working-env/bin/activate
exec working-env/bin/paster serve $2

