# import os
# import shutil
# from Utilities import extract_number
# # print list  folders in folder
# folder = "D:/thesisdata\distorted\MetaTestset_1"
# copy_dir = "D:/temp"
# for folder in os.listdir(folder):
#     for file in os.listdir(f"D:/thesisdata\distorted\MetaTestset_1/{folder}"):
#         if extract_number(file, prefix=".*-", sufix="-.*") == 52:
#             # copy file into copy dir
#             shutil.copy2(f"D:/thesisdata\distorted\MetaTestset_1/{folder}/{file}", f"{copy_dir}")
            

import numpy as np

print([0, 0.3, 0.5, 0.6, 0.7, 0.8] + list(np.linspace(0.9,1.0,11, endpoint=True)))
