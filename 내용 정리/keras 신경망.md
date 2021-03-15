# keras 신경망 

>  참조 경로 : https://www.tensorflow.org/guide/keras/sequential_model?hl=ko
> Keras Mnist : https://www.tensorflow.org/tutorials/keras/classification?hl=ko

### -- 얼굴의 Pixel별 온도 데이터를 이용하여 얼굴인지 아닌지를 분류하는 신경망 모델

1.  ###  데이터셋 만들기

    ```python
    # Real image
    import glob	  # 파일의 경로명을 이용하여 파일들의 리스트를 뽑을 때 사용
    import numpy as np

    foldername = []

    for i in range(20201201, 20201220):
        foldername.append(str(i))

        x_train = []
        x_label = []
        path = r'D:\conda\image'	# r로 시작하는 원시(raw) 문자열을 사용
        for day in foldername:
            filenames = glob.glob(path + '\\' + day + "/*.txt")
            # 인자로 받은 패턴과 이름이 일치하는 모든 파일과 디렉터리의 리스트를 반환
            for filename in filenames:
                if (len(filename) < 50): continue	# 잡다한 파일 skip
                    f = open(filename, 'r', errors='ignore')
                    lines = f.readlines()
                    line = []	# 110 * 120
                    for i, d in enumerate(lines):
                        tmp = lines[i].split(' ')
                        if (i == 320):	# 온도값 저장
                            temp = tmp[0]
                            if (i < 100 or len(tmp) < 100): continue
                                # 블랙바디 부분 (50줄까지)과 온도 데이터 이외의 라인 저장 안함
                                line.append(tmp[:120])

                                x_train.append(line)
                                x_label.append(one_hot_encoding(1, 2))
    ```

      ```python
    def one_hot_encoding(n, length):
        one_hot = [0] * length
        one_hot[n] = 1

        return one_hot
      ```
    - 동일한 양식으로 `Fake image` 와 `Test image` 로드
    
      ###### :arrow_right: 원-핫 인코딩 (One-Hot Encoding)
    
      >단어 집합의 크기를 벡터의 차원으로 하고, 표현하고 싶은 단어의 인덱스에 1의 값을 부여하고, 다른 인덱스에는 0을 부여하는 단어의 벡터 표현 방식
    
      ex) 문장 : `나는 자연어 처리를 배운다` 
    
      ```python
      # 위 문장에 대해서 원-핫 인코딩을 진행하는 코드
      def one_hot_encoding(word, word2index):
             one_hot_vector = [0]*(len(word2index))
             index=word2index[word]
           one_hot_vector[index]=1
             return one_hot_vector
      one_hot_encoding("자연어",word2index) # [0, 0, 1, 0, 0, 0]  
      ```
      

2. ### 로드 데이터 확인

   ```python
   # Real image
   x_train1 = np.array(x_train, dtype='float32')
   x_label1 = np.array(x_label, dtype='float32')
   x_train1.shape	# (6697, 110, 120)
   # Fake image
   y_train1 = np.array(y_train, dtype='float32')
   y_label1 = np.array(y_label, dtype='float32')
   y_train1.shape	# (392, 110, 120)
   
   # Real + Fake
   train_data = np.concatenate((x_train1, y_train1), axis = 0)
   train_data.shape  # (7089, 110, 120) - 총 7089개의 레이블
   train_label = np.concatenate((x_label1, y_label1), axis = 0)
   train_label.shape	# (7089, 2) - 1, 0 두개의 label값을 가짐
   ```

   ```python
   # Test image
   test_data = np.array(test_train, dtype='float32')
   test_label = np.array(test_label, dtype='float32')
   test_data.shape  # (20, 110, 120)
   ```

3. ### 데이터 전처리

   - 2차원 배열인 데이터를 1차원의 데이터로 평탄화
   - 신경망 모델에 주입하기 전 픽셀값(255)으로 나누어 값의 범위를 0~1 사이로 조정

   ```python
   train_data = train_data.reshape((7089, 110*120))
   train_data = train_data.astype('float32') / 255
   
   test_data = test_data.reshape((20, 110*120))
   test_data = test_data.astype('float32') / 255
   ```

