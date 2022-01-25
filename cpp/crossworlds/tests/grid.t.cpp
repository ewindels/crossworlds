#include <gtest/gtest.h>
#include <grid.h>
#include <unordered_set>


TEST(Grid, Init) {
    Grid grid(3, 3);
    ASSERT_EQ(grid.height(), 3);
}

TEST(Grid, SetAndRead) {
    Grid grid(3, 3);
    grid.letter(3) = 'A';
    ASSERT_EQ(grid.letter(3), 'A');
}
