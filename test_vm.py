from vm import VM


def test_instruction_halt():
    vm = VM(['halt'])
    assert not vm.halted
    vm.step()
    assert vm.halted
