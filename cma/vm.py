from .visualization import render_vm_state_to_html
import logging
import itertools
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

OP_PREFIX = "op_"


def op_func_name(op_func):
    return op_func.__name__.split(OP_PREFIX, 1).pop().upper()


def op(*type_casters, **kwargs):
    logger = logging.getLogger()
    def make_op(func):
        #logger.debug("op {} with {} arguments".format(func.__name__, len(type_casters)))
        def call_op(self, *args):
            # TODO: check number of arguments
            checked_args = args
            if 'defaults' in kwargs:
                checked_args = [d if v is None else v for v, d in itertools.zip_longest(args, kwargs['defaults'])]
            cast_args = [c(self, v) for c,v in zip(type_casters, checked_args)]
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
        self.FP = 0
        self.S = [0 for __ in range(memory_size)] # main memory
        self.maxS = memory_size-1 # max memory address in main memory
        self.SP = 0 # stack pointer
        self.EP = memory_size // 4
        self.HP = self.maxS
        self.halted = False

    def _set_sp_rel(self, rel_idx):
        # TODO: boundary check
        self.SP += rel_idx

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
        # TODO: boundary check
        self._write(value, self.SP + rel_idx)

    def _push_S(self, value):
        self._inc_sp()
        self._write_sp_rel(value)

    def _get_sp(self):
        return self.SP

    def peek(self, rel_idx=0):
        """ Return the value on top of the stack. """
        # TODO: boundary check
        return self.S[self.SP+rel_idx]

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

    @op(constant, defaults=[1])
    def op_pop(self, m):
        # TODO: range check
        self._set_sp_rel(-m)

    @op(constant, defaults=[1])
    def op_load(self, m):
        a = self._read_sp_rel(0)

        for i in range(m):
            w = self._read(a+i)
            if i > 0:
                self._inc_sp()
            self._write_sp_rel(w)

    @op(constant, defaults=[1])
    def op_store(self, m):
        a = self._read_sp_rel(0)
        for i in range(m):
            w = self._read_sp_rel(i-m)
            self._write(w, a + i)
        self._set_sp_rel(m-1)

    @op()
    def op_dup(self):
        w = self._read_sp_rel(0)
        self._push_S(w)

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

    @op(constant)
    def op_loadrc(self, j):
        self._inc_sp()
        self._write_sp_rel(self.FP + j)

    @op(constant, constant, defaults=[None, 1])
    def op_loadr(self, j, m):
        a = self.FP + j
        for i in range(m):
            w = self._read(a + i)
            self._inc_sp()
            self._write_sp_rel(w)

    @op(constant, constant, defaults=[None, 1])
    def op_storer(self, j, m):
        a = self.FP + j
        for i in range(m):
            w = self._read_sp_rel(i-m)
            self._write(w, a + i)
        self._set_sp_rel(m-1)

    @op()
    def op_new(self):
        n = self._read_sp_rel(0)
        if self.HP - n > self.EP:
            self.HP = self.HP - n
            self._write_sp_rel(self.HP, 0)
        else:
            self._write_sp_rel(0, 0)

    @op()
    def op_mark(self):
        # TODO: boundary checks
        self._write_sp_rel(self.EP, 1)
        self._write_sp_rel(self.FP, 2)
        self._set_sp_rel(2)

    @op()
    def op_call(self):
        # TODO: boundary checks
        self.FP = self.SP
        tmp = self.PC
        self.PC = self._read_sp_rel(0)
        self._write_sp_rel(tmp, 0)

    @op(constant)
    def op_enter(self, m):
        assert m >= 0
        self.EP = self.SP + m
        if self.EP >= self.HP:
            raise Exception("Stack Overflow")

    @op(constant)
    def op_alloc(self, m):
        assert m >= 0
        self.SP = self.SP + m

    @op(constant, constant)
    def op_slide(self, q, m):
        assert q >= 0
        assert m >= 0
        if q > 0:
            if m == 0:
                self.SP = self.SP - q
            else:
                self.SP = self.SP - q - m
                for i in range(m):
                    self._inc_sp()
                    self._write_sp_rel(self._read_sp_rel(q), 0)

    @op(constant)
    def op_return(self, q):
        assert q >= 0
        self.PC = self._read(self.FP)
        self.EP = self._read(self.FP-2)
        if self.EP >= self.HP:
            raise Exception("Stack Overflow")
        self.SP = self.FP - q
        self.FP = self._read(self.FP-1)

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

    def _repr_html_(self):
        return render_vm_state_to_html(self)
