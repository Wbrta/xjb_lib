#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

ll euler(ll n) {
	ll ans = n;  
    for (ll i = 2; i * i <= n; ++i) {  
        if (n % i == 0) {  
            ans -= ans / i;  
            while (n % i == 0)  
                n /= i;  
        }
    }
    if (n > 1) ans -= ans / n;  
    return ans;  
}

ll fast(ll n, ll times, ll mod) {
	ll ans = 1;
	while (times) {
		if (times & 1) ans = (ans * n) % mod;
		n = (n * n) % mod;
		times >>= 1;
	}
	return ans;
}

int main() {
	int a = 1139;
	int b = 488;
	int c = 937;
	int p = 1e9 + 7;
	ll euler_p = euler(p);
	ll e2_p = euler(euler_p);
	ll ans = fast(a, fast(b, (c % e2_p) + e2_p, euler_p) + euler_p, p);
	cout << ans << endl;
	return 0;
}
