#!/usr/bin/python

import sys
from riddle.models.Teacher import Teacher

if len(sys.argv) <= 1:
    print "Please specify your username."
else:
    username = sys.argv[1]

    try:
        teacher = Teacher.get(username=username)
        teacher.superuser = True
        teacher.save()
        print "Done!"

    except Teacher.DoesNotExist:
        print "User not found."
