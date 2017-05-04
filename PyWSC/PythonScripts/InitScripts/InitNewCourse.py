#!/usr/bin/env python
"""
    Script for initial course creation. Calls other scripts by simply importing them.
"""
from PythonScripts.Imports import Utility as util

util.ask_user_to_continue('Sind Sie Sicher, dass sie einen neuen Kurs erstellen wollen?\n' \
              'Fortfahren? (ja/j)')
print('Klonen des Template Kurses')
from PythonScripts.InitScripts import CloneCourse
print('Löschen der bestehenden Gruppen')
from PythonScripts.InitScripts import DeleteGroups
print('Erzeugen der Übungsgruppen')
from PythonScripts.InitScripts import CreateGroups
print('Einschreiben des Py-Clients')
from PythonScripts.InitScripts import EnrolClient

# wait for user prompt
util.wait_for_user_input_to_keep_console_opened()

if __name__ == '__main__':
    import os, sys

    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '..'))
