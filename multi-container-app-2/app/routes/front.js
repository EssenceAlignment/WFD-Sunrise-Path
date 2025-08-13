const express = require('express');
const Todo = require('./../models/Todo');
const rateLimit = require('express-rate-limit');

const router = express.Router();

// Rate limiter for destructive actions
const destroyLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: "Too many requests, please try again later."
});

// Home page route
router.get('/', async (req, res) => {

    const todos = await Todo.find()
    res.render("todos", {
        tasks: (Object.keys(todos).length > 0 ? todos : {})
    });
});

// POST - Submit Task
router.post('/', (req, res) => {
    const newTask = new Todo({
        task: req.body.task
    });

    newTask.save()
    .then(task => res.redirect('/'))
    .catch(err => console.log(err));
});

// POST - Destroy todo item
router.post('/todo/destroy', destroyLimiter, async (req, res) => {
    const taskKey = req.body._key;
    const err = await Todo.findOneAndRemove({_id: taskKey})
    res.redirect('/');
});


module.exports = router;