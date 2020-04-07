CC=		gcc
CFLAGS=		-g -Wall -std=gnu99 -fPIC
LD=		gcc
LDFLAGS=	-L.
AR=		ar
ARFLAGS=	rcs

TARGETS=	libstr.a \
		libstr.so

all:		$(TARGETS)

test:
	@$(MAKE) -sk test-all

test-all:	test-libstr test-str test-quiz

test-libstr:	libstr.so
	curl -sLO https://gitlab.com/nd-cse-20289-sp20/cse-20289-sp20-assignments/raw/master/homework08/test_libstr.py
	chmod +x test_libstr.py
	./test_libstr.py -v

test-str:	str-static str-dynamic
	curl -sLO https://gitlab.com/nd-cse-20289-sp20/cse-20289-sp20-assignments/raw/master/homework08/test_str.sh
	chmod +x test_str.sh
	./test_str.sh

test-quiz:	answers.json
	curl -sLO https://gitlab.com/nd-cse-20289-sp20/cse-20289-sp20-assignments/raw/master/homework08/test_quiz.py
	chmod +x test_quiz.py
	./test_quiz.py

clean:
	rm -f $(TARGETS) *.o


library.o:   library.c
	$(CC) $(CFLAGS) -c -o $@ $^

main.o: main.c
	$(CC) $(CFLAGS) -c -o $@ $^

libstr.so:   library.o
	$(CC) $(LDFLAGS) -fPIC -shared -o  $@ $^

str-dynamic: main.o libstr.so
		$(CC) $(LDFLAGS) -o $@ $< -lstr

libstr.a: library.o
	$(AR) $(ARFLAGS)  $@ $^


str-static: main.o libstr.a
	$(CC) $(LDFLAGS) -o -static $@ $< -lstr
