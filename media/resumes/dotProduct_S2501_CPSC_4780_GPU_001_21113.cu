#include <stdio.h>
#include <sys/time.h>

const int threads_per_block = 512;

// Forward function declarations
float CPU_big_dot(float *A, float *B, int N);
float GPU_big_dot(float *A, float *B, int N);
float *get_random_vector(int N);
long long start_timer();
long long stop_timer(long long start_time, const char *name);
void die(const char *message);

int main(int argc, char **argv) {
	// Seed the random generator (use a constant here for repeatable results)
	srand(10);

	// Determine the vector length
	//int N = 100000;  // default value
	int N = 1 << 24;  // default value
	if (argc > 1) N = atoi(argv[1]); // user-specified value

	// Generate two random vectors
	long long vector_start_time = start_timer();
	float *A = get_random_vector(N);
	float *B = get_random_vector(N);
	stop_timer(vector_start_time, "Vector generation");
	
	// Compute their dot product on the CPU
	long long CPU_start_time = start_timer();
	float C_CPU = CPU_big_dot(A, B, N);
	long long CPU_time = stop_timer(CPU_start_time, "\nCPU");
	
	// Compute their dot product on the GPU
	long long GPU_start_time = start_timer();
	float C_GPU = GPU_big_dot(A, B, N);
	long long GPU_time = stop_timer(GPU_start_time, "\t            Total");
	
	// Compute the speedup or slowdown
	if (GPU_time > CPU_time) printf("\nCPU outperformed GPU by %.2fx\n", (float) GPU_time / (float) CPU_time);
	else                     printf("\nGPU outperformed CPU by %.2fx\n", (float) CPU_time / (float) GPU_time);
	
	// Check the correctness of the GPU results
        if (fabs(C_CPU - C_GPU) > 0.000001) 
	  printf("\nvalues incorrect, CPU dot product = %f, GPU dot product = %f\n", C_CPU, C_GPU);
	else           
	  printf("\nvalues correct, CPU dot product = %f, GPU dot product = %f\n", C_CPU, C_GPU);

}

// A GPU kernel that computes the vector dot product of A and B
// (each thread computes a single value of the result)
__global__ void dot_product_kernel(float *A, float *B, float *C, int N) {
	// Determine which element this thread is computing
	int thread_id = threadIdx.x + blockIdx.x * blockDim.x;
	
	// Compute a single element of the result vector (if the element is valid)
	if (thread_id < N) C[thread_id] = A[thread_id] * B[thread_id];
}

// Returns the vector dot product of A and B (computed on the GPU)
float GPU_big_dot(float *A_CPU, float *B_CPU, int N) {
	
	long long memory_start_time = start_timer();

	// Allocate GPU memory for the inputs and the result
	int vector_size = N * sizeof(float);
	float *A_GPU, *B_GPU, *C_GPU;
	if (cudaMalloc((void **) &A_GPU, vector_size) != cudaSuccess) die("Error allocating GPU memory");
	if (cudaMalloc((void **) &B_GPU, vector_size) != cudaSuccess) die("Error allocating GPU memory");
	if (cudaMalloc((void **) &C_GPU, vector_size) != cudaSuccess) die("Error allocating GPU memory");
	
	// Transfer the input vectors to GPU memory
	cudaMemcpy(A_GPU, A_CPU, vector_size, cudaMemcpyHostToDevice);
	cudaMemcpy(B_GPU, B_CPU, vector_size, cudaMemcpyHostToDevice);
	
	stop_timer(memory_start_time, "\nGPU:\t  Transfer to GPU");
	
	// Determine the number of thread blocks in the grid 
	int blocks_per_grid = (int) ((float) (N + threads_per_block - 1) / (float) threads_per_block);
	
	// Execute the kernel to compute the vector dot product on the GPU
	long long kernel_start_time = start_timer();
	dot_product_kernel<<< blocks_per_grid , threads_per_block >>> (A_GPU, B_GPU, C_GPU, N);
	cudaDeviceSynchronize();  // this is only needed for timing purposes
	stop_timer(kernel_start_time, "\t Kernel execution");
	
	// Check for kernel errors
	cudaError_t error = cudaGetLastError();
	if (error) {
	  char message[256];
	  sprintf(message, "CUDA error: %s", cudaGetErrorString(error));
	  die(message);
	}
	
	// Allocate CPU memory for the result
	float *C_CPU = (float *) malloc(vector_size);
	if (C_CPU == NULL) die("Error allocating CPU memory");
	
	// Transfer the result from the GPU to the CPU
	memory_start_time = start_timer();
	cudaMemcpy(C_CPU, C_GPU, vector_size, cudaMemcpyDeviceToHost);
	stop_timer(memory_start_time, "\tTransfer from GPU");
	
	// Free the GPU memory
	cudaFree(A_GPU);
	cudaFree(B_GPU);
	cudaFree(C_GPU);

        // Do the summation of multiplication in CPU
        float sum = 0;
	for (int i = 0; i < N; i++) sum += C_CPU[i]; 
	
	return sum;
}

// Returns the vector dot product of A and B
float CPU_big_dot(float *A, float *B, int N) {	
	// Compute the dot product
        float sum = 0;
	for (int i = 0; i < N; i++) sum += A[i] * B[i];
	
	// Return the result
	return sum;
}

// Returns a randomized vector containing N elements
float *get_random_vector(int N) {
	if (N < 1) die("Number of elements must be greater than zero");
	
	// Allocate memory for the vector
	float *V = (float *) malloc(N * sizeof(float));
	if (V == NULL) die("Error allocating CPU memory");
	
	// Populate the vector with random numbers
	for (int i = 0; i < N; i++) V[i] = (float) rand() / (float) rand();
	
	// Return the randomized vector
	return V;
}

// Returns the current time in microseconds
long long start_timer() {
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return tv.tv_sec * 1000000 + tv.tv_usec;
}

// Prints the time elapsed since the specified time
long long stop_timer(long long start_time, const char *name) {
	struct timeval tv;
	gettimeofday(&tv, NULL);
	long long end_time = tv.tv_sec * 1000000 + tv.tv_usec;
	printf("%s: %.5f sec\n", name, ((float) (end_time - start_time)) / (1000 * 1000));
	return end_time - start_time;
}

// Prints the specified message and quits
void die(const char *message) {
	printf("%s\n", message);
	exit(1);
}

