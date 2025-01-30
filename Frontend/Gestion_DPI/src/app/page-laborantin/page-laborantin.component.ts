import {ChangeDetectionStrategy, Component, inject, model, signal, AfterViewInit} from '@angular/core';import { HeaderComponent } from '../header-component/header.component';
import {FormControl, Validators, FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {MatFormFieldModule} from '@angular/material/form-field';
import { CommonModule } from '@angular/common';
import {MatTableModule} from '@angular/material/table';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatButtonModule} from '@angular/material/button';
import {OnInit } from '@angular/core';
import { LaborantinService } from '../laborantin.service';
import { Inject } from '@angular/core';
import { Chart,CategoryScale,BarController, LinearScale, BarElement, Title, Tooltip, Legend, UpdateModeEnum, ChartOptions,ChartConfiguration,} from 'chart.js';
import {
  MAT_DIALOG_DATA,
  MatDialog,
  MatDialogActions,
  MatDialogClose,
  MatDialogContent,
  MatDialogRef,
  MatDialogTitle,
} from '@angular/material/dialog';
import { ChangeDetectorRef } from '@angular/core';

import { ColdObservable } from 'rxjs/internal/testing/ColdObservable';

interface Patient{
  nom:string,
  prenom: string,
  id_dpi: number,
  bilans: Bilan[],
}

interface Bilan{
  blan_id:number,
  description: string,
  remplit: string,
}

