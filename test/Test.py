import sys
import os

projectPath = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(projectPath)

print(projectPath)

import control.OPcontrol
#import models.DBconnect as DBconnect