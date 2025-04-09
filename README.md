# ML-based Intrusion Detector

Main goal: To build a ML-based intrusion detector (classifier) capable of
distinguishing between normal connections and intrusions (attacks).

Objectives : 
Specific objectives:
Introduction to basic tools for ML-based DevOps in Python3 :
- Jupyter Notebook, Pandas, Sklearn, Keras

Retrieve training data from InfluxDB and build structured data frames.

Train intrusion detector following main ML steps:
- Data inspection and visualization
- Feature selection
- Model training (DT, SVM, ANN)
- Model evaluation and selection
Export trained model for future usage in operation.



## Tools
- Jupyter Notebook
- Pandas
- Sklearn
- Keras
- InfluxDB
- Telegraf
- Tensorflow

## Commands
jupyter notebook
http://localhost:8888/tree

influxd -config ~/custom-influxdb.conf
telegraf --config ./telegraf.conf

influx -port 8089