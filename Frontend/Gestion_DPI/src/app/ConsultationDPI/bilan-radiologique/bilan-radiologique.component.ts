import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';

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
  images:{name:string,url:string}[]= [
    { name: 'image1.png', url: '../../../assets/images/undraw_polaroid_qqdz.png' },
    { name: 'image2.png', url: '../../../assets/images/undraw_polaroid_qqdz.png' },
    { name: 'image3.png', url: '../../../assets/images/undraw_polaroid_qqdz.png' },
     
]
  downloadImage(imageUrl: string, fileName: string): void {
    const link = document.createElement('a'); // Créez un élément <a> dynamiquement
    link.href = imageUrl; // Définit l'URL de l'image
    link.download = fileName; // Définit le nom par défaut pour le téléchargement
    link.click(); // Simule un clic sur le lien pour initier le téléchargement
  }
}
