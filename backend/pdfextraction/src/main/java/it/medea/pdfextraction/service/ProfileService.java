package it.medea.pdfextraction.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import it.medea.pdfextraction.model.Profile;
import it.medea.pdfextraction.model.ProfilePatchDTO;
import it.medea.pdfextraction.repository.ProfileRepository;

@Service
public class ProfileService {
    @Autowired
    private ProfileRepository profileRepository;

    public List<Profile> allProfiles() {
        return profileRepository.findAll();
    }

    public Optional<Profile> singleProfile(String id) { 
        return profileRepository.findById(id);
    }

    public Profile createProfile(Profile profile) {
        return profileRepository.save(profile);
    }

    public Profile updateProfile(String id, Profile updatedProfile) {  
        Profile existingProfile = profileRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Profilo non trovato con ID: " + id));
        
        existingProfile.setName(updatedProfile.getName());
        existingProfile.setSurname(updatedProfile.getSurname());
	    existingProfile.setCodiceFiscale(updatedProfile.getCodiceFiscale());
	    existingProfile.setBirthDate(updatedProfile.getBirthDate());
	    existingProfile.setSex(updatedProfile.getSex()); 
	    existingProfile.setAge(updatedProfile.getAge());
	    existingProfile.setHeight(updatedProfile.getHeight()); // Controllare
	    existingProfile.setWeight(updatedProfile.getHeight()); // Controllare
        return profileRepository.save(existingProfile);
    }

    public Profile patchProfile(String id, ProfilePatchDTO partialProfile) {  
        Profile existingProfile = profileRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Profilo non trovato con ID: " + id));
        
        Optional.ofNullable(partialProfile.getName()).ifPresent(existingProfile::setName);
        Optional.ofNullable(partialProfile.getSurname()).ifPresent(existingProfile::setSurname);
        Optional.ofNullable(partialProfile.getCodiceFiscale()).ifPresent(existingProfile::setCodiceFiscale);
        Optional.ofNullable(partialProfile.getBirthDate()).ifPresent(existingProfile::setBirthDate);
        Optional.ofNullable(partialProfile.getAge()).ifPresent(existingProfile::setAge);
        Optional.ofNullable(partialProfile.getHeight()).ifPresent(existingProfile::setHeight);
        Optional.ofNullable(partialProfile.getWeight()).ifPresent(existingProfile::setWeight);
        Optional.ofNullable(partialProfile.getSex()).ifPresent(existingProfile::setSex);
        return profileRepository.save(existingProfile);
    }
}
