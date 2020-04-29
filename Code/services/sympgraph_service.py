import json
from os import path
import sys
sys.path.append(path.abspath('../models'))
from sympgraph_model import sympgraphModel

class SympgraphService():
    def __init__(self):
        self.sympgraph_model = sympgraphModel()

    def getSymptoms(self, query):
        results = self.sympgraph_model.fetch(query)
        if(len(results) == 0):
            return []
        return results
