#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1

    def get_balance(self):
        """Calculate the balance factor of a node."""
        if not node:
            return 0
        return self.left.height - self.right.height	

	def right_rotation(self):
		newRoot = self.left
		T2 = newRoot.right

		#rotating
		newRoot.right = self
		self.left = T2

		#height update
		newRoot.height = 1 + max((newRoot.left.height),(newRoot.right.height))
		self.height = 1 + max((self.left.height),(self.right.height))

		#returning the new root
		return newRoot
	
	def left_rotataion(self):
		newRoot = self.right
		T2 = newRoot.left

		#rotating
		newRoot.left = self
		self.right = T2

		#height update
		newRoot.height = 1 + max((newRoot.left.height),(newRoot.right.height))
		self.height = 1 + max((self.left.height),(self.right.height))

		#returning the new root
		return newRoot

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None

	"""searches for a node in the dictionary corresponding to the key (starting at the given node)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	
	Complexity: 𝑂(𝑙𝑜𝑔𝑛)
	"""
	def nodesubtreesearch(self,key):
		len_search = 0  # in how many edges we pass
		node = self
		while node.is_real_node():
			len_search +=1
			if key == node.key:
				return node #found
			elif key < node.key:
				node = node.left
			else:
				node = node.right

		return node, len_search+1

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
		while (nodeparent!=None) and (node == nodeparent.right):
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




"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
<<<<<<< HEAD
	
=======
		self.max = None
		self.TreeSize = 0

>>>>>>> 2696fb2052e2cefa0680ab752ebfb81741d866bb

	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	
	Complexity: 𝑂(𝑙𝑜𝑔𝑛)
	"""
	def search(self, key):
		return self.root.key.nodesubtreesearch(key)



	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	
	Complexity: 𝑂(𝑙𝑜𝑔𝑛)
	"""
	def finger_search(self, key):
		len_search = 0
		node = self.max
		root = self.root
		if not node.is_real_node():
			return None, 1
		while (node.parent!=None) and (node.key>key): #findind the root of subtree where key is in
			len_search +=1
			node = node.parent

		foundnode, e = node.nodesubtreesearch(key)
		return foundnode,e+len_search





	def solid_insert(self, key, val):
		node = AVLNode(key, val)
        if self == None:
			node.height = 0
			self.Tree_Size = 1
			self.max = key
            return node
		# Recur into the left or right subtree
		if key < node.key:
			node.left = self.solid_insert(node.left, key, val)
			node.left.parent = node
		else:
			node.right = self.solid_insert(node.right, key, val)
			node.right.parent = node

		# Update height of this node after insertion
		node.height = 1 + max(self.height(node.left), self.height(node.right))

		# Update treesize and max value
		self.Tree_Size += 1
		if self.max < key:
			self.max = key

		return node
	
def promotion_count(self, node):
    """Counts the number of promotions (height updates) for a node."""
    if not node or not node.parent:  # Base case: node is None or the root
        return 0

    # Calculate the parent's new height based on its children
    left_height = node.parent.left.height if node.parent.left else -1
    right_height = node.parent.right.height if node.parent.right else -1
    new_parent_height = 1 + max(left_height, right_height)

    # Check if the parent's height increases
    if new_parent_height > node.parent.height:
        node.parent.height = new_parent_height  # Update parent's height
        return 1 + self.promotion_count(node.parent)  # Count promotion and recurse
    else:
        return 0  # No promotion occurs

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

		node = solid_insert(self, key, val)
        promotions = promotions_count(self, node)
		e_distance = self.root.height - node.height

        # Check balance factor and rotate if needed
        balance = get_balance(node)

		#determine the rotation that's needed (left-left, left-right, right-right, right-left)

        # Left-Left (Right Rotation)
        if balance > 1 and key < node.left.key:
            return self.right_rotation(node), e_distance, promotions - 1

        # Left-Right (Left-Right Rotation)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotation(node.left)
            return self.right_rotation(node), e_distance, promotions - 2

        # Right-Right (Left Rotation)
        if balance < -1 and key > node.right.key:
            return self.left_rotation(node), e_distance, promotions - 1

        # Right-Left (Right-Left Rotation)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotation(node.right)
            return self.left_rotation(node), e_distance, promotions - 2

        return node, e_distance, promotions  # Return the updated node, edge distance, and promotions

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
	#חסר עדכון גבהים בלמעלה של העץ
	def finger_insert(self, key, val):
		len_search = 0
		node = self.max
		while (node.parent != None) and (node.key > key):  # findind the root of subtree where key is in
			len_search += 1
			node = node.parent
		nodeTree = AVLTree()
		nodeTree.root = node
		newnode, e, numpromote, = nodeTree.insert(key, val)
		return  newnode, e+len_search, numpromote


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
		node = self.root.min_node()
		for i in range(self.TreeSize):
			argument = (node.key,node.value)
			arr.append(argument)
			node = node.Successor()
		return arr


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	Complexity: 𝑂(1)
	"""
	def max_node(self):
		return self.max

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


