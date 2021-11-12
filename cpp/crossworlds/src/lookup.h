#ifndef LOOKUP
#define LOOKUP

#include <unordered_set>
#include <utility>
#include <string>
#include <unordered_map>
#include <map>

class LookUp {
    public:
        LookUp(std::unordered_set<std::string> vocabulary);
        void setLookups(std::unordered_set<std::string> vocabulary);

        std::unordered_set<std::string> lookupLength(int length);
        std::unordered_set<std::string> lookupLetterIndex(int index, char letter);

    private:
        std::map<std::pair<int, char>, std::unordered_set<std::string>> d_lettersIndicesLookup;
        std::unordered_map<int, std::unordered_set<std::string>> d_lengthLookup;
};

#endif
