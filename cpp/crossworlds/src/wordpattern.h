#ifndef WORDPATTERN
#define WORDPATTERN

#include <map>
#include <set>
#include <unordered_set>
#include <string>
#include <utility>
#include <grid.h>

class WordPattern {
    public:
        WordPattern(int row, int col, int length, Grid& grid);

        virtual int getCoor(int index, int orthogonalOffset = 0) = 0;
        char& letter(int index);
        void setWord(std::string word);

    protected:
        int d_row;
        int d_col;
        int d_length;
        std::set<int> d_lettersIndices;
        std::set<int> d_linkedLettersIndices;
        std::unordered_set<std::string> d_candidates;
        Grid d_grid;
};

class WordPatternHorizontal : public WordPattern {
    public:
        using WordPattern::WordPattern;
        int getCoor(int index, int orthogonalOffset = 0);
};

class WordPatternVertical : public WordPattern {
    public:
    using WordPattern::WordPattern;
        int getCoor(int index, int orthogonalOffset = 0);
};

#endif
