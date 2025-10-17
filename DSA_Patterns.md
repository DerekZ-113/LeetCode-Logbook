# LeetCode Pattern Templates - Complete Reference

## 1. Two Pointers Pattern

### Pattern Recognition
Use two pointers when:
- Array is sorted and need to find pairs/triplets
- Need O(1) space for in-place operations
- Comparing elements from both ends
- Finding cycles in linked lists
- Partitioning arrays based on a condition
- String/array palindrome problems

### Template 1: Opposite Direction (Converging)
```python
def two_pointers_opposite(arr):
    left = 0
    right = len(arr) - 1
    result = 0  # or []
    
    while left < right:
        current = arr[left] + arr[right]  # or other logic
        
        if condition_met(current):
            result = update_result(result, current)
            left += 1
            right -= 1
        elif need_smaller:
            right -= 1
        else:  # need_larger
            left += 1
    
    return result
```
**Practice:** LC 167 (Two Sum II), LC 15 (3Sum), LC 11 (Container With Most Water), LC 42 (Trapping Rain Water)

### Template 2: Same Direction (Sliding)
```python
def two_pointers_same_direction(arr):
    slow = 0
    
    for fast in range(len(arr)):
        if condition_met(arr[fast]):
            arr[slow], arr[fast] = arr[fast], arr[slow]
            slow += 1
    
    return slow  # often returns new length
```
**Practice:** LC 26 (Remove Duplicates), LC 27 (Remove Element), LC 283 (Move Zeroes), LC 80 (Remove Duplicates II)

### Template 3: Fast & Slow (Cycle Detection)
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
    # Detect cycle first, then find start
    # After detection, reset one pointer to head
    # Move both one step until they meet
```
**Practice:** LC 141 (Linked List Cycle), LC 142 (Linked List Cycle II), LC 287 (Find Duplicate Number), LC 202 (Happy Number)

### Template 4: Three Pointers (3Sum Pattern)
```python
def threeSum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue  # skip duplicates
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            # Two pointer logic here
            # Remember to skip duplicates after finding valid triplet
    
    return result
```
**Practice:** LC 15 (3Sum), LC 16 (3Sum Closest), LC 18 (4Sum), LC 259 (3Sum Smaller)

### Template 5: Partition (Dutch National Flag)
```python
def partition(nums):
    low = 0      # boundary of smaller elements
    mid = 0      # current element
    high = len(nums) - 1  # boundary of larger elements
    
    while mid <= high:
        if nums[mid] < pivot:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == pivot:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # Don't increment mid!
```
**Practice:** LC 75 (Sort Colors), LC 215 (Kth Largest Element), LC 324 (Wiggle Sort II)

### Key Points
- **Time:** O(n) for single pass, O(n²) for 3Sum variants, O(n log n) if sorting needed
- **Space:** O(1) for in-place, O(n) if sorting needed
- **Common mistakes:**
  - Wrong loop condition (`<` vs `<=`)
  - Forgetting to skip duplicates in 3Sum
  - Incrementing mid after swapping with high in partition
  - Not handling empty/single element inputs
- **Tips:**
  - For 3Sum variants, sort first then fix one pointer
  - When elements equal, usually move both pointers
  - Fast/slow for cycle uses 2x speed difference

---

## 2. Binary Search Pattern

### Pattern Recognition
Use binary search when:
- Array is sorted (or partially sorted/rotated)
- Finding a target in sorted collection
- Finding boundary/insertion point
- Optimization problems (minimize/maximize with constraint)
- Answer lies in a range and you can verify validity
- O(log n) complexity needed

### Template 1: Classic Binary Search
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
    
    return -1
```
**Practice:** LC 704 (Binary Search), LC 74 (Search 2D Matrix), LC 240 (Search 2D Matrix II)

### Template 2: Find Leftmost (bisect_left)
```python
def find_leftmost(nums, target):
    left, right = 0, len(nums)  # Note: right = len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left

# Using bisect:
import bisect
index = bisect.bisect_left(nums, target)
```
**Practice:** LC 34 (Find First and Last Position), LC 278 (First Bad Version), LC 35 (Search Insert Position)

### Template 3: Find Rightmost (bisect_right)
```python
def find_rightmost(nums, target):
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left - 1  # Last valid position

# Using bisect:
index = bisect.bisect_right(nums, target) - 1
```
**Practice:** LC 34 (Find First and Last Position), LC 744 (Find Smallest Letter)

### Template 4: Binary Search on Answer
```python
def binary_search_answer(arr):
    def is_valid(mid):
        # Check if mid satisfies condition
        return True/False
    
    left, right = min_answer, max_answer
    
    while left < right:
        mid = left + (right - left) // 2
        
        if is_valid(mid):
            right = mid  # or left = mid + 1 depending on problem
        else:
            left = mid + 1  # or right = mid - 1
    
    return left
```
**Practice:** LC 875 (Koko Eating Bananas), LC 1011 (Capacity to Ship), LC 410 (Split Array Largest Sum), LC 1231 (Divide Chocolate)

### Template 5: Rotated Array Search
```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # Check which half is sorted
        if nums[left] <= nums[mid]:  # Left half sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # Right half sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
```
**Practice:** LC 33 (Search Rotated Array), LC 81 (Search Rotated Array II), LC 153 (Find Minimum), LC 154 (Find Minimum II)

### Key Points
- **Time:** O(log n) for all templates
- **Space:** O(1)
- **Common mistakes:**
  - Infinite loop (use `left + (right - left) // 2` to avoid overflow)
  - Off-by-one errors with boundaries
  - Wrong condition (`<` vs `<=`, `len(nums)` vs `len(nums)-1`)
  - Not handling duplicates in rotated array
- **Tips:**
  - Use bisect module when applicable
  - For find leftmost: `right = mid`, for rightmost: `left = mid + 1`
  - Binary search on answer: think "can I do it in X time/with X capacity?"
  - Draw out the search space to visualize boundaries

---

## 3. BFS (Breadth-First Search) Pattern

### Pattern Recognition
Use BFS when:
- Finding shortest path in unweighted graph
- Level-order traversal needed
- Finding minimum steps/moves
- Exploring nodes at same distance before going deeper
- Need to process by layers/rings
- Finding all nodes at distance K

### Template 1: Tree Level-Order Traversal
```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result
```
**Practice:** LC 102 (Binary Tree Level Order), LC 103 (Zigzag Level Order), LC 107 (Level Order Bottom), LC 637 (Average of Levels)

### Template 2: Graph BFS (Shortest Path)
```python
from collections import deque

def bfs_shortest_path(graph, start, target):
    queue = deque([(start, 0)])  # (node, distance)
    visited = {start}
    
    while queue:
        node, dist = queue.popleft()
        
        if node == target:
            return dist
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # Target not reachable
```
**Practice:** LC 127 (Word Ladder), LC 433 (Minimum Genetic Mutation), LC 752 (Open the Lock), LC 1091 (Shortest Path in Binary Matrix)

