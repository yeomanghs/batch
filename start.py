#import modules
import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import os
import re
from subprocess import Popen

file = 'D:/Users/figohjs/Desktop/Batch/Readme.xlsx'
folder = 'D:/Users/figohjs/Desktop/Batch/'

#read excel file
df = pd.read_excel(file)
df.index = np.arange(1, df.shape[0] + 1)

#sidebars
option = st.sidebar.selectbox("Type of Environment", ['Main', "Virtual"])

#button to appl dict
buttonToApp = {}

#activated List

#button to previous status dict
buttonToStatus = {'button%s'%i:False for i in range(df.shape[0])}

#num of appl using virtual environ 
ind = df.query('Type == "Main"').shape[0]

# #function to show working path
# def showWorkingPath():
#     wk = st.file_uploader("Upload working path")
#     if wk is not None:
#         #realWk = re.search('(.*)/*$', str(wk)).group(1)
#         #print(st.code(wk.read()))

def keyInWorkingPath(key, print = False):
    startPath = "D:/Users/figohjs/Documents"
    wp = st.text_input('Full Working Path:', startPath, key = key)
    button = st.button('Launch Jupyter notebook', key = 'JN')
    return wp, button

#function to run batch file
def runBatchFile(filename):
    # p = subprocess.Popen(folder + filename + '.bat', shell = True, stdout = subprocess.PIPE)
    # stdout, stderr = p.communicate()
    # return p.returncode
    os.chdir(folder)
    os.startfile(filename + '.bat')

if option == 'Main':
    df = df.query('Type == "%s"'%option)
    for no, row in enumerate(df.iterrows()):
        space = ' '*10
        st.markdown(row[1]['File'])
        st.markdown('Desc:' + row[1]['Desc'])
        buttonToApp['button' + str(no)] = row[1]['File']
        exec("button%s = st.button('Activate', key = str(%s))"%(no, no))
        st.write('-'*10)
    #showWorkingPath()
    fullPath, buttonJN = keyInWorkingPath(1)
    if buttonJN:
        os.chdir(folder)
        #os.startfile('hello.bat abc')
        Popen(['launchJN.bat', fullPath])

elif option == 'Virtual':
    df = df.query('Type == "%s"'%option)
    for no, row in enumerate(df.iterrows()):
        space = ' '*10
        st.markdown(row[1]['File'])
        st.markdown('Desc:' + row[1]['Desc'])
        buttonToApp['button' + str(no + ind)] = row[1]['File']
        exec("button%s = st.button('Activate', key = str(%s))"%(no + ind, no + ind))
        st.write('-'*10)
    #showWorkingPath()
    fullPath, buttonJN = keyInWorkingPath(2)
    if buttonJN:
        os.chdir(folder)
        #os.startfile('hello.bat abc')
        Popen(['launchJNTestEnv.bat', fullPath])

#activate batch files if False to True
currentButton = [i for i in globals() if re.search('button\d+', i)]
for i in currentButton:
    #if False to True
    if globals()[i]:
        runBatchFile(buttonToApp[i])

            

