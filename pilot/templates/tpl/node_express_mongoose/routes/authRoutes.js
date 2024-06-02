const express = require('express');
const User = require('../models/User');
const bcrypt = require('bcrypt');
const { check, validationResult } = require('express-validator');
const router = express.Router();

const userNameValidationRules = [
  check('username')
    .notEmpty()
    .withMessage('Username is required')
    .isLength({ max: 20 })
    .withMessage('Username must not exceed 20 characters'),
];

const passwordValidationRules = [
  check('password')
    .notEmpty()
    .withMessage('Password is required')
    .isLength({ min: 8, max: 32 })
    .withMessage('Password must be between 8 and 32 characters'),
];

router.get('/auth/register', (req, res) => {
  res.render('register');
});

router.post(
  '/auth/register',
  userNameValidationRules,
  passwordValidationRules,
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).render('register', { errors: errors.array() });
    }

    try {
      const { username, password } = req.body;
      const hashedPassword = await bcrypt.hash(password, 10);
      await User.create({ username, password: hashedPassword });
      res.redirect('/auth/login');
    } catch (error) {
      console.error('Registration error:', error);
      res.status(500).send(error.message);
    }
  }
);

router.get('/auth/login', (req, res) => {
  res.render('login');
});

router.post(
  '/auth/login',
  userNameValidationRules,
  passwordValidationRules,
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).render('login', { errors: errors.array() });
    }

    try {
      const { username, password } = req.body;
      const user = await User.findOne({ username });
      if (!user) {
        return res.status(400).send('User not found');
      }
      const isMatch = await bcrypt.compare(password, user.password);
      if (isMatch) {
        req.session.userId = user._id;
        return res.redirect('/');
      } else {
        return res.status(400).send('Password is incorrect');
      }
    } catch (error) {
      console.error('Login error:', error);
      return res.status(500).send(error.message);
    }
  }
);

router.get('/auth/logout', (req, res) => {
  req.session.destroy(err => {
    if (err) {
      console.error('Error during session destruction:', err);
      return res.status(500).send('Error logging out');
    }
    res.redirect('/auth/login');
  });
});

module.exports = router;


npm install express-validator
