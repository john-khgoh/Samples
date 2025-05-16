// A simple binary search tree implementation
// Includes methods: insert,delete,exist,search,predecessor,swap,toJson

#include <iostream>
//#include <optional>
#include <string>
#include <vector> 
using namespace std;

//TreeNode class
class TreeNode {
public:
    TreeNode(int key,bool notFound,TreeNode* left,TreeNode* right);

    int key;
    bool notFound; //When a key is not found, (1) the key is set to maxKey(std::numeric_limits<int>::min() and (2) notFound is set to true
    TreeNode* left;
    TreeNode* right;
    
};

//TreeNode constructor
TreeNode::TreeNode(int key, bool notFound = false, TreeNode* left=nullptr,TreeNode* right=nullptr):key(key),notFound(notFound),left(left),right(right) {

}

//BinarySearchTree class
class BinarySearchTree {
public:
    BinarySearchTree();

    //Public Methods
    void insertNode(int key);
    void deleteNode(int key);
    bool nodeExist(int key);
    TreeNode* searchNode(int key);
    TreeNode* predecessorNode(int key);
    string toJson();
    int findNewMin();
    int findNewMax();
    void swap(int oldKey, int newKey);

    TreeNode* insertNodeDFS(TreeNode* root, int key);
    TreeNode* deleteNodeDFS(TreeNode* root, int key, bool* foundFlag);
    bool nodeExistDFS(TreeNode* root, int key);
    string toJsonDFS(TreeNode* root);
    TreeNode* searchNodeDFS(TreeNode* root, int key);
    TreeNode* predecessorNodeDFS(TreeNode* root, TreeNode* parent, int key, bool leftParent, bool rightParent, bool* searchFlag);
    void findNewMinDFS(TreeNode* root, int* minimum);
    void findNewMaxDFS(TreeNode* root, int* maximum);
    
    //Variables
    TreeNode* tree;
    int size;
    int minKey;
    int maxKey;
};

//BinarySearchTree constructor
BinarySearchTree::BinarySearchTree():tree(nullptr),size(0),minKey(std::numeric_limits<int>::max()),maxKey(std::numeric_limits<int>::min()) {

}

TreeNode* BinarySearchTree::insertNodeDFS(TreeNode* root, int key) {
    if (root==nullptr) {
        TreeNode* newNode = new TreeNode(key, false, nullptr, nullptr);
        return newNode;
    }
    if (root && key > root->key) {
        root->right = insertNodeDFS(root->right, key);
    } else if (root && key < root->key) {
        root->left = insertNodeDFS(root->left, key);
    }
    return root;
}

void BinarySearchTree::insertNode(int key) {
    size += 1;
    //If the tree has not been initialized
    if (tree==nullptr) {
        tree = new TreeNode(key,false,nullptr,nullptr);
    } else {
        tree = insertNodeDFS(tree,key);
    }
    minKey = std::min(minKey, key);
    maxKey = std::max(maxKey, key);
}

TreeNode* BinarySearchTree::deleteNodeDFS(TreeNode* root, int key, bool* foundFlag) {
    if (root==nullptr) {
        return root;
    }
    if (key > root->key) {
        root->right = deleteNodeDFS(root->right,key,foundFlag);
    } else if (key < root->key) {
        root->left = deleteNodeDFS(root->left,key,foundFlag);
    } else {
        *foundFlag = true;
        if (root->right == nullptr) {
            return root->left;
        } else if (root->left == nullptr) {
            return root->right;
        } 
        TreeNode* temp = root->right;
        while (temp->left != nullptr) {
            temp = temp->left;
        }
        root->key = temp->key;
        root->right = deleteNodeDFS(root->right, temp->key, foundFlag);
    }
    return root;
}

void BinarySearchTree::deleteNode(int key) {
    bool foundFlag = false;
    if (tree) {
        tree = deleteNodeDFS(tree, key, &foundFlag);
    }
    if (foundFlag) {
        size -= 1;
        if (key == minKey) {
            minKey = findNewMin();
        } 
        if (key == maxKey) {
            maxKey = findNewMax();
        }
        foundFlag = false;
    }
}

bool BinarySearchTree::nodeExistDFS(TreeNode* root, int key) {
    if (root == nullptr) {
        return false;
    }
    bool left = false;
    bool right = false;

    if (key > root->key) {
        right = nodeExistDFS(root->right, key);
    }
    else if (key < root->key) {
        left = nodeExistDFS(root->left, key);
    }
    else {
        return true;
    }

    return left || right;
}

bool BinarySearchTree::nodeExist(int key) {
    if (tree != nullptr) {
        return nodeExistDFS(tree, key);
    }
    else {
        return false;
    }
}

TreeNode* BinarySearchTree::searchNodeDFS(TreeNode* root, int key) {
    if (root==nullptr) {
        return root;
    } 
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;

    if (key > root->key) {
        return searchNodeDFS(root->right, key);
    } else if (key < root->key) {
        return searchNodeDFS(root->left, key);
    } else {
        return root;
    }
}

