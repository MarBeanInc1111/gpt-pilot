const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    unique: true,
    required: true,
    minlength: 3,
    maxlength: 32
  },
  password: {
    type: String,
    required: true,
    minlength: 8,
    maxlength: 1024
  },
  passwordConfirmation: {
    type: String,
    required: true,
    validate: {
      validator: function(value) {
        return value === this.password;
      },
      message: 'Passwords do not match'
    }
  }
});

userSchema.pre('save', async function(next) {
  const user = this;
  if (!user.isModified('password')) return next();
  const saltRounds = 10;
  try {
    const hash = await bcrypt.hash(user.password, saltRounds);
    user.password = hash;
    user.passwordConfirmation = undefined;
    next();
  } catch (err) {
    console.error('Error hashing password:', err);
    return next(err);
  }
});

userSchema.methods.comparePassword = function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

const User = mongoose.model('User', userSchema);

module.exports = User;
