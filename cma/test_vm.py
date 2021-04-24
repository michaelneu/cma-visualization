from .vm import VM


def _test_binary_op(op_name, x, y, z):
    instructions = [
        'loadc %d' % x,
        'loadc %d' % y,
        op_name
    ]
    # TODO: add additional state checks
    vm = VM(instructions)
    for _ in range(len(instructions)):
        vm.step()
    assert vm._get_sp() == 1
    assert vm.peek() == z


def _test_unary_op(op_name, x, z):
    instructions = [
        'loadc %d' % x,
        op_name
    ]
    # TODO: add additional state checks
    vm = VM(instructions)
    for _ in range(len(instructions)):
        vm.step()
    assert vm._get_sp() == 1
    assert vm.peek() == z


def test_instruction_halt():
    vm = VM(['halt'])
    assert not vm.halted
    vm.step()
    assert vm.halted


def test_instruction_add():
    _test_binary_op('add', 1, 2, 3)


def test_instruction_sub():
    _test_binary_op('sub', 5, 4, 1)


def test_instruction_mul():
    _test_binary_op('mul', 3, 4, 12)


def test_instruction_div():
    _test_binary_op('div', 42, 2, 21)


def test_instruction_mod():
    _test_binary_op('mod', 7, 3, 1)


def test_instruction_and():
    _test_binary_op('and', 0, 0, 0)
    _test_binary_op('and', 0, 1, 0)
    _test_binary_op('and', 1, 0, 0)
    _test_binary_op('and', 1, 1, 1)


def test_instruction_or():
    _test_binary_op('or', 0, 0, 0)
    _test_binary_op('or', 0, 1, 1)
    _test_binary_op('or', 1, 0, 1)
    _test_binary_op('or', 1, 1, 1)


def test_instruction_eq():
    _test_binary_op('eq', 42, 0, 0)
    _test_binary_op('eq', 42, 42, 1)


def test_instruction_neq():
    _test_binary_op('neq', 42, 0, 1)
    _test_binary_op('neq', 42, 42, 0)


def test_instruction_le():
    _test_binary_op('le', 42, 0, 0)
    _test_binary_op('le', 42, 42, 0)
    _test_binary_op('le', 0, 42, 1)


def test_instruction_leq():
    _test_binary_op('leq', 42, 0, 0)
    _test_binary_op('leq', 42, 42, 1)
    _test_binary_op('leq', 0, 42, 1)


def test_instruction_gr():
    _test_binary_op('gr', 42, 0, 1)
    _test_binary_op('gr', 42, 42, 0)
    _test_binary_op('gr', 0, 42, 0)


def test_instruction_geq():
    _test_binary_op('geq', 42, 0, 1)
    _test_binary_op('geq', 42, 42, 1)
    _test_binary_op('geq', 0, 42, 0)


def test_instruction_neg():
    _test_unary_op('neg', 42, -42)
    _test_unary_op('neg', -42, 42)


def test_instruction_not():
    _test_unary_op('not', 0, 1)
    _test_unary_op('not', 1, 0)


def test_store_and_load():
    # a <- (b + (b * c)) with {&a = 5, &b = 6, &c = 7}
    a_ref, b_ref, c_ref = 5, 6, 7

    instructions = [
        'loadc %d' % b_ref,
        'load',
        'loadc %d' % b_ref,
        'load',
        'loadc %d' % c_ref,
        'load',
        'mul',
        'add',
        'loadc %d' % a_ref,
        'store'
    ]
    # TODO: add additional state checks

    b_val, c_val = 7, 13

    vm = VM(instructions)
    vm._write(b_val, b_ref)
    vm._write(c_val, c_ref)
    for _ in range(len(instructions)):
        vm.step()
    a_val = vm._read(a_ref)
    assert a_val == b_val + b_val * c_val


