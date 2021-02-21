from math import sqrt
import copy

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

        if self.branches[flag] is None :
            dim = (self.dim + 1) % 2
            self.branches[flag] = kd_node(x, y, dim, parent = self)
        else:
            self.branches[flag].add_element(x, y)

# =============================================================================

    def build(self, point_list):
        if len(point_list) >= 5:
            cols = point_list.columns.tolist()
            df_dict = {
                'up': point_list[point_list[cols[self.dim]] >= self.coords[self.dim]],
                'low': point_list[point_list[cols[self.dim]] < self.coords[self.dim]]
            }

            for key in self.branches:
                if len(df_dict[key]):
                    if self.branches[key] is None:
                        check_dim = (self.dim + 1) % len(self.coords)
                        df_dict[key]['calc'] = (df_dict[key][cols[check_dim]] - df_dict[key][cols[check_dim]].median()).abs()

                        ind = df_dict[key][df_dict[key]['calc'] == df_dict[key]['calc'].min()].index[0]
                        point = df_dict[key].loc[ind, :]
                        self.add_element(point['x'], point['y'])
                        df_dict[key].drop(ind, inplace=True)

                    self.branches[key].build(df_dict[key])
            del df_dict

        else:
            for key in point_list.index:
                point = point_list.loc[key, :]
                self.add_element(point['x'], point['y'])
        del point_list

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

    # -----------------------------------------------

    def replace_self(self, point):
        self.x, self.y = point.x, point.y
        self.coords = [self.x, self.y]

    def delete_self(self):
        self.parent.cut_leaf(self)

    def cut_leaf(self, leaf):
        for x in self.branches:
            if self.branches[x] is leaf:
                self.branches[x] = None
                return

    # -----------------------------------------------

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

    def search_element(self, x, y):
        if (self.x == x) and (self.y == y):
            return True
        elif self.in_low_branch(x,y):
            if self.branches['low'] is not None:
                return self.branches['low'].search_element(x,y)
            else:
                return False
        else:
            if self.branches['up'] is not None:
                return self.branches['up'].search_element(x,y)
            else:
                return False

# =============================================================================

    def knn_search(self, x, y, k=1, bounding_box=None, current_best=None):
        if bounding_box is None:
            bounding_box = dict()
            for i in range(len(self.coords)):
                bounding_box[i] = {'up': None,
                'low': None}

        flag = self.in_low_branch(x,y)
        flag_a = 'low' if flag else 'up'
        flag_b = 'up' if flag else 'low'

        if current_best is None:
            if self.branches[flag_a] is not None:
                bb = self.calc_branch_bounding_box(bounding_box, flag_a)
                current_best = self.branches[flag_a].knn_search(x, y, k, bb)
                current_best = self.check_self_dist(x, y, k, current_best)
            else:
                dist = sqrt((x - self.x)**2 + (y - self.y)**2)
                current_best = [{
                    'point': self,
                    'distance': dist
                }]

        else:
            current_best = self.check_self_dist(x, y, k, current_best)

            if self.branches[flag_a] is not None:
                bb = self.calc_branch_bounding_box(bounding_box, flag_a)
                if self.check_branch(x, y, current_best=current_best, bbox=bb):
                #check branch -- pass cur best
                    current_best = self.branches[flag_a].knn_search(x, y, k, bb, current_best=current_best)
            
        if self.branches[flag_b] is not None:
            bb = self.calc_branch_bounding_box(bounding_box, flag_b)
            if self.check_branch(x, y, current_best=current_best, bbox=bb):
                #check branch -- pass cur best
                current_best = self.branches[flag_b].knn_search(x, y, k, bb, current_best=current_best)
                    
        return current_best

    # -----------------------------------------------

    def calc_branch_bounding_box(self, boundind_box, branch):
        bb = copy.deepcopy(boundind_box)
        bb[self.dim][branch] = self.coords[self.dim]
        return bb

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

    def check_branch(self, x, y, current_best, bbox):
        worst_best_d = -1
        for i in range(len(current_best)):
            if current_best[i]['distance'] > worst_best_d:
                worst_best_d = current_best[i]['distance']

        coords = [x, y]
        dist = 0
        for dim in bbox:
            if (bbox[dim]['up'] is not None)  and (bbox[dim]['up'] > coords[dim]):
                dim_dist = (bbox[dim]['up'] - coords[dim]) ** 2
                dist += dim_dist
            elif (bbox[dim]['low'] is not None)  and (bbox[dim]['low'] < coords[dim]):
                dim_dist = (bbox[dim]['low'] - coords[dim]) ** 2
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
                for _ in range(lv+1):
                    blank += '  '
                print(f"{blank}{x}:", end='')
                
                if self.branches[x] is None:
                    print("-null-")
                else:
                    self.branches[x].print(lv+1)