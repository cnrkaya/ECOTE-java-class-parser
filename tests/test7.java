class Superman{
	int health;
	int power;
	
	public Superman(int health, int power) {
		super();
		this.health = health;
		this.power = power;
	}

	void attack(Batman target) {
		target.health -= power;
	}
}

class Batman{
	int health;
	int power;
	
	public Batman(int health, int power) {
		this.health = health;
		this.power = power;
	}

	void attack(Superman target) {
		target.health -= power;
	}
	
}