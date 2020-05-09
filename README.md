# COVID-19 real-time analysis project
- - -
### Purpose of the project
In the context of the COVID-19 pandemic, a simple website/ dashboard would be easy for everybody to follow the latest global figures as well as get more useful information.

### Real-time?
YES, the only manual-thing is that you need to re-run the python code and click the 'refresh' button in Data Studio. This could be called automation somehow.
This manual process could be automated if using Airflow!
### Stages, tech stacks & status for project

| Stage | Tech stacks | Status |
| ----------- | ----------- | ----------- |
| First | Python, Google Cloud API, Bigquery, SQL, Data Studio, Flourish, Tableau (optional) | ✓ Done|
| Second | Add more useful functions to the dashboard | Processing |
| Third | HTML, Javascript, CSS, Google Analytics, Google Tag Manager | Pending |
| Fourth (Optional) | Airflow (high priority), explore new cloud database (low) | Pending |
* Note: 
1. The fourth stage, I need time to research. 
2. The first tage, We can use Tableau desktop version to connect with Bigquery for automation (feed new data everyday), but Flourish is free and it is pretty awesome! 

### Instant set up
##### Environment Installation (ds)
Anaconda or Pycharm. Creating environment with Pycharm is easy to do. If with Anaconda:
```
$ pwd
$ cd ...                             [to the project dir ]
$ EXPORT PATH = "...."               [path to your anaconda]
$ conda create -n <envs> python=3.7      [python version should be over 3.0 to use the cutting-edge API/ modules]
$ source activate <envs>
```

##### Useful modules
`$ pip install numpy pandas matplotlib seaborn requests`
##### Google Cloud 
`$ pip install google-cloud-bigquery`
if it does not work, use this command instead:
`$ conda install pandas-gbq --channel conda-forge`
##### Datasource
get directly from Johns Hopkins University: <a href="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series">JHU CSSE COVID-19 Dataset</a>
##### ETL (naive approach)
* Daily data: each day, a new csv file will be created -> create a function to modify and Extract the latest csv file -> Transform -> Load to the data warehouse
* Time series data: get directly from source, or load it into another database (optional)
##### Source code
Stay tune! The code is ready, It will be posted later the same time with the next updated version!