### Template 3: Multi-Source BFS
```python
from collections import deque

def multi_source_bfs(grid):
    m, n = len(grid), len(grid[0])
    queue = deque()
    
    # Add all sources to queue
    for i in range(m):
        for j in range(n):
            if grid[i][j] == source_value:
                queue.append((i, j, 0))  # (row, col, distance)
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        x, y, dist = queue.popleft()
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < m and 0 <= ny < n and not_visited(grid[nx][ny]):
                grid[nx][ny] = mark_visited
                queue.append((nx, ny, dist + 1))
    
    return grid
```
**Practice:** LC 994 (Rotting Oranges), LC 286 (Walls and Gates), LC 542 (01 Matrix), LC 1162 (As Far from Land)

### Template 4: BFS with State
```python
from collections import deque

def bfs_with_state(start):
    # State can be tuple: (x, y, keys_collected) or (node, path_taken)
    queue = deque([(start_state)])
    visited = {start_state}  # Set of states, not just positions
    
    while queue:
        current_state = queue.popleft()
        
        if is_target(current_state):
            return current_state
        
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    return None
```
**Practice:** LC 864 (Shortest Path to Get All Keys), LC 847 (Shortest Path Visiting All Nodes), LC 815 (Bus Routes)

### Key Points
- **Time:** O(V + E) for graphs, O(N) for trees where N is nodes
- **Space:** O(V) for visited set, O(width) for queue
- **Common mistakes:**
  - Not tracking visited nodes (infinite loop)
  - Marking visited after popping (duplicates in queue)
  - Not processing level by level when needed
  - Using list instead of deque (O(n) vs O(1) popleft)
- **Tips:**
  - Always mark visited when adding to queue, not when popping
  - Use tuple for complex states: (position, keys, steps)
  - For grid problems, can mark visited in-place with special value

---

## 4. DFS (Depth-First Search) Pattern

### Pattern Recognition
Use DFS when:
- Exploring all paths/possibilities
- Tree/graph traversal (preorder, inorder, postorder)
- Finding connected components
- Detecting cycles
- Topological sorting
- Backtracking problems
- Path sum problems

### Template 1: Tree DFS (Recursive)
```python
def dfs_tree(root):
    if not root:
        return
    
    # Preorder: process root first
    process(root.val)
    dfs_tree(root.left)
    dfs_tree(root.right)
    
    # Inorder: left, root, right
    # Postorder: left, right, root
    
def dfs_with_return(root):
    if not root:
        return base_value
    
    left_result = dfs_with_return(root.left)
    right_result = dfs_with_return(root.right)
    
    # Combine results
    current_result = combine(root.val, left_result, right_result)
    return current_result
```
**Practice:** LC 104 (Maximum Depth), LC 110 (Balanced Binary Tree), LC 124 (Binary Tree Maximum Path Sum), LC 543 (Diameter)

### Template 2: Tree DFS (Iterative)
```python
def dfs_iterative(root):
    if not root:
        return []
    
    stack = [root]
    result = []
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Add right first so left is processed first (LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result
```
**Practice:** LC 94 (Inorder Traversal), LC 144 (Preorder Traversal), LC 145 (Postorder Traversal)

### Template 3: Graph DFS
```python
def dfs_graph(graph, start):
    visited = set()
    
    def dfs(node):
        visited.add(node)
        
        # Process current node
        process(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    
    dfs(start)
    return visited

# Finding all connected components
def find_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = set()
    components = 0
    
    for i in range(n):
        if i not in visited:
            dfs(graph, i, visited)
            components += 1
    
    return components
```
**Practice:** LC 200 (Number of Islands), LC 547 (Number of Provinces), LC 695 (Max Area of Island), LC 733 (Flood Fill)

### Template 4: DFS with Path
```python
def dfs_all_paths(root, target):
    result = []
    
    def dfs(node, path, remaining):
        if not node:
            return
        
        path.append(node.val)
        
        if not node.left and not node.right:  # Leaf node
            if remaining == node.val:
                result.append(path[:])  # Copy current path
        
        dfs(node.left, path, remaining - node.val)
        dfs(node.right, path, remaining - node.val)
        
        path.pop()  # Backtrack
    
    dfs(root, [], target)
    return result
```
**Practice:** LC 113 (Path Sum II), LC 257 (Binary Tree Paths), LC 129 (Sum Root to Leaf), LC 437 (Path Sum III)

### Template 5: Grid DFS
```python
def dfs_grid(grid):
    m, n = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def dfs(i, j):
        # Boundary and validity check
        if not (0 <= i < m and 0 <= j < n) or grid[i][j] == invalid:
            return 0  # or base case
        
        # Mark visited (or use separate visited set)
        original = grid[i][j]
        grid[i][j] = '#'  # Mark as visited
        
        result = 1  # or process current cell
        
        for di, dj in directions:
            result += dfs(i + di, j + dj)
        
        # Optional: restore if needed
        # grid[i][j] = original
        
        return result
    
    # Process all cells or specific starting points
    total = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == target:
                total += dfs(i, j)
    
    return total
```
**Practice:** LC 200 (Number of Islands), LC 79 (Word Search), LC 130 (Surrounded Regions), LC 417 (Pacific Atlantic Water)

### Key Points
- **Time:** O(V + E) for graphs, O(N) for trees
- **Space:** O(H) for recursion stack where H is height/depth
- **Common mistakes:**
  - Not handling cycles in graphs (need visited set)
  - Modifying path/list without copying when collecting results
  - Forgetting to backtrack in path problems
  - Stack overflow in deep recursion
- **Tips:**
  - Use visited set for graphs, not needed for trees
  - For path problems, remember to backtrack (path.pop())
  - Can convert recursive to iterative using explicit stack
  - For grid problems, can mark visited in-place or use set

---

## 5. Backtracking Pattern

### Pattern Recognition
Use backtracking when:
- Finding all possible solutions
- Problems mention "all combinations", "all permutations", "all subsets"
- Constraint satisfaction problems (N-Queens, Sudoku)
- Decision tree where you make choices and might need to undo
- Path finding with specific conditions
- String/array partitioning problems
- "Generate all valid..." problems

### Template 1: Subsets (Choose or Don't Choose)
```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path[:])  # Add copy of current subset
        
        for i in range(start, len(nums)):
            # Include nums[i]
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()  # Backtrack
    
    backtrack(0, [])
    return result

# With duplicates
def subsetsWithDup(nums):
    nums.sort()  # Sort to handle duplicates
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue  # Skip duplicates
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result
```
**Practice:** LC 78 (Subsets), LC 90 (Subsets II), LC 491 (Increasing Subsequences)

### Template 2: Permutations
```python
def permute(nums):
    result = []
    
    def backtrack(path, available):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for num in available:
            path.append(num)
            new_available = available.copy()
            new_available.remove(num)
            backtrack(path, new_available)
            path.pop()
    
    backtrack([], nums)
    return result

# More efficient with used array
def permuteEfficient(nums):
    result = []
    used = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            # Handle duplicates: if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
            
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    
    backtrack([])
    return result
```
**Practice:** LC 46 (Permutations), LC 47 (Permutations II), LC 784 (Letter Case Permutation), LC 943 (Find Shortest Superstring)

