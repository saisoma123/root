#!/usr/bin/python3

### generate COnv2d model using Pytorch

from __future__ import print_function
import numpy as np
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F


result = []

class Net(nn.Module):
    
    def __init__(self, nd = 1, nc = 1, nl = 4):
        super(Net, self).__init__()

        self.nc = nc
        self.nl = nl
              
        nout = 50
        if (nl == 1) : nout = nc 
        self.out0 = nn.Linear(in_features=nd, out_features=50)
        self.out1 = nn.Linear(in_features=50, out_features=100)
        self.out2 = nn.Linear(in_features=100, out_features=100)
        self.out3 = nn.Linear(in_features = 100, out_features = nc)

    def forward(self, x):

      x = self.out0(x)
      x = F.relu(x)
      if (self.nl == 1) : return x
      x = self.out1(x)
      x = F.relu(x)
      x = self.out2(x)
      x = F.relu(x)
      x = self.out3(x)

      return x

def main():

   parser = argparse.ArgumentParser(description='PyTorch model generator')
   parser.add_argument('params', type=int, nargs='+',
                    help='parameters for the Dense network : batchSize , inputChannels, nlayers ')
   
   args = parser.parse_args()
  
  
   bsize = 1
   d = 10
   nlayers = 4
   noutput = 4

   np = len(args.params)
   if (np < 2) : exit()
   bsize = args.params[0]
   d = args.params[1] 
   if (np > 2) : nlayers = args.params[2]
  

   print ("using batch-size =",bsize,"input dim =",d,"nlayers =",nlayers)

   xinput  = torch.zeros([])
   for ib in range(0,bsize):
      xa = torch.ones([1,d]) * (ib+1)
      #concatenate tensors 
      if (ib == 0) : 
         xinput = xa
      else :
         xinput = torch.cat((xinput,xa),0) 

   print("input data",xinput.shape)
   print(xinput)
   
   name = "LinearModel_B" + str(bsize)

   saveOnnx=True
   loadModel=False
   savePtModel = False

    
   model = Net(d,noutput,nlayers)
    
   model(xinput)

   if loadModel :
        print('Loading model from file....')
        checkpoint = torch.load(name + ".pt")
        model.load_state_dict(checkpoint['model_state_dict'])

  
   y = model.forward(xinput)

   print("output data : shape, ",y.shape)
   print(y)

   if savePtModel :
      torch.save({'model_state_dict':model.state_dict()}, name + ".pt")

   if saveOnnx:
        torch.onnx.export(
                model,
                xinput,
                name + ".onnx",
                export_params=True
        )

   outSize = y.nelement()
   yvec = y.reshape([outSize])
   # for i in range(0,outSize):
   #      print(float(yvec[i]))

   f = open(name + ".out", "w")
   for i in range(0,outSize):
        f.write(str(float(yvec[i]))+" ")
        
        
    

if __name__ == '__main__':
    main()
