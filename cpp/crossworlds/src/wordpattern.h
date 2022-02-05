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
    WordPattern(const int         row,
                const int         col,
                const int         length,
                Grid<h,w>&  grid,
                const Vocabulary& vocabulary);

    virtual int getCoor(const int index,
                        const int orthogonalOffset = 0) = 0;
    virtual int getIndex(const int coor) = 0;
    const char& getLetter(const int index);
    void setLetter(const int  index,
                    const char letter);
    bool setWord(const std::string& word);
    bool updateOrthogonalLetters(const int   index,
                                    const char& letter);

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
WordPattern::WordPattern(const int         row,
                         const int         col,
                         const int         length,
                         Grid<h,w>&  grid,
                         const Vocabulary& vocabulary)
: d_row(row)
, d_col(col)
, d_length(length)
, d_vocabulary(vocabulary)
, d_letters(length)
, d_height(h)
, d_width(w)
{
};

class WordPatternHorizontal : public WordPattern
{
  public:
    template<std::size_t h, std::size_t w>
    WordPatternHorizontal(const int         row,
                            const int         col,
                            const int         length,
                            Grid<h,w>&        grid,
                            const Vocabulary& vocabulary);
    int getCoor(const int index,
                const int orthogonalOffset = 0) override;
    int getIndex(const int coor) override;
};

template<std::size_t h, std::size_t w>
WordPatternHorizontal::WordPatternHorizontal(const int         row,
                                             const int         col,
                                             const int         length,
                                             Grid<h,w>&         grid,
                                             const Vocabulary& vocabulary)
: WordPattern(row, col, length, grid, vocabulary)
{
    int patternCoor = row * w + col;
    for ( int i = 0; i < length; i++ ) {
        d_letters[i] = &grid.getLetter(patternCoor + i);
    }
};

class WordPatternVertical : public WordPattern
{
  public:
    template<std::size_t h, std::size_t w>
    WordPatternVertical(const int         row,
                        const int         col,
                        const int         length,
                        Grid<h,w>&        grid,
                        const Vocabulary& vocabulary);
    int getCoor(const int index,
                const int orthogonalOffset = 0) override;
    int getIndex(const int coor) override;
};

template<std::size_t h, std::size_t w>
WordPatternVertical::WordPatternVertical(const int         row,
                                         const int         col,
                                         const int         length,
                                         Grid<h,w>&        grid,
                                         const Vocabulary& vocabulary)
: WordPattern(row, col, length, grid, vocabulary)
{
    int patternCoor = row * w + col;
    for ( int i = 0; i < length; i++ ) {
        d_letters[i] = &grid.getLetter(patternCoor + i * w);
    }
};

class OrthogonalPattern
{
  protected:
    WordPattern* d_pattern;
    int d_crossedIndex;

};

#endif
