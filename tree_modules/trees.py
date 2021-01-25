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
        pass
    def build(self):
        pass

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
            self.root = quadtree_node(x, y, dim=0, parent=self)

class kd_tree(tree):
    def add_element(self, x, y):
        if self.root is not None:
            self.root.add_element(x, y)
        else:
            self.root = kd_node(x, y, dim=0, parent=self)