TreeNode* BinarySearchTree::searchNode(int key) {
    TreeNode* notFoundObj = new TreeNode(std::numeric_limits<int>::min(),true);
    if (tree) {
        TreeNode* res = searchNodeDFS(tree,key);
        if (res == nullptr) {
            return notFoundObj;
        } else {
            return res;
        }
    } else {
        return notFoundObj;
    }
}

TreeNode* BinarySearchTree::predecessorNodeDFS(TreeNode* root, TreeNode* parent, int key, bool leftParent, bool rightParent, bool* searchFlag) {
    if (root==nullptr) {
        return root;
    }

    if (root->key > key) {
        TreeNode* res = predecessorNodeDFS(root->left, root, key, false, true, searchFlag);
        //std::optional<TreeNode*> res = predecessorNodeDFS(root->left, root, key, false, true, searchFlag);
        if (res==nullptr && searchFlag) {
            if (leftParent) {
                *searchFlag = false;
                return parent;
            } else {
                return nullptr;
            }
        } else if (res) {
            return res;
        } else {
            return nullptr;
        }
    } else if (root->key < key) {
        TreeNode* res = predecessorNodeDFS(root->right,root,key,true,false,searchFlag);
        //std::optional<TreeNode*> res = predecessorNodeDFS(root->right, root, key, true, false, searchFlag);
        if (res==nullptr && searchFlag) {
            if (leftParent) {
                *searchFlag = false;
                return parent;
            } else {
                return nullptr;
            }
        } else if (res) {
            return res;
        } else {
            return nullptr;
        }
    } else {
        if (root->left) {
            TreeNode* temp = root->left;
            while (temp->right) {
                temp = temp->right;
            }
            return temp;
        } else {
            if (rightParent) {
                *searchFlag = true;
                return nullptr;
            } else {
                return parent;
            }
        }
    }
}

TreeNode* BinarySearchTree::predecessorNode(int key) {
    bool searchFlag = false;
    TreeNode* notFoundObj = new TreeNode(std::numeric_limits<int>::min(), true);
    if (tree && key != minKey && size > 1) {
        TreeNode* res = predecessorNodeDFS(tree, NULL, key, false, false, &searchFlag);
        if (res==nullptr) {
            return notFoundObj;
        } else {
            return res;
        }
    } else {
        return notFoundObj;
    }
}

void BinarySearchTree::findNewMinDFS(TreeNode* root, int* minimum) {
    if (root==nullptr) {
        return;
    }
    *minimum = min(*minimum, root->key);
    findNewMinDFS(root->left,minimum);
}

int BinarySearchTree::findNewMin() {
    int minimum = std::numeric_limits<int>::max();
    if (tree) {
        findNewMinDFS(tree,&minimum);
    }
    return minimum;
}

void BinarySearchTree::findNewMaxDFS(TreeNode* root, int* maximum) {
    if (root == nullptr) {
        return;
    }
    *maximum = max(*maximum, root->key);
    findNewMaxDFS(root->right, maximum);
}

int BinarySearchTree::findNewMax() {
    int maximum = std::numeric_limits<int>::min();
    if (tree) {
        findNewMaxDFS(tree, &maximum);
    }
    return maximum;
}

void BinarySearchTree::swap(int oldKey, int newKey) {
    if (nodeExist(oldKey)) {
        deleteNode(oldKey);
        insertNode(newKey);
    }
}

string BinarySearchTree::toJsonDFS(TreeNode* root) {
    if (root == nullptr) {
        return "null";
    }
    string json = "{\"value\":" + std::to_string(root->key) + ", \"left\":" + toJsonDFS(root->left) + ", \"right\":" + toJsonDFS(root->right) + "}";
    return json;
}

string BinarySearchTree::toJson() {
    if (tree) {
        TreeNode* root = tree;
        return toJsonDFS(root);
    } else {
        return "{}";
    }
    
}

int main()
{
    BinarySearchTree b = BinarySearchTree();

    vector<int> nodeList = {50,17,72,12,23,54,76,9,14,19,67};
    for (int i=0; i < nodeList.size();i++) {
        b.insertNode(nodeList[i]);
    }

    printf("SearchNode 100:%d\n", b.searchNode(100)->key);
    b.swap(19, 18);
    b.swap(76, 99);
    b.swap(9, 5);
    b.deleteNode(12);
    printf("SearchNode 18:%d\n", b.searchNode(18)->key);
    printf("76 exists?%d\n", b.nodeExist(76));
    printf("99 exists?%d\n", b.nodeExist(99));
    printf("Size:%d\n", b.size);
    printf("MinKey:%d\n",b.minKey);
    printf("MaxKey:%d\n", b.maxKey);
    printf("Predecessor node of 99: %d\n", b.predecessorNode(99)->key);
    printf("Predecessor node of 12: %d\n", b.predecessorNode(12)->key);
    cout << b.toJson();
}