### Template 3: Combinations (Choose K)
```python
def combine(n, k):
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        
        # Optimization: need k - len(path) more numbers
        # Available: n - i + 1 numbers from i to n
        # Condition: n - i + 1 >= k - len(path)
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result

# Combination Sum (can reuse elements)
def combinationSum(candidates, target):
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            # Use i not i+1 because we can reuse
            backtrack(i, path, remaining - candidates[i])
            path.pop()
    
    backtrack(0, [], target)
    return result
```
**Practice:** LC 77 (Combinations), LC 39 (Combination Sum), LC 40 (Combination Sum II), LC 216 (Combination Sum III)

### Template 4: Grid/Board Problems (N-Queens Style)
```python
def solveNQueens(n):
    result = []
    board = [['.'] * n for _ in range(n)]
    
    def is_valid(row, col):
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check diagonal (top-left)
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # Check anti-diagonal (top-right)
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(row):
        if row == n:
            result.append([''.join(row) for row in board])
            return
        
        for col in range(n):
            if is_valid(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return result
```
**Practice:** LC 51 (N-Queens), LC 52 (N-Queens II), LC 37 (Sudoku Solver), LC 36 (Valid Sudoku)

### Template 5: String/Pattern Building
```python
def generateParenthesis(n):
    result = []
    
    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append(path)
            return
        
        if open_count < n:
            backtrack(path + '(', open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(path + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result

# Word Break with backtracking
def wordBreak(s, wordDict):
    wordSet = set(wordDict)
    result = []
    
    def backtrack(start, path):
        if start == len(s):
            result.append(' '.join(path))
            return
        
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in wordSet:
                path.append(word)
                backtrack(end, path)
                path.pop()
    
    backtrack(0, [])
    return result
```
**Practice:** LC 22 (Generate Parentheses), LC 140 (Word Break II), LC 93 (Restore IP Addresses), LC 131 (Palindrome Partitioning)

### Template 6: General Backtracking Framework
```python
def backtrack_general(data):
    result = []
    
    def is_valid_state(state):
        # Check if current state is a valid solution
        return True
    
    def get_candidates(state):
        # Return list of candidates to try from current state
        return []
    
    def backtrack(state):
        if is_valid_state(state):
            result.append(copy_state(state))
            # return if only need one solution
        
        for candidate in get_candidates(state):
            if not is_valid_candidate(candidate, state):
                continue
            
            # Make move
            make_move(state, candidate)
            
            # Recurse
            backtrack(state)
            
            # Undo move (backtrack)
            undo_move(state, candidate)
    
    backtrack(initial_state)
    return result
```

### Key Points
- **Time:** Usually O(2^N) or O(N!) depending on problem
- **Space:** O(N) for recursion depth
- **Common mistakes:**
  - Not copying results before adding to result list
  - Forgetting to backtrack (pop/undo changes)
  - Not handling duplicates properly (sort first, skip same elements)
  - Wrong loop range or start index
  - Not pruning invalid branches early
- **Tips:**
  - Draw decision tree to visualize
  - For duplicates: sort first, then skip if `nums[i] == nums[i-1]` and i > start
  - Use index/start parameter to avoid revisiting
  - Prune early - return if current path can't lead to solution
  - For optimization, consider memoization if subproblems repeat

---

## 6. Dynamic Programming Pattern

### Pattern Recognition
Use DP when:
- Problem asks for optimal value (max/min)
- Counting number of ways
- Can be broken into overlapping subproblems
- Decisions depend on previous decisions
- Problems mention "optimal", "maximum", "minimum", "longest", "shortest"
- Can't use greedy (need to try all possibilities)
- Recurrence relation exists

### Template 1: 1D DP (Linear)
```python
# Bottom-up
def dp_1d_bottom_up(nums):
    n = len(nums)
    dp = [0] * n  # or (n+1) based on problem
    
    # Base case
    dp[0] = base_value
    
    for i in range(1, n):
        # Recurrence relation
        dp[i] = max/min(dp[i-1] + nums[i], nums[i])
        # Or: dp[i] = dp[i-1] + dp[i-2] + ...
    
    return dp[-1]  # or max(dp)

# Top-down with memoization
def dp_1d_top_down(nums):
    memo = {}
    
    def dp(i):
        if i < 0:  # Base case
            return 0
        if i in memo:
            return memo[i]
        
        # Recurrence relation
        result = max(dp(i-1), dp(i-2) + nums[i])
        memo[i] = result
        return result
    
    return dp(len(nums) - 1)

# Space optimized (only need last few states)
def dp_1d_optimized(nums):
    prev2 = prev1 = 0
    
    for num in nums:
        current = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = current
    
    return prev1
```
**Practice:** LC 70 (Climbing Stairs), LC 198 (House Robber), LC 139 (Word Break), LC 300 (LIS), LC 322 (Coin Change)

### Template 2: 2D DP (Grid/Two Sequences)
```python
# Bottom-up
def dp_2d_bottom_up(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    
    # Base cases
    dp[0][0] = grid[0][0]
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    
    # Fill table
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    
    return dp[m-1][n-1]

# For two strings (LCS, Edit Distance)
def dp_two_strings(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases (if needed)
    for i in range(m + 1):
        dp[i][0] = i  # For edit distance
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # or + 1 for LCS
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
    
    return dp[m][n]
```
**Practice:** LC 62 (Unique Paths), LC 64 (Minimum Path Sum), LC 72 (Edit Distance), LC 1143 (LCS), LC 115 (Distinct Subsequences)

### Template 3: State Machine DP
```python
# Stock problems with states
def maxProfit(prices, k):
    if not prices:
        return 0
    
    n = len(prices)
    # States: [day][transactions_used][holding_stock]
    # Can optimize to 2D by reusing transaction count
    
    # Common states for stock problems:
    # held = stock currently held
    # sold = just sold, cooling
    # rest = can buy
    
    held = -prices[0]  # Bought on day 0
    sold = 0  # No stock to sell on day 0
    rest = 0  # Starting with no stock
    
    for price in prices[1:]:
        prev_held = held
        prev_sold = sold
        prev_rest = rest
        
        held = max(prev_held, prev_rest - price)  # Hold or buy
        sold = prev_held + price  # Sell
        rest = max(prev_rest, prev_sold)  # Rest or come off cooldown
    
    return max(sold, rest)
```
**Practice:** LC 121 (Best Time to Buy Stock), LC 122 (Stock II), LC 123 (Stock III), LC 188 (Stock IV), LC 309 (Stock with Cooldown)

