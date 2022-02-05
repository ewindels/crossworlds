#ifndef GRID
#define GRID

#include <set>
#include <string>
#include <cstddef>

template<std::size_t h, std::size_t w>
class Grid
{
public:
    Grid();

    int height() const;
    int width() const;
    char& letter(int coor);

private:
    int d_height;
    int d_width;
    char d_letters[h*w] = { ' ' };
};

template<std::size_t h, std::size_t w>
Grid<h,w>::Grid()
: d_height(h),
  d_width(w)
{
}

template<std::size_t h, std::size_t w>
int Grid<h,w>::height() const
{
    return d_height;
}

template<std::size_t h, std::size_t w>
int Grid<h,w>::width() const
{
    return d_width;
}

template<std::size_t h, std::size_t w>
char& Grid<h,w>::letter(int coor) {
    return d_letters[coor];
}

#endif
