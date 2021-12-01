from hashlib import sha256
import secrets


digest_size = 32 #bytes = 256 bits
# must be doubled in hexa.

#
# Winternitz parameters:
# 
w = 8 # one byte
W = 256  #2^w
l1 = 32
l2 = 2
lW = l1+l2

#
# Encoding functions
#

def _int_from_bytes(xbytes: bytes) -> int:
  return int.from_bytes(xbytes, 'big')

def _even_hex(x):
  y = hex(x)[2:]
  if (len(y)%2 == 1):
    y = "0"+y
  return y

def _hex_length(x,l0):
  y = hex(x)[2:]
  while len(y)<l0:
    y = "0"+y
  return y

def _signature_encoding(sign):
  acc = ""
  for s in sign:
    acc = acc+s
  return acc

def _signature_decoding(sign_enc):
  sign = []
  if len(sign_enc) == lW * digest_size * 2 :
    for i in range(lW):
      sign.append(sign_enc[2*i*digest_size:2*(i+1)*digest_size])
    return True,sign
  else:
    return False,sign
  

#
#
# Internal functions of the scheme
#
#


def _sequence(digest):
  #digest must be a string representing a hex value
  #_sequence outputs a list of int
  seq = []
  s = 0
  for i in range(l1):
    x = int(digest[i:i+2],16)
    seq.append(x)
    s += x
  check  = (l1*W - s)
  new_d  = hex(check)[2:]
  while (len(new_d) < 2*l2):
    new_d = "0"+new_d
  for i in range(l2):
    x = int(digest[i:i+2],16)
    seq.append(x)
  return seq


def _main(key,seq):
  # key is a list of hex strings
  # seq is a list of int
  res = []
  for i in range(lW):
    x = bytes.fromhex(key[i])
    e = seq[i]
    for j in range(e):
      x = sha256(x).digest()
    res.append(_hex_length(_int_from_bytes(x),2*digest_size))
  return res

def _keysequence(sk):
  #sk must be a hex string
  #returns a list of hex strings
  def key_derivation(sk,i):
    #returns a hex-string
    ski = sk + _even_hex(i)
    y = sha256(bytes.fromhex(ski)).hexdigest()
    while (len(y) < 2*digest_size):
      y = "0"+y
    return y

  return [key_derivation(sk,i) for i in range(lW)]

def _get_key(pks):
  acc = ""
  for i in range(lW):
    acc = acc + pks[i]
  y= sha256(bytes.fromhex(acc)).hexdigest()
  while (len(y) < 2*digest_size) :
    y = "0" + y
  return y

#
#
# Functions of the signature scheme
#
#

def sign(sk,message):
  digest = sha256(message).hexdigest()
  seq    = _sequence(digest)
  keys   = _keysequence(sk)
  sign   = _main(keys,seq)
  return _signature_encoding(sign)


def verify(pk,message,sign_enc):
  formated,sign = _signature_decoding(sign_enc)
  if formated:
    digest   = sha256(message).hexdigest()
    seq      = _sequence(digest)
    true_seq = [(W - e) for e in seq ]
    pks      = _main(sign,true_seq)
    return (pk == _get_key(pks))
  else:
    return False

def key_regen(sk):
  keys = _keysequence(sk)
  e_max = [W for i in range(lW)]
  pks = _main(keys,e_max)
  pk = _get_key(pks)
  return pk

def key_gen():
  x    = secrets.randbits(8*digest_size)
  sk   = _hex_length(x,2*digest_size)
  return (sk,key_regen(sk))

#
# Nonce generation function
#

def nonce():
  x = secrets.randbits(8*digest_size)
  return _hex_length(x,2*digest_size) 

#
#
# Test
#
#(sk,pk) = key_gen()
#sign = sign(sk,b'toto')
#print("message signed")
#b = verify(pk,b'toto',sign)
#if b:
#  print("verified")
#else:
#  print("not verified")
#
#b = verify(pk,b'toro',sign)
#if b:
#  print("verified")
#else:
#  print("not verified")
