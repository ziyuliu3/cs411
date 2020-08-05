from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from .filters import ProductFilter
# from django.forms import inlineformset_factory

# Create your views here.
# def gotohome(request):
#     redener(request,)
def home(request,pk,ck): #ck is seller id
    location = Location.objects.get(id=pk) #location pk
    # location = Location.objects.all()
    productset=location.product_set.all()
    seller = Seller.objects.get(id=ck)
    myFilter = ProductFilter(request.GET, queryset=productset)#shishikan
    productset = myFilter.qs
    context={'location':location, 'productset':productset,'myFilter':myFilter,'seller':seller}

    return render(request, 'accounts/dashboard.html',context)

# def products(request,pk):
#     seller = Seller.objects.get(id=pk)
#     list1 = t.find1(seller.filt_c)
#     #from list1, which return closest filt_p; we need the product
#     for i in list1:
#         targetproduct=Product.objects.get(filt_p=i)
#     productset = seller.product_set.all()
#     myFilter = ProductFilter(request.GET, queryset=productset)#shishikan
#     productset = myFilter.qs
#     context={'seller':seller, 'productset':productset,'myFilter':myFilter,'targetproduct':targetproduct}
#     return render(request, 'accounts/products.html',context)

    # productset=Product.objects.all()
    # return render(request, 'accounts/products.html',{'productset':productset})

def location(request, pk):
    #index = pk  #找sellerid
    seller = Seller.objects.get(id=pk)
    location = Location.objects.all()
    #add='accounts/location/' + str(index) +'/.html'
    # productset=Location.product_set.all()
    # myFilter=ProductFilter()
    # context={'location':location, 'productset':productset,'myFilter':myFilter }
    return render(request, 'accounts/location.html' ,{'location':location,'seller':seller})

def customer(request,pk):
    customer = Customer.objects.get(id=pk) # 目的是哪个custom返回哪个界面 用到product上去？？pt9
    # orders = customer.order_set.all()
    # context = {'customer': customer, 'orders': orders}
    return render(request, 'accounts/customer.html')

@csrf_exempt
def login(request):
    if request.method == "GET":
        # return render(request, "login.html")
        # return HttpResponse('1')
        return render(request, 'accounts/login.html')
    else:
       username = request.POST.get('username')
       password = request.POST.get('password')
       reg=Seller.objects.filter(username__exact=username, password__exact=password)
       if reg:
            seller = Seller.objects.get(username=username)
            # context={'seller':seller,'username':username}
            id=seller.id
            # return HttpResponse(seller.id)
            return redirect('/products/'+str(id)+'/')
       else:
           return HttpResponse('Login fail.')

# def createProduct(request,pk): #pk is seller id
#     form = ProductForm()
#     index = pk
#     # ProductFormSet=inlineformset_factory(Location,Product,fields=('location',),extra=10)
#     if request.method == 'POST':
#         #print('Printing POST:'request.POST)
#         form = ProductForm(request.POST)

#         filt = ()
#         if form.is_valid():
#             form.save()
#             a=Product.objects.last()
#             filt = filtCalculator_P(a.location_id,a.category,a.price,a.depreciation,t)
#             newproduct=Product.objects.get(id=a.id)
#             newproduct.filt_p= filt
#             newproduct.save()
#             return redirect('/products/'+str(index)+'/') #传送
#     context = {'form':form}
#     return render(request, 'accounts/product_form.html', context)

def updateProduct(request,ck,pk):
    product = Product.objects.get(id=pk)
    index = ck
    form = ProductForm(instance=product)
    if request.method == 'POST':
        #print('Printing POST:'request.POST)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            #return HttpResponse('update ok')
            filt = filtCalculator_P(product.location_id,product.category,product.price,product.depreciation) #产品filt指
            # # return HttpResponse(t.find1())
            #product=Product.objects.get(id=.id)
            product.filt_p= filt
            product.save()
            return redirect('/products/'+str(index)+'/') #传送
    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)

