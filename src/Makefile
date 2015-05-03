coord2block:coord2block.o
	gcc -O0 -g -o coord2block coord2block.o ./samtools11/htslib-1.1/libhts.a ./samtools11/libbam.a -lm -lz -pthread
coord2block.o:
	gcc -O0 -g -DUSE_BAM -c coord2block.c -o coord2block.o -I ./samtools11 -I ./samtools11/htslib-1.1 -I ./samtools11/htslib-1.1/htslib

clean:
	rm -f *.o
	rm coord2block
