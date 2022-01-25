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
        std::set<std::string>& usedWords();

    private:
        int d_height;
        int d_width;
        char* d_letters_p;
        std::set<std::string> d_usedWords;
};

#endif
