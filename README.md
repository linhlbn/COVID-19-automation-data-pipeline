# COVID-19 real-time analysis project
<a href="https://datastudio.google.com/s/qSPC32qTzPs"> Click here to navigate to the dashboard </a>
## Purpose of the project
In the context of the COVID-19 pandemic, my project - a website/ dashboard that would be easy for everybody to follow the latest global figures as well as get more useful information such as: 
* The social (data) analyst wants to show their insider about the epidemic status
* The journalist wants to get the information about future of the pandemic by reading the prediction chart as a reference. 
* Everyone who lives in affected countries could recognize then protect themself from the danger zone as well as release the pressure of mental health (worry, fear, etc) after seeing the downtrend of the epidemic.

## Real-time?
YES, the only manual-thing is that you need to re-run the python code and click the 'refresh' button in Data Studio.
This manual process could be automated if using Airflow!
## Stages, tech stacks & status for project

| Stage | Tech stacks | Status |
| ----------- | ----------- | ----------- |
| First | Python, Google Bigquery API, Bigquery, SQL, Data Studio, Flourish, Facebook Prophet, Tableau (optional) | ✓ Done|
| Second (a) | Add more useful functions to the dashboard | ✓ Done |
| Second (b) | Add more machine learning model to support some specific questions | Processing |
| Third (Optional) | HTML, Javascript, CSS, Google Analytics, Google Tag Manager | Pending |
| Fourth (Optional) | Airflow (optional, if yes -> high priority), explore new cloud database (low) | Pending |
* Note: 
1. The fourth stage, I need time to research. 
2. The first tage, We can use Tableau desktop version to connect with Bigquery for automation (feed new data everyday), but Flourish is free and it is pretty awesome! 

## Instant set up
### Environment Installation
Anaconda or Pycharm. Creating environment with Pycharm is easy to do. If with Anaconda:
```
$ pwd
$ cd ...                              [to the project dir ]
$ EXPORT PATH = "...."                [path to your anaconda]
$ conda create -n <envs> python=3.7   [python version should be over 3.0 to use the cutting-edge API/ modules]
$ source activate <envs>
$ (<envs>) python --version           [check version, it should be 3.7.4]
```

### Used modules
`$ pip install numpy pandas matplotlib seaborn io requests datetime `
### Google Bigquery API & Facebook Prophet
`$ pip install google-cloud-bigquery fbprophet` <br>
if it does not work for Google Bigquery, use this command instead: 
> `$ conda install pandas-gbq --channel conda-forge`
### Datasource
get directly from Johns Hopkins University: <a href="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series">JHU CSSE COVID-19 Dataset</a>
### ETL (naive approach)
* Daily data: each day, a new csv file will be created -> create a function to modify and extract the latest data to csv file -> Transform data in the file -> Load to the data warehouse
* Time series data: get directly from source, or load it into another database (optional)
* Queries command in the source code, the Google Cloud Platform and Data Studio. 
## Source code
Stay tune! The code is ready, It will be posted later the same time with the next updated version!
