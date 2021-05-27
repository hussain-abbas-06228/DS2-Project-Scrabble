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

        for x,y in lst[::-1]:
            dic[x] = y

        return dic




test = {'!': 13, 'm': 2, 'o': 2, 'n': 1, 'a': 2, 'p': 3, 'l': 1, 'e': 1}
p = Pagoda1()
print(p.make_dic(test))

# for x,y in  test.items():
#     print(x,y)
#     p.insert_1(y,x)

# p.print_root()

# lst = []
# new = {}
# while p.is_empty() == False:
#     temp = p.print_root()
#     p.delete_1()
#     lst.append((temp[1],temp[0]))
#     #new[temp[1]] = temp[0]

# print(lst)
# lst = lst[::-1]
# for x,y in lst:
#     new[x] = y

# print(new)


# p.insert_1('zoo')
# p.print_root()

# p.insert_1('banana')
# p.print_root()

# p.delete_1()
# p.print_root()

# p.delete_1()
# p.print_root()
# print(p.is_empty())

# p.delete_1()
# print(p.is_empty())





# p.clear()

# print(p.is_empty())