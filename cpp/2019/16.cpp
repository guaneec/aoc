#include <fstream>
#include <iostream>
#include <vector>
#include <cmath>

using std::vector;

template <typename T>
void show(std::vector<T> v) {
    for(auto i: v) {
        std::cout << i;
    }    
    std::cout << std::endl;
}

vector<int> fft(const vector<int> &v) {
    auto n = v.size();
    vector<int> rets(n, 0);
    vector<int> sums(n);
    for (int i = n-1; i >= 0; --i) {
        if (i == n-1) {
            sums[i] = v[i];
        } else {
            sums[i] = sums[i+1] + v[i];
        }
    }
    vector<int> signs{1, 1, -1, -1};
    for (int m = 1; m <= n; ++m) {
        auto sign = signs[m%4];
        for (int i = 0; i <= n / m; ++i) {
            rets[i-1] += sign * sums[i*m-1];
        }
    }
    for (auto& r: rets) {
        r = std::abs(r) % 10;
    }
    
    return rets;
}

int main() {
    std::ifstream f("../../data/2019/16.input.txt");
    vector<int> a;
    while(f) {
        int i = f.get() - '0';
        if (0 <= i && i <= 9) a.push_back(i);
    }
    a.reserve(a.size() * 10000);
    int n = a.size();
    for (int i = 1; i < 10000; ++i) {
        a.insert(a.end(), a.begin(), a.begin() + n);
    }
    int offset = 0;
    for (int i = 0; i < 7; ++i) {
        offset = offset * 10 + a[i];
    }
    std::cout << a.size() << " | ";
    for (int i = 0; i < 8; ++i) {
        std::cout << a[i+offset];
    }
    std::cout << '\n';
    for (int i = 0; i < 100; ++i) {
        std::cout << i << '\n';
        a = fft(a);
    }
    std::cout << a.size() << " | ";
    for (int i = 0; i < 8; ++i) {
        std::cout << a[i+offset];
    }
}