def deleteProduct(request,ck,pk):
    #seller = Seller.objects.get(id=ck)
    product = Product.objects.get(id=pk)
    index = ck
    if request.method == 'GET':

        context = {'item':product}
        # return HttpResponse(request.method=='GET')
        return render(request, 'accounts/delete.html', context)
    #t.delete(product.filt_p)
    product.delete()
    return redirect('/products/'+str(index)+'/')
    # return redirect('/location') #传送 change from products to login
        #return HttpResponse('del')

def buyProduct(request,ck,pk): #ck for seller, pk for product
    product = Product.objects.get(id=pk)
    index=ck
    seller = Seller.objects.get(id=ck)
    if request.method == "POST":
        product.delete()
        return redirect('/products/'+str(index)+'/')
        # return redirect('/') #传送
    context = {'item':product,'seller':seller}

    return render(request, 'accounts/buy.html', context)

def register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        reg = Seller.objects.filter(username__exact=username)
        if not reg:
            seller = Seller.objects.create(username=username, password=password,email=email)
            ##add funcition to go to filter.html and do btree calculation
            return redirect('/filter/'+str(seller.id)+'/')

            # return HttpResponse('添加成功')
        else:
            #    return redirect(request, 'accounts/register.html')

            return redirect('/register')
            # return HttpResponse('notok')


    # if request.method == 'GET':
    #     return render(request, 'accounts/register.html')
    # else:
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     gender = request.POST.get('gender')
    #     Customer.objects.create(name=name,password=password,gender = gender)
    #     return HttpResponse('添加成功')

def userPreference(request, pk):
    if request.method == "GET":
        return render(request, "accounts/filter.html")
    else:
        location = request.POST.get('location')
        catagory = request.POST.get('catagory')
        prefer = request.POST.get('prefer')
        filt = filtCalculator(location, catagory, float(prefer))
        newseller=Seller.objects.get(id=pk)
        newseller.filt_c= filt
        newseller.save()
        return redirect('/login')


def filtCalculator(location, catagory, prefer):
    count = 0
    if(location == 'Urbana'):
        count += 2
    if(location == 'Champaign'):
        count += 4
    if(location == 'Springfield'):
        count += 6
    if(catagory == 'Lifestyle'):
        count += 10
    if(catagory == 'Kitchen'):
        count += 20
    if(catagory == 'Fashion'):
        count += 30
    if(catagory == 'Beauty'):
        count += 40
    if(catagory == 'Study'):
        count += 50
    count += prefer
    return count

# def filtCalculator_P(loc, cat, pro, dep, t):
#     perc = pro/(dep+pro)
#     thelocval = 0
#     thecatval = 0
#     if (loc == 'Urbana'):
#         thelocval = 1
#     elif (loc == 'Champaign'):
#         thelocval = 2
#     elif (loc == 'Springfield'):
#         thelocval = 3
#     if (cat == 'Lifestyle'):
#         thecatval = 1
#     elif (cat == 'Kitchen'):
#         thecatval = 2
#     elif (cat == 'Fashion'):
#         thecatval = 3
#     elif (cat == 'Beauty'):
#         thecatval = 4
#     elif (cat == 'Study'):
#         thecatval = 5
#     thevalue = thelocval * 2 + thecatval * 10 + perc
#     while t.find(thevalue)[0]:
#         thevalue = thevalue + 0.01
#     t.insert(thevalue)
#     return thevalue





debugMode = False

import sys

def debug(s):
    if debugMode:
        print ()



#class Node
class Node:
    def __init__(self, parent=None, prevNode=None, nextNode=None):
        self.parent   = parent
        self.children = []
        self.keys     = []
        self.prevNode = prevNode
        self.nextNode = nextNode

    def __str__(self):
        return "node:<%s>" % self.keys



