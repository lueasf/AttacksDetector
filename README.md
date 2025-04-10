# ML-based Intrusion Detector

Main goal: To build a ML-based intrusion detector (classifier) capable of
distinguishing between normal connections and intrusions (attacks).

Objectives : 
* Retrieve training data from InfluxDB and build structured data frames.
* Train intrusion detector following main ML steps:
    - Data inspection and visualization
    - Feature selection
    - Model training (DT, SVM, ANN)
    - Model evaluation and selection
* Export trained model.
* Deploy trained model in GCP with Docker and a Flask API.


## Attacks 
The attacks in the database are DDos, R2L, U2R and probing.

**DDoS** (Distributed Denial of Service) is when a large number of requests are sent to a server in a short time.

**R2L** (Remote to Local) is when an attacker tries to gain access to a remote system by exploiting vulnerabilities in the system (Ex: guessing passwords).

**U2R** (User to Root) is when an attacker tries to gain access to a system by exploiting vulnerabilities in the system (Ex: Buffer Overflow).

**Probing** is when an attacker tries to gain information about a system by sending requests to the system (Ex: Port scanning).


## Dataset
The dataset is from the KDD Cup 1999, which is a benchmark dataset for network intrusion detection systems. It was created by the MIT Lincoln Laboratory, and contains a wide variety of intrusions simulated in a military network environment. 


## Tools
- _Jupyter Notebook_
- _Python Libs_ : Pandas, Sklearn, Keras, Tensorflow,...
- _InfluxDB_ is used here to simulate a scenario where the data is stored in this database.
- _Telegraf_ is used here to collect the data from the database and send it to the ML-based intrusion detector.


## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## InfluxDB
We can either use the influx (-port 8089) command to connect to the database and write SQL queries or we can connect to the client using the influxdb python library.
```sql
SELECT COUNT("Attack Type") AS total FROM traffic GROUP BY "Attack Type"
```

## Telegraf
I use Telegraf to load the csv files into InfluxDB, to be able to do queries.


## Test for the API 
```bash
python3 test_request.py
``` 
Prediction result:
{
    "confidence": 0.9999682903289795,
    "prediction": "normal",
    "status": "success"
}
First with the Flask App, then with the Docker.
I also have a shell script to test the API with the Docker image.


## Commands
$ jupyter notebook
go on http://localhost:8888/tree

sudo pkill -f influxd

launch the db server
$ influxd -config config/custom-influxdb.conf

connect to the shell client
$ influx -port 8089

load csv and send it to influxdb in the intrusion database
$ telegraf --config config/telegraf.conf

# Todo
- save the model in a keras format
- re build the docker image
- test in local
- test in GCP
- automate the process with bash script