#id1:212201735
#name1:Gad Rozen
#username1:gadrozen
#id2: 314621509
#name2: Hila Etziony
#username2: hilaetziony


"""A class representing a node in an AVL tree"""

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


    """returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self):
        return self.key is not None and self.value is not None

    """updates the height of self"""

    def update_height(self):
        self.height = 1 + max(self.left.height, self.right.height)

    "reset node pointers"

    def delete_pointers(self):
        self.left = AVLNode(None, None)
        self.left.parent = self
        self.right = AVLNode(None, None)
        self.right.parent = self
        self.parent = None


"""
A class implementing an AVL tree.
"""

class AVLTree(object):
    """
	Constructor, you are allowed to add more fields.
	"""

    def __init__(self):
        self.root = None
        self.maxNode = None
        self.Size = 0

    """creates a new node with the given key and value, 
	   node.left and node.right is virtual node, 
	   height is updated and parent is None.

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item 
	@type val: string
	@param val: the value of the item
	@rtype: AVLNode
	@returns: new node with the given key and value
	"""

    def create_leaf(self, key, val):
        new_node = AVLNode(key, val)
        new_node.left = AVLNode(None, None)
        new_node.left.parent = new_node
        new_node.right = AVLNode(None, None)
        new_node.right.parent = new_node
        new_node.update_height()
        return new_node

    """Searches for a node in the AVL tree by key and returns the node along with the number of steps taken until the key is found + 1.

    The function searches for the key in the tree while counting the number of steps taken until the node with the desired key is found + 1.
    If the key is not found, it returns the last node checked, or None if ReturnLastNode is set to False.

    @type node: AVLNode
    @param node: The starting node where the search begins.
    @type key: int
    @param key: The key of the node to search for.
    @type stepsTaken: int
    @param stepsTaken: The number of steps taken so far during the search.
    @type ReturnLastNode: bool
    @param ReturnLastNode: If True, the function returns the last node checked if the key is not found. If False, it returns None.
    @rtype: (AVLNode, int)
    @returns: A tuple containing the found node (or None if not found) and the number of steps taken until the node was found + 1. If ReturnLastNode is False, the function returns None if the key is not found.
    """

    def Search_by_node(self, node, key, stepsTaken=0, ReturnLastNode=False):
        if self.root is None:
            return None, stepsTaken +1
        KeepFatherNode = node
        stepsTaken += 1
        while node.key is not None:
            KeepFatherNode = node
            if node.key == key:
                return node, stepsTaken
            elif key < node.key:
                node = node.left
            else:
                node = node.right

            if node.key is not None:
                stepsTaken += 1
        # if node not found and we want to return his father
        if ReturnLastNode:
            return KeepFatherNode, stepsTaken
        return None, stepsTaken

    """searches for a node in the dictionary corresponding to the key (starting at the root)
    The function searches for the key in the tree, starting from the root node.
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""

    def search(self, key):
        if self.root is None:
            return None, 1
        TopNode = self.get_root()
        return self.Search_by_node(TopNode, key)  

    """searches for a node in the dictionary corresponding to the key, starting at the max

	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""

    def finger_search(self, key):
        if self.root is None:
            return None, 1
        return self.finger_search_by_node(key)

    """Searches for a node in the AVL tree by key, starting at the max

    @type key: int
    @param key: The key of the node to search for.
    @type ReturnLastNode: bool
    @param ReturnLastNode: If True, the function returns the last node checked if the key is not found. If False, it returns None if the key is not found.
    @rtype: (AVLNode, int)
    @returns: A tuple containing the found node (or None if not found) and the number of steps taken during the search +1.
    """

    def finger_search_by_node(self, key , ReturnLastNode = False):
        pathNodeCount = 0
        max_node = self.maxNode


        # climb up to the first node whose key is smaller or equal to key
        while max_node.key != self.get_root().key and max_node.key > key:
            if max_node.parent.key < key:
                break
            max_node = max_node.parent
            pathNodeCount += 1

        return self.Search_by_node(max_node, key , pathNodeCount , ReturnLastNode )


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
        steps, promote = 0,0
        # create the node with the key and value
        new_node = self.create_leaf(key, val)
        # search the place in the AVL tree for the new node
        if self.root is not None:
            n, steps = self.Search_by_node(self.root, key, ReturnLastNode=True)
            # if the key is already in the tree - change its node's value and return
            if n.key == key:
                n.value = val
                return n, steps, 0
            else:
                new_node.parent = n
            self.update_parent_child(new_node)
        else:
            self.root = new_node
        self.update_size_and_maxNode_after_insert(new_node)
        promote = self.rebalancing_after_insert(new_node)
        return new_node, steps, promote

    """update the new node to be his new left or right child according to the key

    @type new_node: Node
    @param new_node: the new node that was inserted
    """
    def update_parent_child(self,new_node):
        if new_node.key < new_node.parent.key:
            new_node.parent.left = new_node
        else:
            new_node.parent.right = new_node

    """update size and maxNode after insert

    @type new_node: Node
    @param new_node: the new node that was inserted
    """
    def update_size_and_maxNode_after_insert(self, new_node):
        # update maxNode and size fields of the tree
        self.Size += 1
        if self.maxNode is None:
            self.maxNode = new_node
        elif new_node.key > self.maxNode.key:
            self.maxNode = new_node

    """rebalancing self after insert

	@type new_node: Node
	@param new_node: the new node that was inserted
	@rtype: int
	@returns: the number of PROMOTE cases during the AVL rebalancing
  	"""

    def rebalancing_after_insert(self, new_node):
        # rebalancing the tree if necessary
        promote = 0
        # check if new node is not the root
        if new_node.parent is not None:
            # the parent is a leaf
            if new_node.parent.height == 0:
                promote = self.rebalance_from_specific_node(new_node.parent)
        return promote

    """rebalancing self from a given node 

	@type node: AVLNode
	@param node: the node that was inserted
	@rtype: int
	@returns: the number of PROMOTE cases during the AVL rebalancing
	"""

    def rebalance_from_specific_node(self, node):
        fixed = False
        promote = 0
        while not fixed:
            diff_height_left_side = node.height - node.left.height
            diff_height_right_side = node.height - node.right.height
            # tree is fixed - rebalancing self is finished
            if diff_height_left_side == 1 and diff_height_right_side == 1:
                fixed = True
            # Case 1 from class and its symmetry case.
            elif (diff_height_left_side == 0 and diff_height_right_side == 1) or (
                    diff_height_left_side == 1 and diff_height_right_side == 0):
                node.update_height()
                promote += 1
                if node.parent is not None:
                    node = node.parent
                else:
                    fixed = True
            # Case 2 & 3 from c                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         lass
            elif diff_height_left_side == 0 and diff_height_right_side == 2:
                left_child = node.left
                left_child_diff_height_left_side = left_child.height - left_child.left.height
                left_child_diff_height_right_side = left_child.height - left_child.right.height
                # Case 2 from class
                if left_child_diff_height_left_side == 1 and left_child_diff_height_right_side == 2:
                    self.rotate_right(node)
                    fixed = True
                # Case 3 from class
                elif left_child_diff_height_left_side == 2 and left_child_diff_height_right_side == 1:
                    self.rotate_left_right(node)
                    fixed = True
                # this case is relevant only for join and not for insert.
                elif left_child_diff_height_left_side == 1 and left_child_diff_height_right_side == 1:
                    node = self.rotate_right(node)
                    if node.parent is not None:
                        node = node.parent
                    else:
                        fixed = True
            # symmetry case of case 2 & 3 from class
            elif diff_height_left_side == 2 and diff_height_right_side == 0:
                right_child = node.right
                right_child_diff_height_left_side = right_child.height - right_child.left.height
                right_child_diff_height_right_side = right_child.height - right_child.right.height
                # symmetry of case 3 from class
                if right_child_diff_height_left_side == 1 and right_child_diff_height_right_side == 2:
                    self.rotate_right_left(node)
                    fixed = True
                # symmetry of case 2 from class
                elif right_child_diff_height_left_side == 2 and right_child_diff_height_right_side == 1:
                    self.rotate_left(node)
                    fixed = True
                # this case is relevant only for join and not for insert.
                elif right_child_diff_height_left_side == 1 and right_child_diff_height_right_side == 1:
                    node = self.rotate_left(node)
                    if node.parent is not None:
                        node = node.parent
                    else:
                        fixed = True
        return promote

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
	"""

    def finger_insert(self, key, val):
        steps, promote = 0, 0
        # create the node with the key and value
        new_node = self.create_leaf(key, val)
        # search the place in the AVL tree for the new node
        if self.root is not None:
            n, steps = self.finger_search_by_node(key, ReturnLastNode=True)
            # if the key is already in the tree - change its node's value and return
            if n.key == key:
                n.value = val
                return n, steps, 0
            else:
                new_node.parent = n
            self.update_parent_child(new_node)
        else:
            self.root = new_node
        self.update_size_and_maxNode_after_insert(new_node)
        promote = self.rebalancing_after_insert(new_node)
        return new_node, steps, promote

    """rotate right the node's subtree

	@type node: AVLNode
	@param node: the root of the subtree that will be rotated
	@rtype node: AVLNode
	@returns: the root of the subtree after rotation
	"""

    def rotate_right(self, node):
        new_head = node.left
        node.left = new_head.right
        node.left.parent = node

        new_head.right = node
        new_head.parent = node.parent
        node.parent = new_head

        if new_head.parent is None:
            self.root = new_head
        else:
            if new_head.parent.key < new_head.key:
                new_head.parent.right = new_head
            else:
                new_head.parent.left = new_head

        node.update_height()
        new_head.update_height()

        return new_head

    """rotate left the node's subtree

	@type node: AVLNode
	@param node: the root of the subtree that will be rotated
	@rtype node: AVLNode
	@returns: the root of the subtree after rotation
	"""

    def rotate_left(self, node):
        new_head = node.right
        node.right = new_head.left
        node.right.parent = node

        new_head.left = node
        new_head.parent = node.parent
        node.parent = new_head

        if new_head.parent is None:
            self.root = new_head
        else:
            if new_head.parent.key < new_head.key:
                new_head.parent.right = new_head
            else:
                new_head.parent.left = new_head

        node.update_height()
        new_head.update_height()

        return new_head

    """double rotation - rotate left and then rotate right the node's subtree

	@type node: AVLNode
	@param node: the root of the subtree that will be rotated
	@rtype node: AVLNode
	@returns: the root of the subtree after double rotation
	"""

    def rotate_left_right(self, node):
        self.rotate_left(node.left)
        return self.rotate_right(node)

    """double rotation - rotate right and then rotate left the node's subtree

	@type node: AVLNode
	@param node: the root of the subtree that will be rotated
	@rtype node: AVLNode
	@returns: the root of the subtree after double rotation
	"""

    def rotate_right_left(self, node):
        self.rotate_right(node.right)
        return self.rotate_left(node)

    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""

    def delete(self, node):
        fathernode = node
        #delete root that has less than 2 kids
        if (node.key == self.root.key) and (not(node.left.is_real_node() and node.right.is_real_node())):
            # root has no kids
            if (not node.left.is_real_node()) and (not node.right.is_real_node()):
                self.root = None
                self.maxNode = None
                node.delete_pointers()
            # root has only one left child
            elif node.left.is_real_node():
                left = node.left
                self.root = left
                self.maxNode = left
                left.delete_pointers()
                node.delete_pointers()
            #root have only a right child
            else:
                self.root = node.right
                node.delete_pointers()
                self.root.delete_pointers()
            self.Size += -1
            return
        # Case 2: node has 2 children
        elif node.left.is_real_node() and node.right.is_real_node():
            succ = self.successor(node)
            fathersucc = succ.parent
            succ = self.local_delete(succ)

            #maybe handle the unreal nodes that point succ
            succ.left.parent = None
            succ.right.parent = None
            #update succ instend of node
            succ.left = node.left
            succ.right= node.right
            succ.parent = node.parent
            #handle heights of succ if succ is the son of node
            if node.key == fathersucc.key:
                fathersucc = succ
                succ.height = node.height
            else:
                succ.update_height()

            succ.left.parent = succ
            succ.right.parent = succ
            if succ.parent is not None:
                if succ.parent.left.key == node.key:
                    succ.parent.left = succ
                else:
                    succ.parent.right = succ
            else:
                self.root = succ
            node.parent = None
            node.right = AVLNode(None, None)
            node.left  = AVLNode(None, None)
            node = fathersucc
        else:
            node =self.local_delete(node , True)

        self.Size += -1
        self.delete_rebalance(node)
        return

    """
      Deletes a node from the tree. The function handles the deletion of a node
      in various scenarios:
      - If the node is a leaf (no children), it removes the node and adjusts 
        the parent’s pointers.
      - If the node has only one child (either left or right), it replaces 
        the node with its only child.

      @type node: AVLNode
      @param node: The node to be deleted.
      @type Returnfathernode: bool
      @param Returnfathernode: If `True`, the function returns the parent node 
                                of the deleted node. Otherwise, it returns the node itself.
      @rtype: AVLNode
      @returns: The parent of the deleted node (if Returnfathernode is True),
                or the updated node itself (if Returnfathernode is False).
      """
    #Assume that node has a parent.
    def local_delete(self,node, Returnfathernode = False):
        fathernode = node.parent
        # Case 0: mode is a leaf
        if node.height == 0:
            if fathernode.right.key == node.key:
                node.parent = None
                fathernode.right = AVLNode(None, None)
                fathernode.right.parent = fathernode
                if Returnfathernode:
                    #update max node
                    if node.key == self.maxNode.key:
                        self.maxNode = fathernode
                    node = fathernode

            else:
                node.parent = None
                fathernode.left = AVLNode(None, None)
                fathernode.left.parent = fathernode
                if Returnfathernode:
                    node = fathernode

        # Case 1: node has only one child
        # node has only a left child
        elif node.left.is_real_node() and (not node.right.is_real_node()):
            if node.parent.right.key == node.key:
                fathernode.right = node.left
                #update max node
                if node.key == self.maxNode.key:
                    self.maxNode = node.left
            else:
                fathernode.left = node.left
            node.left.parent = fathernode
            # clean useless pointers
            node.left = AVLNode(None, None)
            node.left.parent = node
            node.parent = None
            if Returnfathernode:
                node = fathernode
        # node has only a right child
        elif (not node.left.is_real_node()) and node.right.is_real_node():
            if node.parent.left.key == node.key:
                fathernode.left = node.right
            else:
                fathernode.right = node.right
            node.right.parent = fathernode
            # clean useless pointers
            node.right = AVLNode(None, None)
            node.right.parent = node
            node.parent = None
            if Returnfathernode:
                node = fathernode
        return node

    """
        Rebalances the AVL tree starting from the given node after a deletion.
        This function ensures that the tree maintains its balance property after
        a node has been deleted. It checks the height differences between the
        left and right subtrees at each node and applies the appropriate rotations
        to restore balance.

        @type node: AVLNode
        @param node: The node at which to start the rebalancing process.
        @rtype: None
        @returns: None
        """
    def delete_rebalance(self, node):
        fixed = False

        while not fixed and node is not None:
            diff_height_left_side = node.height - node.left.height
            diff_height_right_side = node.height - node.right.height
            # tree is fixed - finishing mode
            if (diff_height_left_side == 2 and diff_height_right_side == 1)or (
                    diff_height_left_side == 1 and diff_height_right_side == 2):
                node.update_height()
                fixed = True

            # Case 1 from class and its symmetry case.
            elif (diff_height_left_side == 2 and diff_height_right_side == 2):
                node.update_height()
                if node.parent is not None:
                    node = node.parent
                else:
                    fixed = True
            # symmetry case of case 2 & 3 & 4from class
            elif diff_height_left_side == 1 and diff_height_right_side == 3:
                left_child = node.left
                left_child_diff_height_left_side = left_child.height - left_child.left.height
                left_child_diff_height_right_side = left_child.height - left_child.right.height
                # symmetry of case 2 from class
                if left_child_diff_height_left_side == 1 and left_child_diff_height_right_side == 1:
                    self.rotate_right(node)
                    fixed = True
                # symmetry of case 3 from class
                elif left_child_diff_height_left_side == 1 and left_child_diff_height_right_side == 2:
                    node = self.rotate_right(node)
                    if node.parent is not None:
                        node = node.parent
                    else:
                        fixed = True
                # symmetry of case 4 from class
                elif left_child_diff_height_left_side == 2 and left_child_diff_height_right_side == 1:
                    node = self.rotate_left_right(node)
                    if node.parent is not None:
                        node = node.parent
                    else:
                        fixed = True
             # Case 2 & 3 & 4 from class
            elif diff_height_left_side == 3 and diff_height_right_side == 1:
                right_child = node.right
                right_child_diff_height_left_side = right_child.height - right_child.left.height
                right_child_diff_height_right_side = right_child.height - right_child.right.height
                # Case 2 from class
                if right_child_diff_height_left_side == 1 and right_child_diff_height_right_side == 1:
                    self.rotate_left(node)
                    fixed = True
                # Case 3 from class
                elif right_child_diff_height_left_side == 2 and right_child_diff_height_right_side == 1:
                    node = self.rotate_left(node)
                    if node.parent is not None:
                        node = node.parent
                    else:
                        fixed = True
                # Case 4 from class
                elif right_child_diff_height_left_side == 1 and right_child_diff_height_right_side == 2:
                    node = self.rotate_right_left(node)
                    if node.parent is not None:
                        node = node.parent
                    else:
                        fixed = True
        return

    """returns the successor node of a given node in the AVL tree

    If the node has a right child, the successor is the leftmost node in the right subtree. 
    If the node does not have a right child, the successor is one of its ancestors.

    @type node: AVLNode
    @param node: the node for which to find the successor
    @rtype: AVLNode
    @returns: the successor node, or None if the node has no successor
    """

    def successor(self, node):
        # Case 1: If the node has a right child
        if node.right.key is not None:
            node = node.right
            while node.left.key is not None:
                node = node.left
            return node

        # Case 2: If the node does not have a right child
        while node.parent is not None:
            if node.parent.left.key == node.key:
                return node.parent
            node = node.parent


        return None



    """joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separating self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""

    def join(self, tree2, key, val):
        middle_node = self.create_leaf(key, val)
        new_max_node = None
        new_size = None
        # pu middle node in self if 2 tree's roots are None
        if self.root is None and tree2.root is None:
            self.root = middle_node
            self.Size = 1
            self.maxNode = middle_node
            return
        # update new_size and new_max_node if self.root is None
        elif self.root is None:
            new_size = 1 + tree2.Size
            if middle_node.key < tree2.maxNode.key:
                new_max_node = tree2.maxNode
            else:
                new_max_node = middle_node
        # update new_size and new_max_node if tree2.root is None
        elif tree2.root is None:
            new_size = 1 + self.Size
            if middle_node.key < self.maxNode.key:
                new_max_node = self.maxNode
            else:
                new_max_node = middle_node
        # update new_size and new_max_node if self.root and tree2.root are not None
        else:
            if self.maxNode.key < tree2.maxNode.key:
                new_max_node = tree2.maxNode
            else:
                new_max_node = self.maxNode
            new_size = self.Size + 1 + tree2.Size
        node1 = self.root
        node2 = tree2.root
        union_tree = self.join_by_node(node1, middle_node, node2)
        # update self with the united tree.
        self.root = union_tree
        self.maxNode = new_max_node
        self.Size = new_size

    """joins 2 nodes with given middle node, not maintain size and maxNode fields

    @type node1: AVLNode 
    @param node1: the root of the subtree 1 for join
    @type middle_node: AVLNode 
    @param middle_node: the node that separating between node 1 and node 2 
    @type node2: AVLNode
    @param node2: the root of the subtree 2 for join
    @pre: all keys in subtree of node1 are smaller than middle_node's key and all keys in subtree of node2 are larger than key,
    or the opposite way 
    @rtype: AVLNode
	@returns: the node that is the head of the united subtrees of node1 and node2 when middle_node connects between them.
    """

    def join_by_node(self, node1, middle_node, node2):
        # if node1 and node 2 are None - return middle node
        if node1 is None and node2 is None:
            return middle_node
        # if node1 or node2 are None - put node1/node2 (the node that is not None) as a root of new tree,
        # then search in the tree the node that will be middle_node's parent and update middle_node's parent and
        # update node's left/right child to be middle_node and rebalance the tree.
        elif node1 is None or node2 is None:
            t = AVLTree()
            if node1 is None:
                node2.parent = None
                t.root = node2
            else:
                node1.parent = None
                t.root = node1
            middle_node.parent, steps = t.Search_by_node(t.root, middle_node.key, ReturnLastNode=True)
            t.update_parent_child(middle_node)
            t.rebalance_from_specific_node(middle_node.parent)
            return t.root
        # if node1 and node 2 are virtual node - return middle node
        if (not node1.is_real_node()) and (not node2.is_real_node()):
            return middle_node
        # if node1 or node2 are virtual nodes - put node1/node2 (the node that is not virtual node) as a root of new tree,
        # then search in the tree the node that will be middle_node's parent and update middle_node's parent and
        # update node's left/right child to be middle_node and rebalance the tree.
        elif not node1.is_real_node() or not node2.is_real_node():
            t = AVLTree()
            if not node1.is_real_node():
                node2.parent = None
                t.root = node2
            else:
                node1.parent = None
                t.root = node1
            middle_node.parent, steps = t.Search_by_node(t.root, middle_node.key, ReturnLastNode=True)
            t.update_parent_child(middle_node)
            t.rebalance_from_specific_node(middle_node.parent)
            return t.root
        # node 1 and node 2 are real node
        else:
            if node1.key > middle_node.key:
                tmp = node1
                node1 = node2
                node2 = tmp
            #if node1's height is smaller than node2's height so join the subtree of node1 to the tree of node2
            if node1.height < node2.height:
                h = node1.height
                t = AVLTree()
                t.root = node2
                n = t.root
                while n.height > h:
                    n = n.left
                #n is the first vertex on the left spine of t with height <= h
                middle_node.parent = n.parent
                n.parent.left = middle_node
                n.parent = middle_node
                node1.parent = middle_node
                middle_node.right = n
                middle_node.left = node1
                middle_node.update_height()
                t.rebalance_from_specific_node(middle_node.parent)
                return t.root
            #if node1's height is larger than node2's height so join the subtree of node1 to the tree of node1
            elif node1.height > node2.height:
                h = node2.height
                t = AVLTree()
                t.root = node1
                n = t.root
                while n.height > h:
                    n = n.right
                #n is the first vertex on the right spine of t1 with height <= h
                middle_node.parent = n.parent
                n.parent.right = middle_node
                n.parent = middle_node
                node2.parent = middle_node
                middle_node.left = n
                middle_node.right = node2
                middle_node.update_height()
                t.rebalance_from_specific_node(middle_node.parent)
                return t.root
            else:
                t = AVLTree()
                middle_node.left = node1
                middle_node.right = node2
                node1.parent = middle_node
                node2.parent = middle_node
                middle_node.update_height()
                t.root = middle_node
                return t.root


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
        SmallerKeys = node.left
        BiggerKeys = node.right
        isLeftBranch = self.isLeftBranch(node)
        keepFatherNode = node.parent
        # fixed pointers
        SmallerKeys.parent = None
        BiggerKeys.parent = None
        node = node.parent
        while node is not None:
            #If we have reached the father from the left branch
            if isLeftBranch:
                keepFatherNode = node.parent
                isLeftBranch = self.isLeftBranch(node)
                # clean useless pointers
                node.right.parent = None
                node.left.parent = None
                Right = node.right
                node = self.create_leaf(node.key, node.value)
                BiggerKeys.parent = None

                BiggerKeys = self.join_by_node(BiggerKeys, node, Right)
                node = keepFatherNode
            # If we have reached the father from the right branch
            else:
                keepFatherNode = node.parent
                isLeftBranch = self.isLeftBranch(node)
                # clean useless pointers
                node.right.parent = None
                node.left.parent = None
                Left = node.left
                node = self.create_leaf(node.key, node.value)
                SmallerKeys.parent = None

                SmallerKeys = self.join_by_node(SmallerKeys, node, Left)
                node = keepFatherNode
        t1 , t2  = AVLTree() , AVLTree()
        t1.root = SmallerKeys
        t1.maxNode = self.returnmaxnode(SmallerKeys)
        t2.root = BiggerKeys
        t2.maxNode = self.returnmaxnode(BiggerKeys)
        if not SmallerKeys.is_real_node():
            t1.root = None
            t1.maxNode = None
        if not BiggerKeys.is_real_node():
            t2.root = None
            t2.maxNode = None

        return t1, t2

    """
        Determines whether the given node is a left child of its parent.

        @type node: AVLNode
        @pre: node is in self
        @rtype: bool
        @returns: True if the node is the left child of its parent, False otherwise
    """

    def isLeftBranch(self,node):
        if node.parent is None:
            return False

        if node.parent.left.key == node.key:
            return True
        return False

    """
        Returns the maximum node in the subtree rooted at the given node.

        @type node: AVLNode
        @pre: node is in self
        @rtype: AVLNode or None if it isn't a real node
        @returns: the maximum node in the subtree, or None if the subtree is empty
    """

    def returnmaxnode(self,node):
        if node.key is None:
            return None

        while node.right.key is not None:
            node = node.right
        return node


    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of tuples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        lst = []
        self.rec_avl_to_array(self.root, lst)
        return lst

    """adding tuples (key, value) of every node in the tree to an empty list according to in order walking on the tree

	@type node: AVLNode
	@param node: the node in the dictionary that is the root of the subtree for rec_avl_to_array
	@type lst: list
	@param lst: An empty list to be filled with tuples (key, value) 
	"""

    def rec_avl_to_array(self, node, lst):
        if node is not None:
            if node.key is not None:
                self.rec_avl_to_array(node.left, lst)
                lst.append((node.key, node.value))
                self.rec_avl_to_array(node.right, lst)

    """returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""

    def max_node(self):
        return self.maxNode

    """returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        return self.Size

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root
