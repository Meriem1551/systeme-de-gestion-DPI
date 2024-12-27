import { Component ,OnInit} from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import { ConsulterDpiService } from '../../services/consulter-dpi.service';

export interface ValeursBio {
  Pression_arterielle: string;
  Glycemie: string;
  Niveau_cholesterol: string;
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
  constructor( private consulterDpiService : ConsulterDpiService ){} ;
   
  ngOnInit(): void {
    this.consulterDpiService.getValeurBio().subscribe((data) => {
      this.valeurs = data ; // Filtrer les éléments qui ont "Ordo" ou "Bilans" égaux à 'oui'
    });
  }
     
}
