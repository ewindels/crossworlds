#include <vocabulary.h>

void Vocabulary::addUsedWord(const std::string& word)
{
    d_usedWords.insert(word);
}

bool Vocabulary::hasUsedWord(const std::string& word)
{
    return d_usedWords.find(word) != d_usedWords.end();
}

void Vocabulary::removeUsedWord(const std::string& word)
{
    d_usedWords.erase(word);
}

LookUp::LookUp(StringSet vocabulary)
{
    setLookups(vocabulary);
}

void LookUp::setLookups(StringSet vocabulary)
{
    for (std::string const& word : vocabulary) {
        d_lengthLookup[word.size()].insert(word);
        int i = 0;
        for (char const& letter : word) {
            d_lettersIndicesLookup[std::make_pair(i, letter)].insert(word);
            i++;
        }
    }
}

LookUp::StringSet LookUp::lookupLength(int length)
{
    return d_lengthLookup[length];
}

LookUp::StringSet LookUp::lookupLetterIndex(int  index,
                                            char letter)
{
    return d_lettersIndicesLookup[std::make_pair(index, letter)];
}
