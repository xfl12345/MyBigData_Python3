import os
from mybigdata.src.main.model.conf.loader.json_schema_loader import get_root_path

# source code URL=https://www.runoob.com/python/os-walk.html
for root, dirs, files in os.walk(get_root_path(), topdown=False):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
