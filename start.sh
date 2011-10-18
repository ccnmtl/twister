#!/bin/bash
cd $1
source ve/bin/activate
exec ve/bin/paster serve $2

