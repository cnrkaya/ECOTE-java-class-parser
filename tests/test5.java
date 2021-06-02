
class Birthday{
	public int year; 
	public int month;
	public int day;
	public Birthday(int year, int month, int day) {
		this.year = year;
		this.month = month;
		this.day = day;
	}
}

class Person{
	public Birthday bday;
	public Person(Birthday bday) {
		this.bday = bday;
	}
	public boolean isAdult() {
		if(this.bday.year + 18 > 2021) {
			return true;
		}
		return false;
	}
}


class ChildProfile {
	public String authority;
	public ChildProfile() {
		authority = "Cartoons";
	}
}

class AdultProfile{
	public String authority;	
	public AdultProfile() {
		authority = "All Content";
	}
}

class User{
	Person person;
	public User(Person person) {
		this.person = person;
		boolean isAdult = person.isAdult();

		if(isAdult){
			AdultProfile aProfile = new AdultProfile();
			System.out.println(aProfile.authority);
		}else {
			ChildProfile cProfile = new ChildProfile();
			System.out.println(cProfile.authority);
		}
	}
	
}
