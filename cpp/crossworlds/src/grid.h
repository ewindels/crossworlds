#ifndef GRID
#define GRID

#include <map>
#include "lookup.h"

class Grid {
    public:
        Grid(int height, int width);

        int height() const;
        int width() const;
        char& letter(int coor);

    private:
        int d_height;
        int d_width;
        char* d_letters_p;
};

#endif
