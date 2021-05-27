# Huffman Encoding Algorithm

string = 'DS2:INDEXEDCORPORA'
class Node1:
   def __init__(self, val: str, dat: str) -> None:
      self._left = None
      self._right = None
      self._value = val
      self._data = dat

class Pagoda1:
   def __init__(self):
      self._root:Node1 = None
   
   def is_empty(self):
      if self._root == None:
         return True
      return False

   def clear(self):
      self._root = None

   def Merge(self, root: Node1, newnode: Node1):
      if root == None:
         return newnode
      elif newnode == None:
         return root
      else:
         bottomroot: Node1 = root._right
         root._right = None
         bottomnew: Node1 = newnode._left
         newnode._left = None
         r:Node1 = None
         temp:Node1 = None

         while (bottomroot != None and bottomnew != None):
            if bottomroot._value < bottomnew._value:
               temp = bottomroot._right
               if r == None:
                  bottomroot._right = bottomroot
               else:
                  bottomroot._right = r._right
                  r._right = bottomroot
               
               r = bottomroot
               bottomroot = temp
            else:
               temp = bottomnew._left
               if r == None:
                  bottomnew._left = bottomnew
               else:
                  bottomnew._left = r._left
                  r._left = bottomnew
               
               r = bottomnew
               bottomnew = temp
         
         if bottomnew == None:
            root._right = r._right
            r._right = bottomroot
            return root
         else:
            newnode._left = r._left
            r._left = bottomnew
            return newnode

   def print_root(self):
      return ((self._root._value, self._root._data))
    #   a:Node = self._root._right
    #   b:Node = self._root._left

    #   print("right    ",a._value, a._data)
    #   print("left    ",b._value, b._data)

   def insert_2(self, n: Node1, root: Node1):
      n._left = n
      n._right = n
      return self.Merge(root, n)

   def insert_1(self, val, dat):
      n = Node1(val, dat)
      self._root = self.insert_2(n, self._root)

   def delete_1(self):
      self._root = self.delete_2(self._root)

   def delete_2(self, root :Node1):
      L : Node1 = None
      R : Node1 = None
      if root == None:
         print("is empty:((")
         return None

      else:
         if root._left == root:
            L = None
         else:
            L = root._left
            while L._left != root:
               L = L._left
            
            L._left = root._left

         if root._right == root:
            R = None
         else:
            R = root._right
            while R._right != root:
               R = R._right
            
            R._right = root._right

         return self.Merge(L,R)

   def sort_dic(self, inpt):
        lst = []
        dic = {}
        for x,y in  inpt.items():
            self.insert_1(y,x)

        while self.is_empty() == False:
            temp = self.print_root()
            self.delete_1()
            lst.append((temp[1],temp[0]))

        return lst



class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

def compression(string):
    lst = []
    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    P = Pagoda1()

    freq = P.sort_dic(freq)

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])

    d = dict()
    for (char, frequency) in freq:
        d.update({char: huffmanCode[char]})
    lst.append(d)

    encoded_string = ''
    for char in string:
        encoded_string += d[char]
    lst.append(str(encoded_string))

    return lst

def huffman_decoding(encoded_string, codes):
    decoded_string = ''
    keys = list(codes.keys())
    values = list(codes.values())
    interchanged_dict = dict()
    for i in range(len(keys)):
        interchanged_dict.update({values[i]: keys[i]})
    temp = ''
    for char in encoded_string:
        if temp not in values:
            temp += char
        else:
            decoded_string += interchanged_dict[temp]
            temp = ''
            temp += char
    decoded_string += interchanged_dict[temp]
    return decoded_string


table = compression(string)
print(table)

result = huffman_decoding(table[1],table[0])
print(result)