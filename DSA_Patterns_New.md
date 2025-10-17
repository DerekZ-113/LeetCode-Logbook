# DSA Interview Patterns - Consolidated Edition

## Philosophy

This guide consolidates common patterns into their universal forms. Each pattern has ONE core template that adapts to different scenarios, rather than multiple "templates" that are really just applications of the same idea.

**Key principle**: A template is a reusable structure. An application shows that structure used in a specific context.

---

## Pattern 1: DFS (Depth-First Search)

### When to Use

DFS is your tool when you need to:
- Explore all paths or possibilities exhaustively
- Find connected components in graphs or grids
- Detect cycles
- Generate combinations, permutations, or all valid solutions
- Search for a path with specific properties
- Any problem requiring "find all..." or "explore all..."

**Applies to**: Trees, graphs (adjacency list/matrix), grids, backtracking problems (combinations/permutations/puzzles)

### The Universal Template

```python
def dfs(current_state, [optional_params]):
    """
    Universal DFS - Works for ALL DFS problems
    Only 3 things change based on problem:
    1. How you mark visited (Step 1)
    2. How you find neighbors (Step 3)  
    3. Whether you need cleanup (Step 4)
    """
    
    # STEP 1: Mark visited (ALWAYS FIRST)
    mark_visited(current_state)
    
    # STEP 2: Process current node (if needed)
    result = process_current(current_state)
    
    # STEP 3: Explore neighbors
    for neighbor in get_neighbors(current_state):
        if is_valid(neighbor):
            result = combine(result, dfs(neighbor, [updated_params]))
    
    # STEP 4: Backtrack/cleanup (only if needed)
    restore_state_if_needed(current_state)
    
    return result  # Only if accumulating
```

### Adaptation Guide

The 4 steps stay the same. Here's what changes:

#### Step 1: Marking Visited

| Data Structure | How to Mark |
|----------------|-------------|
| **Grid** | `grid[r][c] = VISITED_MARKER` |
| **Graph (adjacency list)** | `visited.add(node)` |
| **Graph (adjacency matrix)** | `visited.add(node)` |
| **Tree** | Skip (no cycles) |
| **Backtracking** | `path.append(choice)` |

#### Step 3: Finding Neighbors

| Data Structure | How to Get Neighbors |
|----------------|---------------------|
| **Grid** | `for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]` |
| **Adjacency List** | `for neighbor in graph[node]` |
| **Adjacency Matrix** | `for j in range(n): if matrix[node][j] == 1` |
| **Tree** | `dfs(node.left)` and `dfs(node.right)` |
| **Backtracking** | `for choice in available_choices` |

#### Step 4: Backtracking (Cleanup)

**Need it when**: Multiple paths share state (backtracking problems, path tracking)
**Don't need it when**: Just exploring/marking (most graph/grid traversals)

```python
# Backtracking - need cleanup
path.append(choice)
dfs(next_state)
path.pop()  # MUST restore state

# Graph traversal - no cleanup needed
visited.add(node)
dfs(neighbor)
# visited stays marked
```

### Code Examples

**Simple Grid Traversal:**
```python
def dfs(r, c):
    grid[r][c] = '-1'  # Step 1: Mark
    count = 1          # Step 2: Process
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:  # Step 3: Neighbors
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
            count += dfs(nr, nc)
    return count  # No Step 4 needed
```

**Backtracking (needs cleanup):**
```python
def backtrack(start, path):
    result.append(path[:])  # Step 2: Process
    for i in range(start, len(nums)):  # Step 3: Choices
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()  # Step 4: MUST cleanup!
```

### Common Mistakes

1. **Not marking visited at the START of DFS** - leads to infinite loops or double counting
2. **Forgetting to backtrack in path problems** - `path.pop()` after recursion
3. **Checking bounds AFTER calling DFS** - check before calling, not inside
4. **Using list instead of set for visited** - O(n) lookups vs O(1)
5. **Not copying when saving results** - `result.append(path)` vs `result.append(path[:])`
6. **Confused about grid marking** - `grid[r][c] = visited` vs maintaining separate visited set
7. **Matrix iteration error** - forgetting to iterate through indices for adjacency matrix

### Key Tips

