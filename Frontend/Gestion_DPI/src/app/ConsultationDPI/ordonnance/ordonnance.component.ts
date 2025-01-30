import { Component , OnInit } from '@angular/core';
import { MAT_DIALOG_DATA,MatDialog,MatDialogRef, } from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';
import {MatTableModule } from '@angular/material/table';
import { ListMeds , ConsulterDpiService } from '../../services/consulter-dpi.service';


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
    constructor(
       public dialogRef: MatDialogRef<OrdonnanceComponent>,
       @Inject(MAT_DIALOG_DATA) public data: any, // Injected data
       private consulterDpiService: ConsulterDpiService // Service pour les appels API
     ) {}
    
    ngOnInit(): void {
      const id_consult = this.data.id_consult; 
      // récupérer les données (l'ordonnance) du backend 
      this.consulterDpiService.getListMeds(id_consult).subscribe((data) => {
        console.log("dataordo",data);

        this.dataSource = data ; 
      });
    }


 
 

}
