ROOT_DIR = '/var/atlassian/application-data/jira/export/'

DAILY_DIR = '/daily/';
WEEKLY_DIR = '/weekly/';
MONTHLY_DIR = '/monthly/';
YEARLY_DIR = '/yearly/';

DAILY_COUNT = 14;
WEEKLY_COUNT = 4;
MONTHLY_COUNT = 12;
YEARLY_COUNT = 10;

RSYNC_HOST = '@192.168.122.4::backups/';
RSYNC_USER = 'rsync-user';
RSYNC_PASS = '/etc/rsyncd.secret'; #contain password only, no user
RSYNC_CMD = 'rsync -avvzhr --progress ' + ROOT_DIR + ' ' + RSYNC_USER +  RSYNC_HOST + ' --password-file=' + RSYNC_PASS; 
#sudo rsync -avvzhr --progress * rsync-user@192.168.122.4::backups/
#rsync -avzhr  * rsync-user@192.168.122.4::backups/ --password-file='/etc/rsyncd.secret'

