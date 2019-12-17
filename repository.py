#!/usr/bin/env python
# coding: utf-8

# In[17]:


from git import Repo
import shutil
import os
import pygount
import json

class Repository:
    
    def __init__(self, repository, path, analysisFile):
        self.repository = repository
        self.path = path
        self.analysisFile = analysisFile
        
        self.codelines = 0
        self.emptylines = 0
        self.commentlines = 0
        
        
    def download(self):
        Repo.clone_from(self.repository.clone_url, self.path+self.repository.name)
        print("Cloned Repository: ", self.repository.name)
        
    
    def analyse(self):
        
        ending = ''
        
        if self.repository.language == "Python":
            ending = '.py'
        elif self.repository.language == "Java":
            ending = '.java'
        else:
            print("Error in analyse: language of repository matches neither Python nor Java")
            return
        
        # Recursive iteration through repository
        contents = self.repository.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repository.get_contents(file_content.path))
            else:
                if os.path.splitext(file_content.path)[1]==ending:
                    analysis = pygount.source_analysis(self.path+self.repository.name+'/'+file_content.path, self.repository.language, encoding = 'utf-8')
                    self.codelines += analysis.code + analysis.string
                    self.emptylines += analysis.empty
                    self.commentlines += analysis.documentation
        
        print("Analysed Repository: ", self.repository.name)
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
        }
            
        with open(self.analysisFile, 'a+') as f:
            f.write(json.dumps(repo_info, indent=4))
            f.write(',')
            
        print("Dumped data from Repository: {} (into file: {})".format(self.repository.name, self.analysisFile))
        

