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

home_dir = os.getenv("HOME")

parser = argparse.ArgumentParser()
parser.add_argument("profile", help="profile to set as default")

args = parser.parse_args()
profile_to_swap_to = args.profile

profile_to_swap_to

# Read the current credentials file
with open(home_dir + '/.aws/credentials', 'r') as curr_creds:
    curr_creds_lines = curr_creds.readlines()
    # If no backup exists make one from the exisiting,
    # just in case formatting is ikky and something breaks
    if not os.path.exists(home_dir + '/.aws/credentials_backup'):
        with open(home_dir + '/.aws/credentials_backup', 'w') as backup_file:
            for line in curr_creds_lines:
                backup_file.write(line)

# If passed in the "restore" arg
# Restore the credentials from the backup
if profile_to_swap_to == 'restore':
    print 'restoring from credentials_backup'
    with open(home_dir + '/.aws/credentials_backup', 'r') as backup_file:
        backup_file_creds_lines = backup_file.readlines()
        with open(home_dir + '/.aws/credentials', 'w') as curr_creds:
            for line in backup_file_creds_lines:
                curr_creds.write(line)
else:
    print 'Swapping to: ' + profile_to_swap_to
    # Otherwise just swap the profile to the requested one
    # Read through the file for the profile to swap to
    with open(home_dir + '/.aws/credentials', 'r') as curr_creds:
        curr_creds_lines = curr_creds.readlines()
        # Go through and find the creds to swap to
        for line in curr_creds_lines:
            if line == '[' + profile_to_swap_to + ']\n':
                access_key_id = curr_creds_lines[curr_creds_lines.index(line) + 1]
                secret_key = curr_creds_lines[curr_creds_lines.index(line) + 2]
    # Using the lines from the read write over the old file with new default
    with open(home_dir + '/.aws/credentials', 'w') as curr_creds:
        # Find line numbers of default to overwrite
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
