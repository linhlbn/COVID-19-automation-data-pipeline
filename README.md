# COVID-19 real-time analysis project
- - -
### Purpose of the project
In the context of the COVID-19 pandemic, a simple website/ dashboard would be easy for everybody to follow the latest global figures as well as get more useful information.
### Stages, tech stacks & status 
| Stage | Tech stacks | Status |
| ----------- | ----------- | ----------- |
| First | Python, Google Cloud API, Google Bigquery, SQL, Google Data Studio, Flourish | ✓ Done|
| Second | Add more useful functions to the dashboard | Processing |
| Third | HTML, Javascript, CSS, Google Analytics, Google Tag Manager | Pending |
| Fourth (Optional) | Airflow (high priority) explore new cloud database (low) | Pending |
* Note: the fourth stage, I need time to research. 
### Instant set up
##### Environment Installation (ds)
Anaconda or Pycharm. Creating environment is easy to do, if with Anaconda:
```
$ pwd
$ cd ...                             [to the project dir ]
$ EXPORT PATH = "...."               [path to your anaconda]
$ conda create -n ds python=3.7      [python version should be over 3.0 to use the cutting-edge API/ modules]
```

##### Useful module
`$ pip install numpy pandas matplotlib seaborn requests`
##### Google Cloud 
`$ pip install google-cloud-bigquery`
##### Datasource
get directly from Johns Hopkins University: <a href="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series">JHU CSSE COVID-19 Dataset</a>
##### ETL
* Daily data: each day, a new csv file will be created -> create a function to modify and Extract the latest csv file -> Transform -> Load to the data warehouse
* Time series data: get directly from source, or load it into another database (optional)
##### Source code
Stay tune! The code is ready, It will be posted later the same time with the next updated version!
