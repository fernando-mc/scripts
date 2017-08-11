#!/usr/bin/env python
# Python Script to swap AWS Profile configs

# Assumes that credentials file is at ~/.aws/credentials

import argparse
import ConfigParser
import os

Config = ConfigParser.ConfigParser()
Config.read(os.path.expanduser('~/.aws/credentials'))

def get_profile_to_swap_to():
    """Parse the profile requested from user input"""
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", help="profile to set as default")
    args = parser.parse_args()
    profile_to_swap_to = args.profile
    sections = Config.sections()
    if profile_to_swap_to in sections:
        return profile_to_swap_to
    else:
        section_list = ''
        for i in sections:
            section_list += (i + '\n')
        raise ValueError(
            "The profile '{0}' is not in your credentials file. \n\n" \
            "Available profiles are:\n{1}".format(
                profile_to_swap_to, 
                section_list
            )
        )

def swap_profile(profile_to_swap_to):
    key = Config.get(profile_to_swap_to, 'aws_access_key_id')
    secret = Config.get(profile_to_swap_to, 'aws_secret_access_key')
    Config.set('default', 'aws_access_key_id', key)
    Config.set('default', 'aws_secret_access_key', secret)
    with open(os.path.expanduser('~/.aws/credentials'), 'wb') as configfile:
        Config.write(configfile)

def main():
    profile = get_profile_to_swap_to()
    swap_profile(profile)
    print 'Swapped to profile: {0}'.format(profile)

if __name__ == "__main__":
    main()
