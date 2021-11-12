#include "gtest/gtest.h"
#include <wordpattern.h>
#include <unordered_set>


TEST(WordPattern, GetCoor) {
    Grid grid(2, 2);
    WordPatternVertical wordPattern(0, 1, 2, grid);
    ASSERT_EQ(wordPattern.getCoor(0), 1);
    ASSERT_EQ(wordPattern.getCoor(1, -1), 2);
}

TEST(WordPattern, SetAndReadLetter) {
    Grid grid(2, 2);
    WordPatternVertical wordPattern(0, 1, 2, grid);
    wordPattern.letter(0) = 'A';
    ASSERT_EQ(grid.letter(1), 'A');
}

