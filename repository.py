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

# This represents a repository class
# its attributes are:  * Repository: of type pyGithub repository
#                      * Path: the path where the repository should be cloned
#                      * AnalysisFile: the path to the file where the results should be saved
#                      * Codelines: number of codelines from all source code files of a repository
#                      * Emptylines: number of emptylines from all source code files of a repository
#                      * Commentlines: number of commentlines from all source code files of a repository
#                      * AverageCC: the average cyclomatic complexity of a repository (average of all source code files)
class Repository:
    
    def __init__(self, repository, path, analysisFile):
        self.repository = repository
        self.path = path
        self.analysisFile = analysisFile
        
        self.codelines = 0
        self.emptylines = 0
        self.commentlines = 0
        
        self.averageCC = 0
        
    
    # method that clones a given repository in a specified path
    def download(self):
        Repo.clone_from(self.repository.clone_url, self.path+self.repository.name)
        print("Cloned Repository: ", self.repository.name)
     
    
    # method that analyses a repository (iterates through all code files and analyses it)
    def analyse(self):
        
        ending = ''
        # sets an ending variable to differentate the source code files of Python and Java repos 
        if self.repository.language == "Python":
            ending = '**/*.py'
        elif self.repository.language == "Java":
            ending = '**/*.java'
        else:
            print("Error in analyse: language of repository matches neither Python nor Java")
            return

        directory_in_str = self.path+self.repository.name

        pathlist = Path(directory_in_str).glob(ending)
        
        # loops through all folders in a repository to find all source code files and analyses them
        for path in pathlist:
            # because path is object not string
            path_in_str = str(path)
            analysis = pygount.source_analysis(path_in_str, self.repository.language, encoding = 'utf-8')
            self.codelines += analysis.code + analysis.string
            self.emptylines += analysis.empty
            self.commentlines += analysis.documentation   
            
        print("Analysed Repository: ", self.repository.name)
        return
    
    # analyses the complexity of a given repository
    def analyseComplexity(self):
        ending = ''
        
        # sets an ending variable to differentate the source code files of Python and Java repos 
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
        # loops through all folders in a repository to find all source code files and analyses their cyclomatic complexity
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
        
    
    # deletes a given repository from hard drive                
    def delete(self):
        shutil.rmtree(self.path+self.repository.name)
        print("Deleted Repository: ", self.repository.name)
     
    # dumps all analysed information of a repository into a given json file
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
        

