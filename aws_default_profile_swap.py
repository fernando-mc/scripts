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

parser = argparse.ArgumentParser()
parser.add_argument("profile", help="profile to set as default")
args = parser.parse_args()

profile_to_swap_to = args.profile

count_one = 0
count_two = 0

print 'Swapping to: ' + profile_to_swap_to

with open('~/.aws/credentials', 'r') as file:
    lines = file.readlines()
    # Find creds to set as default
    for i in lines:
        if i == '[' + profile_to_swap_to + ']\n':
            access_key_id = lines[count_one + 1]
            secret_key = lines[count_one + 2]
        count_one += 1

with open('~/.aws/credentials', 'wr') as file:
    # Find line numbers of default to overwrite
    for line in lines:
        if line == '[default]\n':
            file.write('[default]\n')
        elif lines[count_two - 1] == '[default]\n':
            file.write(access_key_id)
        elif lines[count_two - 2] == '[default]\n':
            file.write(secret_key)
        else:
            file.write(line)
        count_two += 1
