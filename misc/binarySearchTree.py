#Simple implementation of a Binary Search Tree
#Methods include insert,delete,exist,search,swap,predecessorSearch,toJson
#For the json output, you can visualize it at jsoncrack.com/editor

from random import randint

class TreeNode:
    def __init__(self,key=0,left=None,right=None):
        self.key = key
        self.left = left
        self.right = right

class BinarySearchTree:
    def __init__(self):
        self.tree = None
        self.size = 0
        self.minKey = float("inf")
        self.maxKey = float("-inf")
    
    def insert(self,key) -> None:

        def dfs(root):
            if not root:
                newNode = TreeNode(key=key,left=None,right=None)
                return newNode
            if root and key > root.key:
                root.right  = dfs(root.right)
            elif root and key < root.key:
                root.left = dfs(root.left)
            
            return root
        
        self.size += 1
        if not self.tree:
            self.tree = TreeNode(key)
        else:
            self.tree = dfs(self.tree)

        self.minKey = min(self.minKey,key)
        self.maxKey = max(self.maxKey,key)
    
    def delete(self,key) -> None:
    
        def dfs(root,key):
            if not root:
                return None
            
            if key > root.key:
                root.right = dfs(root.right,key)
            elif key < root.key:
                root.left = dfs(root.left,key)
            else: # key == root.key
                self.foundFlag = True
                #The node has only one leaf 
                if not root.right:
                    return root.left
                elif not root.left:
                    return root.right
                #The node has both leaves
                temp = root.right
                while temp.left:
                    temp = temp.left
                root.key = temp.key
                root.right = dfs(root.right,temp.key)
                    
            return root
        
        self.foundFlag = False
        if self.tree:
            self.tree = dfs(self.tree,key)
        if self.foundFlag:
            self.size -= 1
            if key == self.minKey:
                self.minKey = self.findNewMin()
            if key == self.maxKey:
                self.maxKey = self.findNewMax()
            self.foundFlag = False
        
    def exist(self,key) -> bool:
    
        def dfs(root):
        
            if not root:
                return False
            left = right = False
            if key > root.key:
                right = dfs(root.right)   
            elif key < root.key:
                left = dfs(root.left)
            else: #key == root.key:
                return True
            
            return left or right
        
        if self.tree:
            return dfs(self.tree)
        else:
            return False
    
    def search(self,key):
    
        def dfs(root):
            if not root:
                return None
            left = right = None
            
            if key > root.key:
                return dfs(root.right)
            elif key < root.key:
                return dfs(root.left)
            else:
                return root

        if self.tree:
            return dfs(self.tree)
        else:
            return None
    
    def findNewMin(self):
    
        def dfs(root):
            if not root:
                return None
            self.minimum = min(self.minimum,root.key)
            dfs(root.left)
        
        self.minimum = float("inf")
        if self.tree:
            dfs(self.tree)
        return self.minimum
    
    def findNewMax(self):
    
        def dfs(root):
            if not root:
                return None
            self.maximum = max(self.maximum,root.key)
            dfs(root.right)
        
        self.maximum = float("-inf")
        if self.tree:
            dfs(self.tree)
        return self.maximum
    
    def swap(self,oldKey,newKey) -> None:
        
        if self.exist(oldKey):
            self.delete(oldKey)
            self.insert(newKey)
    
    def predecessorSearch(self,key):
        def dfs(root,parentNode,leftParent,rightParent) -> TreeNode:
            if not root:
                return None
            
            if root.key > key:
                res = dfs(root.left,root,False,True)
                if not res and self.flag:
                    if leftParent:
                        self.flag = False
                        return parentNode
                    else:
                        return None
                elif res:
                    return res
                else:
                    return None
            elif root.key < key:
                res = dfs(root.right,root,True,False)
                if not res and self.flag:
                    if leftParent:
                        self.flag = False
                        return parentNode
                    else:
                        return None
                elif res:
                    return res
                else:
                    return None
            else: #root.key == key:
                
                #Node has left subtree
                if root.left:
                    temp = root.left
                    while temp.right:
                        temp = temp.right
                    return temp
                
                #Node has no left subtree
                else:
                    #Node is the left child of parent
                    if rightParent:
                        #Return closest ancestor which is a left parent of it's child node
                        self.flag = True
                        return None
                    #Node is the right child of parent
                    else: 
                        #Return parent node value
                        return parentNode
                    
        self.flag = False
        if self.tree and key != self.minKey and self.size > 1:
            return dfs(self.tree,None,False,False)
        else:
            return TreeNode(None)
    
    def successorSearch(self,key):
        def dfs(root,parentNode,leftParent,rightParent) -> TreeNode:
            if not root:
                return None
            
            if root.key > key:
                res = dfs(root.left,root,False,True)
                if not res and self.flag:
                    if rightParent:
                        self.flag = False
                        return parentNode
                    else:
                        return None
                elif res:
                    return res
                else:
                    return None
            elif root.key < key:
                res = dfs(root.right,root,True,False)
                if not res and self.flag:
                    if rightParent:
                        self.flag = False
                        return parentNode
                    else:
                        return None
                elif res:
                    return res
                else:
                    return None
            else: #root.key == key:
                
                #Node has right subtree
                if root.right:
                    temp = root.right
                    while temp.left:
                        temp = temp.left
                    return temp
                
                #Node has no right subtree
                else:
                    #Node is the right child of parent
                    if leftParent:
                        #Return closest ancestor which is a right parent of it's child node
                        self.flag = True
                        return None
                    #Node is the left child of parent
                    else: 
                        #Return parent node value
                        return parentNode
            
        if self.tree and key != self.minKey and self.size > 1:
            return dfs(self.tree,None,False,False)
        else:
            return TreeNode(None)
    
    def toJson(self) -> str:
        def dfs(root):
            if not root:
                return None
            #self.array.append(root.key)
            json = "{\"value\":%s,\"left\":%s,\"right\":%s}" %(root.key,dfs(root.left),dfs(root.right))
            return json
        
        if self.tree:
            json = dfs(self.tree)
            json = json.replace("None","null")
            return json
        else:
            return "{}"  
    
t = BinarySearchTree()
for i in range(20):
    t.insert(randint(0,100))
print(t.size)
print(t.minKey)
print(t.maxKey)
res = t.toJson()
print(res)
