# -*- coding: utf-8 -*-
"""data_processing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bMocFCCfScIc_1y5nyU9rf2JWJ6qUmq5
"""

from tensorflow.keras import preprocessing
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.layers import Input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
import numpy as np
import h5py
import os
import re
import random
import keras

import pickle
# data generator class

  #train,val,test별로 사진코드들을 모아놓은 리스트 생성
def sorted_img_code_list(get_path):
  sorted_list= list()  
  with open(get_path, 'r') as f:
    line = f.read().splitlines()
    for filename in line:
      sorted_list.append(filename)
  return sorted_list 
  #시퀀스 중 가장 긴 시퀀스를 찾는 메서드


def img_code_list(train_code_path, val_code_path, test_code_path):
  train_list = sorted_img_code_list(train_code_path)
  val_list = sorted_img_code_list(val_code_path)
  test_list = sorted_img_code_list(test_code_path)
  return train_list,val_list,test_list

def get_max(t,seq):
  max_len =0
  for elem in seq.values():
    sequences = list()
    for line in elem:
      encoded_text = t.texts_to_sequences([line])[0]
      sequences.append(encoded_text)
  
    max_expec = max(len(l) for l in sequences)
    if max_len < max_expec :
      max_len = max_expec  
  return max_len

def create_tokenizer(seq):
  t = Tokenizer()
    #t.fit_on_texts([line for value in self.seq.values()])
  ALL_text = list()
  for elem in seq.values():
    for line in elem:
      ALL_text.append(line)
  t.fit_on_texts(ALL_text)
  return t


def save_all_seq_data(t,seq,max_len,train_list,val_list,test_list,
                      train_seq_path_X,train_seq_path_Y,
                      val_seq_path_X,val_seq_path_Y,
                      test_seq_path_X,test_seq_path_Y):
  save_seq_data(t,seq,train_list,train_seq_path_X,train_seq_path_Y,max_len)
  save_seq_data(t,seq,val_list,val_seq_path_X,val_seq_path_Y,max_len)
  save_seq_data(t,seq,test_list,test_seq_path_X,test_seq_path_Y,max_len)


def save_seq_data(t,seq,sorted_list,seq_path_X,seq_path_Y,max_len):
  ALL_text = list()
  h5_X = h5py.File(seq_path_X,'w')
  h5_Y = h5py.File(seq_path_Y,'w')
  
  vocab_size = len(t.word_index)+1    
  
  idx =0
  for elem in sorted_list:
    text = seq[elem]
    sequences = list()
    x_list = list()
    y_list = list()
      #시퀀스로 만듬
    for line in text:        
      encoded_text = t.texts_to_sequences([line])[0]
      for i in range(1,len(encoded_text)):
        sequence = encoded_text[:i+1]
        sequences.append(sequence)
      
    for x in sequences :
      In= pad_sequences([x[:-1]], maxlen = max_len, padding = 'pre')[0]
      x_list.append(In)          
    for y in sequences :
      y_list.append(to_categorical(y[-1],num_classes=vocab_size))      
    h5_X.create_dataset(elem, data = x_list)
    h5_Y.create_dataset(elem, data = y_list)
    if idx % 200 == 0:
      print('processing' + str(idx))

    idx = idx+1
  h5_X.close()
  h5_Y.close()    

  #텍스트 정재하고 이를 이미지 파일 코드와 dict로 만들어줌
def sequence_refining(token_path):
  textList = list()
  dic = {}      
  with open(token_path, 'r') as f:
    readed = f.read().splitlines()
    filename =''
    for line in readed:
      filename, disc  = line.split('\t')
      rfilename, num = filename.split('#')
      disc = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', disc)
      disc = "sq "+disc+ " eq"
      if rfilename in dic.keys():
        dic[rfilename].append(disc)
      else :
        dic[rfilename] = [disc]      
  return dic        

#image에서 사전 훈련된 CNN(inception_V3)를 이용해 특징을 뽑은 뒤 h5 포맷으로 저장 
def save_img_feature(sorted_save_path,img_data_directory,CNN_Model,img_list):
  h5 = h5py.File(sorted_save_path,'w')  
  indx=0    
  for img in img_list:      
    img_path = os.path.join(img_data_directory, img)
    loaded_img = image.load_img(img_path, target_size = (299, 299))
    loaded_img = image.img_to_array(loaded_img)
    loaded_img = preprocess_input(loaded_img)
    loaded_img = np.expand_dims(loaded_img, 0)
    feature = CNN_Model.predict(loaded_img)
      
    if indx % 100 == 0:
      print('processing'+str(indx))
        
    h5.create_dataset(img, data=feature)
    indx= indx+1
  print("complet")
  h5.close()

def save_all_img_feature(img_data_directory,CNN_model,
                         train_list,val_list,test_list,
                         train_feature_path,val_feature_path,test_feature_path):
  save_img_feature(train_feature_path,img_data_directory,CNN_model, train_list)
  save_img_feature(val_feature_path,img_data_directory,CNN_model, val_list)
  save_img_feature(test_feature_path,img_data_directory,CNN_model, test_list)


