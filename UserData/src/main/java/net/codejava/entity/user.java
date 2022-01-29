package net.codejava.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "users", schema = "myapp")


public class user {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(columnDefinition = "serial")
	private long id;
	
	@Column (name = "username")
	private String username;
	
	@Column (name = "password")
	private String password;
	
	@Column (name = "date")
	private String date;
	
	@Column (name = "action_performed")
	private String actionPerformed;
	
	@Column (name = "searched_data")
	private String searchedData;
	
	// Constructor 
	public user(String username, String password, String date, String actionPerformed, String searchedData) {
		super();
		this.username = username;
		this.password = password;
		this.date = date;
		this.actionPerformed = actionPerformed;
		this.searchedData = searchedData;
	}
	public user()
	{
		
	}
	
	// Setters and Getter of the fields
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	public String getDate() {
		return date;
	}
	public void setDate(String date) {
		this.date = date;
	}
	public String getActionPerformed() {
		return actionPerformed;
	}
	public void setActionPerformed(String actionPerformed) {
		this.actionPerformed = actionPerformed;
	}
	public String getSearchedData() {
		return searchedData;
	}
	public void setSearchedData(String searchedData) {
		this.searchedData = searchedData;
	}
	
	
	
	

}
