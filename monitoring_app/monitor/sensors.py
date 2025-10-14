import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return (mem.percent, mem.used, mem.total)

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return (disk.percent, disk.used, disk.total)

    