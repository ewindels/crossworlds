#ifndef WORDPATTERN
#define WORDPATTERN

#include <map>
#include <set>
#include <vector>
#include <unordered_set>
#include <string>
#include <utility>
#include <grid.h>

class WordPattern {
    public:
        WordPattern(int row, int col, int length, Grid& grid);

        virtual int getCoor(int index, int orthogonalOffset = 0) = 0;
        virtual int getIndex(int coor) = 0;
        char& letter(int index);
        bool setWord(std::string word);
        bool updateOrthogonalLetters(int index, char letter);

    protected:
        int d_row;
        int d_col;
        int d_length;
        std::vector<char> d_letters;
        std::set<int> d_linkedLettersIndices;
        std::unordered_set<std::string> d_candidates;
        std::map<int, WordPattern*> d_orthogonalMap;
        Grid d_grid;
};

class WordPatternHorizontal : public WordPattern {
    public:
        using WordPattern::WordPattern;
        int getCoor(int index, int orthogonalOffset = 0) override;
        int getIndex(int coor) override;
};

class WordPatternVertical : public WordPattern {
    public:
        using WordPattern::WordPattern;
        int getCoor(int index, int orthogonalOffset = 0) override;
        int getIndex(int coor) override;
};

#endif
