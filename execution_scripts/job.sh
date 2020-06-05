#!/bin/bash

# Go back to the project root, out of execution_scripts
cd /data/s2550709/CoChangeAnalysis

# Execute required programs
python3 -X faulthandler ./run_exploration.py -p poi -s 20-05-2011 -e 14-05-2020 -o apache -b trunk
python3 -X faulthandler ./run_exploration.py -p spring-framework -s 12-04-2015 -e 14-05-2020 -o spring-projects -b master
#python3 ./run_exploration.py -p pdfbox -s 13-10-2011 -e 14-05-2020 -o apache -b trunk
#python3 ./run_exploration.py -p jackson-databind -s 18-07-2012 -e 14-05-2020 -o FasterXML -b master
#python3 ./run_exploration.py -p hibernate-orm -s 27-02-2013 -e 14-05-2020 -o hibernate -b master
# Wait before closing the terminal
#read -p "Press any key to continue" x