#include <wordpattern.h>

char& WordPattern::letter(int index) {
    return *d_letters[index];
}

bool WordPattern::setWord(std::string word) {
    for ( const auto &mapPair : d_orthogonalMap ) {
        int index = mapPair.first;
        if ( letter(index) != ' ' ) {
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

bool WordPattern::updateOrthogonalLetters(int index, char letter) {
    return true;
}

int WordPatternHorizontal::getCoor(int index, int orthogonalOffset) {
    return d_height * (d_row + orthogonalOffset) + d_col + index;
}

int WordPatternHorizontal::getIndex(int coor) {
    return coor % d_width - d_col;
}

int WordPatternVertical::getCoor(int index, int orthogonalOffset) {
    return d_height * (d_row + index) + d_col + orthogonalOffset;
}

int WordPatternVertical::getIndex(int coor) {
    return coor / d_width - d_row;
}
