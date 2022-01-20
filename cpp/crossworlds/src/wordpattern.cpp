#include <wordpattern.h>

WordPattern::WordPattern(int row, int col, int length, Grid& grid)
: d_row(row),
  d_col(col),
  d_length(length),
  d_grid(grid)
{
}

char& WordPattern::letter(int index) {
    return d_grid.letter(getCoor(index));
}

bool WordPattern::setWord(std::string word) {
    for ( const auto &mapPair : d_orthogonalMap ) {
        int index = mapPair.first;
        if ( d_orthogonalMap.find(index) != d_orthogonalMap.end() ) {
            if ( !updateOrthogonalLetters(index, word[index]) ) {
                return false;
            };
        };
    };
    return true;
}

bool WordPattern::updateOrthogonalLetters(int index, char letter) {
    return true;
}

int WordPatternHorizontal::getCoor(int index, int orthogonalOffset) {
    return d_grid.height() * (d_row + orthogonalOffset) + d_col + index;
}

int WordPatternHorizontal::getIndex(int coor) {
    return coor % d_grid.width() - d_col;
}

int WordPatternVertical::getCoor(int index, int orthogonalOffset) {
    return d_grid.height() * (d_row + index) + d_col + orthogonalOffset;
}

int WordPatternVertical::getIndex(int coor) {
    return coor / d_grid.width() - d_row;
}
