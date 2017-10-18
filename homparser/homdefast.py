import sys


class Node(object):
    __slots__ = ()
    """ Abstract base class for AST nodes.
    """
    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.
            buf:
                Open IO buffer into which the Node is printed.
            offset:
                Initial offset (amount of leading spaces)
            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.
            nodenames:
                True if you want to see the actual node names
                within their parents.
            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)


class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.
        For example:
        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []
            def visit_Constant(self, node):
                self.values.append(node.value)
        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:
        cv = ConstantVisitor()
        cv.visit(node)
        Notes:
        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """
    def visit(self, node):
        """ Visit a node.
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c_name, c in node.children():
            self.visit(c)


class Argument(Node):
    __slots__ = ('type', 'name')

    def __init__(self, type, name):
        self.type = type
        self.name = name


class BinaryExpr(Node):
    __slots__ = ('op', 'lexpr','rexpr')

    def __init__(self, op, lexpr, rexpr):
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr

    def children(self):
        nodelist = []
        if self.lexpr is not None: nodelist.append(("lexpr", self.lexpr))
        if self.rexpr is not None: nodelist.append(("rexpr", self.rexpr))
        return tuple(nodelist)


class UnaryExpr(Node):
    __slots__ = ('op', 'expr')

    def __init__(self, op, e):
        self.op = op
        self.expr = e

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)


class FunctionCall(Node):
    __slots__ = ('name', 'args')

    def __init__(self, funcname, funcargs):
        self.name = funcname
        self.args = funcargs

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.args is not None: nodelist.append(("args", self.args))
        return tuple(nodelist)


class ArrayAccess(Node):
    __slots__ = ('name', 'subscript')

    def __init__(self, arrayname, arraysubscript):
        self.name = arrayname
        self.subscript = arraysubscript

    def children(self):
        nodelist = []
        if self.name is not None: nodelist.append(("name", self.name))
        if self.subscript is not None: nodelist.append(("subscript", self.subscript))
        return tuple(nodelist)

class ConditionalExpression(Node):
    __slots__ = ('condition', 'lexpr', 'rexpr')

    def __init__(self, cond, btrue, bfalse):
        self.condition = cond
        self.lexpr = btrue
        self.rexpr = bfalse


class Block(Node):
    __slots__ = ('statements')

    def __init__(self, statements):
        self.statements = statements


class Assignment(Node):
    __slots__ = ('lvalue', 'rvalue')

    def __init__(self, lval, rval):
        self.lvalue = lval
        self.rvalue = rval

    def children(self):
        nodelist = []
        if self.lvalue is not None: nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None: nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)


class SelectionStatement(Node):
    __slots__ = ('cond', 'thenb', 'elseb')

    def __init__(self, cond, thenb, elseb):
        self.cond = cond
        self.thenb = thenb
        self.elseb = elseb


class IterationStatement(Node):
    __slots__ = ('init', 'guard', 'update', 'body')

    def __init__(self, init, guard, update, body):
        self.init = init
        self.guard = guard
        self.update = update
        self.body = body


class JoinSpec(Node):
    __slots__ = ('argsl', 'argsr', 'returns', 'locals', 'body')

    def __init__(self, argsl, argsr, returns, flocals, body):
        self.argsl = argsl
        self.argsr = argsr
        self.returns = returns
        self.locals = flocals
        self.body = body


class SequentialSpec(Node):
    __slots__ = ('args', 'returns', 'locals', 'body')

    def __init__(self, args, returns, flocals, body):
        self.args = args
        self.returns = returns
        self.locals = flocals
        self.body = body


class Program(Node):
    __slots__ = ('sequential', 'join')

    def __init__(self, seq, join):
        self.sequential = seq
        self.join = join
