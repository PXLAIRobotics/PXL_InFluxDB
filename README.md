# PXL InfluxDB

This project contains a backend API, InfluxDB.

## Technical Details

### Uvicorn

**Uvicorn** is a lightning-fast "ASGI" server.

It runs asynchronous Python web code in a single process.

### Gunicorn

You can use **Gunicorn** to start and manage multiple Uvicorn worker processes.

That way, you get the best of concurrency and parallelism in simple deployments.

### FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+.

The key features are:

* **Fast**: Very high performance, on par with **NodeJS** and **Go** (thanks to Starlette and Pydantic).
* **Fast to code**: Increase the speed to develop features by about 200% to 300% *.
* **Less bugs**: Reduce about 40% of human (developer) induced errors. *
* **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Less bugs.
* **Robust**: Get production-ready code. With automatic interactive documentation.
* **Standards-based**: Based on (and fully compatible with) the open standards for APIs: <a href="https://github.com/OAI/OpenAPI-Specification" target="_blank">OpenAPI</a> (previously known as Swagger) and <a href="http://json-schema.org/" target="_blank">JSON Schema</a>.

<small>* estimation based on tests on an internal development team, building production applications.</small>

### InfluxDB
InfluxDB is an open-source time series database developed by the company InfluxData. It is written in the Go programming language for storage and retrieval of time series data in fields such as operations monitoring, application metrics, Internet of Things sensor data, and real-time analytics. It also has support for processing data from Graphite.

* Has no external dependencies
* Provides SQL-like language
* Listens on port 8086
* Built-in time-centric functions for querying a data structure composed of measurements, series, and points. 
  * Point: consists of several key-value pairs called the fieldset and a timestamp. 
  * Series: points grouped together by a set of key-value pairs called the tagset. 
  * Measurement: series are grouped together by a string identifier to form a measurement.

Values can be 64-bit integers, 64-bit floating points, strings, and booleans. Points are indexed by their time and tagset. Retention policies are defined on a measurement and control how data is downsampled and deleted. Continuous Queries run periodically, storing results in a target measurement.

## Prerequisites

* A Unix-like system with Bash
* Docker


## Setup

0. 
```./001_build_images.sh```

1. 
```./002_create_and_start_containers.sh```

Wait for the images to be downloaded and the containers to be set up.

**DevBox**

Attach a bash shell to the FastAPI container by executing the following script:

2. 
```./003_attach_bash_to_devbox_container.sh```

**InfluxDB**

Attach a bash shell to the InfluxDB container by executing the following script:

2. 
```./003_attach_bash_to_influxdb_container.sh```

