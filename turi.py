#!/usr/bin/env python3

import sys

def interpret (prog, itpeio, otpeio):
  opcodes = {0x08: 'READ', 0x09: 'WRITE',
             0x0A: 'LOAD', 0x0B: 'STORE',
             0x0C: 'ADD' , 0x0D: 'SUB'  ,
             0x0E: 'MUL' , 0x0F: 'DIV'  ,
             0x07: 'JUMP', 0x06: 'JZERO',
            #0x06: 'JPOS', 0x05: 'AND'  ,
            #0x04: 'NOT' , 0x03: 'OR'   ,
             0x00: 'HALT'}
             
  argtypes ={0x00: 'NONE', 0x10: 'CONST',
             0x20: 'REG' , 0x30: 'IREG' }
             
  bz=0   #Program counter
  reg={} #Register file
  acc=0  #Accumulator
  
  print ('OpCode | AType | Arg      | Accu     | Registers')
    
  
  while (True):
    opcode=  opcodes [(prog[bz] & 0x0F)]
    argtype= argtypes[(prog[bz] & 0x30)]
    arg=None
    arglen=1
    
    
    if (argtype=='NONE'):
      arg=None
      arglen=1
    elif (argtype in ['REG', 'IREG']):
      arg=prog[bz+1]
      arglen=2
    elif (argtype=='CONST'):
      arg =prog[bz+1]<<24
      arg|=prog[bz+2]<<16
      arg|=prog[bz+3]<<8
      arg|=prog[bz+4]<<0
      arglen=5
      
    bz+=arglen
    
    if (opcode=='READ'):
      rde= itpeio.read(4)
      if(len(rde) != 4):
        print ("End of Tape")
        return()
      acc =rde[0]<<24
      acc|=rde[1]<<16
      acc|=rde[2]<<8
      acc|=rde[3]<<0
      
    elif (opcode=='WRITE'):
      wrt= bytearray([(acc>>24)&0xFF, (acc>>16)&0xFF, (acc>>8)&0xFF, (acc>>0)&0xFF])
      otpeio.write(wrt)
      
    elif (opcode=='LOAD'):
      if(argtype=='NONE'):
        acc=0
      elif(argtype=='REG'):
        acc=reg[arg]
      elif(argtype=='IREG'):
        acc=reg[reg[arg]]
      elif(argtype=='CONST'):
        acc=arg
        
    elif (opcode=='STORE'):
      if(argtype=='REG'):
        reg[arg]=acc
      elif(argtype=='IREG'):
        reg[reg[arg]]=acc
        
    elif (opcode in ['ADD','SUB', 'MUL', 'DIV']):
      if(argtype=='REG'):
        num=reg[arg]
      elif(argtype=='IREG'):
        num=reg[reg[arg]]
      elif(argtype=='CONST'):
        num=arg
        
      if(opcode=='ADD'): acc+=num
      if(opcode=='SUB'): acc-=num
      if(opcode=='MUL'): acc*=num
      if(opcode=='DIV'): acc//=num
        
    print ('{:6} | {:5} | {:08x} | {:08x} | {}'.format(opcode, argtype, arg or 0, acc,str(reg)))
        
    if (opcode=='JUMP'):
      bz=arg
    elif (opcode=='JZERO'):
      if (acc==0): bz=arg
    elif (opcode=='HALT'):
      return
      g
def main (argv):
  if (len(argv) != 4):
    print ('{} prog.ctr itape.tpe otape.tpe'.format(argv[0]))
    exit (1)
    
  progio = open(argv[1], 'rb')
  itpeio = open(argv[2], 'rb')
  otpeio = open(argv[3], 'wb')
  
  prog = progio.read()
  
  progio.close()
  
  interpret (prog, itpeio, otpeio)
  
  itpeio.close()
  otpeio.close()

  
if __name__ == '__main__':
  main(sys.argv)
