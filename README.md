# ElasticPhish

Example application using the [Elastic](https://www.elastic.co/) stack to store and visualize phishing domains detected using the [certstream](https://certstream.calidog.io/) tool for consuming live Certificate Transparency Log data.

The folder contains a working phishing detection tool (prototype) and configuration files for Logstash and Filebeat. The goal of this project was to:
1. Provide a working example of a phishing domain detector
2. Highlight components of the Elastic stack and how they can be used to visualize the intelligence
3. Show the power of CertStream to provide SOC teams additional intelligence on malicious actors

## Installation

#### Python
The script was built using Python 3.7.3, but should work across Python 2 & 3 versions

You will need to first install the following Python libraries: certstream, yaml, tld

```
pip install -r requirements.txt
```


#### Elastic
Navigate to the Elastic [download](https://www.elastic.co/downloads/) page and download the latest versions of Elasticsearch, Logstash, Kibana, and Filebeat. At the time of publishing, it is version 7.0.

In the Logstash folder, add the `logstash.conf` file to the `/config/` directory. The config assumes you for PoC purposes that you are running on a single machine, so notice the use of localhost. The address can be changed to reflect different containers/vm configurations.

In the Filebeat folder, replace the `filebeat.yml` file with the provided `filebeat.yml`. It is *important* that you modify the path in line 28 to reflect the location where you will be writing the phishing domains to.


#### CertStream
On lines 11 & 12 of the `elasticphish.py` script are two different options for url instantiation. The first connects directly to a CertStream server run by CaliDog. The second is pointing to a local version of the [CertStream Server](https://github.com/CaliDog/certstream-server) running on a local instance. 

It is recommended that you run your own CertStream server to obtain the best performance and reduce downtime. The CaliDog server should be used for testing to ensure that proper setup has been performed.

For instructions on deploying the CertStream Server, refer to the CaliDog Github page.


## Operation

#### Elastic
Refer to Elastic documentation for full configuration and operating commands. The following are simple commands to start each of the processes, and should not be considered and exhaustive explanation.
```
from elasticsearch folder, run: bin/elasticsearch
from kibana folder, run: bin/kibana
from logstash folder, run: bin/logstash -f logstash.conf
from filebeat folder, run: ./filebeat -e -c filebeat.yml
```

#### ElasticPhish Script
```
python elasticphish.py
```