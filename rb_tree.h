#ifndef RED_BLACK_TREE_H
#define RED_BLACK_TREE_H

namespace wiklvrain {

const bool RED = false;
const bool BLACK = true;

template<typename K, typename V = int>
struct rb_tree_node {
  typedef rb_tree_node<K, V>* pRBnode;
  
  K key;
  V value;
  bool color;
  pRBnode left, right;
  
  rb_tree_node(K _key, V _value, bool _color = BLACK): key(_key), value(_value), color(_color) {
    left = nullptr;
    right = nullptr;
  }
};

template<typename K, typename V = int>
class rb_tree {
public:
protected;
  typedef K key_type;
  typedef V value_type;
  typedef rb_tree_node<K, V> Node;
  typedef Node* pNode;
private:
  void left_rotate();
  void right_rotate();

  Node root;
};
}

#endif
