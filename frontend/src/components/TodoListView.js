import TodoItem from './Todo';


function TodoView(props) {
  return (
    <div>
      <ul>
        {props.todoList.map((todo, index) =>
           <li key={index}>
            <TodoItem todo={todo} />
           </li>
        )}
      </ul>
    </div>
  )
}

export default TodoView;
