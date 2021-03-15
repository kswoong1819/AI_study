# CNN

> 출처 : https://www.tensorflow.org/tutorials/images/cnn

## Mnist

### 1. 데이터셋 준비

```python
import tensorflow as tf
from tensorflow.keras import datasets, layers, models

(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# 픽셀 값을 0~1 사이로 정규화합니다.
train_images, test_images = train_images / 255.0, test_images / 255.0
```

### 2. 합성곱 층 만들기

- CNN은 배치(batch) 크기를 제외하고 (이미지 높이, 이미지 너비, 컬러 채널) 크기의 텐서(tensor)를 입력으로 받음.
- 컬러 이미지는 (R,G,B) 세 개의 채널을 가짐.
  - mnist는 흑백의 이미지이기 때문에 컬러 채널을 1로 입력.

```python
#  Conv2D와 MaxPooling2D 층을 쌓는 일반적인 패턴으로 합성곱 층을 정의
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
```

```python
# 모델의 구조를 출력
model.summary()
```
- Conv2D와 MaxPooling2D 층의 출력은 (높이, 너비, 채널) 크기의 3D 텐서
- 높이와 너비 차원은 네트워크가 깊어질수록 감소
- Conv2D 층에서 출력 채널의 수는 첫 번째 매개변수에 의해 결정 (예를 들면, 32 또는 64)
- 일반적으로 높이와 너비가 줄어듦에 따라 (계산 비용 측면에서) Conv2D 층의 출력 채널을 늘릴 수 있다.

<img src="CNN.assets\image-20210315095002800.png" alt="image-20210315095002800" style="zoom:80%;" />

### 3. Dense층 추가

```python
model.add(layers.Flatten())	 # 3D -> 1D
model.add(layers.Dense(64, activation='relu'))
# 10개의 클래스를 가지므로 10개의 출력과 소프트맥스 활성화 함수를 사용
model.add(layers.Dense(10, activation='softmax'))
```

```python
# 최종 모델 구조
model.summary()
```

- 두 개의 Dense 층을 통과하기 전에 (4, 4, 64) 출력을 (1024) 크기의 벡터로 펼침.

<img src="CNN.assets\image-20210315095931465.png" alt="image-20210315095931465" style="zoom:80%;" />

### 4. 모델 컴파일과 훈련하기

```python
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)
```

### 5.  모델 평가

```python
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
# 0.9895
```

