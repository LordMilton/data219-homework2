#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:12:02 2018

@author: Ashley
"""
#%%
import pandas as pd
import numpy as np
import statsmodels.nonparametric.smoothers_lowess
import matplotlib.pyplot as plt
everything = pd.read_csv('activity.csv')


students = everything[['name','year','major','school','creds']]

gpas = everything[['name','GPAFr', 'GPASo','GPAJr','GPASr']]
gpas.columns = ['name','Fr', 'So', 'Jr', 'Sr']
gpas = pd.melt(gpas, ['name'], var_name = 'year', value_name = 'gpa')
gpas = gpas[~np.isnan(gpas.gpa)]

schools = everything[['school','type','mascot']].drop_duplicates()

del everything

location = ['urban','rural','rural','urban','rural','urban']
schools['location'] = location
#%% Questions

#how many students are there in this data set?
print("There are " + str(len(students['name'])) + " students in this data set")

#How many total end-of-year GPA measurements do we have in this data set?
print("There are " + str(len(gpas['gpa'])) + " end-of-year GPA measurements in this data set")

#“What’s the overall average end-of-year GPA for these students?”
agv_gpa = round(gpas['gpa'].mean(), 2)
print("The overall average end-of-year GPA is " + str(agv_gpa))

#“How many students are there in rural vs. urban schools?”
student_location = pd.merge(students, schools, left_on = 'school', right_on = 'school')
student_location['location'].value_counts()
print("There are 10995 rural students and 9005 urban students")

#“How does the average freshman GPA compare between rural and urban schools?”
fresh_loc = student_location[(student_location.year == "Fresh")]
fresh_gpa = gpas[((gpas.year == "Fr"))] 
yet_another_merge = pd.merge(fresh_loc, fresh_gpa, left_on = 'name', right_on = 'name')
fresh_gpa_urban = yet_another_merge[yet_another_merge.location == 'urban']
fresh_gpa_rural = yet_another_merge[yet_another_merge.location == 'rural']
agv_gpa_urban = round(fresh_gpa_urban['gpa'].mean(), 2)
agv_gpa_rural = round(fresh_gpa_rural['gpa'].mean(), 2)

print("The average freshman GPA for urban students is " + str(agv_gpa_urban))
print("The average freshman GPA for rural students is " + str(agv_gpa_rural))    

#%%
# do freshmen GPAs differon average from non-freshmen? plot

fr_and_nonfr = gpas.copy()
fr_and_nonfr = fr_and_nonfr.replace(to_replace= 'Sr', value= 'nonfr')
fr_and_nonfr = fr_and_nonfr.replace(to_replace= 'Jr', value= 'nonfr')
fr_and_nonfr = fr_and_nonfr.replace(to_replace= 'So', value= 'nonfr')

fr_and_nonfr.boxplot(column= 'gpa', by= 'year', notch = True)
plt.xlabel('Year (Freshman/Non-Freshman)', fontsize=15)
plt.ylabel('GPA', fontsize=15)
plt.title('Freshman GPAs vs Non-Freshman GPAs', fontsize=16)
plt.suptitle("")

#%%QUESTION 11
# does the average year-end GPA vary significantly by major?
students['major'].value_counts()
gpa_majors = pd.merge(students, gpas, left_on = 'name', right_on = 'name')

gpa_majors = gpa_majors.drop(labels=['creds','name','school','year_x','year_y'], axis=1)
print(gpa_majors.head())
gpa_majors_plot = gpa_majors.boxplot(column='gpa',by='major',notch=True)
plt.xlabel('Major', fontsize=15)
plt.ylabel('GPA', fontsize=15)
plt.title('GPAs Compared by Major', fontsize=16)
plt.suptitle("")


#%% Question 12
#does the average year-end GPA vary significantly by school?
gpa_schools = pd.merge(gpas, students, on='name')
gpa_schools = gpa_schools.drop(labels=['year_y', 'creds', 'major', 'name', 'year_x'], axis=1)
gpa_schools.boxplot(column='gpa', by='school', notch=True)
plt.xlabel('GPA', fontsize=15)
plt.ylabel('School', fontsize=15)
plt.title('GPAs Compared By School', fontsize=16)
plt.suptitle("")

#%% Question 13
#Create a scatterplot showing number-of-credits vs. average-yearly-GPA, with a LOESS fit.
students_avgGpa = pd.merge(gpas,students,on='name')
students_avgGpa = students_avgGpa.drop(labels=['major','year_x','year_y','school','creds'],axis=1)
students_avgGpa = students_avgGpa.groupby('name').mean()
students_avgGpa = students_avgGpa.reset_index()
print(students_avgGpa.head())

students_credits = students.copy()
students_credits = students_credits.drop(labels=['major','year','school'],axis=1)
students_credits = students_credits.drop_duplicates()
print(students_credits.head())

gpa_creds = pd.merge(students_avgGpa,students_credits,on='name')
plt.scatter(gpa_creds.creds, gpa_creds.gpa)
lowess = statsmodels.nonparametric.smoothers_lowess.lowess(gpa_creds.gpa, gpa_creds.creds, frac=1/4)
plt.plot(lowess[:,0], lowess[:,1], color='red')
plt.xlabel('Current Credits', fontsize=15)
plt.ylabel('Average Yearly GPA', fontsize=15)
plt.title('Average GPA vs Current Number of Credits', fontsize=16)
