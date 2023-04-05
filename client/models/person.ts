import mongoose from "mongoose";
import uniqueValidator from "mongoose-unique-validator";

// Un schema es muy similar a definir un type en graphQL. Aun así, tienen sus
// diferencias y es muy importante mantenerlos separados por si en un futuro
// queremos dejar de usar GraphQL. Las validaciones tienen que existir y tienen
// que estar.

const schema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    unique: true,
  },
  age: {
    type: Number,
    required: true,
  },
  email: {
    type: String,
    required: true,
  },
});

schema.plugin(uniqueValidator);

export default mongoose.model("Person", schema);
