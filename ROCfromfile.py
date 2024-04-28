from result_methods import Roc
import json
import os

roc = Roc(None, None, None, None)
# load from json
with open("assets/results\GOOD ROC/roc_curve.json") as file:
    results = json.load(file)

# make new folder
# os.makedirs("D:\Coding\PerceptionHash/assets/results\GOOD ROC/new")
roc.generate_graphs(results, "assets/results\GOOD ROC\ROC_GOODFONT")
# roc.generate_auc(results, "D:\Coding\PerceptionHash/assets/results\GOOD ROC/new")