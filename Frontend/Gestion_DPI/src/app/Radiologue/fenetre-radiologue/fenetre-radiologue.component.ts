import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-fenetre-radiologue',
  imports: [MatDialogContent ,
    MatDialogActions,
    MatDialogClose , 
    MatDialogTitle ,
    CommonModule,
    FormsModule,
    MatDialogContainer],
  templateUrl: './fenetre-radiologue.component.html',
  styleUrl: './fenetre-radiologue.component.css'
})
export class FenetreRadiologueComponent {
  
  files: File[] = []; // Liste des fichiers sélectionnés
   compteRendu : string ='';
  // Gestionnaire pour sélectionner plusieurs fichiers
  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      // Ajoute les nouveaux fichiers sélectionnés à la liste existante
      Array.from(input.files).forEach(file => {
        this.files.push(file);
      });
    }
  }

  // Fonction simulée pour uploader les fichiers (peut être reliée au backend)
  uploadFiles() {
    if (this.files.length > 0) {
      console.log('Fichiers sélectionnés :', this.files);
      alert(`${this.files.length} fichier(s) chargé(s) avec succès !`);
    } else {
      alert('Aucun fichier sélectionné.');
    }
  }

   // Supprimer un fichier sélectionné
   removeFile(index: number) {
    this.files.splice(index, 1);
  }
  annuler(){
    this.files.splice(0, this.files.length);
    this.compteRendu ='';
  }

  valeurEnvoyee: string = "oui"; 

  constructor(
    public dialogRef: MatDialogRef<FenetreRadiologueComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any // Reçoit les données envoyées par le parent
  ) {}

  // Fonction pour envoyer la valeur fixe au parent
  enregistrer() {
    this.dialogRef.close(this.valeurEnvoyee); // Envoie "oui" au parent
  }
}
  