def test_storea_and_loada():
    # a <- (b + (b * c)) with {&a = 5, &b = 6, &c = 7}
    a_ref, b_ref, c_ref = 5, 6, 7

    instructions = [
        'loada %d' % b_ref,
        'loada %d' % b_ref,
        'loada %d' % c_ref,
        'mul',
        'add',
        'storea %d' % a_ref,
        'pop'
    ]
    # TODO: add additional state checks

    b_val, c_val = 7, 13

    vm = VM(instructions)
    assert vm._get_sp() == 0
    vm._write(b_val, b_ref)
    vm._write(c_val, c_ref)
    for _ in range(len(instructions)):
        vm.step()
    assert vm._get_sp() == 0
    a_val = vm._read(a_ref)
    assert a_val == b_val + b_val * c_val


def test_loadc():
    c = 42
    instructions = [
        'loadc %d' % c
    ]
    # TODO: add additional state checks

    vm = VM(instructions)
    assert vm._get_sp() == 0
    for _ in range(len(instructions)):
        vm.step()
    assert vm._get_sp() == 1
    assert vm.peek() == c


def test_pop():
    instructions = [
        'loadc 42',
        'pop'
    ]
    # TODO: add additional state checks

    vm = VM(instructions)
    assert vm._get_sp() == 0
    for _ in range(len(instructions)):
        vm.step()
    assert vm._get_sp() == 0


def test_jump_and_jumpz():
    # if (x > y)
    #  x <- x - y;
    # else
    #  y <- y - x;
    x_ref, y_ref = 4, 7

    instructions = [
        'loada 4',
        'loada 7',
        'gr',
        'jumpz A',
        'loada 4',
        'loada 7',
        'sub',
        'storea 4',
        'pop',
        'jump B',
        'A: loada 7',
        'loada 4',
        'sub',
        'storea 7',
        'pop',
        'B:'
    ]

    x_val, y_val = 4, 3
    vm = VM(instructions)
    assert vm._get_sp() == 0
    vm._write(x_val, x_ref)
    vm._write(y_val, y_ref)
    while not vm.halted:
        vm.step()
    x, y = x_val, y_val
    x_val = vm._read(x_ref)
    assert x_val == x - y  # 4 > 3 => x = x - y

    x_val, y_val = 3, 4
    vm = VM(instructions)
    assert vm._get_sp() == 0
    vm._write(x_val, x_ref)
    vm._write(y_val, y_ref)
    while not vm.halted:
        vm.step()
    x, y = x_val, y_val
    y_val = vm._read(y_ref)
    assert y_val == y - x  # !(4 > 3) => y = y - x


def test_jumpi():
    # TODO
    pass


def test_dup():
    # TODO
    instructions = [
        'loadc 42',
        'dup'
    ]
    vm = VM(instructions)
    assert vm._get_sp() == 0
    for _ in range(len(instructions)):
        vm.step()
    assert vm._get_sp() == 2
    assert vm._read(1) == 42
    assert vm._read(2) == 42
    pass


def test_store_and_load_m():
    # a <- (b + (b * c)) with {&a = 5, &b = 6, &c = 7}
    a_ref, b_ref, c_ref = 5, 6, 7

    instructions = [
        'loadc %d' % b_ref,
        'load',
        'loadc %d' % b_ref,
        'load 2',
        'mul',
        'add',
        'dup',
        'dup',
        'loadc %d' % a_ref,
        'store 3'
    ]
    # TODO: add additional state checks

    b_val, c_val = 7, 13

    vm = VM(instructions)
    vm._write(b_val, b_ref)
    vm._write(c_val, c_ref)
    for _ in range(len(instructions)):
        vm.step()
    a = vm._read(a_ref)
    b = vm._read(b_ref)
    c = vm._read(c_ref)
    assert a == b_val + b_val * c_val
    assert b == b_val + b_val * c_val
    assert c == b_val + b_val * c_val


def test_new():
    instructions = [
        'loadc 5',
        'new',
        'loadc 10',
        'new',
        'loadc 1',
        'new'
    ]
    vm = VM(instructions)
    for _ in range(len(instructions)):
        vm.step()
    a_ref = vm.peek(-2)
    b_ref = vm.peek(-1)
    c_ref = vm.peek(0)

    assert a_ref > vm.EP
    assert b_ref > vm.EP
    assert c_ref > vm.EP
    assert vm.maxS - a_ref == 5
    assert a_ref - b_ref == 10
    assert b_ref - c_ref == 1
