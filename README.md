# Data processing and distribution system  based on Apache NiFi

This git repository is a supplement to my BSc Thesis. It contains python scripts that I have used to obtain, process and visualize performance data. They are located in the python_scripts folder. As for the second one, it contains NiFi configuration files. NiFi_detail_images keeps detail images depicting the data flow.

## python_scripts
* performance.py - gather system utilization info and save it into .csv file
* dump_performance.py - convert raw statistics about system utilization into pickle object
* dump_processing_times.py - extract mean processing times from the results and  convert to pickle object
* make_final_plots_and_tables.py -  visualize data stored in pickle objects
* make_summary_plot.py - plot processing and mean times in function of node numbers
### requirements, in brackets, versions of external modules used by me, python 3.8:
* numpy (1.18.5)
* pickle
* time
* psutil (5.8.0)
* matplotlib (3.3.3)
* os
* itertools
* csv

## NiFi_configuration

It contains nifi.properties, authorizers.xml, zookeeper.properties and state-management.xml which are described in the thesis. 

## NiFi_detail_images

Images of the data processing flow in detailImages are ordered by their position in the flow.
