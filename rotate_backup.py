#python tool for syncing backups.
#sudo sudo rsync -avvzhr --progress * rsync-user@192.168.122.4::backups/
from asyncio import subprocess
import os
import glob;
import shlex;
import shutil;
import datetime;
import subprocess;
from datetime import datetime

from config import *;

def gettimes(current_files):#retn ['file':filetime, ...]
    return { current_files[i]: datetime.strptime(current_files[i],"%Y_%b_%d--%H%M.zip") for i in range(0, len(current_files))};

def yearly_bak(newfile, newfiletime):
    if newfiletime.day != 1 or newfiletime.month != 1:#бэкап только полночи 1 января
        return;
    elif newfiletime.hour == 12:
        return;
    else:
        os.chdir(ROOT_DIR + YEARLY_DIR);
        files_count = len(glob.glob("*.zip"));
        if files_count >= YEARLY_COUNT:
            current_files = [b for b in os.listdir() if b.endswith('.zip')];
            current_files = gettimes(current_files);
            for idx in range (files_count - YEARLY_COUNT + 1):
                oldest_file = min(current_files, key=current_files.get)
                if(newfiletime > current_files[oldest_file]):
                    shutil.copy(ROOT_DIR + newfile, ROOT_DIR + YEARLY_DIR + newfile);#копировать, не перемещать
                    os.remove(oldest_file);
        else:
            shutil.copy(ROOT_DIR + newfile, ROOT_DIR + YEARLY_DIR + newfile);
    return;

def monthly_bak(newfile, newfiletime):
    if newfiletime.day != 1:#бэкап только полночи 1 числа каждого месяца
        return;
    elif newfiletime.hour == 12:
        return;
    else:
        os.chdir(ROOT_DIR + MONTHLY_DIR);
        files_count = len(glob.glob("*.zip"));
        if files_count >= MONTHLY_COUNT:
            current_files = [b for b in os.listdir() if b.endswith('.zip')];
            current_files = gettimes(current_files);
            for idx in range (files_count - MONTHLY_COUNT + 1):
                oldest_file = min(current_files, key=current_files.get)
                if(newfiletime > current_files[oldest_file]):
                    shutil.copy(ROOT_DIR + newfile, ROOT_DIR + MONTHLY_DIR + newfile);#копировать, не перемещать
                    os.remove(oldest_file);
        else:
            shutil.copy(ROOT_DIR + newfile, ROOT_DIR + MONTHLY_DIR + newfile);
    return;

def weekly_bak(newfile, newfiletime):
    if newfiletime.weekday() != 0:#бэкап только полночи понедельники
        return;
    elif newfiletime.hour == 12:
        return;
    else:
        os.chdir(ROOT_DIR + WEEKLY_DIR);
        files_count = len(glob.glob("*.zip"));
        if files_count >= WEEKLY_COUNT:
            current_files = [b for b in os.listdir() if b.endswith('.zip')];
            current_files = gettimes(current_files);
            for idx in range (files_count - WEEKLY_COUNT + 1):
                oldest_file = min(current_files, key=current_files.get)
                if(newfiletime > current_files[oldest_file]):
                    shutil.copy(ROOT_DIR + newfile, ROOT_DIR + WEEKLY_DIR + newfile);#копировать, не перемещать
                    os.remove(oldest_file);
        else:
            shutil.copy(ROOT_DIR + newfile, ROOT_DIR + WEEKLY_DIR + newfile);
    return;

def daily_bak(newfile):

    newfiletime = datetime.strptime(newfile,"%Y_%b_%d--%H%M.zip");

    weekly_bak(newfile, newfiletime);
    monthly_bak(newfile, newfiletime);
    yearly_bak(newfile, newfiletime);

    os.chdir(ROOT_DIR + DAILY_DIR);
    
    files_count = len(glob.glob("*.zip"));

    if files_count >= DAILY_COUNT:
        current_files = [b for b in os.listdir() if b.endswith('.zip')];
        #создать словарь: имя_файла: время файла?
        current_files = gettimes(current_files);
        for idx in range (files_count - DAILY_COUNT + 1):
            #заменить самые старые файлы
            oldest_file = min(current_files, key=current_files.get)
            if(newfiletime > current_files[oldest_file]):
                shutil.move(ROOT_DIR + newfile, ROOT_DIR + DAILY_DIR + newfile);
                os.remove(oldest_file);
    else:
        shutil.move(ROOT_DIR + newfile, ROOT_DIR + DAILY_DIR + newfile); #недостаточно файлов

    os.chdir(ROOT_DIR);
    return;

def do_rsync():
    cmd = shlex.split(RSYNC_CMD);
    sp = subprocess.Popen(cmd, stdin =subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True, bufsize = 0);

    now = datetime.now();
    logfile = open('rotate_backup_' + now.strftime("%m.%d.%Y_%H-%M-%S") + '.log', 'w');
    logfile.write(sp.stdout.read());
    logfile.close();
    return;

try:
    olddir = os.getcwd();
    os.chdir(ROOT_DIR);
    if not os.path.exists(ROOT_DIR + DAILY_DIR):
        os.mkdir(ROOT_DIR + DAILY_DIR);
    if not os.path.exists(ROOT_DIR + WEEKLY_DIR):
        os.mkdir(ROOT_DIR + WEEKLY_DIR);
    if not os.path.exists(ROOT_DIR + MONTHLY_DIR):
        os.mkdir(ROOT_DIR + MONTHLY_DIR);
    if not os.path.exists(ROOT_DIR + YEARLY_DIR):
        os.mkdir(ROOT_DIR + YEARLY_DIR);
except OSError as ex:
    print(str(ex));
    exit(0);
else:
    for file in glob.glob("*.zip"):
        daily_bak(file);
    os.chdir(olddir);
    do_rsync();
    exit(0);

#переместить в daily n файлов не старше недели, если в daily меньше DAILY_COUNT файлов. удалить лишние (самые старые) файлы потом
#переместить в weekly n файлов не старше 4 недель, если в weekly меньше WEEKLY_COUNT файлов. удалить лишние (самые старые) файлы потом
#переместить в monthly n файлов не старше 12 месяцев, если в weekly меньше MONTHLY_COUNT файлов. удалить лишние (самые старые) файлы потом
#переместить в early n файлов не старше года, если в yearly меньше YEARLY_COUNT файлов. удалить лишние (самые старые) файлы потом
