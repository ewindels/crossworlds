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

void WordPattern::setWord(std::string word) {
}

int WordPatternHorizontal::getCoor(int index, int orthogonalOffset) {
    return d_grid.height() * (d_row + orthogonalOffset) + d_col + index;
}

int WordPatternVertical::getCoor(int index, int orthogonalOffset) {
    return d_grid.height() * (d_row + index) + d_col + orthogonalOffset;
}
