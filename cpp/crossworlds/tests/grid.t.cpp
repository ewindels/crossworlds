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

TEST(Grid, SetAddandRemoved) {
    Grid grid(3, 3);
    grid.addUsedWord("foo");
    grid.addUsedWord("bar");
    ASSERT_TRUE(grid.hasUsedWord("foo"));
    ASSERT_FALSE(grid.hasUsedWord("test"));
    grid.removeUsedWord("foo");
    ASSERT_FALSE(grid.hasUsedWord("foo"));
}