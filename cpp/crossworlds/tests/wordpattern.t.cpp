#include <gtest/gtest.h>
#include <wordpattern.h>
#include <unordered_set>

class WordPatternTest : public ::testing::Test
{
  public:
    Grid<2,2> grid;
    Vocabulary vocabulary;
    WordPatternVertical wordPatternV;
    WordPatternHorizontal wordPatternH;

    WordPatternTest()
    : wordPatternV(0, 1, 2, grid, vocabulary)
    , wordPatternH(1, 0, 2, grid, vocabulary)
    {
    }
};

TEST_F(WordPatternTest, GetCoor)
{
    ASSERT_EQ(wordPatternV.getCoor(0), 1);
    ASSERT_EQ(wordPatternV.getCoor(1, -1), 2);
    ASSERT_EQ(wordPatternH.getCoor(0), 2);
    ASSERT_EQ(wordPatternH.getCoor(1, -1), 1);
}

TEST_F(WordPatternTest, SetAndReadLetter)
{
    wordPatternV.setLetter(0, 'A');
    ASSERT_EQ(grid.getLetter(1), 'A');
    wordPatternV.setLetter(0, 'B');
    ASSERT_EQ(grid.getLetter(1), 'B');
}

TEST_F(WordPatternTest, GetIndex)
{
    ASSERT_EQ(wordPatternV.getIndex(1), 0);
    ASSERT_EQ(wordPatternV.getIndex(3), 1);
    ASSERT_EQ(wordPatternH.getIndex(2), 0);
    ASSERT_EQ(wordPatternH.getIndex(3), 1);
}
