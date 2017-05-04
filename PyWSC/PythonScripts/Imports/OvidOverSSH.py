#!/usr/bin/env python 3.3
import random

import paramiko as pm

from PythonScripts.Imports import Config
from PythonScripts.Imports import Emails
from PythonScripts.Imports import Utility as util


def write_pw_from_old_group_to_new_group_and_send_email_to_student(matrnr, old_group_name, new_group_name):
    ssh_password = Config.get_ovid_ssh_password()
    git_dir_path = Config.get_ovid_git_dir_path()

    old_group_dir = 'g' + old_group_name
    new_group_dir = 'g' + new_group_name

    old_group_pw_file = old_group_dir + '/.passwd'
    new_group_pw_file = new_group_dir + '/.passwd'

    student = 's' + str(matrnr)

    command_list = [
        'cd ' + git_dir_path,
        'echo ' + ssh_password + ' | sudo -S chmod 666 ' + old_group_pw_file,
        'sudo chmod 666 ' + new_group_pw_file,
        'sudo grep ' + student + ' ' + old_group_pw_file + ' >> ' + new_group_pw_file,
        'sudo chmod 755 ' + old_group_pw_file,
        'sudo chmod 755 ' + new_group_pw_file,
        'sudo chmod 666 ' + old_group_pw_file,
        "sudo sed -i '/" + student + "/d' " + old_group_pw_file,
        'sudo chmod 755 ' + old_group_pw_file,
    ]

    result = send_commands_to_ovid(command_list)

    if str(result['exit_status']) == '0':
        email_subject = 'GDI: Zugangsdaten für Ihr Repository in Eclipse'
        student_email_address = str(matrnr) + Config.get_email_default_email_domain_students()
        email_text = \
            'Die URI Ihres Repositorys: http://' + Config.get_ovid_ssh_host_name() + '/git/' + new_group_dir + '/' + new_group_dir + '.git\n' \
            + 'Ihr Account-Name: ' + student + '\n' \
            + 'Ihr Passwort: Ist gleich geblieben!\n'
        Emails.sendMailWithTextBody(student_email_address, email_subject, email_text)

        if Config.get_behavior_send_ovid_information_email():
            Emails.sendMailWithTextBody(Config.get_ovid_administrator_email_address(), 'REMINDER: ' + email_subject,
                                        'Student ' + str(
                                            matrnr) + ' wechselt von Gruppe ' + old_group_name + ' (' + git_dir_path + old_group_pw_file + ') zur Gruppe ' + new_group_name + ' (' + git_dir_path + new_group_pw_file + ').\n\n' + email_text)
    else:
        command_list_repair = [
            'cd ' + git_dir_path,
            'echo ' + ssh_password + ' | sudo -S chmod 755 ' + old_group_pw_file,
            'sudo chmod 755 ' + new_group_pw_file
        ]
        repair_result = send_commands_to_ovid(command_list_repair)
        if Config.get_behavior_send_ovid_error_email():
            send_email_with_error_messages_to_ovid_admin(result, repair_result, 'Student ' + str(
                                            matrnr) + ' wechselt von Gruppe ' + old_group_name + ' (' + git_dir_path + old_group_pw_file + ') zur Gruppe ' + new_group_name + ' (' + git_dir_path + new_group_pw_file + ').')


