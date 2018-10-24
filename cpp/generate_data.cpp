#include <bits/stdc++.h>
using namespace std;

int main(int argc, char **argv) {
  if (argc < 3) {
    cout << "Usage: " << argv[0] << " [content] [size of output file] {output file path}" << endl;
    return 1;
  }
  string content(argv[1]);
  string path = "";
  int size_of_output_file = atoi(argv[2]);
  int times = size_of_output_file / content.size(); // the times of how to generate the size of output file by print content
  
  if (argc == 4) {
    path += argv[3];
  } else {
    path += "output";
  }
  ofstream out(path);
  while (times--) {
    out << content;
  }
  out.close();
  return 0;
}
