#ifndef SKIP_LIST_H
#define SKIP_LIST_H

#include <stddef.h>
#include <stdlib.h>

template<typename K, typename V = int>
struct skip_list_node {
  K key;
  V value;
  size_t level;
  skip_list_node* forward[1];
};

template<typename K, typename V = int>
class skip_list {
protected:
  typedef K key_type;
  typedef V value_type;
  typedef skip_list_node<K, V> Node;
  typedef Node* pNode;

  #define NPOS static_cast<pNode>(nullptr)
public:
  skip_list(int max_level = 15);
  ~skip_list();
  
  bool insert(key_type key);
  bool insert(key_type key, value_type value);
  
  bool erase(key_type key);
  bool erase_once(key_type key);
  
  bool exist(key_type key);

  pNode find(key_type key);
private:
  pNode start;
  pNode finish;

  const size_t MAX_LEVEL;
  
  int random_level();
  pNode new_node(K key, V value);
};

template<typename K, typename V>
skip_list<K, V>::skip_list(int max_level) : MAX_LEVEL(max_level) {
  start = (pNode)malloc(sizeof(Node) + MAX_LEVEL * sizeof(pNode));
  finish = (pNode)malloc(sizeof(Node) + MAX_LEVEL * sizeof(pNode));
  for (int i = 0; i < MAX_LEVEL; ++i)
    start->forward[i] = NPOS;
  for (int i = 0; i < MAX_LEVEL; ++i)
    finish->forward[i] = NPOS;
}

template<typename K, typename V>
skip_list<K, V>::~skip_list() {
  pNode node = start->forward[0];
  while (node != finish) {
    pNode &tmp = node->forward[0];
    free(node);
    node = tmp;
  }
  free(start);
  free(finish);
}

template<typename K, typename V>
bool skip_list<K, V>::insert(key_type key) {
  return insert(key, value_type(0));
}

template<typename K, typename V>
bool skip_list<K, V>::insert(key_type key, value_type value) {
  pNode* update = new pNode[MAX_LEVEL];
  for (int i = 0; i < MAX_LEVEL; ++i) {
    pNode node = start;
    while (node->forward[i] != finish && node->forward[i]->key < key) 
      node = node->forward[i];
    update[i] = &node;
  }
  
  pNode node = new_node(key, value);
  if (node == NPOS) {
    delete[] update;
    return false;
  }

  for (int i = 0; i < MAX_LEVEL; ++i) {
    node->forward[i] = (*update[i])->forward[i];
    (*update[i])->forward[i] = node;
  }

  delete[] update;
  return true;
}

template<typename K, typename V>
bool skip_list<K, V>::erase(key_type key) {
  bool is_success = erase_once(key);
  while (is_success && erase_once(key));
  return is_success;
}

template<typename K, typename V>
bool skip_list<K, V>::erase_once(key_type key) {
  
}

template<typename K, typename V>
bool skip_list<K, V>::exist(key_type key) {
  if (find(key) == NPOS) return false;
  else return true;
}

template<typename K, typename V>
typename skip_list<K, V>::pNode skip_list<K, V>::find(key_type key) {
  size_t level_now = MAX_LEVEL;
  pNode target_node = start->forward[level_now - 1];
  while (target_node < finish) {
    if (level_now - 1 < 0) {
      target_node = NPOS;
      break;
    }
    if (target_node->forward[level_now - 1]->key == key) {
      target_node = target_node->forward[level_now - 1];
      break;
    } else if (target_node->forward[level_now - 1]->key < key) {
      target_node = target_node->forward[level_now - 1];
    } else {
      level_now -= 1;
    }
  }
  if (target_node >= finish) target_node = NPOS;
  return target_node;
}

template<typename K, typename V>
int skip_list<K, V>::random_level() {
  int level = 1;
  while (rand() % 2) ++level;
  level = (level <= MAX_LEVEL ? level : MAX_LEVEL);
  return level;
}

template<typename K, typename V>
typename skip_list<K, V>::pNode skip_list<K, V>::new_node(K key, V value) {
  int level = random_level();
  pNode node = (pNode)malloc(sizeof(Node) + level * sizeof(pNode));
  node->key = key;
  node->value = value;
  node->level = level;
  return node;
}

#endif
