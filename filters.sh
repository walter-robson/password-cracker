#!/bin/bash

q1_answer() {
    # TODO: List only the first five last names in sorted order
    curl -sL https://yld.me/raw/Hk1 | cut -d ',' -f 2 | sort | head -n 5
}

q2_answer() {
    # TODO: Count how many phone numbers end in an even number
    curl -sL https://yld.me/raw/Hk1 | cut -d ',' -f 4 | grep '[24680]$' | wc -l
}

q3_answer() {
    # TODO: List the first names that contain two consecutive repeated letters
    curl -sL https://yld.me/raw/Hk1 | cut -d ',' -f 3 | grep -E '(.)\1'
}

q4_answer() {
    # TODO: Count all the netids that contain no numbers
    curl -sL https://yld.me/raw/Hk1 | cut -d ',' -f 1 | grep -Eo '[^1234567890]*$' | wc -l
}

q5_answer() {
    # TODO: List all the netids that contain all of the last name
    curl -sL https://yld.me/raw/Hk1
}

q6_answer() {
    # TODO: List the first names of people who have both two consecutive
    # repeated letters in their netid and two consecutive repeated numbers in
    # their phone number
    curl -sL https://yld.me/raw/Hk1 | cut -d ',' -f 1,3,4 | grep -E '(.)\1' | head -n 2 | cut -d ',' -f 2

}
