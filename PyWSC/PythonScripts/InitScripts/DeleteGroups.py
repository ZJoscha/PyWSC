#!/usr/bin/env python
if __name__ == '__main__':
    import os, sys

    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '..'))

from PythonScripts.Imports import WebService as ws
from PythonScripts.Imports import Utility as util
from PythonScripts.Imports import Config

"""
    Deletes groups from freshly cloned course.
    Due to avoid null-errors in moodle the template course has a few (placeholder) groups for the groupchoice module.
    Or if we reuse an old course several groups may be still in it.
    We want to delete those groups before creating new ones.
"""

# get all groups of course
result_get_course_groups = ws.do_post_on_webservice('core_group_get_course_groups', {'courseid': Config.get_current_course_id()})

payload = {}
for n in range(0, len(result_get_course_groups)):
    #if ('Platzhalter' in result_get_course_groups[n]['name']):
    payload.update({'groupids[' + str(n) + ']': result_get_course_groups[n]['id']})

ws.do_post_on_webservice('core_group_delete_groups', payload)

#wait for user prompt
util.wait_for_user_input_to_keep_console_opened()