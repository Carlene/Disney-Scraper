# ####################### Standard Libraries #####################################
# import os
# from selenium.webdriver.common.by import By
# ####################### My Libraries ###########################################

# folder = str(os.getcwd())
# folder = folder.replace("C:", "")
# print(folder)
# for root, dirs, files in os.walk("."):
#     if "git" in root:
#         continue
#     elif "ipynb" in root:
#         continue
#     elif "pycache" in root:
#         continue
#     else:
#         for name in files:
#             print("filename")
#             print(os.path.join(root, name))
#             print("end filename")
#         for name in dirs:
#             print("dirname")
#             print(os.path.join(root, name))
#             print("end dirname")

try:
    1/0
except Exception as e:
    print(f"Couldn't because {e}")