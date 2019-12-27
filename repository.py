#!/usr/bin/env python
# coding: utf-8

# In[2]:


from git import Repo
import shutil
import os
import pygount
import json
from pathlib import Path
import lizard

class Repository:
    
    def __init__(self, repository, path, analysisFile):
        self.repository = repository
        self.path = path
        self.analysisFile = analysisFile
        
        self.codelines = 0
        self.emptylines = 0
        self.commentlines = 0
        
        # average cyclomatic complexity per repository
        self.averageCC = 0
        
        
    def download(self):
        Repo.clone_from(self.repository.clone_url, self.path+self.repository.name)
        print("Cloned Repository: ", self.repository.name)
        
    
    def analyse(self):
        
        ending = ''
        
        if self.repository.language == "Python":
            ending = '**/*.py'
        elif self.repository.language == "Java":
            ending = '**/*.java'
        else:
            print("Error in analyse: language of repository matches neither Python nor Java")
            return

        directory_in_str = self.path+self.repository.name

        pathlist = Path(directory_in_str).glob(ending)
        
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            analysis = pygount.source_analysis(path_in_str, self.repository.language, encoding = 'utf-8')
            self.codelines += analysis.code + analysis.string
            self.emptylines += analysis.empty
            self.commentlines += analysis.documentation   
            
        print("Analysed Repository: ", self.repository.name)
        return
    
    def analyseComplexity(self):
        ending = ''
        
        if self.repository.language == "Python":
            ending = '**/*.py'
        elif self.repository.language == "Java":
            ending = '**/*.java'
        else:
            print("Error in analyse: language of repository matches neither Python nor Java")
            return

        directory_in_str = self.path+self.repository.name

        pathlist = Path(directory_in_str).glob(ending)
        
        sum = 0
        function_count = 0
        
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            
           
            analysis = lizard.analyze_file(path_in_str)
            for element in analysis.function_list:
                sum += element.__dict__['cyclomatic_complexity']
                function_count += 1
            
        
        self.averageCC = sum/function_count
        
        print("Analysed Complexity of Repository: ", self.repository.name)
        return
        
    
                    
    def delete(self):
        shutil.rmtree(self.path+self.repository.name)
        print("Deleted Repository: ", self.repository.name)
        
    def dump(self):
        
        repo_info = {
                    'owner': self.repository.owner.login,
                    'name': self.repository.name,
                    'language': self.repository.language,
                    'stars': self.repository.stargazers_count,
                    'forks': self.repository.forks_count,
                    'codelines': self.codelines,
                    'commentlines': self.commentlines,
                    'emptylines': self.emptylines,
                    'averageCC': self.averageCC,
        }
            
        with open(self.analysisFile, 'a+') as f:
            f.write(json.dumps(repo_info, indent=4))
            f.write(',')
            
        print("Dumped data from Repository: {} (into file: {})".format(self.repository.name, self.analysisFile))
        

