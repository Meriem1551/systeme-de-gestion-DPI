import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { PageRadiologueService } from '../../services/page-radiologue.service';

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
   isLoading: boolean = false; // Loading indicator
   ngOnInit(): void {
   // const id_bilan = this.data.id_bilan
    // this.pageRadiologueService.updatebilanrad(id_bilan)

   }

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
    private pageRadiologueService : PageRadiologueService,
    @Inject(MAT_DIALOG_DATA) public data: any // Reçoit les données envoyées par le parent
  ) {}

  // Fonction pour envoyer la valeur fixe au parent
  enregistrer() {
    this.isLoading = true; // Active l'indicateur de chargement
    let completedRequests = 0; // Compteur pour suivre les requêtes terminées
    let hasError = false; // Pour suivre les erreurs
  
    // Parcourt chaque fichier et effectue une requête PUT individuelle
    this.files.forEach((file, index) => {
      const formData = new FormData();
      formData.append('compte_rendu', this.compteRendu); // Compte rendu envoyé avec chaque image
      formData.append('image', file); // Ajoute l'image actuelle
  
      // Appelle la méthode updatebilanrad pour chaque fichier
      this.pageRadiologueService
        .updatebilanrad(this.data.element.id_bilanradiologique, formData)
        .subscribe(
          (response) => {
            completedRequests++; // Incrémente le compteur en cas de succès
  
            // Vérifie si toutes les requêtes ont été traitées
            if (completedRequests === this.files.length && !hasError) {
              this.dialogRef.close(this.valeurEnvoyee); // Ferme la boîte de dialogue
            }
          },
          (error) => {
            hasError = true; // Indique une erreur
            console.error(error);
          },
          () => {
            // Désactive l'indicateur de chargement après la dernière requête
            if (completedRequests === this.files.length) {
              this.isLoading = false;
            }
          }
        );
    });
  
    // Si aucun fichier n'est sélectionné, envoie uniquement le compte rendu
    if (this.files.length === 0) {
      const formData = new FormData();
      formData.append('compte_rendu', this.compteRendu); // Envoie uniquement le compte rendu
  
      this.pageRadiologueService
        .updatebilanrad(this.data.element.id_bilanradiologique, formData)
        .subscribe(
          (response) => {
            this.dialogRef.close(this.valeurEnvoyee); // Ferme la boîte de dialogue
          },
          (error) => {
            console.error(error);
          }
        )
        .add(() => (this.isLoading = false)); // Désactive l'indicateur de chargement
    }
  }
  
  }

  