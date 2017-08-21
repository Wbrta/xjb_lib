#include "skip_list.h"

int main() {
  skip_list<int> sl;
  sl.insert(10);
  sl.insert(2);
  sl.insert(10);
  sl.insert(20);
  sl.insert(25);
  sl.show();
  sl.erase(10);
  sl.show();
  return 0;
}
