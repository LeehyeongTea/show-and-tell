# show-and-tell

show-and-tell 모델을 what is the Role of Recurrent Neural Networks(RNNs) in an Image Caption Generator?(2017) 논문의 방법론으로 구현한 모델

1. 기존의 show-and-tell 모델

  encoder-decoder LSTM 모델에서 encoder부분을 사전 훈련된 CNN을 사용함.

  ![show and tell 캡쳐](https://user-images.githubusercontent.com/42109314/111209299-32368f80-860f-11eb-88f8-c9a367f2d98c.PNG)

  사전 훈련된 CNN의 feature를 LSTM의 첫번째 input으로 넣어준다. 

2. what is the Role of Recurrent Neural Networks(RNNs) in an Image Caption Generator? 방법론

  ![방법론2](https://user-images.githubusercontent.com/42109314/111211218-7f1b6580-8611-11eb-8ce2-1ef8212363fc.PNG)

  사전 훈련된 CNN의 feature와 RNN의 output의 행렬합한 뒤 DenseNet에 입력시켜 분류한다.



3. Requirements

   python3, tensorflow, NLTK, matplotlib, PIL, h5py,  pickle

4. 실행 방법

   1. data_processing.py 실행 - 학습할 데이터가 저장될 path, 학습데이터가 저장될 path를 지정
   2. model.py 실행 - 학습할 데이터가 저장된 path, 학습된 모델들이 저장될 path를 지정해야함
   3.  evalutaion.py 실행 - 학습할 데이터가 저장된 path, 모델 path를 지정해야함

5. 결과

   greedy-search를 활용 

   BLEU-1: 0.5714937980366791 

   BLEU-2: 0.3440705692607763 

   BLEU-3: 0.244745379753475 

   BLEU-4: 0.12625593506226632 

   k=3 인 beam-search를 활용 

   BLEU-1: 0.6128750481633843 

   BLEU-2: 0.3630172269816211 

   BLEU-3: 0.2559594519059041 

   BLEU-4: 0.13715272634208575