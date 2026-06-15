__kernel void update(const int M, const int N,
            __global const int* prev, __global int* next) {
    const int row = get_global_id(0);
    const int col = get_global_id(1);

    int sum = 0;
    for(int i = -1; i < 2; i++) {
        for(int j = -1; j < 2; j++) {
            sum += prev[M*(row + 1 + i) + col + 1 + j];
        }
    }
    int center = prev[M*(row + 1) + col + 1];

    if(center == 0) {
        next[M*(row + 1) + col + 1] = sum == 3 ? 1 : 0;
    }
    else {
        sum--;
        next[M*(row + 1) + col + 1] = sum >= 2 && sum <= 3 ? 1 : 0;
    }
}