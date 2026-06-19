from backend.app.services.github_analyzer.github_analyzer import GitHubAnalyzer
from backend.app.services.leetcode_analyzer.leetcode_analyzer import LeetCodeAnalyzer

class AnalyzerRegistry:

    def __init__(self):
        '''
        Initializes the registry with available analyzers.
        (If new analyzers are added in the future, they should be registered here using add method.)
        '''
        self.analyzers = {
            "github": GitHubAnalyzer(),
            "leetcode": LeetCodeAnalyzer()
        }
    
    def add(self,name:str, analyzer):
        '''
        Adds a new analyzer to the registry.
        '''
        self.analyzers[name] = analyzer
    
    def run_all(self,username:str) -> dict:
        '''
        Runs all registered analyzers for the given username and returns a combined result.
        '''
        results = {}
        for name, analyzer in self.analyzers.items():
            results[name] = analyzer.analyze(username)
        return results