### Template 4: Interval DP
```python
def intervalDP(nums):
    n = len(nums)
    # dp[i][j] = answer for interval from i to j
    dp = [[0] * n for _ in range(n)]
    
    # Base case: single elements
    for i in range(n):
        dp[i][i] = base_value
    
    # Iterate by interval length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            # Try all split points
            for k in range(i, j):
                dp[i][j] = max(dp[i][j], 
                              dp[i][k] + dp[k+1][j] + cost(i, j, k))
    
    return dp[0][n-1]

# Alternative: Memoization approach
def intervalDPMemo(nums):
    memo = {}
    
    def dp(i, j):
        if i > j:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        
        result = 0
        for k in range(i, j + 1):
            result = max(result, 
                        dp(i, k-1) + dp(k+1, j) + cost(i, j, k))
        
        memo[(i, j)] = result
        return result
    
    return dp(0, len(nums) - 1)
```
**Practice:** LC 312 (Burst Balloons), LC 1039 (Min Score Triangulation), LC 1000 (Merge Stones), LC 516 (Longest Palindromic Subsequence)

### Template 5: 0/1 Knapsack
```python
def knapsack(weights, values, capacity):
    n = len(weights)
    # dp[i][w] = max value using first i items with weight limit w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]
            
            # Take item i-1 if possible
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

# Space optimized to 1D
def knapsack_1d(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # Traverse backwards to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]

# Unbounded knapsack (can use items multiple times)
def unbounded_knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```
**Practice:** LC 416 (Partition Equal Subset), LC 494 (Target Sum), LC 474 (Ones and Zeroes), LC 518 (Coin Change 2)

### Template 6: DP on Trees
```python
# Tree DP with DFS
def treeDP(root):
    def dfs(node):
        if not node:
            return (0, 0)  # Return tuple for different states
        
        # Post-order traversal - solve children first
        left_rob, left_not = dfs(node.left)
        right_rob, right_not = dfs(node.right)
        
        # If we rob this node
        rob = node.val + left_not + right_not
        
        # If we don't rob this node
        not_rob = max(left_rob, left_not) + max(right_rob, right_not)
        
        return (rob, not_rob)
    
    return max(dfs(root))
```
**Practice:** LC 337 (House Robber III), LC 968 (Binary Tree Cameras), LC 124 (Binary Tree Max Path Sum)

### Key Points
- **Time:** Usually O(n) for 1D, O(n²) for 2D, O(n³) for interval DP
- **Space:** Can often optimize from O(n²) to O(n) or O(1)
- **Common mistakes:**
  - Wrong base cases
  - Incorrect recurrence relation
  - Not considering all transitions
  - Array index out of bounds
  - Using updated values when should use previous row
- **Tips:**
  - Start with recursive solution, then add memoization, then convert to bottom-up
  - For space optimization, only keep states you need (often last 1-2 rows)
  - Draw the state transition diagram
  - For 0/1 knapsack, traverse backwards when using 1D array
  - For unbounded problems, can reuse current row values

---

## 7. Trie (Prefix Tree) Pattern

### Pattern Recognition
Use Trie when:
- Prefix matching/searching problems
- Autocomplete/suggestions
- Word validation in board games
- Finding all words with common prefix
- Word search in matrix
- Spell checker implementation
- Problems with many string lookups
- Need to check if string is prefix of another

### Template 1: Basic Trie Implementation
```python
class TrieNode:
    def __init__(self):
        self.children = {}  # or [None] * 26 for lowercase only
        self.is_end = False
        # Optional: self.word = None  # Store complete word at end

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
**Practice:** LC 208 (Implement Trie), LC 211 (Design Add and Search Words), LC 642 (Design Search Autocomplete)

### Template 2: Trie with Wildcard/Regex
```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
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
**Practice:** LC 211 (Add and Search Word), LC 745 (Prefix and Suffix Search)

### Template 3: Trie for Word Search in Board
```python
def findWords(board, words):
    # Build Trie from words list
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word  # Store complete word at leaf
    
    m, n = len(board), len(board[0])
    result = []
    
    def dfs(i, j, node):
        if i < 0 or i >= m or j < 0 or j >= n:
            return
        
        char = board[i][j]
        if char not in node.children:
            return
        
        next_node = node.children[char]
        
        if next_node.word:
            result.append(next_node.word)
            next_node.word = None  # Avoid duplicates
        
        board[i][j] = '#'  # Mark visited
        
        # Explore 4 directions
        dfs(i + 1, j, next_node)
        dfs(i - 1, j, next_node)
        dfs(i, j + 1, next_node)
        dfs(i, j - 1, next_node)
        
        board[i][j] = char  # Restore
        
        # Prune: remove leaf nodes with no word
        if not next_node.children and not next_node.word:
            del node.children[char]
    
    for i in range(m):
        for j in range(n):
            dfs(i, j, root)
    
    return result
```
**Practice:** LC 212 (Word Search II), LC 79 (Word Search)

### Template 4: Trie for Maximum XOR
```python
class BitTrie:
    def __init__(self):
        self.root = {}
    
    def insert(self, num):
        node = self.root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node:
                node[bit] = {}
            node = node[bit]
    
    def find_max_xor(self, num):
        node = self.root
        max_xor = 0
        
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            # Try to go opposite direction for max XOR
            toggled = 1 - bit
            
            if toggled in node:
                max_xor |= (1 << i)
                node = node[toggled]
            else:
                node = node[bit]
        
        return max_xor

def findMaximumXOR(nums):
    trie = BitTrie()
    max_xor = 0
    
    for num in nums:
        trie.insert(num)
        max_xor = max(max_xor, trie.find_max_xor(num))
    
    return max_xor
```
**Practice:** LC 421 (Maximum XOR), LC 1707 (Maximum XOR With Element), LC 1803 (Count Pairs With XOR in Range)

### Template 5: Trie with Count/Frequency
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0  # Prefix count
        self.end_count = 0  # Word end count

class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.root = TrieNode()
        self.current = self.root
        self.search_term = ""
        
        # Build initial trie
        for sentence, count in zip(sentences, times):
            self.add(sentence, count)
    
    def add(self, sentence, count):
        node = self.root
        for char in sentence:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += count
        node.end_count += count
    
    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # DFS to find all words with this prefix
        result = []
        
        def dfs(node, path):
            if node.end_count > 0:
                result.append((path, node.end_count))
            for char, child in node.children.items():
                dfs(child, path + char)
        
        dfs(node, prefix)
        # Sort by frequency then lexicographically
        result.sort(key=lambda x: (-x[1], x[0]))
        return [word for word, _ in result[:3]]
```
**Practice:** LC 642 (Design Search Autocomplete), LC 1804 (Implement Trie II), LC 677 (Map Sum Pairs)

### Template 6: Replace Words with Trie
```python
def replaceWords(dictionary, sentence):
    # Build Trie from dictionary
    root = TrieNode()
    for word in dictionary:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def find_root(word):
        node = root
        for i, char in enumerate(word):
            if char not in node.children:
                return word
            node = node.children[char]
            if node.is_end:
                return word[:i + 1]
        return word
    
    words = sentence.split()
    return ' '.join(find_root(word) for word in words)
