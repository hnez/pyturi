#!/usr/bin/env python3

import sys

def interpret (prog, itpeio, otpeio):
  opcodes = {0x08: 'READ', 0x09: 'WRITE',
             0x0A: 'LOAD', 0x0B: 'STORE',
             0x0C: 'ADD' , 0x0D: 'SUB'  ,
             0x0E: 'MUL' , 0x0F: 'DIV'  ,
             0x07: 'JUMP', 0x08: 'JZERO',
            #0x06: 'JPOS', 0x05: 'AND'  ,
            #0x04: 'NOT' , 0x03: 'OR'   ,
             0x00: 'HALT'}
             
  argtypes ={0x00: 'NONE', 0x10: 'CONST',
             0x20: 'REG' , 0x30: 'IREG' }
             
  bz=0   #Program counter
  reg={} #Register file
  acc=0  #Accumulator
  
  print (' '.join('{:02x}'.format(x) for x in prog))
  
  while (True):
    try:
      opcode=  opcodes [(prog[bz] & 0x0F)]
      argtype= argtypes[(prog[bz] & 0x30)]
    
      print ("{:02x}:{} {}".format(prog[bz], opcode,argtype))
    except KeyError:
      pass
    
    bz+=1
    

def main (argv):
  if (len(argv) != 4):
    print ('{} prog.ctr itape.tpe otape.tpe'.format(argv[0]))
    exit (1)
    
  progio = open(argv[1], 'rb')
  itpeio = open(argv[2], 'rb')
  otpeio = open(argv[2], 'wb')
  
  prog = progio.read()
  
  progio.close()
  
  interpret (prog, itpeio, otpeio)
  
  itpeio.close()
  otpeio.close()

  
if __name__ == '__main__':
  main(sys.argv)
