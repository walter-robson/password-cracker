#!/bin/bash

q1_answer() {
    # TODO: List only the names of the turtles in sorted order.
    curl -sL https://yld.me/raw/lE8 | grep -E '[A-Z]' | sed -e 's/:.*//' | sort
}

q2_answer() {
    # TODO: List only the colors of the turtles in all capitals.
    curl -sL https://yld.me/raw/lE8 | grep -Eo ':.*:' | sed -e 's/://' | sed -s 's/://' | tr 'a-z' 'A-Z'
}

q3_answer() {
    # TODO: Replace all weapons with plowshares
    curl -sL https://yld.me/raw/lE8 | sed -E 's/(:.*:).*/\1plowshare/'
}

q4_answer() {
    # TODO: List only the turtles whose names end in lo.
    curl -sL https://yld.me/raw/lE8 | grep -Eo '[A-Z].*lo'
}

q5_answer() {
    # TODO: List only the turtles with names that have two consecutive vowels.
    curl -sL https://yld.me/raw/lE8 | grep -Eo '.*[aeiou][aeiou].*:' | sed -e 's/:.*//'
}

q6_answer() {
    # TODO: Count how many colors don't begin with a vowel
    curl -sL https://yld.me/raw/lE8 | grep -E ':[^aeiou].*:' | wc -l
}

q7_answer() {
    # TODO: List only the turtles names whose name ends with a vowel and whose weapon ends with a vowel.
    curl -sL https://yld.me/raw/lE8 | grep -E '.*[aeiou]:.*:.*[aeiou]$' | cut -d : -f1
}

q8_answer() {
    # TODO: List only the turtles names with two of the same consecutive letter (i.e. aa, bb, etc.)
    curl -sL https://yld.me/raw/lE8 | grep -E '([a-z])\1' | cut -d : -f2
}
