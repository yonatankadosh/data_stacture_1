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

    """returns the node balance factor
        	@rtype: int
        	@returns: left child height - right child height
        	Complexity: 𝑂(1)
        	"""

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

    """fixing the node height after changes
        	Complexity: 𝑂(1)
        	"""

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

    """ 
        returns the node with the Successor key in the tree 
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

    """
            Finds the node with the largest key smaller than the current node's key.
            @rtype: AVLNode
            @returns: The predecessor node, or None if no predecessor exists.
            Complexity: O(log n)
            """
    def Predecessor(self):
        # אם יש עץ שמאלי, המחסיר הוא הצומת הגדול ביותר בו
        if self.left and self.left.is_real_node():
            return self.left.max_node()

        # אחרת, נעלה במעלה העץ עד שנמצא צומת שהוא בן ימני
        node = self
        node_parent = node.parent
        while node_parent is not None and node == node_parent.left:
            node = node_parent
            node_parent = node.parent

        return node_parent

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

    """ create a new node with virtual children

        	@type key: int
        	@pre: key currently does not appear in the dictionary
        	@param key: key of item that is to be inserted to self
        	@type val: string
        	@param val: the value of the item
        	@rtype: AVLNode
        	@returns: the new node
        	Complexity: 𝑂(1)
        	"""

    def create_new_node(self, key, val):
        new_node = AVLNode(key, val)
        new_node.left = AVLNode()  # Virtual left child
        new_node.right = AVLNode()  # Virtual right child
        new_node.left.parent = new_node
        new_node.right.parent = new_node
        return new_node

    """ Update the max node in the tree after inserting a new node

            	@type key: int
            	@type new_node: AVLNode
            	@param key: key of item that is to be inserted to self
            	@param new_node: the new node in the tree
            	Complexity: 𝑂(1)
            	"""

    def update_max_node(self, key, new_node):
        """Update the max node in the tree."""
        if self.maxnode is None or key > self.maxnode.key:
            self.maxnode = new_node

    """
    Rebalances the AVL tree starting from the given node upwards to the root.

    This function ensures that after an insertion or deletion, the AVL tree
    remains balanced by updating the height of nodes and performing the
    necessary rotations.

    @type node: AVLNode
    @param node: The starting node from which to begin rebalancing.

    @type height_promotions: int
    @param height_promotions: The current count of height promotions (increases in height).

    @rtype: (AVLNode, int)
    @return: A tuple containing the new root of the tree and the updated count
             of height promotions.

    Complexity: 𝑂(logn)
    """

    def rebalance_upwards(self, node, height_promotions):
        current = node
        while current:
            # עדכון הגובה של הצומת הנוכחי
            old_height = current.height
            current.update_height()
            new_height = current.height

            # ספירת קידום אם הגובה גדל
            if new_height > old_height:
                height_promotions += 1

            # חישוב איזון מחדש
            balance = current.get_balance()

            if balance > 1:  # Left-heavy
                if current.left.get_balance() < 0:  # Left-Right case
                    current.left = self.left_rotation(current.left)
                current = self.right_rotation(current)

            elif balance < -1:  # Right-heavy
                if current.right.get_balance() > 0:  # Right-Left case
                    current.right = self.right_rotation(current.right)
                current = self.left_rotation(current)

            # עדכון השורש אם יש שינוי
            if current.parent is None:  # Current node is the new root
                self.root = current

            # מעבר לצומת האב
            current = current.parent

        # חזרה לשורש אם צריך
        while self.root and self.root.parent:
            self.root = self.root.parent

        return self.root, height_promotions

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

    	Complexity: 𝑂(logn)
    	"""

    def insert(self, key, val):
        if not self.root:
            # If the tree is empty, create a new root.
            self.root = self.create_new_node(key, val)
            self.maxnode = self.root
            self.TreeSize += 1
            return self.root, 1, 0

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
        new_node = self.create_new_node(key, val)

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

        return new_node, edge_count+1, height_promotions

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
        # Start from the maximum node and move upwards
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

    	Complexity o(logn)
    	"""

    def finger_insert(self, key, val):
        if not self.root:
            # אם העץ ריק, צור שורש חדש
            return self.insert(key, val)

        # התחלה מהמקסימום
        current = self.maxnode
        edge_count = 0

        # מציאת תת-העץ שבו המפתח החדש נמצא
        while current.parent and current.key > key:
            edge_count += 1
            current = current.parent

        # המשך חיפוש בתת-העץ שמצאנו
        parent = current
        direction = None

        while parent.is_real_node():
            if key < parent.key:
                direction = "left"
                if not parent.left.is_real_node():
                    break
                parent = parent.left
            else:
                direction = "right"
                if not parent.right.is_real_node():
                    break
                parent = parent.right
            edge_count += 1

        # יצירת הצומת החדש
        new_node = self.create_new_node(key, val)

        # חיבור הצומת החדש להורה
        if direction == "left":
            parent.left = new_node
        else:
            parent.right = new_node
        new_node.parent = parent

        # עדכון maxnode אם יש צורך
        if self.maxnode is None or key > self.maxnode.key:
            self.maxnode = new_node

        # איזון מחדש של העץ
        height_promotions = 0
        self.root, height_promotions = self.rebalance_upwards(new_node, height_promotions)
        self.TreeSize += 1

        return new_node, edge_count+1, height_promotions

    def left_rotation(self, node):
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

    """
        Performs a right rotation on the given node.

        Left rotation is used to fix left-heavy imbalance in an AVL tree.
        It involves shifting the node's left child up and making the node
        the right child of its left child.

        @type node: AVLNode
        @param node: The node to perform the right rotation on.
        @rtype: AVLNode
        @return: The new root of the subtree after rotation.

        Complexity: O(1)
        """

    def right_rotation(self, node):
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
    	Complexity: O(logn)
    	"""

    def delete(self, node):
        if not node.is_real_node():
            return

        def transplant(u, v):
            """
            Replace the subtree rooted at u with the subtree rooted at v.
            @type u: AVLNode
            @param u: The node to be replaced
            @type v: AVLNode
            @param v: The node to replace u

            Complexity: O(1)
            """
            if u.parent is None:
                self.root = v
            elif u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v

            if v.is_real_node():
                v.parent = u.parent

        # Case 1: Node is a leaf (no children)
        if not node.left.is_real_node() and not node.right.is_real_node():
            transplant(node, AVLNode())
            # Rebalance the tree upwards from the parent of the deleted node
            self.root, _ = self.rebalance_upwards(node.parent, 0)

        # Case 2: Node has only one child
        elif not node.left.is_real_node() or not node.right.is_real_node():
            transplant(node, node.right if node.right.is_real_node() else node.left)
            # Rebalance the tree upwards from the parent of the deleted node
            self.root, _ = self.rebalance_upwards(node.parent, 0)

        # Case 3: Node has two children
        else:
            # Find the successor
            successor = node.Successor()

            if successor.parent != node:
                transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor

            transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            # Rebalance the tree upwards from the successor
            self.root, _ = self.rebalance_upwards(successor, 0)

        # Update the maxnode if needed
        if node == self.maxnode:
            self.maxnode = node.Predecessor()

        # Update the tree size
        self.TreeSize -= 1

        # Disconnect the deleted node's references
        node.parent = None
        node.left = None
        node.right = None

    """joins self with item and another AVLTree

    	@type tree2: AVLTree 
    	@param tree2: a dictionary to be joined with self
    	@type key: int 
    	@param key: the key separting self and tree2
    	@type val: string
    	@param val: the value corresponding to key
    	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    	or the opposite way
        Complexity: 𝑂(logn)
    	"""

    def join(self, tree2, key, val):
        # edge cases
        if tree2 is None or tree2.root is None:  # If tree2 is empty
            new_node = self.create_new_node(key, val)
            if self.root:
                if key < self.root.key:
                    new_node.right = self.root
                    self.root.parent = new_node
                else:
                    new_node.left = self.root
                    self.root.parent = new_node
            return new_node

        if self.root is None:  # If the current tree is empty
            new_node = self.create_new_node(key, val)
            if tree2.root:
                if key < tree2.root.key:
                    new_node.right = tree2.root
                    tree2.root.parent = new_node
                else:
                    new_node.left = tree2.root
                    tree2.root.parent = new_node
            return new_node

        new_root = self.create_new_node(key, val)
        if tree2.root.key < self.root.key:
            # Assign `self` and `tree2` as left and right subtrees
            new_root.right = self.root
            new_root.left = tree2.root

        else:
            # Updete max value assuming tree2 max val is not giiven
            max_tree_2 = tree2.root
            while max_tree_2.right:
                max_tree_2 = max_tree_2.right
            self.maxnode = max_tree_2

            # Assign `self` and `tree2` as right and left subtrees
            new_root.left = self.root
            new_root.right = tree2.root

        # Update parent pointers
        if self.root:
            self.root.parent = new_root
        if tree2.root:
            tree2.root.parent = new_root

        # Rebalance the tree from the new root
        self.root = self.rebalance(new_root)

        # Clear tree2
        tree2.root = None

        return self.root

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """

    def split(self, x):
        """Splits the AVL tree into two trees: T1 (keys < x) and T2 (keys > x)."""
        T1 = AVLTree()  # Tree containing keys < x
        T2 = AVLTree()  # Tree containing keys > x
        current = self.root

        while current and current.is_real_node():
            if x < current.key:
                if current.right and current.right.is_real_node():
                    subtree = AVLTree()
                    subtree.root = current.right
                    T2.root = self.join(subtree, current.key, current.value)
                current = current.left
            elif x > current.key:
                if current.left and current.left.is_real_node():
                    subtree = AVLTree()
                    subtree.root = current.left
                    T1.root = self.join(subtree, current.key, current.value)
                current = current.right
            else:
                break

        if not current or not current.is_real_node():
            raise ValueError(f"Key {x} not found in the tree.")

        if current.left and current.left.is_real_node():
            left_subtree = AVLTree()
            left_subtree.root = current.left
            T1.root = self.join(left_subtree, current.key, current.value)
            current.left = None  # Detach the left subtree

        if current.right and current.right.is_real_node():
            right_subtree = AVLTree()
            right_subtree.root = current.right
            T2.root = self.join(right_subtree, current.key, current.value)
            current.right = None  # Detach the right subtree

        # Clear the original tree (self)
        self.root = None
        self.maxnode = None
        self.TreeSize = 0

        return T1, T2

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


