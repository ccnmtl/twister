#!/bin/bash
cd $1
source ve/bin/activate
ve/bin/python setup.py develop
exec ve/bin/paster serve $2