4. ### Sequential 모델 구성

   > `Sequential` 모델은 각 레이어에 **정확히 하나의 입력 텐서와 하나의 출력 텐서**가 있는 **일반 레이어 스택**에 적합합니다.

   > 모델의 층을 구성한 다음 모델을 컴파일
   - ##### 층설정

     ```python
     from tensorflow.keras import models, layers
     
     model = models.Sequential()
     # add() 메서드를 통해 Sequential 모델을 점진적으로 작성
     # input_shape() 모델의 시작 형상
     model.add(layers.Dense(512, activation='relu', input_shape=(110 * 120,)))
     model.add(layers.Dense(128, activation='relu'))
     model.add(layers.Dense(32, activation='relu'))
     model.add(layers.Dense(8, activation='relu'))
   model.add(layers.Dense(2, activation='softmax'))
     
     model.summary()
     ```

     ![image-20210312104634484](keras 신경망.assets\image-20210312104547152.png)

     :ballot_box_with_check: 마지막 계층에 단일 노드로 하고 이진 분류 설정을 할 경우 마지막 레이어에 대한 모델은 sigmoid를 이용.

     - softmax - categorical_crossentropy (label이 여러개일때)
     
     	- model.add(layers.Dense(10, activation='softmax')) `10 = label 갯수`
     - sigmoid - binary_crossentropy (label이 2개일때)
     
   - ##### 모델 컴파일

     ```python
     from tensorflow.keras import optimizers
     model.compile(optimizer='rmsprop',
                    loss='categorical_crossentropy',
                    metrics=['acc'])
     ```

     - *손실 함수*(Loss function)

       > MeanSquaredError() - KLDivergence() - CosineSimilarity() - etc.

       훈련 하는 동안 모델의 오차를 측정합니다. 모델의 학습이 올바른 방향으로 향하도록 이 함수를 최소화해야 합니다.

     - *옵티마이저*(Optimizer)

       > SGD()(with or without momentum) - RMSprop() - Adam() - etc

       데이터와 손실 함수를 바탕으로 모델의 업데이트 방법을 결정합니다.

     - *지표*(Metrics)

       > AUC() - Precision() - Recall() - etc.

       훈련 단계와 테스트 단계를 모니터링하기 위해 사용합니다.

5. ### 모델 훈련

   ```python
   history = model.fit(train_data, train_label, epochs=10, batch_size=32)
   ```

   - x : 입력 데이터
   - y : 라벨 값
   - epochs : 학습 반복 횟수 (무조건 높다고 좋은것은 아님 `오버피팅(overfitting)`)
   - batch_size : 몇 개의 샘플로 가중치를 갱신할 것인지 지정 (배치사이즈가 작을수록 가중치 갱신이 자주 일어남.)
   - validation_split : 데이터의 끝 x%만큼을 validation_data로 활용
     - 예를 들어, validation_split = 0.2는 traninig 데이터의 20퍼를 검증데이터로 활용하겠다는 뜻

6. ### 훈련 결과 가시화

   ```python
   import matplotlib.pyplot as plt
   
   plt.clf()
   acc_values = history_dict['acc']
   epochs = range(1, len(history_dict['acc']) + 1)
   
   plt.plot(epochs, acc_values, 'bo', label='Training acc')
   plt.title('Training accuracy')
   plt.xlabel('Epochs')
   plt.ylabel('Loss')
   plt.legend()
   
   plt.show()
   ```

   ![image-20210312110859570](keras 신경망.assets\image-20210312110859570.png)

7. ### 정확도 평가

   ```python
   results = model.evaluate(test_data, test_label)
   results
   # 1/1 [==============================] - 0s 1ms/step - loss: 0.2089 - acc: 1.0000
   # [0.20888206362724304, 1.0]
   ```

8. ### 모델 사용 & 예측

   ```python
   predictions = model.predict(test_data)
   predictions
   '''
   array([[0.0013634 , 0.99863654],
          [0.00307557, 0.99692446],
          ...
          [0.83238196, 0.16761802],
          [0.83029497, 0.16970503]], dtype=float32)
   '''
   ```

   

