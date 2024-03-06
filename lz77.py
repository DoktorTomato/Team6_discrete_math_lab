class LZ77:
    def __init__(self, buffer_size: int):
        self.buffer_size = buffer_size

    def encode(self, text: str) -> str:
        matched=""
        encoded=[]
        ind=0
        while ind<len(text):
            element=text[ind]
            if element not in matched[-(self.buffer_size//2):]:
                matched+=element
                encoded.append((0,0,element))
                ind+=1
            else:
                while element in matched[-(self.buffer_size//2):]:
                    ind+=1
                    element+=text[ind]
                if len(element)>2:
                    for i,el in enumerate(matched[::-1]):
                        if el==element[-2]:
                            ofset=i+1+len(element[:-2])
                            matchi=len(element[:-1])
                            left=text[ind]
                            encoded.append((ofset,matchi,left))
                            matched+=element
                            ind=len(matched)
                            break
                else:
                    for i,el in enumerate(matched[::-1]):
                        if el==element[0]:
                            ofset=i+1
                            matchi=1
                            left=text[ind]
                            encoded.append((ofset,matchi,left))
                            matched+=element
                            ind+=len(element)-1
                            break
        return encoded
    def decode(self, code: str) -> str:
        decoded=''
        proses=''
        for cod in code:
            matches=cod[1]
            ofset=cod[0]
            i=0
            while i<matches:
                proses+=decoded[-ofset+i]
                i+=1
            proses+=cod[2]
            decoded+=proses
            proses=""
        return decoded
def test():
    lz = LZ77(buffer_size=10)
    text = "abacababacabc"
    text1 = "abac ababacabc"
    encoded=lz.encode(text)
    encoded1=lz.encode(text1)
    assert encoded1==[(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'c'),(0, 0, " "),(5, 3, 'b'), (2, 1, 'c'), (4, 2, 'c')]
    assert lz.decode(encoded1)== "abac ababacabc"
    assert lz.encode(text) == [(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'c'), (4, 3, 'b'), (2, 1, 'c'), (4, 2, 'c')]
    assert lz.decode(encoded) == "abacababacabc"
    text2 = "This is the test of LZ77 algorythm"
    encoded2=lz.encode(text2)
    assert lz.decode(encoded2) == text2, lz.decode(encoded2)
if __name__== '__main__':
    test()
    print("All assertions passed successfully!")