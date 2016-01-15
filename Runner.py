#!/usr/bin/python3

import sys 
import os
import parser as sp
import SteinerTree 

'''
    Run this file as a script to pass multiple 
    pass the file containing the settings as arguments
'''


settings = []

if(len(sys.argv) != 2):
    raise IOError('file path missing')
    
else:
  print('Executing Runner with file', sys.argv[1])
  settings = sp('weights.txt')  # [(41 30 0.9 0.05 3),(41 30 0.9 0.05 3)]
  
  for s in settings:
    steiner_tree = SteinerTree(s)
    steiner_tree.run();

    



