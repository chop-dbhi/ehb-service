import random
import string

class encryptionBaseMethods(object):

    @staticmethod
    def _max_db_length(unique, user_specified_length, block_size, aes_object):

        def encrypted_length(usl):
            ml = usl + 2
            modulus = ml % block_size
            if modulus > 0:
                ml += block_size - modulus
            return (ml + aes_object.check_sum_length()) * 2

        if unique:
            l = encrypted_length(user_specified_length)
            while(l > 255):
                user_specified_length -= 1
                l = encrypted_length(user_specified_length)
            return (l, user_specified_length)

        else:
            return (encrypted_length(user_specified_length), user_specified_length)

    @staticmethod
    def _padding_length(value, block_size):
        # The total length of the encrypted value including zero byte must be even in order
        # to convert to hex
        return block_size - ((len(value)+2) % block_size) + 2

    @staticmethod
    def _semi_random_padding_string(length):
        '''
        Would like to add some random padding, but it needs to be reproducable
        for values of the same length to ensure uniqueness requirements are satisfied,
        ie two values of the same length need to have the same padding so that
        IF the field is required to be unique it can be compared to other values in the db
        '''
        mod = max(length % 10, 1)
        seed = 0
        temp = length
        for i in range(7):
            seed += (10**i)*mod
            temp += 1
            mod = max(temp % 10, 1)
        random.seed(seed)
        random_padding = ''.join([random.choice(string.printable) for i in range(length)])
        # convert string to bytes
        return random_padding.encode("utf8")
        # return ''.join([random.choice(string.printable) for i in range(length)])

    def _split_byte():
        return b'\0'
