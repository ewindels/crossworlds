#ifndef VOCABULARY
#define VOCABULARY

#include <unordered_set>
#include <set>
#include <vector>
#include <utility>
#include <string>
#include <unordered_map>
#include <map>

class Vocabulary
{
    public:
        void addUsedWord(const std::string& word);
        bool hasUsedWord(const std::string& word);
        void removeUsedWord(const std::string& word);

    private:
        std::set<std::string> d_usedWords;
        std::vector<int> d_cacheFactor;
};

class LookUp
{
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