#class Tree
class Tree:

    def __init__(self):
        self.root = Node()
        self.threshold = 2 # this is hard coded for now

    def overflow(self, node):
        """ overflows a node """

        debug("overflowing node %s with parent %s" % (node, node.parent))
        assert len(node.keys) > self.threshold

        keys = node.keys

        if not node.children:

            # is leaf

            debug ("  is leaf")

            if not node.parent:
                debug("  Creating parent and resetting root")
                node.parent = Node(None)
                self.root = node.parent

            lnode = Node(node.parent)
            rnode = Node(node.parent)

            lnode.prevNode = node.prevNode
            lnode.nextNode = rnode
            rnode.prevNode = lnode
            rnode.nextNode = node.nextNode

            if node.prevNode:
                node.prevNode.nextNode = lnode

            if node.nextNode:
                node.nextNode.prevNode = rnode

            insertPosition = 0

            if node in node.parent.children:
                insertPosition = node.parent.children.index(node)
                node.parent.children.remove(node)

            node.parent.children.insert(insertPosition, rnode)
            node.parent.children.insert(insertPosition, lnode)

            lnode.keys.append(keys[0])
            rnode.keys.append(keys[1])
            rnode.keys.append(keys[2])

            hoist = keys[1]
            node.parent.keys.append(hoist)
            node.parent.keys.sort()

            if len(node.parent.keys) > self.threshold:
                debug("  I noticed my parent looks like %s, so I am overflowing" % node.parent)
                self.overflow(node.parent)

        elif node == self.root:

            # I am root

            debug("  is root")

            # My keys will look like [A|B|C]

            newroot = Node(None)
            newroot.keys.append(keys[1])

            lnode = Node(newroot)
            rnode = Node(newroot)

            lnode.keys.append(keys[0])
            rnode.keys.append(keys[2])

            for child in node.children[:2]:
                lnode.children.append(child)
                child.parent = lnode

            for child in node.children[2:]:
                rnode.children.append(child)
                child.parent = rnode

            newroot.children.append(lnode)
            newroot.children.append(rnode)

            newroot.keys.sort()

            self.root = newroot

        else:

            # internal node

            debug("  internal node")

            lnode = Node(node.parent)
            rnode = Node(node.parent)

            lnode.keys.append(keys[0])
            rnode.keys.append(keys[2])

            for child in node.children[:2]:
                lnode.children.append(child)
                child.parent = lnode

            for child in node.children[2:]:
                rnode.children.append(child)
                child.parent = rnode

            if node in node.parent.children:
                insertPosition = node.parent.children.index(node)
                node.parent.children.remove(node)

            node.parent.children.insert(insertPosition, rnode)
            node.parent.children.insert(insertPosition, lnode)

            hoist = keys[1]
            node.parent.keys.append(hoist)
            node.parent.keys.sort()

            if len(node.parent.keys) > self.threshold:
                self.overflow(node.parent)

    def find1(self, val, node=None):

        # recurse down the right tree path until we hit the
        # leaf node that the value should be in, then return
        # a tuple, t, where t[0] is True or False depending on
        # whether the value was found, and t[1] is the leaf
        # node where the value _should_ have been.

        if node is None:
            node = self.root

        if node.children:

            # non-leaf, we need to work out what child to
            # descend to, and then recurse

            nodeToDescend = 0

            for i, k in enumerate(node.keys):
                if val < k:
                    break
                else:
                    nodeToDescend += 1

            return self.find1(val, node.children[nodeToDescend])

        else:

            # leaf

            if val in node.keys:
                # found it
                return node.keys
            else:
                # it's not in the tree
                return node.keys

    def find(self, val, node=None):

        # recurse down the right tree path until we hit the
        # leaf node that the value should be in, then return
        # a tuple, t, where t[0] is True or False depending on
        # whether the value was found, and t[1] is the leaf
        # node where the value _should_ have been.

        if node is None:
            node = self.root

        if node.children:

            # non-leaf, we need to work out what child to
            # descend to, and then recurse

            nodeToDescend = 0

            for i, k in enumerate(node.keys):
                if val < k:
                    break
                else:
                    nodeToDescend += 1

            return self.find(val, node.children[nodeToDescend])

        else:

            # leaf

            if val in node.keys:
                # found it
                return (True, node)
            else:
                # it's not in the tree
                return (False, node)

    def underflow(self, node):
        """ Handles merging/shrinking of nodes for underflow """

        assert len(node.keys) < self.threshold/2

        # deletion is even more complicated than insertion. Apparently
        # some implementations just recreate the tree from scratch when
        # there are more deleted items than normal ones and don't lose
        # much performance. Since I'm trying to learn though, I guess
        # I'll implement it for real. Here goes.

        debug("Underflowing %s" % node)

        if node == self.root:

            # if root

            debug("  Was root node")

            if len(node.children) == 1:
                self.root = node.children[0]
            elif len(node.children) == 0:
                pass
            else:
                raise Exception("Should we even be here?")

        else:

            # if not root

            # do we have any siblings that have more than the minimum number of keys?

            debug("  Not root.")
            debug("  Going to try looking for siblings")
            dist = lambda x: abs(node.parent.children.index(node) - node.parent.children.index(n))
            siblings = [n for n in node.parent.children if dist(n) == 1]
            candidates = [n for n in siblings if len(n.keys) > (self.threshold/2)]

            assert len(siblings) > 0

            if len(candidates) > 0:

                # found a sibling to borrow from.

                debug("  candidate siblings : %s" % ", ".join([str(s) for s in candidates]))

                candidate = candidates[-1] #  prefer right-appropriation

                if node.parent.children.index(candidate) > node.parent.children.index(node):
                    debug("  this is a right-appropriation")
                    swapper = candidate.keys[0]
                    candidate.keys.remove(swapper)
                    node.keys.append(swapper)
                    debug("  borrowing %s" % swapper)
                    node.parent.keys = [candidate.keys[0]] # this is wrong fix later
                else:
                    debug("  this is a left-appropriation")
                    swapper = candidate.keys[-1]
                    candidate.keys.remove(swapper)
                    node.keys.insert(0, swapper)
                    debug("  borrowing %s" % swapper)
                    node.parent.keys = [swapper] # this is wrong fix later

            else:

                # no candidates. Forced to merge

                debug("  no candidate siblings. Reverting to merge")

                merger = siblings[-1] #  prefer right-merge

                if node.parent.children.index(merger) > node.parent.children.index(node):
                    node.parent.children.remove(node)
                    del node.parent.keys[0]
                else:
                    node.parent.children.remove(node)
                    del node.parent.keys[-1]

                if len(node.parent.keys) < self.threshold/2:
                    self.underflow(node.parent)



    def insert(self, val):

        found, node = self.find(val)
        assert node is not None

        if found:
            return False

        debug("inserting %s into node: %s" % (val, node))

        node.keys.append(val)
        node.keys.sort()

        if len(node.keys) > self.threshold:
            # overflow
            debug("  overflowing")
            self.overflow(node)
        else:
            # no overflow
            debug("  normal insert")

        return True

    def delete(self, val):

        found, node = self.find(val)
        assert node is not None

        if not found:
            return False

        debug("deleting %s from %s" % (val, node))

        node.keys.remove(val)

        if len(node.keys) < self.threshold/2:
            # underflow
            self.underflow(node)
        else:
            # no underflow
            debug("  normal delete")

        return True

    def pretty(self):
        """ Given a tree, prettys it """

        def printNode(n, inc=1):
            print ("%s%s (parent = %s)" % (" "*inc, n, n.parent))
            for c in n.children:
                printNode(c, inc+1)

        # print the tree structure

        print
        print ("-start-")

        printNode(self.root)

        # get the left-most node

        node = self.root
        while node.children:
            node = node.children[0]

        # print the linked-list structure

        nodes = [node]
        while node.nextNode:
            node = node.nextNode
            nodes.append(node)

        print
        print (" -> ".join([str(n) for n in nodes]))

        # get the right-most node

        node = self.root
        while node.children:
            node = node.children[-1]

        # print the linked list structure

        nodes = [node]
        while node.prevNode:
            node = node.prevNode
            nodes.append(node)

        print
    #         print (" -> ".join([str(n) for n in nodes]))

        print
        print ("-end-")

