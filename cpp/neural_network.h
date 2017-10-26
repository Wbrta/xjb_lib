#ifndef HEAD_NEURAL_NETWORK_H
#define HEAD_NEURAL_NETWORK_H

#include <cmath>
#include <vector>

/**
 * This neural network is three-layer Back-Propagation network.
 * It can be specify the hidden layer size.
 */
class NeuralNetwork {
public:
  NeuralNetwork();
  virtual ~NeuralNetwork();

  
private:
  double sigmod(double x);
  double tanh(double x);
  
  std::vector<double> input, hidden, output;
  std::vector<std::vector<double>> w1, w2; // w1 is weight of input and hidden, 
};

double NeuralNetwork::sigmod(double x) {
  double ans = 1;
  ans /= (1.0 + exp(-x));
  return ans;
}
#endif
