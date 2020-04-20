import os 

MOUNT_DIR = "./mn"

statlist = []
statlist.append(os.stat(MOUNT_DIR).st_ino)

path = MOUNT_DIR

def search(path):
    x = os.listdir(path)
    for i in x:
        if i == "MATCH":
            print("MATCH:::" + path)
        try:
            if not os.stat(path + "/" + i).st_ino in statlist:
                statlist.append(os.stat(path + "/" + i).st_ino)
                search(path + "/" + i)
        except:
            continue

search(path)