struct Figure(){
    let field = 0
}

struct Rectangle(Figure){
    let a = 2
    let b = 3
}

impl Rectangle(Figure){
    func calcField(count){
        self.field = self.a*self.b*count
        return self.field
    }
}

let rect = alloc Rectangle

return "Field is equal to: " + rect.calcField(3)