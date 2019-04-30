# ElasticPhish

Example application using the [Elastic](https://www.elastic.co/) stack to store and visualize phishing domains detected using the [certstream](https://certstream.calidog.io/) tool for consuming live Certificate Transparency Log data.

The folder contains a working phishing detection tool (prototype) and configuration files for Logstash and Filebeat. The goal of this project was to:
1. Provide a working example of a phishing domain detector
2. Highlight components of the Elastic stack and how they can be used to visualize the intelligence
3. Show the power of CertStream to provide SOC teams additional intelligence on malicious actors

### Installation

The script was built using Python 3.7.3, but should work across Python 2 & 3 versions

You will need to first install the following Python libraries: certstream, yaml, tld

```
pip install -r requirements.txt
```

