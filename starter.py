import os
import sys

if len(sys.argv) != 2:
    exit()


folder_name = sys.argv[1]

for file in os.listdir(folder_name):
    print(file)
