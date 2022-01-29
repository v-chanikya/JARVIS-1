package net.codejava.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import net.codejava.entity.user;


@Repository
public interface userRepo extends JpaRepository<user, Long>{
	

}
