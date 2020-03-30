test:
	@$(MAKE) -sk test-all

test-all:	test-scripts test-hulk test-quiz

test-scripts:
	curl -sLO https://gitlab.com/nd-cse-20289-sp20/cse-20289-sp20-assignments/raw/master/homework06/test_hulk.sh
	curl -sLO https://gitlab.com/nd-cse-20289-sp20/cse-20289-sp20-assignments/raw/master/homework06/hulk_test.py
	curl -sLO https://gitlab.com/nd-cse-20289-sp20/cse-20289-sp20-assignments/raw/master/homework06/hashes.txt
	curl -sLO https://gitlab.com/nd-cse-20289-sp20/cse-20289-sp20-assignments/raw/master/homework06/test_quiz.py
	chmod +x test_hulk.sh hulk_test.py test_quiz.py

test-hulk:
	./test_hulk.sh

test-quiz:
	./test_quiz.py
