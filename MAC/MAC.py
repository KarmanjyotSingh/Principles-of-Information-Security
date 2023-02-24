import sys
sys.path.append('../PRF')
from PRF import PRF as prf

class MAC:
    def __init__(self, security_parameter: int, 
                 prime_field: int,
                 generator: int, 
                 seed: int):
        """
        Initialize the values here
        :param security_parameter: 1ⁿ
        :type security_parameter: int
        :param prime_field: q
        :type prime_field: int
        :param generator: g
        :type generator: int
        :param seed: k
        :type seed: int
        """

        self.security_parameter = security_parameter
        self.prime_field = prime_field
        self.generator = generator
        self.seed = seed
        self.prf = prf(security_parameter = security_parameter,
                          prime_field = prime_field,
                            generator = generator,
                            key = seed)
        
    
    def mac(self, message: str, random_identifier: int) -> str:
        """
        Generate tag t
        :param random_identifier: r
        :type random_identifier: int
        :param message: message encoded as bit-string
        :type message: str
        """
        n = self.security_parameter 
        l = n//4 # length of the tag parameters
        msg_len = len(message)
        d = msg_len//l # number of blocks ( each of length n/4 )
        d_str = bin(d)[2:].zfill(l) # convert d to binary and pad with 0s to length n/4      
        r_str = bin(random_identifier)[2:].zfill(l) # generate random identifier of length n/4
        tag_array = r_str
        for block in range(d):
            r = r_str
            i = bin(block+1)[2:].zfill(l) # convert block number to binary and pad with 0s to length n/4
            m_i = message[block*l:(block+1)*l] # get the block of message
            x = r+d_str+i+m_i # concatenate the strings
            x = int(x,2)
            y = self.prf.evaluate(x) # evaluate the PRF at x
            tag_array+=bin(y)[2:].zfill(n) # append the tag to the tag array
        
        return tag_array

    def vrfy(self, message: str, tag: str) -> bool:
        """
        Verify whether the tag commits to the message
        :param message: m
        :type message: str
        :param tag: t
        :type tag: str
        """
        n = self.security_parameter
        l = n//4
        msg_len = len(message)
        d = msg_len//l
        # get the random seed 
        r_str = tag[:l]
        r = int(r_str,2)
        t_generated = self.mac(message,r)
        
        return True if t_generated == tag else False

# read from csv 

# [24, 827, 127, 400,"101100101000101000101111",8]
# [28, 617, 150, 123,"111011101100101001110",2  ]]  
# a = [28, 617, 150, 123,"111011101100101001110",2  ]
# mac = MAC(security_parameter = a[0],
#             prime_field = a[1],
#             generator = a[2],
#             seed = a[3])
# t = mac.mac(a[4],a[5])
# print(t)
# print(mac.vrfy(a[4],t))