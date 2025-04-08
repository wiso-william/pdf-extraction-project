package it.medea.pdfextraction.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import it.medea.pdfextraction.model.Profile;

@Repository
public interface ProfileRepository extends MongoRepository<Profile, String> {}
