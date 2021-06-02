class Pen{
	int price;
	public Pen(int price) {
		this.price = price;
	}	
}
class Pencil{
	int price;
	public Pencil(int price) {
		this.price = price;
	}
}

class Person{
	protected Pen pencil;
	
	public Person(Pen pencil) {
		this.pencil = pencil;
	}
	class Child{
		public Child() {}
		int sayPencilPrice(Pencil pencil){ 
			return pencil.price;
		}
	}
}