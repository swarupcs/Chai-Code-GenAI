import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [todos, setTodos] = useState([]);
    const [title, setTitle] = useState('');

    useEffect(() => {
        fetchTodos();
    }, []);

    const fetchTodos = async () => {
        const response = await axios.get('http://localhost:3000/api/todos');
        setTodos(response.data);
    };

    const addTodo = async () => {
        if (title) {
            await axios.post('http://localhost:3000/api/todos', { title });
            setTitle('');
            fetchTodos();
        }
    };

    return (
        <div>
            <h1>TODO Application</h1>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Add a new todo"
            />
            <button onClick={addTodo}>Add</button>
            <ul>
                {todos.map((todo) => (
                    <li key={todo._id}>{todo.title}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;