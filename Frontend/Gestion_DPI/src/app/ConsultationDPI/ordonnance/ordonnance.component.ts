import { Component , OnInit } from '@angular/core';
//import { MAT_DIALOG_DATA,MatDialog } from '@angular/material/dialog';
//import { Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import {MatTableModule} from '@angular/material/table';
import { ListMeds , ConsulterDpiService } from '../../services/consulter-dpi.service';
/*
export interface meds {
Medicament : string ;
Dose : string ;
Duree : string ;

}
const ELEMENT_DATA_med : meds[] = [
  {
    Medicament: 'Paracétamol',Dose: '500mg',Duree: '3 fois par jour pendant 5 jours'
  },
  {
    Medicament: 'Ibuprofène',Dose: '200mg',Duree: '2 fois par jour pendant 7 jours'
  },
  {
    Medicament: 'Amoxicilline',Dose: '250mg', Duree: '3 fois par jour pendant 7 jours'
  }
];*/

@Component({
  selector: 'app-ordonnance',
  imports: [MatDialogContent ,
            MatDialogActions,
            MatDialogClose , 
            MatDialogTitle ,
            MatTableModule,
            CommonModule,
            MatDialogContainer],
  templateUrl: './ordonnance.component.html',
  styleUrl: './ordonnance.component.css'
})
export class OrdonnanceComponent implements OnInit{

  dataSource : ListMeds[]=[];
  displayedColumns: string[] = [ 'Medicament','Dose', 'Duree'];
    constructor( private consulterDpiService : ConsulterDpiService ){} ;
    
    ngOnInit(): void {
      this.consulterDpiService.getListMeds().subscribe((data) => {
        this.dataSource = data ; // Filtrer les éléments qui ont "Ordo" ou "Bilans" égaux à 'oui'
      });
    }


 
 

}
