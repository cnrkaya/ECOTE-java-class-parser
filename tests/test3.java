class Bill{
	public float amount;
	public Bill(float amount){this.amount = amount; }
}
class Client{
	private float balance;
	public Client (float balance){this. balance = balance; }
	boolean payBill( Bill bill){
		if( balance >= bill.amount){
			balance -= bill.amount;
			return true;
		}
		return false;
	}
}