- **Step 1 is non-negotiable**: Mark visited before anything else
- **Step 2 is optional**: Not all problems need processing
- **Step 3 syntax changes**: But structure stays identical
- **Step 4 rarely needed**: Only backtracking problems require cleanup
- **For grids**: Usually mark in-place, rarely need separate visited set
- **For graphs**: Always need visited set (unless it's a tree)
- **For backtracking**: ALWAYS need Step 4 (cleanup/undo)
- **Mental model**: "What do I do with THIS node? Then what do I do with its NEIGHBORS?"

### Time & Space Complexity

- **Time**: O(V + E) for graphs, O(N) for trees, O(2^N) or O(N!) for backtracking
- **Space**: O(H) for recursion depth where H is height/depth; O(V) for visited set

---

## Pattern 2: Topological Sort

### When to Use

Topological Sort is your tool when you need to:
- Order tasks with dependencies/prerequisites
- Course scheduling problems
- Build order/compilation order
- Process nodes with no incoming edges first
- Detect cycles in directed graphs
- Find if valid ordering exists

**Key indicator**: Problem mentions "prerequisites", "dependencies", "order", or directed acyclic graph (DAG)

### The Two Core Approaches

There are only 2 ways to do topological sort. Pick based on preference and cycle detection needs.

#### Approach 1: Kahn's Algorithm (BFS with In-Degree)

```python
def topological_sort_bfs(numNodes, edges):
    from collections import deque, defaultdict
    
    # Build graph and calculate in-degrees
    graph = defaultdict(list)
    in_degree = [0] * numNodes
    
    for prereq, course in edges:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Queue nodes with no prerequisites
    queue = deque([i for i in range(numNodes) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        # Reduce in-degree for neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycle
    if len(result) == numNodes:
        return result  # Valid topological order
    else:
        return []  # Cycle detected
```

**When to use**: 
- Default choice - simpler and more intuitive
- Cycle detection is natural (check if all nodes processed)
- Need to track levels/parallel processing

#### Approach 2: DFS with State Tracking

```python
def topological_sort_dfs(numNodes, edges):
    from collections import defaultdict
    
    graph = defaultdict(list)
    for prereq, course in edges:
        graph[prereq].append(course)
    
    # States: 0=unvisited, 1=visiting, 2=visited
    state = [0] * numNodes
    result = []
    has_cycle = False
    
    def dfs(node):
        nonlocal has_cycle
        if state[node] == 1:  # Found cycle
            has_cycle = True
            return
        if state[node] == 2:  # Already processed
            return
        
        state[node] = 1  # Mark as visiting
        
        for neighbor in graph[node]:
            dfs(neighbor)
            if has_cycle:
                return
        
        state[node] = 2  # Mark as visited
        result.append(node)  # Add in reverse order
    
    for i in range(numNodes):
        if state[i] == 0:
            dfs(i)
            if has_cycle:
                return []
    
    return result[::-1]  # Reverse for correct order
```

**When to use**:
- Need to explore full paths
- Comfortable with recursion
- Want to collect additional path information

### Key Differences

| Aspect | Kahn's (BFS) | DFS |
|--------|--------------|-----|
| **Implementation** | Iterative, queue-based | Recursive |
| **Cycle Detection** | Natural (count != n) | Need state tracking |
| **Order** | Build directly | Build reversed, flip at end |
| **Intuition** | "Process nodes with no deps first" | "Go deep, add on way back" |
| **Preference** | Usually easier | If you prefer recursion |

### Code Examples

**Kahn's minimal:**
```python
queue = deque([i for i in range(n) if in_degree[i] == 0])
result = []
while queue:
    node = queue.popleft()
    result.append(node)
    for neighbor in graph[node]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)
return result if len(result) == n else []
```

**DFS minimal:**
```python
def dfs(node):
    if state[node] == 1: return True  # Cycle
    if state[node] == 2: return False
    state[node] = 1
    for nei in graph[node]:
        if dfs(nei): return True
    state[node] = 2
    result.append(node)
    return False
```

### Common Mistakes

1. **Not initializing in-degree correctly** - missing nodes with 0 in-degree
2. **Wrong cycle detection in DFS** - not using 3 states (0/1/2)
3. **Forgetting to reverse DFS result** - DFS builds backward
4. **Off-by-one with indexing** - 0-indexed vs 1-indexed nodes
5. **Not handling disconnected components** - loop through all nodes
6. **Processing prerequisites backward** - edge direction matters

### Key Tips

- **Default to Kahn's** - usually cleaner for interviews
- **In-degree = 0 means ready** - no dependencies left
- **DFS state 1 = currently exploring** - seeing it again = cycle
- **For lexicographic order** - use min-heap instead of queue
- **Track levels** - process queue layer by layer for parallel tasks
- **Result length check** - if != n, there's a cycle

### Time & Space Complexity

- **Time**: O(V + E) for both approaches
- **Space**: O(V + E) for graph + O(V) for queue/recursion

---

## Pattern 3: Trie (Prefix Tree)

### When to Use

Trie is your tool when you need to:
- Prefix matching or searching
- Autocomplete/word suggestions
- Word validation (dictionary)
- Finding all words with common prefix
- Word search in grid/board
- Spell checker
- Problems with many string lookups with shared prefixes

**Key indicator**: Multiple string operations with common prefixes, or "starts with" queries

### The Core Structures

#### Structure 1: Basic Trie

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # or [None] * 26 for lowercase only
        self.is_end = False
        # Optional: self.word = None  # Store complete word

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

**Variations:**
- Add `self.count = 0` to track prefix frequency
- Add `self.word = word` at end to store complete word (useful for board search)
- Use array `[None] * 26` for lowercase-only (faster but less flexible)

#### Structure 2: Wildcard Trie (DFS Search)

For patterns with '.' wildcard matching any character:

```python
def search_with_wildcard(word):
    def dfs(node, i):
        if i == len(word):
            return node.is_end
        
        char = word[i]
        if char == '.':
            # Try all possible children
            for child in node.children.values():
                if dfs(child, i + 1):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return dfs(node.children[char], i + 1)
    
    return dfs(self.root, 0)
```

**Key insight**: Wildcard search is just DFS through the trie with branching at '.'

### Adaptation Guide

**Basic Trie → Word Search in Board:**
- Build trie from word list
- DFS through board, pruning with trie
- Store complete word at leaf nodes

**Basic Trie → Autocomplete:**
- Add frequency counter to nodes
- DFS from prefix node to collect all words
- Sort by frequency

**Basic Trie → Replace Words:**
- Insert all roots into trie
- For each word, traverse until `is_end = True`
- Return prefix or original word

### Code Examples

**Minimal basic operations:**
```python
# Insert
node = root
for c in word:
    if c not in node.children:
        node.children[c] = TrieNode()
    node = node.children[c]
node.is_end = True

# Search
node = root
for c in word:
    if c not in node.children:
        return False
    node = node.children[c]
return node.is_end
```

**Minimal wildcard:**
```python
def dfs(node, i):
    if i == len(word):
        return node.is_end
    if word[i] == '.':
        return any(dfs(child, i+1) for child in node.children.values())
    return word[i] in node.children and dfs(node.children[word[i]], i+1)
```

### Common Mistakes

1. **Not marking word endings** - `is_end = False` for all nodes by default
2. **Dict vs Array confusion** - dict for any chars, array[26] only for lowercase
3. **Not pruning in board search** - remove branches with no words
4. **Forgetting to restore board** - backtracking in word search
5. **Wrong bit order in Bit Trie** - process MSB to LSB (31 to 0)
6. **Not handling empty string** - edge case in search

### Key Tips

- **Dict vs Array**: Use dict `{}` for sparse/any characters, array `[None]*26` for lowercase only
- **Store word at end**: Avoids rebuilding in word search problems
- **Prune aggressively**: Delete empty branches to save space
- **DFS for wildcards**: Branch at '.' to try all children
- **Memory optimization**: Can store only end nodes if just checking existence

### Time & Space Complexity

**Basic Operations:**
- **Insert/Search**: O(m) where m is word length
- **Space**: O(ALPHABET_SIZE × N × M) worst case; O(total chars) typical

**Word Search in Board:**
- **Time**: O(rows × cols × 4^L) where L is max word length
- **Space**: O(N × M) for trie where N is words, M is avg length

---

## Pattern 4: Two Pointers

### When to Use

Two Pointers is your tool when you need to:
- Array is sorted and need to find pairs/triplets
- In-place operations requiring O(1) space
- Comparing elements from different positions
- Finding cycles in linked lists
- Partitioning arrays based on condition
- String/array palindrome problems

**Key indicator**: Sorted array, in-place modification, or cycle detection

### The Three Core Patterns

#### Pattern 1: Opposite Direction (Converging)

Pointers start at opposite ends and move toward each other.

```python
def opposite_direction(arr):
    left, right = 0, len(arr) - 1
    result = 0
    
    while left < right:
        current = arr[left] + arr[right]
        
        if condition_met(current):
            # Process and move both
            result = update_result(result, current)
            left += 1
            right -= 1
        elif need_larger:
            left += 1
        else:  # need_smaller
            right -= 1
    
    return result
```

**When to use:**
- Sorted array problems
- Finding pairs with target sum
- Container/area problems
- Palindrome checking

**3Sum/4Sum Note:** These are just opposite direction with an outer loop fixing one element. Not a separate pattern.

#### Pattern 2: Same Direction (Slow/Fast & Sliding Window)

Both pointers move forward. Two main variants:

**Variant A: Variable Window (Slow/Fast)**
```python
def same_direction(arr):
    slow = 0
    
    for fast in range(len(arr)):
        if condition_met(arr[fast]):
            arr[slow], arr[fast] = arr[fast], arr[slow]
            slow += 1
    
    return slow  # Often returns new length
```

**When to use:**
- Removing elements in-place
- Partitioning array
- Processing valid elements only

**Variant B: Fixed Window**
```python
def fixed_window(arr, k):
    # Initialize window sum/result
    window_sum = sum(arr[:k])
    result = window_sum
    
    for right in range(k, len(arr)):
        # Add new element, remove leftmost
        window_sum += arr[right] - arr[right - k]
        result = max(result, window_sum)
    
    return result
```

**When to use:**
- Maximum/minimum in window of size k
- Average of k consecutive elements
- Any calculation over fixed-size subarray

#### Pattern 3: Fast & Slow (Cycle Detection)

Fast pointer moves 2x speed of slow pointer.

```python
def has_cycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False

def find_cycle_start(head):
    # Find meeting point first
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    
    if not fast or not fast.next:
        return None
    
    # Find start: reset slow to head, move both 1 step
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow
```

**When to use:**
- Linked list cycle detection
- Finding cycle start
- Finding middle of linked list
- Happy Number problems

### Code Examples

**Opposite direction (Two Sum II):**
```python
left, right = 0, len(arr) - 1
while left < right:
    total = arr[left] + arr[right]
    if total == target:
        return [left, right]
    elif total < target:
        left += 1
    else:
        right -= 1
```

**Same direction (Remove Duplicates):**
```python
slow = 0
for fast in range(len(arr)):
    if arr[fast] != arr[slow]:
        slow += 1
        arr[slow] = arr[fast]
return slow + 1
```

**Fast & Slow (Find Middle):**
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow  # slow is at middle
```

### Common Mistakes

1. **Wrong loop condition** - `<` vs `<=`, causes off-by-one or infinite loop
2. **Not handling duplicates in 3Sum** - skip same elements: `if i > 0 and nums[i] == nums[i-1]: continue`
3. **Moving both pointers incorrectly** - sometimes only one should move
4. **Fast & Slow initialization** - start both at head, not head and head.next
5. **Not checking fast.next before fast.next.next** - causes null pointer error
6. **Forgetting edge cases** - empty array, single element, all duplicates

### Key Tips

- **For sorted arrays** - opposite direction is usually the answer
- **For in-place operations** - same direction (slow/fast)
- **For cycles** - fast & slow with 2x speed
- **Skip duplicates in 3Sum**: Check `i > start` before skipping
- **Opposite direction intuition**: Move pointer that's "wrong direction" from target
- **Fast & Slow always works**: Even if no cycle, fast will reach end
- **Finding cycle start**: Reset one pointer to head after detection, move both 1 step

### Time & Space Complexity

**All patterns:**
- **Time**: O(n) for single pass; O(n²) for 3Sum (n iterations × n two-pointer)
- **Space**: O(1) - in-place operations

---

## Pattern 5: BFS (Breadth-First Search)

### When to Use

BFS is your tool when you need to:
- Find shortest path in unweighted graph/grid
- Explore nodes level by level
- Process by layers/rounds/generations
- Find minimum steps/moves
- Explore neighbors before going deeper
- Need to track which level/round you're on

**Key indicator**: "Shortest", "minimum", "level-order", or need to process layer by layer

### The Two Core Patterns

The only real difference: do you need to track which level/round you're on?

#### Pattern 1: Standard BFS (No Level Tracking)

Just process nodes in order. Use for shortest path, existence checks, exploration.

```python
from collections import deque

def bfs_standard(start):
    queue = deque([start])
    visited = {start}
    
    while queue:
        node = queue.popleft()
        
        # Process current node
        if is_target(node):
            return True
        
        for neighbor in get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return False
```

**When to use:**
- Shortest path counting
- Checking if target reachable
- Graph/grid exploration
- Don't care which level/round

**Tracking distance:** Add distance to queue: `queue.append((neighbor, dist + 1))`

#### Pattern 2: Level-Order BFS (With Level Tracking)

Process layer by layer using `level_size = len(queue)` loop.

```python
from collections import deque

def bfs_level_order(start):
    queue = deque([start])
    visited = {start}
    level = 0
    
    while queue:
        level_size = len(queue)  # Process entire level
        
        for _ in range(level_size):
            node = queue.popleft()
            
            # Process node at this level
            process(node, level)
            
            for neighbor in get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        level += 1
    
    return level
```

**When to use:**
- Tree level-order traversal
- Minimum rounds/generations/steps
- Need to process entire level together
- Parallel processing simulation

#### Bit Mask for Matching
```python
# ========================================
# BITMASK OPERATIONS CHEAT SHEET
# ========================================

# OPERATION 1: Set a bit (collect/mark item)
# "I just picked up item at position X"
mask |= (1 << position)

# OPERATION 2: Check if bit is set (do I have item?)
# "Do I have the item at position X?"
if mask & (1 << position):
    # Yes, you have it
else:
    # No, you don't have it

# OPERATION 3: Check if all bits set (have everything?)
# "Do I have all N items?"
all_items_mask = (1 << total_count) - 1
if mask == all_items_mask:
    # You have everything!
```

### Adaptations

**Multi-Source BFS:**
Just initialize queue with all sources instead of one:
```python
queue = deque()
for source in sources:
    queue.append(source)
    visited.add(source)
```

**Complex State (tuples in queue):**
Store more info: `(node, keys_collected, steps)`, `(r, c, distance)`, etc.
```python
queue = deque([(start, 0, set())])  # (node, dist, keys)
visited = {(start, frozenset())}    # Must match state
```

**Grid BFS:**
Nodes are `(row, col)`, neighbors are 4 directions:
```python
for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != blocked:
        # Add to queue
```

### Code Examples

**Standard BFS (shortest path):**
```python
queue = deque([(start, 0)])
visited = {start}
while queue:
    node, dist = queue.popleft()
    if node == target:
        return dist
    for nei in graph[node]:
        if nei not in visited:
            visited.add(nei)
            queue.append((nei, dist + 1))
```

**Level-Order BFS (tree levels):**
```python
queue = deque([root])
result = []
while queue:
    level = []
    for _ in range(len(queue)):
        node = queue.popleft()
        level.append(node.val)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
    result.append(level)
```

### Common Mistakes

1. **Marking visited after popping** - mark when adding to queue to avoid duplicates
2. **Using list instead of deque** - `list.pop(0)` is O(n), `deque.popleft()` is O(1)
3. **Not tracking visited** - infinite loops in graphs with cycles
4. **Wrong level tracking** - must use `level_size = len(queue)` before inner loop
5. **Complex state without proper visited** - must track full state, not just node
6. **Grid bounds checking** - check before adding to queue, not after popping

### Key Tips

- **Always mark visited when adding to queue**, not when popping
- **Use deque**, never list for BFS queue
- **Level tracking**: `level_size = len(queue)` then `for _ in range(level_size)`
- **Multi-source**: Just add all sources to queue initially
- **Complex state**: Use tuples and match visited set structure
- **For grids**: Treat `(r, c)` as node, 4 directions as neighbors
- **Shortest path**: BFS guarantees shortest in unweighted graphs

### Time & Space Complexity

- **Time**: O(V + E) for graphs; O(rows × cols) for grids
- **Space**: O(V) for visited set and queue

---

## Pattern 6: Binary Search

### When to Use

Binary Search is your tool when you need to:
- Array is sorted (or rotated sorted)
- Finding target value or insertion point
- Finding boundary conditions
- Optimization problems (minimize/maximize with verification)
- Answer exists in a range and you can check validity
- Need O(log n) time complexity

**Key indicator**: Sorted data, "find target", "first/last position", or can verify if value works

### The Three Core Templates

#### Template 1: Classic Binary Search (Exact Match)

Standard binary search to find exact target.

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found
```

**When to use:**
- Find if target exists
- Get index of target
- Simple existence check

**Key points:**
- Use `left <= right` (inclusive)
- Use `left + (right - left) // 2` to avoid overflow
- Return -1 if not found

#### Template 2: Find Boundary (Leftmost/Rightmost)

Find the boundary position. Only ONE character difference between left and right.

```python
def find_leftmost(nums, target):
    """Find first occurrence (insertion point if not exists)"""
    left, right = 0, len(nums)  # Note: right = len(nums), not len(nums)-1
    
    while left < right:  # Note: <, not <=
        mid = left + (right - left) // 2
        
        if nums[mid] < target:  # ← Key difference
            left = mid + 1
        else:
            right = mid
    
    return left

def find_rightmost(nums, target):
    """Find last occurrence + 1 (one past last valid position)"""
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] <= target:  # ← Only difference: <= instead of <
            left = mid + 1
        else:
            right = mid
    
    return left - 1  # Subtract 1 for actual last position
```

**When to use:**
- Find first/last occurrence
- Find insertion position
- Find range of target values
- Problems asking for "first position where..."

**Key points:**
- Use `right = len(nums)` (exclusive upper bound)
- Use `left < right` (not `<=`)
- Never use `mid - 1` or `mid + 1` for `right`
- Leftmost: `nums[mid] < target`
- Rightmost: `nums[mid] <= target` (just add `=`)

**Python shortcut:** Use `bisect.bisect_left()` and `bisect.bisect_right()`

#### Template 3: Binary Search on Answer

Search the "answer space" rather than the array. Different paradigm.

```python
def binary_search_answer(arr, condition):
    """Find minimum/maximum value that satisfies condition"""
    def is_valid(mid):
        # Check if mid value works
        # Often involves iterating through arr
        return True/False
    
    left, right = min_possible, max_possible
    
    while left < right:
        mid = left + (right - left) // 2
        
        if is_valid(mid):
            right = mid  # Can we do better (smaller)?
        else:
            left = mid + 1  # Need larger value
    
    return left
```

**When to use:**
- "Minimize maximum" or "maximize minimum"
- Can verify if answer X works
- Koko eating bananas, split array, capacity problems
- Optimization with verification function

**Key points:**
- Not searching array, searching answer range
- Need `is_valid()` function to check if value works
- Decide if looking for min or max, adjust logic accordingly
- Think: "Can I do it with X capacity/speed/value?"

### Code Examples

**Classic (exact match):**
```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = left + (right - left) // 2
    if nums[mid] == target: return mid
    elif nums[mid] < target: left = mid + 1
    else: right = mid - 1
return -1
```

**Boundary (find first position):**
```python
left, right = 0, len(nums)
while left < right:
    mid = left + (right - left) // 2
    if nums[mid] < target:
        left = mid + 1
    else:
        right = mid
return left
```

**Search on answer (Koko bananas):**
```python
def can_eat_all(speed):
    hours = sum((pile + speed - 1) // speed for pile in piles)
    return hours <= h

left, right = 1, max(piles)
while left < right:
    mid = left + (right - left) // 2
    if can_eat_all(mid):
        right = mid  # Try slower
    else:
        left = mid + 1  # Need faster
return left
```

### Common Mistakes

1. **Integer overflow** - use `left + (right - left) // 2`, not `(left + right) // 2`
2. **Wrong loop condition** - classic uses `<=`, boundary uses `<`
3. **Wrong initial right** - classic uses `len(nums) - 1`, boundary uses `len(nums)`
4. **Off-by-one errors** - carefully decide when to use `mid`, `mid + 1`, `mid - 1`
5. **Infinite loop** - usually from wrong `left`/`right` updates
6. **Not handling edge cases** - empty array, single element, target not in array
7. **Confusing leftmost/rightmost** - only difference is `<` vs `<=`

### Key Tips

- **Classic search**: `left <= right`, `right = len(nums) - 1`
- **Boundary search**: `left < right`, `right = len(nums)` (exclusive)
- **Leftmost vs rightmost**: One comparison operator difference (`<` vs `<=`)
- **Answer space search**: Think "what range am I searching?" not "what array?"
- **Always use `left + (right - left) // 2`** - prevents overflow
- **Draw it out**: Visualize the search space shrinking
- **Use bisect module**: When you just need leftmost/rightmost position

### Time & Space Complexity

- **Time**: O(log n) for all binary search variants
- **Space**: O(1) - iterative implementation

---

## Pattern 7: Monotonic Stack & Queue

### When to Use

**Monotonic Stack** - use when you need to:
- Find next/previous greater/smaller element
- Problems asking for nearest larger/smaller values
- Stock span, temperature problems
- Histogram/rectangle problems
- Building visibility problems

**Monotonic Queue** - use when you need to:
- Sliding window maximum/minimum
- Track max/min in dynamic window
- Subarray problems with min/max constraints

**Key indicator**: "Next greater", "previous smaller", "sliding window max/min"

### The Two Core Patterns

#### Pattern 1: Monotonic Stack

One template - just change the comparison based on what you're looking for.

```python
def monotonic_stack(nums):
    n = len(nums)
    result = [-1] * n  # Or whatever default
    stack = []  # Stack of indices
    
    for i in range(n):
        # Pop based on what you're finding
        while stack and should_pop(nums[stack[-1]], nums[i]):
            index = stack.pop()
            result[index] = nums[i]  # Or i, depending on problem
        
        stack.append(i)
    
    return result
```

**The key decision: When to pop?**

| What you're finding | Stack type | Pop condition |
|---------------------|------------|---------------|
| **Next Greater** | Decreasing | `nums[stack[-1]] < nums[i]` |
| **Next Smaller** | Increasing | `nums[stack[-1]] > nums[i]` |
| **Previous Greater** | Decreasing | Same, iterate backwards |
| **Previous Smaller** | Increasing | Same, iterate backwards |

**Mental model:**
- Finding **greater**? Keep stack **decreasing** (pop smaller)
- Finding **smaller**? Keep stack **increasing** (pop larger)

**Always store indices, not values** - gives you both position and value.

#### Pattern 2: Monotonic Queue (Deque)

For sliding window max/min problems.

```python
from collections import deque

def sliding_window_max(nums, k):
    dq = deque()  # Monotonic decreasing (indices)
    result = []
    
    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Maintain monotonic property
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result after first window
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

**For sliding window min:** Change comparison to `nums[dq[-1]] > nums[i]`

**Key differences from stack:**
- Use deque (need to remove from both ends)
- Remove out-of-window elements from front
- Remove violated monotonic elements from back
- Front always has the max/min

### Code Examples

**Next Greater Element:**
```python
stack = []
result = [-1] * n
for i in range(n):
    while stack and nums[stack[-1]] < nums[i]:
        result[stack.pop()] = nums[i]
    stack.append(i)
```

**Previous Smaller Element:**
```python
stack = []
result = [-1] * n
for i in range(n):
    while stack and nums[stack[-1]] >= nums[i]:
        stack.pop()
    if stack:
        result[i] = nums[stack[-1]]
    stack.append(i)
```

**Sliding Window Max:**
```python
dq = deque()
for i in range(len(nums)):
    while dq and dq[0] <= i - k:
        dq.popleft()
    while dq and nums[dq[-1]] < nums[i]:
        dq.pop()
    dq.append(i)
    if i >= k - 1:
        result.append(nums[dq[0]])
```

### Common Mistakes

1. **Wrong monotonic direction** - greater needs decreasing stack, smaller needs increasing
2. **Not handling equal elements** - decide if `<` or `<=`, affects duplicates
3. **Storing values instead of indices** - always store indices for flexibility
4. **Forgetting to process remaining stack** - after loop, remaining elements have no answer
5. **Queue: not removing out-of-window** - must check `dq[0] <= i - k`
6. **Queue: wrong comparison** - max needs decreasing (`<`), min needs increasing (`>`)

### Key Tips

- **Stack: Store indices** - access both position and value
- **Stack direction**: Greater → decreasing, Smaller → increasing
- **Queue: Two while loops** - one for window, one for monotonic property
- **Queue front = answer** - max/min is always at `dq[0]`
- **Equal elements**: Decide `<` vs `<=` based on if you want "next strictly greater" or not
- **Applications**: Histogram = prev/next smaller, Stock span = next greater

### Time & Space Complexity

- **Time**: O(n) - each element pushed/popped once
- **Space**: O(n) worst case for stack/queue

---

## Pattern 8: Heap (Priority Queue)

### When to Use

Heap is your tool when you need to:
- Find K largest/smallest elements
- Merge K sorted arrays/lists
- Find median from stream
- Track running min/max efficiently
- Priority-based processing (tasks, meetings, scheduling)
- Repeated min/max operations

**Key indicator**: "K largest/smallest", "merge K sorted", "median", "priority", frequent min/max queries

### The Three Core Patterns

#### Pattern 1: Top K Elements

Maintain heap of size K to track K largest or smallest elements.

```python
import heapq

def top_k_largest(nums, k):
    """Use min heap of size k for k largest"""
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap

def top_k_smallest(nums, k):
    """Use max heap (negate values) of size k for k smallest"""
    heap = []
    
    for num in nums:
        heapq.heappush(heap, -num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [-x for x in heap]
```

**When to use:**
- K most/least frequent elements
- K closest points
- Kth largest/smallest element
- Any "top K" problem

**Key insight:**
- **K largest** → use **min heap** (kick out smallest)
- **K smallest** → use **max heap** (negate values, kick out largest)

**Python shortcut:** `heapq.nlargest(k, nums)` or `heapq.nsmallest(k, nums)`

#### Pattern 2: Merge K Sorted

Merge multiple sorted lists/arrays using heap.

```python
def merge_k_sorted(lists):
    """Merge k sorted arrays/lists"""
    heap = []
    result = []
    
    # Add first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))  # (value, list_idx, element_idx)
    
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # Add next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result
```

**When to use:**
- Merge K sorted lists/arrays
- Kth smallest in sorted matrix
- Smallest range covering elements from K lists

**Key points:**
- Heap stores `(value, source_index, element_index)`
- Always add next element from same source after popping

#### Pattern 3: Two-Heap (Median Finder)

Use max heap (left half) and min heap (right half) to track median.

```python
class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (negate values) - left half
        self.large = []  # Min heap - right half
    
    def addNum(self, num):
        # Add to max heap (left half)
        heapq.heappush(self.small, -num)
        
        # Balance: largest of small must be ≤ smallest of large
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Size balance: small can have at most 1 more element
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

**When to use:**
- Find median from data stream
- Sliding window median
- Any problem tracking middle value dynamically

**Key insight:**
- Left heap (max) has smaller half
- Right heap (min) has larger half
- Median is top of larger heap or average of both tops

### Code Examples

**Top K frequent:**
```python
from collections import Counter
count = Counter(nums)
return [num for num, _ in heapq.nlargest(k, count.items(), key=lambda x: x[1])]
```

**Merge K lists (linked lists):**
```python
heap = []
for i, lst in enumerate(lists):
    if lst:
        heapq.heappush(heap, (lst.val, i, lst))

while heap:
    val, i, node = heapq.heappop(heap)
    result.append(node)
    if node.next:
        heapq.heappush(heap, (node.next.val, i, node.next))
```

### Common Mistakes

1. **Python has min heap only** - negate values for max heap
2. **Not maintaining heap size K** - must pop when `len(heap) > k`
3. **Wrong heap for top K** - largest needs min heap, smallest needs max heap
4. **Tuple comparison issues** - add index as tiebreaker: `(priority, index, item)`
5. **Two-heap imbalance** - keep sizes balanced (differ by at most 1)
6. **Not checking empty heaps** - always verify heap not empty before accessing top

### Key Tips

- **Python only has min heap** - negate for max heap or use `heapq.nlargest/nsmallest`
- **Top K largest = min heap** - counterintuitive but correct
- **Use tuples for priority** - `(priority, tiebreaker, data)`
- **Merge K: track source** - store which list element came from
- **Two heaps: left ≥ right size** - small can have 1 extra element max
- **heappushpop/heapreplace** - more efficient than separate push+pop

### Time & Space Complexity

**Top K:**
- **Time**: O(n log k) - n operations on heap of size k
- **Space**: O(k)

**Merge K:**
- **Time**: O(n log k) - n total elements, heap of size k
- **Space**: O(k) for heap

**Median Finder:**
- **Time**: O(log n) per operation
- **Space**: O(n) for storing all elements

---

## Pattern 9: Union-Find (Disjoint Set)

### When to Use

Union-Find is your tool when you need to:
- Track connected components dynamically
- Detect cycles in undirected graphs
- Merge groups/sets efficiently
- Check if two elements are in same group
- Count number of separate groups
- Friend circles, network connectivity
- Minimum spanning tree (Kruskal's)

**Key indicator**: "Connected components", "group/merge", "same set", dynamic connectivity

### The Core Structure

Only two operations: `find` (what group?) and `union` (merge groups).

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # Each node is its own parent initially
        self.rank = [0] * n           # Tree height for balancing
        self.count = n                # Number of separate groups
        # Optional: self.size = [1] * n  # Size of each component
    
    def find(self, x):
        """Find root/representative of x's group (with path compression)"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        """Merge groups containing x and y (with union by rank)"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same group
        
        # Union by rank - attach smaller tree under larger
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            # Optional: self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            # Optional: self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            # Optional: self.size[root_x] += self.size[root_y]
        
        self.count -= 1  # One less separate group
        return True  # Successfully merged
    
    def is_connected(self, x, y):
        """Check if x and y are in same group"""
        return self.find(x) == self.find(y)
    
    def get_count(self):
        """Return number of separate groups"""
        return self.count
```

**The optimizations (critical for O(α(n)) ≈ O(1)):**
1. **Path compression** in `find`: Make all nodes point directly to root
2. **Union by rank** in `union`: Attach shorter tree under taller tree

**Without these:** Operations become O(n). **With these:** Operations become O(α(n)) ≈ O(1) amortized.

### Common Applications

**Cycle Detection:**
```python
uf = UnionFind(n)
for u, v in edges:
    if not uf.union(u, v):
        return True  # Edge creates cycle
return False
```

**Connected Components:**
```python
uf = UnionFind(n)
for u, v in edges:
    uf.union(u, v)
return uf.get_count()  # Number of components
```

**Grid Union-Find (for islands):**
```python
def index(r, c):
    return r * cols + c

uf = UnionFind(rows * cols)
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':
            for dr, dc in [(0,1), (1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    uf.union(index(r, c), index(nr, nc))
```

### Code Examples

**Basic usage:**
```python
uf = UnionFind(5)  # 5 elements: 0,1,2,3,4

uf.union(0, 1)  # Merge 0 and 1
uf.union(2, 3)  # Merge 2 and 3

uf.is_connected(0, 1)  # True
uf.is_connected(0, 2)  # False

uf.get_count()  # 3 groups: {0,1}, {2,3}, {4}
```

**Find redundant connection:**
```python
uf = UnionFind(n)
for u, v in edges:
    if not uf.union(u, v):
        return [u, v]  # This edge creates cycle
```

### Common Mistakes

1. **Not using path compression** - results in O(n) operations instead of O(1)
2. **Not using union by rank** - creates tall trees, slow operations
3. **Checking connection before union** - `union` already returns if they were connected
4. **Off-by-one with indexing** - watch for 0-indexed vs 1-indexed problems
5. **Grid problems: wrong index calculation** - use `r * cols + c`, not `r * rows + c`
6. **Not checking union return value** - tells you if cycle was created

### Key Tips

- **Always implement both optimizations** - path compression + union by rank
- **Union returns boolean** - use it to detect cycles
- **For grids**: Convert (r, c) to single index: `r * cols + c`
- **Count tracking**: Decrement on successful union
- **Size tracking**: Useful for "largest component" problems
- **Undirected graphs only** - Union-Find doesn't work well for directed graphs

### Time & Space Complexity

**With optimizations:**
- **Time**: O(α(n)) ≈ O(1) per operation (amortized)
  - α(n) is inverse Ackermann function, effectively constant
- **Space**: O(n) for parent and rank arrays

**Without optimizations:**
- **Time**: O(n) per operation - unacceptable!

---

## Pattern 10: Dynamic Programming

### When to Use

DP is your tool when you need to:
- Optimal value (max/min)
- Count number of ways
- Overlapping subproblems
- Decisions depend on previous decisions
- Can't use greedy (need to try all possibilities)
- Recurrence relation exists

**Key indicator**: "Optimal", "maximum", "minimum", "longest", "shortest", "number of ways"

### The Six Core Types

DP problems fall into distinct categories with different recurrence patterns. Recognize the type, apply the template.

#### Type 1: 1D DP (Linear)

Problems on a sequence with decisions at each position.

```python
def dp_1d(nums):
    n = len(nums)
    dp = [0] * n
    dp[0] = base_case
    
    for i in range(1, n):
        dp[i] = max(dp[i-1] + nums[i], dp[i-2] + nums[i])  # Recurrence
    
    return dp[-1]

# Space optimized (if only need last few states)
def dp_1d_optimized(nums):
    prev2 = prev1 = 0
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2, prev1 = prev1, curr
    return prev1
```

**Examples:** Climbing Stairs, House Robber, Coin Change, Longest Increasing Subsequence

**Key:** `dp[i]` = answer for subproblem ending at i

#### Type 2: 2D DP (Grid or Two Sequences)

Problems on grids or comparing two sequences.

```python
def dp_2d_grid(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    
    # Base cases
    dp[0][0] = grid[0][0]
    for i in range(1, m): dp[i][0] = dp[i-1][0] + grid[i][0]
    for j in range(1, n): dp[0][j] = dp[0][j-1] + grid[0][j]
    
    # Fill table
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    
    return dp[m-1][n-1]

def dp_two_strings(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    
    # Base cases (if needed)
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return dp[m][n]
```

**Examples:** Unique Paths, Edit Distance, LCS, Minimum Path Sum

**Key:** `dp[i][j]` = answer for subproblem at (i,j) or first i of s1, first j of s2

#### Type 3: State Machine DP

Multiple states per position, transitions between states.

```python
def state_machine(prices):
    # Track different states
    held = -prices[0]  # Currently holding stock
    sold = 0           # Just sold
    rest = 0           # Resting
    
    for price in prices[1:]:
        prev_held, prev_sold, prev_rest = held, sold, rest
        
        held = max(prev_held, prev_rest - price)  # Hold or buy
        sold = prev_held + price                   # Sell
        rest = max(prev_rest, prev_sold)          # Rest
    
    return max(sold, rest)
```

**Examples:** Stock Buy/Sell problems, State transitions

**Key:** Track all possible states, define transitions between them

#### Type 4: Interval DP

Problems on ranges/intervals, often combining smaller intervals.

```python
def interval_dp(nums):
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    
    # Base case: single elements
    for i in range(n):
        dp[i][i] = base_value
    
    # Iterate by interval length
    for length in range(2, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            # Try all split points
            for k in range(i, j):
                dp[i][j] = max(dp[i][j], 
                              dp[i][k] + dp[k+1][j] + cost(i, j, k))
    
    return dp[0][n-1]
```

**Examples:** Burst Balloons, Minimum Score Triangulation, Palindrome problems

**Key:** Build from smaller intervals to larger, try all split points

#### Type 5: 0/1 Knapsack

Choose items with weights/values, capacity constraint.

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity+1) for _ in range(n+1)]
    
    for i in range(1, n+1):
        for w in range(capacity+1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]
            
            # Take item i-1 (if fits)
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i-1][w-weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

# Space optimized (1D)
def knapsack_1d(weights, values, capacity):
    dp = [0] * (capacity+1)
    
    for i in range(len(weights)):
        # Iterate backwards to avoid using updated values
        for w in range(capacity, weights[i]-1, -1):
            dp[w] = max(dp[w], dp[w-weights[i]] + values[i])
    
    return dp[capacity]
```

**Examples:** Partition Equal Subset, Target Sum, Coin Change variants

**Key:** For each item, decide take or don't take. For 0/1: iterate backwards in 1D.

**Unbounded variant:** Can reuse items - iterate forward in 1D

#### Type 6: Tree DP

DP on tree structures using DFS.

```python
def tree_dp(root):
    def dfs(node):
        if not node:
            return (0, 0)  # (take, not_take)
        
        left_take, left_not = dfs(node.left)
        right_take, right_not = dfs(node.right)
        
        # If we take this node
        take = node.val + left_not + right_not
        
        # If we don't take this node
        not_take = max(left_take, left_not) + max(right_take, right_not)
        
        return (take, not_take)
    
    return max(dfs(root))
```

**Examples:** House Robber III, Binary Tree Cameras, Tree DP problems

**Key:** Post-order DFS, return multiple states from subtrees

### Quick Recognition Guide

| Pattern | Recognition |
|---------|------------|
| **1D** | Linear sequence, decision at each position |
| **2D** | Grid paths, two strings/sequences |
| **State Machine** | Multiple states, transitions between them |
| **Interval** | Ranges, combining subproblems, "burst", "merge" |
| **Knapsack** | Items with weight/value, capacity limit |
| **Tree DP** | Tree structure, decisions on nodes |

### Common Mistakes

1. **Wrong base cases** - most DP bugs come from here
2. **Incorrect recurrence relation** - doesn't capture all transitions
3. **Index errors** - off by one in array access
4. **Using updated values** - in knapsack 1D, must iterate backwards
5. **Not considering all cases** - take vs don't take, all splits, etc.
6. **Forgetting memoization** - top-down without memo is just recursion

### Key Tips

- **Start with recursion + memo**, then convert to bottom-up if needed
- **1D space optimization**: Only keep states you need (last 1-2 rows)
- **Knapsack 0/1**: Backward iteration when using 1D array
- **Interval DP**: Always try all split points k from i to j
- **Draw the state transition** - visualize dependencies
- **Base cases matter** - spend time getting these right

### Time & Space Complexity

- **1D**: O(n) time, O(n) or O(1) space
- **2D**: O(n²) or O(mn) time, O(n²) or O(mn) space
- **Interval**: O(n³) time typically
- **Knapsack**: O(n × capacity) time, O(capacity) space optimized

---

## Complete! 🎯

You now have 10 consolidated patterns covering all major algorithm types. Each pattern is stripped down to its essence - just the core template, key tips, and common mistakes. No fluff, no 100 pages of examples.

**What you've built:**
- DFS (covers all graph/tree/backtracking)
- Topological Sort
- Trie
- Two Pointers
- BFS
- Binary Search
- Monotonic Stack/Queue
- Heap
- Union-Find
- Dynamic Programming

Use this as your quick reference before interviews or when solving problems. The patterns are muscle memory now - just recognize the type and apply the template.