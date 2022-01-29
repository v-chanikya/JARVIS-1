package net.codejava.controller;

import java.sql.Date;
import java.text.SimpleDateFormat;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import net.codejava.entity.user;
import net.codejava.exception.ResourceNotFound;
import net.codejava.repository.userRepo;


@RestController
@RequestMapping("/api/users")
public class userController {
	
	@Autowired
	private userRepo userrepo;
	
	// get all users
	@GetMapping
	public List<user> getAllUsers(){
		return this.userrepo.findAll();
	}
	
	// get user by id
	@GetMapping("/{id}")
	public user getUserById(@PathVariable (value = "id") long userId){
		return this.userrepo.findById(userId).orElseThrow(() -> new ResourceNotFound("User not found for id " + userId));
	}
	// save use
	@PostMapping
	public user createUser(@RequestBody user User) {
		SimpleDateFormat formatter= new SimpleDateFormat("yyyy-MM-dd 'at' HH:mm:ss z");
		Date date = new Date(System.currentTimeMillis());
		System.out.println(formatter.format(date));
		User.setDate(formatter.format(date));
		return this.userrepo.save(User);
	}
	
	// update user by id
	@PutMapping("/{id}")
	public user updateUser(@RequestBody user User, @PathVariable ("id") long userId) {
		user existing = this.userrepo.findById(userId).orElseThrow(() -> new ResourceNotFound("User not found for id " + userId)); 
		existing.setUsername(User.getUsername());
		existing.setPassword(User.getPassword());
		existing.setDate(User.getDate());
		existing.setActionPerformed(User.getActionPerformed());
		existing.setSearchedData(User.getSearchedData());
		return this.userrepo.save(existing);
	}
	
	// delete user by id 
	@DeleteMapping(("/{id}"))
	public ResponseEntity<user> deleteUser( @PathVariable ("id") long userId){
		user existing = this.userrepo.findById(userId).orElseThrow(() -> new ResourceNotFound("User not found for id " + userId)); 
		this.userrepo.delete(existing);
		return ResponseEntity.ok().build();
		
	}
	

}
