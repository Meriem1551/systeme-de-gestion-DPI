import { Component } from '@angular/core';
import { HeaderComponent } from "../header-component/header.component";
import { CreationDPIService } from '../creation-dpi.service';
import { FormsModule } from '@angular/forms'; 

@Component({
  selector: 'app-creation-dpi',
  imports: [HeaderComponent, FormsModule],
  templateUrl: './creation-dpi.component.html',
  styleUrl: './creation-dpi.component.css'
})
export class CreationDPIComponent {
title="Creation du DPI";
labels = ["Nom", "Prenom", "Numero de securité sociale", "Date de naissance", "Adresse", "Téléphone", "Mutuelle", "Medecin traitant", "Personne a contacter"];
buttons = ["Ajouter le DPI", "Annuler"]
names = ["nom", "prenom", "nss", "ddn", "adresse", "num_tel", "mutuelle", "medecin", "contact"];

constructor(private creationDPIService: CreationDPIService) { }


onSubmit(formData: any):void{
  const dpiData = {
    nom_patient: formData.nom,
    prenom_patient: formData.prenom,
    nss: formData.nss,
    date_de_naissance: formData.ddn,
    adresse: formData.adresse,
    telephone: formData.num_tel,
    mutuelle: formData.mutuelle,
    personne_a_contacter: formData.contact,
    nom_complet_medecin: formData.medecin
  };
  this.creationDPIService.createDPI(dpiData).subscribe({
    next: (response) => {
      console.log('DPI créé avec succès:', response);
      localStorage.setItem('dpi_id', response.dpi_id);
      alert('Le dossier a ete cree avec succes');
      window.location.reload();
    },
    error: (err) => {
      console.error('Erreur lors de la création du DPI:', err);
    }
  });


}

}
