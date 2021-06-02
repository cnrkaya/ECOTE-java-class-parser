class Engine{
	private int power;
	public Engine(int power){this.power = power;}
	int getPower(){return power;}
}
class Car{
	public Car( Engine engine ){this.engine = engine;}
	void setEngine(int power){
		Engine myEngine = new Engine(power);
		System.out.print(myEngine.power);
	}
}
