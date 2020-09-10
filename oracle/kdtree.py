import numpy as np
import heapq

# KDTree implementation
# Allows for finding nearest neighbor vectors in O(logn) time
class KDTree:

    # Init function
    def __init__(self, vectors, dim):
        self.dim = dim
        self.root = self.build_kdtree(vectors)

    # Recursively build the tree
    def build_kdtree(self, vectors, depth=0):
        n = len(vectors)
        mid = int(n / 2)
        # If the vector list is empty, then return None
        if n == 0:
            return None
        # Recursion
        axis = depth % self.dim
      #  print(vectors[0])
        sorted_vectors = sorted(vectors, key=lambda vec: vec["vector"][axis])
        return KDTreeNode(sorted_vectors[mid],
                          self.build_kdtree(sorted_vectors[:mid], depth=depth+1),
                          self.build_kdtree(sorted_vectors[mid+1:], depth=depth+1))
    
    # Get k best vectors from KDTree
    def get_best_vectors(self, vector, k):
        # Run the KNN search algorithm
        bpq = BoundedPriorityQueue(k)
        self._closest_vec(self.root, bpq, vector)
        # Return vectors, sorted by distance to the pivot
        ans = []
        for key in bpq.value_dict.keys():
            ans += [(-key, data) for data in bpq.value_dict[key]]  
        ans = sorted(ans, key = lambda it: it[0])
        return ans
    
    # Runs the K Nearest Neighbors Search algorithm
    def _closest_vec(self, curr, bpq, vec, depth=0):
        if curr == None:
            return
        # Add element to the Bounded Priority Queue
        bpq.insert_element(curr.vec, -distance(curr.vec, vec), curr.data)
        axis = depth % self.dim # Calculate axis
        # Search the half of the tree that contains the test point
        other = None
        if vec[axis] < curr.vec[axis]:
            self._closest_vec(curr.left, bpq, vec, depth=depth+1)
            other = curr.right
        else:
           self._closest_vec(curr.right, bpq, vec, depth=depth+1)
           other = curr.left
        # If the candidate hypersphere crosses this splitting plane, look on the other side 
        # of the plane by examining the other subtree
        if len(bpq.heap) != bpq.size or -bpq.heap[0] >= abs(curr.vec[axis] - vec[axis]):
            self._closest_vec(other, bpq, vec, depth=depth+1)


# Nodes for the KDTree
class KDTreeNode:

    def __init__(self, vec, left_node, right_node):
        self.vec = vec['vector']
        self.data = vec # stores the other data in the dictionary
        self.left = left_node
        self.right = right_node


# Bounded Priority Queue for K Nearest Neighbor Search
class BoundedPriorityQueue:

    def __init__(self, size):
        self.size = size
        self.heap = []
        self.value_dict = {}

    # insert element vector.  The value determines position (-distance)
    def insert_element(self, element, value, data):
        # If element_distance is greater than the current min, insert
        if len(self.heap) == self.size:
            if  value <= self.heap[0]:
                return
            # remove min element
            rem = heapq.heappop(self.heap)
            # Delete the values associated with dist
            # If the list has one element, delete the key
            # If it has more than one, pop off the end
            if len(self.value_dict[rem]) == 1:
                del self.value_dict[rem]
            else:
                self.value_dict[rem].pop()
        # Add element_distance => element mapping to the distance_dict
        if value not in self.value_dict:
            self.value_dict[value] = []
        self.value_dict[value].append(data)
        # insert new element
        heapq.heappush(self.heap, value)
        heapq.heapify(self.heap) # Build min heap


# Returns the euclidean distance between two vectors
def distance(vec1, vec2):
    return np.linalg.norm(vec1 - vec2)
