#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <errno.h>

bool g_debug = false;
#define INVALID UINT16_MAX

void pdata(uint16_t *data, int data_len, int data_width) {
  int i,w;
  for (i=0; i< data_len; i++) {
    if (data[i] == INVALID)
      continue;
    printf("line-%d: ", i);
    for (w=data_width-1; w>=0; w--) {
      printf("%c", (data[i]&(1<<w))?'1':'0');
    }
    printf("\n");
  }
}

int get_gamma(uint16_t *data, int data_len, int data_width) {
  int i,w, valid=0;
  uint16_t sums[data_width];
  uint16_t gamma=0;

  for (w = data_width-1; w >=0; w--) {
    sums[w] = 0;
    for (i = 0; i < data_len; i++) {
      if (data[i] == INVALID)
        continue;
      sums[w] += (data[i] & (1<<w)) >> w;
      //printf("line-%d (0x%x), bit-%d: %d  sums[%d]: %d\n", i, data[i], w, (data[i] & (1<<w)) >> w, w, sums[w]);
      if (w==0)
        valid++;  // just count the valid ones in the last
    }
  }
  if (g_debug) printf("get_gamma() %d valid datapoints\n", valid);

  for (w = data_width-1; w >=0; w--) {
    if (sums[w] < valid/2.0) {
      if (g_debug) printf("  bit-%d: %d/%d set '0': 0x%x\n", w, sums[w], valid, gamma);
    } else { // tie goes to 1
      gamma |= (1 << w);
      if (g_debug) printf("  bit-%d: %d/%d set '1': 0x%x\n", w, sums[w], valid, gamma);
    }
  }

  if (g_debug) {
    printf("Got gamma 0x%x: ", gamma);
    for (w=data_width-1; w>=0; w--) {
      printf("%c", (gamma&(1<<w))?'1':'0');
    }
    printf("\n");
  }
  return(gamma);
}

int bit_criteria(uint16_t *src_data, int data_len, int data_width, bool epsilon) {

  uint16_t *data = NULL;
  int criteria, w, i, lastmatch;
  int valid_count = data_len;

  data = calloc(data_len, sizeof(uint16_t));
  if (!data) {
    fprintf(stderr, "%s\n", strerror(errno));
    return -1;
  }
  memcpy(data, src_data, data_len * sizeof(uint16_t));
  if (g_debug) pdata(data, data_len, data_width);

  for (w = data_width-1; (w >= 0) && (valid_count > 1); w--) {
    criteria = get_gamma(data, data_len, data_width);
    if (epsilon)
      criteria = (~criteria) & ((1 << data_width) - 1);

    if (g_debug) printf("bit-%d:  criteria: 0x%x  criteria mask: 0x%x\n", w, criteria, (criteria & (1<<w)));
    for (i = 0; (i < data_len) && (valid_count > 1); i++) {
      if (data[i] == INVALID) {
        continue;
      }
      if (g_debug) printf("  data[%d]: 0x%x citeria: 0x%x  mask: 0x%x\n", i, data[i], criteria, (1<<w));

      if ((data[i] & (1<<w)) == (criteria & (1<<w))) {
	lastmatch=i;
        if (g_debug) printf("  data[%d]: (0x%x & 0x%x)=0x%x  citeria: (0x%x & 0x%x)=0x%x: match; keep it (lastmatch=%d)\n", i, data[i], (1<<w), data[i] & (1<<w), criteria, (1<<w), criteria & (1<<w), lastmatch);
      } else {
        if (g_debug) printf("  data[%d]: (0x%x & 0x%x)=0x%x  citeria: (0x%x & 0x%x)=0x%x: mismatch; drop it\n", i, data[i], (1<<w), data[i] & (1<<w), criteria, (1<<w), criteria & (1<<w));
	data[i] = INVALID;
	valid_count--;
      }
    }
    if (g_debug) pdata(data, data_len, data_width);
  }
  if (g_debug) printf("bit criteria %d (0x%x)\n", data[lastmatch], data[lastmatch]);

  return data[lastmatch];

}

int main(void)
{
  char *line = NULL;
  ssize_t len = 0;
  ssize_t linesize = 0;
  int linenum = 0;

  uint16_t *data = NULL;
  int bit, pos;
  int width=0;

  int gamma, epsilon, o2, co2;

  while (1) {
    len = getline(&line, &linesize, stdin);
    if (len <= 0)
      break;
    line[len--] = '\0'; // skip the '\n' at the end
    //printf("line-%d [%ld bits]: %s", linenum, len, line);
    if (width) {
      if (len !=width) {
        printf("line-%d Error: width doesn't match\n", linenum);
	return 1;
      }
    } else {
        width = len;
    }

    data = realloc(data, (linenum+1) * sizeof(uint16_t));
    if (!data) {
      fprintf(stderr, "%s", strerror(errno));
      return -1;
    }
    data[linenum] = 0;


    for (pos = len-1; pos >= 0; pos--) {
      bit = len - 1 - pos; 
      if (line[pos] == '1')
          data[linenum] |= 1 << bit;
    }
    linenum++;
  }

  gamma = get_gamma(data, linenum, width);
  epsilon = (~gamma) & ((1 << width) - 1);
  printf("Part 1: gamma: %d  epsilon: %d  product: %d\n", gamma, epsilon, gamma * epsilon);

  o2 = bit_criteria(data, linenum, width, 0);
  co2 = bit_criteria(data, linenum, width, 1);
  printf("Part 2: O2 gen: %d  co2 scrub: %d  product: %d\n", o2, co2, o2 * co2);

  free(line);
  return 0;
}
