#!/usr/bin/env python
# coding: utf-8

# In[5]:


from git import Repo


class Repository:
    
    def __init__(self, repository, path):
        self.repository = repository
        self.path = path
        
    def download(self):
        Repo.clone_from(self.repository.clone_url, self.path)
        print("Cloned Repository: ", self.repository.name)

