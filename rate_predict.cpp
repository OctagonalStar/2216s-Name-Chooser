#include <iostream>
#include <cmath>
#include <map>
#include <tuple>

using namespace std;
unsigned int all = 0;


bool is_input_allow(unsigned int ac, unsigned int rp){
    if(all && rp <= ac && ac < all){
        return true;
    }
    return false;
}


[[maybe_unused]] double no_improve(){
    return 1/(double)all;
}


[[maybe_unused]] double delete_improve(int ac, int rp){
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


double decrease_improve(double ac, double rp, map<tuple<int, int>, double> *cache){
    if(rp > ac){
        return 0;
    }
    if(ac == 0 && rp == 0){
        return 1/(double)all;
    }
    if(cache->count(make_tuple((int)ac, (int)rp))) {
        return cache->at(make_tuple((int)ac, (int)rp));
    }
    if(rp == 0){
        cache->insert(pair<tuple<int, int>, double> (make_tuple((int)ac, (int)rp),
                                                     decrease_improve(ac - 1, rp, cache)+
                                                     pow((1/(double)all), ac)*(1-(((double)all - 1)/pow(((double)all), ac)))));
        return cache->at(make_tuple((int)ac, (int)rp));
    }
    cache->insert(pair<tuple<int, int>, double> (make_tuple((int)ac, (int)rp),decrease_improve(ac - 1, rp - 1, cache)*(1/(double)all) +
                                                 decrease_improve(ac - 1, rp, cache)+
            (ac - rp) * (pow((1/(double)all), ac)*(1-(((double)all - 1)/pow(((double)all), ac))))));
    return cache->at(make_tuple((int)ac, (int)rp));
}

int main(){
    unsigned int allChosen = 0;
    unsigned int repeatTimes = 0;
    map<tuple<int, int>, double> cache = {};
    cin >> allChosen >> repeatTimes >> all;
    while (!is_input_allow(allChosen, repeatTimes)) {
        cout << "请重新输入" << endl;
        cin >> allChosen >> repeatTimes >> all;
    }
    cout << decrease_improve(allChosen, repeatTimes, &cache) << endl;
    // for(auto it = cache.begin(); it != cache.end(); ++it){
    //     cout << "(" << get<0>(it->first) << "," << get<1>(it->first) << ")\t\t" << it->second << endl;
    // }
    return 0;
}