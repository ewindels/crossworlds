#include <vocabulary.h>

void Vocabulary::addUsedWord(const std::string& word) {
    d_usedWords.insert(word);
};

bool Vocabulary::hasUsedWord(const std::string& word) {
    return d_usedWords.find(word) != d_usedWords.end();
};

void Vocabulary::removeUsedWord(const std::string& word) {
    d_usedWords.erase(word);
};

LookUp::LookUp(std::unordered_set<std::string> vocabulary) {
    setLookups(vocabulary);
}

void LookUp::setLookups(std::unordered_set<std::string> vocabulary) {
    for (std::string const& word : vocabulary) {
        d_lengthLookup[word.size()].insert(word);
        int i = 0;
        for (char const& letter : word) {
            d_lettersIndicesLookup[std::make_pair(i, letter)].insert(word);
            i++;
        }
    }
}

std::unordered_set<std::string> LookUp::lookupLength(int length) {
    return d_lengthLookup[length];
}

std::unordered_set<std::string> LookUp::lookupLetterIndex(int index, char letter) {
    return d_lettersIndicesLookup[std::make_pair(index, letter)];
}
