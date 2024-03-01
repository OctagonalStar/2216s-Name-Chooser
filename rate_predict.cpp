#include<iostream>
#include <cmath>

using namespace std;
int all = 0;

bool is_input_allow(int ac, int rp){
    if(rp || ac || all){
        if(rp <= ac && ac < all){
            return true;
        }
    }
    return false;
}


double no_improve(int ac, int rp){
    return 1/(double)all;
}


double delete_improve(int ac, int rp){
    /*repeat in this turn
     *repeated => rete = 0
     *not repeated => rate = 1/lefts
     *lefts = all - ac
     */
    if(ac != rp){
        return 0;
    }
    return (1-((double)ac/(double)all))*(1/((double)all-(double)ac));
}


double decrease_improve(double ac, double rp){
    if(rp > ac){
        return 0;
    }
    if(ac == 0 && rp == 0){
        return 1/(double)all;
    }
    if(rp == 0){
        return decrease_improve(ac - 1, rp)+
               pow((1/(double)all), ac)*(1-(((double)all - 1)/pow(((double)all), ac)));
    }
    return decrease_improve(ac - 1, rp - 1)*(1/(double)all) +
           decrease_improve(ac - 1, rp)+
           pow((1/(double)all), ac)*(1-(((double)all - 1)/pow(((double)all), ac)));
}

int main(){
    int allChosen = 0;
    int repeatTimes = 0;
    cin >> allChosen >> repeatTimes >> all;
    while (!is_input_allow(allChosen, repeatTimes)) {
        cout << "请重新输入" << endl;
        cin >> allChosen >> repeatTimes >> all;
    }
    cout << decrease_improve(allChosen, repeatTimes) << endl;
    return 0;
}