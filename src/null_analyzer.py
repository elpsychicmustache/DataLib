# ElPsychicMustache
# 2024-11-12

# Decided to move the entire NullAnalysis step of DataframeManager.process_data step, since it is a hefty process.
#   The idea is to abstract that step a little more and make DataframeManager more clean

import pandas as pd

class NullAnalyzer:
    def __init__(self):
        pass