def write_new_pw_to_group_and_send_email_to_student(matrnr, new_group_name):
    new_password = random.choice('abcdefghij') + str(random.randrange(0, 1000001))
    new_group_dir = 'g' + new_group_name
    new_group_pw_file = new_group_dir + '/.passwd'
    student = 's' + str(matrnr)

    ssh_password = Config.get_ovid_ssh_password()
    git_dir_path = Config.get_ovid_git_dir_path()

    command_list = [
        'cd ' + git_dir_path,
        'echo ' + ssh_password + ' | sudo -S chmod 666 ' + new_group_pw_file,
        'sudo htpasswd -b ' + new_group_pw_file + ' ' + student + ' ' + new_password,
        'sudo chmod 755 ' + new_group_pw_file
    ]

    result = send_commands_to_ovid(command_list)

    if str(result['exit_status']) == '0':
        email_subject = 'GDI: Zugangsdaten für Ihr Repository in Eclipse'
        student_email_address = str(matrnr) + Config.get_email_default_email_domain_students()
        email_text = \
            'Die URI Ihres Repositorys: http://' + Config.get_ovid_ssh_host_name() + '/git/' + new_group_dir + '/' + new_group_dir + '.git\n' \
            + 'Ihr Account-Name: ' + student + '\n' \
            + 'Ihr Passwort: ' + new_password + '\n'
        Emails.sendMailWithTextBody(student_email_address, email_subject, email_text)

        if Config.get_behavior_send_ovid_information_email():
            Emails.sendMailWithTextBody(Config.get_ovid_administrator_email_address(), 'REMINDER: ' + email_subject,
                                        'Student ' + str(
                                            matrnr) + ' wurde in Gruppe ' + new_group_name + ' (' + git_dir_path + new_group_pw_file + ') eingetragen.\n\n' + email_text)
    else:
        command_list_repair = [
            'cd ' + git_dir_path,
            'echo ' + ssh_password + ' | sudo -S chmod 755 ' + new_group_pw_file
        ]
        repair_result = send_commands_to_ovid(command_list_repair)
        if Config.get_behavior_send_ovid_error_email():
            send_email_with_error_messages_to_ovid_admin(result, repair_result, 'Student ' + str(
                                            matrnr) + ' wurde in Gruppe ' + new_group_name + ' (' + git_dir_path + new_group_pw_file + ') eingetragen.')


def send_email_with_error_messages_to_ovid_admin(send_commands_to_ovid_result, repair_result, action_text = None):
    if str(repair_result['exit_status']) != '0':
        email_subject = 'OVID: Fehler bei Gruppenwechsel für ' + Config.get_course_creation_course_name()
        email_text = ''
        if action_text:
            email_text = action_text + '\n\n'
        email_text += 'Folgende Fehler traten beim durchführen des Gruppenwechsels auf:\n' \
                     + 'Exit Status: ' + str(send_commands_to_ovid_result['exit_status']) + '\n' \
                     + 'Errors: ' + str(send_commands_to_ovid_result['errors']) + '\n' \
                     + 'Commands: ' + send_commands_to_ovid_result['commands'] + '\n\n' \
                     + 'Folgende Reparaturen wurden vorgenommen:\n' \
                     + 'Repair-Status: ' + str(repair_result['exit_status']) + '\n' \
                     + 'Repair-Errors: ' + str(repair_result['errors']) + '\n' \
                     + 'Repaid-Commands: ' + repair_result['commands'] + '\n'

        Emails.sendMailWithTextBody(Config.get_ovid_administrator_email_address(), email_subject, email_text)


def send_commands_to_ovid(commands):
    hostname = Config.get_ovid_ssh_host_name()
    username = Config.get_ovid_ssh_user_name()
    password = Config.get_ovid_ssh_password()

    client = pm.SSHClient()
    client.set_missing_host_key_policy(
        pm.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    if isinstance(commands, list):
        prepared_commands = '; '.join(commands)
    else:
        prepared_commands = commands

    if Config.get_behavior_log():
        print('*********** COMMANDS TO OVID ***********')
        if isinstance(commands, list):
            for command in commands:
                print(command)
        else:
            print(commands)
        print('****************************')
        # util.ask_user_to_continue('Diese Befehle werden an OVID gesendet.\nMöchten Sie fortfahren? (ja/j = ja, ANY = nein)')

    stdin, stdout, stderr = client.exec_command(prepared_commands)
    exit_status = str(stdout.channel.recv_exit_status())
    ssh_stdout = stdout.readlines()
    ssh_stderr = stderr.readlines()
    client.close()
    if str(exit_status) != '0':
        print('****** ERROR IN SSH TO OVID ******')
        print('SSH Exit Status:')
        print(str(exit_status))
        print('SSH Output:')
        print(ssh_stdout)
        print('SSH Error Output:')
        print(ssh_stderr)
        print('')
    return {'exit_status': exit_status, 'errors': ssh_stderr, 'commands': prepared_commands}


if __name__ == '__main__':
    write_new_pw_to_group_and_send_email_to_student(1120479, '1-123')  # <- error
    write_pw_from_old_group_to_new_group_and_send_email_to_student(1120479, '1-1', '1-123') # <- should be error - but works silently :(
    write_pw_from_old_group_to_new_group_and_send_email_to_student(1120479, '1-123', '1-1')  # <- error
