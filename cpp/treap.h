#ifndef WIKLVRAIN_TREAP_H
#define WIKLVRAIN_TREAP_H

#include <ctime>
#include <limits>
#include <cstdlib>
#include <utility>
#include <initializer_list>

namespace wiklvrain {

template<typename K, typename V = int>
struct treap_node {
  typedef K key_type;
  typedef V value_type;

  key_type key;
  value_type value;

  treap_node* left;
  treap_node* right;

  treap_node(key_type _key, value_type _value): key(_key), value(_value) {
    srand((unsigned)time(NULL));
    fix = rand() % std::numeric_limits<size_t>::max();
    left = nullptr;
    right = nullptr;
  }
  size_t getFix() { return fix; }
private:
  size_t fix;
};

template<typename K, typename V = int>
class treap {
protected:
  typedef K key_type;
  typedef V value_type;
  typedef treap_node<key_type, value_type> Node;
  typedef Node* pNode;
public:
  treap();
  treap(key_type _key, value_type _value = 0);
  treap(std::initializer_list<key_type> il);
  treap(std::initializer_list<std::pair<key_type, value_type>> ils);
private:
  pNode root;
};

}


#endif
