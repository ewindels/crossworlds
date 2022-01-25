#ifndef GRID
#define GRID

#include <lookup.h>
#include <set>
#include <string>

class Grid {
    public:
        Grid(int height, int width);

        int height() const;
        int width() const;
        char& letter(int coor);
        void addUsedWord(const std::string& word);
        bool hasUsedWord(const std::string& word);
        void removeUsedWord(const std::string& word);

    private:
        int d_height;
        int d_width;
        char* d_letters_p;
        std::set<std::string> d_usedWords;
};

#endif
