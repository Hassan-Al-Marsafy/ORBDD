import re

class Bdd:
    class Node:
        def __init__(self, var, zero=None, one=None, parent=None):
            self.var = var
            self.zero = zero
            self.one = one
            self.parents = [] if parent is None else [parent]

        def __str__(self):
            return str(self.var)

    def __init__(self):
        self.root = None
        self.vars = {}
        self.nodes = []
        self.constOne = self.createNode(True, None, None, False)
        self.constZero = self.createNode(False, None, None, False)

    def createNode(self, var, zero, one, parent=None, optmzd=False):
        node = Bdd.Node(var, zero, one, parent)
        if not optmzd:
            self.nodes.append(node)
        return node
    
    def get_var(self, input_string):
        proccessChars = set(input_string.replace("'", '').split())
        finalVars = sorted(filter(lambda x: x not in {'', '+'}, proccessChars))
        return (finalVars)

    def calculate_cofactors(self, input_string, current_var):
      terms = input_string.split('+') if isinstance(input_string, str) else [input_string]
      positive_cofactors, negative_cofactors = [], []

      var_dash = current_var + "'"

      for term in terms:
          term = re.sub(' +', '', term)  
          if var_dash in term:
              t = term.replace(var_dash, "")
              if t != '':
                  negative_cofactors.append(t)
              else:
                  negative_cofactors.append('1')
          elif current_var in term:
              t = term.replace(current_var, "")
              if t != '':
                  positive_cofactors.append(t)
              else:
                  positive_cofactors.append('1')
          else:
              if term != '':
                  negative_cofactors.append(term)
                  positive_cofactors.append(term)

      positive_cofactors_str = positive_cofactors[0] if len(positive_cofactors) == 1 else ' + '.join(positive_cofactors)
      negative_cofactors_str = negative_cofactors[0] if len(negative_cofactors) == 1 else ' + '.join(negative_cofactors)




    def generateTree(self,input_string,my_node_vars, optmzd=False):
      if len(my_node_vars)==1:
        symbols=[i for i in input_string.split(' ') if i !='']
        myvar=my_node_vars[0]
        insertat=[]
        for i in range(len(symbols[0:-1])):
          if symbols[i]!= '+' and symbols[i+1] !='+':
            insertat.append(i+1)
        for i in range(len(symbols)):
          if symbols[i]==myvar+"'":
              symbols[i] = 'NOT '+myvar
        for i in reversed(insertat):
          symbols.insert(i,'AND')
        input_string=' '.join(symbols)
        
        output=[SOP_Class().evaluate_function(input_string,i)for i in ['0','1']]
        
        lst=[self.constZero,self.constOne]
        boolean_values = {
            'True': 1,
            'False': 0,
            0:0,
            1:1,
            '0':0,
            '1':1,
        }

        thisnode= self.createNode(my_node_vars.pop(),lst[boolean_values[output[0]]],lst[boolean_values[output[1]]])
        lst[boolean_values[output[1]]].parents.append(thisnode)
        lst[boolean_values[output[0]]].parents.append(thisnode)
        return thisnode
      elif len(my_node_vars)==0:
        return None
      else:
        my_node_var=my_node_vars.pop()
        pos_cofactors,neg_cofactors=self.generate_positive_negative_cofactors(input_string,my_node_var)

        myposchild=None
        mynegchild=None
        if(neg_cofactors==True):
          mynegchild=self.constOne
        elif(neg_cofactors==False):
          mynegchild=self.constZero
        else:
          mynegchild=self.generateTree(neg_cofactors,my_node_vars.copy())
        zero
        if(pos_cofactors==True):
          myposchild=self.constOne
        elif(pos_cofactors==False):
          myposchild=self.constZero
        else:
          myposchild=self.generateTree(pos_cofactors,my_node_vars.copy())
        
        thisnode=self.createNode (my_node_var,mynegchild,myposchild)
        myposchild.parents.append(thisnode)
        mynegchild.parents.append(thisnode)
        
        return thisnode

    def  optmzdGenerateTree(self,input_string,my_node_vars):
      if len(my_node_vars)==1:
        symbols=[i for i in input_string.split(' ') if i !='']
        myvar=my_node_vars[0]
        insertat=[]
        for i in range(len(symbols[0:-1])):
          if symbols[i]!= '+' and symbols[i+1] !='+':
            insertat.append(i+1)
        for i in range(len(symbols)):
          if symbols[i]==myvar+"'":
              symbols[i] = 'NOT '+myvar
        for i in reversed(insertat):
          symbols.insert(i,'AND')
        input_string=' '.join(symbols)
        
        output=[SOP_Class().evaluate_function(input_string,i)for i in ['0','1']]
        
        lst=[self.constZero,self.constOne]
        boolean_values = {
            'True': 1,
            'False': 0,
            0:0,
            1:1,
            '0':0,
            '1':1,
        }
        thisnode= self.createNode(my_node_vars.pop(),lst[boolean_values[output[0]]],lst[boolean_values[output[1]]], optmzd = True)
        if self.compare_nodes(lst[boolean_values[output[0]]],lst[boolean_values[output[1]]]):
          return lst[boolean_values[output[0]]]
        for node in self.nodes:
          if self.compare_nodes(node,thisnode):
            lst[boolean_values[output[1]]].parents.append(node)
            lst[boolean_values[output[0]]].parents.append(node)
            return node
        lst[boolean_values[output[1]]].parents.append(thisnode)
        lst[boolean_values[output[0]]].parents.append(thisnode)   
        self.nodes.append(thisnode)
        return thisnode
      elif len(my_node_vars)==0:
        return None
      else:
        outputmy_node_vars=my_node_vars.pop()
        pos_cofactors,neg_cofactors=self.calculate_cofactors(input_string,outputmy_node_vars)
        myposchild=None
        mynegchild=None
        if(neg_cofactors==True):
          mynegchild=self.myture
        elif(neg_cofactors==False):
          mynegchild=self.zeroConst
        else:
          mynegchild=self. optmzdGenerateTree(neg_cofactors,my_node_vars.copy())
        if(pos_cofactors==True):
          myposchild=self.myture
        elif(pos_cofactors==False):
          myposchild=self.zeroConst
        else:
          myposchild=self. optmzdGenerateTree(pos_cofactors,my_node_vars.copy())
        if self.NodeComparer(mynegchild,myposchild):
          return myposchild
        thisnode=self.createNode(outputmy_node_vars,mynegchild,myposchild,  optmzd = True)
        for node in self.nodes:
          if self.compare_nodes(node,thisnode):
            myposchild.parents.append(node)
            mynegchild.parents.append(node)
            return node
        myposchild.parents.append(thisnode)
        mynegchild.parents.append(thisnode)
        self.nodes.append(thisnode)
        return thisnode

    def NodeComparer(self, node1, node2):
            if node1 is None:
                return node2 is None
            if node2 is None:
                return False
            return (
                node1.var == node2.var and
                self.compare_nodes_optimized(node1.zero, node2.zero) and
                self.compare_nodes_optimized(node1.one, node2.one)
            )
    
    def parse(self, input_string):
      sop = SOP_Class()
      try:
          input_string = sop.generate_SOP(input_string)
      except Exception as err:
          print(f"invalid input: {err}")

      factors = sorted(self.get_var(input_string)[0], reverse=True)
      self.vars = factors.copy()

      if not input_string:
          self.root = self.constZero
      else:
          self.root = self.generateTree(input_string, factors)

    def optmzdParse(self,input_string):

      sop = SOP_Class()

      try:
        input_string = sop.generate_SOP(input_string)
      except Exception as err:
          print(f"invalid input: {err}")

      factors=self.get_var(input_string)[0]
      factors= list(sorted(factors,reverse=True))
      self.vars=factors.copy()
      if input_string=='':
        self.root=self.zeroConst
      else:
        self.root = self.optmzdGenerateTree(input_string,factors)

    def improve_bdd(self):
      delete=[]
      for i,node in enumerate (self.nodes):
        if (len(node.parents)!=0):
          for j,node2 in enumerate(self.nodes):
            if(j>i):
              if (self.compare_nodes(node,node2)):
                for parent in node.parents:
                  if(parent.zero==node):
                    parent.zero=node2
                    if i not in delete:
                      delete.append(i)
                  if(parent.one==node):
                    parent.one=node2
                    if i not in delete:
                      delete.append(i)

                node2.parents.extend(node.parents)
                node.parents.clear()
                        
      for i in reversed(delete):
          del self.nodes[i]

      delete=[]
      for i,node in enumerate (self.nodes):
        if self.compare_nodes(node.zero,node.one) and node.one!=None:
          for parent in node.parents:
            if(self.compare_nodes(parent.zero,node)):
              parent.zero=node.zero
              if i not in delete:
                delete.append(i)
            if(self.compare_nodes(parent.one,node)):
              parent.one=node.zero
              if i not in delete:
                delete.append(i)
              node.zero.parents.append(parent)
                
          try:
            node.parents.clear()
          except:
            
            print("Invalid to delete: ", node , 'from', node.zero)
            
          if node==self.root:
              delete.append(i)
              self.root=node.zero
    
      for i in reversed(delete):
            del self.nodes[i]

    def evaluate(self,input):
      if self.root is None:
        print("the root node is not found or the tree is empty")
        return None
      else:
        if type(input) is str:
          lst=list(reversed([bool(int(i))for i in input]))
          resultsultNode=self.root
          while(resultsultNode.var!=True and resultsultNode.var!=False):
            n=lst[self.vars.index(resultsultNode.var)]
            if(n==False):
              resultsultNode=resultsultNode.zero
            elif(n==True):
              resultsultNode=resultsultNode.one
            
        return resultsultNode.var 

    def truthTable(self):
      inputs=self.biCombinations(len(self.vars))
      results=[]
      for i in reversed(self.vars):
        print (i,end=' ')
      print ('  | f')
      print ((len(self.vars)+1)*'--',end='')
      print('+--')
      for input in inputs:
        for c in input:
          print( c, end=' ')
        output=int(self.evaluate(input))
        print('  |',output)
        results.append(output)
      
      print('combinations num = ',2**len(inputs[0]))
      return results
 

    def biCombinations(self,n):
      def biCombinationsRcrsv(n: int, prefix: str) :
          if n == 0:
              return [prefix]
          return biCombinationsRcrsv(n - 1, prefix + "0") + biCombinationsRcrsv(n - 1, prefix + "1")
      return biCombinationsRcrsv(n, "")
  
    def construct(self,input, opt = False):
      if opt:
         self.optmzdParse(input)
      else:
        self.parse(input)  
        self.improve_bdd()

    def travPreorder(root):
      if root is not None:
        print(root.var,":" ,id(root.zero)," , ",id(root.one)) 

        travPreorder(root.zero)

        travPreorder(root.one)