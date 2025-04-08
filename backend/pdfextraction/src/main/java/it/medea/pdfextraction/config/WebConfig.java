package it.medea.pdfextraction.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // Consente CORS su tutte le rotte
                .allowedOrigins("http://localhost:5173") // Permette solo le richieste da React su localhost:3000
                .allowedMethods("GET", "POST", "PUT", "DELETE") // Metodi HTTP consentiti
                .allowedHeaders("*"); // Permette qualsiasi header
    }
}

