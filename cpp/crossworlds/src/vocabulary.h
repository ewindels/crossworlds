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
};

class LookUp
{
    using StringSet = std::unordered_set<std::string>;

  public:
    LookUp(StringSet vocabulary);
    void setLookups(StringSet vocabulary);

    StringSet lookupLength(int length);
    StringSet lookupLetterIndex(int  index,
                                char letter);

  private:
    std::map<std::pair<int, char>, StringSet> d_lettersIndicesLookup;
    std::unordered_map<int, StringSet> d_lengthLookup;
};

#endif
