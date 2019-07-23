from vm import VM


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
        'storea %d' % a_ref
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

