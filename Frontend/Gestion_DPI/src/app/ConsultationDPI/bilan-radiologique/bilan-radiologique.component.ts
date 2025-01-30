import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import { MAT_DIALOG_DATA,MatDialog,MatDialogRef, } from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { ConsulterDpiService } from '../../services/consulter-dpi.service';
interface Img {
      bilan_radiologique : number;
      id_image : number ;
      image: string;
}

@Component({
  selector: 'app-bilan-radiologique',
  imports: [MatDialogContent ,
    MatDialogActions,
    MatDialogClose , 
    MatDialogTitle ,
    CommonModule,
    MatDialogContainer],
  templateUrl: './bilan-radiologique.component.html',
  styleUrl: './bilan-radiologique.component.css'
})
export class BilanRadiologiqueComponent {
  description = 'description';
 urlback = 'http://localhost:8000'
  images:{name:string,url:string}[]= [ // le tableau des images médicaux 
   // { name: 'image1.png', url: '../../../assets/images/undraw_polaroid_qqdz.png' },     
]
  downloadImage(imageUrl: string, fileName: string): void {
    const link = document.createElement('a'); // Créez un élément <a> dynamiquement
 
    // Si l'URL est correcte, créer un objet Blob pour le téléchargement
      fetch(imageUrl)
     .then(response => response.blob())  // Récupère le fichier sous forme de Blob
     .then(blob => {
       const url = window.URL.createObjectURL(blob);  // Créer une URL pour le Blob
       link.href = url;
       link.download = fileName;  // Le nom du fichier
       link.click();  // Lance le téléchargement
       window.URL.revokeObjectURL(url);  // Libère l'URL une fois le téléchargement effectué
     })
  .catch(err => console.error('Erreur de téléchargement de l\'image:', err));
  }

  constructor(
         public dialogRef: MatDialogRef<BilanRadiologiqueComponent>,
         @Inject(MAT_DIALOG_DATA) public data: any, // Injected data
         private consulterDpiService: ConsulterDpiService // Service for API calls
       ) {}
      
      ngOnInit(): void {
        const id_consult = this.data.id_consult; 
        // récupérer les données (l'ordonnance) du backend 
        this.consulterDpiService.getBilanRadiologiquesByIdConsult(id_consult).subscribe((data) => {
          console.log("databilanrad",data);
          this.description = data.bilan_radiologique.compte_rendu ;
          data.bilan_radiologique.images.forEach((img : Img)=>{
            // Extraire le nom de l'image
            const nomimage = img.image.split('/').pop()!;
            const urlimage = `${this.urlback}${img.image}`
            this.images.push({ name: nomimage, url: urlimage });
          })
          
          
          
        });
      }
}
