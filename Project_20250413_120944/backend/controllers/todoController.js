const Todo = require('../models/Todo');

// Create a new Todo
const createTodo = async (req, res) => {
    const { title } = req.body;
    try {
        const newTodo = await Todo.create({ title });
        res.status(201).json(newTodo);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

// Get all Todos
const getAllTodos = async (req, res) => {
    try {
        const todos = await Todo.find();
        res.status(200).json(todos);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

module.exports = { createTodo, getAllTodos };