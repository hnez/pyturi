#!/usr/bin/env python3

import sys

def parse(text):
  print ("Parsing ...")
  
  def splitline(line):
    ret={}
   
    splt=line.split(':',1)
  
    #separate labels, keep rest intact
    if(len(splt)==2):
      line=splt[1]
      ret['l']=splt[0]
    
    #separate arguments, keep opcode intact
    splt=line.split(' ',1)
    if(len(splt)==2):
      line=splt[0]
      ret['a']=splt[1]
    
    if(line):
      ret['o']=line.upper()
     
    return (ret)
      
  #parse into lines
  lines=text.split('\n') 
  
  #strip leading whitespaces
  lines=[x.lstrip() for x in lines]
  
  #strip comments
  lines=[x.split('--')[0]  for x in lines]
    
  #strip trailing whitespaces
  lines=[x.rstrip() for x in lines]
  
  #split by semicolons
  lines=''.join(lines).split(';')
  
  #split the line syntax ([label:]opcode [argument])
  lines= [splitline(x) for x in lines]
  
  return (lines)

def tucompile(pinput):
  opcodes = {'READ': 0x08, 'WRITE':0x09,
             'LOAD': 0x0A, 'STORE':0x0B,
             'ADD' : 0x0C, 'SUB'  :0x0D,
             'MUL' : 0x0E, 'DIV'  :0x0F,
             'JUMP': 0x07, 'JZERO':0x08,
            #'JPOS': 0x06, 'AND'  :0x05,
            #'NOT' : 0x04, 'OR'   :0x03,
             'HALT': 0x00}
             
  argtypes ={'NONE': 0x00, 'CONST':0x10,
             'REG' : 0x20, 'IREG' :0x30}
  
  def getargument(pi):
    if ('a' not in pi):
      return ([argtypes['NONE'], 0])
    if (pi['a'][:4] == 'R[R['):
      num=int(pi['a'][4:].rstrip(']'))
      return ([argtypes['IREG'], num])
    if (pi['a'][:2] == 'R['):
      num=int(pi['a'][2:].rstrip(']'))
      return ([argtypes['REG'], num])
    try:
      return ([argtypes['CONST'],int(pi['a'])])
    except ValueError:
      return ([argtypes['CONST'], None])
  
  output=bytearray()
  
  print ("Assembling...")
  #assemble
  for i, op in enumerate(pinput):
    if ('o' in op):
      at, a= getargument(op)
      
      opcode=0
      opcode|=opcodes[op['o']]
      opcode|=at
      
      pinput[i]['p']=len(output)
      output.append(opcode)
      
      if (at in [argtypes['IREG'], argtypes['REG']]):
        output.append(a)
        
      if (at in [argtypes['CONST']]):
        if a is None:
          pinput[i]['u']=len(output)
          a=0
        
        #Turi.py is Big-endian
        output.append((a>>24)&0xFF)
        output.append((a>>16)&0xFF)
        output.append((a>>8)&0xFF)
        output.append((a>>0)&0xFF)
  
  print ("Linking...")
  #link
  for op in pinput:
    if ('u' in op):
      label=op['a']
      res=tuple(filter(lambda x: 'l' in x and x['l'] == label, pinput))[0]
      a=res['p']
      
      #Turi.py is Big-endian
      output[op['u']+0]=(a>>24)&0xFF
      output[op['u']+1]=(a>>16)&0xFF
      output[op['u']+2]=(a>>8 )&0xFF
      output[op['u']+3]=(a>>0 )&0xFF
    
  #print ('\n'.join(str(x) for x in pinput))
  #print (' '.join('{:02x}'.format(x) for x in output))
  
  return (output)

def main (argv):
  if (len(argv) != 3):
    print ('{} infile.vtr outfile.ctr'.format(argv[0]))
    exit (1)
    
  inio = open(argv[1], 'r')
  instring = inio.read()
  inio.close()
  
  prog= parse(instring)
  comp=tucompile(prog)
  
  print ("Writing Output...")
      
  outio = open(argv[2], 'wb')
  outio.write(comp)
  outio.close()
  
if __name__ == '__main__':
  main(sys.argv)