```
**Practice:** LC 648 (Replace Words), LC 820 (Short Encoding of Words), LC 472 (Concatenated Words)

### Key Points
- **Time:** O(m) for insert/search where m is word length; O(n*m) for n words
- **Space:** O(ALPHABET_SIZE * N * M) worst case for N words of length M
- **Common mistakes:**
  - Not marking word endings
  - Forgetting to handle wildcards properly
  - Not pruning empty branches in word search
  - Using array instead of dict for sparse character sets
  - Not restoring board state in backtracking
- **Tips:**
  - Use dict for sparse alphabets, array[26] for lowercase only
  - Can store additional info at nodes (frequency, complete word)
  - For board problems, store complete word at end to avoid rebuilding
  - Prune aggressively in word search to improve performance
  - For XOR problems, process bits from MSB to LSB

---

## 8. Union-Find (Disjoint Set) Pattern

### Pattern Recognition
Use Union-Find when:
- Finding connected components dynamically
- Detecting cycles in undirected graphs
- Checking if two nodes are in same group
- Merging sets/groups efficiently
- Minimum spanning tree (Kruskal's)
- Problems with "connectivity" or "equivalence"
- Account merging type problems
- Friend circles/network connectivity

### Template 1: Basic Union-Find
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Number of components
    
    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already connected
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.count -= 1
        return True  # Successfully connected
    
    def is_connected(self, x, y):
        return self.find(x) == self.find(y)
    
    def get_count(self):
        return self.count
```
**Practice:** LC 547 (Number of Provinces), LC 684 (Redundant Connection), LC 323 (Number of Connected Components)

### Template 2: Union-Find with Size
```python
class UnionFindSize:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n  # Size of each component
        self.count = n
        self.max_size = 1  # Track largest component
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by size - attach smaller to larger
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
            self.max_size = max(self.max_size, self.size[root_y])
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.max_size = max(self.max_size, self.size[root_x])
        
        self.count -= 1
        return True
    
    def get_size(self, x):
        return self.size[self.find(x)]
```
**Practice:** LC 695 (Max Area of Island), LC 128 (Longest Consecutive Sequence), LC 924 (Minimize Malware Spread)

### Template 3: Detect Cycle in Graph
```python
def findRedundantConnection(edges):
    """Find edge that creates cycle"""
    n = len(edges)
    uf = UnionFind(n + 1)  # 1-indexed nodes
    
    for u, v in edges:
        if not uf.union(u, v):
            # This edge creates a cycle
            return [u, v]
    
    return []

def hasCycle(n, edges):
    """Check if undirected graph has cycle"""
    uf = UnionFind(n)
    
    for u, v in edges:
        if uf.is_connected(u, v):
            return True
        uf.union(u, v)
    
    return False
```
**Practice:** LC 684 (Redundant Connection), LC 685 (Redundant Connection II), LC 261 (Graph Valid Tree)

### Template 4: Grid Union-Find
```python
def numIslands2(m, n, positions):
    """Add lands dynamically and count islands"""
    uf = UnionFind(m * n)
    grid = [[0] * n for _ in range(m)]
    result = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    islands = 0
    
    def index(i, j):
        return i * n + j
    
    for r, c in positions:
        if grid[r][c] == 1:
            result.append(islands)
            continue
        
        grid[r][c] = 1
        islands += 1
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                if uf.union(index(r, c), index(nr, nc)):
                    islands -= 1
        
        result.append(islands)
    
    return result
```
**Practice:** LC 305 (Number of Islands II), LC 200 (Number of Islands), LC 130 (Surrounded Regions)

### Template 5: Account/Email Merging
```python
def accountsMerge(accounts):
    """Merge accounts with common emails"""
    uf = UnionFind(len(accounts))
    email_to_id = {}
    
    # Build union-find structure
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            else:
                email_to_id[email] = i
    
    # Group emails by root
    from collections import defaultdict
    merged = defaultdict(set)
    for email, idx in email_to_id.items():
        root = uf.find(idx)
        merged[root].add(email)
    
    # Build result
    result = []
    for root, emails in merged.items():
        name = accounts[root][0]
        result.append([name] + sorted(emails))
    
    return result
```
**Practice:** LC 721 (Accounts Merge), LC 737 (Sentence Similarity II), LC 990 (Satisfiability of Equality)

### Template 6: Weighted Union-Find
```python
class WeightedUnionFind:
    """Union-Find with edge weights/distances"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.weight = [1.0] * n  # Weight from node to parent
    
    def find(self, x):
        if self.parent[x] != x:
            # Path compression with weight update
            original_parent = self.parent[x]
            self.parent[x] = self.find(self.parent[x])
            self.weight[x] *= self.weight[original_parent]
        return self.parent[x]
    
    def union(self, x, y, value):
        """x / y = value"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return
        
        # root_x -> root_y with proper weight
        self.parent[root_x] = root_y
        # weight[x] * weight[root_x] = value * weight[y]
        self.weight[root_x] = value * self.weight[y] / self.weight[x]
    
    def query(self, x, y):
        """Return x / y if connected, else -1"""
        if x not in range(len(self.parent)) or y not in range(len(self.parent)):
            return -1.0
        
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x != root_y:
            return -1.0
        
        return self.weight[x] / self.weight[y]
```
**Practice:** LC 399 (Evaluate Division), LC 952 (Largest Component Size)

### Template 7: MST with Kruskal's
```python
def minimumSpanningTree(n, edges):
    """Find MST using Kruskal's algorithm"""
    # Sort edges by weight
    edges.sort(key=lambda x: x[2])
    
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges = []
    
    for u, v, weight in edges:
        if uf.union(u, v):
            mst_weight += weight
            mst_edges.append([u, v, weight])
            
            # Early termination
            if len(mst_edges) == n - 1:
                break
    
    return mst_weight, mst_edges
```
**Practice:** LC 1584 (Min Cost to Connect Points), LC 1168 (Optimize Water Distribution), LC 1135 (Connecting Cities)

### Key Points
- **Time:** O(α(n)) ≈ O(1) for find/union with path compression and union by rank
- **Space:** O(n) for parent and rank arrays
- **Common mistakes:**
  - Not using path compression (leads to O(n) find)
  - Forgetting to check if already connected before union
  - Off-by-one errors with node indexing (0-indexed vs 1-indexed)
  - Not tracking component count correctly
  - For grids, forgetting to convert 2D to 1D index
- **Tips:**
  - Always use both path compression and union by rank/size
  - Return boolean from union to check if merge happened
  - For grid problems, use `index = row * cols + col`
  - Can track additional info: size, count, max component
  - For weighted UF, be careful with division/multiplication order

---

## 9. Topological Sort Pattern

### Pattern Recognition
Use Topological Sort when:
- Problems involve prerequisites or dependencies
- Course scheduling problems
- Build order/compilation order
- Directed Acyclic Graph (DAG) ordering
- Need to process nodes with no incoming edges first
- Detecting cycles in directed graphs
- Finding if valid ordering exists
- Task scheduling with constraints

