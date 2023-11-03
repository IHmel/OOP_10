from abc import ABC, abstractmethod
import hashlib


class Hash(ABC):
    @abstractmethod
    def get_hash(self, data):
        pass

class MD5Hash(Hash):
    def get_hash(self, data):
        result = hashlib.md5(data.encode()).hexdigest()
        return result

class SHA1Hash(Hash):
    def get_hash(self, data):
        result = hashlib.sha1(data.encode()).hexdigest()
        return result

class HashStrategy:
    def get_hash(self, data, hash_object):
        return hash_object.get_hash(data)
    
def main():
    data = input('Введите строку для хэширования:\n')

    
    #Шаблонный метод
    md5_hash = MD5Hash()
    md5_result = md5_hash.get_hash(data)
    sha1_hash = SHA1Hash()
    sha1_result = sha1_hash.get_hash(data)
    
    print('\nSHA1 и MD5 для шаблонного метода')
    print(sha1_result)
    print(md5_result)
    
    #Паттерн стратегии
    hash_strategy = HashStrategy()    
    md5_result = hash_strategy.get_hash(data, md5_hash)
    sha1_result = hash_strategy.get_hash(data, sha1_hash)
    
    print('\nSHA1 и MD5 для паттерна стратегии')
    print(sha1_result)
    print(md5_result)

if __name__ == '__main__':
    main()
