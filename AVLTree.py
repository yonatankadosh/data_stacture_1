def printree(t, bykey=True):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    # for row in trepr(t, bykey):
    #        print(row)
    return trepr(t, bykey)
def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if t == None:
        return ["#"]

    thistr = str(t.key) if bykey else str(t.val)

    return conc(trepr(t.left, bykey), thistr, trepr(t.right, bykey))
def conc(left, root, right):
    """Return a concatenation of textual represantations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "|" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result
def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1
def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i

class AVLNode(object):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1 if key is None else 0

    def get_balance(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        return left_height - right_height

    """returns whether self is not a virtual node 

    	@rtype: bool
    	@returns: False if self is a virtual node, True otherwise.
    	Complexity: 𝑂(1)
    	"""
    def is_real_node(self):
        return self.key is not None

    def update_height(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        self.height = 1 + max(left_height, right_height)

    """searches for a node in the dictionary corresponding to the key (starting at the given node)

    	@type key: int
    	@param key: a key to be searched
    	@rtype: (AVLNode,int)
    	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    	and e is the number of edges on the path between the starting node and ending node+1.

    	Complexity: 𝑂(𝑙𝑜𝑔𝑛)
    	"""
    def nodesubtreesearch(self, key):
        edge_distance = 0  # in how many edges we pass
        node = self
        while node and node.is_real_node():
            if key == node.key:
                return node, edge_distance  # found
            elif key < node.key:
                node = node.left
            else:
                node = node.right
            edge_distance += 1

        return node, edge_distance + 1

    """returns the node with the Successor key in the tree 

    			@rtype: AVLNode
    			@returns: the Successor node
    			Complexity: 𝑂(𝑙𝑜𝑔𝑛)
    			"""
    def Successor(self):
        if self.right.is_real_node():
            return self.right.min_node()
        node = self
        nodeparent = node.parent
        while (nodeparent != None) and (node == nodeparent.right):
            node = nodeparent
            nodeparent = node.parent
        return nodeparent

    """returns the node with the minimal key in the node sub tree

        @rtype: AVLNode
        @returns: the minimal node, None if the given node is none
        Complexity: 𝑂(𝑙𝑜𝑔𝑛)
        """
    def min_node(self):
        node = self
        while node.left.is_real_node():
            node = node.left
        return node

class AVLTree(object):
    def __init__(self):
        self.root = None
        self.maxnode = None
        self.TreeSize = 0
    def __repr__(self):  # no need to understand the implementation of this one
        out = ""
        for row in printree(self.root):  # need printree.py file
            out = out + row + "\n"
        return out

    def recursive_insert(self,node, key, val):
        if not node or not node.is_real_node():
            self.TreeSize += 1
            new_node = AVLNode(key, val)
            new_node.left = AVLNode()  # Virtual left child
            new_node.right = AVLNode()  # Virtual right child
            new_node.left.parent = new_node
            new_node.right.parent = new_node
            return new_node, 0

        edge_distance = 0
        if key < node.key:
            node.left, edge_distance = self.recursive_insert(node.left, key, val)
            node.left.parent = node
        else:
            node.right, edge_distance = self.recursive_insert(node.right, key, val)
            node.right.parent = node

        node.update_height()
        node = self.rebalance(node)
        return node, edge_distance + 1


    def update_max_node(self, key, new_node):
        """Update the max node in the tree."""
        if self.maxnode is None or key > self.maxnode.key:
            self.maxnode = new_node

    def rebalance(self, node):
        """Rebalance the tree at the given node."""
        balance = node.get_balance()

        if balance > 1:  # Left-heavy
            if node.left.get_balance() < 0:  # Left-Right case
                node.left = node.left.left_rotation()
            return node.right_rotation()

        if balance < -1:  # Right-heavy
            if node.right.get_balance() > 0:  # Right-Left case
                node.right = node.right.right_rotation()
            return node.left_rotation()

        # Ensure leaves have virtual children
        if not node.left:
            node.left = AVLNode()
            node.left.parent = node
        if not node.right:
            node.right = AVLNode()
            node.right.parent = node

        return node

    def promotion_count(self, node):
        """Count height promotions during rebalancing."""
        if not node or not node.parent:
            return 0

        left_height = node.parent.left.height if node.parent.left else -1
        right_height = node.parent.right.height if node.parent.right else -1
        new_parent_height = 1 + max(left_height, right_height)

        if new_parent_height > node.parent.height:
            node.parent.height = new_parent_height
            return 1 + self.promotion_count(node.parent)
        return 0

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    	@type key: int
    	@pre: key currently does not appear in the dictionary
    	@param key: key of item that is to be inserted to self
    	@type val: string
    	@param val: the value of the item
    	@rtype: (AVLNode,int,int)
    	@returns: a 3-tuple (x,e,h) where x is the new node,
    	e is the number of edges on the path between the starting node and new node before rebalancing,
    	and h is the number of PROMOTE cases during the AVL rebalancing
    	"""
    def insert(self, key, val):
        if not self.root:
            # If the tree is empty, create a new root.
            self.root = AVLNode(key, val)
            self.root.left = AVLNode()  # Virtual left child
            self.root.right = AVLNode()  # Virtual right child
            self.root.left.parent = self.root
            self.root.right.parent = self.root
            self.maxnode = self.root
            self.TreeSize += 1
            return self.root, 0, 0

        # Traverse the tree to find the correct insertion point
        current = self.root
        parent = None
        direction = None
        edge_count = 0

        while current.is_real_node():
            parent = current
            edge_count += 1
            if key < current.key:
                direction = "left"
                current = current.left
            else:
                direction = "right"
                current = current.right

        # Create the new node
        new_node = AVLNode(key, val)
        new_node.left = AVLNode()  # Virtual left child
        new_node.right = AVLNode()  # Virtual right child
        new_node.left.parent = new_node
        new_node.right.parent = new_node

        # Attach the new node to the parent
        if direction == "left":
            parent.left = new_node
        else:
            parent.right = new_node
        new_node.parent = parent

        # Update the max node if necessary
        if self.maxnode is None or key > self.maxnode.key:
            self.maxnode = new_node
        # add to the tree size
        self.TreeSize += 1

        # Rebalance the tree upwards
        height_promotions = 0
        self.root, height_promotions = self.rebalance_upwards(new_node, height_promotions)

        return new_node, edge_count, height_promotions

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    	@type key: int
    	@param key: a key to be searched
    	@rtype: (AVLNode,int)
    	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    	and e is the number of edges on the path between the starting node and ending node+1.

    	Complexity: 𝑂(𝑙𝑜𝑔𝑛)
    	"""
    def search(self, key):
        return self.root.nodesubtreesearch(key)

    """searches for a node in the dictionary corresponding to the key, starting at the max

    	@type key: int
    	@param key: a key to be searched
    	@rtype: (AVLNode,int)
    	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    	and e is the number of edges on the path between the starting node and ending node+1.

    	Complexity: 𝑂(𝑙𝑜𝑔𝑛)
    	"""
    def finger_search(self, key):
        edge_distance = 0
        node = self.maxnode
        if not node.is_real_node():
            return None, 1
        while (node.parent is not None) and (node.key > key):  # finding the root of subtree where key is in
            edge_distance += 1
            node = node.parent

        foundnode, e = node.nodesubtreesearch(key)
        return foundnode, e + edge_distance

    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    	@type key: int
    	@pre: key currently does not appear in the dictionary
    	@param key: key of item that is to be inserted to self
    	@type val: string
    	@param val: the value of the item
    	@rtype: (AVLNode,int,int)
    	@returns: a 3-tuple (x,e,h) where x is the new node,
    	e is the number of edges on the path between the starting node and new node before rebalancing,
    	and h is the number of PROMOTE cases during the AVL rebalancing

    	Complexity
    	"""
    def finger_insert(self, key, val):

        if not self.root:
            # If the tree is empty, create a new root.
            return self.insert(key, val)

        # Start from the maximum node and move upwards
        current = self.maxnode
        edge_count = 0

        while current and current.key > key:
            edge_count += 1
            current = current.parent

        # Determine where to insert the new node
        if key < current.key:
            parent = current
            direction = "left"
        else:
            parent = current
            direction = "right"

        # Create the new node
        new_node = AVLNode(key, val)
        new_node.left = AVLNode()  # Virtual left child
        new_node.right = AVLNode()  # Virtual right child
        new_node.left.parent = new_node
        new_node.right.parent = new_node

        # Attach the new node to the parent
        if direction == "left":
            parent.left = new_node
        else:
            parent.right = new_node
        new_node.parent = parent

        # Update the max node if necessary
        if self.maxnode is None or key > self.maxnode.key:
            self.maxnode = new_node

        # Rebalance the tree upwards
        height_promotions = 0
        self.root, height_promotions = self.rebalance_upwards(new_node, height_promotions)
        # add to the tree size
        self.TreeSize += 1

        return new_node, edge_count, height_promotions

    """
        Rebalanced the tree upwards starting from a given node.

        @type node: AVLNode
        @param node: The starting node for rebalancing.
        @type height_promotions: int
        @param height_promotions: The current count of height promotions.
        @rtype: (AVLNode, int)
        @returns: The root of the tree and the updated height promotions count.
        """
    def rebalance_upwards(self, node, height_promotions):
        current = node
        while current:
            current.update_height()
            balance = current.get_balance()

            if balance > 1:  # Left-heavy
                if current.left.get_balance() < 0:  # Left-Right case
                    current.left = self.left_rotation(current.left)
                current = self.right_rotation(current)

            elif balance < -1:  # Right-heavy
                if current.right.get_balance() > 0:  # Right-Left case
                    current.right = self.right_rotation(current.right)
                current = self.left_rotation(current)

            # Ensure the root updates correctly after rotations
            if current.parent is None:  # Current node is the new root
                self.root = current

            # Count promotions
            if current.parent and current.height > current.parent.height:
                height_promotions += 1

            current = current.parent

        # Ensure the root is updated correctly
        while self.root and self.root.parent:
            self.root = self.root.parent

        return self.root, height_promotions

    def left_rotation(self, node):
        """
        Perform a left rotation on the given node.

        @type node: AVLNode
        @param node: The node to perform left rotation on.
        @rtype: AVLNode
        @returns: The new root after rotation.
        """
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        new_root.left = node
        new_root.parent = node.parent
        if node.parent:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        node.parent = new_root
        node.update_height()
        new_root.update_height()
        return new_root

    def right_rotation(self, node):
        """
        Perform a right rotation on the given node.

        @type node: AVLNode
        @param node: The node to perform right rotation on.
        @rtype: AVLNode
        @returns: The new root after rotation.
        """
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
        new_root.right = node
        new_root.parent = node.parent
        if node.parent:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        node.parent = new_root
        node.update_height()
        new_root.update_height()
        return new_root

    """deletes node from the dictionary

    	@type node: AVLNode
    	@pre: node is a real pointer to a node in self
    	"""
    def delete(self, node):
        return

    """joins self with item and another AVLTree

    	@type tree2: AVLTree 
    	@param tree2: a dictionary to be joined with self
    	@type key: int 
    	@param key: the key separting self and tree2
    	@type val: string
    	@param val: the value corresponding to key
    	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    	or the opposite way
    	"""
    def join(self, tree2, key, val):
        return

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """
    def split(self, node):
        return None, None

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    Complexity: 𝑂(nlogn)
    """
    def avl_to_array(self):
        arr = []
        if self.root is None:  # empty tree
            return arr
        node = self.root.min_node()
        print(self.TreeSize)
        for i in range(self.TreeSize):
            argument = (node.key, node.value)
            arr.append(argument)
            node = node.Successor()
        return arr

    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    Complexity: 𝑂(1)
    """
    def max_node(self):
        return self.maxnode

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    Complexity: 𝑂(1)
    """
    def size(self):
        return self.TreeSize

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    Complexity: 𝑂(1)
    """
    def get_root(self):
        return self.root


tree = AVLTree()
tree.insert(1,'1')
print(tree)