### Template 1: Kahn's Algorithm (BFS)
```python
from collections import deque, defaultdict

def topologicalSort(numNodes, prerequisites):
    """BFS approach using in-degree"""
    # Build graph and in-degree
    graph = defaultdict(list)
    in_degree = [0] * numNodes
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Queue all nodes with no prerequisites
    queue = deque([i for i in range(numNodes) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        # Process neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all nodes processed (no cycle)
    if len(result) == numNodes:
        return result
    else:
        return []  # Cycle detected
```
**Practice:** LC 207 (Course Schedule), LC 210 (Course Schedule II), LC 269 (Alien Dictionary)

### Template 2: DFS Topological Sort
```python
def topologicalSortDFS(numNodes, prerequisites):
    """DFS approach with visit states"""
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # States: 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * numNodes
    result = []
    
    def dfs(node):
        if state[node] == 1:  # Cycle detected
            return False
        if state[node] == 2:  # Already processed
            return True
        
        state[node] = 1  # Mark as visiting
        
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        
        state[node] = 2  # Mark as visited
        result.append(node)  # Add to result in reverse order
        return True
    
    for i in range(numNodes):
        if state[i] == 0:
            if not dfs(i):
                return []  # Cycle detected
    
    return result[::-1]  # Reverse to get correct order
```
**Practice:** LC 207 (Course Schedule), LC 210 (Course Schedule II), LC 802 (Find Safe States)

### Template 3: All Topological Sorts
```python
def allTopologicalSorts(numNodes, prerequisites):
    """Find all possible topological orderings"""
    graph = defaultdict(list)
    in_degree = [0] * numNodes
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        
        # Try all nodes with in-degree 0
        for node in list(remaining):
            if in_degree[node] == 0:
                # Choose
                path.append(node)
                remaining.remove(node)
                for neighbor in graph[node]:
                    in_degree[neighbor] -= 1
                
                # Explore
                backtrack(path, remaining)
                
                # Unchoose
                for neighbor in graph[node]:
                    in_degree[neighbor] += 1
                remaining.add(node)
                path.pop()
    
    initial = set(range(numNodes))
    backtrack([], initial)
    return result
```
**Practice:** LC 444 (Sequence Reconstruction), Custom problems requiring all orderings

### Template 4: Alien Dictionary
```python
def alienOrder(words):
    """Derive character order from sorted words"""
    # Build graph from character ordering
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    # Compare adjacent words
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        
        # Invalid case: "abc" before "ab"
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        
        # Find first different character
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
    
    # Kahn's algorithm
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    
    while queue:
        char = queue.popleft()
        result.append(char)
        
        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all characters are included
    if len(result) == len(in_degree):
        return ''.join(result)
    return ""  # Has cycle
```
**Practice:** LC 269 (Alien Dictionary), LC 953 (Verifying Alien Dictionary)

### Template 5: Course Schedule with Queries
```python
def checkIfPrerequisite(numCourses, prerequisites, queries):
    """Check if one course is prerequisite of another"""
    # Build graph
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for a, b in prerequisites:
        graph[a].append(b)
        in_degree[b] += 1
    
    # Find all prerequisites using BFS
    is_prereq = [[False] * numCourses for _ in range(numCourses)]
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    
    while queue:
        node = queue.popleft()
        
        for neighbor in graph[node]:
            # node is prereq of neighbor
            is_prereq[node][neighbor] = True
            
            # All prereqs of node are also prereqs of neighbor
            for i in range(numCourses):
                if is_prereq[i][node]:
                    is_prereq[i][neighbor] = True
            
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return [is_prereq[q[0]][q[1]] for q in queries]
```
**Practice:** LC 1462 (Course Schedule IV), LC 2115 (Find All Possible Recipes)

### Template 6: Parallel Courses
```python
def minimumSemesters(n, relations):
    """Find minimum semesters to complete all courses"""
    graph = defaultdict(list)
    in_degree = [0] * (n + 1)
    
    for prereq, course in relations:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(1, n + 1) if in_degree[i] == 0])
    semesters = 0
    studied = 0
    
    while queue:
        # Process all courses in this semester
        semester_size = len(queue)
        semesters += 1
        
        for _ in range(semester_size):
            course = queue.popleft()
            studied += 1
            
            for next_course in graph[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
    
    return semesters if studied == n else -1
```
**Practice:** LC 1136 (Parallel Courses), LC 2050 (Parallel Courses III)

### Template 7: Task Scheduling with Time
```python
def minimumTime(n, relations, time):
    """Find minimum time to complete all tasks"""
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for prereq, task in relations:
        prereq -= 1  # Convert to 0-indexed
        task -= 1
        graph[prereq].append(task)
        in_degree[task] += 1
    
    # Track earliest completion time for each task
    completion_time = [0] * n
    queue = deque()
    
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
            completion_time[i] = time[i]
    
    while queue:
        task = queue.popleft()
        
        for next_task in graph[task]:
            # Update earliest start time for next_task
            completion_time[next_task] = max(
                completion_time[next_task],
                completion_time[task] + time[next_task]
            )
            
            in_degree[next_task] -= 1
            if in_degree[next_task] == 0:
                queue.append(next_task)
    
    return max(completion_time)
```
**Practice:** LC 2050 (Parallel Courses III), LC 1857 (Largest Color Value in Graph)

### Key Points
- **Time:** O(V + E) for both BFS and DFS approaches
- **Space:** O(V + E) for graph representation
- **Common mistakes:**
  - Not detecting cycles properly
  - Wrong order in DFS (forgetting to reverse)
  - Not handling disconnected components
  - Off-by-one with 0-indexed vs 1-indexed nodes
  - Not initializing in-degree correctly
- **Tips:**
  - Kahn's (BFS) is often easier and detects cycles naturally
  - DFS requires careful state tracking (visiting vs visited)
  - For lexicographical order, use min-heap instead of queue
  - Can track additional info: levels, time, prerequisites
  - Result length != numNodes means cycle exists

---

## 10. Monotonic Stack/Queue Pattern

### Pattern Recognition
Use Monotonic Stack when:
- Finding next/previous greater/smaller element
- Maximum rectangle in histogram
- Stock span problems
- Building visibility problems
- Temperature/price comparison over days
- Problems asking for nearest larger/smaller values

Use Monotonic Queue when:
- Sliding window maximum/minimum
- Jump game problems with constraints
- Finding subarrays with min/max conditions

### Template 1: Next Greater Element
```python
def nextGreaterElement(nums):
    """Find next greater element for each element"""
    n = len(nums)
    result = [-1] * n
    stack = []  # Monotonic decreasing stack (indices)
    
    for i in range(n):
        # Pop smaller elements
        while stack and nums[stack[-1]] < nums[i]:
            idx = stack.pop()
            result[idx] = nums[i]
        
        stack.append(i)
    
    return result

# Circular array variant
def nextGreaterCircular(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    
    # Process array twice for circular
    for i in range(2 * n):
        idx = i % n
        
        while stack and nums[stack[-1]] < nums[idx]:
            result[stack.pop()] = nums[idx]
        
        if i < n:
            stack.append(idx)
    
    return result
```
**Practice:** LC 496 (Next Greater Element I), LC 503 (Next Greater Element II), LC 739 (Daily Temperatures)

