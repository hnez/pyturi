#!/usr/bin/env python3

import struct

"""
    turi.py a interpreter for pyturi bytecode
    Copyright (C) 2014  Leonard Göhrs

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

def interpret (prog, itpeio, otpeio):
  opcodes = {0x08: 'READ', 0x09: 'WRITE',
             0x0A: 'LOAD', 0x0B: 'STORE',
             0x0C: 'ADD' , 0x0D: 'SUB'  ,
             0x0E: 'MUL' , 0x0F: 'DIV'  ,
             0x07: 'JUMP', 0x06: 'JZERO',
             0x05: 'JNEG', 0x04: 'OR',
             0x03: 'NOT' , 0x02: 'AND',
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
    oplen=1
    
    
    if (argtype=='NONE'):
      arg=None
      oplen=1
    elif (argtype in ['REG', 'IREG']):
      ba=bytearray([prog[bz+1]])
      arg=struct.unpack("!B",ba)[0]
      oplen=2
    elif (argtype=='CONST'):
      ba=bytearray(prog[bz+1:bz+5])
      arg=struct.unpack("!l",ba)[0]
      oplen=5
      
    bz+=oplen
    
    if (opcode=='READ'):
      rde= itpeio.readline()
      if not rde:
        raise Exception ("End of tape")
        
      rde=rde.lstrip().rstrip().rstrip(',;:')
      
      acc=(int(rde))      
      
    elif (opcode=='WRITE'):
      wrt=str(acc) + '\n'
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

    elif (opcode in ['ADD','SUB', 'MUL', 'DIV', 'OR', 'AND']):
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
      if(opcode=='OR'):  acc&=num
      if(opcode=='AND'): acc&=num

    elif (opcode=='NOT'):
      acc=~acc

    print ('{:6} | {:5} | {:08x} | {:08x} | {}'.format(opcode, argtype, arg or 0, acc,str(reg)))
        
    if (opcode in ['JUMP', 'JZERO', 'JNEG']):
      if(argtype=='REG'):
        num=reg[arg]
      elif(argtype=='IREG'):
        num=reg[reg[arg]]
      elif(argtype=='CONST'):
        num=arg

      if (opcode=='JUMP'):
        bz=num

      if (opcode=='JNEG'):
        if (acc<0):
          bz=num

      if (opcode=='JZERO'):
        if (acc==0):
          bz=num

    elif (opcode=='HALT'):
      return

def main (argv):
  if (len(argv) != 4):
    print ('{} prog.ctr itape.tpe otape.tpe'.format(argv[0]))
    exit (1)
    
  progio = open(argv[1], 'rb')
  itpeio = open(argv[2], 'r')
  otpeio = open(argv[3], 'w')
  
  prog = progio.read()
  
  progio.close()
  
  interpret (prog, itpeio, otpeio)
  
  itpeio.close()
  otpeio.close()

  
if __name__ == '__main__':
  main(sys.argv)
