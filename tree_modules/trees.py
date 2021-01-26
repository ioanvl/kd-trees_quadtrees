import pandas as pd

from .kdtree import kd_node
from .quadtree import quadtree_node

class tree():
    def __init__(self):
        self.root = None
    
    def add_element(self, x, y):
        raise NotImplemented
    
    def delete_element(self, x, y):
        if self.root is not None:
            return self.root.delete_element(x,y)
        else:
            return False
    
    def cut_leaf(self, leaf):
        self.root = None   
    
    def storage(self):
        if self.root is not None:
            return self.root.storage()
        else:
            return [False]
        
    
    def build(self, point_list):        
        point_list = pd.DataFrame(point_list, columns=['x', 'y'])

        if self.root is None:
            point_list['calc'] = (point_list['x'] - point_list['x'].median()).abs() + (point_list['y'] - point_list['y'].median()).abs()
            ind = point_list[point_list['calc'] == point_list['calc'].min()].index[0]
            point = point_list.loc[ind, :]

            self.add_element(point['x'], point['y'])
            point_list.drop(ind, inplace=True)
        
        self.root.build(point_list)

    def update(self):
        pass

    def search(self, x, y):
        if self.root is not None:
            return self.root.search_element(x,y)
        else:
            return False

    def knn_search(self, x, y, k=1):
        if self.root is not None:
            return self.root.knn_search(x,y,k)
        else:
            return []
        

class quad_tree(tree):
    def add_element(self, x, y):
        if self.root is not None:
            self.root.add_element(x, y)
        else:
            self.root = quadtree_node(x, y)

class kd_tree(tree):
    def add_element(self, x, y):
        if self.root is not None:
            self.root.add_element(x, y)
        else:
            self.root = kd_node(x, y, dim=0, parent=self)