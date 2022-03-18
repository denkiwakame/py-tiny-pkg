def test_import():
    from tinypkg.hi import hi
    assert hi() == '\U0001F40D'
