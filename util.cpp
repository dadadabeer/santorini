#include "util.h"

std::map<std::string, std::tuple<int, int>> DIRECTIONS = {
    {"n", std::make_tuple(-1, 0)},
    {"ne", std::make_tuple(-1, 1)},
    {"nw", std::make_tuple(-1, -1)},
    {"s", std::make_tuple(1, 0)},
    {"se", std::make_tuple(1, 1)},
    {"sw", std::make_tuple(1, -1)},
    {"e", std::make_tuple(0, 1)},
    {"w", std::make_tuple(0, -1)}
};