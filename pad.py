 def nn_search(self, x, y, bounding_box, current_best=None):
        #if (self.x == x) and (self.y == y):
        #    
        #    return True

        if current_best is None:

            if self.in_low_branch(x,y):
                flag_a = low 
                flag_b = up
            else:
                flag_a = up 
                flag_b = low

            if self.branches[flag_a] is not None:

                best = self.branches[flag_a].nn_search(x,y)

                # check self
                    #if better replace best

            else:

                # KEEP distance with self as best 

            if self.branches[flag_b] is not None:
                # check other branch distance
                    #if viable 
                        #check branch -- pass cur best

                        # best = other_branch.nn_search( with cur best )

                # return best



        else: #yparxei current best
            
            # check self
                #if better replace best

            # check branch_a distance
                #if viable 
                    #check branch -- pass cur best
                    # best = branch_a.nn_search( with cur best )

            # check branch_b distance
                #if viable 
                    #check branch -- pass cur best
                    # best = branch_a.nn_search( with cur best )

            # return best