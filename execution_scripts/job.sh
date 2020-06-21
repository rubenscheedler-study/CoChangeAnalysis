#!/bin/bash

# Go back to the project root, out of execution_scripts
cd /data/s2550709/CoChangeAnalysis


# Execute required programs


# python3 -X faulthandler ./run_exploration.py -p swagger-core -s 28-07-2011 -e 14-05-2020 -o swagger-api -b master
# python3 -X faulthandler ./run_exploration.py -p testng -s 30-07-2006 -e 14-05-2020 -o cbeust -b master
# python3 -X faulthandler ./run_exploration.py -p xerces2-j -s 22-01-2004 -e 14-05-2020 -o apache -b trunk
# python3 -X faulthandler ./run_exploration.py -p junit5 -s 31-10-2015 -e 14-05-2020 -o junit-team -b master
# python3 -X faulthandler ./run_exploration.py -p mybatis-3 -s 10-05-2010 -e 14-05-2020 -o mybatis -b master
python3 -X faulthandler ./run_exploration.py -p robolectric -s 06-01-2015 -e 14-05-2020 -o robolectric -b master
# python3 -X faulthandler ./run_exploration.py -p RxJava -s 10-04-2012 -e 14-05-2020 -o ReactiveX -b 3.x
# python3 -X faulthandler ./run_exploration.py -p sonarlint-intellij -s 30-10-2013 -e 14-05-2020 -o SonarSource -b master

# python3 -X faulthandler ./run_exploration.py -p pdfbox -s 13-10-2011 -e 14-05-2020 -o apache -b trunk
# python3 -X faulthandler ./run_exploration.py -p poi -s 20-05-2011 -e 14-05-2020 -o apache -b trunk

# python3 -X faulthandler ./run_exploration.py -p druid -s 02-01-2013 -e 14-05-2020 -o apache -b master
# python3 -X faulthandler ./run_exploration.py -p argouml -s 17-09-2004 -e 14-05-2020 -o argouml-tigris-org -b master
# python3 -X faulthandler ./run_exploration.py -p cassandra -s 14-08-2014 -e 14-05-2020 -o apache -b trunk

# python3 -X faulthandler ./run_exploration.py -p hibernate-orm -s 27-02-2013 -e 14-05-2020 -o hibernate -b master
# python3 -X faulthandler ./run_exploration.py -p jackson-databind -s 18-07-2012 -e 14-05-2020 -o FasterXML -b master
# python3 -X faulthandler ./run_exploration.py -p spring-framework -s 12-04-2015 -e 14-05-2020 -o spring-projects -b master


# Wait before closing the terminal
#read -p "Press any key to continue" x