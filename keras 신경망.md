# keras 신경망 

### 얼굴의 Pixel별 온도 데이터를 이용하여 얼굴인지 아닌지를 분류하는 신경망 모델

### 1. 데이터셋 만들기

- 얼굴이 포함되어 있는 True Data (Real Image)

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

  - 원-핫 인코딩 (One-Hot Encoding)

    >

  ```python
  def one_hot_encoding(n, length):
      one_hot = [0] * length
      one_hot[n] = 1
      
      return one_hot
  ```

  

  

