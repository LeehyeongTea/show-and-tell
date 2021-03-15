# show-and-tell

show-and-tell 모델을 what is the Role of Recurrent Neural Networks(RNNs) in an Image Caption Generator?(2017) 논문의 방법론으로 구현한 모델

1. 기존의 show-and-tell 모델

  encoder-decoder LSTM 모델에서 encoder부분을 사전 훈련된 CNN을 사용함.

  ![show and tell 캡쳐](https://user-images.githubusercontent.com/42109314/111209299-32368f80-860f-11eb-88f8-c9a367f2d98c.PNG)

  사전 훈련된 CNN의 feature를 LSTM의 첫번째 input으로 넣어준다. 
  
2. what is the Role of Recurrent Neural Networks(RNNs) in an Image Caption Generator? 방법론
  
  ![방법론2](https://user-images.githubusercontent.com/42109314/111211218-7f1b6580-8611-11eb-8ce2-1ef8212363fc.PNG)

  사전 훈련된 CNN의 feature와 RNN의 output의 행렬합한 뒤 DenseNet에 입력시켜 분류한다.
  
  
