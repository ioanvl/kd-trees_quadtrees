from math import sqrt
import copy

class quadtree_node():
    def __init__(self, x: float, y: float ):
        self.x = x
        self.y = y
        self.coords = [x, y]

        self.branches = {
            'nw': None,
            'ne': None,
            'se': None,
            'sw': None
        }
    
    def get_quadrant(self, x, y):
        if y >= self.y:
            point = 'n'
        else:
            point = 's'
        if x >= self.x:
            point += 'e'
        else:
            point += 'w'
        return point

# =============================================================================

    def add_element(self, x: float, y: float):
        point = self.get_quadrant(x, y)
        if self.branches[point] is None:
            self.branches[point] = quadtree_node(x, y)
        else:
            self.branches[point].add_element(x, y)

# =============================================================================

    def search_element(self, x,y):
        if (self.x == x) and (self.y == y):
            return True
        else:
            point = self.get_quadrant(x,y)
            if self.branches[point] is not None:
                return self.branches[point].search_element(x,y)
            else:
                return False

# =============================================================================

    def knn_search(self, x, y, k=1, bounding_box=None, current_best=None):
        if bounding_box is None:
            bounding_box = {'x': {'e': None, 'w': None},
                            'y': {'n': None, 's': None}}

        flag = self.get_quadrant(x, y)

        if current_best is None:
            if self.branches[flag] is None:
                dist = sqrt((x - self.x)**2 + (y - self.y)**2)
                current_best = [{
                    'point': self,
                    'distance': dist
                }]
            else:
                bb = self.calc_branch_bounding_box(bounding_box, flag)
                current_best = self.branches[flag].knn_search(x, y, k, bb)
                current_best = self.check_self_dist(x, y, k, current_best)
        else:
            current_best = self.check_self_dist(x, y, k, current_best)
            
            if self.branches[flag] is not None:
                bb = self.calc_branch_bounding_box(bounding_box, flag)
                if self.check_branch(x, y, current_best=current_best, bbox=bb):
                    current_best = self.branches[flag].knn_search(x, y, k, bb, current_best=current_best)
        
        for others in self.branches:
            if others != flag:
                if self.branches[others] is not None:
                    bb = self.calc_branch_bounding_box(bounding_box, others)
                    if self.check_branch(x, y, current_best=current_best, bbox=bb):
                        current_best = self.branches[others].knn_search(x, y, k, bb, current_best=current_best)

        return current_best

# -----------------------------------------------

    def check_self_dist(self, x, y, k, current_best):
        dist = sqrt((x - self.x)**2 + (y - self.y)**2)
        if len(current_best) < k:
            point = {
                'point': self,
                'distance': dist
            }
            current_best.append(point)
            return current_best
        else:
            worst_best_d = -1
            worst_id = None
            for i in range(len(current_best)):
                if current_best[i]['distance'] > worst_best_d:
                    worst_best_d = current_best[i]['distance']
                    worst_id = i
            
            if worst_best_d > dist:
                point = {
                    'point': self,
                    'distance': dist
                }
                current_best.append(point)
                del current_best[worst_id]
            return current_best

# -----------------------------------------------

    def calc_branch_bounding_box(self, boundind_box, branch):
        bb = copy.deepcopy(boundind_box)

        bb['x'][branch[1]] = self.x     # branch [1] = East/West
        bb['y'][branch[0]] = self.y     # branch [0] = North/South

        return bb

    def check_branch(self, x, y, current_best, bbox):
        worst_best_d = -1
        for i in range(len(current_best)):
            if current_best[i]['distance'] > worst_best_d:
                worst_best_d = current_best[i]['distance']

        dist = 0
        # x dist
        if (bbox['x']['e'] is not None)  and (bbox['x']['e'] > x):
            dim_dist = (bbox['x']['e'] - x) ** 2
            dist += dim_dist
        elif (bbox['x']['w'] is not None)  and (bbox['x']['w'] < x):
            dim_dist = (bbox['x']['w'] - x) ** 2
            dist += dim_dist

        # y dist
        if (bbox['y']['n'] is not None)  and (bbox['y']['n'] > y):
                dim_dist = (bbox['y']['n'] - y) ** 2
                dist += dim_dist
        elif (bbox['y']['s'] is not None)  and (bbox['y']['s'] < y):
            dim_dist = (bbox['y']['s'] - y) ** 2
            dist += dim_dist

        dist = sqrt(dist)
        return (dist < worst_best_d)

# =============================================================================

    def storage(self, prev_list=None):
        if prev_list is None:
            prev_list = []

        point = (self.x, self.y)
        prev_list.append(point)

        for i in self.branches:
            if self.branches[i] is not None:
                prev_list = self.branches[i].storage(prev_list)

        return prev_list

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

