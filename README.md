# 📘 AVL Tree Implementation (Python)

## Overview
This project implements an **AVL Tree**, a self-balancing binary search tree where the height difference (balance factor) between left and right subtrees of any node is at most one.

The implementation includes:
- `AVLNode`: A class representing individual nodes.
- `AVLTree`: A class implementing the AVL Tree data structure and its operations.

The code supports:
- Standard operations: **search**, **insert**, **delete**
- Advanced operations: **finger search**, **finger insert**, **join**, **split**
- Tree traversal and conversion to array
- Balance maintenance via single and double rotations

---

## 📂 File Structure
```
AVLTree.py
├── class AVLNode
│   ├── is_real_node()
│   ├── update_height()
│   ├── delete_pointers()
│
└── class AVLTree
    ├── create_leaf()
    ├── search(), finger_search()
    ├── insert(), finger_insert()
    ├── delete(), local_delete(), delete_rebalance()
    ├── join(), join_by_node()
    ├── split()
    ├── avl_to_array(), rec_avl_to_array()
    ├── rotations: rotate_left(), rotate_right(), rotate_left_right(), rotate_right_left()
```

---

## ⚙️ Core Features

### 1. **Insertion**
- Inserts a node while maintaining the AVL property.
- Uses recursive rebalancing and rotations as needed.
- Returns a tuple `(node, steps, promotes)`:
  - `node`: the inserted node  
  - `steps`: number of search steps before insertion  
  - `promotes`: number of promote operations during rebalancing  

### 2. **Deletion**
- Handles all deletion cases:
  - Node with 0, 1, or 2 children.
- Includes `delete_rebalance()` to maintain balance after node removal.

### 3. **Search**
- `search(key)`: Regular AVL search starting from the root.
- `finger_search(key)`: Optimized search starting near the maximum node for faster average lookup.

### 4. **Join and Split**
- **Join**: Merges two AVL trees into one, using a separating key.
- **Split**: Splits an AVL tree into two balanced subtrees around a given node.

### 5. **Rotations**
Maintains balance through:
- **Single Rotations**: `rotate_left()`, `rotate_right()`
- **Double Rotations**: `rotate_left_right()`, `rotate_right_left()`

---

## 🧪 Example Usage

```python
from AVLTree import AVLTree

# Create a new tree
tree = AVLTree()

# Insert values
tree.insert(10, "A")
tree.insert(20, "B")
tree.insert(5, "C")

# Search for a key
node, steps = tree.search(20)
print(node.value)  # Output: "B"

# Delete a key
tree.delete(node)

# Convert tree to sorted array
print(tree.avl_to_array())  # [(5, 'C'), (10, 'A')]
```

---

## 📈 Complexity
| Operation | Time Complexity | Notes |
|------------|-----------------|-------|
| Insertion  | O(log n) | Includes rebalancing |
| Deletion   | O(log n) | Includes rebalancing |
| Search     | O(log n) | Binary search traversal |
| Join/Split | O(log n) | Depends on height difference |

---

## 🧩 Design Notes
- Each node maintains:
  - `key`, `value`
  - `left`, `right`, and `parent` pointers
  - `height`
- Virtual nodes (`key=None, value=None`) are used to simplify balancing logic.
- Tree metadata:
  - `root`: pointer to the tree root
  - `maxNode`: pointer to the node with the maximal key
  - `Size`: total number of nodes

---

## 🧠 Authors
- **Gad Rozen**  
- **Hila Etziony**

---

## 📜 License
This project is intended for **academic and educational use** only.  
Please include proper attribution if reused.
