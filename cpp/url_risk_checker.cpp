#include <iostream>
#include <string>
using namespace std;

int main() {

    string url;

    cout << "Enter Website URL: ";
    cin >> url;

    int score = 0;

    if (url.find("http://") == 0)
        score += 20;

    if (url.find("@") != string::npos)
        score += 25;

    if (url.find("login") != string::npos ||
        url.find("password") != string::npos)
        score += 15;

    cout << "\nTrustShield C++ Scanner\n";

    cout << "Risk Score: " << score << "/100\n";

    if (score >= 50)
        cout << "High Risk";

    else if (score >= 20)
        cout << "Needs Caution";

    else
        cout << "Lower Risk";

    cout << "\nEducational demonstration only.\n";

    return 0;
}