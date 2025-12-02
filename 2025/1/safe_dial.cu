#include <stdio.h>
#include <stdint.h>

#define BEGIN_DIAL         50
#define DIAL_RANGE        100
#define THREADS_PER_BLOCK  16

typedef struct {
    uint8_t dial;  /* 0-99 */
    int32_t move;
} rotate;

__host__ __device__ uint8_t move_dial(uint8_t dial, int32_t move) {
    int32_t temp = dial + move;
    while (temp < 0)
        temp += DIAL_RANGE;
    return (temp % DIAL_RANGE);
}

/*
 * Count how many zero_crosses there are in a dial move by brute force
 */
__global__ void count_cross(rotate *data, int32_t *zero_crosses, size_t len) {
    // Calculate which index this is
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    /* Skip the empty blocks (due to over allocation of memory) */
    if (i >= len) {
      return;
    }

    /* Move the dial one number at a time and check for zero crossing */
    zero_crosses[i] = 0;
    while (data[i].move != 0) {
      if (data[i].move > 0) {
        data[i].dial = (data[i].dial + 1) % 100;
        data[i].move--;
        if (data[i].dial == 0) {
          zero_crosses[i]++;
        }
      } else {
        data[i].dial = (data[i].dial + 99) % 100;
        data[i].move++;
        if (data[i].dial == 0) {
          zero_crosses[i]++;
        }
      }
    }
}

/* Parse data into the struct rotate array */
int ingest_data(const char *filename, rotate **data, size_t *len) {
    int32_t last_dial = BEGIN_DIAL;
    FILE *fp = fopen(filename, "r");

    if (fp == NULL) {
        perror("Error opening file");
        return -1;
    }

    size_t capacity = 16; // initial data buffer size
    size_t count = 0;
    // assume malloc works
    rotate *arr = (rotate *)malloc(capacity * sizeof(rotate));
    if (arr == NULL) {
        perror("Initial allocation failed");
        fclose(fp);
        return -1;
    }

    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        char direction;
        int32_t value;

        if (sscanf(line, " %c%d", &direction, &value) == 2) {
            if (count >= capacity) {
                capacity *= 2;
                rotate *temp = (rotate *)realloc(arr, capacity * sizeof(rotate));
                if (temp == NULL) {
                    perror("Realloc failed");
                    free(arr);
                    fclose(fp);
                    return -1;
                }
                arr = temp;
            }

            arr[count].dial = last_dial;
            if (direction == 'L') {
                arr[count].move = -value;
            } else if (direction == 'R') {
                arr[count].move = value;
            } 

            last_dial = move_dial(arr[count].dial, arr[count].move);
            count++;
        }
    }
    fclose(fp);

    *data = arr;
    *len = count;
    return 0;
}

int main(int argc, char *argv[]) {
    int ret = -1;
    rotate *host_data, *gpu_rotates;
    int32_t *host_zc, *gpu_zc;
    size_t len;

    if (argc != 2) {
      fprintf(stderr, "Usage: %s datafile\n", argv[0]);
      return -1;
    }

    ret = ingest_data(argv[1], &host_data, &len);
    if (ret != 0)
        return ret;

    host_zc = (int32_t *)malloc(len * sizeof(int32_t));
    cudaMalloc(&gpu_zc, len * sizeof(int32_t));
    cudaMalloc(&gpu_rotates, len * sizeof(rotate));

    // Copy host data to GPU
    cudaMemcpy(gpu_rotates, host_data, len * sizeof(rotate), cudaMemcpyHostToDevice);

    // Launch the kernel on the GPU using THREADS_PER_BLOCK
    // The number of blocks is rounded up to cover all elements
    int blocks_per_grid = (len + THREADS_PER_BLOCK-1) / THREADS_PER_BLOCK;
    count_cross<<<blocks_per_grid, THREADS_PER_BLOCK>>>(gpu_rotates, gpu_zc, len);

    //  Copy results from GPU to host
    cudaMemcpy(host_zc, gpu_zc, len * sizeof(int32_t), cudaMemcpyDeviceToHost);

    int sum = 0;
    for (int i = 0; i < len; i++) {
        sum += host_zc[i];
        //printf("Move [%d + %d = %d] had %d zero crossings\n", host_data[i].dial, host_data[i].move,
        //       move_dial(host_data[i].dial, host_data[i].move), host_zc[i]);
    }
    printf("Total Zero crossing: %d\n", sum);

    return 0;
}
