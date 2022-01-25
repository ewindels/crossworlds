#include <grid.h>

Grid::Grid(int height, int width)
: d_height(height),
  d_width(width),
  d_letters_p(new char[height * width])
{
}

int Grid::height() const
{
    return d_height;
}

int Grid::width() const
{
    return d_width;
}

char& Grid::letter(int coor) {
    return d_letters_p[coor];
}

void Grid::addUsedWord(const std::string& word) {
    d_usedWords.insert(word)
};

bool Grid::hasUsedWord(const std::string& word) {

};

void Grid::removeUsedWord(const std::string& word) {

};
