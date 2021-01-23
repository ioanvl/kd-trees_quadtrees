class kd_node():
    def __init__(self, x: float, y: float, dim=0, parent=None):
        self.x = x
        self.y = y
        self.coords = [x, y]
        self.dim = dim
        self.parent = parent

        self.branches = {
            'up': None,
            'low': None
        }

    def in_low_branch(self, x, y):
        p = [x,y]
        return p[self.dim] < self.coords[self.dim]

# =============================================================================

    def add_element(self, x, y):
        flag = 'low' if self.in_low_branch(x, y) else 'up'
#        if self.dim == 0:
#            if x >= self.x:
#                flag = 'up'
#        else:
#            if y >= self.y:
#                flag = 'up'
        
#        if self.in_low_branch(x, y):
#            flag = 'low'
#        else:
#            flag = 'up'

        if self.branches[flag] is None :
            dim = (self.dim + 1) % 2
            self.branches[flag] = kd_node(x, y, dim, parent = self)
        else:
            self.branches[flag].add_element(x, y)

# =============================================================================

    def find_min(self, dim):
        if self.dim == dim:
            if self.branches['low'] is None:
                return self
            else:
                return self.branches['low'].find_min(dim)
        else:
            point = self
            if self.branches['low'] is not None:
                min_left = self.branches['low'].find_min(dim)
                point = self.min_on_dimension(point, min_left, dim)
            if self.branches['up'] is not None:
                min_right = self.branches['up'].find_min(dim)
                point = self.min_on_dimension(point, min_right, dim)
            return point

    def min_on_dimension(self, point_a, point_b, dim):
        if point_a.coords[dim] <= point_b.coords[dim]:
            return point_a
        else:
            return point_b

# =============================================================================

    def delete_element(self, x, y):
        if (self.x == x) and (self.y == y):
            if self.branches['up'] is not None:
                min_point = self.branches['up'].find_min(self.dim)
                self.replace_self(min_point)

                self.branches['up'].delete_element(self.x, self.y)

            elif self.branches['low'] is not None:
                min_point = self.branches['low'].find_min(self.dim)
                self.replace_self(min_point)

                self.branches['up'] = self.branches['low']
                self.branches['low'] = None
                self.branches['up'].delete_element(self.x, self.y)

            else:
                self.delete_self()
            return True

        elif self.in_low_branch(x,y):
            if self.branches['low'] is not None:
                return self.branches['low'].delete_element(x,y)
            else:
                return False
        else:
            if self.branches['up'] is not None:
                return self.branches['up'].delete_element(x,y)
            else:
                return False

    def delete_self(self):
        self.parent.cut_leaf(self)

    def cut_leaf(self, leaf):
        for x in self.branches:
            if self.branches[x] is leaf:
                self.branches[x] = None
                return

    def replace_self(self, point):
        self.x, self.y = point.x, point.y
        self.coords = [self.x, self.y]

# =============================================================================

    def print(self, lv=0):
        print(f"[{self.x}, {self.y}]", end='')
        flag = False
        for x in self.branches:
            if self.branches[x] is not None:
                flag = True
                break
        if not flag:
            print('')
            return
        else:
            print(':')
            for x in self.branches:
                blank = ''
                for i in range(lv+1):
                    blank += '  '
                print(f"{blank}{x}:", end='')
                
                if self.branches[x] is None:
                    print("-null-")
                else:
                    self.branches[x].print(lv+1)