#t = Tree()


def createProduct(request,pk): #pk is seller id
    form = ProductForm()
    index = pk
    # ProductFormSet=inlineformset_factory(Location,Product,fields=('location',),extra=10)
    if request.method == 'POST':
        #print('Printing POST:'request.POST)
        form = ProductForm(request.POST)

        filt = ()
        if form.is_valid():
            form.save()
            a=Product.objects.last()
            a.seller_id=pk
            a.save()
            filt = filtCalculator_P(a.location_id,a.category,a.price,a.depreciation) #产品filt指
            # # return HttpResponse(t.find1())
            newproduct=Product.objects.get(id=a.id)
            newproduct.filt_p= filt
            newproduct.save()
            return redirect('/products/'+str(index)+'/') #传送
    context = {'form':form}
    return render(request, 'accounts/product_form.html', context)

def filtCalculator_P(loc, cat, pro, dep):
    thelocval = 0
    thecatval = 0
    # if (loc == 'Urbana'):
    #     thelocval = 1
    # elif (loc == 'Champaign'):
    #     thelocval = 2
    # elif (loc == 'Springfield'):
    #     thelocval = 3
    if (cat == 'Lifestyle'):
        thecatval = 1
    elif (cat == 'Kitchen'):
        thecatval = 2
    elif (cat == 'Fashion'):
        thecatval = 3
    elif (cat == 'Beauty'):
        thecatval = 4
    elif (cat == 'Study'):
        thecatval = 5
    thevalue = loc * 2 + thecatval * 10 + dep
    # while t.find(thevalue)[0]:
    #     thevalue = thevalue + 0.1
    #t.insert(thevalue)
    return thevalue

    #t.find1()


