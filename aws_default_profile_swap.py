#!/usr/bin/env python
# Pyhton Script to swap AWS Profile configs

# Assumes that credentials file is at 
# and follows this pattern:
# [profile-name]
# aws-key-thing: keyaskjhdaksjdhiausgd
# aws-secret-thing: secretythingsad7uy23hjeasd8uhi2jawd
# [profile-othername]
# aws-key-thing: keyaskjhdaksjdhiausgd
# aws-secret-thing: secretythingsad7uy23hjeasd8uhi2jawd
# [default]
# aws-key-thing: keyaskjhdaksjdhiausgd
# aws-secret-thing: secretythingsad7uy23hjeasd8uhi2jawd

import argparse
import os

HOME_DIR = os.getenv("HOME")

def read_creds_file(filename):
    """Returns the lines of the credentials file if it exists"""
    try:
        with open(HOME_DIR + '/.aws/' + filename, 'r') as curr_creds:
            curr_creds_lines = curr_creds.readlines()
        return curr_creds_lines
    except IOError:
        print 'credentials file does not exist!'

def get_profile_to_swap_to():
    """Parse the profile requested from user input"""
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", help="profile to set as default")
    args = parser.parse_args()
    profile_to_swap_to = args.profile
    creds_string = ''
    for line in read_creds_file('credentials'):
        creds_string += line
    if '[' + profile_to_swap_to + ']\n' in creds_string:
        return profile_to_swap_to
    elif profile_to_swap_to == 'restore':
        return 'restore'
    else:
        raise ValueError("The profile '{0!s}' is not in your credentials file.".format(profile_to_swap_to))

def add_backup_if_none_exists():
    """Adds a backup creds file if none exists"""
    if read_creds_file('credentials') and not os.path.exists(HOME_DIR + '/.aws/credentials_backup'):
        with open(HOME_DIR + '/.aws/credentials_backup', 'w') as backup_file:
            for line in read_creds_file('credentials'):
                backup_file.write(line)

def restore_from_backup():
    backup_file_creds_lines = read_creds_file('credentials_backup')
    with open(HOME_DIR + '/.aws/credentials', 'w') as curr_creds:
        for line in backup_file_creds_lines:
            curr_creds.write(line)
    print 'restored profile from backup'

def swap_to_profile(profile):
    curr_creds_lines = read_creds_file('credentials')
    count = 0
    for line in curr_creds_lines:
        if line == '[' + profile + ']\n':
            access_key_id = curr_creds_lines[count + 1]
            secret_key = curr_creds_lines[count + 2]
        count += 1
    with open(HOME_DIR + '/.aws/credentials', 'w') as curr_creds:
        count = 0
        for line in curr_creds_lines:
            if line == '[default]\n':
                curr_creds.write('[default]\n')
            elif curr_creds_lines[count - 1] == '[default]\n':
                curr_creds.write(access_key_id)
            elif curr_creds_lines[count - 2] == '[default]\n':
                curr_creds.write(secret_key)
            else:
                curr_creds.write(line)
            count += 1
    print 'Success - Swapped profile to ' + profile

def main():
    add_backup_if_none_exists()
    profile_to_swap_to = get_profile_to_swap_to()
    if profile_to_swap_to == 'restore':
        restore_from_backup()
    else: 
        swap_to_profile(profile_to_swap_to)
    
if __name__ == "__main__":
    main()
