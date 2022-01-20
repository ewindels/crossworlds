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

TEST(WordPattern, GetIndex) {
    Grid grid(2, 2);
    WordPatternVertical wordPatternV(0, 1, 2, grid);
    WordPatternHorizontal wordPatternH(1, 0, 2, grid);
    ASSERT_EQ(wordPatternV.getIndex(1), 0);
    ASSERT_EQ(wordPatternV.getIndex(3), 1);
    ASSERT_EQ(wordPatternH.getIndex(2), 0);
    ASSERT_EQ(wordPatternH.getIndex(3), 1);
}
