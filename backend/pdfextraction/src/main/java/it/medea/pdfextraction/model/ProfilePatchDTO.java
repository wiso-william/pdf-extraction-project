package it.medea.pdfextraction.model;

import java.util.Date;

import org.springframework.web.bind.annotation.CrossOrigin;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@CrossOrigin(origins = "*")
public class ProfilePatchDTO {
	private String id;
    private String name;
    private String surname;
    private String codiceFiscale;
    private Date birthDate;
    private Integer age;
    private Integer height;
    private Integer weight;
    private String sex;
}