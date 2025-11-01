from fastmcp import FastMCP
from typing import Annotated, NamedTuple

from todo_db import TodoDB

todo_db = TodoDB(db_file='/Users/johnyong/workspace/geekshacking/mcp/tasks.json')
# todo_db.sample_data()

class Todo(NamedTuple):
    filename: Annotated[str, 'Source file containing the #TODOs']
    text: Annotated[str, 'Text of the #TODO']
    line_num: Annotated[int, 'Line number of the #TODO in the source file']

mcp = FastMCP('TODO-MCP')


@mcp.tool(
        name='tool_add_todo', 
        description='Add a single #TODO text from a source file.'
)
def add_todo(
        filename: Annotated[str, 'Source file containing the #TODO'],
        text: Annotated[str, 'Text of the #TODO'],
        line_num: Annotated[int, 'Line number of the #TODO in the source file']
) -> bool:
    return todo_db.add(filename=filename, text=text, line_num=line_num)


@mcp.tool(
        name='tool_add_todos', 
        description='Add multiple #TODO texts from a source file.'
)
def add_todos(
        todos: Annotated[list[Todo], 'List of #TODOs to add, each containing the filename, text and line number of the #TODO in the soruce file']
) -> int:
    for todo in todos:
        todo_db.add(filename=todo.filename, text=todo.text, line_num=todo.line_num)
    return len(todos)


@mcp.resource(
        name='resource_get_todos_for_file',
        description='Get all todos from a file. Returns an empty array if source file does not exist or there are no #TODOs in the file.',
        uri='todo://{filename}/todos'
)
def get_todos_for_file(
        filename: Annotated[str, 'Source file containing the #TODO']
) -> list[str]:
    todos = todo_db.get(filename=filename)
    return [text for text in todos.values()]


def run():
    mcp.run()


if __name__ == '__main__':
    run()
