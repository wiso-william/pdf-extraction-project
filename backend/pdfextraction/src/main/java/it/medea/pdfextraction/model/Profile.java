package it.medea.pdfextraction.model;


import java.util.Date;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.web.bind.annotation.CrossOrigin;

@Document(collection = "md_dati_estratti")
@Data
@AllArgsConstructor
@NoArgsConstructor
@CrossOrigin(origins = "*")
public class Profile {
	@Id
	private String id;
	
    private String name;
    
    private String surname;
    
    private String codiceFiscale;
    
    private Date birthDate;  
    
    private Integer age;  
    
    private Integer height; // in cm
    
    private Integer weight; // in kg
    
    private String sex; // F o M o O
}
