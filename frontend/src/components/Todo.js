import axios from 'axios';
import React from 'react';

function TodoItem(props) {
  const deleteTodoHandler = (title) => {
    axios.delete(`http://localhost:8000/api/todo${title}`)
      .then(res => console.log(res.data))
      .catch(error => {
        if(error.response) {
          console.log(`My title is: ${title}`)
          console.log(`My error is: ${Object.keys(error.response)}`)
          console.log(`My error is: ${Object.values(error.response)}`)
        }
      })
    }
  return (
    <div>
      <p>
        <span style={{ fontWeight: 'bold, underline' }}>{props.todo.title} : </span> {props.todo.description}

        <button onClick={() => deleteTodoHandler(props.todo.title)}
                className="btn btn-danger btn-sm my-2 mx-2"
                style={{'borderRadius':'50px'}}></button>
      </p>
      <hr></hr>
    </div>
  )
}

export default TodoItem;
