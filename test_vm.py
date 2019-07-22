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
