class Contact{
	public String address;
	public String telephoneNumber;
	public String email;
	public Contact(String address, String telephoneNumber, String email) {
		this.address = address;
		this.telephoneNumber = telephoneNumber;
		this.email = email;
	}
}

class Person{
	public String nameSurname;
	public Contact contact;
	public Person(String nameSurname, Contact contact) {
		super();
		this.nameSurname = nameSurname;
		this.contact = contact;
	}
	void changeEmail(String newEmail) {
		this.contact.email = newEmail;}
}
