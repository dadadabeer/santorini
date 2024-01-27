// #ifndef UTIL_H
// #define UTIL_H

#include <tuple>
#include <map>
#include <vector>
#include <string>

extern std::map<std::string, std::tuple<int, int>> DIRECTIONS;

template <typename MapType>
std::vector<typename MapType::key_type> extractKeys(const MapType& map) {
    std::vector<typename MapType::key_type> keys;
    for (const auto& pair: map) {
        keys.push_back(pair.first);
    }
    return keys;
}

#endif


/* NOTES FOR SELF:
See how we defined DIRECTIONS with extern so we let the compiler know its already initaized somwgere else so don't do it again.
Normally we write the full functions in .cpp but for template functions its a bit diff. We keep them
in the .h file so that it have access to the template and can instantiate it with the necessary types.
*/