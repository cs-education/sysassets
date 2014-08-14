
SOURCES=$(wildcard *mp4)
OBJECTS=$(SOURCES:.mp4=.ogv)
FFMPEG=ffmpeg
FFMPEGFLAGS=-c:v libtheora -c:a libvorbis
FFMPEG_OUT_FLAGS=-qscale:v 7

all: $(OBJECTS)

clean:
	rm -rf *.ogv

%.ogv : %.mp4
	$(FFMPEG) -i $< $(FFMPEGFLAGS) $(FFMPEG_OUT_FLAGS) $@
