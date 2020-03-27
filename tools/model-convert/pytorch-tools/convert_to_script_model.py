'''
convert pytorch model to script model
requirement pytorch > 1.0.0
'''
import torch
from torch.autograd import Variable
input_example = Variable(torch.ones(1,1,28,28)).cuda()
checkpoint = torch.load('./xxx.pth')
y=checkpoint(input_example)
traced_script_module = torch.jit.trace(checkpoint.module, input_example)
traced_script_module.save("xxx.pt")
