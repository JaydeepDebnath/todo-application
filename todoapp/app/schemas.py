type Todo{
    id : id
    title:String
    description:String
    createdAt:String
    updatedAt:String
}

type Query{
    todos : [Todo!]!
    todo(id:ID!):Todo
}

type Mutation{
    todo_creation(title:String!,description:String,createdAt:String,updatedAt:String):Todo!
    update_todo(id:ID!,title:String!,description:String,createdAt:String,updatedAt:String):Todo
    delete_todo(id:ID!):Todo
}