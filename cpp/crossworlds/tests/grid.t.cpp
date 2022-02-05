#include <gtest/gtest.h>
#include <grid.h>
#include <unordered_set>

class GridTest : public ::testing::Test {
    public:
        Grid<3,3> grid;
};

TEST_F(GridTest, Init) {
    ASSERT_EQ(grid.height(), 3);
}

TEST_F(GridTest, SetAndRead) {
    grid.letter(3) = 'A';
    ASSERT_EQ(grid.letter(3), 'A');
}
