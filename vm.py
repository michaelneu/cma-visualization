import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

OP_PREFIX = "op_"


def op_func_name(op_func):
    return op_func.__name__.split(OP_PREFIX, 1).pop().upper()


def op(*type_casters):
    logger = logging.getLogger()
    def make_op(func):
        #logger.debug("op {} with {} arguments".format(func.__name__, len(type_casters)))
        def call_op(self, *args):
            # TODO: check number of arguments
            cast_args = [c(self, v) for c,v in zip(type_casters, args)]
            return func(self, *cast_args)
        return call_op
    return make_op


def unary_int_op(func):
    @op()
    def unary_op(self):
        x = self._read_sp_rel(0)
        result = int(func(x))
        self.logger.debug(f" <- {result} ({op_func_name(func)} {x})")
        self._write_sp_rel(result, 0)
    return unary_op


def binary_int_op(func):
    @op()
    def binary_op(self):
        x, y = self._read_sp_rel(-1), self._read_sp_rel(0)
        result = int(func(x, y))
        self.logger.debug(f" <- {result} ({op_func_name(func)} {x} {y})")
        self._write_sp_rel(result, -1)
        self._dec_sp()
    return binary_op


def binary_bool_op(func):
    @binary_int_op
    def binary_op(x, y):
        return func(x != 0, y != 0)
    return binary_op


def constant(self, value):
    # TODO: type check
    return int(value)


def address(self, value):
    # TODO: type check / check if label exists
    label_val = str(value).lower()
    if label_val in self.labels:
        return self.labels[label_val]
    return int(value)


class instruction:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def execute(self, vm):
        # TODO: make sure instruction exists
        vm.logger.debug(self.name.upper())
        getattr(vm, OP_PREFIX + self.name)(*self.args)

        
def parse_instruction(args, idx, labels):
    if isinstance(args, instruction):
        return args
    
    if isinstance(args, str):
        args = args.split(' ')

    args = [arg.lower() for arg in args]
    # TODO: boundary check (min 1 element in args)

    if args[0].endswith(':'):
        label = args[0][:-1]
        if label in labels:
            raise Exception("Label used multiple times: " + label)
        labels[label] = idx
        args = args[1:]

    if len(args) == 0:
        args = ['halt']

    return instruction(args[0], args[1:])


class VM:
    def __init__(self, C, memory_size=1024):
        self.logger = logging.getLogger()

        self.labels = {}
        self.C = [parse_instruction(i, idx, self.labels) for idx, i in enumerate(C)] # program store
        self.maxC = len(C) - 1 # max memory address in program store
        self.PC = 0 # program counter
        self.S = [0 for __ in range(memory_size)] # main memory
        self.maxS = memory_size-1 # max memory address in main memory
        self.SP = 0 # stack pointer
        self.halted = False
    
    def _inc_sp(self):
        # TODO: boundary check
        self.SP += 1
    
    def _dec_sp(self):
        # TODO: boundary check
        self.SP -= 1

    def _read(self, idx):
        # TODO: boundary check
        return self.S[idx]

    def _jump(self, a):
        # TODO: boundary check
        self.PC = a

    def _read_sp_rel(self, rel_idx=0):
        return self._read(self.SP + rel_idx)

    def _write(self, value, idx):
        # TODO: value type check
        # TODO: boundary check
        self.S[idx] = value

    def _write_sp_rel(self, value, rel_idx=0):
        self._write(value, self.SP + rel_idx)

    def _push_S(self, value):
        self._inc_sp()
        self._write_sp_rel(value)

    def _get_sp(self):
        return self.SP

    def peek(self):
        """ Return the value on top of the stack. """
        # TODO: boundary check
        return self.S[self.SP]

    def step(self, force=False):
        if self.halted and not force:
            return
        
        # TODO: boundary check
        IR = self.C[self.PC]
        self.PC += 1
        IR.execute(self)
    
    @op()
    def op_halt(self):
        self.halted = True

    @op()
    def op_pop(self):
        self._dec_sp()

    @op()
    def op_load(self):
        a = self._read_sp_rel(0)
        w = self._read(a)
        self._write_sp_rel(w)

    @op()
    def op_store(self):
        w = self._read_sp_rel(-1)
        a = self._read_sp_rel(0)
        self._write(w, a)
        self._dec_sp()

    @op(address)
    def op_jump(self, a):
        self._jump(a)

    @op(address)
    def op_jumpi(self, a):
        q = self._read_sp_rel(0)
        self._jump(a + q)
        self._dec_sp()

    @op(address)
    def op_jumpz(self, a):
        b = self._read_sp_rel(0)
        if not b:
            self._jump(a)
        self._dec_sp()

    @op(constant)
    def op_loada(self, a):
        w = self._read(a)
        self._push_S(w)

    @op(constant)
    def op_storea(self, a):
        w = self._read_sp_rel(0)
        self._write(w, a)
        self._dec_sp()

    @op(constant)
    def op_loadc(self, q):
        self._push_S(q)
    
    @binary_int_op
    def op_add(x, y):
        return x + y
    
    @binary_int_op
    def op_sub(x, y):
        return x - y
    
    @binary_int_op
    def op_mul(x, y):
        return x * y
    
    @binary_int_op
    def op_div(x, y):
        return x // y
    
    @binary_int_op
    def op_mod(x, y):
        return x % y
    
    @binary_bool_op
    def op_and(x, y):
        return x and y
    
    @binary_bool_op
    def op_or(x, y):
        return x or y
    
    @binary_int_op
    def op_eq(x, y):
        return x == y
    
    @binary_int_op
    def op_neq(x, y):
        return x != y
    
    @binary_int_op
    def op_le(x, y):
        return x < y
    
    @binary_int_op
    def op_leq(x, y):
        return x <= y
    
    @binary_int_op
    def op_gr(x, y):
        return x > y
    
    @binary_int_op
    def op_geq(x, y):
        return x >= y

    @unary_int_op
    def op_neg(x):
        return -x

    @unary_int_op
    def op_not(x):
        return not bool(x)
