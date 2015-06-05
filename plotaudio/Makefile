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
MAGICKPP_CONFIG = /usr/lib/x86_64-linux-gnu/ImageMagick-6.8.9/bin-Q16/Magick++-config
IMAGEMAGICK_FLAGS = $(shell $(MAGICKPP_CONFIG) --cppflags --cxxflags --ldflags --libs)
LIBS = -lboost_system -lboost_program_options -lsndfile