### Template 2: Previous Smaller Element
```python
def previousSmaller(nums):
    """Find previous smaller element for each element"""
    n = len(nums)
    result = [-1] * n
    stack = []  # Monotonic increasing stack
    
    for i in range(n):
        # Pop greater or equal elements
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        
        if stack:
            result[i] = nums[stack[-1]]
        
        stack.append(i)
    
    return result

# Finding both previous and next smaller
def findSmallerElements(nums):
    n = len(nums)
    prev_smaller = [-1] * n
    next_smaller = [-1] * n
    stack = []
    
    # Previous smaller
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        if stack:
            prev_smaller[i] = stack[-1]
        stack.append(i)
    
    # Next smaller
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        if stack:
            next_smaller[i] = stack[-1]
        stack.append(i)
    
    return prev_smaller, next_smaller
```
**Practice:** LC 84 (Largest Rectangle in Histogram), LC 85 (Maximal Rectangle), LC 907 (Sum of Subarray Minimums)

### Template 3: Largest Rectangle in Histogram
```python
def largestRectangle(heights):
    """Find largest rectangle area in histogram"""
    stack = []  # Monotonic increasing stack of indices
    max_area = 0
    
    for i, h in enumerate(heights):
        # Pop bars taller than current
        while stack and heights[stack[-1]] > h:
            height_idx = stack.pop()
            height = heights[height_idx]
            
            # Calculate width
            if stack:
                width = i - stack[-1] - 1
            else:
                width = i
            
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    # Process remaining bars
    while stack:
        height_idx = stack.pop()
        height = heights[height_idx]
        
        if stack:
            width = len(heights) - stack[-1] - 1
        else:
            width = len(heights)
        
        max_area = max(max_area, height * width)
    
    return max_area
```
**Practice:** LC 84 (Largest Rectangle), LC 85 (Maximal Rectangle), LC 1504 (Count Submatrices With All Ones)

### Template 4: Stock Span
```python
class StockSpanner:
    """Find span of stock prices (consecutive days <= today's price)"""
    def __init__(self):
        self.stack = []  # (price, span)
    
    def next(self, price):
        span = 1
        
        # Pop all smaller or equal prices
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        
        self.stack.append((price, span))
        return span

def calculateSpan(prices):
    """Calculate span for all days"""
    n = len(prices)
    span = [1] * n
    stack = []  # Monotonic decreasing stack of indices
    
    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()
        
        if stack:
            span[i] = i - stack[-1]
        else:
            span[i] = i + 1
        
        stack.append(i)
    
    return span
```
**Practice:** LC 901 (Online Stock Span), LC 907 (Sum of Subarray Minimums), LC 1019 (Next Greater Node)

### Template 5: Monotonic Queue (Sliding Window Max)
```python
from collections import deque

def maxSlidingWindow(nums, k):
    """Find maximum in each sliding window of size k"""
    dq = deque()  # Monotonic decreasing queue (indices)
    result = []
    
    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result after first window
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

# Min sliding window variant
def minSlidingWindow(nums, k):
    dq = deque()  # Monotonic increasing queue
    result = []
    
    for i in range(len(nums)):
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        while dq and nums[dq[-1]] > nums[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```
**Practice:** LC 239 (Sliding Window Maximum), LC 1438 (Longest Subarray With Limited Diff), LC 862 (Shortest Subarray with Sum >= K)

### Template 6: Subarray with Bounded Min/Max
```python
def longestSubarray(nums, limit):
    """Longest subarray where max - min <= limit"""
    min_dq = deque()  # Monotonic increasing
    max_dq = deque()  # Monotonic decreasing
    left = 0
    result = 0
    
    for right in range(len(nums)):
        # Update min queue
        while min_dq and nums[min_dq[-1]] >= nums[right]:
            min_dq.pop()
        min_dq.append(right)
        
        # Update max queue
        while max_dq and nums[max_dq[-1]] <= nums[right]:
            max_dq.pop()
        max_dq.append(right)
        
        # Shrink window if needed
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            left += 1
            
            # Remove elements outside window
            while min_dq and min_dq[0] < left:
                min_dq.popleft()
            while max_dq and max_dq[0] < left:
                max_dq.popleft()
        
        result = max(result, right - left + 1)
    
    return result
```
**Practice:** LC 1438 (Longest Subarray), LC 1499 (Max Value of Equation), LC 1696 (Jump Game VI)

### Template 7: Trapping Rain Water
```python
def trap(height):
    """Calculate trapped rain water"""
    stack = []  # Monotonic decreasing stack
    water = 0
    
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = height[stack.pop()]
            
            if not stack:
                break
            
            # Calculate water between stack[-1] and i
            width = i - stack[-1] - 1
            bounded_height = min(height[stack[-1]], h) - bottom
            water += width * bounded_height
        
        stack.append(i)
    
    return water

# Alternative: Two pointers approach
def trapTwoPointers(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
```
**Practice:** LC 42 (Trapping Rain Water), LC 407 (Trapping Rain Water II), LC 11 (Container With Most Water)

### Key Points
- **Time:** O(n) for single pass
- **Space:** O(n) worst case for stack/queue
- **Common mistakes:**
  - Wrong monotonic direction (increasing vs decreasing)
  - Not handling equal elements correctly
  - Forgetting to process remaining stack elements
  - Index vs value confusion
  - Not removing out-of-window elements in queue
- **Tips:**
  - Draw the histogram/array to visualize
  - Decreasing stack for next greater, increasing for next smaller
  - Store indices instead of values for more flexibility
  - For sliding window, use deque and maintain window bounds
  - Process remaining stack elements after main loop

---

## 11. Heap Pattern

### Pattern Recognition
Use Heap when:
- Finding K largest/smallest elements
- Merging K sorted arrays/lists
- Finding median from stream
- Priority queue problems
- Scheduling problems (meetings, tasks)
- Shortest path (Dijkstra)
- Problems needing frequent min/max operations
- K closest/furthest points

### Template 1: Top K Elements
```python
import heapq

def topKFrequent(nums, k):
    """Find k most frequent elements"""
    from collections import Counter
    count = Counter(nums)
    
    # Min heap of size k - keep k largest
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]

def kLargestElements(nums, k):
    """Find k largest elements"""
    # Method 1: Min heap of size k
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
    
    # Method 2: Max heap (negate values)
    max_heap = [-num for num in nums]
    heapq.heapify(max_heap)
    return [-heapq.heappop(max_heap) for _ in range(k)]
    
    # Method 3: heapq.nlargest
    return heapq.nlargest(k, nums)
```
**Practice:** LC 347 (Top K Frequent), LC 215 (Kth Largest), LC 692 (Top K Frequent Words), LC 451 (Sort by Frequency)