def products(request,pk):
    # for i in Product.objects.all():
    #     number = filtCalculator_P(i.location_id, i.category, i.price, i.depreciation, t)
    #     i.filt_p= number
    #     i.save()
    seller = Seller.objects.get(id=pk)
    # return HttpResponse(t.find1(seller.filt_c))

    # t = Tree()
    # seller = Seller.objects.get(id=pk)
    # list1 = t.find1(seller.filt_c)
    #return HttpResponse(list1)
    # list1 = t.find1(52.6)
    #return HttpResponse(t.find1(52.6))
    #from list1, which return closest filt_p; we need the product
    # for i in list1:
    #     targetproduct=Product.objects.get(filt_p=i)
    productset = seller.product_set.all()
    myFilter = ProductFilter(request.GET, queryset=productset)#shishikan
    productset = myFilter.qs
    context={'seller':seller, 'productset':productset,'myFilter':myFilter}
    return render(request, 'accounts/products.html',context)

#t = Tree()
def recommand(request,pk):
    t = Tree()
    seller = Seller.objects.get(id=pk)
    allproduct=Product.objects.all()
    for i in allproduct:
        number = filtCalculator_P(i.location_id,i.category,i.price,i.depreciation) #产品filt指
        while t.find(number)[0]:
            number = number + 0.01
        i.filt_p=number
        i.save()
        t.insert(number)
    c=seller.filt_c
    list1 = t.find1(c) # list of recommand products
    #return HttpResponse(list1)

    #return HttpResponse(list1[0])
    productset = []
    for i in list1:
        for j in Product.objects.all():
            if j.filt_p == i:
                # list2.append(j.id)
                productset.append(j)



    # number = filtCalculator_P(i.location_id, i.category, i.price, i.depreciation, t)

    # t = Tree()
    # seller = Seller.objects.get(id=pk)
    # list1 = t.find1(seller.filt_c)
    #return HttpResponse(list1)
    # list1 = t.find1(52.6)
    #return HttpResponse(t.find1(52.6))
    #from list1, which return closest filt_p; we need the product
    # for i in list1:
    # targetproduct=Product.objects.get(filt_p=i)

    #productset =  Product.objects.all()
    context={'productset':productset, 'seller':seller}
    return render(request, 'accounts/recommand.html',context)
