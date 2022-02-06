#include <wordpattern.h>
#include <cmath>

const char& WordPattern::getLetter(const int index)
{
    return *d_letters[index];
}

void WordPattern::setLetter(const int  index,
                            const char letter)
{
    *d_letters[index] = letter;
}

bool WordPattern::setWord(const std::string& word)
{
    for ( const auto &mapPair : d_orthogonalMap ) {
        int index = mapPair.first;
        if ( getLetter(index) != ' ' ) {
            if ( !updateOrthogonalLetters(index, word[index]) ) {
                return false;
            }
            d_linkedLettersIndices.insert(index);
        };
    };
    d_vocabulary.addUsedWord(word);
    d_word = word;
    return true;
}

bool WordPattern::updateOrthogonalLetters(const int   index,
                                          const char& letter)
{
    OrthogonalPattern orthogonalPattern = d_orthogonalMap[index];
    orthogonalPattern.updateCandidates(letter);
    return false;
}

int WordPatternHorizontal::getCoor(const int index,
                                   const int orthogonalOffset)
{
    return d_height * (d_row + orthogonalOffset) + d_col + index;
}

int WordPatternHorizontal::getIndex(const int coor) {
    return coor % d_width - d_col;
}

int WordPatternVertical::getCoor(const int index,
                                 const int orthogonalOffset)
{
    return d_height * (d_row + index) + d_col + orthogonalOffset;
}

int WordPatternVertical::getIndex(const int coor) {
    return coor / d_width - d_row;
}

WordPattern* OrthogonalPattern::pattern()
{
    return d_pattern_p;
}

int OrthogonalPattern::index()
{
    return d_index;
}

void OrthogonalPattern::updateCandidates(char letter)
{
    d_pattern_p->d_strRepr[d_index] = letter;
}
