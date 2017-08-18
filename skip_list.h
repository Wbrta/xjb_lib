#ifndef SKIP_LIST_H
#define SKIP_LIST_H

#include <stddef.h>
#include <stdlib.h>

template<typename K, typename V = int>
struct skip_list_node {
  K key;
  V value;
  skip_list_node* forward[1];
};

template<typename K, typename V = int>
class skip_list {
protected:
  typedef K key_type;
  typedef V value_type;
  typedef skip_list_node<K, V> Node;
  typedef Node* pNode;
public:
  skip_list(int max_level);
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
  
  void random_level();
};

template<typename K, typename V>
skip_list<K, V>::skip_list(int max_level) : MAX_LEVEL(max_level) {
  start = (pNode)malloc(sizeof(Node) + MAX_LEVEL * sizeof(pNode));
  finish = (pNode)malloc(sizeof(Node) + MAX_LEVEL * sizeof(pNode));
}

template<typename K, typename V>
skip_list<K, V>::~skip_list() {
  free(start);
  free(finish);
}

template<typename K, typename V>
bool skip_list<K, V>::insert(key_type key) {
  return insert(key, value_type(0));
}

template<typename K, typename V>
bool skip_list<K, V>::insert(key_type key, value_type value) {
  
}

template<typename K, typename V>
bool skip_list<K, V>::erase(key_type key) {

}

template<typename K, typename V>
bool skip_list<K, V>::erase_once(key_type key) {

}

template<typename K, typename V>
bool skip_list<K, V>::exist(key_type key) {

}

template<typename K, typename V>
typename skip_list<K, V>::pNode skip_list<K, V>::find(key_type key) {

}

template<typename K, typename V>
void skip_list<K, V>::random_level() {
  int level = 1;
  while (rand() % 2) ++level;
  level = (level <= MAX_LEVEL ? level : MAX_LEVEL);
  return level;
}

#endif
