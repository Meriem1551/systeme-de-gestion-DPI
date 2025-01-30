import { Component ,OnInit} from '@angular/core';
import { MAT_DIALOG_DATA,MatDialog,MatDialogRef, } from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import { ConsulterDpiService } from '../../services/consulter-dpi.service';

export interface ValeursBio {
  Pression_arterielle: string;
  Glycemie: string;
  Niveau_cholesterol: string;
}

interface ParametreBioMesure {
  bilan_biologique : number ;
  date_mesure:string ;
  id_parametrebiomesure: number;
  nom: string;
  unite_mesure: string;
  valeur_normale: string;
  valeur_mesuree: string;
}
@Component({
  selector: 'app-bilan-biologique',
  imports: [MatDialogContent ,
              MatDialogActions,
              MatDialogClose , 
              MatDialogTitle ,
              CommonModule,
              MatDialogContainer],
  templateUrl: './bilan-biologique.component.html',
  styleUrl: './bilan-biologique.component.css'
})
export class BilanBiologiqueComponent implements OnInit {
  valeurs = {
    Pression_arterielle : '', 
    Glycemie: '',
    Niveau_cholesterol: '',
  }
  constructor(
   public dialogRef: MatDialogRef<BilanBiologiqueComponent>,
   @Inject(MAT_DIALOG_DATA) public data: any, // Injected data
    private consulterDpiService: ConsulterDpiService // Service for API calls
  ) {}



      
      ngOnInit(): void {
        // le ID de la consultation est envoyé de la page du consulter dpi 
        const id_consult = this.data.id_consult; 

        this.consulterDpiService.getBilanBiologiquesByIdConsult(id_consult).subscribe((data) => {
          console.log("dataordo",data);
          // filter les valeurs mésurés pour les afficher 
          data.bilan_biologique.parametre_bio_mesures.forEach((parametre : ParametreBioMesure) => {
           // console.log(parametre.nom); 
            if (this.valeurs.hasOwnProperty(parametre.nom)) {
               if(parametre.nom == "Glycemie"){
              this.valeurs.Glycemie = `${parametre.valeur_mesuree} ${parametre.unite_mesure}`; // Affecte la valeur avec l'unité
               }
           if(parametre.nom == "Pression_arterielle"){
              this.valeurs.Pression_arterielle = `${parametre.valeur_mesuree} ${parametre.unite_mesure}`; // Affecte la valeur avec l'unité
                }
             if(parametre.nom == "Niveau_cholesterol"){
              this.valeurs.Niveau_cholesterol = `${parametre.valeur_mesuree} ${parametre.unite_mesure}`; // Affecte la valeur avec l'unité
               }
          }
        });
          
  
          
        });
      }
  
     
}
