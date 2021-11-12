#include "gtest/gtest.h"
#include "lookup.h"
#include <unordered_set>
#include <string>

TEST(LookUp, Init) {
    std::unordered_set<std::string> vocabulary { "FOO", "BAR" };
    LookUp lookup(vocabulary);
    ASSERT_EQ(lookup.lookupLength(3).size(), 2);
    ASSERT_EQ(lookup.lookupLength(10).size(), 0);
    ASSERT_EQ(lookup.lookupLetterIndex(0, 'F').size(), 1);
    ASSERT_EQ(lookup.lookupLetterIndex(0, 'A').size(), 0);
}

