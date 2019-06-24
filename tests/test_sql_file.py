from model.sql_file import SQLFile


def test_parse():
    raw_content = """
    -- some comment
    /* there's something weird with this statement*/
    select current_timestamp;
    /* maybe another
     * comment
     */
    insert into some_table (field1, field2) values ('value1', 'value2');
    select * from some_table where the_comment like '%;%';
    -- another comment
    """
    statements = SQLFile.parse_content(raw_content)
    assert len(statements) == 3
    assert statements[0].strip() == "select current_timestamp"
    assert statements[1].strip() == "insert into some_table (field1, field2) values ('value1', 'value2')"
    assert statements[2].strip() == "select * from some_table where the_comment like '%;%'"
