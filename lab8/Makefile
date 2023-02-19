LDFLAGS=-L/home/lib -lcrypto
CFLAGS=-Wall -g -I/home/include

.PHONY: all
all: birthday

birthday: birthday.o
	gcc -o $@ $< $(LDFLAGS)

.PHONY: clean
clean:
	rm -vf *.o birthday