### Template 2: Merge K Sorted Lists
```python
def mergeKLists(lists):
    """Merge k sorted linked lists"""
    heap = []
    
    # Add first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    dummy = ListNode(0)
    current = dummy
    
    while heap:
        val, idx, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        
        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    
    return dummy.next

def mergeKArrays(arrays):
    """Merge k sorted arrays"""
    heap = []
    result = []
    
    # (value, array_index, element_index)
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(arrays[arr_idx]):
            heapq.heappush(heap, 
                (arrays[arr_idx][elem_idx + 1], arr_idx, elem_idx + 1))
    
    return result
```
**Practice:** LC 23 (Merge K Sorted Lists), LC 378 (Kth Smallest in Sorted Matrix), LC 632 (Smallest Range Covering K Lists)

### Template 3: Median from Data Stream
```python
class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (negate values)
        self.large = []  # Min heap
    
    def addNum(self, num):
        # Add to max heap
        heapq.heappush(self.small, -num)
        
        # Balance: move largest from small to large
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Size balance
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

# Sliding window median
def medianSlidingWindow(nums, k):
    """Find median in each window of size k"""
    # Similar to MedianFinder but with removal
    # Can use SortedList for easier implementation
    from sortedcontainers import SortedList
    window = SortedList()
    result = []
    
    for i in range(len(nums)):
        window.add(nums[i])
        
        if len(window) > k:
            window.remove(nums[i - k])
        
        if len(window) == k:
            if k % 2:
                result.append(float(window[k // 2]))
            else:
                result.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
    
    return result
```
**Practice:** LC 295 (Find Median from Stream), LC 480 (Sliding Window Median), LC 703 (Kth Largest in Stream)

### Template 4: K Closest Points
```python
def kClosest(points, k):
    """Find k closest points to origin"""
    # Method 1: Max heap of size k
    heap = []
    
    for x, y in points:
        dist = -(x*x + y*y)  # Negative for max heap
        
        if len(heap) < k:
            heapq.heappush(heap, (dist, x, y))
        elif dist > heap[0][0]:
            heapq.heapreplace(heap, (dist, x, y))
    
    return [[x, y] for _, x, y in heap]
    
    # Method 2: Using heapq.nsmallest
    return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)

def kClosestToTarget(points, k, target):
    """Find k closest points to a target point"""
    tx, ty = target
    
    def distance(point):
        return (point[0] - tx)**2 + (point[1] - ty)**2
    
    return heapq.nsmallest(k, points, key=distance)
```
**Practice:** LC 973 (K Closest Points), LC 658 (Find K Closest Elements), LC 1779 (Find Nearest Point)

### Template 5: Task Scheduling
```python
def leastInterval(tasks, n):
    """Schedule tasks with cooldown period n"""
    from collections import Counter
    
    counts = Counter(tasks)
    max_heap = [-cnt for cnt in counts.values()]
    heapq.heapify(max_heap)
    
    time = 0
    cooldown = deque()  # (available_time, count)
    
    while max_heap or cooldown:
        time += 1
        
        # Add tasks back from cooldown
        while cooldown and cooldown[0][0] <= time:
            _, cnt = cooldown.popleft()
            heapq.heappush(max_heap, cnt)
        
        if max_heap:
            cnt = heapq.heappop(max_heap) + 1  # Execute one task
            if cnt < 0:  # Still tasks remaining
                cooldown.append((time + n + 1, cnt))
    
    return time

def scheduleCourse(courses):
    """Take maximum courses before deadlines"""
    # Sort by deadline
    courses.sort(key=lambda x: x[1])
    
    heap = []  # Max heap of course durations
    time = 0
    
    for duration, deadline in courses:
        time += duration
        heapq.heappush(heap, -duration)
        
        # If over deadline, drop longest course
        if time > deadline:
            time += heapq.heappop(heap)  # Add negative value
    
    return len(heap)
```
**Practice:** LC 621 (Task Scheduler), LC 630 (Course Schedule III), LC 1353 (Max Events), LC 1834 (Single-Threaded CPU)

### Template 6: Meeting Rooms
```python
def minMeetingRooms(intervals):
    """Find minimum meeting rooms needed"""
    if not intervals:
        return 0
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min heap of end times
    heap = []
    heapq.heappush(heap, intervals[0][1])
    
    for i in range(1, len(intervals)):
        # If earliest ending meeting finished, reuse room
        if heap[0] <= intervals[i][0]:
            heapq.heappop(heap)
        
        # Add current meeting end time
        heapq.heappush(heap, intervals[i][1])
    
    return len(heap)

def meetingRoomsIII(n, meetings):
    """Allocate meetings to n rooms, return most used"""
    meetings.sort()  # Sort by start time
    
    available = list(range(n))  # Available room numbers
    heapq.heapify(available)
    
    in_use = []  # (end_time, room_number)
    room_count = [0] * n
    
    for start, end in meetings:
        # Free up finished meetings
        while in_use and in_use[0][0] <= start:
            _, room = heapq.heappop(in_use)
            heapq.heappush(available, room)
        
        if available:
            room = heapq.heappop(available)
            heapq.heappush(in_use, (end, room))
        else:
            # Wait for earliest meeting to end
            end_time, room = heapq.heappop(in_use)
            heapq.heappush(in_use, (end_time + end - start, room))
        
        room_count[room] += 1
    
    return room_count.index(max(room_count))
```
**Practice:** LC 253 (Meeting Rooms II), LC 1851 (Min Interval), LC 2402 (Meeting Rooms III)

### Template 7: Dijkstra's Algorithm
```python
def dijkstra(n, edges, start):
    """Find shortest path from start to all nodes"""
    from collections import defaultdict
    
    graph = defaultdict(list)
    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))  # If undirected
    
    dist = [float('inf')] * n
    dist[start] = 0
    
    heap = [(0, start)]  # (distance, node)
    visited = set()
    
    while heap:
        d, u = heapq.heappop(heap)
        
        if u in visited:
            continue
        visited.add(u)
        
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(heap, (dist[v], v))
    
    return dist

def networkDelayTime(times, n, k):
    """Time for signal to reach all nodes"""
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    heap = [(0, k)]
    dist = {}
    
    while heap:
        time, node = heapq.heappop(heap)
        
        if node in dist:
            continue
        dist[node] = time
        
        for nei, w in graph[node]:
            if nei not in dist:
                heapq.heappush(heap, (time + w, nei))
    
    return max(dist.values()) if len(dist) == n else -1
```
**Practice:** LC 743 (Network Delay Time), LC 787 (Cheapest Flight), LC 1514 (Path with Max Probability)

### Key Points
- **Time:** O(n log k) for top K; O(n log n) for sorting-based
- **Space:** O(k) for maintaining k elements; O(n) for all elements
- **Common mistakes:**
  - Forgetting Python uses min heap (negate for max heap)
  - Wrong comparison in heap operations
  - Not handling ties in comparison (use tuple with tiebreaker)
  - Off-by-one in k elements (> k vs >= k)
  - Not checking empty heap before pop
- **Tips:**
  - Use tuple (priority, tiebreaker, item) for complex ordering
  - heapq.heappushpop() and heapq.heapreplace() for efficiency
  - For max heap, negate values or use custom comparison
  - Consider SortedList for problems needing removal
  - Track visited in Dijkstra to avoid revisiting