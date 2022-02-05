#ifndef WORDPATTERN
#define WORDPATTERN

#include <map>
#include <set>
#include <vector>
#include <unordered_set>
#include <string>
#include <utility>
#include <grid.h>
#include <vocabulary.h>

class WordPattern {
    public:
        template<std::size_t h, std::size_t w>
        WordPattern(int row, int col, int length, Grid<h,w>& grid, Vocabulary& vocabulary);

        virtual int getCoor(int index, int orthogonalOffset = 0) = 0;
        virtual int getIndex(int coor) = 0;
        char& letter(int index);
        bool setWord(std::string word);
        bool updateOrthogonalLetters(int index, char letter);

    protected:
        int d_row;
        int d_col;
        int d_height;
        int d_width;
        int d_length;
        std::vector<char*> d_letters;
        std::set<int> d_linkedLettersIndices;
        std::unordered_set<std::string> d_candidates;
        std::map<int, WordPattern*> d_orthogonalMap;
        std::string d_word;
        Vocabulary d_vocabulary;
};

template<std::size_t h, std::size_t w>
WordPattern::WordPattern(int        row,
                         int         col,
                         int         length,
                         Grid<h,w>&  grid,
                         Vocabulary& vocabulary)
: d_row(row),
  d_col(col),
  d_length(length),
  d_vocabulary(vocabulary),
  d_letters(length),
  d_height(h),
  d_width(w)
{
};

class WordPatternHorizontal : public WordPattern {
    public:
        template<std::size_t h, std::size_t w>
        WordPatternHorizontal(int row, int col, int length, Grid<h,w>& grid, Vocabulary& vocabulary);
        int getCoor(int index, int orthogonalOffset = 0) override;
        int getIndex(int coor) override;
};

template<std::size_t h, std::size_t w>
WordPatternHorizontal::WordPatternHorizontal(int         row,
                                             int         col,
                                             int         length,
                                             Grid<h,w>&  grid,
                                             Vocabulary& vocabulary)
: WordPattern(row, col, length, grid, vocabulary)
{
    int patternCoor = row * w + col;
    for ( int i = 0; i < length; i++ ) {
        d_letters[i] = &grid.letter(patternCoor + i);
    }
};

class WordPatternVertical : public WordPattern {
    public:
        template<std::size_t h, std::size_t w>
        WordPatternVertical(int row, int col, int length, Grid<h,w>& grid, Vocabulary& vocabulary);
        int getCoor(int index, int orthogonalOffset = 0) override;
        int getIndex(int coor) override;
};

template<std::size_t h, std::size_t w>
WordPatternVertical::WordPatternVertical(int         row,
                                         int         col,
                                         int         length,
                                         Grid<h,w>&  grid,
                                         Vocabulary& vocabulary)
: WordPattern(row, col, length, grid, vocabulary)
{
    int patternCoor = row * w + col;
    for ( int i = 0; i < length; i++ ) {
        d_letters[i] = &grid.letter(patternCoor + i * w);
    }
};

class OrthogonalPattern {
    protected:
        WordPattern* d_pattern;
        int d_crossedIndex;

};

#endif