@Component({
  selector: 'app-page-laborantin',
  imports: [HeaderComponent,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    MatInputModule,
    CommonModule,
    MatTableModule,
    ReactiveFormsModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './page-laborantin.component.html',
  styleUrl: './page-laborantin.component.css',
})


export class PageLaborantinComponent implements OnInit{
  patients: Patient[] = [];
  patientControl = new FormControl(null, Validators.required);
  patientSelecione: any;
  displayedColumns: string[] = ['description', 'resultat',];
  dataSource : any[] =[];
selectedBilanId: number | null = null;
  constructor(private laborantinService: LaborantinService,   private cdr: ChangeDetectorRef){}

  ngOnInit(): void {
    this.fetchPatients();
  }
  fetchPatients(): void {
    this.laborantinService.getPatientList().subscribe({
      next: (data) => {
        this.patients = data.map((item: any) => ({
          nom: item.utilisateur.last_name,
          prenom: item.utilisateur.first_name,
          id_dpi: item.id_dpi,
          bilans: [],
        }
      ));
    },
      error: (err) => console.error('Error fetching patients:', err),
    });
  }
  loadPatientData(): void {
    // Get the selected patient from the dropdown
    this.patientSelecione = this.patientControl.value;

    if (this.patientSelecione) {
      // Fetch bilans for the selected patient
      this.laborantinService.getBilanList(this.patientSelecione.id_dpi).subscribe({
        next: (data) => {
          // Map bilans and set as dataSource
          this.dataSource = data.map((item: any) => ({
            description: item.bilan.description,
            remplit: item.bilan.laborantin !== null,
            bilan_id: item.bilan.id_bilanbiologique,
          }));
          this.cdr.detectChanges();
        },
        error: (err) => console.error('Error fetching bilans for patient', err),
      });
    } else {
      // Clear dataSource if no patient is selected
      this.dataSource = [];
    }
  }



  clickedRows = new Set<any>();
  trackByPatient(index: number, patient: any): string {
    return `${patient.nom}-${patient.prenom}`; 
  }

  


// //AFFICHER LES FENETRES

  readonly dialog = inject(MatDialog);

  openDialog_remplirResultat(row: any): void {
    const dialogRef = this.dialog.open(RemplirResultat, {
      width: '80vw',
      height: 'auto',
      maxWidth: '80vw',
      data: { bilan_id: row.bilan_id, id_dpi: this.patientSelecione.id_dpi, }, // Pass bilan_id here
    });
  
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
  
}
@Component({
  selector: 'dialog-remplir-resultat',
  templateUrl: 'dialog-remplir-resultat.html',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
    MatExpansionModule,
    CommonModule,
    MatButtonModule
  ],
})


//REMPLIR RESULTATS
export class RemplirResultat {
  readonly dialogRef = inject(MatDialogRef<RemplirResultat>);
  readonly data = inject(MAT_DIALOG_DATA);

  params: { name: string; id: number }[] = [
    { id: 1, name:'Pression_arterielle' },
    { id: 2, name: 'Glycemie' },
    { id: 3, name: 'Niveau_cholesterol' },
  ];
   divs: { id: number; parametre: string; valeur: string ; date: string}[] = [];
   nextId = 1;
   isDisable: boolean = true; 

   constructor(private laborantinUpdate: LaborantinService){};
  
   onNoClick(): void {
    this.dialogRef.close();
  }
  readonly panelOpenState = signal(false);

  ajouter() {
    this.divs.push({ id: this.nextId++, parametre: '', valeur: '', date:''});
  }

  deleteDiv(id: number) {
    this.divs = this.divs.filter(div => div.id !== id);
  }
  readonly dialog = inject(MatDialog);
  openDialog_genererGraphe(): void {
  
    const dialogRef = this.dialog.open(GenererGraphe, {
      width: '80vw',
      height: 'auto',
      maxWidth: '80vw',
      data: {
        id_dpi: this.data.id_dpi,
      },
    });
  }
  
 
  enregistrer() {
    this.isDisable = false;
    const mesures = this.divs.map(div => {
      // Find the ID for the entered parameter name
      const matchedParam = this.params.find(param => param.name === div.parametre);
      if (!matchedParam) {
        alert(`Paramètre "${div.parametre}" non valide`);
        throw new Error(`Invalid paramètre: ${div.parametre}`);
      }
  
      return {
        "id-mesure": matchedParam.id, // Send the ID of the parameter
        "valeur_mesure": div.valeur,
        "date_mesure": div.date,
      };
    });
  
    const bilan_id = this.data.bilan_id;
    const updateData = {
      bilan_id: bilan_id, // Include the bilan_id passed from the parent
      laborantin_id: 1,
      mesure: mesures,
    };
  
    this.laborantinUpdate.postBilanResultat(updateData).subscribe({
      next: response => {
        console.log("L'ajout des paramètres a réussi", response);
        // Show a success message (optional), but keep the dialog open
        alert("Les données ont été enregistrées avec succès.");
      },
      error: err => {
        console.log("L'ajout des paramètres a échoué", err);
        console.error("Failed to send data:", err.error); // Log the error body
      },
    });
  }
  
}


interface Graphe{
  nom : string;
  valAnc : number;
  valNouv : number
}
@Component({
  selector: 'dialog-generer-graphe',
  templateUrl: 'dialog-generer-graphe.html',
  imports: [
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
    MatExpansionModule,
    CommonModule,

  ],
})




export class GenererGraphe implements OnInit{
  readonly dialogRef = inject(MatDialogRef<GenererGraphe>);
  readonly data = inject(MAT_DIALOG_DATA);


   graphe : Graphe[]=[]
   valAnc: any[] = [];
   valNouv: any[] = [];
   chart: any;

   constructor(private drawingGrapheService: LaborantinService) {
    Chart.register(
      CategoryScale, 
      LinearScale,    
      BarElement,     
      Title,          
      Tooltip,       
      Legend,
      BarController        
    );
  }

  ngOnInit(): void {
    this.fetchGraphData(this.data.id_dpi);
  }


  fetchGraphData(id_dpi: number): void {
    this.drawingGrapheService.getGraphData(id_dpi).subscribe({
      next: data => {
        // Process data directly into grapheObject
        data.parametres.forEach((param: any) => {
          const grapheObject: Graphe = {
            nom: param.nom, // Assuming param.nom exists
            valAnc: param.mesurebefore, // Directly use mesurebefore
            valNouv: param.mesureafter, // Directly use mesureafter
          };
          this.graphe.push(grapheObject); // Push directly to graphe array
        });
  
        // Create the chart with the processed data
        this.createChart();
      },
      error: err => {
        console.error('Error fetching graph data', err);
      }
    });
  }
  createChart() {
    const labels = this.graphe.map(item => item.nom);
    console.log(labels);
    const valAnc = this.graphe.map(item => item.valAnc);
    console.log(valAnc);
    const valNouv = this.graphe.map(item => item.valNouv);
    console.log(valNouv);

    const ctx = document.getElementById('barChart') as HTMLCanvasElement;  
    if (ctx) {
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Ancien',
              data: valAnc,
              backgroundColor: 'rgb(33, 150, 243)',
              
              borderWidth: 1,
              barThickness: 'flex', 
              maxBarThickness: 50,
            },
            {
              label: 'Nouveau',
              data: valNouv,
              backgroundColor: 'rgb(76, 175, 80)',
              
              borderWidth: 1,
              barThickness: 'flex', 
              maxBarThickness: 50,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              stacked: true,
              grid: {
                display: false, 
              }, 
            },

            y: {
              stacked: true,
            },
          },
        },
      });
    } else {
      console.error('Canvas element not found!');
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
  
}