#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# libraries here
from flask import Flask, render_template, request
from bokeh.charts import Histogram
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
import pandas as pd
import os
import json
import tldextract
import collections
from collections import defaultdict

app = Flask(__name__)

#template for bar graph
def plot_bar(x_,y_, title_):
    x = x_
    counts = y_

    p = figure(x_range=x, plot_height=350, title= title_,
           toolbar_location=None, tools="")
    p.vbar(x=x, top=counts, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return p


#template for scatter plot
def plot_point(x_,y_,x_label,y_label,title_):
    x = range(1,len(x_)+1)
    y = y_


    p = figure(
        title = title_,
        x_axis_label = x_label,
        y_axis_label = y_label
    )

    p.circle(x,y, line_width =2)
    return (p)

#specific function to call plot_bar and plot top domain appears on search
def plot_top_domain(domain_count):
    sorted_x = sorted(domain_count.items(), key=lambda kv: kv[1])
    sorted_dict = collections.OrderedDict(sorted_x)

    #Pick up the most count from ascending sorted list
    x_ = list(sorted_dict.keys())[-5:]
    y_ = list(sorted_dict.values())[-5:]
    title = 'Domain Counts'
    
    p = plot_bar(x_,y_,title)
    return p

#specific function to call plot_bar and plot top google search
def plot_top_google(google_search_count):
    sorted_x = sorted(google_search_count.items(), key=lambda kv: kv[1])
    sorted_dict = collections.OrderedDict(sorted_x)
    print(plot_top_google)

    #Pick up the most count from ascending sorted list
    x_ = list(sorted_dict.keys())[-5:]
    y_ = list(sorted_dict.values())[-5:]
    title = 'Top Google Search Counts'
    
    p = plot_bar(x_,y_,title)
    return p


def plot_user_page_num (user_page_num):
    x = list(user_page_num.keys())
    y = list(user_page_num.values())
    x_axis_label = 'Users'
    y_axis_label = 'Counts'
    title = "Maximum Page Number Each User Search"

    
    p = plot_point(x,y,x_axis_label,y_axis_label,title)
    return p


def plot_main(user_page_num,domain_count,google_search_count):

    
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Most Appeared Domain Names on Search"
           

    if current_feature_name == 'Most Appeared Domain Names on Search':
        plot = plot_top_domain(domain_count)
    
    
    if current_feature_name == 'Top Google Search':
        plot = plot_top_google(google_search_count)
    
    if current_feature_name == 'Maximum Page Number Each User Search':
        plot = plot_user_page_num(user_page_num)


    return (current_feature_name,plot)



def read_file(file_name,user_page_num,domain_count,google_search_count):
    
    MAX_page_num = 0
    
    with open('data/'+file_name) as json_file:
        
        data = json.load(json_file)
        user_id = data['userID']
        for each_search_data in data['searchData']:
            



            #getting top domain counts    
            if each_search_data['searchResults'] is not None:
                for each_search in each_search_data['searchResults']:
                
                    ext = tldextract.extract(each_search['url'])
                    domain_count[ext.domain] += 1
            
            #getting top google search counts        
            #count only on page 0 of the search to avoid multiple count
            # subjective : will count twice if same user type the same search again. 
            if (each_search_data['searchQueryString'] != 'dummySearch') and (each_search_data['searchQueryString'] is not None) and (each_search_data['searchQueryPageNum'] == 0.0):
                google_search_count[each_search_data['searchQueryString']] += 1

            #getting maximum searchQuery number for each query
            if(MAX_page_num < each_search_data['searchQueryPageNum']):
                MAX_page_num = int(each_search_data['searchQueryPageNum'])


        user_page_num[user_id] = MAX_page_num
        



#load file function will call read file function to store json data 
def load_files(user_page_num,domain_count,google_search_count):

    entries =  os.listdir('data/') 
    for entry in entries:
        
        if entry.endswith("json"):            
            read_file(entry,user_page_num,domain_count,google_search_count)
            

# Index page
@app.route('/')
def index():
    
        
    #variables to store after reading the file
    user_page_num = {}
    domain_count = defaultdict(int)
    google_search_count = defaultdict(int)
    graph_features = ['Most Appeared Domain Names on Search','Top Google Search','Maximum Page Number Each User Search']


    #load file to read and store json data 
    load_files(user_page_num,domain_count,google_search_count)

    #plot main function
    current_feature_name,plot = plot_main(user_page_num,domain_count,google_search_count)
    
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("index.html", script=script, div=div,
        feature_names=graph_features,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)
