all: build

clean:
	rm -fr plotaudio.bin

.PHONY: build
build: plotaudio.bin

plotaudio.bin: main.cpp $(shell ls *.h)
	g++ $(CXXFLAGS) -o $@ $< $(LIBS) $(IMAGEMAGICK_FLAGS)

CONFIGURATION ?= RELEASE
DEBUG_CXXFLAGS = -ggdb -DDEBUG
RELEASE_CXXFLAGS = -O3
COMMON_CXXFLAGS = -std=gnu++0x -Werror -Wall
CXXFLAGS = $(COMMON_CXXFLAGS) $($(CONFIGURATION)_CXXFLAGS)
IMAGEMAGICK_FLAGS = $(shell Magick++-config --cppflags --cxxflags --ldflags --libs)
LIBS = -lboost_system-mt -lboost_program_options-mt -lsndfile
