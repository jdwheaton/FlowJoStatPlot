# FlowJoStatPlot
A python package (and eventual web app) to quickly plot summary statistics output from the FlowJo table editor.

## The Problem:
Those who regularly analyze flow cytometry (FACS) experiments will be familiar with the following workflow:

1. Gate your populations of interest
2. Generate summary statistics (% of parent, gMFI, etc.) for these populations using the table editor
3. Copy the table to an Excel spreadsheet
4. Laboriously copy and manually reformat (usually transpose) these values into some statistical / graphing software such as GraphPad Prism

Steps 3 and 4 are *repetetive, incredibly boring, and time-consuming*. For my workflow - and that of many others - this task should be easy to automate with Python, but this doesn't appear to have been done yet.

## The (Eventual) Solution:

This repository will serve as a home for code related to this mission. Eventually, the usage should look something like this:

1. Export CSV file from FlowJo table editor
2. Use your favorite spreadsheet editor to assign grouping variables within the CSV file ***OR*** Specify a simple pattern to automagically append these values within this python module.
3. Define the sample groupings of interest (i.e. one-factor vs two-factor experiments)
4. Automatically have summary plots generated for each and every parameter in the table, with automatic gate detection and labeling. This may be extended to provide simple statistics as well.

If the above is accomplished, it should be relatively trivial to turn this into a Django or Flask web-app that allows users to upload a CSV file and receive a PDF with all of the graphs!

