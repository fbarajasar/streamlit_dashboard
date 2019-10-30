# Visualizing the Olympic Games History

![alt text](https://github.com/fbarajasar/olympics_project/blob/master/jesse-owens-berlin.jpg)

## Live App Prototype
https://olympics-dashboard.herokuapp.com/


## The Dataset
This is a historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016. The data contains 271116 rows and 15 columns. Each row corresponds to an individual athlete competing in an individual Olympic event (athlete-events). For this exercise, I will focus on the Summer Olympic Games.
The Idea

## The Idea
The app should allows users to interact with the dataset and make it easy for them to extract and share insights about the Olympic Games with other app users.

## The Pipeline
1. Extract and Clean the data from the CSV
3. Store data in an SQLite DB.
4. Do some precalculations on the data and store them as tables in the db.
4. Code a series of Python functions that query the DB and filter and aggregate the data in different ways
5. Use Streamlit to create a user interface that connects to the Python functions coded on the back-end. Those function return data that is converted into charts and displayed in the application.


## Libraries Used in the Project
### For Storage
SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. SQLite is the most used database engine in the world. SQLite is built into all mobile phones and most computers and comes bundled inside countless other applications that people use every day.

### For Analysis and i/o operations
Pandas is a Python package providing fast, flexible, and expressive data structures designed to make working with "relational" or "labelled" data both easy and intuitive. It aims to be the fundamental high-level building block for doing practical, real-world data analysis in Python.

### For Visualization
Matplotlib is a Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms. Matplotlib can be used in Python scripts, the Python and IPython shells, the Jupyter notebook, web application servers, and four graphical user interface toolkits.

### For the Front End
Streamlit is an open-source Python library that makes it easy to build beautiful apps for visualizing data.

## For Deployment
### The App is deployed here:
https://olympics-dashboard.herokuapp.com/
### The app source code lives here: 
https://github.com/fbarajasar/olympics_project
