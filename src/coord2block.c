//use samtools to translate a list of coordinates to bytes, per passed in index file (must already be downloaded)

#include <stdio.h>
#include "samtools11/sam.h"
#include "samtools11/htslib-1.1/htslib/bgzf.h"
#include "samtools11/htslib-1.1/htslib/sam.h"
#include "samtools11/bam.h"
#include "samtools11/samtools.h"

typedef uint64_t u64;
typedef hts_pair64_t p64;


//much of the basic loading code was pulled directly from samtools/htslib 1.1 source
//u64 byte_offset(const bam_index_t *idx, header, int ref_if, int start, int end)
u64 byte_offset(const bam_index_t *idx, bam_hdr_t *header, char *range)
{
        //bam_iter_t iter = bam_iter_query(idx, ref_id, start, end);
	hts_itr_t *iter = sam_itr_querys(idx, header, range); // parse a region in the format like `chr2:100-200'
	if (iter == NULL) 
	{	
		// reference name is not found
                fprintf(stderr, "[main_samview] region \"%s\" specifies an unknown reference name.\n", range);
		return -1;
	} 
	u64 current_offset = iter->curr_off;
	p64 *off_pair = iter->off;
	u64 u = off_pair->u>>16;
	u64 v = off_pair->v>>16;
	printf("offset pair: u:%d v:%d\n",u,v);
	bam_iter_destroy(iter);
	return current_offset;
}

int main(int argc, char **argv)
{
	if(argc < 3)
	{
		printf("must submit the bam filename and at least one range\n");
		return -1;
	}
	samFile *in = 0;
	bam_hdr_t *header = NULL;

	char* bamf = argv[1];
	char* range = argv[2];
	if ((in = hts_open(bamf, "r")) == 0) 
	{
        	printf("failed to open \"%s\" for reading", bamf);
		return -1;
	}
	//char** ranges = process_ranges(argv);
	if ((header = sam_hdr_read(in)) == 0) 
	{
		fprintf(stderr, "[main_samview] fail to read the header from \"%s\".\n", bamf);
		return -1;
	}
	hts_idx_t *idx = sam_index_load(in, bamf); // load index
	if (idx == 0) 
	{
		// index is unavailable
        	fprintf(stderr, "[main_samview] random alignment retrieval only works for indexed BAM or CRAM files.\n");
		return -1;
	}

	//now get the byte offsets
	u64 current_off = byte_offset(idx, header, range);
	printf("range: %s; current_offset: %u\n",range,current_off);
	hts_idx_destroy(idx); // destroy the BAM index
	if ( header ) bam_hdr_destroy(header);
}
