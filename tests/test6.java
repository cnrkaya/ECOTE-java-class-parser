class Engine{
	private int power;
	public Engine(int power){this.power = power;}
	int getPower(){return power;}
}
class Car{
	private Engine engine;
	public Car( Engine engine ){this.engine = engine;}
	
	int getCarPower(){ return this.engine.getPower(); }
}
