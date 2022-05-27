## Introduction
For GIT (Github) testing only! Tool for backuping various archive files to remote server by rsync
## Current Releases
0.1 - Initial commit. <br />
## Platforms
Any Linux. Python3 required.
### Usage
Typical usage: adding to crontab to execute daily in 6 AM:
'sudo crontab -e' and type '0 6 * * * /path/to/rotate_backup.py' <br />
create_random_files_jira.sh is a small script for generating random files in in the specified folder. Files looks like common jira backup files: backuped twice in a day for a whole year
## Config file
Configure setting in config.py: <br />
ROOT_DIR is your archives source directory <br />
DAILY_DIR is a directory to store your daily archives <br />
WEEKLY_DIR is a directory to store your monthly archives <br />
YEARLY_DIR is a directory to store your yearly archives <br />

You can decide yourself how many files to store in every directory: <br />
DAILY_COUNT files will be stored (and synced) to remote daily directory <br />
WEEKLY_COUNT files will be stored (and synced) to remote weekly directory <br />
MONTHLY_COUNT files will be stored (and synced) to remote monthly directory <br />
YEARLY_COUNT files will be stored (and synced) to remote yearly directory <br />
Other settings: <br />
RSYNC_HOST is your remote rsync server in a format: '@ip_or_hostname::remote_dir' <br />
RSYNC_USER is remote rsync user <br />
RSYNC_PASS is file, where rsync user's password is saved. Usually, file permission is 600. Do not write user to this file, password only. <br />
RSYNC_CMD is combined command for running rsync client <br />
## Licenses
Use and modify on your own risk.
