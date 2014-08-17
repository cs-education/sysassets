
SOURCES=$(wildcard *mp4)
OGG_FILES=$(SOURCES:.mp4=.ogv)
WEBM_FILES=$(SOURCES:.mp4=.webm)
#-qscale:v 9
FFMPEG=ffmpeg
FFMPEG_OGG_FLAGS=-c:v libtheora -c:a libvorbis  -maxrate 800k -b 700k
FFMPEG_WEBM_FLAGS=-q:v 9 -c:v libvpx -c:a libvorbis 

all: $(OGG_FILES) $(WEBM_FILES)

clean:
	rm -rf *.ogv *.webm

%.ogv : %.mp4
	rm -f $@ 
	$(FFMPEG) -i $< $(FFMPEG_OGG_FLAGS) $@

%.webm : %.mp4
	rm -f $@ 
	$(FFMPEG) -i $< $(FFMPEG_WEBM_FLAGS) $@


