#include <stdio.h>

#define image_h 32
#define image_w 32

int arr[image_h][image_w];

int main() {
	freopen("input.txt", "r", stdin);
	for (int i = 0; i < 32; i++)
		for (int j = 0; j < 32; j++)
			scanf("%d", &arr[i][j]);

	int new_h = 32, new_w = 64;
	double rate_h = (double)new_h / (double)image_h;
	double rate_w = (double)new_w / (double)image_w;
	int row_x, row_y;

	for (int i = 0; i < new_h; i++) {
		for (int j = 0; j < new_w; j++) {
			row_x = (int)(i / rate_h);
			row_y = (int)(j / rate_w);

			double fx1 = i / (double)rate_h - (double)row_x;
			double fx2 = 1 - fx1;
			double fy1 = j / (double)rate_w - (double)rate_w;
			double fy2 = 1 - fx2;

			double P1 = arr[]

			double w1 = fx2 * fy2;
			double w2 = fx1 * fy2;
			double w3 = fx2 * fy1;
			double w4 = fx1 * fy1;

		}
	}
}