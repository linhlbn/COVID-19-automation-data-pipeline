# COVID 19 automation serverless data pipeline
<a href="https://datastudio.google.com/s/qSPC32qTzPs"> Click here to navigate to the dashboard </a> <br>
| Table of Contents |
| --- |
| I/ Purpose of the project |
| II/ Stages, tech stacks & status for project |
| III/ Instant set up |
| IV/ Question & My Solution |
_____
## I/ Purpose of the project
In the context of the COVID-19 pandemic, my project - a website/ dashboard that would make it easy for everybody to follow the latest global figures as well as get more useful information such as:
* The social (data) analyst wants to show their insider about the epidemic status
* The journalist wants to get the information about future of the pandemic by reading the prediction part as a reference.
* Everyone who lives in affected countries could recognize and protect themself from the danger zone as well as release the pressure of mental health (worry, fear, etc) after seeing the downtrend of the epidemic.

## II/ Stages, tech stacks & status for the project

| Stage | Tech stacks | Status |
| ----------- | ----------- | ----------- |
| First | Python, Google Bigquery API, Bigquery (Google Cloud Platform), SQL, Data Studio, Flourish, Facebook Prophet, Tableau Desktop version(optional) | ✓ Done|
| Second | Add more useful information to the dashboard | ✓ Done |
| Third | Predict cases | ✓ Done |

* Note:
1. The fifth stage, I need time to research.
2. In The first stage, We can use the Tableau desktop version to connect with Bigquery for automation the racing chart, but Flourish is free and it is pretty awesome!

## III/ Instant set up
### Environment Installation
Anaconda or Pycharm. Creating an environment with Pycharm is easy to do. If with Anaconda:
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
### Datasource & Approach
Johns Hopkins University: <a href="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series">JHU CSSE COVID-19 Dataset</a>
> The Python script includes functions to retrieve the latest data, transform & add new features for ad-hoc analysis as well as the suitable form for visualizing.

## IV/ Question & My Solution
##### Automation?
YES, the only manual thing is that:
* need to re-run the Python code and click the 'refresh' button in Data Studio to update the latest data from source and transformed data to new ad-hoc features -> could be totally automated if implement the fifth stage!
* update data for the racing chart on Flourish -> could be automated if using the Tableau Desktop version to connect with Bigquery and set the scheduled query.
##### Why Flourish instead of Tableau?
Flourish is free and it is pretty awesome, Tableau costs $70/month with the personal package - Tableau Creator.
##### Why Google Bigquery as a Data Warehouse?
I can use IBM-Db2 with IBM Watson Studio, but the `IBM-db` module has conflicted with my local machine environment - cannot execute the module. Besides that, the most important thing is:
Google Bigquery is a serverless data warehouse (SaaS) that is a highly scalable, cost-effective, and real-time analysis with great performance. You not only can run a query to analyze terabytes-petabytes of data within seconds but also use it effectively with a friendly user experience on Google Cloud Platform.
##### I need to see your source code as a reference!
Updated (I was working on this project when I was a first-year student, therefore, the code was quite messy)