if __name__ == "__main__":
  #model 생성
  model = InceptionV3()
  CNN_Model = Model(inputs=model.inputs, outputs = model.layers[-2].output)
  saved_data_path = input()
  #전처리된 데이터가 저장될 경로

  data_base_directory =input()
  #데이터 셋이 있는 경로

  
  #이미지 데이터 경로
  img_data_directory = os.path.join(data_base_directory,'flickr8k_dataset','Flicker8k_Dataset')


  #이미지 데이터 프로세싱 결과가 저장될 경로
  train_feature_path = os.path.join(saved_data_path, 'train_features.hdf5')
  val_feature_path = os.path.join(saved_data_path, 'val_features.hdf5')
  test_feature_path = os.path.join(saved_data_path, 'test_features.hdf5')

  #시퀀스 데이터 프로세싱 결과가 저장될 경로
  train_seq_path_X = os.path.join(saved_data_path,'train_sequence_X.hdf5')
  val_seq_path_X = os.path.join(saved_data_path,'val_sequence_X.hdf5')
  test_seq_path_X = os.path.join(saved_data_path,'test_sequence_X.hdf5')

  train_seq_path_Y = os.path.join(saved_data_path,'train_sequence_Y.hdf5')
  val_seq_path_Y = os.path.join(saved_data_path,'val_sequence_Y.hdf5')
  test_seq_path_Y = os.path.join(saved_data_path,'test_sequence_Y.hdf5')  
  
  #분류된 이미지 데이터의 code가 담겨있는 txt파일 경로
  text_path = os.path.join(data_base_directory,'flickr8k_text')
  train_code_path = os.path.join(text_path,'Flickr_8k.trainImages.txt')
  val_code_path = os.path.join(text_path,'Flickr_8k.devImages.txt')
  test_code_path = os.path.join(text_path,'Flickr_8k.testImages.txt')
  
  #이미지 코드에 따라 저장되있는 이미지를 묘사하는 문자열들이 저장된 txt파일 경로
  token_path = os.path.join(text_path,'Flickr8k.token.txt')


  

  #코드 분류
  train_list,val_list,test_list = img_code_list(train_code_path, val_code_path, test_code_path)

  #이미지 feature 저장
  save_all_img_feature(img_data_directory,CNN_Model,
                       train_list,val_list,test_list,
                         train_feature_path,val_feature_path,test_feature_path)


  #텍스트 정제
  sequence = sequence_refining(token_path)
  
  #tokenizer 생성
  tokenizer = create_tokenizer(sequence)
  
  #max_len 구하기
  max_len = get_max(tokenizer,sequence)
  
  #print(max_len)
  #sequence data 저장
  
  save_all_seq_data(tokenizer,sequence,max_len,
                    train_list,val_list,test_list,
                    train_seq_path_X,train_seq_path_Y,
                    val_seq_path_X,val_seq_path_Y,
                    test_seq_path_X,test_seq_path_Y)
  





  req_token_path = os.path.join(saved_data_path,'token.pickle')
  req_seq_path = os.path.join(saved_data_path,'sequence.pickle')
  req_train_list_path = os.path.join(saved_data_path,'train_list.pickle')
  req_val_list_path = os.path.join(saved_data_path,'val_list.pickle')
  req_test_list_path = os.path.join(saved_data_path,'test_list.pickle')
  with open(req_token_path, 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
  with open(req_seq_path, 'wb') as handle:
    pickle.dump(sequence, handle, protocol=pickle.HIGHEST_PROTOCOL)
  with open(req_train_list_path, 'wb') as handle:
    pickle.dump(train_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
  with open(req_val_list_path, 'wb') as handle:
    pickle.dump(val_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
  with open(req_test_list_path, 'wb') as handle:
    pickle.dump(test_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
  

  data_h5_paths = os.path.join(saved_data_path, 'needs.hdf5')
  needs_h5 = h5py.File(data_h5_paths,'w')
  needs_h5.create_dataset('token_path',data=token_path)
  needs_h5.create_dataset('train_code_path', data = train_code_path)
  needs_h5.create_dataset('val_code_path', data = val_code_path)
  needs_h5.create_dataset('test_code_path', data = test_code_path)
  needs_h5.create_dataset('train_feature_path',data =train_feature_path)
  needs_h5.create_dataset('val_feature_path', data = val_feature_path)
  needs_h5.create_dataset('test_feature_path', data = test_feature_path)
  needs_h5.create_dataset('train_seq_path_X', data = train_seq_path_X)
  needs_h5.create_dataset('val_seq_path_X', data = val_seq_path_X)
  needs_h5.create_dataset('test_seq_path_X', data = test_seq_path_X)
  
  needs_h5.create_dataset('train_seq_path_Y', data = train_seq_path_Y)
  needs_h5.create_dataset('val_seq_path_Y', data = val_seq_path_Y)
  needs_h5.create_dataset('test_seq_path_Y', data = test_seq_path_Y)
  needs_h5.create_dataset('max_len', data = max_len,dtype='int')
  needs_h5.create_dataset('vocab_size', data = len(tokenizer.word_index)+1,dtype ='int')
  needs_h5.create_dataset('req_token_path',data = req_token_path)
  needs_h5.create_dataset('req_seq_path',data = req_seq_path)
  needs_h5.create_dataset('req_train_list_path',data = req_train_list_path)
  needs_h5.create_dataset('req_val_list_path',data = req_val_list_path)
  needs_h5.create_dataset('req_test_list_path',data = req_test_list_path)
  
  
  
  print('end')
  needs_h5.close()