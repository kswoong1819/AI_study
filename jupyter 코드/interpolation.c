#include <stdio.h>

#define image_h 32
#define image_w 32
#define new_h 64
#define new_w 64

double arr[image_h][image_w];

void save_file(double n_arr[new_h][new_w]) {
	FILE* fp;

	fp = fopen("new_input.txt", "wt");
	if (fp == NULL) {
		printf("실패!!");
		return;
	}

	for (int i = 0; i < new_h; i++) {
		for (int j = 0; j < new_w; j++) {
			fprintf(fp, "%0.2f ", n_arr[i][j]);
		}
		fprintf(fp, "\n");
	}

	fclose(fp);
	printf("성공!!");
	return;
}

int main() {
	freopen("input.txt", "r", stdin);
	for (int i = 0; i < 32; i++)
		for (int j = 0; j < 32; j++)
			scanf("%lf", &arr[i][j]);

	double new_arr[new_h][new_w];

	double rate_h = (double)new_h / (double)image_h;
	double rate_w = (double)new_w / (double)image_w;
	int row_x, row_y;

	for (int i = 0; i < new_h; i++) {
		for (int j = 0; j < new_w; j++) {
			row_x = (int)(j / rate_w);
			row_y = (int)(i / rate_h);

			double fx1 = j / (double)rate_w - (double)row_x;
			double fx2 = 1 - fx1;
			double fy1 = i / (double)rate_h - (double)row_y;
			double fy2 = 1 - fy1;

			double P1 = arr[(int)(i / rate_h)][(int)(j / rate_w)];
			double P2 = arr[(int)(i / rate_h)][(int)((j + rate_w) / rate_w)];
			double P3 = arr[(int)((i + rate_h) / rate_h)][(int)(j / rate_w)];
			double P4 = arr[(int)((i+ rate_h) / rate_h)][(int)((j+ rate_w) / rate_w)];

			double w1 = fx2 * fy2;
			double w2 = fx1 * fy2;
			double w3 = fx2 * fy1;
			double w4 = fx1 * fy1;

			double value = P1 * w1 + P2 * w2 + P3 * w3 + P4 * w4;
			new_arr[i][j] = value;
		}
	}
	save_file(new_arr);
	
	return 0;
}
